---
type: concept
tags: [wiki, 全栈, playwright, ui测试, 联调]
created: 2026-10-05
updated: 2026-10-05
source: "[[50-项目记录/工单/工单-Playwright 覆盖登录流程]]"
status: 待办
priority: P2
---

# Playwright 覆盖登录流程

## 摘要
用 Playwright 补登录流程的 UI 自动化用例，纳入提交前检查。状态：待办，仅有验收标准，未启动。

## 详情

### 环境
- 前端 Vue + Vite（5173），后端 FastAPI（8000）
- 前置：后端接口已跑通，登录接口稳定

### 验收标准
- [ ] 正常登录成功跳转首页
- [ ] 错误密码提示正确
- [ ] 未登录访问受保护路由会重定向
- [ ] 能接入 CI 或本地一键执行

> [!warning] 待办
> 处理过程与结论待实施后回填。注意与 [[concepts/slowapi-rate-limiting]] 的限流规则配合（限流可能干扰登录测试，需白名单或固定窗口）。

## 关联
- 所属项目: [[entities/project-fullstack-admin]]
- 相关概念: [[concepts/slowapi-rate-limiting]]（登录限流会影响本测试）
- 关联工单: [[50-项目记录/工单/工单-Playwright 覆盖登录流程]]

## 引用来源
- [1] [[50-项目记录/工单/工单-Playwright 覆盖登录流程]] — 原始工单（待办 P2）

## 变更记录
- 2026-10-05: 初始创建，编译自 Playwright 登录工单（待办，仅验收标准）
