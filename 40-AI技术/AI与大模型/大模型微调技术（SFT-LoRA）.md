---
title: 大模型微调技术（SFT/LoRA）
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI与大模型
  - 大模型
  - 微调
  - SFT
  - LoRA
  - PEFT
aliases:
  - 大模型微调
  - SFT与LoRA
source: 网络资料整理
---

# 大模型微调技术（SFT/LoRA）

> [!摘要] 摘要
> 本文档系统讲解大模型微调中的两条核心路线：**监督微调（SFT）**与**参数高效微调（LoRA/QLoRA）**，覆盖基础概念、数学机制、完整实践步骤、最佳实践与常见坑，并汇总截至 2026-11 的官方版本动态。适合已掌握 Transformer 基础、需要把微调真正落地到项目中的工程师。本知识点是 [[AI与大模型-从入门到精通]] 进阶篇「微调机制」的展开，与 RAG、推理部署构成模型落地的完整链条。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本号与日期均来自 2026-11 检索时点的官方发布信息，框架迭代极快，实际使用时请以官方仓库当日状态复核。

- **PEFT v0.21.3 为最新版本**：v0.21.0 新增 Riemannian 预条件 LoRA 优化器、KaSA、Super-Tuning、ShadowPEFT 等方法；v0.21.1 起支持张量并行（Tensor Parallel）；v0.21.2 修复了 Transformers ≥ 5.18 的 encoder-decoder 兼容问题。LoRA 相关工具链仍在快速演进。来源：[Hugging Face PEFT Releases](https://github.com/huggingface/peft/releases)
- **TRL v1.17.0（2026-11-08）**：展示了对 **Mistral-Large-4-1T-A52B**（1T 总参 / 52B 激活，FP8）在单节点 8×B300 上做 **LoRA SFT**（约 142 GiB/卡），说明 LoRA/PEFT 已能适配超大规模 MoE 模型；AsyncGRPO 默认启用 score centering（`score_centering=True`）；修正了 top-k/top-p 过滤下的重要性采样偏差；新增 AMD Instinct GPU 支持。来源：[TRL v1.17.0 Release Notes](https://github.com/huggingface/trl/releases/tag/v1.17.0)
- **Hugging Face Transformers 已进入 v5 世代**：当前最新 v5.22.2，其中 v5.20.0（2026-10-14）引入 UltraBERT 系列等。微调脚本与 PEFT 均需关注其版本兼容。来源：[Hugging Face Transformers Releases](https://github.com/huggingface/transformers/releases/tag/v5.20.0)
- **训练底座 PyTorch 2.15.0（2026-10-26）**：默认 wheel 迁移到 CUDA 13.2（另提供 CUDA 13.4 wheel），要求 Python 3.10+。来源：[PyTorch 2.15 Release Blog](https://pytorch.org/blog/pytorch-2-15-release-blog/)
- **量化基座 bitsandbytes 0.49.2（2026-10-26）**：CPU 4bit 性能显著优化，新增 ROCm CDNA `blocksize=64` 支持，是 QLoRA 的常用底座。来源：[bitsandbytes Releases](https://github.com/bitsandbytes-foundation/bitsandbytes/releases)
- **多 LoRA 服务侧**：SGLang v0.5.23（2026-10-30）支持**在量化 MoE 模型上服务 LoRA adapter**；vLLM 亦支持多 LoRA，便于按租户/任务动态切换适配器。来源：[SGLang Releases](https://github.com/sgl-project/sglang/releases)

## 二、基础概念

**微调（Fine-tuning）** 是在预训练基座模型之上，用领域数据继续训练，让模型学会特定任务、格式或风格，而不必从零训练。大模型工程中通常遵循三阶段流程：

1. **预训练（Pre-Training）**：在海量无标注/弱标注数据上做下一个 token 预测，获得通用语言能力，成本最高。
2. **监督微调（SFT）**：用高质量的「指令—回答」样本训练，让模型学会按指定格式、语气和任务要求作答，即**学格式、学任务**。
3. **偏好优化（DPO/PPO/GRPO 等）**：用偏好数据（更好/更差的成对回答）让模型学会**取舍与价值对齐**。

> [!note] 概念边界
> **SFT 与偏好优化职责不同**：SFT 主要解决「怎么回答」，偏好优化解决「哪个回答更好」。不要用 SFT 去硬扛价值观对齐，也不要期待偏好优化替代格式学习。

**LoRA（Low-Rank Adaptation）** 是参数高效微调（PEFT）的代表方法。它冻结基座模型的原始权重 $W$，只训练一对低秩适配矩阵，从而把需要更新的参数量从「全部」压缩到 **0.1%–3%** 量级，且**不增加推理成本**（训练后可将适配矩阵合并回原权重）。

**QLoRA** 在 LoRA 基础上叠加三项技术，进一步压低显存需求：

- **NF4 量化**：把基座权重量化到 4bit；
- **双重量化（Double Quantization）**：对量化常数再量化，进一步节省显存；
- **分页优化器（Paged Optimizer）**：借助统一内存避免显存尖峰导致的 OOM。

## 三、核心机制

**三种微调路线对比**

| 路线 | 训练参数 | 显存开销 | 效果上限 | 适用场景 |
| --- | --- | --- | --- | --- |
| 全量微调 | 全部参数 | 最大 | 最高 | 算力充裕、追求极致效果 |
| LoRA | 低秩矩阵（约 0.1%–3%） | 中等 | 稳定、接近全量 | 通用任务、多任务/多租户 |
| QLoRA | 低秩矩阵 + 量化基座 | 最低 | 略低于 LoRA | 显存受限、消费级显卡 |

**LoRA 的数学形式**

原始权重 $W \in \mathbb{R}^{d \times k}$ 被冻结，引入两个小矩阵 $B \in \mathbb{R}^{d \times r}$、$A \in \mathbb{R}^{r \times k}$，前向计算变为：

$$
h = Wx + \Delta W x = Wx + \frac{\alpha}{r} B A x
$$

其中 $r$（rank）是低秩维度，$\frac{\alpha}{r}$ 是缩放系数。训练结束后可直接把 $BA$ 加到 $W$ 上合并，推理时**没有额外开销**。

**LoRA 关键参数**

| 参数 | 含义 | 常见取值 |
| --- | --- | --- |
| `r`（rank） | 低秩矩阵维度，越大表达力越强、参数越多 | 8、16、32、64 |
| `alpha`（α） | 缩放系数，与 r 共同决定有效学习率 | 通常取 r 的 1–2 倍 |
| `target_modules` | 需要插入 LoRA 的模块，如 `q_proj`、`v_proj`、`gate_proj` | 按模型结构选择，务必覆盖关键投影 |
| `dropout` | 防过拟合 | 0.05–0.1 |
| `lr` | 学习率 | 1e-4 ~ 5e-5（LoRA 通常高于全量微调） |
| `batch_size` / `epochs` | 批大小与训练轮数 | 按数据量与显存权衡，一般 2–3 轮 |

> [!warning] 参数关系
> `alpha` 与 `r` 必须配套调整：只增大 `r` 而不调 `alpha`，等效于缩小了适配强度，效果可能不升反降。实践中常保持 `alpha = r` 或 `alpha = 2r` 起步。

**SFT 与偏好优化的机制差异**：SFT 直接对「标准答案」做监督学习，损失函数是标准交叉熵；偏好优化（如 DPO）则构造偏好对，用对比损失拉近优选回答、推远劣选回答。2025 年起以可验证奖励为代表的 **GRPO** 成为主流对齐路线，TRL v1.17.0 中 AsyncGRPO 已默认启用 score centering 来修正 FP8 采样器下的目标退化。

## 四、实践步骤（含代码/命令示例）

### 1. 环境准备

```bash
# 建议 Python 3.10+（部分推理引擎已要求 3.11+）
python --version

# 安装微调核心依赖（版本以当日官方仓库为准）
pip install "transformers>=5.20.0" "peft>=0.21.0" "trl>=1.17.0"
pip install "accelerate" "datasets" "bitsandbytes>=0.49.2"
```

### 2. 准备数据（JSONL）

SFT 数据通常是「指令—回答」格式，例如 `sft_data.jsonl`：

```json
{"instruction": "把下面这句话翻译成英文。", "input": "人工智能正在改变软件开发。", "output": "Artificial intelligence is transforming software development."}
{"instruction": "总结下面这段文字的要点。", "input": "（正文内容……）", "output": "要点如下：1…… 2……"}
```

数据质量比数量更关键：**去重、去噪声、保证格式统一、人工抽检**，避免模型学到错误格式或领域偏见。

### 3. LoRA 微调（Python）

使用 TRL 的 SFT 训练器配合 PEFT 的 LoRA 配置：

```python
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-8B"  # 换成目标基座，显存不足可换更小模型

# 1) 加载模型与分词器
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# 2) LoRA 配置
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)

# 3) 训练配置
sft_config = SFTConfig(
    output_dir="./output/qwen3-sft-lora",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    bf16=True,
)

# 4) 加载数据并启动训练
dataset = load_dataset("json", data_files="sft_data.jsonl", split="train")
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=sft_config,
    peft_config=lora_config,
    formatting_func=lambda example: (
        f"### 指令:\n{example['instruction']}\n\n"
        f"### 输入:\n{example.get('input', '')}\n\n"
        f"### 回答:\n{example['output']}"
    ),
)
trainer.train()
trainer.save_model()  # 保存 adapter 权重
```

### 4. 显存不足时改用 QLoRA

只需把模型加载改为 4bit，并加上分页优化器配置：

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=bnb_config)
```

### 5. 训练超参（YAML 参考）

```yaml
# sft_lora_args.yaml
r: 16
lora_alpha: 32
lora_dropout: 0.05
target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]

num_train_epochs: 3
per_device_train_batch_size: 4
gradient_accumulation_steps: 4
learning_rate: 2.0e-4
lr_scheduler_type: cosine
warmup_ratio: 0.03
logging_steps: 10
save_strategy: epoch
bf16: true
gradient_checkpointing: true
```

> [!tip] 小技巧
> 显存不足优先开 `gradient_checkpointing` 并降低 `per_device_train_batch_size`、增大 `gradient_accumulation_steps`，保持等效全局批大小不变。

### 6. 合并 adapter 并部署

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model = PeftModel.from_pretrained(base, "./output/qwen3-sft-lora")
merged = model.merge_and_unload()
merged.save_pretrained("./qwen3-sft-merged")
```

## 五、最佳实践与常见坑

**最佳实践**

- **先评估、后调优**：先定义成功指标与测试集（准确率、格式合规、领域指标），再迭代训练，避免「感觉变好了」。
- **数据质量优先**：SFT 效果的上限基本由数据决定，务必做清洗、去重、格式统一与人工抽检。
- **参数与算力匹配**：小任务用小 `r`（8–16）；任务复杂、领域差异大再加大 `r` 与 `target_modules`。
- **控制轮数与学习率**：LoRA 训练 2–3 轮通常足够，学习率高于全量微调，过高易过拟合、过低学不动。
- **保留基线对照**：用未微调模型跑同一套测试集，量化微调带来的真实增益。
- **生产锁版本**：PEFT/TRL/Transformers 迭代快且存在破坏性变更，生产环境应**锁定版本**并记录复现配置。

**常见坑**

| 现象 | 可能原因 | 对策 |
| --- | --- | --- |
| 显存溢出（OOM） | 全量微调、序列过长、批过大 | 改用 LoRA/QLoRA、开启梯度检查点、降低上下文长度 |
| 模型「学废了」、泛化变差 | 训练轮数过多、学习率过高、数据质量差 | 减少 epoch、调低学习率、换更干净数据 |
| 格式学不到位 | 数据格式不一致、`target_modules` 未覆盖关键投影 | 统一模板、补齐目标模块、必要时提高 `r` |
| 合并后效果异常 | 合并方式或基座版本不一致 | 用同版本基座 `merge_and_unload()`，核对 tokenizer |
| 训练慢 | 未用 FlashAttention、未启用 bf16 | 开启 `bf16`/FlashAttention、调整并行策略 |
| 服务切换异常 | 多 LoRA 配置与引擎不匹配 | 确认引擎支持该模型结构，SGLang 可在量化 MoE 上服务 LoRA |

> [!warning] 版本风险
> PEFT、TRL、Transformers 与推理引擎版本间存在兼容约束（如 PEFT v0.21.2 修复了 Transformers ≥ 5.18 的 encoder-decoder 兼容问题）。升级前务必核对依赖矩阵，生产环境锁定版本。

## 六、核心要点速查

1. 大模型三阶段：预训练 → SFT（学格式/任务）→ 偏好优化（学取舍），二者职责不可互相替代。
2. LoRA 冻结原权重，只训练低秩矩阵 $W' = W + BA$，更新参数约 0.1%–3%，**不增加推理成本**。
3. QLoRA = LoRA + NF4 量化 + 双重量化 + 分页优化器，是低显存场景的首选。
4. LoRA 关键参数：`r`、`alpha`、`target_modules`、`dropout`、学习率、批大小、轮数，`alpha` 需与 `r` 配套。
5. SFT 数据质量决定效果上限：清洗、去重、统一格式、人工抽检缺一不可。
6. 先评估后调优：建立测试集、指标与基线，量化每次改动的真实收益。
7. 显存不足优先量化与梯度检查点，而非盲目降低任务规模。
8. 训练后用 `merge_and_unload()` 合并 adapter，推理阶段无额外开销。
9. 截至 2026-11：PEFT 最新 v0.21.3，TRL 最新 v1.17.0，Transformers 进入 v5 世代。
10. 框架迭代快，版本号以官方仓库为准，生产环境务必锁定版本。

## 七、学习资源

1. [Hugging Face PEFT Releases（官方仓库）](https://github.com/huggingface/peft/releases)
2. [TRL v1.17.0 Release Notes（官方仓库）](https://github.com/huggingface/trl/releases/tag/v1.17.0)
3. [Hugging Face Transformers Releases（官方仓库）](https://github.com/huggingface/transformers/releases)
4. [bitsandbytes Releases（官方仓库）](https://github.com/bitsandbytes-foundation/bitsandbytes/releases)
5. [SGLang Releases（官方仓库）](https://github.com/sgl-project/sglang/releases)
6. [阿里云 PAI 大模型微调指引（官方文档）](https://www.alibabacloud.com/help/zh/pai/llm-fine-tuning-experience)
7. [vLLM Releases（官方仓库）](https://github.com/vllm-project/vllm/releases)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[自然语言处理-BERT模型详解]]
- [[深度学习-PyTorch入门]]
- [[机器学习-机器学习基础入门总结]]
- [[40-AI技术]]

## 九、变更记录

- 2026-11-19：首次创建。
