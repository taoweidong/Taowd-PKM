---
title: Agent智能体开发基础
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI/大模型
  - AI/LLM
  - Agent
  - 智能体
  - MCP
aliases:
  - Agent开发基础
  - 智能体开发基础
source: 网络资料整理
---

# Agent智能体开发基础

> [!摘要] 摘要
> 本文聚焦「Agent 智能体」这一知识点的**开发基础**：从智能体的本质与核心范式出发，讲清「思考—行动—观察」循环、工具调用、规划、记忆、错误恢复等关键机制，并给出可直接运行的最小智能体与本地模型服务示例。内容以截至 2026-11 的官方动态为基准（LangChain v1、LangGraph v1.1、MCP 2026-07-28），适用于想要从零构建第一个可落地 Agent 的开发者，并梳理生产中常见的坑与排查方法。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本号与日期均来自 2026-11 检索时点的官方信息，框架迭代极快，写作与定稿前请以官方仓库当日状态复核；无法核实处已标注「以官方仓库为准」。

- **LangChain 进入 v1 世代**：**v1.0 GA** 以 `create_agent` 作为构建 Agent 的标准方式，取代 LangGraph 的 `createReactAgent`，遗留能力移入 `@langchain/classic`。**LangChain v1.4.3 于 2026-09-28 发布**。来源：[LangChain Changelog](https://docs.langchain.org/oss/javascript/releases/changelog)、[LangChain v1 说明](https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1)
- **LangGraph v1.1.0（2026-03-10）**：引入 `version="v2"` 的类型安全 stream/invoke，支持 Pydantic/dataclass 自动强转；当前 langgraph 最新版本为 1.2.18。来源：[LangGraph Releases](https://github.com/langchain-ai/docs/blob/933a2f92/src/oss/python/releases/changelog.mdx)
- **Model Context Protocol（MCP）2026-07-28 规范发布**：第五个规范版本，核心转向**无状态请求/响应模型**（可部署到 serverless/边缘），加强授权、官方扩展转正；官方称 MCP 月度 SDK 下载量已超 **4 亿**，较上一年增长 4 倍，已成为 Agent 连接外部工具与数据的事实标准。来源：[MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/index)、[Anthropic：Bringing MCP 2026-07-28 to Claude](https://websitemain.claude.com/blog/bringing-mcp-2026-07-28-to-claude)

> [!warning] 破坏性变更提示
> LangChain 1.0 重写、LangGraph v1.1 的 `version="v2"`、`create_agent` 取代旧接口等均属破坏性变更，生产项目应**锁定版本**并评估迁移动作，避免升级后接口不兼容。

## 二、基础概念

**Agent（智能体）** 是指以大语言模型为决策核心、能感知环境、自主规划并调用外部工具、多轮执行直到完成目标的系统。与「单次问答」不同，Agent 具备**闭环执行能力**：模型不只给答案，还能决定下一步做什么、观察结果、再决定是否继续。

**核心范式：ReAct（Reasoning + Acting）**。ReAct 论文（Yao 等，ICLR 2023）确立了「**思考—行动—观察**」交错的主流模式：模型先推理当前该做什么（Thought），再输出动作（Action，如调用工具），拿到观察结果（Observation）后进入下一轮推理。来源：[ReAct 论文](https://arxiv.org/abs/2210.03629)

**一个完整 Agent 的五个要素**：

- **模型（Model）**：决策大脑，负责推理、工具选择与最终回答。
- **工具（Tools）**：可被调用的外部能力，如搜索、数据库、代码执行、文件读写。
- **规划（Planning）**：把复杂目标拆解为可执行的步骤序列。
- **记忆（Memory）**：短期记忆（当前上下文）与长期记忆（外置存储）共同支撑多轮一致性。
- **执行与恢复（Execution & Recovery）**：驱动循环运行，并对超时、报错等异常做重试或降级。

**与相邻知识点的关系**：提示工程决定「单次指令质量」，微调决定「模型行为风格」，RAG 为生成提供外部知识接地，而 Agent 把这些能力**编排进一个可循环执行的流程**，是四者之上的应用层。

## 三、核心机制

**1. 思考—行动—观察循环**

Agent 的标准执行流是：模型推理 → 输出工具调用 → 宿主执行工具 → 将结果回填上下文 → 模型继续推理，直至产出最终答案或触发终止条件。关键约束是**每轮都保留完整历史**，让模型基于最新观察决策，而不是「无状态地重新猜测」。

**2. 工具调用（Function Calling）**

模型通过结构化输出声明要调用的函数名与参数，由宿主执行后回传结果。工具的**名称与描述是模型选择工具的依据**：描述越明确、边界越清晰，越能减少误调用。工具签名应保持简单、可预期，避免把复杂业务逻辑塞进一个工具。

**3. 规划与反思**

- **规划**：先分解任务再逐项执行，避免模型在长任务中「跑偏」。
- **反思**：对中间结果自检，发现错误时回退或调整策略，提升长程任务的成功率。

**4. 记忆**

- **短期记忆**：直接放在上下文窗口内，受长度与成本限制。
- **长期记忆**：外置到向量库/数据库，按相关性检索后注入，解决「会话太长、关键信息被稀释」的问题。

**5. 错误恢复与人在环**

生产级 Agent 必须处理限流、超时、瞬时错误等异常，LangChain 官方建议以**中间件**统一处理，而不是在业务代码里散落重试。高风险动作（如写库、发消息、执行命令）应保留**人在环（human-in-the-loop）**审核。

**6. MCP：连接工具与数据的标准协议**

MCP 将「Agent 如何发现并调用外部工具/数据源」标准化，使同一套智能体可跨工具复用。2026-07-28 版转向无状态请求/响应后，更易于部署到 serverless 与边缘环境。

## 四、实践步骤（含代码/命令示例）

**步骤 1：环境准备**

```bash
python --version          # 建议 Python 3.11+
pip install "langchain>=1.4.3" langgraph langchain-openai
```

**步骤 2：本地模型服务（可选，便于离线/私有数据）**

```bash
# 用 vLLM 启动 OpenAI 兼容服务，Agent 通过标准接口调用
vllm serve Qwen/Qwen3.5-32B --served-model-name qwen3.5 -tp 4
```

**步骤 3：定义工具**

```python
def search_docs(query: str) -> str:
    """根据关键词在文档库中检索，返回最相关的片段。"""
    # 实际项目在此接入向量检索或全文搜索，这里以简化逻辑示意
    hits = ["...检索结果片段..."]
    return "\n".join(hits[:3])
```

**步骤 4：用 LangChain 1.0 构建最小智能体**

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    model=model,
    tools=[search_docs],
    prompt=(
        "你是一个严谨的助手。涉及知识库问题时必须调用 search_docs 工具，"
        "不要凭记忆编造；拿到结果后再组织回答，并说明信息来源。"
    ),
)

for chunk in agent.stream({"messages": [("user", "帮我查一下公司报销制度")]}):
    print(chunk)
```

**步骤 5：接 MCP 工具（标准化扩展）**

```bash
# 以 MCP 协议接入外部工具服务（示例命令，具体以所用客户端为准）
npx @modelcontextprotocol/inspector   # 打开 MCP 调试器，验证工具发现与调用
```

**步骤 6：加中间件做错误恢复**

```python
from langchain.agents.middleware import RetryOnErrorMiddleware

agent = create_agent(
    model=model,
    tools=[search_docs],
    middleware=[RetryOnErrorMiddleware(max_retries=2, backoff=1.5)],
    prompt="...",
)
```

> [!warning] 密钥安全
> 不要将 API Key 硬编码进代码。通过环境变量或密钥管理服务注入，避免泄露到版本库。

## 五、最佳实践与常见坑

| 现象 | 可能原因 | 排查与对策 |
| --- | --- | --- |
| 模型不调用工具、直接回答 | 工具描述含糊、提示未强调 | 重写工具名称与描述，在提示中明确「必须调用」 |
| 工具调用参数错误 | 参数未做约束、缺少校验 | 用 Pydantic 定义参数结构，宿主侧加校验 |
| 多轮后上下文膨胀、成本暴涨 | 缺少记忆压缩 | 对历史做摘要/裁剪，长期信息外置到向量库 |
| 调用超时或限流 | 外部工具不稳定 | 用中间件统一重试、退避、超时与降级 |
| 长任务中途跑偏 | 缺少显式规划与检查点 | 先分解任务，每步校验中间结果并允许回退 |
| 升级后接口报错 | 框架破坏性变更 | 锁定版本，升级前对照官方 changelog 做回归 |
| 高风险操作被直接执行 | 缺少人在环 | 对写库、外发等动作加人工审核节点 |

> [!tip] 评估闭环
> 至少维护**测试集**（真实用例）、**指标**（成功率/延迟/工具误用率）、**基线**（当前版本对照），每次改动都有可量化对照，避免「感觉变好了」的主观判断。

## 六、核心要点速查

1. Agent 是以大模型为决策核心、能多轮「感知—决策—执行」的闭环系统，区别于单次问答。
2. 主流范式是 ReAct：思考（Thought）→ 行动（Action）→ 观察（Observation）循环，见 [ReAct 论文](https://arxiv.org/abs/2210.03629)。
3. 五要素：模型、工具、规划、记忆、执行与错误恢复，缺一不可。
4. 工具调用靠**名称与描述**引导模型选择，参数用结构化定义并加宿主侧校验。
5. 记忆分短期（上下文内）与长期（外置检索注入），长任务必须做记忆压缩。
6. MCP 2026-07-28 版转向无状态，是 Agent 连接工具与数据的事实标准。
7. LangChain v1 以 `create_agent` 为标准建智能体方式，取代 `createReactAgent`。
8. 错误恢复用中间件统一处理限流/超时/重试，高风险动作保留人在环。
9. 生产务必做可观测性：tracing、评估、告警与对话级安全监控。
10. 版本号与新特性以官方仓库/文档为准，生产项目锁定版本、规避破坏性变更。

## 七、学习资源

1. [ReAct: Synergizing Reasoning and Acting in Language Models（论文）](https://arxiv.org/abs/2210.03629)
2. [Model Context Protocol Specification 2026-07-28（官方规范）](https://modelcontextprotocol.io/specification/2026-07-28/index)
3. [Anthropic：Bringing MCP 2026-07-28 to Claude（官方博客）](https://websitemain.claude.com/blog/bringing-mcp-2026-07-28-to-claude)
4. [LangChain Agents（官方文档）](https://docs.langchain.com/oss/python/langchain/agents)
5. [LangChain Changelog（官方）](https://docs.langchain.org/oss/javascript/releases/changelog)
6. [LangChain v1 说明（官方）](https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1)
7. [LangGraph Releases（官方）](https://github.com/langchain-ai/docs/blob/933a2f92/src/oss/python/releases/changelog.mdx)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[AI工具-LangChain实战]]
- [[AI学习路径]]
- [[40-AI技术]]

## 九、变更记录

- 2026-11-19：首次创建。
