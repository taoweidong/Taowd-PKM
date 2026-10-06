---
type: concept
tags: [wiki, obsidian, 插件, 资源]
created: 2026-10-05
updated: 2026-10-06
source: "[[10-个人知识管理/Obsidian/常用插件]]"
---

# 常用插件与 Obsidian 资源

## 摘要

`常用插件` 是 Obsidian 常用插件与学习资源的收集页。本页在原笔记（QuickAdd / Git / Tasks 三个核心插件 + 一批官方与社区链接）基础上，**补全了本库实际启用的插件清单**（依据 [[AGENTS]] 记录的插件生态），把"半成品收集页"升级为可用参考。

## 详情

### 本库实际启用的插件（基于 [[AGENTS]] 插件生态）

| 插件 | 功能 | 状态 |
|------|------|------|
| Dataview | 把仓库当动态数据库，工作台看板引擎 | 详见 [[concepts/obsidian-dataview]] |
| QuickAdd | 一键 Capture / Template / Multi / Macro 自动化 | 详见 [[concepts/obsidian-quickadd]] |
| Templater | 文件创建时自动套用模板（优先于内置模板） | 本库已启用 |
| Tasks | 任务管理，自定义状态（Todo/Done/In Progress/Cancelled） | 本库已启用（原笔记提及） |
| Omnisearch | 全文搜索，权重：文件名 > 目录 > H1 > H2 > H3 > 标签 | 本库已启用 |
| Excalidraw | 绘图，存于 `Excalidraw/` 目录 | 本库已启用 |
| obsidian-git | 自动备份，每 5 分钟 auto-commit | 本库已启用 |
| Homepage | 自定义启动页 | 详见 [[concepts/obsidian-homepage]] |

### 原笔记核心插件表（源）

