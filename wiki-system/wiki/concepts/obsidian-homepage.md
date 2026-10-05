---
type: concept
tags: [wiki, obsidian, 插件, homepage, 启动页]
created: 2026-10-05
updated: 2026-10-05
source: "[[10-个人知识管理/Obsidian/Homepage插件使用指南]]"
---

# Obsidian Homepage

## 摘要
Homepage 插件自定义 Obsidian 启动页：启动时/新窗口自动打开预设笔记（如仪表盘、每日笔记），支持变量与多工作区独立配置。

## 详情

### 核心功能
- 自动打开指定页面（`Dashboard.md` 等）
- 多场景触发：启动、新窗口、文件删除后
- 智能路径：`{{today}}` / `{{last}}` 变量、相对/文件夹路径
- 工作区独立主页

### 关键配置
| 参数 | 说明 |
|------|------|
| Homepage | 主页路径，如 `Dashboard.md` |
| Open on startup | 启动打开 |
| Open on new window | 新窗口打开 |
| Auto create homepage | 文件不存在则自动建 |
| Reset view | 关闭其他标签页（保持整洁） |

### 变量
- `{{today}}`：当日每日笔记（需 Daily Notes）
- `{{last}}`：上次关闭前的笔记
- 以 `/` 结尾的路径 → 打开文件夹浏览模式

> [!tip] 搭配建议
> 与 **QuickAdd** / **Templater** 组合可打造动态主页（如 Templater 自动插入当日任务）。

## 关联
- 相关概念: [[concepts/obsidian-quickadd]]（一键启动流搭档）
- 相关概念: [[concepts/project-ticket-system]]（仪表盘可设为 Homepage）
- 参见: [[10-个人知识管理/Obsidian/Homepage插件使用指南]]

## 引用来源
- [1] [[10-个人知识管理/Obsidian/Homepage插件使用指南]] — 安装/配置/FAQ 详见原文

## 变更记录
- 2026-10-05: 初始创建，编译自 Homepage 指南
