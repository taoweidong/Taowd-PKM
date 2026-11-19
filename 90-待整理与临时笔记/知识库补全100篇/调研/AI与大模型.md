---
title: AI 与大模型 调研
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI与大模型
  - 调研
  - 知识库补全100篇
---

> 调研目的：为「AI 与大模型」方向的 18 个知识点提供截至 2026 年 11 月的**最新官方支持与关键事实**，供后续撰写 18 篇详细文档引用。
> 调研方法：`web_search` + `web_fetch`，优先官方文档、官方 GitHub 仓库与权威技术站点。
> 时效说明：版本号、发布日期均来自检索时点（2026-11）的官方页面；框架迭代极快，写作前请以官方仓库当日状态复核。

## 一、主题最新动态（截至 2026-11）

- **vLLM v0.34.0 发布（2026-11-15）**：10 个新模型；**可扩展 KV cache 默认开启**（按预热后实际空闲显存动态定容，如 MiniMax-M3 在 H200 上从 433k 提升到 672k token）；**Model Runner V2 成为唯一 GPU 运行器**（V1 被移除）；默认 block size 改为 64；默认 CUDA 13.0。Blackwell 与 MI355X 上解码/吞吐大幅提速（Step5 在 GB200 上解码最高 1.95×）。来源：<https://github.com/vllm-project/vllm/releases/tag/v0.34.0>
- **SGLang v0.5.23 发布（2026-10-30）**：1007 个 PR、257 位贡献者；新增 Muse Spark Open、Beam-1.0、MiniMax-M3.1-Flash、MiniCPM-V 4.7 等模型；DeepSeek-V4.1 在 GB300 上 prefill 吞吐最高 1.5×；低延迟 megakernel/monokernel 插件使单用户解码最高提升 44%（GB300）/75%（MI350X）；支持在量化 MoE 模型上服务 LoRA adapter；可通过 SGLang-TorchTPU 运行于 Google TPU7x。**SGLang 自 v0.5.22 起要求 Python 3.11+**。来源：<https://github.com/sgl-project/sglang/releases>
- **TensorRT-LLM v1.4.0rc4（预发布，2026-11-15）**：Modeling V2 目标扩展至 GLM-5.2 / GLM-5.3-Flash / MiniMax-M3 / Qwen3.8-Flash-Next 的 NVFP4；新增 KVCM V2 稀疏 KV offload、DSpark 置信度调度、Gumbel-max 文本水印；KV cache manager V2 成为推荐架构（V1 进入弃用流程）。稳定线文档为 1.2.0（2026-03-11 发布说明）。来源：<https://github.com/NVIDIA/TensorRT-LLM/releases>、<https://nvidia.github.io/TensorRT-LLM/1.2.0/release-notes.html>
- **PyTorch 2.15.0 发布（2026-10-26）**：默认 wheel 迁移到 **CUDA 13.2**（提供 CUDA 13.4 wheel）；cudnn/MPS 内核重写，单行 softmax（128k 词表）降速 8×；线性代数求解器重写（512×512 QR 从约 7 秒降至 1.5ms）。要求 Python 3.10+。来源：<https://pytorch.org/blog/pytorch-2-15-release-blog/>
- **Hugging Face Transformers 进入 v5 世代**：当前最新 v5.22.2；v5.20.0（2026-10-14）引入 UltraBERT 系列、MOSS-Transcribe-Diarize 等。来源：<https://github.com/huggingface/transformers/releases/tag/v5.20.0>
- **PEFT v0.21.3（最新）**：v0.21.0 新增 Riemannian 预条件 LoRA 优化器、KaSA、Super-Tuning、ShadowPEFT 等方法；v0.21.2 修复 Transformers ≥5.18 的 encoder-decoder 兼容问题；v0.21.1 支持 Tensor Parallel。来源：<https://github.com/huggingface/peft/releases>
- **TRL v1.17.0（2026-11-08）**：支持在单节点 8×B300 上对 **Mistral-Large-4-1T-A52B**（1T 总参 / 52B 激活，FP8）做 LoRA SFT；AsyncGRPO 默认启用 score centering（`score_centering=True`）；修正 top-k/top-p 过滤下的重要性采样偏差；新增 AMD Instinct GPU 支持。来源：<https://github.com/huggingface/trl/releases/tag/v1.17.0>
- **LangChain / LangGraph**：LangChain **v1.0 GA** 以 `create_agent` 作为构建 Agent 的标准方式（取代 LangGraph 的 `createReactAgent`），遗留能力移入 `@langchain/classic`；**LangChain v1.4.3 于 2026-09-28 发布**；**LangGraph v1.1.0（2026-03-10）** 引入 `version="v2"` 的类型安全 stream/invoke、Pydantic/dataclass 自动强转。当前 langgraph 最新 1.2.18。来源：<https://docs.langchain.org/oss/javascript/releases/changelog>、<https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1>
- **LlamaIndex v0.14.23（2026-06-24）** 为当前最新稳定线。来源：<https://security.snyk.io/package/pip/llama-index/versions>、<https://github.com/run-llama/llama_index/releases/tag/v0.14.18>
- **Model Context Protocol（MCP）2026-07-28 规范发布**：第五个规范版本，核心转向**无状态请求/响应模型**（可部署到 serverless/边缘），加强授权、官方扩展转正；官方称 MCP 月度 SDK 下载量已超 **4 亿**，较上一年增长 4 倍。来源：<https://modelcontextprotocol.io/specification/2026-07-28/index>、<https://websitemain.claude.com/blog/bringing-mcp-2026-07-28-to-claude>
- **OpenAI 模型线**：GPT-5.2（2025-12-11）、**GPT-5.3-Codex（2026-02-05，首个 Codex+GPT-5 训练栈融合的 agentic 编码模型，速度提升约 25%）**；**GPT-5.5（2026 年 4 月旗舰，1M 上下文）**。来源：<https://help.openai.com/en/articles/9624314-model-release-notes>、<https://github.com/gptme/gptme/blob/main/gptme/llm/llm_openai_models.py>
- **Anthropic 模型线**：**Claude Fable 5.2 / Mythos 5.2（2026-11-11 发布）**，同底座两种版本，输出速度较 5.1 提升约 30%，编码/推理/视觉增强；Fable 含网络安全与生物安全护栏（面向全部用户），Mythos 移除部分护栏。来源：<https://cloudfresh.com/gc/news/claude-fable-5-2-and-mythos-5-2/>
- **开源模型生态**：2026 年 4 月一周内六家实验室发布开源模型，其中 **五家采用 Apache 2.0 完全宽松许可**，Google 将 Gemma 迁移至该许可；OpenAI 发布其首个 120B 规模开放模型；Qwen3.5（2026.02）/ Qwen3.6 / Qwen3.8（2.4T-A95B）、GLM-5.x、DeepSeek-V4/V4.1、Kimi K3、Mistral Large 4（1T/52B）构成主要开源阵营。来源：<https://zenodo.org/records/23963897>、<https://www.respan.ai/blog/best-open-source-llms>
- **量化与本地推理**：bitsandbytes 0.49.2（2026-10-26，CPU 4bit 大幅优化、新增 ROCm CDNA blocksize=64 支持）；**llama.cpp v0.8.0（2026-10-28）**，支持 Liquid AI LFM3 系列与 DeepSeek-V4.1 Flash，新增实验性 `/v1/realtime` 实时音频与 `POST /tts`。来源：<https://github.com/bitsandbytes-foundation/bitsandbytes/releases>、<https://shop.zimaspace.com/ko/blogs/tech-ai-hub/llama-cpp-0-8-0-new-models-realtime-voice-local-ai>
- **向量数据库**：**Milvus 3.0 于 2026-07-16 官宣 GA**（Apache 2.0，支持 K8s/Docker，提供 Python/Go/Node SDK），其 GitHub 稳定 tag 仍为 2.6.21（2026-07）；Qdrant 稳定线 1.18.x；Weaviate 稳定线 1.38.x（1.39 为 RC）。来源：<https://cloud.vk.ru/blog/vektornie-bazi-dannikh-dlya-rag-kak-vibrat-dvizhok-i-podnyat-odrant-v-vk-cloud/>