| 插件 | 功能 | 链接 |
|------|------|------|
| QuickAdd | [[Obsidian QuickAdd 插件使用指南]] | [Pkmer Docs](https://pkmer.cn/Pkmer-Docs/10-obsidian/obsidian%E7%A4%BE%E5%8C%BA%E6%8F%92%E4%BB%B6/quickadd/) |
| Git | 全平台自动同步（obsidian-git） | [归子莫的博客](https://blog.guizimo.com/archives/x36CnPAP) |
| Tasks | 任务管理 | [obsidian.vip 中文文档](https://obsidian.vip/zh/tasks/) |

### 学习资源（源笔记链接）

- [Obsidian 官网](https://obsidian.md/) · [官方社区](https://forum.obsidian.md/) · [中文社区](https://forum-zh.obsidian.md/) ·  · [路线图(Trello)](https://trello.com/b/Psqfqp7I/obsidian-roadmap)
- [官方中文帮助文档](https://publish.obsidian.md/help-zh/)
- [PKMer 知识库](https://pkmer.cn/) — 含《利用 AI 构建完美的 Obsidian 资料库结构》
- 知乎：[知识管理体系搭建实战指南](https://zhuanlan.zhihu.com/p/1912968515327075959) · [Obsidian 胎教级教程](https://zhuanlan.zhihu.com/p/26089182467)

> [!note] 关于原笔记草稿痕迹
> 源笔记含占位 `xxx`、"`测试一下提交`"、一张粘贴图片 `Pasted image 20251108171816.png`，属未整理草稿，本页未收录；建议作者在源笔记中清理。

## 网络精选（高质量博客 · 2026-10-06 增补）

> 本节为 2026-10-06 从全网检索并下载、仍在线的高质量博客本地镜像，覆盖 Dataview、Templater/QuickAdd 自动化、Obsidian Git 同步、Excalidraw/Canvas 视觉化、双链与知识管理实践、Tasks/周期笔记等子方向。每篇均已落盘至 `wiki-system/sources/obsidian-common-plugins/`。

### 摘要

- **Dataview 把仓库当数据库**：提供三种查询写法——DQL（`TABLE ... FROM ... WHERE ...`）、Inline DQL（行内 `= ...` 实时算单个值）、DataviewJS（`dataviewjs` 代码块用 `dv` API 做任意复杂查询），均写入 Markdown 代码块并随仓库变更实时刷新，是看板/清单/聚合视图的引擎。
- **Templater / QuickAdd 把重复劳动降到最低**：Templater 用 `<% tp.xxx %>` 语法在新建笔记时注入日期、标题、光标位与 JS 脚本；QuickAdd 可一键从模板建笔记、做 Capture 捕获、用宏(Macro)组合多步操作，配合 user scripts 实现"输入前缀即生成指定笔记"的自动化模板流。
- **Obsidian Git 实现免费多端版本化同步**：用私有 Git 仓库 + obsidian-git 插件，设自动提交/拉取/推送间隔（10–15 分钟）即可替代付费同步；关键是 `.gitignore` 忽略 `workspace.json` 等界面状态文件，避免多端切换时的合并冲突循环。
- **双链 + MOC + 定期清扫让知识自然涌现**：以"原子化"(一篇一概念)笔记、`[[双链]]`、MOC(内容地图)导航、每周"链接清扫"孤立笔记，构建可生长的知识网络；配合 Tasks + Dataview 的实时查询能自动浮现逾期与停滞项目（如周复盘系统）。
- **Excalidraw / Canvas 提供视觉化层**：Excalidraw 以手绘风绘图，绘板可嵌入 `.md` 并与笔记双向链接；Canvas 为核心白板，以开放 `.canvas`(JSON) 格式保存，可拖入笔记/媒体/网页卡片并用连线表达关系。

### 博客清单

| 主题 | 博客标题 | 本地镜像 |
|------|----------|----------|
| Dataview | Dataview 官方文档：DQL / Inline DQL / DataviewJS | [[wiki-system/sources/obsidian-common-plugins/blacksmithgu_github_io_obsidian-dataview_queries_dql-js-inline_153b238f.md\|Dataview 官方文档：DQL/JS/Inline]] |
| Templater | 掘金：使用 Templater 减少重复工作，提高效率 | [[wiki-system/sources/obsidian-common-plugins/juejin_cn_post_7381347654767804425_6a3fa724.md\|掘金：Templater 减少重复工作]] |
| QuickAdd | PKMer：基于 QuickAdd 的自动化模板教学 | [[wiki-system/sources/obsidian-common-plugins/pkmer_cn_Pkmer-Docs_10-obsidian_obsidian_E4_BD_BF_E7_94_A8_E6_8A_80_E5_B7_A7_de_792acd09.md\|PKMer：QuickAdd 自动化模板]] |
| Obsidian Git | How to sync an Obsidian vault with git (and stay sane) | [[wiki-system/sources/obsidian-common-plugins/everydayterminal_com_posts_how-to-git-sync-obsidian-vault_b72a4b7a.md\|用 Git 同步 Obsidian 仓库]] |
| Excalidraw | CSDN：Obsidian 最强绘图插件 Excalidraw 完全指南 | [[wiki-system/sources/obsidian-common-plugins/blog_csdn_net_m0_74961596_article_details_159770513_be96c2ed.md\|CSDN：Excalidraw 完全指南]] |
| 双链/知识管理 | 用双向链接重构你的知识网络 | [[wiki-system/sources/obsidian-common-plugins/www_wubaqi_com_202608251135_html_32016f6d.md\|用双向链接重构知识网络]] |
| Tasks/周复盘 | The Obsidian Weekly Review System: A Step-by-Step Workflow | [[wiki-system/sources/obsidian-common-plugins/www_obsibrain_com_blog_obsidian-weekly-review-system_c86e41df.md\|Obsidian 周复盘系统工作流]] |
| 周期笔记 | 用 Obsidian 設計自己的週計畫與週誌 | [[wiki-system/sources/obsidian-common-plugins/muki_tw_obsidian-template-daily-weekly-journal-tasks_76404e52.md\|用 Obsidian 设计周计划与周志]] |
| 插件总览 | Best Obsidian Plugins to Boost Your Productivity | [[wiki-system/sources/obsidian-common-plugins/thecodeconsole_com_unlocking-the-power-of-plugins-in-obsidian_8157d95a.md\|必装插件提升生产力]] |
| 插件总览 | The Best Obsidian Plugins to Organize Your Notes (Lifehacker) | [[wiki-system/sources/obsidian-common-plugins/lifehacker_com_best-obsidian-plugins_56cbb02b.md\|Lifehacker：最佳插件推荐]] |

## 关联

- 目录综述: [[concepts/personal-knowledge-mgmt]]
- 插件指南: [[concepts/obsidian-quickadd]] · [[concepts/obsidian-dataview]] · [[concepts/obsidian-homepage]]
- 方法: [[concepts/note-organization-principles]]

## 引用来源

- [1] [[10-个人知识管理/Obsidian/常用插件]] — 插件表格与资源链接（源）
- [2] [[AGENTS]] — 本库插件生态（Dataview/QuickAdd/Templater/Tasks/Omnisearch/Excalidraw/obsidian-git/Homepage）

## 变更记录

- 2026-10-05（初版）: 编译自常用插件，标注为半成品。
- 2026-10-05（补全）: 依据 [[AGENTS]] 补全本库实际启用插件清单；保留源资源链接；标注源笔记草稿痕迹待清理。
- 2026-10-06：网络检索并下载 10 篇仍在线的高质量博客至 sources/obsidian-common-plugins/，新增「网络精选」合成知识段。
