---
title: Transformer架构详解
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI/大模型
  - Transformer
  - 自注意力
  - 模型架构
aliases:
  - Transformer架构
  - Transformer架构详解
source: 网络资料整理
---

# Transformer架构详解

> [!摘要] 本文系统讲解 **Transformer 架构**：从 2017 年原始论文的 encoder-decoder 结构出发，拆解自注意力、多头注意力、前馈网络、残差与位置编码等核心机制，并对比现代大语言模型（LLM）常用的 decoder-only + RoPE/RMSNorm/SwiGLU/GQA-MLA 变体，最后给出可运行的代码与部署实践。定位为 [[AI与大模型-从入门到精通]] 体系下的模型基础篇，帮助读者建立"能读懂结构、能动手实现、能避免常见坑"的完整认知。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本信息来自调研时点（2026-11）的官方来源，框架迭代极快，写作与引用前请以官方仓库当日状态复核；未核实的条目一律标注「以官方仓库为准」。

- **原始论文**：Vaswani 等《Attention Is All You Need》发表于 NeurIPS 2017（arXiv:1706.03762），首次提出**自注意力（Self-Attention）**、多头注意力与 encoder-decoder 结构，奠定现代 LLM 的架构基础。[Attention Is All You Need（arXiv）](https://arxiv.org/abs/1706.03762)
- **vLLM v0.34.0（2026-11-15）**：**可扩展 KV cache 默认开启**（按预热后实际空闲显存动态定容）；**Model Runner V2 成为唯一 GPU 运行器**（V1 被移除）；默认 block size 改为 64、默认 CUDA 13.0；Blackwell 与 MI355X 上解码/吞吐显著提速。该版本已支持稀疏 MLA、DeepSeek 系 MLA 与 KV 压缩等架构，可作为现代注意力变体在生产引擎中的落地佐证。[vLLM v0.34.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.34.0)
- **Hugging Face Transformers 进入 v5 世代**：当前最新为 v5.22.2，v5.20.0（2026-10-14）引入 UltraBERT 系列、MOSS-Transcribe-Diarize 等；v5 世代对注意力与 MoE 相关实现持续优化。[Hugging Face Transformers Releases](https://github.com/huggingface/transformers/releases/tag/v5.20.0)
- **PyTorch 2.15.0（2026-10-26）**：默认 wheel 迁移到 CUDA 13.2，要求 Python 3.10+，为 Transformer 训练/推理提供底层算子支持。[PyTorch 2.15 Release Blog](https://pytorch.org/blog/pytorch-2-15-release-blog/)
- **TensorRT-LLM v1.4.0rc4（预发布，2026-11-15）**：Modeling V2 目标扩展至 GLM-5.2、MiniMax-M3 等模型的 NVFP4；KV cache manager V2 成为推荐架构，V1 进入弃用流程。稳定线文档为 1.2.0（2026-03-11）。[TensorRT-LLM Releases](https://github.com/NVIDIA/TensorRT-LLM/releases)

## 二、基础概念

- **什么是 Transformer**：一种完全基于**自注意力机制**的序列建模架构，抛弃了 RNN/CNN 的循环与局部卷积，直接建模序列中任意位置间的依赖关系，便于并行计算、捕捉长程依赖。
- **整体数据流**：`文本 → tokenization → 词嵌入（Embedding） → 位置编码 → 若干 Transformer 层（注意力 + 前馈） → 输出层 → 下一个 token 预测`。LLM 的生成是**自回归**的：逐 token 预测下一个 token，再拼接输入继续预测。
- **两种主流结构**：
  - **Encoder-Decoder**（2017 原始形态）：编码器负责双向理解输入，解码器负责自回归生成，典型如 BERT/T5。
  - **Decoder-only**（现代 LLM 主流）：仅保留带因果掩码的解码器，兼顾理解与生成，是 GPT、Qwen、Llama 等的通用底座。
- **Transformer 层的两大子层**：每一层都包含**注意力子层**（捕捉词间关系）与**前馈网络子层**（逐位置做非线性变换），二者均套**残差连接 + 层归一化**。

## 三、核心机制

**1. 缩放点积注意力**

输入经线性投影得到查询（Query）、键（Key）、值（Value），核心公式：

$$\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V$$

- 点积衡量 query 与每个 key 的相关性，除以 $\sqrt{d_k}$ 防止内积过大导致 softmax 梯度消失。
- 结果对 value 加权求和，即为该位置的输出表示。

**2. 多头注意力（Multi-Head Attention）**

将 Q/K/V 投影到多个子空间并行计算注意力，再拼接，使模型同时捕捉位置、语法、语义等不同类型的依赖关系，避免单一注意力子空间表达力不足。

**3. 前馈网络（FFN）**

每个位置独立地经过两层线性变换 + 非线性激活（原始论文用 ReLU；现代 LLM 普遍改用 **SwiGLU**），提供模型的非线性与表达能力。

**4. 残差连接与归一化**

子层输出与输入相加（残差）保证梯度稳定；原始 Transformer 用 LayerNorm，现代 LLM 常用 **RMSNorm**（更省算力、效果稳定）。

**5. 位置编码**

注意力本身不包含顺序信息，必须注入位置。原始 Transformer 使用**正余弦函数**；现代 LLM 主流采用 **RoPE（旋转位置编码）**，将相对位置信息编码进 Q/K，长上下文与外推能力更好。

**6. KV Cache**

自回归解码时缓存历史 token 的 K/V，避免每步重复计算，用显存换算力，是解码加速的核心。其显存随序列长度线性增长，是推理优化的关键抓手。

**原始 Transformer 与现代 LLM 的差异**

| 维度 | 原始 Transformer（2017） | 现代 LLM（主流） |
| --- | --- | --- |
| 结构 | encoder-decoder | decoder-only（因果掩码） |
| 位置编码 | 正余弦函数 | RoPE |
| 归一化 | LayerNorm（子层前置/后置） | RMSNorm |
| 前馈网络 | 两层 ReLU | SwiGLU |
| 注意力 | 多头全注意力 | GQA / MLA 等稀疏/分组变体 |

## 四、实践步骤（含代码/命令示例）

**1. 环境准备**

```bash
# 建议 Python 3.11+（SGLang 自 v0.5.22 起要求 Python 3.11+）
python --version

# 安装模型库与推理引擎
pip install "transformers>=5.0" "torch>=2.15"
pip install "vllm>=0.34.0"
```

**2. 用 Hugging Face Transformers 跑通一个 Transformer**

```python
import torch
from transformers import AutoTokenizer, AutoModel

# 加载预训练模型：BERT 为 encoder，GPT 系为 decoder
name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModel.from_pretrained(name)
model.eval()

# tokenization -> embedding -> 前向
inputs = tokenizer("Hello, Transformer!", return_tensors="pt",
                   padding=True, truncation=True)
with torch.no_grad():
    outputs = model(**inputs)

hidden = outputs.last_hidden_state   # [batch, seq_len, hidden_size]
print(hidden.shape)
```

**3. 手写缩放点积注意力，理解内部计算**

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q, k, v, mask=None):
    # q/k/v: [batch, heads, seq, d_k]
    scores = torch.matmul(q, k.transpose(-2, -1)) / (q.size(-1) ** 0.5)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, v), weights

q = torch.randn(1, 4, 5, 64)
k = torch.randn(1, 4, 5, 64)
v = torch.randn(1, 4, 5, 64)
out, attn = scaled_dot_product_attention(q, k, v)
print(out.shape, attn.shape)   # [1,4,5,64] [1,4,5,5]
```

**4. 用 vLLM 部署 decoder-only 模型**

```bash
# vllm serve 是标准入口（旧入口 python -m vllm.entrypoints.openai.api_server 已弃用）
vllm serve Qwen/Qwen2.5-7B-Instruct \
  --served-model-name qwen2.5-7b \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.9

# 调用验证（OpenAI 兼容接口）
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5-7b","messages":[{"role":"user","content":"解释一下自注意力"}]}'
```

## 五、最佳实践与常见坑

- **不要把 2017 年结构直接等同于当今 LLM**：现代 LLM 多为 decoder-only + RoPE + RMSNorm + SwiGLU + GQA/MLA，概念边界要分清。
- **注意力复杂度为 O(n²)**：序列越长计算与显存开销越大，长上下文需配合 FlashAttention、分块预填充等优化。
- **KV cache 显存不可忽视**：仅压缩权重不等于整体显存下降，KV cache 在生产批规模下可能占用大量显存，需与权重量化分开评估，善用 vLLM 的可扩展 KV cache、前缀复用。
- **位置编码与训练长度强相关**：RoPE 有外推边界，随意超出训练上下文可能明显掉点，需明确模型上下文窗口。
- **归一化与残差不可随意删改**：破坏结构会导致训练不稳定，微调/定制结构时应保留核心骨架。
- **关注版本破坏性变更**：vLLM Model Runner V1 被移除、Transformers v5 世代迁移等均有破坏性变更，生产环境务必**锁定版本**并做回归验证。
- **版本号以官方仓库为准**：框架迭代极快，引用版本与特性时注明日期，避免把预发布版当成稳定版。

## 六、核心要点速查

1. Transformer 的核心是**自注意力**：用 Q/K/V 计算词与词相关性，多头并行捕捉多种关系。
2. 核心公式：`softmax(QKᵀ/√d_k)V`，除以 √d_k 防止 softmax 梯度消失。
3. 每层由**注意力 + 前馈网络**两个子层构成，均套**残差连接 + 归一化**。
4. 注意力不含顺序信息，必须注入**位置编码**：原始为正余弦，现代 LLM 主流为 **RoPE**。
5. **encoder-decoder** 是原始形态，现代 LLM 主流为 **decoder-only** + 因果掩码。
6. **KV Cache** 缓存历史 K/V，用显存换算力，是自回归解码加速与推理优化的关键。
7. 现代 LLM 常见改进：RMSNorm、SwiGLU、GQA/MLA，显著优于原始结构。
8. 解码是**自回归下一个 token 预测**，速度受 KV cache 与注意力计算制约。
9. 训练/推理前明确上下文窗口，位置编码外推有边界。
10. 版本迭代快，破坏性变更多，生产环境应锁定版本并回源核对。

## 七、学习资源

1. [Attention Is All You Need（原始论文，arXiv:1706.03762）](https://arxiv.org/abs/1706.03762)
2. [Hugging Face Transformers Releases（官方仓库）](https://github.com/huggingface/transformers/releases)
3. [vLLM v0.34.0 Release Notes（官方 GitHub）](https://github.com/vllm-project/vllm/releases/tag/v0.34.0)
4. [TensorRT-LLM Releases（官方 GitHub）](https://github.com/NVIDIA/TensorRT-LLM/releases)
5. [PyTorch 2.15 Release Blog（官方博客）](https://pytorch.org/blog/pytorch-2-15-release-blog/)
6. [Hugging Face Transformers 官方文档](https://huggingface.co/docs/transformers)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[自然语言处理-BERT模型详解]]
- [[AI学习路径]]

## 九、变更记录

- 2026-11-19：首次创建。
