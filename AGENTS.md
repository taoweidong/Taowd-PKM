# AGENTS.md — 陶伟东 知识库

这是一个 **Obsidian 个人知识库**，不是软件项目。无构建/测试/lint/CI 工具。AI 代理的工作是增删改查 `.md`、`.canvas` 及其他 Obsidian 管理的文件。

## 核心事实

- **语言**: 全部中文。笔记、目录名、wikilink 均为中文。
- **目录编号**: `00-` 到 `99-` 前缀。新增文件默认放 `90-待整理与临时笔记/` (见 `.obsidian/app.json`)。
- **~60% 笔记为空占位**: 由 `10-个人知识管理/obsidian_init.py` 脚本批量生成。识别标志: `*本页面内容待完善...*`。
- **Git 自动提交**: `obsidian-git` 插件每 5 分钟 auto-commit，信息格式 `Obsidian 自动提交备份: {{date}}`。
- **没有 CI/CD**，没有测试框架。

## AI 代理工作前必须加载的技能

`.opencode/skills/` 目录下的技能必须在操作对应文件类型前加载:

| 技能 | 何时加载 |
|------|---------|
| `obsidian-markdown` | 创建/编辑任何 `.md` 文件 |
| `obsidian-cli` | 通过 CLI 与运行的 Obsidian 交互 |
| `json-canvas` | 创建/编辑 `.canvas` 文件 |
| `obsidian-bases` | 创建/编辑 `.base` 文件 |
| `defuddle` | 抓取网页内容 |

## Obsidian 配置要点

| 配置项 | 值 |
|--------|-----|
| 新文件位置 | `90-待整理与临时笔记/` |
| 附件位置 | `99-附件/` |
| 模板目录 | `95-模板/` |
| 日记格式 | `80-日记记录/YYYY/MM/YYYY-MM-DD日记.md` |
| 日记模板 | `95-模板/每日笔记模板.md` |
| 周报格式 | `YYYY/YYYY-ww周报` (periodic-notes 插件) |
| Canvas 白板 | `90-待整理与临时笔记/白板/` |
| 链接更新 | `alwaysUpdateLinks: true` (改名自动更新引用) |
| 快捷键 | `Cmd+Q` → QuickAdd, `Cmd+R` / `Cmd+Shift+F` → Omnisearch |
| CSS 片段 | `custom-code-bg.css` (代码块背景样式) |

## Markdown 语法要点

- **Wikilinks**: `[[笔记名]]`, `[[笔记名|显示文字]]`, `[[笔记名#标题]]`
- **嵌入**: `![[笔记名]]`
- **Callouts**: `> [!note]`, `> [!warning]`, `> [!tip]`, `> [!info]` 等
- **标签**: `#标签` 或 `#父级/子级` (层级标签)
- **Frontmatter**: YAML 格式，`tags` 字段常用
- 所有 Obsidian 特有语法详见 `obsidian-markdown` 技能引用

## 分类目录速查

| 区间 | 内容 | 索引文件 |
|------|------|---------|
| `00-` | 索引与导航 | `00-索引与导航/00-索引与导航.md` |
| `10-` | 个人知识管理 | `10-个人知识管理/10-个人知识管理.md` |
| `20-` | 技术积累 | `20-技术积累/20-技术积累.md` |
| `30-` | 软件设计 | `30-软件设计/30-软件设计.md` |
| `40-` | AI 技术 | `40-AI技术/40-AI技术.md` |
| `50-` | 项目记录 | `50-项目记录/50-项目记录.md` |
| `60-` | 参考资料 | `60-参考资料/60-参考资料.md` |
| `70-` | 代码片段 | `70-代码片段/70-代码片段.md` |
| `80-` | 日记记录 | 无固定索引，按 `YYYY/MM/` 组织 |
| `90-` | 待整理笔记 | `90-待整理与临时笔记/90-待整理与临时笔记.md` |
| `95-` | 模板 | `95-模板/95-模板.md` |
| `99-` | 附件 | `99-附件/99-附件.md` |

## 插件生态

| 插件 | 作用 |
|------|------|
| `obsidian-git` | 自动备份，每 5 分钟 |
| `templater-obsidian` | 文件创建时自动套用模板 (优先于内置模板) |
| `quickadd` | 3 个宏: 新建文档/添加任务/打开今日日记 |
| `dataview` | 查询引擎，模板中用于动态列表 |
| `obsidian-tasks-plugin` | 任务管理，自定义状态 (Todo/Done/In Progress/Cancelled) |
| `omnisearch` | 全文搜索，权重: 文件名 > 目录 > H1 > H2 > H3 > 标签 |
| `obsidian-excalidraw-plugin` | 绘图，存于 `Excalidraw/` 目录 |

## 注意事项

- 不要运行 `npm install`、`cargo build` 等 — 这不是软件项目。
- 不要向 `.obsidian/` 目录写入配置文件，除非明确要求。
- 创建笔记时考虑使用 `95-模板/` 下的模板。
- 为笔记添加 frontmatter (至少 `tags` 字段) 以支持 Dataview 查询。
- 首次操作 `.md` 文件前务必加载 `obsidian-markdown` 技能。