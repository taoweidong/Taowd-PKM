---
title: 多Agent协作与编排
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI/大模型
  - AI/Agent
  - AI/多Agent
  - 编排
  - LangGraph
aliases:
  - 多智能体协作与编排
  - Multi-Agent Orchestration
source: 网络资料整理
---

# 多Agent协作与编排

> [!摘要] 摘要
> 本文聚焦「多 Agent 协作与编排」这一知识点：讲解多智能体（Multi-Agent）系统的分工思路、编排（Orchestration）与并行的区别，剖析确定性编排器、状态图流转、共享状态与人在环等核心机制，并给出基于 LangGraph / LangChain 的可运行实践步骤。适合已掌握单 Agent 工具调用、希望把复杂长程任务拆解为多角色协作的工程师。本文是 [[AI与大模型-从入门到精通]] 在 Agent 方向的深化，与 MCP 协议、Agent 框架共同构成智能体工程的落地主线。

## 一、最新动态（截至 2026-11）

> [!info] 来源说明
> 以下版本号与事实均来自 2026-11 检索时点的调研文件，框架迭代极快，实际使用前请以官方仓库当日状态复核。

- **LangChain v1.0 GA**：以 `create_agent` 作为构建 Agent 的标准方式，取代 LangGraph 的 `createReactAgent`，遗留能力移入 `@langchain/classic`；**LangChain v1.4.3 于 2026-09-28 发布**。来源：[LangChain Changelog](https://docs.langchain.org/oss/javascript/releases/changelog)
- **LangGraph v1.1.0（2026-03-10）**：引入 `version="v2"` 的类型安全 `stream`/`invoke`，支持 Pydantic/dataclass 自动强转；当前 `langgraph` 最新为 **1.2.18**（小版本号以官方仓库为准）。LangChain 的 `create_agent` 亦构建于 LangGraph 之上。来源：[LangGraph Releases](https://github.com/langchain-ai/docs/blob/933a2f92/src/oss/python/releases/changelog.mdx)
- **MCP 规范 2026-07-28 发布**：第五个规范版本，核心转向**无状态请求/响应模型**（可部署到 serverless/边缘），加强授权并让官方扩展转正。官方称 MCP 月度 SDK 下载量已超 **4 亿**、较上一年增长 4 倍，已成为 Agent 连接外部工具与数据的事实标准，是多 Agent 系统共享工具层的基础。来源：[MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/index)
- **确定性编排范式落地**：以确定性编排器协调多个专业 Agent 的思路已出现工程化实例——「Cortex」用**确定性有限状态机**编排 11 个专业 Agent，配合分层人在环与零 token 开销的发言者选择，完成长程异构任务。来源：[Zenodo 记录 20819131](https://zenodo.org/records/20819131)

> [!warning] 写作与使用提示
> 编排框架与协议仍在快速演进，本文不把任何版本写成绝对「最新」。涉及 `langgraph` 小版本号与 MCP 扩展细节时，以官方仓库/规范为准。

## 二、基础概念

**多 Agent（Multi-Agent）**：由多个具备独立目标、角色与工具集的智能体组成的系统，通过协作完成单一 Agent 难以承担的复杂任务。与「单 Agent + 多工具」的区别在于，各 Agent 有独立的**角色设定、提示词、可用工具与职责边界**，可以独立决策、再汇总结果。

**编排（Orchestration）**：用一个**确定性的控制流**协调多个 Agent 的执行顺序、数据流转与终止条件，例如「先由研究 Agent 搜集资料 → 再由写作 Agent 成稿 → 最后由评审 Agent 打分，未达标则回退」。编排强调**谁在何时做什么由外部控制流决定**，而不是交给模型自行协商。

**多 Agent 并行 ≠ 编排**：

- **多 Agent 并行**：多个 Agent 同时执行互不依赖的子任务，本质是「并发调度」，没有统一的中心化控制流。
- **编排**：强调**状态化、有序、可回退**的协调，通常是「串行 + 条件分支 + 循环」的图结构。

> [!note] 关键认知
> 编排的价值在于**确定性与可观测性**：当任务涉及多个专业环节（检索、编码、评审、审批）时，把流程固化为状态图，比让模型在长上下文里自行规划更稳定、更易复现、更易定位失败。

**常见拓扑结构**

| 拓扑 | 说明 | 适用场景 |
| --- | --- | --- |
| 主管-Worker（Supervisor-Worker） | 编排器分配任务、回收结果 | 任务可清晰拆解、需统一调度 |
| 流水线（Pipeline） | 按固定顺序逐级加工，上一步输出为下一步输入 | 阶段明确、有前后依赖 |
| 层级（Hierarchical） | 上层 Agent 分解目标、下层执行并汇总 | 长程、多层级目标 |
| 评审/辩论（Review/Debate） | 多个角色对同一产物迭代提意见 | 质量敏感、需多视角校验 |
| 动态协商（Dynamic） | 由模型决定交接给谁（handoff） | 路径不确定、需灵活路由 |

## 三、核心机制

**1. 编排器（Orchestrator）**
编排器是控制核心，负责：任务拆分、决定下一个执行的 Agent、传递共享状态、判断终止条件。推荐让编排器**保持确定性**——用状态机或状态图表达，而不是让模型自行决定全局流程，否则难以调试和保证一致性。

**2. 状态图（State Graph）**
把流程建模为「节点 = Agent 或步骤，边 = 条件转移」。节点内部执行单个 Agent，节点之间通过共享状态（State）传递数据。这是 LangGraph 的核心抽象，天然支持循环、分支与回退。

**3. 共享状态与上下文传递**
多个 Agent 通过统一的 State 结构交换数据（如 `draft`、`feedbacks`、`score`）。状态要**最小化、结构化**：只保留下游真正需要的字段，避免把各 Agent 的原始思考全部塞进共享上下文造成噪声与成本膨胀。

**4. 发言者选择（Speaker Selection）**
在多 Agent 共处一个上下文时，需要决定「此刻由谁发言」。工程实例（Cortex）通过**零 token 开销的发言者选择**，避免让模型消耗算力去推测该谁说话，直接由编排器指定。

**5. 人在环（Human-in-the-loop）**
对高风险或需确认的环节（发布、删除、对外发送、预算超限）保留人工审批节点。编排结构天然适合插入审批门，实现「分层人在环」。

**6. MCP 工具接入**
各 Agent 的工具层建议统一走 **MCP 2026-07-28 无状态请求/响应模型**，把「工具发现—调用—结果回传」标准化，降低多 Agent 间的工具适配成本。

**7. 终止与收敛控制**
必须显式定义终止条件：最大步数、分数达标阈值、超时、错误重试上限。否则多 Agent 循环容易陷入「打分—改写—再打分」的无限循环。

## 四、实践步骤（含代码/命令示例）

**步骤 0：环境准备**

```bash
# Python 3.11+ 环境
python --version

# 安装编排相关依赖（按需取舍）
pip install "langgraph>=1.1.0" "langchain>=1.0"
pip install langchain-openai  # 或对接 vLLM 等 OpenAI 兼容服务
```

**步骤 1：拆解任务，定义角色与状态**

明确各 Agent 的职责、输入输出，以及共享状态结构。下面是一个「写作 → 评审 → 达标即结束，未达标则重写」的最小编排。

```python
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class ReviewState(TypedDict):
    draft: str                       # 当前稿件
    feedbacks: Annotated[list[str], operator.add]  # 累积评审意见
    score: int                       # 评审得分，用于判断是否达标

def writer_node(state: ReviewState) -> dict:
    """写作 Agent：依据评审意见产出新稿件。"""
    feedback = state["feedbacks"][-1] if state["feedbacks"] else "请直接成稿。"
    draft = f"基于反馈「{feedback}」生成的稿件……"
    return {"draft": draft}

def reviewer_node(state: ReviewState) -> dict:
    """评审 Agent：对稿件打分并给出改进意见。"""
    score = 6 if "基于反馈" in state["draft"] else 4   # 简化示意
    feedback = "结构清晰，但论证不够充分，请补充数据支撑。"
    return {"score": score, "feedbacks": [feedback]}

def should_continue(state: ReviewState) -> str:
    """编排器：决定走回写作节点还是结束。"""
    return "reviewer" if state["score"] < 8 else END
```

**步骤 2：组装状态图并运行**

```python
def build_graph():
    graph = StateGraph(ReviewState)
    graph.add_node("writer", writer_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_edge(START, "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_conditional_edges("reviewer", should_continue, {"reviewer": "writer", END: END})
    return graph.compile()

app = build_graph()
result = app.invoke({"draft": "", "feedbacks": [], "score": 0})
print(result["draft"], result["score"])
```

**步骤 3：用 LangChain `create_agent` 构建带工具的子 Agent**

编排图中的每个节点，可以是调用 `create_agent` 构建的「子智能体」，由它负责该环节的工具选择与推理。

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def web_search(query: str) -> str:
    """检索资料，供写作环节调用。"""
    return f"关于「{query}」的检索结果摘要……"

sub_agent = create_agent(
    model=model,
    tools=[web_search],
    prompt="你是一个资料检索助手，仅依据工具返回结果作答，不得编造。",
)

# 把 sub_agent 作为状态图中的一个节点执行，即可与其他角色协作
```

**步骤 4：用 YAML 描述编排配置（便于版本化与评审）**

```yaml
# orchestration.yaml：描述多 Agent 编排，交由编排器解释执行
name: content-pipeline
max_steps: 5                       # 最大循环步数，防止死循环
termination:
  score_threshold: 8               # 评审分数达标即结束
  timeout_seconds: 300
agents:
  writer:
    prompt: "根据反馈撰写稿件，控制篇幅。"
    tools: []
  reviewer:
    prompt: "从结构、论据、语言三方面打分并给出改进意见。"
    tools: []
flow:
  start: writer
  steps:
    - from: writer
      to: reviewer
    - from: reviewer
      condition: "score < threshold"
      to: writer
      on_failure: stop              # 达到 max_steps 或超时则停止
```

**步骤 5：接入 MCP 工具，统一工具层**

```bash
# 以本地 MCP 服务为例（具体命令以所用客户端为准）
npx @modelcontextprotocol/server-filesystem /path/to/workspace
```

在子 Agent 的配置中声明 MCP 服务，即可让各角色复用同一套工具与数据源，避免每个 Agent 各自实现连接逻辑。

## 五、最佳实践与常见坑

**最佳实践**

- **先定评估与终止，再搭编排**：先明确「什么算完成」（分数阈值、步数上限、超时），再设计节点，避免搭完无法收敛。
- **编排器保持确定性**：全局控制流用状态图/状态机表达，不要交给模型自由协商；把「判断是否达标」写成确定性函数。
- **共享状态最小化、结构化**：只传下游需要的字段，用 TypedDict/Pydantic 约束，避免上下文污染与成本失控。
- **分层人在环**：高风险环节（发布、删除、对外发送）前置人工审批节点，其余环节自动流转。
- **工具标准化**：统一走 MCP，降低多 Agent 的工具适配与维护成本。
- **可观测性**：为每次节点执行打 trace（输入、输出、耗时、token），便于定位哪个环节失败或超时。
- **锁定框架版本**：LangChain 1.0 重写存在破坏性变更历史（`createReactAgent` 被取代、旧功能迁入 `@langchain/classic`），生产环境建议锁定版本并先在测试环境验证升级。

**常见坑**

| 现象 | 原因 | 对策 |
| --- | --- | --- |
| 无限循环改写 | 终止条件缺失或阈值设置不当 | 设 `max_steps`、分数阈值与超时，三重兜底 |
| 状态爆炸、上下文过长 | 共享状态塞入全部原始思考 | 结构化、最小化状态，只保留必要字段 |
| 错误被静默吞掉 | 子 Agent 未把失败显式写回状态 | 统一错误状态字段，失败即终止或转人工 |
| 编排混乱 | 让模型自行决定全局控制流 | 控制流交给确定性编排器，模型只负责本环节 |
| 成本失控 | 多 Agent 反复回退、token 叠加 | 控制回退次数，评估每一步是否有必要 |
| 版本不兼容 | 直接升级框架 | 锁定版本，升级前跑通回归用例 |

> [!warning] 概念边界
> 多 Agent 并非「越多越强」。角色过多会放大协调成本与 token 开销；当任务可以被单 Agent + 结构化提示完成时，优先用更简单的方案。

## 六、核心要点速查

1. **多 Agent** 是多个有独立角色、工具与职责边界的智能体；**编排** 是用确定性控制流协调它们，二者不等价。
2. **多 Agent 并行**强调并发执行，**编排**强调状态化、有序、可回退的流程。
3. 常见拓扑：主管-Worker、流水线、层级、评审/辩论、动态 handoff。
4. 编排器是控制核心，推荐用**确定性状态机/状态图**表达，而非交给模型自行规划全局流程。
5. **状态图**是主流抽象：节点 = Agent/步骤，边 = 条件转移，天然支持循环、分支与回退。
6. 共享状态要**最小化、结构化**，只保留下游真正需要的字段。
7. 发言者选择可用**零 token 开销**方式由编排器指定，避免模型反复推测该谁说话。
8. **人在环**用于高风险环节，编排结构天然支持插入审批门，实现分层人工介入。
9. 工具层建议统一走 **MCP 2026-07-28 无状态模型**，标准化工具发现与调用。
10. 必须显式定义**终止条件**：最大步数、分数阈值、超时，防止无限循环。
11. LangChain v1 以 `create_agent` 取代 `createReactAgent`，`create_agent` 构建于 LangGraph 之上。
12. LangGraph v1.1.0 的 `version="v2"` 提供类型安全的 `stream`/`invoke`；生产建议**锁定版本**。
13. 版本号与新特性以官方仓库/文档为准，社区二手信息需回源核对。

## 七、学习资源

1. [LangGraph Releases（官方仓库）](https://github.com/langchain-ai/docs/blob/933a2f92/src/oss/python/releases/changelog.mdx)
2. [LangChain Changelog（官方文档）](https://docs.langchain.org/oss/javascript/releases/changelog)
3. [Model Context Protocol Specification 2026-07-28（官方规范）](https://modelcontextprotocol.io/specification/2026-07-28/index)
4. [Cortex 确定性编排 11 个专业 Agent（Zenodo 记录）](https://zenodo.org/records/20819131)
5. [ReAct 论文（Yao 等，ICLR 2023，多 Agent 思考-行动-观察范式的基础）](https://arxiv.org/abs/2210.03629)
6. [LangChain Agents 官方文档（中间件、工具、限流与错误处理建议）](https://docs.langchain.com/oss/python/langchain/agents)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[LLM-Agent与MCP协议]]
- [[AI工具-LangChain实战]]
- [[AI应用场景分析]]
- [[AI学习路径]]

## 九、变更记录

- 2026-11-19：首次创建。