## 二、版本与关键事实表

| 项目 / 组件 | 版本号 | 发布日期 | 关键变化 | 官方来源 URL |
|---|---|---|---|---|
| vLLM | v0.34.0（最新） | 2026-11-15 | 可扩展 KV cache 默认开启；Model Runner V2 唯一运行器；默认 block size 64；CUDA 13.0；Blackwell/MI355X 提速 | <https://github.com/vllm-project/vllm/releases/tag/v0.34.0> |
| SGLang | v0.5.23（最新） | 2026-10-30 | 1007 PR；DeepSeek-V4.1 prefill 1.5×；低延迟 megakernel/monokernel；量化 MoE 上服务 LoRA；Python 3.11+ | <https://github.com/sgl-project/sglang/releases> |
| TensorRT-LLM | v1.4.0rc4（预发布）；1.2.0（稳定线文档） | 2026-11-15 / 2026-03-11 | Modeling V2 目标扩展；KVCM V2 稀疏 KV offload；KV cache manager V2 推荐，V1 弃用 | <https://github.com/NVIDIA/TensorRT-LLM/releases> |
| PyTorch | 2.15.0（Stable） | 2026-10-26 | 默认 CUDA 13.2；MPS/cudnn 内核重写；要求 Python 3.10+ | <https://pytorch.org/blog/pytorch-2-15-release-blog/> |
| Transformers | v5.22.2（最新）；v5.20.0 | 2026-10（v5.20.0 为 2026-10-14） | v5 世代，UltraBERT、MOSS-Transcribe-Diarize 等 | <https://github.com/huggingface/transformers/releases/tag/v5.20.0> |
| PEFT | v0.21.3（最新） | 2026-11（v0.21.x 线） | 新 LoRA 变体（Riemannian、KaSA、Super-Tuning、ShadowPEFT）；TP 支持 | <https://github.com/huggingface/peft/releases> |
| TRL | v1.17.0 | 2026-11-08 | Mistral-Large-4-1T LoRA SFT；AsyncGRPO score centering 默认；AMD GPU 支持 | <https://github.com/huggingface/trl/releases/tag/v1.17.0> |
| bitsandbytes | 0.49.2 | 2026-10-26 | CPU 4bit 优化；ROCm CDNA blocksize=64 | <https://github.com/bitsandbytes-foundation/bitsandbytes/releases> |
| llama.cpp | v0.8.0 | 2026-10-28 | LFM3 系列、DeepSeek-V4.1 Flash；实验性实时音频、TTS | <https://shop.zimaspace.com/ko/blogs/tech-ai-hub/llama-cpp-0-8-0-new-models-realtime-voice-local-ai> |
| LangChain | v1.4.3 | 2026-09-28 | v1.0 GA 后持续修复；`create_agent` 标准接口 | <https://docs.langchain.org/oss/javascript/releases/changelog> |
| LangGraph | v1.1.0（最新 1.2.18） | 2026-03-10 | `version="v2"` 类型安全 stream/invoke；Pydantic/dataclass 强转 | <https://github.com/langchain-ai/docs/blob/933a2f92/src/oss/python/releases/changelog.mdx> |
| LlamaIndex | v0.14.23（最新） | 2026-06-24 | 持续修复与依赖升级 | <https://security.snyk.io/package/pip/llama-index/versions> |
| MCP | 2026-07-28 规范 | 2026-07-28 | 无状态核心；授权加固；官方扩展转正；月 SDK 下载 4 亿+ | <https://modelcontextprotocol.io/specification/2026-07-28/index> |
| Milvus | 3.0（GA）；2.6.21（GitHub tag） | 2026-07-16 | Apache 2.0；K8s/Docker；Python/Go/Node SDK | <https://cloud.vk.ru/blog/vektornie-bazi-dannikh-dlya-rag-kak-vibrat-dvizhok-i-podnyat-odrant-v-vk-cloud/> |
| OpenAI GPT | GPT-5.3-Codex；GPT-5.5 | 2026-02-05；2026-04 | Codex 与 GPT-5 训练栈融合；GPT-5.5 旗舰、1M 上下文 | <https://help.openai.com/en/articles/9624314-model-release-notes> |
| Anthropic Claude | Fable 5.2 / Mythos 5.2 | 2026-11-11 | 输出提速约 30%；两种护栏配置 | <https://cloudfresh.com/gc/news/claude-fable-5-2-and-mythos-5-2/> |
| Transformer 原始论文 | — | 2017 | 提出自注意力机制，奠定 LLM 架构基础 | <https://arxiv.org/abs/1706.03762> |

