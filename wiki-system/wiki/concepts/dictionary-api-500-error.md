---
type: concept
tags: [wiki, 全栈, fastapi, sqlmodel, bug]
created: 2026-10-05
updated: 2026-10-05
source: "[[50-项目记录/工单/工单-Dictionary API 返回 500]]"
status: 已完成
priority: P0
---

# Dictionary API 返回 500（SQLModel 2.x 踩坑）

## 摘要
全栈后台管理系统的字典管理接口 `/api/system/dict/list` 返回 500，根因是 SQLModel 2.x 中 `result.scalars().all()` 误用，取值时抛异常。

## 详情

### 现象
- 环境：FastAPI + SQLModel 2.x
- 调用字典列表接口 → 500 Internal Server Error，前端拿不到字典数据

### 根因
SQLModel 2.x 的 `Result` API 与 1.x 有行为差异。代码中对当前查询对象误用了 `result.scalars().all()`，导致取值时抛异常。

### 修复
改用与 2.x 匹配的取值方式：
- 先 `result.scalars()` 再按需 `.all()` / `.first()`
- 或直接 `session.exec(statement).all()`

### 沉淀
> [!warning] 升级告警
> SQLModel 2.x 的 `Result` API 与 1.x 不同，**升级时需全量排查取值调用**，不止 Dictionary 一处。

## 关联
- 所属项目: [[entities/project-fullstack-admin]]
- 关联工单: [[50-项目记录/工单/工单-Dictionary API 返回 500]]

## 引用来源
- [1] [[50-项目记录/工单/工单-Dictionary API 返回 500]] — 原始工单结论

## 变更记录
- 2026-10-05: 初始创建，编译自 Dictionary API 500 工单（已完成 P0）
