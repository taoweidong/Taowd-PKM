# raw/ — 原始资料投放区

> 本目录是 LLM Wiki 的**第一层（原始资料层）**，只读。

## 用途
把你想要"编译"进知识库的资料原文放进来，然后告诉 LLM Wiki 专家「处理 raw/ 里的新文件」，即可触发 Ingest 流程：

1. LLM 读取原始资料，与你讨论要点；
2. 提炼成 `wiki/` 下的结构化知识页（entity / concept / topic）；
3. 自动建立交叉引用、标注矛盾；
4. 更新 `wiki/index.md` 与 `wiki/log.md`。

## 命名建议
- 论文：`paper-xxx.md`
- 文章：`article-xxx.md`
- 笔记：`notes-xxx.md`
- 网页抓取：可用 `defuddle` 技能把网页转成干净 markdown 后放入。

> [!warning] 只读
> 本目录内容**不会被修改**，请放心投放。