## 三、分知识点关键事实

### 1. 大语言模型基础概念与工作原理

- **核心原理**：LLM 通过**下一个 token 预测（next-token prediction）**进行自回归生成；能力来自大规模预训练与规模扩展（scaling laws）。基础要素包括词表（vocabulary）、token、上下文窗口（context window）、温度/采样参数。
- **可核实事实**：vLLM、SGLang 等现代引擎均基于"自回归解码 + KV cache"范式，vLLM v0.34.0 已将 KV cache 管理作为核心优化点（可扩展 KV cache 默认开启）。来源：<https://github.com/vllm-project/vllm/releases/tag/v0.34.0>
- 权威参考：Hugging Face Transformers 教程、OpenAI 模型文档。

### 2. Transformer 架构详解

- **原始论文**：Vaswani 等《Attention Is All You Need》，NeurIPS 2017，arXiv:1706.03762，首次提出**自注意力（self-attention）**、多头注意力、位置前馈网络与 encoder-decoder 结构。来源：<https://arxiv.org/abs/1706.03762>
- **现代变体**：当代 LLM 普遍采用 decoder-only + RoPE 位置编码、RMSNorm、SwiGLU 前馈层、GQA/MLA 注意力等改进；v0.34.0 的 vLLM 已支持稀疏 MLA、DeepSeek 系 MLA 与 KV 压缩等架构。来源：<https://github.com/vllm-project/vllm/releases/tag/v0.34.0>
- 写作时可对比"原始 Transformer"与"现代 LLM 结构"的差异，避免把 2017 年结构直接等同于当今 LLM。

