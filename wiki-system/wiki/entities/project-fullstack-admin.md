---
type: entity
tags: [wiki, 项目, 全栈, fastapi, vue]
created: 2026-10-05
updated: 2026-10-05
source: "[[50-项目记录/项目-全栈后台管理系统]]"
status: 联调中
stack: [FastAPI, SQLModel, Vue3, Vite, Alembic, uv]
---

# 全栈后台管理系统

## 摘要
FastAPI + Vue 的企业级后台管理脚手架，带完整 RBAC 权限体系与 Alembic 数据库迁移。当前状态：联调中，后端 2030 个 pytest 用例全通过。

## 详情

### 一句话定位
FastAPI + Vue 的企业级后台管理脚手架，带完整 RBAC 权限体系与 Alembic 迁移。

### 技术栈
| 层 | 技术 | 端口 | 说明 |
|---|---|---|---|
| 后端 | FastAPI + SQLModel | 8000 | API 前缀 `/api/system` |
| 前端 | Vue3 + Vite | 5173 | |
| 数据库 | Alembic 迁移 | - | |
| 包管理 | uv | - | |
| 测试 | pytest + Playwright | - | 后端 2030 用例全通过 |

### 本地启动
```bash
uv run uvicorn main:app --reload --port 8000
cd web && npm run dev
npm run lint && npm run build && uv run pytest   # 提交前三连
```

### 里程碑
- [x] 需求确认 / 技术方案 / 后端实现 / 前端实现
- [ ] 联调测试 / 上线部署

### 关键决策
> [!note] 为什么用 SQLModel
> 同时兼顾 Pydantic 校验与 SQLAlchemy ORM，减少 DTO 与 Model 的双份定义。

> [!warning] DTO 序列化约定
> 接口返回 DTO 对象时必须 `.model_dump()`，直接返回 Pydantic 对象会在 FastAPI 响应序列化时出问题。

### 踩坑记录
| 日期 | 问题 | 根因 | 解决 |
|---|---|---|---|
| 2026-09 | Dictionary API 返回 500 | SQLModel 2.x 中 `result.scalars().all()` 误用 | 见 [[50-项目记录/工单/工单-Dictionary API 返回 500]] |
| 2026-09 | Linux 下 pytest-cov 安装卡住 | 版本解析死锁 | 锁定版本后重装 |

## 关联
- 所属体系: [[concepts/project-ticket-system]]（项目-工单管理体系）
- 关联工单: [[50-项目记录/工单/工单-Dictionary API 返回 500]]
- 技术积累: [[20-技术积累]]

## 引用来源
- [1] [[50-项目记录/项目-全栈后台管理系统]] — 原始项目笔记

## 变更记录
- 2026-10-05: 初始创建，编译自 [[50-项目记录/项目-全栈后台管理系统]]
