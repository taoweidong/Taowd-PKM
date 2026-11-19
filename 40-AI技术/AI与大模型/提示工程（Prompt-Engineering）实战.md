---
title: 提示工程（Prompt-Engineering）实战
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI与大模型
  - 提示工程
  - Prompt Engineering
  - 实战
aliases:
  - 提示工程
  - Prompt Engineering
source: 网络资料整理
---

# 提示工程（Prompt-Engineering）实战

> [!摘要] 摘要
> 本文聚焦**提示工程（Prompt Engineering）**这一知识点：从基础概念与底层机制讲起，给出可直接复用的实践步骤（含 Python、YAML、Bash 示例），并整理最佳实践、常见坑与速查清单。定位是[[AI与大模型-从入门到精通]]知识体系下的实战篇，适合需要在真实业务中稳定调用大模型、控制输出质量与格式的开发者。提示工程是**工程手段，不是模型能力的替代品**，需与微调、RAG 等技术互补使用。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下内容来自 2026 年 11 月的调研文件，版本号与日期均以官方发布为准；框架与模型迭代极快，落地前请回官方仓库复核。

- **官方指南持续更新**：OpenAI 官方《Best practices for prompt engineering with the OpenAI API》明确提示工程的常见有效格式与原则（清晰指令、示例、角色设定、输出规范等）；Anthropic 官方提示工程文档覆盖逐步思考（extended thinking）、上下文组织与工具使用。[OpenAI 提示工程最佳实践](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)、[Anthropic 提示工程概览](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- **模型上下文显著扩大**：OpenAI **GPT-5.5（2026 年 4 月旗舰，1M 上下文）**、GPT-5.3-Codex（2026-02-05，首个 Codex+GPT-5 训练栈融合的 agentic 编码模型）；Anthropic **Claude Fable 5.2 / Mythos 5.2（2026-11-11 发布）**，输出速度较 5.1 提升约 30%。长上下文意味着提示组织与上下文管理的重要性上升。[OpenAI 模型发布说明](https://help.openai.com/en/articles/9624314-model-release-notes)、[Anthropic Claude 发布报道](https://cloudfresh.com/gc/news/claude-fable-5-2-and-mythos-5-2/)
- **Agent 与工具调用成为提示工程的延伸**：**MCP 2026-07-28 规范**发布，核心转向无状态请求/响应模型，官方称月 SDK 下载量已超 4 亿。提示中的系统指令、工具描述与角色设定，正逐步被标准化封装。[MCP 规范 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/index)
- **框架侧**：LangChain **v1.0 GA** 以 `create_agent` 作为构建 Agent 的标准方式（取代 LangGraph 的 `createReactAgent`），遗留能力移入 `@langchain/classic`；**LangChain v1.4.3（2026-09-28）**。生产使用建议锁定版本。[LangChain Changelog](https://docs.langchain.org/oss/javascript/releases/changelog)
- **开源模型侧**：Qwen3.5 / Qwen3.6 / Qwen3.8、DeepSeek-V4/V4.1、GLM-5.x 等构成主要开源阵营，中文场景常以 Qwen 系为默认。具体模型版本与能力以官方模型卡为准。

## 二、基础概念

- **定义**：提示工程是通过**设计、组织输入提示**，稳定、可控地激发模型完成特定任务的方法。它不改变模型权重，而是通过输入侧的工程手段影响输出。
- **定位**：提示工程是**工程手段而非模型能力替代**。它解决"如何调用"的问题，无法凭空补足模型不具备的知识；知识性、领域性问题应交给微调或 RAG，三者互补。
- **提示的基本组成**：
  - **角色设定**：给模型一个身份（如"资深数据分析师"），稳定语气与专业度。
  - **任务指令**：说清"做什么"，动词明确、目标具体。
  - **背景上下文**：提供必要事实、规则、参考资料。
  - **示例（Few-shot）**：给出 1–3 个输入输出样例，示范期望风格与格式。
  - **输出规范**：明确格式（Markdown、JSON）、长度、结构与约束。
- **关键参数**：`temperature`（温度，越低越稳定）、`top_p`（核采样，控制候选集）、`top_k`、`max_tokens`。参数与提示需配合调优。

## 三、核心机制

- **下一个 token 预测**：LLM 自回归地逐 token 生成，提示文本会进入前向计算、直接改变条件概率分布。因此**提示措辞、顺序与详略都会影响结果**。
- **上下文窗口与注意力**：提示全部进入上下文，但模型对长上下文的中间信息敏感度下降（"lost in the middle"现象）。**关键指令与约束应放在开头或结尾，而非埋在中间**。
- **温度与采样**：温度接近 0 时输出确定性强，适合抽取、分类、代码；需要创意或多样性时适度提高温度，并配合 `top_p` 控制。
- **少样本学习（Few-shot）**：示例把"任务格式与风格"具象化，比纯指令更稳定，是格式类任务的首选。
- **思维链（CoT）**：要求模型"先推理、后作答"，显式暴露中间步骤，显著提升复杂推理与计算的准确率。
- **结构化输出**：用 JSON Schema、函数调用或结构化标签约束输出，降低格式不稳定。
- **工具调用（Function Calling）**：模型输出结构化调用请求，由外部执行后回传结果，是提示工程与 Agent 的衔接点。
- **提示链与上下文工程**：复杂任务拆成多步、逐段调用（提示链）；长上下文通过摘要、裁剪、分层组织来控制成本与注意力稀释（上下文工程）。

## 四、实践步骤（含代码/命令示例）

**推荐流程**：明确目标与评估标准 → 写第一版提示 → 结构化沉淀模板 → 迭代优化 → 代码验证 → 回归管理。

**1. 明确目标与评估标准，建立测试集**

先定义"成功"是什么，再用真实用例建测试集，避免"感觉变好了"的主观判断。

**2. 写第一版提示，用模板沉淀**

```yaml
prompt_template:
  version: v2
  role: 资深技术文档工程师
  task: 将用户提供的会议纪要改写为结构化技术文档
  constraints:
    - 不得新增事实，仅做重组与润色
    - 保留原始要点，删除重复内容
  output_format:
    type: markdown
    sections: [标题, 背景, 结论, 待办事项]
  examples:
    - input: "上周讨论了接口联调进度和排期。"
      output: "## 背景\n接口联调按计划推进。\n## 结论\n……"
```

**3. 用 Python 调用模型验证提示**

```python
from openai import OpenAI

client = OpenAI()  # 从环境变量 OPENAI_API_KEY 读取，勿硬编码

resp = client.chat.completions.create(
    model="gpt-5.5",          # 具体模型名以官方文档当日为准
    temperature=0.2,
    messages=[
        {"role": "system", "content": "你是一名严谨的客服助手，只依据给定信息回答，不确定时明确说明。"},
        {"role": "user", "content": "用户反馈：订单未收到，要求退款。请给出回复。"},
    ],
)
print(resp.choices[0].message.content)
```

**4. 结构化输出与函数调用**

```python
from anthropic import Anthropic

client = Anthropic()  # 从环境变量 ANTHROPIC_API_KEY 读取
msg = client.messages.create(
    model="claude-fable-5-2",  # 具体模型名以官方文档当日为准
    max_tokens=1024,
    system="你是资深数据分析师，回答须给出依据与计算过程，不确定时标注。",
    messages=[{"role": "user", "content": "分析近三个月销售环比变化，输出结论与依据。"}],
)
print(msg.content[0].text)
```

**5. 用 Bash 做提示回归测试**

```bash
# 把提示版本写入文件，便于版本管理与回滚
cat > prompts/v2-summary.txt <<'EOF'
你是严谨的摘要助手：只依据原文摘要，保留关键事实，不超过 100 字。
EOF

# 逐条运行测试集并统计通过率
pass=0; total=0
for q in tests/cases/*.txt; do
  total=$((total + 1))
  out=$(openai chat -f "$q" -p prompts/v2-summary.txt)
  if echo "$out" | grep -q "[0-9]"; then pass=$((pass + 1)); fi
done
echo "通过率：$pass/$total"
```

**6. 多轮对话与 Agent 提示**

多轮场景在系统提示中明确"何时调用工具、何时请求人工"，并维护对话历史与窗口长度，必要时压缩历史或外置记忆。

## 五、最佳实践与常见坑

- **先评估、后调优**：先定指标与测试集，再迭代提示；每次**只改一个变量**，便于归因。
- **指令具体可执行**：避免"请好好写"这类模糊表述，改用"输出不超过 100 字、分三点、用 Markdown"。
- **约束与示例并用**：格式不稳定时优先补示例，而非堆指令；指令过长会稀释注意力、增加成本。
- **控制温度**：抽取/分类/代码用低温度；创意写作可适度提高，但避免盲目拉满。
- **不要把提示当万能药**：知识性幻觉、领域术语缺失，应交给 RAG 检索接地或微调，而不是反复改提示。
- **注意长上下文**：关键信息放首尾，避免把指令埋在中间；超长上下文做压缩与分层。
- **安全与对抗**：提示可能被注入（Prompt Injection），多轮越狱更难检测，需配合对话级监控与策略执行，不能仅靠单轮安全指标。
- **模型差异**：换模型或升级模型后必须重新测试，提示效果随模型变化，不要假设提示可跨模型直接迁移。

## 六、核心要点速查

1. 提示工程是工程手段，不替代模型能力，与微调、RAG 互补。
2. 提示五要素：角色设定、任务指令、背景上下文、示例、输出规范。
3. 模型自回归生成，提示措辞与顺序直接影响输出。
4. 关键指令放首尾，规避长上下文的"中间迷失"。
5. 格式类任务优先用少样本示例；复杂推理用思维链。
6. 结构化输出用 JSON Schema / 函数调用，降低格式不稳定。
7. 温度低更稳定，温度高更多样，需配合 `top_p` 控制。
8. 先评估后调优：测试集、指标、基线三件套缺一不可。
9. 复杂任务用提示链拆分，长上下文用上下文工程压缩。
10. 注意提示注入与多轮越狱，需对话级安全监控。
11. 换模型必须重测提示，不可默认跨模型迁移。

## 七、学习资源

1. [Best practices for prompt engineering with the OpenAI API（OpenAI 官方）](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
2. [Prompt engineering overview（Anthropic / Claude 官方文档）](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
3. [Model Context Protocol Specification 2026-07-28（官方规范）](https://modelcontextprotocol.io/specification/2026-07-28/index)
4. [OpenAI Model Release Notes（模型线与版本信息）](https://help.openai.com/en/articles/9624314-model-release-notes)
5. [LangChain Changelog（框架版本与 `create_agent` 演进）](https://docs.langchain.org/oss/javascript/releases/changelog)
6. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（RAG 原始论文，arXiv:2005.11401）](https://arxiv.org/abs/2005.11401)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