### 3. 提示工程（Prompt Engineering）实战

- **官方指南**：OpenAI 官方《Best practices for prompt engineering with the OpenAI API》持续更新，明确提示工程的常见有效格式与原则（清晰指令、示例、角色设定、输出规范等）。来源：<https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api>
- Anthropic 官方提示工程文档覆盖逐步思考（extended thinking）、上下文组织、工具使用等。来源：<https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>
- 提示工程是**工程手段而非模型能力替代**，与微调、RAG 互补，写作时不宜夸大其效果。

### 4. 大模型微调技术（SFT/LoRA）

- **PEFT 官方版本事实**：PEFT 最新 **v0.21.3**；v0.21.0 新增 Riemannian 预条件 LoRA 优化器、KaSA、Super-Tuning、ShadowPEFT；v0.21.2 修复 Transformers ≥5.18 兼容问题。来源：<https://github.com/huggingface/peft/releases>
- **LoRA 仍是主流**：TRL v1.17.0 展示对 **Mistral-Large-4-1T-A52B** 在单节点 8×B300 上做 LoRA SFT（约 142 GiB/卡），说明 LoRA/PEFT 已能适配超大规模 MoE 模型。来源：<https://github.com/huggingface/trl/releases/tag/v1.17.0>
- 关键参数：`rank`（r）、`alpha`、`target_modules`、`dropout`、学习率、批大小、训练轮数；LoRA 常与 QLoRA（4bit 量化基座）配合。

### 5. 大模型训练体系（预训练/SFT/RLHF）

- **典型三阶段**：预训练（Pre-Training）→ 监督微调（SFT）→ 偏好优化（DPO/PPO 等），阿里云 PAI 官方微调指引明确该流程与 SFT/DPO 策略选择。来源：<https://www.alibabacloud.com/help/zh/pai/llm-fine-tuning-experience>
- **对齐技术演进**：从 PPO 到 DPO 及无参考变体，再到 2025 年起以可验证奖励为代表的 **GRPO** 浪潮；TRL v1.17.0 中 AsyncGRPO 默认启用 score centering 以修正 FP8 采样器下的目标退化。来源：<https://github.com/huggingface/trl/releases/tag/v1.17.0>
- RLHF 是"对齐"的工程实现，写作时需区分 SFT（学格式）与偏好优化（学取舍）。

### 6. 大模型推理优化与量化

