---
type: concept
tags: [wiki, 开源项目, 后台管理, 权限认证, 配置中心, 收藏夹Ingest]
created: 2026-10-05
updated: 2026-10-05
source: "[[topics/browser-bookmarks]]"
---

# 精选开源项目（收藏夹 Ingest · 第 1 批）

> 从浏览器收藏夹「开源项目」主题（共 59 条）中优先 Ingest 的 10 个高相关项目，聚焦**后台管理脚手架 / 权限认证 / 配置中心**，与 [[概念:全栈后台管理系统]]（KontainKeeper：FastAPI + Vue + RBAC）技术栈高度相关。

## 摘要

这是一份「可借鉴的后台系统开源基座」清单。核心结论：
- **后端**：FastAPI Best Architecture 与本项目（FastAPI + RBAC + JWT/OAuth2）技术栈几乎完全重合，是最直接的参考；Java 侧 pig / RuoYi / ELADMIN 提供 Spring 生态的成熟 RBAC + 代码生成范式。
- **前端**：vue-element-admin（Vue2 经典）、vue-vben-admin（Vue3+Vite+TS 现代）是当前主流中后台模板。
- **权限**：Sa-Token 是轻量一站式 Java 权限认证框架，可作为 RBAC 鉴权层参考。
- **基础设施**：Apollo 解决多环境配置中心，适合 500 台规模机器的统一配置治理。

> [!tip] 与 KontainKeeper 的关系
> 收藏夹中大量 Vue 后台模板 + Spring/FastAPI RBAC 脚手架，印证了「最大化复用开源组件、降低自研」的重构方向（见 [[概念:全栈后台管理系统]]）。

## 详情

### 后端脚手架

**1. FastAPI Best Architecture (fba)**
- 定位：企业级 FastAPI 后端架构方案，前后端分离，三层架构（API → Service → CRUD/DAO）
- 技术栈：FastAPI (Py3.10+)、JWT / RBAC / OAuth2.0、MySQL·PostgreSQL 一等支持、Redis（缓存+队列）、Celery、Docker Compose、全链路日志（Trace ID）
- AI 赋能：内置 skills + LLMs.txt + MCP，适配 Claude Code / Cursor / Codex
- 适合场景：中后台、企业级后端服务、AI 辅助开发
- 仓库：https://github.com/fastapi-practices/fastapi-best-architecture
- ★ **与 KontainKeeper 后端栈几乎一致，最高优先级参考**

**2. pig（微服务 RBAC）**
- 定位：基于 Spring Boot 4.1 + Spring Cloud 2025 & Alibaba + SAS OAuth2 的微服务 RBAC 权限管理系统（支持微服务/单体）
- 特性：认证中心（Spring Authorization Server）、网关、用户权限、监控、代码生成、定时任务；Docker Compose 一键编排 MySQL/Redis/Nacos
- 规模：45.8k Stars · Apache-2.0
- 文档：https://wiki.pig4cloud.com

**3. ELADMIN**
- 定位：简单易上手的 Spring Boot 后台管理框架（Mybatis-Plus 版）
- 技术栈：SpringBoot + JPA/Mybatis-Plus + Security + Redis + Vue，前后端完全分离
- 特性：内置代码生成器，一键生成前后端代码
- 文档：https://eladmin.vip/

**4. RuoYi 若依**
- 定位：基于 SpringBoot 的权限管理系统，国内最流行的开源后台之一
- 生态：RuoYi（Bootstrap）、RuoYi-Vue（SpringBoot+Vue）、RuoYi-Cloud（SpringCloud+Vue）、RuoYi-App（UniApp）
- 特性：完善权限管理、代码生成器、完全响应式（电脑/平板/手机）、多语言
- 版本：v4.8.3
- 官网：http://ruoyi.vip/

**5. Django-Vue-Admin**
- 定位：Django + Vue3 前后端分离管理框架
- 注：本次抓取的具体文档页返回 404，项目主页（https://django-vue-admin.com）可正常访问，需另抓

### 前端 Admin 模板

**6. vue-element-admin**
- 定位：基于 Vue + element-ui 的生产级后台前端方案（作者 PanJiaChen）
- 技术栈：Vue / element-ui / vuex / vue-router / axios / Mock.js
- 特性：登录登出、权限管理、i18n、Excel/PDF/富文本等大量内置组件；衍生 vue-admin-template、electron-vue-admin、vue-typescript-admin-template
- 预览：https://panjiachen.github.io/vue-element-admin

**7. vue-vben-admin**
- 定位：基于 Vue3 + Vite + TypeScript + Shadcn UI 的免费开源中后台模板
- 特性：现代化技术栈、主题定制、内置 i18n、动态路由权限生成
- 仓库：https://github.com/vbenjs/vue-vben-admin

### 权限认证

**8. Sa-Token**
- 定位：一站式 Java 权限认证框架（Gitee GVP，GitHub 18k+ Stars）
- 特性：登录认证（多端/单端/互斥）、权限/角色认证、踢人下线、Redis 集成、前后端分离 Token 策略、SSO 单点登录、OAuth2.0、微服务鉴权
- 官网：https://sa-token.cc/
- ★ **RBAC/鉴权层可直接对标本项目权限设计**

### 配置中心

**9. Apollo 配置中心（apolloconfig/apollo）**
- 定位：分布式配置中心，统一管理多环境（DEV/FAT/UAT/PRO）配置
- 技术栈：Spring Boot/Cloud、MySQL、Portal 管理界面；支持虚拟机/Docker/Kubernetes 部署
- 特性：多环境隔离、灰度发布与审核、高可用双活、LDAP 登录、开放平台 API
- 部署指南：https://www.apolloconfig.com/#/zh/deployment/distributed-deployment-guide
- ★ **适合 500 台规模机器的统一配置治理**

### 资源导航

**10. HelloGitHub**
- 定位：发现和分享有趣、入门级开源项目的社区平台
- 用途：日常淘优质开源项目
- 官网：https://hellogithub.com/

## 关联

- 来源索引：[[topics/browser-bookmarks]]（开源项目主题共 59 条，本页为第 1 批 10 条）
- 项目体系：[[概念:全栈后台管理系统]]、[[entities/project-fullstack-admin]]
- 权限实践：[[concepts/slowapi-rate-limiting]]（本项目接口限流）、[[concepts/dictionary-api-500-error]]

## 引用来源

- 各项目官网 / GitHub / Gitee（见上文链接），抓取于 2026-10-05
- 原始收藏：[[90-待整理与临时笔记/favorites_2026_10_5]] → 经 [[topics/browser-bookmarks]] 归类

## 变更记录

- 2026-10-05：第 1 批 Ingest「开源项目」主题下 10 个高相关项目（后端脚手架 5 / 前端模板 2 / 权限 1 / 配置中心 1 / 导航 1）。Django-Vue-Admin 深链 404，标记待补抓。
