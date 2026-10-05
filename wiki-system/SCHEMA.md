# SCHEMA.md — LLM Wiki 规则配置

> 本文件是 [[wiki-system]] 编译层的"宪法"。任何 Ingest / Query / Lint 操作都必须遵守这里的规则。

## 1. 定位与范围

这是 **Obsidian 个人知识库（`E:\陶伟东-知识库`）内部的一个 LLM Wiki 编译子系统**，收纳在 `wiki-system/` 顶层目录下，与既有的 `00-`~`99-` 主结构**并存、互不干扰**。

- `00-`~`99-` 主结构：数据采集层，日常随手记、项目笔记、工单、日记。
- `wiki-system/`：知识编译层，把主结构笔记和 `raw/` 中的原始资料"提炼"成结构化、可增量更新、带交叉引用的知识页。

## 2. 三层结构

| 层 | 路径 | 角色 | 规则 |
|----|------|------|------|
| 第一层 原始资料 | `wiki-system/raw/` | 用户投放的文章/论文/笔记原文 | **只读**，永不修改；Ingest 时从这里读取 |
| 第二层 编译知识 | `wiki-system/wiki/` | LLM 编译维护的知识层 | 含 `index.md`、`log.md`、`entities/`、`concepts/`、`topics/` |
| 第三层 规则配置 | `wiki-system/SCHEMA.md` | 本文件 | 定义全部规则 |

## 3. 页面模板

每个 Wiki 页必须包含 YAML frontmatter + 固定章节，兼容 Obsidian Properties 与 Callouts：

```yaml
---
type: entity | concept | topic | comparison
tags: [wiki, ...]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: "[[50-项目记录/xxx]]"   # 主要来源 wikilink
---
```

章节顺序：**摘要 → 详情 → 关联 → 引用来源 → 变更记录**。
- 用 Obsidian callout `> [!note]` / `> [!warning]` 标注重点与矛盾。
- 详情中可嵌入主结构的视图：`` ![[项目库.base#全部项目]] ``。

## 4. 命名规则

- 页面文件名 `kebab-case`，如 `transformer-architecture.md`。
- 目录：`entities/`（人物/公司/产品/项目）、`concepts/`（技术/方法论）、`topics/`（主题综述/对比）。

## 5. 引用规则

- 库内链接统一用 Obsidian wikilink `[[note]]` 或 `[[路径/note]]`，便于重命名自动更新。
- 跨层引用主结构内容用 `[[50-项目记录/xxx]]` 等带路径形式。
- 外部资料用标准 Markdown 链接 `[text](url)`。

## 6. 质量原则（红线）

- **Never Hallucinate**：所有知识必须来自 `raw/` 或主结构笔记，或明确标注为 AI 推理。
- **Always Cite**：每个知识点标注来源 `[[...]]`。
- **Mark Conflicts**：不同来源冲突时用 `> [!warning] ⚠️ 矛盾` callout 明确标记。

## 7. 操作纪律

- `raw/` 只读；主结构笔记也不修改（除非用户明确要求）。
- 每次 Ingest 后必须更新 `wiki/index.md` 与 `wiki/log.md`。
- 增量更新：更新已有页时追加新内容并写"变更记录"，不覆盖历史。
- Lint 周期：每月检查矛盾、过时、孤立页、缺失引用。