- **量化格式现状（2026）**：AWQ（INT4 权重，数据中心生产常用）、GPTQ（vLLM 多 LoRA 场景）、GGUF/K-quants（llama.cpp/端侧）、FP8（Hopper/Ada/Blackwell 近无损）、MXFP4/NVFP4（新模型原生）。来源：<https://github.com/rohitg00/ai-engineering-from-scratch/blob/8afa245ebc2e8861480edf8c4911a2b6d9769688/phases/17-infrastructure-and-production/09-production-quantization/docs/en.md>
- **bitsandbytes 0.49.2（2026-10-26）**：CPU 4bit 性能显著优化（AVX512/AVX512BF16 内核），ROCm CDNA 支持 blocksize=64。来源：<https://github.com/bitsandbytes-foundation/bitsandbytes/releases>
- **KV cache 与权重量化是两条线**：仅压缩权重不等于降低端侧显存，KV cache 在生产批规模下可能占 10–30GB，写作时务必分开表述。
- 其他推理优化：连续批处理（continuous batching）、分块预填充（chunked prefill）、前缀缓存、投机解码（speculative decoding）、张量/流水线/专家/上下文并行。

### 7. 推理引擎对比（vLLM/SGLang/TensorRT-LLM）

- **vLLM v0.34.0（2026-11-15）**：以高吞吐著称，PagedAttention、连续批处理、分块预填充、前缀缓存、结构化输出；支持 OpenAI 兼容 API、张量/流水线/专家/上下文并行；默认 CUDA 13.0。来源：<https://github.com/vllm-project/vllm/releases/tag/v0.34.0>
- **SGLang v0.5.23（2026-10-30）**：以**前缀复用（radix cache）**与低延迟见长，适合长系统提示、RAG 高前缀重叠场景；支持量化 MoE 上的 LoRA、TPU7x。来源：<https://github.com/sgl-project/sglang/releases>
- **TensorRT-LLM v1.4.0rc4**：NVIDIA 深度优化，Modeling V2、KV cache manager V2 推荐、KVCM V2 稀疏 KV offload，对 NVIDIA 硬件/黑金刚（GB200/GB300）与 MoE 最成熟。来源：<https://github.com/NVIDIA/TensorRT-LLM/releases>
- **选型经验**：高前缀重叠选 SGLang；通用高吞吐/生态广选 vLLM；NVIDIA 全栈深度优化选 TensorRT-LLM。来源：<https://www.truefoundry.io/blog/sglang-vs-vllm-vs-tensorrt-llm>

### 8. RAG 检索增强生成

- **原始论文**：Lewis 等《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》，arXiv:2005.11401，首次提出 RAG 框架。来源：<https://arxiv.org/abs/2005.11401>
- **工程要点（2026）**：检索质量（chunk 切分、重排 rerank、查询改写）与生成质量需**分开评估**；建议为检索设定独立 SLO（如 p95 检索延迟、recall@k），而非只看回答质量。来源：<https://redwerk.com/blog/rag-best-practices/>
- **官方框架支持**：LangChain、LlamaIndex 均提供 RAG 组件；LlamaIndex 最新 v0.14.23。来源：<https://security.snyk.io/package/pip/llama-index/versions>

### 9. Agent 智能体开发基础

- **核心范式**：ReAct（Reasoning + Acting）论文（Yao 等，ICLR 2023，arXiv:2210.03629）确立"思考—行动—观察"交错的主流模式。来源：<https://arxiv.org/abs/2210.03629>
- **标准连接协议**：**MCP 2026-07-28 规范**将 MCP 核心转向无状态请求/响应，官方称月 SDK 下载量超 4 亿、较上年增长 4 倍，已成为 Agent 连接外部工具/数据的事实标准。来源：<https://modelcontextprotocol.io/specification/2026-07-28/index>、<https://websitemain.claude.com/blog/bringing-mcp-2026-07-28-to-claude>
- **生产级要素**：工具调用、规划、记忆、错误恢复、人在环（human-in-the-loop）；LangChain 官方建议以中间件处理限流/超时/瞬时错误。来源：<https://docs.langchain.com/oss/python/langchain/agents>

### 10. 多 Agent 协作与编排

