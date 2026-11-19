---
title: AI与大模型-从入门到精通
date: 2026-11-18
updated: 2026-11-18
tags:
  - AI/大模型
  - AI/LLM
  - LLM
  - Transformer
  - RAG
  - Agent
aliases:
  - AI与大模型
  - 大语言模型原理与应用全景
source: https://github.com/vllm-project/vllm/releases/tag/v0.32.0
---

# AI与大模型-从入门到精通

> [!summary] 摘要
> 本文覆盖大语言模型（LLM）从底层原理到工程落地的完整链条：以 [[自然语言处理-BERT模型详解]] 所需的 Transformer 与注意力机制为模型基础，串起 Prompt 工程、微调（LoRA/QLoRA）、RAG、AI Agent、推理部署与安全治理。适合想从零建立 LLM 知识体系的学习者，以及需要把大模型真正落地到生产中的工程师；结构上按「入门 → 进阶 → 精通 → 速查」递进，并提供官方权威学习资源与库内关联笔记。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下内容均以官方发布与权威来源为准；社区二手信息与未确认的版本号需回源核对，标注「以官方文档为准」的条目请勿直接引用为确定事实。

| 版本 / 更新 | 关键更新点 | 来源 |
| --- | --- | --- |
| vLLM v0.32.0（2026 年 10 月） | 814 次提交、363 位贡献者（121 位新贡献者）；默认启用 `POST /v1/systemone` 结构化决策端点（choice/noul/score）；NVFP4 低精度 KV Cache 扩展到 SM8x/SM12x/SM90；Model Runner V2 在 ROCm 上成为默认；移除 Python 3.10、收紧默认 CORS、约束 transformers/tokenizers 版本等破坏性变更。 | [vLLM v0.32.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.32.0) |
| LangChain / LangGraph 1.0（2025 年 10 月 GA） | `createAgent` 取代 LangGraph 的 `createReactAgent`，成为构建智能体的标准方式；新增跨供应商标准内容块 `contentBlocks`；`langchain` 包精简，旧功能迁至 `@langchain/classic`。 | [LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones](https://www.langchain.com/blog/langchain-langgraph-1dot0) |
| Model Context Protocol（MCP）规范 2026-07-28 修订 | 协议走向无状态：移除协议级会话与 `initialize`/`notifications`/`initialized` 握手，每请求携带版本与能力；新增 MRTR 多轮请求模式（`InputRequiredResult`）、`tasks` 官方扩展、`server/discover` 端点；Roots/Sampling/Logging 进入弃用窗口。 | [MCP Specification 2026-07-28 — Key Changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog) |
| Anthropic Agent Skills（2025 年 12 月发布，2026 年 10 月捐赠） | 2025 年 12 月作为开放标准发布；2026 年 10 月捐赠给 Linux 基金会旗下 Agentic AI Foundation（AAIF）；超 70 个智能体平台已集成（含 ChatGPT、Cursor、GitHub Copilot、VS Code），公开 Skills 约 100 万个、累计安装约 2.8 亿次。 | [Donating Agent Skills to the Agentic AI Foundation](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) |
| OpenAI Agents SDK（2026 年 4 月 15 日更新） | 引入受控沙箱（sandbox）执行、可检查的模型原生 harness 与可配置记忆；harness 与沙箱可同机或异地运行，支持容器提供商与外部存储挂载、会话快照恢复。 | [OpenAI Agents SDK 更新（gihyo 技术报道）](https://gihyo.jp/article/2026/04/openai-agents-sdk-updates) |
| Qwen3.5-397B-A17B（Qwen3.5-Plus，2026 年 2 月 16 日） | 阿里巴巴开源的原生多模态基础模型：线性注意力 + 稀疏 MoE，总参数 397B、激活约 17B；处理文本/图像/视频并生成文本，支持 201 种语言与方言，定位高效推理部署。 | [Alibaba Open-Sources Qwen3.5](https://www.alibabagroup.com/en-US/document-1960233590314762240) |
| SGLang（截至 2026 年 11 月初） | 最新稳定版为 v0.5.20（后续小版本号以官方仓库为准），聚焦 SM120（Blackwell）、dLLM serving 路线与异构后端 KV 缓存管理。 | [sgl-project/sglang](https://github.com/sgl-project/sglang) |
| Hugging Face Transformers v5.x | v5.19.0 于 2026-10-05 发布，其后更新至 v5.22.x；对 Flash Attention 性能回归、MoE 解码优化等做了修复（最新版本号以官方仓库为准）。 | [Hugging Face Transformers Releases](https://github.com/huggingface/transformers/releases) |

> [!warning] 升级提示
> vLLM v0.32.0 包含移除 Python 3.10、收紧默认 CORS、约束 transformers/tokenizers 版本等破坏性变更；生产环境升级前务必核对自身依赖与调用方，避免升级后接口或运行环境不兼容。

## 二、入门篇

### 2.1 基础概念

> [!note] 核心认知
> **Transformer 的核心是自注意力（Self-Attention）**：用 Q/K/V 三个投影计算词与词之间的相关性，多头注意力（Multi-Head Attention）并行捕捉不同类型的语义关系。LLM 的完整流水线是「tokenization → embedding → 注意力层 → 采样/解码」。

- **自注意力机制**：输入经线性投影得到查询（Query）、键（Key）、值（Value）；注意力权重由 Q 与 K 的缩放点积决定，再对 V 加权求和。公式核心为 $\text{Attention}(Q,K,V)=\text{softmax}(QK^{T}/\sqrt{d_k})V$。
- **多头注意力**：将注意力在多个子空间并行计算后拼接，使模型同时关注位置、语法、语义等不同维度的关系。详见 [[自然语言处理-BERT模型详解]]。
- **自回归生成**：模型逐个 token 预测下一个词，形成 `输入 → 预测下一个 token → 拼接 → 继续预测` 的循环。
- **KV Cache**：缓存历史 token 的 Key/Value，避免每步重复计算，是自回归解码加速的关键，也是后续推理优化的核心抓手。

**常用解码策略**

| 策略 | 说明 | 适用场景 |
| --- | --- | --- |
| 贪心（Greedy） | 每步取概率最高的 token | 结果稳定、可复现的确定性任务 |
| 温度采样（Temperature） | 通过温度系数调整概率分布，温度越低越保守 | 需要平衡多样性与质量 |
| Top-p（核采样） | 只在累积概率达 p 的候选集中采样 | 通用、控制随机性较精细 |
| Top-k | 只在概率最高的 k 个候选中采样 | 简单限制候选集 |

**Prompt 工程入门**：先明确成功标准、建立评估测试集、写出第一版提示，再迭代优化。基础技巧包括：

- **清晰指令**：说清任务目标、约束与输出格式。
- **少样本示例（Few-shot）**：给出 1–3 个输入输出示例，示范期望风格。
- **角色设定**：为模型设定专家角色，稳定输出语气与专业度。

**RAG 入门五步**：切分（chunking）→ 向量化（embedding）→ 索引（index）→ 检索（retrieval）→ 生成（generation）。

> [!tip] 顺序建议
> **先优化源文档的结构与写作，再谈检索调优**。源文档本身结构混乱时，再高级的检索算法也无法救回质量。

### 2.2 环境准备

- **语言与包管理**：准备 Python 环境（建议 Python 3.11+），使用 `venv`/`uv`/`conda` 隔离依赖；注意 vLLM v0.32.0 已移除 Python 3.10。
- **模型获取**：准备模型 API Key（如 OpenAI、Claude、通义等），或下载本地模型权重（Hugging Face / ModelScope）。
- **算力规划**：按模型规模估算 GPU 与显存；显存不足时优先考虑量化或 QLoRA，而非强行全量微调。
- **推理框架**：通用生产首选 vLLM；资源受限或 CPU 场景考虑 llama.cpp；前缀共享高的 Agent/RAG 负载可评估 SGLang。
- **向量库**：按规模选择 pgvector（PostgreSQL 生态）、LanceDB（轻量嵌入式）、Milvus（大规模分布式）。

> [!example] 环境快速检查
> ```bash
> # 检查 Python 版本（vLLM v0.32.0 起不再支持 3.10）
> python --version
>
> # 安装推理与开发基础依赖（按需取舍）
> pip install "vllm>=0.32.0"
> pip install langchain langgraph
> pip install llama-index
> pip install pymilvus pgvector
> ```

### 2.3 第一个实践（含代码示例）

**目标**：用 LangChain 1.0 的 `createAgent` 搭建一个带工具的最小智能体，跑通「模型调用 + 工具选择」循环。

> [!note] 前置知识
> 建议先完成 [[AI学习路径]] 中的基础阶段，并对 [[AI工具-LangChain实战]] 的框架概念有初步认识。

> [!example] Python：最小工具调用智能体
> ```python
> from langchain.agents import create_agent
> from langchain_openai import ChatOpenAI
>
> # 1. 选择模型：API 或本地推理服务（如 vLLM 提供的 OpenAI 兼容接口）
> model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
>
> # 2. 定义工具：模型通过名称与描述自行决定何时调用
> def get_current_time() -> str:
>     """返回当前本地时间，用于回答与时间相关的查询。"""
>     import datetime
>     return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
>
> # 3. 构建智能体：createAgent 取代旧版 createReactAgent
> agent = create_agent(
>     model=model,
>     tools=[get_current_time],
>     prompt="你是一个严谨的助手，涉及时间问题时必须调用工具，不要凭记忆编造。",
> )
>
> # 4. 运行：观察模型的推理、工具调用与最终回答
> for chunk in agent.stream({"messages": [("user", "现在几点了？")]}):
>     print(chunk)
> ```

> [!warning] 密钥安全
> 不要将 API Key 硬编码进代码。使用环境变量或密钥管理服务注入，避免泄露到版本库。

## 三、进阶篇

### 3.1 核心机制

**注意力与 KV Cache**

- **缩放点积注意力**：Q/K 点积后除以 $\sqrt{d_k}$ 再做 softmax，防止梯度消失。
- **KV Cache 的取舍**：用显存换取计算，减少重复前向计算；但缓存随序列长度线性增长，是显存占用的主要来源，催生了后续的量化与前缀复用优化。

**Prompt 进阶**

- **结构化输出约束**：用 JSON Schema、函数调用或 XML/结构化标签约束输出，降低格式不稳定。
- **工具调用（Function Calling）**：让模型输出结构化的调用请求，由外部执行后回传结果。
- **长上下文组织与上下文压缩**：对超长上下文做摘要、裁剪与分层组织，控制成本与注意力稀释。
- **多轮对话管理**：维护历史消息、控制窗口长度，必要时做历史压缩与记忆外置。
- **思维链（CoT）与提示链（Prompt Chaining）**：CoT 让模型显式推理；提示链把复杂任务拆成多步、逐段调用。

**RAG 优化**

- **混合检索**：向量检索 + BM25 关键词检索互补，再用 Reciprocal Rank Fusion（RRF）融合排序。
- **查询改写**：将口语化查询改写为更利于检索的表述，提升召回。
- **重排序（Rerank）**：对召回结果用交叉编码器等模型二次排序，提升精度。
- **上下文工程（Context Engineering）**：从「塞更多内容」转向精心编排上下文内容，减少噪声。
- **Agentic RAG**：多步检索——先检索再判断是否需要补充检索，形成多跳问答。

**微调机制**

> [!note] 三种微调路线
> - **全量微调**：更新全部参数，效果上限高，但成本与显存开销最大。
> - **LoRA**：仅训练低秩适配矩阵，通常仅训练 0.1%–3% 的参数，**不增加推理成本**、效果更稳定。
> - **QLoRA**：在 LoRA 之上叠加 NF4 量化、双重量化与分页优化器，显存需求极低。

LoRA 用低秩矩阵适配权重，QLoRA 在其上叠加量化，实现低成本大模型微调。

**推理优化核心手段**

- **连续批处理（Continuous Batching）**：动态地把请求加入批次，提升吞吐。
- **PagedAttention**：以分页方式管理 KV Cache，显著提高显存利用率。
- **KV Cache 量化与前缀复用**：低精度缓存（如 NVFP4）与前缀树复用，降低显存与重复计算。
- **投机解码（Speculative Decoding）**：用小模型先草拟多个 token，大模型并行验证，加速解码。
- **FlashAttention**：通过分块与重算优化注意力的计算与显存访问。

### 3.2 最佳实践

- **先评估、后调优**：官方指南一致强调先定义成功指标与测试集，再做提示或模型迭代。
- **框架侧**：用中间件控制动态提示、工具选择与上下文；配套可观测性（tracing）、评估（LLM-as-judge）与人在回路（human-in-the-loop）。
- **检索侧**：优先保证切分粒度合理与混合检索；引用要可溯源，便于核查。
- **微调侧**：按资源与目标选择全量 / LoRA / QLoRA，微调不增加推理成本。
- **部署侧**：以 OpenAI 兼容接口暴露服务，降低调用方迁移成本。

> [!tip] 评估闭环
> 建议至少维护三类资产：**测试集**（真实用例）、**指标**（准确率/格式合规/延迟等）、**基线**（当前版本对照）。每次改动都有可量化对照，避免「感觉变好了」的主观判断。

### 3.3 常见问题与排查

| 现象 | 可能原因 | 排查与对策 |
| --- | --- | --- |
| 检索不到 / 不准确 | 切分粒度不当、单一检索方式 | 检查切分粒度，启用向量 + BM25 混合检索，再加 rerank |
| 输出格式不稳定 | 约束不足、示例不够 | 加强结构化输出约束，补充少样本示例 |
| 显存不足（OOM） | 模型过大、缓存膨胀、全量微调 | 量化、QLoRA、KV Cache 量化、降低上下文长度 |
| 延迟高 | TTFT/TPOT 偏高、批处理与缓存命中差 | 排查 TTFT/TPOT，启用连续批处理与前缀缓存，评估投机解码 |
| 幻觉 | 缺乏外部知识接地 | 用 RAG 检索接地、引用溯源、事实校验 |
| 多轮对话失控 | 缺少对话级监控 | 增加对话级安全监控与策略执行 |

> [!warning] 多轮越狱
> **多轮越狱比单轮更难检测**。单轮安全指标不能替代部署安全，必须引入对话级监控与策略执行。

## 四、精通篇

### 4.1 架构与设计

**推理引擎选型矩阵**

| 引擎 | 核心优势 | 适用场景 | 代价 / 注意 |
| --- | --- | --- | --- |
| vLLM | PagedAttention + 连续批处理，显存利用率高；供应商中立、模型覆盖广 | 通用生产默认 | 需关注版本破坏性变更 |
| SGLang | RadixAttention 前缀树，高前缀共享负载优势明显（约 29% 吞吐优势） | Agent / RAG 等前缀共享高的负载 | 相对小众，生态与排障资源较少 |
| TensorRT-LLM | NVIDIA-only，深度调优后可比 vLLM 快 30%–50% | NVIDIA 专属、高并发、完成深度调优 | 搭建与重建成本高 |

> [!danger] 选型铁律
> **性能数字高度依赖负载形状，脱离负载谈吞吐没有意义。** 必须用贴近自身真实负载的压测数据做选型，而不是照搬榜单数字。

**Agent 架构**

- **模型原生 harness**：负责工具调用、审批、追踪（tracing），是智能体的控制核心。
- **沙箱（Sandbox）**：提供隔离的文件、命令、包执行环境，支持会话快照恢复；harness 与沙箱可同机或异地运行。
- **协议层**：MCP 已走向无状态，支持 MRTR 多轮请求；多智能体场景可配合 A2A 等协议。

**多模态架构**

原生多模态模型（如 Qwen3.5 的线性注意力 + 稀疏 MoE）直接融合文本/图像/视频，支持长视频理解与 GUI 智能体；**推理成本是多模态落地的核心约束**。

### 4.2 生产实践

- **多模型 / 多节点服务**：按模型与流量划分服务实例，做负载均衡与版本隔离。
- **Prefill/Decode 分离（PD 分离）**：将预填充与解码阶段拆分，优化不同阶段的资源利用与延迟。
- **专家负载均衡（EPLB）**：针对 MoE 模型，在多个专家节点间均衡负载，避免热点。
- **显存释放与休眠（sleep）**：空闲时释放显存、按需唤醒，降低闲置成本。
- **多种量化**：FP8、NVFP4、AWQ、GPTQ 等，按精度与吞吐取舍。
- **OpenAI 兼容接口**：统一对外协议，降低多供应商迁移成本。

**vLLM 生产要点**

> [!info] vLLM v0.32.0 关键变更
> 引入 `/v1/systemone` 结构化决策端点、Model Runner V2、低精度 KV Cache（NVFP4 扩展到 SM8x/SM12x/SM90）；升级需注意破坏性变更：**移除 Python 3.10、默认 CORS 收紧、transformers/tokenizers 版本约束**。

**可观测性是生产必备**

- **Tracing**：全链路追踪每次调用，定位延迟与错误来源。
- **评估（LLM-as-judge）**：用模型对输出质量做自动评分，辅助回归检测。
- **人在回路（Human-in-the-loop）**：高风险环节保留人工审核。
- **告警**：对延迟、错误率、幻觉与安全异常设置阈值告警。

### 4.3 生态与前沿

- **Agent Skills 开放标准**：以 `SKILL.md` 文件夹封装领域知识、跨平台复用；由 Anthropic 于 2026 年 10 月捐赠给 AAIF，走向社区共治，超 70 个平台已集成。
- **MCP 规范持续演进**：2026-07-28 版走向无状态，新增 MRTR 多轮请求、`tasks` 扩展与 `server/discover` 端点，是智能体连接工具与数据的事实标准。
- **框架生态**：LangChain v1 以 `createAgent` + 中间件为标准建智能体方式，旧功能迁至 `@langchain/classic`；LlamaIndex 用检索相关原语做数据接入；OpenAI Agents SDK 以 Agent/Handoff/Guardrail 原语起步。
- **模型选型需多维评估**：响应速度、吞吐、推理准确率、对话质量、安全行为，**不能只看基准分数**。
- **安全与幻觉治理**：幻觉靠检索接地、引用溯源、事实校验；前沿模型评估出现沙箱逃逸案例，需在技术上强制边界。

> [!tip] 前沿跟踪方法
> 版本号与新特性以**官方仓库/文档为准**，社区二手信息需回源核对。优先订阅官方 release 与规范 changelog。

## 五、核心要点速查

1. Transformer 的核心是自注意力：用 Q/K/V 计算词与词相关性，多头并行捕捉多种关系。
2. LLM 自回归逐 token 生成，KV Cache 缓存历史键值，是推理优化的关键抓手。
3. Prompt 工程先评估后调优：先定义成功标准与测试集，再迭代提示。
4. 常用提示技巧：清晰指令、少样本示例、角色设定、XML/结构化标签、思维链。
5. RAG 五步：切分 → 向量化 → 索引 → 检索 → 生成，检索质量决定生成质量。
6. RAG 进阶用混合检索（向量 + BM25）与重排序，必要时引入上下文工程与 Agentic RAG。
7. 模型微调三选：全量、LoRA（0.1%–3% 参数）、QLoRA（量化降显存）；微调不增加推理成本。
8. LoRA 用低秩矩阵适配权重，QLoRA 在其上叠加量化，实现低成本大模型微调。
9. 推理优化核心手段：连续批处理、PagedAttention、KV Cache 量化/前缀复用、投机解码、FlashAttention。
10. vLLM 是通用生产默认（供应商中立、OpenAI 兼容），SGLang 适合前缀共享高的 Agent/RAG 负载。
11. 推理引擎选型看负载形状，脱离负载谈吞吐没有意义。
12. Agent 核心是「模型调用 + 工具选择」循环，关键能力含工具调用、规划、记忆与多轮执行。
13. MCP 已是智能体连接工具与数据的事实标准，2026-07-28 版走向无状态。
14. Agent Skills 以 SKILL.md 文件夹封装领域知识、跨平台复用，2026 年 10 月捐给 AAIF。
15. LangChain v1 以 createAgent + 中间件为标准建智能体方式，旧功能迁至 @langchain/classic。
16. 可观测性是生产必备：tracing、评估（LLM-as-judge）、人在回路与告警。
17. 多模态模型正走向原生融合（文本/图像/视频）与高效推理，成本是落地关键。
18. 模型选型需多维评估：延迟、吞吐、推理质量、对话质量与安全行为。
19. 幻觉治理靠检索接地、引用溯源与事实校验；多轮对话需额外的对话级安全监控。
20. 版本号与新特性以官方仓库/文档为准，社区二手信息需回源核对。

## 六、学习资源

> [!note] 来源说明
> 以下为本文所依据的外部官方文档与权威来源，均为标准 Markdown 链接。

1. [vLLM v0.32.0 Release Notes（官方 GitHub）](https://github.com/vllm-project/vllm/releases/tag/v0.32.0)
2. [LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones（官方博客）](https://www.langchain.com/blog/langchain-langgraph-1dot0)
3. [What's new in LangChain v1（官方文档）](https://docs.langchain.com/oss/javascript/releases/langchain-v1)
4. [Model Context Protocol Specification 2026-07-28 — Key Changes（官方规范）](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
5. [Donating Agent Skills to the Agentic AI Foundation（Anthropic 官方）](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)
6. [Alibaba Open-Sources Qwen3.5, A Natively Multimodal Model Built For High-Efficiency Inference（阿里巴巴官方）](https://www.alibabagroup.com/en-US/document-1960233590314762240)
7. [Prompt engineering overview（Anthropic / Claude 官方文档）](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
8. [OpenAI Agents SDK 更新：サンドボックス対応やメモリ制御を追加（gihyo 技术报道）](https://gihyo.jp/article/2026/04/openai-agents-sdk-updates)
9. [编写优化 RAG 应用程序的最佳实践（AWS 官方指南）](https://docs.aws.amazon.com/zh_cn/prescriptive-guidance/latest/writing-best-practices-rag/writing-best-practices-rag.pdf)
10. [Announcing Retrieval Harness（LlamaIndex 官方博客）](https://www.llamaindex.ai/blog/announcing-retrieval-harness)
11. [DB-Engines Ranking of Vector DBMS（权威数据库排行）](https://db-engines.com/en/ranking/vector+dbms)
12. [Hugging Face Transformers Releases（官方仓库）](https://github.com/huggingface/transformers/releases)

## 七、关联笔记

- [[AI学习路径]]
- [[机器学习-机器学习基础入门总结]]
- [[机器学习-线性回归]]
- [[深度学习-PyTorch入门]]
- [[深度学习-TensorFlow使用笔记]]
- [[自然语言处理-BERT模型详解]]
- [[AI工具-LangChain实战]]
- [[AI应用场景分析]]
- [[40-AI技术]]

## 八、变更记录

- 2026-11-18 首次创建
