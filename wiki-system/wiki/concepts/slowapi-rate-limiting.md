---
type: concept
tags: [wiki, 全栈, fastapi, slowapi, 限流]
created: 2026-10-05
updated: 2026-10-05
source: "[[50-项目记录/工单/工单-接入 slowapi 接口限流]]"
status: 进行中
priority: P1
---

# 接入 slowapi 接口限流

## 摘要
为全栈后台管理系统的 `/api/system` 高频接口加限流防刷。选型 **slowapi**（基于 limits 库，与 FastAPI 集成最顺）。当前状态：进行中，仅有验收标准，尚未落地。

## 详情

### 选型
- **slowapi**：基于 `limits` 库，与 FastAPI 依赖注入/装饰器风格契合

### 验收标准
- [ ] 登录接口按 IP 限流（如 5 次/分钟）
- [ ] 超限返回 429 + 明确提示
- [ ] 限流规则可配置，不硬编码
- [ ] 补充对应 pytest 用例

> [!warning] 待办
> 处理过程与结论尚空，需实施后回填。限流规则"可配置不硬编码"是关键约束。

## 关联
- 所属项目: [[entities/project-fullstack-admin]]
- 相关概念: [[concepts/playwright-login-flow]]（登录流程亦属 `/api/system` 防护面）
- 关联工单: [[50-项目记录/工单/工单-接入 slowapi 接口限流]]

## 引用来源
- [1] [[50-项目记录/工单/工单-接入 slowapi 接口限流]] — 原始工单（进行中 P1）

## 变更记录
- 2026-10-05: 初始创建，编译自 slowapi 限流工单（进行中，仅验收标准）