- **编排思路**：以确定性编排器协调多个专业 Agent，例如"Cortex"确定性有限状态机编排 11 个专业 Agent，配合分层人在环与零 token 开销的发言者选择，完成长程异构任务。来源：<https://zenodo.org/records/20819131>
- **框架支持**：LangGraph 用**图（state graph）**表达多 Agent 状态流转，v1.1.0 的 `version="v2"` 提供类型安全；LangChain `create_agent` 亦构建于 LangGraph 之上。来源：<https://github.com/langchain-ai/docs/blob/933a2f92/src/oss/python/releases/changelog.mdx>
- 写作时区分"多 Agent 并行"与"编排（orchestration）"，避免混淆概念。

### 11. 大模型幻觉与安全对齐

- **幻觉成因与缓解**：幻觉（hallucination）源于模型对参数化记忆的过度依赖；缓解方向包括检索接地（RAG）、温度/采样控制、事实性评估、机制可解释性研究（如温度自适应 softmax 用于医疗记录场景）。来源：<https://zenodo.org/records/19229177>
- **对抗与红队**：2026 年研究显示，提示改写类攻击（人格设定、虚构框架、说服式改写）可绕过部分前沿模型的安全过滤；CHASE 提出黑盒攻击者与安全防御者**协同进化**的红蓝对抗框架，用 GRPO 训练攻击者。来源：<https://aclanthology.org/2026.aacl-long.36/>
- **伦理对齐新挑战**：TRIAL 方法表明，将有害请求嵌入伦理框架的多轮红队可稳定获得高攻击成功率，需区分"工具性响应"与"有害结果"。来源：<https://aclanthology.org/2026.acl-long.197/>
- 安全对齐是持续对抗过程，不宜写成"已解决"。

### 12. 大模型评测与基准

- **主流基准**：MMLU、GSM8K、GPQA、MMLU-Pro、HellaSwag、ARC、HumanEval、LiveCodeBench、SciCode 等；各基准的"排名区分度"与数据污染问题需注意（有研究指出 HELM 与 Open LLM Leaderboard 在 MMLU 上区分度有限）。来源：<https://zenodo.org/records/23007588/files/Which-AI-model-is-truly-the-best-Kankaras-2026-preprint.pdf>
- **评测工具**：EleutherAI `lm-evaluation-harness`（支持 200+ 任务、可接 vLLM 加速）、Stanford HELM、Hugging Face Open LLM Leaderboard v2（已归档）。来源：<https://www.morphllm.com/llm-eval-harness>、<https://github.com/ml-engineering-curriculum/model-evaluation-engineer-learning/blob/main/lessons/mod-104-llm-benchmark-harnesses/resources.md>
- 写作提示：引用榜单分数时注明版本、few-shot 设置与评测时间，避免跨版本比较。

### 13. 向量数据库与嵌入模型

- **嵌入模型（2026）**：OpenAI `text-embedding-3-small`（1536 维）/ `text-embedding-3-large`（3072 维，支持 Matryoshka 维度裁剪）；Gemini Embedding 2 在 4K–32K 全长度区间评分 1.000；另有 Voyage、Jina v4、Cohere Embed v4、BGE-M3（可自托管）。来源：<https://blog.milvus.io/zh-hant/blog/choose-embedding-model-rag-2026.md>、<https://raw.githubusercontent.com/ericrisco/rsc-harness/refs/heads/main/skills/embeddings-search/references/models.md>
- **向量数据库版本**：Milvus 3.0 于 2026-07-16 GA（Apache 2.0，K8s/Docker，多语言 SDK）；Qdrant 稳定线 1.18.x；Weaviate 稳定线 1.38.x。来源：<https://cloud.vk.ru/blog/vektornie-bazi-dannikh-dlya-rag-kak-vibrat-dvizhok-i-podnyat-odrant-v-vk-cloud/>
- 选型时注意区分**内存型 / 磁盘型 / 云托管**，以及是否支持过滤、混合检索（关键词+向量）与重排。

### 14. LangChain 与 LangGraph 开发

