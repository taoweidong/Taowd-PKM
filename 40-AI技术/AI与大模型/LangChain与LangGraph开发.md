---
title: LangChain与LangGraph开发
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI与大模型
  - LangChain
  - LangGraph
  - Agent
aliases:
  - LangChain与LangGraph
  - LangChain LangGraph 开发
source: 网络资料整理
---

# LangChain与LangGraph开发

> [!summary] 摘要
> 本文聚焦**大模型应用开发的编排层**：LangChain 提供模型调用、工具、提示与集成的统一接口，LangGraph 以「状态图（State Graph）」表达可控的智能体流程，二者共同构成 2026 年构建 Agent、RAG 与多步流程的主流工程底座。内容覆盖最新动态、基础概念、核心机制、可运行的实践步骤、最佳实践与常见坑、速查要点与学习资源，适合已具备 LLM 基础、希望把模型能力落地为稳定生产应用的工程师。

## 一、最新动态（截至 2026-11）

> [!info] 时效说明
> 以下版本号与日期均来自 2026-11 检索时点的官方来源；框架迭代极快，使用前请以官方仓库当日状态复核。

- **LangChain v1.0 GA**：以 `create_agent` 作为构建 Agent 的标准方式，**取代 LangGraph 旧的 `createReactAgent`**；统一 **content blocks（内容块）**；精简包结构，遗留能力移入 `@langchain/classic`。来源：[LangChain v1 说明](https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1)
- **LangChain v1.4.3（2026-09-28 发布）**：v1.0 GA 后的持续修复版本。来源：[LangChain Changelog](https://docs.langchain.org/oss/javascript/releases/changelog)
- **LangGraph v1.1.0（2026-03-10 发布）**：引入 `version="v2"` 的**类型安全 stream/invoke**，支持 Pydantic / dataclass 自动强转；当前 langgraph 最新版本号以官方仓库为准（检索时点为 1.2.18）。来源：[LangGraph Releases](https://github.com/langchain-ai/langgraph)
- **MCP 2026-07-28 规范发布**：协议核心转向**无状态请求/响应模型**，加强授权、官方扩展转正，已成为 Agent 连接外部工具与数据的事实标准，官方称月 SDK 下载量超 4 亿。来源：[MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/index)

> [!warning] 升级提示
> LangChain 1.0 重写后仍存在破坏性变更历史（包结构调整、旧接口迁移）。**生产环境务必锁定依赖版本**，升级前核对调用方与依赖树。

## 二、基础概念

- **LangChain**：大模型应用框架，把模型调用、提示词管理、工具调用、结构化输出、外部集成（向量库、数据库、API）封装为统一接口，降低从「单次调用」到「应用」的工程成本。
- **LangGraph**：基于**状态图（State Graph）**的编排框架。把智能体流程抽象为节点（Node）与边（Edge），状态在节点间流转并可持久化，从而对复杂、循环、可回退的流程做确定性控制。
- **Agent（智能体）**：以「模型调用 + 工具选择」为核心的循环——模型决定是否调用工具、调用哪个工具、用工具结果继续推理，直到给出最终回答。范式基础是 ReAct（Reasoning + Acting，[论文](https://arxiv.org/abs/2210.03629)）。
- **Tool / 工具**：可被模型调用的函数，通过名称与描述让模型自主决定何时调用；是 Agent 与外部世界交互的入口。
- **State / 状态**：图节点之间传递的数据结构，可定义为 Pydantic 模型或 dataclass，支持在图执行过程中读写、累加与持久化。
- **中间件（Middleware）**：在模型调用前后插入逻辑，用于动态改写提示、限流、超时、错误重试与可观测性埋点。

**分工关系**：LangChain 偏「模型接入与组件集成」，LangGraph 偏「流程编排与状态控制」。LangChain 的 `create_agent` 本身也构建在 LangGraph 之上，二者配合使用是当前主流做法。

## 三、核心机制

**1. `create_agent` 标准接口（LangChain v1）**

`create_agent(model, tools, prompt)` 取代 `createReactAgent`，内部完成「模型 → 工具循环 → 观察 → 再推理」的闭环，返回可直接 `invoke` / `stream` 的智能体。工具只需是带类型注解与 docstring 的普通函数，模型据此自行判断调用时机。

**2. 状态图（LangGraph）**

- **节点（Node）**：一个处理函数，接收当前 `state`，返回对 state 的更新（局部更新或整体替换）。
- **边（Edge）**：定义执行顺序，可为普通线性边，也可为**条件边（Conditional Edge）**，由状态动态决定下一步走向哪个分支。
- **状态持久化与断点**：状态可落盘，配合检查点（checkpoint）实现中断恢复、人在环审批与审计。
- **类型安全**：LangGraph v1.1.0 的 `version="v2"` 对 `stream`/`invoke` 做类型检查，并自动把输入强转为 Pydantic / dataclass，减少类型相关错误。

**3. 工具调用机制**

模型先输出结构化的调用请求（函数名 + 参数），由框架执行真实函数，再把结果回传，模型据此继续。工具描述越清晰、参数类型越明确，调用准确率越高。

**4. 内容块（Content Blocks）**

LangChain v1 统一了跨供应商的**内容块**表示，将文本、图片、文件等不同类型的内容用统一结构承载，便于在多家模型间迁移而不必改写上层逻辑。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境准备

```bash
# 建议 Python 3.11+；创建隔离环境
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# 安装 LangChain 与 LangGraph
pip install -U langchain langgraph
# 按模型供应商安装集成（示例：OpenAI）
pip install langchain-openai
```

### 4.2 用 `create_agent` 构建最小智能体

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# 1. 选择模型（可用 vLLM/Ollama 等提供的 OpenAI 兼容接口替换）
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. 定义工具：名称与 docstring 决定模型能否正确调用
def get_current_time() -> str:
    """返回当前本地时间，用于回答与时间相关的查询。"""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. 构建智能体：create_agent 取代旧版 createReactAgent
agent = create_agent(
    model=model,
    tools=[get_current_time],
    prompt="你是一个严谨的助手，涉及时间问题必须调用工具，不要凭记忆编造。",
)

# 4. 运行并观察推理与工具调用过程
for chunk in agent.stream({"messages": [("user", "现在几点了？")]}):
    print(chunk)
```

### 4.3 用 LangGraph 定义带条件分支的状态图

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动累加消息
    need_search: bool                        # 自定义控制字段


def call_model(state: AgentState) -> dict:
    # 真实场景中在此调用模型并做工具循环
    return {"messages": [("assistant", "已根据状态完成本轮处理。")]}


def should_continue(state: AgentState) -> str:
    # 条件边：根据状态决定下一步
    return "call_model" if state.get("need_search") else END


builder = StateGraph(AgentState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")
builder.add_conditional_edges("call_model", should_continue, {
    "call_model": "call_model",  # 需要继续时回到模型
    END: END,
})

app = builder.compile()
result = app.invoke(
    {"messages": [("user", "帮我查一下资料")], "need_search": True},
)
print(result["messages"][-1][1])
```

> [!warning] 密钥安全
> 不要将 API Key 硬编码进代码或提交到版本库，应通过环境变量或密钥管理服务注入。

## 五、最佳实践与常见坑

**最佳实践**

- **先锁定版本再开发**：LangChain 1.0 重写、LangGraph v1.1 引入 `version="v2"` 等均有破坏性变更，`pyproject.toml` / `requirements.txt` 中写死版本号，避免上游升级打挂。
- **工具设计优先**：工具名、docstring、参数类型要写清楚，模型调用准确率直接取决于这些描述。
- **先评估后调优**：建立测试集与基线，用可量化指标（准确率、格式合规、延迟）衡量改动，而不是凭感觉。
- **用中间件统一治理**：限流、超时、瞬时错误重试、动态提示改写统一交给中间件，避免散落在业务代码。
- **长流程用状态图 + 检查点**：可中断、可恢复、可审计，比纯线性调用更利于生产。
- **MCP 连接外部工具**：统一用 MCP 规范对接工具与数据源，降低对接与迁移成本。

**常见坑**

| 现象 | 原因 | 对策 |
| --- | --- | --- |
| 工具不被调用 / 调用错误 | 工具描述含糊、缺少参数类型 | 补充清晰 docstring 与类型注解，必要时在提示中说明使用场景 |
| 升级后报错、接口消失 | 破坏性变更与版本漂移 | 锁定版本；升级前查 changelog，必要时迁移至 `@langchain/classic` |
| 图执行顺序不符合预期 | 条件边映射或状态更新写错 | 检查 `add_conditional_edges` 的映射表与状态字段累加规则 |
| 多轮对话历史丢失或重复 | 消息未做累加（`add_messages`） | 用 `Annotated[list, add_messages]` 正确累加历史 |
| 输出格式不稳定 | 缺少结构化约束 | 用工具调用或 JSON Schema 约束输出，补充示例 |
| 长流程延迟高 | 未持久化状态、无断点 | 使用检查点持久化状态，必要时拆分流程 |

## 六、核心要点速查

1. LangChain v1.0 以 `create_agent` 为标准建 Agent 方式，取代 `createReactAgent`；遗留能力移入 `@langchain/classic`。
2. LangChain v1.4.3（2026-09-28）；LangGraph v1.1.0（2026-03-10）提供 `version="v2"` 类型安全 stream/invoke。
3. LangChain 偏模型接入与集成，LangGraph 偏状态图编排；`create_agent` 构建于 LangGraph 之上。
4. Agent 核心是「模型调用 + 工具选择」循环，ReAct 是其范式基础。
5. 工具用名称 + docstring + 参数类型描述，模型据此自主决定调用。
6. LangGraph 核心概念：节点、边、条件边、状态、检查点。
7. 状态更新用 `Annotated[list, add_messages]` 累加，避免消息丢失或重复。
8. 内容块（content blocks）统一跨供应商的内容表示，利于模型迁移。
9. MCP 2026-07-28 走向无状态，是 Agent 对接工具与数据的事实标准。
10. 生产第一原则：**锁定版本**，先评估后调优，用中间件统一治理限流/重试/可观测性。

## 七、学习资源

1. [LangChain v1 说明（官方文档）](https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1)
2. [LangChain Changelog（官方）](https://docs.langchain.org/oss/javascript/releases/changelog)
3. [LangGraph Releases（官方仓库）](https://github.com/langchain-ai/langgraph)
4. [LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones（官方博客）](https://www.langchain.com/blog/langchain-langgraph-1dot0)
5. [Model Context Protocol Specification 2026-07-28（官方规范）](https://modelcontextprotocol.io/specification/2026-07-28/index)
6. [ReAct: Synergizing Reasoning and Acting in Language Models（论文）](https://arxiv.org/abs/2210.03629)
7. [LangChain 官方文档（Agents）](https://docs.langchain.com/oss/python/langchain/agents)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[AI工具-LangChain实战]]

## 九、变更记录

- 2026-11-19：首次创建。
