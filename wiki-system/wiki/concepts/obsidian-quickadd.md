---
type: concept
tags: [wiki, obsidian, 插件, quickadd, 自动化]
created: 2026-10-05
updated: 2026-10-05
source: "[[10-个人知识管理/Obsidian/Obsidian QuickAdd 插件使用指南]]"
---

# Obsidian QuickAdd

## 摘要
QuickAdd 是 Obsidian 的效率"瑞士军刀"——通过快捷键/命令/按钮触发预定义 Choice，把多步重复操作压成一步。核心是 Capture / Template / Multi / Macro 四种 Choice。

## 详情

### 四种 Choice 模式
| 模式 | 作用 | 典型场景 |
|------|------|---------|
| Capture | 把选中文本/输入内容追加到指定笔记 | 灵感速记到收件箱、摘录入文献笔记 |
| Template | 基于模板一键生成新笔记 | 每日笔记、读书笔记、项目卡片 |
| Multi | 组合多个 Choice 顺序执行 | 建日记同时捕获剪贴板内容 |
| Macro | 写 JS 调用 Obsidian/插件 API | 批量改 Frontmatter、调 API 建笔记 |

### 核心变量
- `{{value}}` / `{{VALUE}}`：捕获内容 / 用户输入（用于文件名）
- `{{date:FORMAT}}` / `{{time:FORMAT}}`：日期时间（Moment.js 格式）
- `{{title}}` / `{{note_title}}`：新笔记/当前笔记标题（需 Templater）

> [!tip] 最佳实践
> Template 模式配合 **Templater** 插件（条件/循环/用户输入）威力最大；Capture 用 `Insert after` 精准插入到目标笔记指定标题下。

### 触发方式
命令面板、`Setup Hotkey`（强烈推荐）、Buttons 插件按钮、URI 命令。

> [!warning] 配置备份
> Choices 存于 `.obsidian/plugins/quickadd/data.json`，定期备份整个库或该文件。

## 关联
- 相关概念: [[concepts/obsidian-homepage]]（Homepage 建议搭配 QuickAdd 打造一键启动流）
- 相关概念: [[concepts/obsidian-dataview]]（Macro 可调用 Dataview）
- 参见: [[10-个人知识管理/Obsidian/Obsidian QuickAdd 插件使用指南]]

## 引用来源
- [1] [[10-个人知识管理/Obsidian/Obsidian QuickAdd 插件使用指南]] — 详细安装与 Capture/Template 配置步骤见原文

## 变更记录
- 2026-10-05: 初始创建，编译自 QuickAdd 指南