- **LangChain v1**：生产就绪的 Agent 基础框架，三大改进为 `create_agent`（取代 `createReactAgent`）、统一 **content blocks**、精简包结构（遗留能力移入 `@langchain/classic`）。来源：<https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1>
- **LangGraph v1.1.0（2026-03-10）**：`version="v2"` 提供类型安全 stream/invoke，支持 Pydantic/dataclass 自动强转；LangChain **v1.4.3（2026-09-28）**。来源：<https://docs.langchain.org/oss/javascript/releases/changelog>、<https://newreleases.io/project/github/langchain-ai/langgraph/release/1.1.0>
- **注意**：LangChain 1.0 重写后仍存在破坏性变更历史，生产中建议**锁定版本**。来源：<https://panoply.io/tools/langchain/>

### 15. LlamaIndex 知识库构建

- **版本事实**：LlamaIndex 最新稳定 **v0.14.23（2026-06-24）**；核心包 `llama-index-core` 随版本迭代（v0.14.18 起弃用 Python 3.9）。来源：<https://security.snyk.io/package/pip/llama-index/versions>、<https://github.com/run-llama/llama_index/releases/tag/v0.14.18>
- **定位**：以"数据/索引为中心"构建 RAG 与知识库，核心组件包括 Ingestion Pipeline、解析器、切分、向量索引、查询引擎（Retriever + Reader）；适合文档型知识库场景。
- 写作时可对比 LlamaIndex 与 LangChain 的分工：前者偏数据接入与索引，后者偏 Agent 编排。

### 16. 多模态大模型（视觉/语音）

- **能力演进**：从"只看图"走向"图像+语音+视频"理解与语音生成；开源侧 Qwen3-VL / Qwen3.5-Omni（覆盖文本、图像、音频、视频，最大 256K 序列，支持 10 小时音频）、Gemma 4（多模态）、Qwen3-VL-MoE 等。来源：<https://www.digitaltoday.co.kr/en/view/44651/alibaba-ai-qwen35-omni-launches-with-vibe-coding-and-real-time-response>、<https://docs.nvidia.com/nemo/automodel/v0.4/model-coverage/vision-language-models/overview>
- **端到端语音多模态**：VITA-1.5 提出多阶段训练，使 LLM 同时理解视觉与语音，保持视觉语言能力并支持语音到语音对话。来源：<https://dl.acm.org/doi/10.52202/085713-2529>
- 多模态提示词与纯文本提示词的差异、失败模式（OCR、图表、密集截图）需在文档中单独说明。

### 17. 大模型部署与服务化

- **服务化栈**：以 vLLM / SGLang / TensorRT-LLM 提供 OpenAI 兼容 API，配合容器与 K8s 编排（KServe 管理生命周期、Knative 弹性伸缩、Istio 服务网格），并叠加认证、限流、计量等组件。来源：<https://ieeexplore.ieee.org/document/11668330>
- **vLLM 服务化细节**：`vllm serve` 为标准启动方式（旧的 `python -m vllm.entrypoints.openai.api_server` 已弃用）；提供 Docker 镜像（CUDA/ROCm/CPU/XPU）；支持故障容错 DP+EP 缩容、checkpoint/restore、NUMA 绑定、KV connector（NIXL/Mooncake）。来源：<https://github.com/vllm-project/vllm/releases/tag/v0.34.0>
- **端侧部署**：llama.cpp v0.8.0 支持 GGUF 本地推理、实时音频与 TTS，适合消费级硬件。来源：<https://shop.zimaspace.com/ko/blogs/tech-ai-hub/llama-cpp-0-8-0-new-models-realtime-voice-local-ai>

### 18. 开源大模型生态与选型

- **许可格局（2026）**：开源生态形成高集中度格局；2026 年 4 月一周内六家实验室发布开源模型，其中五家采用 **Apache 2.0**，Google 将 Gemma 迁移至该许可；OpenAI 发布首个 120B 规模开放模型。来源：<https://zenodo.org/records/23963897>
- **代表阵营**：Google Gemma 4（31B dense / 26B A4B，Apache 2.0，256K 上下文，多语言）、Alibaba Qwen（Qwen3.5/3.6/3.8 全尺寸全模态）、Meta Llama 4、DeepSeek-V4/V4.1、GLM-5.x、Kimi K3、Mistral Large 4（1T/52B）。来源：<https://www.respan.ai/blog/best-open-source-llms>
- **选型维度**：参数量与激活量、上下文长度、许可证（Apache 2.0 vs 自定义）、中文能力、多模态支持、显存需求、推理框架适配度、社区与工具链成熟度。中文场景通常优先 Qwen 系；低显存端侧优先 Gemma；长上下文与通用任务可评估 Llama/DeepSeek。

