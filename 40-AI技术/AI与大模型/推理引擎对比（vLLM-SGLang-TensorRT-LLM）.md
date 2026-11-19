---
title: 推理引擎对比（vLLM/SGLang/TensorRT-LLM）
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI与大模型
  - 推理引擎
  - 模型部署
aliases:
  - 推理引擎对比
  - vLLM-SGLang-TensorRT-LLM 对比
source: 网络资料整理
---

# 推理引擎对比（vLLM/SGLang/TensorRT-LLM）

> [!摘要]
> 本文对比生产环境三大主流 LLM 推理引擎 **vLLM、SGLang、TensorRT-LLM** 的定位、核心机制、适用负载与选型取舍，并给出可直接运行的部署、调用与压测示例。核心结论：**没有通用最优解**——通用高吞吐与生态广度选 vLLM，高前缀复用的 Agent/RAG 负载选 SGLang，NVIDIA 全栈深度优化选 TensorRT-LLM，最终必须用贴近真实负载的压测数据做决定。文中版本号均来自 2026-11 调研时点的官方发布，落地前请回官方仓库复核。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本号与日期均来自 2026-11 检索时点的官方发布页面，框架迭代极快，使用前请以官方仓库当日状态复核。

| 引擎 | 最新版本 | 发布日期 | 关键变化 | 来源 |
| --- | --- | --- | --- | --- |
| vLLM | v0.34.0 | 2026-11-15 | 可扩展 KV cache **默认开启**；Model Runner V2 成为唯一 GPU 运行器（V1 已移除）；默认 block size 改为 64；默认 CUDA 13.0；Blackwell 与 MI355X 上解码/吞吐大幅提速（Step5 在 GB200 上解码最高 1.95×） | [vLLM Releases](https://github.com/vllm-project/vllm/releases/tag/v0.34.0) |
| SGLang | v0.5.23 | 2026-10-30 | 1007 个 PR、257 位贡献者；新增 Muse Spark Open、Beam-1.0、MiniMax-M3.1-Flash、MiniCPM-V 4.7 等模型；DeepSeek-V4.1 在 GB300 上 prefill 吞吐最高 1.5×；低延迟 megakernel/monokernel 插件使单用户解码最高提升 44%（GB300）/75%（MI350X）；支持在量化 MoE 模型上服务 LoRA adapter；可通过 SGLang-TorchTPU 运行于 Google TPU7x；**自 v0.5.22 起要求 Python 3.11+** | [SGLang Releases](https://github.com/sgl-project/sglang/releases) |
| TensorRT-LLM | v1.4.0rc4（**预发布**）；稳定线文档为 1.2.0 | 2026-11-15 / 2026-03-11 | Modeling V2 目标扩展至 GLM-5.2 / GLM-5.3-Flash / MiniMax-M3 / Qwen3.8-Flash-Next 的 NVFP4；新增 KVCM V2 稀疏 KV offload、DSpark 置信度调度、Gumbel-max 文本水印；**KV cache manager V2 成为推荐架构，V1 进入弃用流程** | [TensorRT-LLM Releases](https://github.com/NVIDIA/TensorRT-LLM/releases)、[1.2.0 Release Notes](https://nvidia.github.io/TensorRT-LLM/1.2.0/release-notes.html) |

> [!warning] 预发布与稳定版的区分
> TensorRT-LLM **v1.4.0rc4 是预发布版本，不能写成正式稳定版**。写作与选型时务必注明这一点，稳定线文档为 1.2.0。

## 二、基础概念

**推理引擎**负责把训练好的模型权重加载进 GPU，按请求完成自回归解码，并以 HTTP 接口（通常为 OpenAI 兼容协议）对外提供服务。它与训练框架（PyTorch、Megatron 等）分工不同：训练解决"把模型学出来"，推理解决"把模型跑得快、跑得稳、撑得住并发"。

评估推理引擎，先看四个维度：

- **吞吐（Throughput）**：单位时间处理的 token 数或请求数，决定单卡/单节点能服务多少用户。
- **延迟（Latency）**：拆分为 **TTFT（首 token 时间，主要由 prefill 决定）** 与 **TPOT（每 token 时间，主要由 decode 决定）**，交互式场景更看重延迟而非纯吞吐。
- **显存占用**：权重占用 + **KV cache** 占用，后者随并发与上下文长度增长。
- **工程能力**：OpenAI 兼容接口、并行策略（TP/PP/EP/CP）、前缀缓存、结构化输出、可观测性等。

三者定位一句话概括：**vLLM 是通用生产默认，SGLang 主打前缀复用，TensorRT-LLM 主打 NVIDIA 全栈深度优化**。

## 三、核心机制

三者都基于"自回归解码 + KV cache"范式，共享连续批处理、分块预填充、前缀缓存、投机解码等手段，差异在于各自把资源压向了不同的方向。

### 3.1 vLLM：PagedAttention + 连续批处理

- **PagedAttention**：把 KV cache 像操作系统管理内存一样按块（block）分页存放，避免为每条请求预留整段连续显存，显著降低碎片与浪费。v0.34.0 默认 block size 已改为 64，**可扩展 KV cache 默认开启**（按预热后实际空闲显存动态定容，例如 MiniMax-M3 在 H200 上从 433k 提升到 672k token）。
- **连续批处理（Continuous Batching）**：请求到达即动态入批，不必等整批补齐，最大化 GPU 利用率，是其高吞吐的来源。
- **配套能力**：分块预填充、前缀缓存、结构化输出、OpenAI 兼容 API，支持张量/流水线/专家/上下文并行（TP/PP/EP/CP）。v0.34.0 中 **Model Runner V2 已成为唯一 GPU 运行器（V1 已移除）**。

### 3.2 SGLang：RadixAttention 前缀复用

- **RadixCache（前缀树）**：把系统提示、RAG 检索结果、工具定义等**公共前缀**组织成前缀树，相同前缀只计算一次，后续请求直接命中，从根源上省掉重复 prefill。
- **适用负载**：长系统提示、高前缀重叠的 Agent / RAG 场景收益最明显，这是它相对 vLLM 的核心优势。
- **配套能力**：v0.5.23 支持在**量化 MoE 模型上服务 LoRA adapter**，可通过 SGLang-TorchTPU 运行于 Google TPU7x。

### 3.3 TensorRT-LLM：NVIDIA 全栈深度优化

- **全栈调优**：从算子、kernel 到 KV cache 管理全链路针对 NVIDIA 硬件优化，对 **Blackwell（GB200/GB300）** 与 **MoE** 模型最成熟。
- **KV cache 管理**：**KV cache manager V2 为推荐架构，V1 进入弃用流程**；新增 **KVCM V2 稀疏 KV offload**，进一步降低显存压力。
- **代价**：需要用其工具链编译构建（trtllm 构建流程），搭建与重建成本高于 vLLM，且生态相对封闭。

> [!note] 关键认知
> **KV cache 与权重量化是两条线**。只量化权重不等于整体显存下降——生产批规模下，KV cache 本身可能占到 10–30GB，必须单独评估，并可通过 KV 量化（如 NVFP4）与前缀复用来压缩。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境准备

```bash
# 检查 Python 版本（SGLang 自 v0.5.22 起要求 Python 3.11+）
python --version

# 按引擎安装（按需取舍，避免依赖冲突）
pip install "vllm==0.34.0"
pip install "sglang==0.5.23"
pip install "tensorrt-llm"
```

### 4.2 用 vLLM 部署服务

```bash
vllm serve Qwen/Qwen3.5-397B-A17B \
  --tensor-parallel-size 4 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --enable-prefix-caching
```

> [!info] 常用参数
> `--tensor-parallel-size` 控制张量并行度；`--max-model-len` 决定最大上下文；`--gpu-memory-utilization` 控制 KV cache 可用显存比例；`--enable-prefix-caching` 开启前缀缓存。vLLM 以 `vllm serve` 为标准启动方式，旧的 `python -m vllm.entrypoints.openai.api_server` 已弃用。

### 4.3 用 SGLang 部署服务

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen3.5-397B-A17B \
  --tp-size 4 \
  --context-length 32768 \
  --mem-fraction-static 0.90
```

### 4.4 用 TensorRT-LLM 部署服务

```bash
# TensorRT-LLM 需先按官方流程构建 engine，再用 trtllm-serve 启动
trtllm-serve \
  --model Qwen/Qwen3.5-397B-A17B \
  --tp-size 4 \
  --kv_cache_config v2 \
  --host 0.0.0.0 --port 8000
```

> [!warning] 构建成本
> TensorRT-LLM 的 engine 需针对目标 GPU 型号编译，更换硬件或版本后通常要重建，生产中应预留构建与版本锁定成本。

### 4.5 统一 OpenAI 兼容调用

```python
from openai import OpenAI

# 三者均暴露 OpenAI 兼容接口，只需替换 base_url
for name, base_url in [
    ("vLLM", "http://localhost:8000/v1"),
    ("SGLang", "http://localhost:8000/v1"),
    ("TensorRT-LLM", "http://localhost:8000/v1"),
]:
    client = OpenAI(base_url=base_url, api_key="EMPTY")
    resp = client.chat.completions.create(
        model="Qwen/Qwen3.5-397B-A17B",
        messages=[{"role": "user", "content": "用一句话介绍推理引擎"}],
        temperature=0.2,
    )
    print(name, "->", resp.choices[0].message.content[:40])
```

### 4.6 压测：用真实负载验证选型

```python
import time
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

def bench(prompt: str, rounds: int = 20) -> None:
    t0 = time.perf_counter()
    for _ in range(rounds):
        start = time.perf_counter()
        stream = client.chat.completions.create(
            model="Qwen/Qwen3.5-397B-A17B",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        first = None
        n = 0
        for chunk in stream:
            if first is None and chunk.choices and chunk.choices[0].delta.content:
                first = time.perf_counter() - start
            n += 1
        t0 = time.perf_counter()
    print(f"TTFT≈{first * 1000:.1f}ms, 平均 TPOT≈{(time.perf_counter() - t0) / rounds * 1000:.1f}ms")

bench("请详细解释什么是 KV cache，并给出优化手段。")
```

> [!tip] 选型铁律
> **性能数字高度依赖负载形状，脱离负载谈吞吐没有意义。** 请用贴近自身真实负载（并发数、输入/输出长度、前缀重叠度、模型类型）的压测数据做选型，而不是照搬榜单数字。

## 五、最佳实践与常见坑

**选型经验（经验性建议，非绝对结论）**：

- **高前缀重叠**（Agent、RAG、固定长系统提示）→ 优先 **SGLang**，前缀复用收益最大。
- **通用高吞吐、模型覆盖广、生态中立** → 优先 **vLLM**，生产默认选择。
- **NVIDIA 全栈深度优化、GB200/GB300 等 Blackwell 硬件、MoE 模型** → 优先 **TensorRT-LLM**。

**常见坑**：

| 现象 / 问题 | 原因 | 对策 |
| --- | --- | --- |
| 显存不足（OOM） | 只算权重、忽略 KV cache 膨胀 | 分开估算权重与 KV cache；降低 `max-model-len`、调低 `gpu-memory-utilization`、启用 KV 量化与前缀缓存 |
| 升级后启动失败 | 破坏性变更 | vLLM Model Runner V1 已移除、默认 block size 64、默认 CUDA 13.0；SGLang 要求 Python 3.11+；TensorRT-LLM KV cache manager V1 已弃用。**生产锁定版本** |
| 把 RC 当稳定版 | 版本语义不清 | TensorRT-LLM v1.4.0rc4 为预发布，稳定线为 1.2.0 |
| 吞吐不符合预期 | 负载形状与压测条件不符 | 用真实负载压测，记录 TTFT/TPOT/吞吐，而非照搬他人数字 |
| 量化后显存仍高 | 混淆权重量化与整体显存 | KV cache 独立于权重量化，需单独优化 |
| 多模型 / 多节点不稳定 | 缺乏版本隔离与编排 | 按模型与流量拆分实例，做负载均衡与版本隔离；MoE 模型考虑专家负载均衡（EPLB）与 PD 分离 |

> [!warning] 版本风险提示
> 推理引擎迭代极快，vLLM 已移除 Model Runner V1、TensorRT-LLM 的 KV cache manager V1 进入弃用流程，升级前务必核对自身依赖与调用方，避免升级后接口不兼容。

## 六、核心要点速查

1. 三大引擎都基于"自回归解码 + KV cache"范式，共享连续批处理、分块预填充、前缀缓存、投机解码等手段。
2. **vLLM**：PagedAttention + 连续批处理，显存利用率高、模型覆盖广、生态中立，是通用生产默认。
3. **SGLang**：RadixAttention 前缀树复用，长系统提示与高前缀重叠的 Agent/RAG 负载优势明显。
4. **TensorRT-LLM**：NVIDIA 全栈深度优化，对 Blackwell（GB200/GB300）与 MoE 最成熟，但构建成本高、生态封闭。
5. 选型三句话：高前缀重叠选 SGLang，通用高吞吐选 vLLM，NVIDIA 全栈深度优化选 TensorRT-LLM。
6. KV cache 与权重量化是两条线，生产批规模下 KV cache 可能占 10–30GB，必须单独评估。
7. vLLM v0.34.0：可扩展 KV cache 默认开启、Model Runner V2 唯一运行器、默认 block size 64、默认 CUDA 13.0。
8. SGLang v0.5.23：自 v0.5.22 起要求 Python 3.11+，支持量化 MoE 上的 LoRA 服务。
9. TensorRT-LLM 的 v1.4.0rc4 为预发布，KV cache manager V2 推荐、V1 弃用。
10. 延迟拆成 TTFT（prefill）与 TPOT（decode），交互式场景优先看延迟而非纯吞吐。
11. 选型铁律：用贴近真实负载的压测数据说话，脱离负载谈吞吐没有意义。
12. 生产建议锁定版本、保留回滚能力，升级前核对破坏性变更。

## 七、学习资源

1. [vLLM Releases（官方 GitHub）](https://github.com/vllm-project/vllm/releases)
2. [vLLM v0.34.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.34.0)
3. [SGLang Releases（官方 GitHub）](https://github.com/sgl-project/sglang/releases)
4. [TensorRT-LLM Releases（官方 GitHub）](https://github.com/NVIDIA/TensorRT-LLM/releases)
5. [TensorRT-LLM 1.2.0 Release Notes（官方文档）](https://nvidia.github.io/TensorRT-LLM/1.2.0/release-notes.html)
6. [SGLang vs vLLM vs TensorRT-LLM（选型对比）](https://www.truefoundry.io/blog/sglang-vs-vllm-vs-tensorrt-llm)
7. [PyTorch 2.15 Release Blog（官方）](https://pytorch.org/blog/pytorch-2-15-release-blog/)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[40-AI技术]]
- [[大模型基础核心要点]]
- [[LLM应用开发-RAG与Agent]]
- [[AI学习路径]]

## 九、变更记录

- 2026-11-19：首次创建。
