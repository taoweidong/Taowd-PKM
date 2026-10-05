---
type: concept
tags: [wiki, obsidian, 插件, dataview, 查询]
created: 2026-10-05
updated: 2026-10-05
source: "[[10-个人知识管理/Obsidian/Obsidian Dataview插件使用指南]]"
---

# Obsidian Dataview

## 摘要
Dataview 是 Obsidian 的社区插件，把仓库变成**动态数据库**：通过类 SQL 的 DQL 查询，自动收集、筛选、排序、展示笔记 Frontmatter 与行内字段中的元数据。[[concepts/project-ticket-system|工程师工作台]]的看板即由它驱动。

## 详情

### 元数据来源
- **YAML Frontmatter**：笔记顶部结构化属性（`author` / `status` / `rating` 等）
- **Inline Fields**：正文 `key:: value` 键值对
- **隐式字段**：`file.name` / `file.folder` / `file.link` / `file.tags` / `file.inlinks` / `file.outlinks` / `file.mtime` 等

### 四种呈现命令
`LIST` / `TABLE` / `TASK` / `CALENDAR`

### DQL 结构
```dataview
[LIST|TABLE|TASK|CALENDAR] [字段 AS "别名"]
FROM [#标签 | "文件夹" | [[笔记]] | "" ]
WHERE 条件
SORT 字段 ASC/DESC
GROUP BY 字段
```

### 典型用法
- 书籍库：`TABLE author, rating FROM #书籍 SORT publish-date DESC`
- 任务：`TASK FROM "Projects" WHERE !completed AND due < date(today) + dur(7 days)`
- 统计：`TABLE length(rows) AS 数量 FROM "" GROUP BY type`
- 日历：`CALENDAR file.mtime FROM "Journal"`

### 进阶
- **DataviewJS**：用 JavaScript 做复杂渲染（`dv.pages()` / `dv.table()`）
- **动态仪表盘**：多个查询块组合成实时汇总页（即工作台的实现基础）

> [!tip] 一致性是关键
> 字段名拼写必须一致，否则查询匹配不到。先打元数据基础，再从 `LIST FROM #tag` 起步。

## 关联
- 相关概念: [[concepts/project-ticket-system]]（工作台看板由 Dataview 驱动）
- 相关概念: [[concepts/obsidian-quickadd]]（常配合 QuickAdd 自动写入带 Frontmatter 的笔记）
- 参见: [[10-个人知识管理/Obsidian/Obsidian Dataview插件使用指南]]

## 引用来源
- [1] [[10-个人知识管理/Obsidian/Obsidian Dataview插件使用指南]] — 官方文档与示例库链接见原文

## 变更记录
- 2026-10-05: 初始创建，编译自 Dataview 指南