## 四、写作要点与风险提示

1. **版本时效性风险（最高）**：推理引擎、训练框架、模型版本迭代极快，本文版本号均为 2026-11 检索时点数据。写作与定稿前必须**以官方 GitHub Releases / 官方文档当日状态复核**；避免在文档中把某个版本写成"最新"而不加日期。
2. **"最新"表述需带日期**：如"截至 2026-11，vLLM 最新为 v0.34.0"，避免绝对化表述。
3. **区分预发布与稳定版**：TensorRT-LLM v1.4.0rc4 为预发布，不能写成正式稳定版；Milvus 3.0 已官宣 GA 但 GitHub 稳定 tag 仍为 2.6.21，需注明差异。
4. **量化表述易错**：不要把"权重量化"等同于"整体显存下降"，KV cache 独立于权重量化；AWQ/GPTQ/GGUF/FP8/MXFP4 各有适用硬件与引擎，不可混用结论。
5. **对比结论不可绝对化**：vLLM / SGLang / TensorRT-LLM 无通用最优解，"高前缀重叠选 SGLang、通用高吞吐选 vLLM、NVIDIA 全栈选 TensorRT-LLM"是经验性建议，需结合模型、GPU、序列长度、并发实测。
6. **基准分数需带条件**：引用 MMLU、GPQA 等分数时注明评测版本、few-shot 设置、评测时间；榜单存在区分度与数据污染问题，不可跨版本直接比较。
7. **幻觉与安全对齐不宜写成"已解决"**：2026 年研究仍显示提示改写类攻击可绕过部分安全过滤，安全是持续对抗过程。
8. **Transformer 概念边界**：2017 年原始 Transformer 为 encoder-decoder，现代 LLM 多为 decoder-only + RoPE/RMSNorm/SwiGLU/GQA-MLA，不要把原始结构直接等同于当今 LLM。
9. **框架版本与破坏性变更**：LangChain 1.0 重写、LangGraph v1.1 的 `version="v2"`、vLLM Model Runner V1 移除等均有破坏性变更，生产文档应提示**锁定版本**与迁移动作。
10. **开源许可需核对**：同系列不同版本许可可能不同（如 Gemma 迁移至 Apache 2.0），选型时以官方模型卡许可证为准，避免引用过时许可信息。
11. **来源分层**：优先官方仓库/官方文档（本文已尽量采用），第三方博客与聚合站（如 respan.ai、cloudfresh、cloud.vk.ru）仅作补充佐证，关键版本号务必回官方源核对。

## 附：主要来源清单

- vLLM Releases：<https://github.com/vllm-project/vllm/releases>
- SGLang Releases：<https://github.com/sgl-project/sglang/releases>
- TensorRT-LLM Releases：<https://github.com/NVIDIA/TensorRT-LLM/releases>
- PyTorch 2.15 Release Blog：<https://pytorch.org/blog/pytorch-2-15-release-blog/>
- Hugging Face Transformers Releases：<https://github.com/huggingface/transformers/releases>
- Hugging Face PEFT Releases：<https://github.com/huggingface/peft/releases>
- Hugging Face TRL Releases：<https://github.com/huggingface/trl/releases>
- bitsandbytes Releases：<https://github.com/bitsandbytes-foundation/bitsandbytes/releases>
- OpenAI Model Release Notes：<https://help.openai.com/en/articles/9624314-model-release-notes>
- Anthropic / Claude 官方博客与文档：<https://websitemain.claude.com/blog/bringing-mcp-2026-07-28-to-claude>
- LangChain Changelog：<https://docs.langchain.org/oss/javascript/releases/changelog>
- LangChain v1 说明：<https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1>
- LlamaIndex Releases / Snyk 版本列表：<https://security.snyk.io/package/pip/llama-index/versions>
- Model Context Protocol 规范：<https://modelcontextprotocol.io/specification/2026-07-28/index>
- Transformer 论文：<https://arxiv.org/abs/1706.03762>
- ReAct 论文：<https://arxiv.org/abs/2210.03629>
- RAG 论文：<https://arxiv.org/abs/2005.11401>
