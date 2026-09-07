---
type: 工单
project: "[[项目-全栈后台管理系统]]"
status: 已完成
priority: P0
category: Bug
due: 2026-09-03
created: 2026-09-02
tags:
  - 工单
---

# Dictionary API 返回 500

## 描述

字典管理接口调用返回 500，前端拿不到字典数据。

## 上下文

**环境**：FastAPI + SQLModel 2.x
**复现步骤**：

1. 调用 `/api/system/dict/list`
2. 返回 500 Internal Server Error

## 处理过程

1. 打开服务端日志，定位到 SQL 执行层异常
2. 排查查询语句写法

## 结论

**根因**：SQLModel 2.x 中误用 `result.scalars().all()`。在 2.x 版本里该 API 行为变更，对当前查询对象不适用，导致取值时抛异常。

**修复**：改用与 SQLModel 2.x 匹配的取值方式（先 `result.scalars()` 再按需 `.all()` / `.first()`，或直接用 `session.exec(statement).all()`）。

**沉淀**：SQLModel 2.x 的 `Result` API 与 1.x 有差异，升级时需全量排查取值调用。

## 关联

- 所属项目：[[项目-全栈后台管理系统]]
- 相关笔记：[[20-技术积累]]
