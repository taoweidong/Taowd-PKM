---
title: 大模型训练体系（预训练/SFT/RLHF）
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI与大模型
  - LLM
  - 模型训练
  - SFT
  - RLHF
  - 对齐
aliases:
  - 大模型训练体系
  - 预训练-SFT-RLHF
source: 网络资料整理
---

# 大模型训练体系（预训练/SFT/RLHF）

> [!摘要] 摘要
> 本篇系统讲解大语言模型从「基础模型」到「可上线模型」的完整训练体系：**预训练（Pre-Training）** 在海量语料上学会语言与世界知识，**监督微调（SFT）** 教会模型按指令与格式作答，**偏好优化（RLHF/DPO/GRPO）** 把模型对齐到人类偏好与价值观。三者是一条递进且各有分工的流水线——预训练决定能力上限，SFT 决定「会做什么」，偏好优化决定「做得多符合期望」。定位在 [[AI与大模型-从入门到精通]] 体系中的「训练/对齐」环节，衔接 [[大模型-Transformer与注意力机制]] 与 [[大模型-训练范式与微调实战]]，适合需要理解训练全流程、准备动手做微调与对齐的工程师。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本号均来自 2026-11 检索时点的官方发布；训练框架迭代极快，写作与生产使用时请以官方仓库当日状态复核，无法确认处标注「以官方仓库为准」。

