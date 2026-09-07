# 项目长期记忆

## 知识库定位

`E:\陶伟东-知识库` 是 **Obsidian 个人知识库**，不是软件项目。无构建/测试/lint/CI。
操作 `.md` 前加载 `.opencode/skills/obsidian-markdown`，操作 `.base` 前加载 `.opencode/skills/obsidian-bases`。

## 工程师工作台（2026-09-07 建成）

三层架构：**Markdown 笔记（数据层）→ .base 视图（视图层）→ 工程师工作台.md（展示层）**

| 角色 | 路径 |
|---|---|
| 总入口 | `50-项目记录/工程师工作台.md` |
| 项目库 | `50-项目记录/项目库.base` |
| 工单库 | `50-项目记录/工单库.base` |
| 模板 | `95-模板/项目模板.md`、`95-模板/工单模板.md` |
| 工单存放 | `50-项目记录/工单/` |

**核心约定**：项目与工单靠 frontmatter 的 `type` 字段区分（`项目` / `工单`），Bases 和 Dataview 统一用它筛选。

- 项目字段：`status` `stack` `backend_port` `frontend_port` `started` `health` `repo`
- 工单字段：`project`(wikilink) `status` `priority`(P0-P3) `category` `due` `created`

## Obsidian Bases 避坑

- 日期相减返回 **Duration**，必须先取 `.days` / `.hours` 再做数值运算
- view 的 filter 里直接写 `date(due) < today()`，比引用 `formula.xxx == true` 更稳
- 公式含双引号时，整个公式用单引号包裹：`'if(done, "Yes", "No")'`
- 校验 YAML 用系统 Python（`D:/Program Files/Python3.10/python.exe`，自带 pyyaml）；managed python 3.13 未装 pyyaml

## 用户协作习惯

- 验证结果用表格，探索结果用清单，报错要根因分析
- 文档产出后需保存、commit、push
- 助手称呼：陶陶