- **TRL v1.17.0（2026-11-08 发布）**：支持在**单节点 8×B300** 上对 **Mistral-Large-4-1T-A52B**（1T 总参 / 52B 激活，FP8）做 LoRA SFT，说明 PEFT 路线已能适配超大规模 MoE 基座；**AsyncGRPO 默认启用 score centering**（`score_centering=True`），并修正了 top-k/top-p 过滤下的重要性采样偏差；新增 AMD Instinct GPU 支持。来源：[TRL Releases](https://github.com/huggingface/trl/releases/tag/v1.17.0)
- **PEFT v0.21.3（当前最新，v0.21.x 线）**：v0.21.0 新增 Riemannian 预条件 LoRA 优化器、KaSA、Super-Tuning、ShadowPEFT 等方法；v0.21.2 修复 Transformers ≥5.18 的 encoder-decoder 兼容问题；v0.21.1 支持 Tensor Parallel。来源：[PEFT Releases](https://github.com/huggingface/peft/releases)
- **对齐技术路线**：从 PPO 到 DPO 及无参考变体，再到 **2025 年起以可验证奖励为代表的 GRPO 浪潮**，已成为后训练主流方向之一。阿里云 PAI 官方微调指引明确「预训练 → 监督微调（SFT）→ 偏好优化（DPO 等）」的标准流程与 SFT/DPO 策略选择。来源：[阿里云 PAI 大模型微调指引](https://www.alibabacloud.com/help/zh/pai/llm-fine-tuning-experience)、[TRL Releases](https://github.com/huggingface/trl/releases/tag/v1.17.0)
- **训练基座相关版本**：PyTorch **2.15.0（2026-10-26）**，默认 wheel 迁移到 CUDA 13.2，要求 Python 3.10+；Hugging Face Transformers 已进入 **v5 世代**，当前最新 **v5.22.2**（v5.20.0 于 2026-10-14 发布）；量化训练常用 bitsandbytes **0.49.2（2026-10-26）**。来源：[PyTorch 2.15 Release Blog](https://pytorch.org/blog/pytorch-2-15-release-blog/)、[Transformers Releases](https://github.com/huggingface/transformers/releases/tag/v5.20.0)、[bitsandbytes Releases](https://github.com/bitsandbytes-foundation/bitsandbytes/releases)

## 二、基础概念

> [!note] 一句话理解
> **预训练学知识，SFT 学格式，偏好优化学取舍。** 三者并非互相替代，而是能力与对齐的两个不同层面。

- **预训练（Pre-Training）**：在大规模无标注/弱标注语料上，以**下一个 token 预测（next-token prediction）**为训练目标，让模型掌握语言规律与世界知识。这是模型能力（智力）的主要来源，遵循 scaling laws，通常需要海量算力与数据，成本最高。
- **监督微调（SFT，Supervised Fine-Tuning）**：用人工构造的「指令—回答」样本继续训练，让模型**学会按指令作答、遵循格式与角色设定**。SFT 不显著增加新知识，主要解决「预训练模型只会续写、不会按要求作答」的问题。
- **偏好优化 / RLHF（Reinforcement Learning from Human Feedback）**：在 SFT 模型之上，用人类偏好数据（更好/更差的回答对）训练奖励模型或直接优化策略，让模型**学会判断与取舍**，输出更符合人类价值观、有用且安全的响应。PPO 是 RLHF 的经典实现，DPO、GRPO 是其演进变体。
- **关键基础要素**：词表（vocabulary）、token、上下文窗口（context window）、采样参数（温度、top-p/top-k）等，是理解训练与推理的共同底座。
- **奖励模型（RM，Reward Model）**：RLHF 中用于给模型输出打分的模型，是 PPO 四模型（策略、价值、奖励、参考）之一。

## 三、核心机制

### 3.1 预训练：下一个 token 预测

模型对每个位置预测下一个 token 的概率分布，训练目标是最大化语料上的平均负对数似然。工程上的核心是**数据配比**（知识/代码/多语言比例）与**并行策略**：数据并行（DP）、张量并行（TP）、流水线并行（PP）、专家并行（EP，针对 MoE），以及混合精度训练与显存优化（梯度累积、ZeRO、激活重算等）。预训练结束后得到的是「基础模型」，一般具备续写能力但缺乏指令遵循与对齐。

### 3.2 SFT：从续写到作答

把样本整理成 `指令 + 可选输入 → 回答` 的格式，对模型做监督学习。核心在于**数据质量与多样性**：覆盖真实任务、控制长度与难度分布、避免单一风格导致过拟合。资源充足时可全量微调，算力受限时用 **LoRA / QLoRA** 只训练低秩适配矩阵（通常仅 0.1%–3% 参数），且**不增加推理成本**。关键超参：`rank`（r）、`alpha`、`target_modules`、`dropout`、学习率、批大小、训练轮数。

### 3.3 偏好优化：从对齐到工程实现

- **PPO**：经典 RLHF，同时训练策略模型与价值模型，用奖励模型打分并加 KL 约束防止偏离参考模型，稳定但实现复杂、训练成本高。
- **DPO（Direct Preference Optimization）**：**无参考模型、无需奖励模型**，直接在偏好对上做分类式优化，把 RLHF 简化为监督学习，工程上更易落地。
- **GRPO（Group Relative Policy Optimization）**：以可验证奖励（可计算、可验证的指标）为代表，从组内相对优劣估计优势，兼顾效果与训练稳定性，2025 年起成为后训练主流方向。

> [!warning] 概念边界
> RLHF 是「对齐」的**工程实现手段**，不要与「对齐」目标本身混同。SFT 与偏好优化目标不同：前者学格式与指令遵循，后者学价值取舍，二者数据、损失、评估方式都应区分。

## 四、实践步骤（含代码/命令示例）

**1. 环境准备**（建议 Python 3.11+，训练框架注意与基座模型版本兼容）

```bash
# 创建独立虚拟环境
python -m venv .venv-llm
# Windows PowerShell
.\.venv-llm\Scripts\Activate.ps1

# 安装训练与微调核心依赖
pip install "torch>=2.15.0" "transformers>=5.22.2" "trl>=1.17.0" "peft>=0.21.3"
pip install accelerate datasets bitsandbytes
```

**2. 预训练最小示例**（自建语料做 next-token 预训练，用 HF Trainer）

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

model_name = "Qwen/Qwen2.5-7B"  # 以官方仓库可用模型为准
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")

def tokenize(batch):
    texts = [f"{t}\n" for t in batch["text"]]
    return tokenizer(texts, truncation=True, max_length=2048)

ds = load_dataset("text", data_files="corpus.txt", split="train")
ds = ds.map(tokenize, batched=True)

args = TrainingArguments(
    output_dir="./ckpt-pretrain",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,
    logging_steps=50,
    save_strategy="steps",
    save_steps=500,
)
Trainer(model=model, args=args, train_dataset=ds).train()
```

**3. SFT：用 PEFT 做 LoRA 指令微调**

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

MODEL = "Qwen/Qwen2.5-7B"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype="auto")

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora)

ds = load_dataset("json", data_files="sft_data.json", split="train")
ds = ds.map(lambda b: tokenizer(
    f"### 指令：\n{b['instruction']}\n### 回答：\n{b['output']}",
    truncation=True, max_length=2048), batched=True)

args = TrainingArguments(
    output_dir="./ckpt-sft",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    logging_steps=20,
    save_strategy="steps", save_steps=200,
)
Trainer(model=model, args=args, train_dataset=ds).train()
model.save_pretrained("./ckpt-sft-final")
```

**4. 偏好优化：用 TRL 做 DPO**（无参考模型，实现更简单）

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOConfig, DPOTrainer

MODEL = "Qwen/Qwen2.5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype="auto")

ref = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype="auto")  # 参考模型
ds = load_dataset("json", data_files="pref_data.json", split="train")  # 含 chosen/rejected

trainer = DPOTrainer(
    model=model,
    ref_model=ref,
    args=DPOConfig(output_dir="./ckpt-dpo", beta=0.1, num_train_epochs=1),
    train_dataset=ds,
)
trainer.train()
trainer.save_model("./ckpt-dpo-final")
```

**5. 训练启动命令**（多卡，训练脚本 `train_sft.py`）

```bash
accelerate launch --num_processes 8 --mixed_precision bf16 train_sft.py
```

> [!tip] 资源不足时
> 显存不够优先选 QLoRA（4bit 量化基座 + LoRA），而不是强行全量微调；同时用梯度累积、降低序列长度、减少并发显存占用来控成本。

## 五、最佳实践与常见坑

**最佳实践**

- **先评估、后训练**：训练前先定义成功指标与固定测试集（准确率、格式合规、安全性），训练后与基线对比，避免「感觉变好了」的主观判断。
- **数据优先**：SFT 的瓶颈在数据质量而非模型；优先做数据清洗、格式统一、难度与领域配比，再谈超参。
- **分层训练、按需选择**：只需改格式 → SFT；需要对齐价值观/偏好 → 叠加 DPO/GRPO；追求训练吞吐与稳定性 → 评估 GRPO。
- **版本锁定**：训练框架（TRL/PEFT/Transformers）与基座模型版本需组合验证，生产环境锁定版本，避免破坏性变更影响复现。
- **用可验证奖励**：能用代码/规则校验的奖励，优先 GRPO 等可验证奖励路线，比人工奖励模型更稳、成本更低。

**常见坑**

| 现象 | 可能原因 | 对策 |
| --- | --- | --- |
| SFT 后只会套模板、泛化差 | 数据单一、过拟合、轮数过多 | 增加数据多样性，降低 epoch，留评估集监控 |
| 显存 OOM | 全量微调、序列过长、未开梯度累积 | 改用 LoRA/QLoRA，缩短序列，梯度累积/激活重算 |
| RLHF 训练不稳定、奖励虚高 | PPO 调参复杂、奖励模型缺陷、KL 约束过弱/过强 | 先用 DPO/GRPO，调 KL 系数，监控奖励与回复长度 |
| 对齐后能力退化（「对齐税」） | 偏好优化过度、参考约束过强 | 控制 beta/KL、保留部分 SFT 能力，分步验证 |
| 版本不兼容报错 | TRL/PEFT 与 Transformers 版本不匹配 | 按官方兼容矩阵锁定版本，升级前回源核对 |
| 训练结果无法复现 | 未固定种子、数据顺序变化 | 固定 `seed`，固定数据加载顺序与版本 |

## 六、核心要点速查

1. 训练三阶段：**预训练（学知识）→ SFT（学格式）→ 偏好优化（学取舍）**，三者递进、不可替代。
2. 预训练目标为**下一个 token 预测**，能力与数据、算力规模强相关，遵循 scaling laws。
3. SFT 把续写模型改造成**指令作答模型**，核心是数据质量与多样性。
4. LoRA 仅训练 0.1%–3% 参数且**不增加推理成本**，QLoRA 叠加 4bit 量化进一步降显存。
5. PPO 是 RLHF 经典实现，**DPO 无参考模型、无需奖励模型**，GRPO 以可验证奖励为代表（2025 年起成主流）。
6. RLHF 是「对齐」的**工程实现**，需与对齐目标、SFT 明确区分。
7. 训练前先建**评估集与基线**，训练后用数据对比，避免主观判断。
8. 显存不足优先 QLoRA，而非强行全量微调。
9. 训练框架与基座模型**锁定版本**，生产前核对官方兼容性。
10. 版本号以官方仓库当日状态为准，社区二手信息需回源核对。

## 七、学习资源

1. [阿里云 PAI 大模型微调指引（官方，三阶段流程与 SFT/DPO 策略）](https://www.alibabacloud.com/help/zh/pai/llm-fine-tuning-experience)
2. [TRL Releases（官方，DPO/GRPO/AsyncGRPO 实现）](https://github.com/huggingface/trl/releases)
3. [PEFT Releases（官方，LoRA/QLoRA 及新变体）](https://github.com/huggingface/peft/releases)
4. [Hugging Face Transformers Releases（官方）](https://github.com/huggingface/transformers/releases)
5. [PyTorch 2.15 Release Blog（官方）](https://pytorch.org/blog/pytorch-2-15-release-blog/)
6. [Transformer 原始论文：Attention Is All You Need（arXiv:1706.03762）](https://arxiv.org/abs/1706.03762)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[大模型-训练范式与微调实战]]
- [[大模型-Transformer与注意力机制]]
- [[大模型基础核心要点]]
- [[深度学习-PyTorch入门]]

## 九、变更记录

- 2026-11-19：首次创建。
