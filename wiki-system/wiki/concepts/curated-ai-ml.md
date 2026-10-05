---
type: concept
tags: [wiki, 收藏夹Ingest, AI, 大模型, AGENTS, 云原生]
created: 2026-10-05
updated: 2026-10-05
source: "[[topics/browser-bookmarks]]"
---

# AI 与大模型（收藏夹 Ingest）

> 编译自 [[topics/browser-bookmarks]] 的「AI 与大模型」主题（共 8 条）。本主题体量小且与当前 AI 辅助开发强相关，故逐条抓取真实内容提炼要点（抓取于 2026-10-05）。

## 摘要

这是一份「AI 工具链 + AI 辅助开发规范」的精选清单，恰好覆盖作者当前工作流的三条主线：
- **AI 辅助开发规范**：AGENTS.md / OpenCode 规则体系（如何让 AI 智能体高效协作项目）。
- **AI 创作/建站工具**：WeaveFox（自然语言生成应用）、千问 Token Plan、CNB 云原生构建（含 NPC/知识库）。
- **AI 基础设施**：本地 AI 开发主机升级方案、WSL Ubuntu 镜像、Vue 官方指南（前端基座）。

> [!tip] 与 KontainKeeper 的关系
> AGENTS.md 规范 + CNB 的 NPC/知识库 + 本地大模型推理，正是「AI 辅助全栈开发」的可落地路径，与 [[entities/project-fullstack-admin]] 的重构方向一致。

## 详情

### 1. OpenCode 规则详解：AGENTS.md、优先级与自定义指令 ✅已抓
- 来源：https://ai.iamchen.cn/content/29
- `AGENTS.md` 是给模型的「自定义指令」文件（项目级规则），会进入模型上下文、影响其行为，定位是「把每次都要重复告诉模型的话沉淀成长期规则」。
- 创建方式：`/init`（扫描项目自动生成/补充）或手写（更可控）。
- 分工：**项目级** `AGENTS.md`（项目根，提交 Git 服务团队）vs **全局** `~/.config/opencode/AGENTS.md`（个人偏好，不提交）。
- 兼容 Claude Code：回退读取项目 `CLAUDE.md`、全局 `~/.claude/CLAUDE.md`、`~/.claude/skills/`；可用 `OPENCODE_DISABLE_CLAUDE_CODE=1` 关闭。
- **优先级**：本地向上遍历 `AGENTS.md`/`CLAUDE.md` → 全局 `opencode AGENTS.md` → 全局 `claude CLAUDE.md`；同类只取第一个匹配（不叠加）。
- 模块化扩展：`opencode.json` 的 `instructions` 字段可引用本地 md / 目录 / glob（`packages/*/AGENTS.md`）/ 远程 URL，与 `AGENTS.md` 合并而非替代。
- ⚠️ OpenCode **不会自动解析** `AGENTS.md` 内的文件引用，需显式按需加载（或走 `instructions`）。

### 2. 手把手编写 AGENTS.md（知乎） ✅已抓
- 来源：https://zhuanlan.zhihu.com/p/2015507552046167271
- 定位：面向 AI 智能体的规范配置文件，统一多 AI 工具上下文、显性化项目隐性规则，与面向人类的 `README.md` 分工。
- 适用场景：自动化运维、智能交互、流程协作、定制化开发。
- 标准结构：**必选**（项目基础信息 / 环境搭建与开发流程 / 测试规范 / 代码风格 / 操作边界与禁止行为）+ **可选**（提交与 PR 规范 / 安全规范 / 调试排错）。
- 避坑：避免冗余目录列表、纯文字风格指南、非通用指令、用脚本自动生成。
- 最佳实践：指令前置、代码示例优先、边界三级（✅必须做 / ⚠️先询问 / 🚫绝对禁止）、技术栈标版本号、渐进式披露（细节拆到独立文件 `@./agent_docs/xxx.md`）。

### 3. WeaveFox — 自然语言生成应用 ✅已抓
- 来源：https://www.weavefox.cn/
- 通过自然语言对话「零门槛」创造个人专属工具与独立应用。
- 场景：**软件原型**（文档/线框图 → 可运行交互原型）、**实用工具**（计算器/说明书/幻灯片/数据看板）、**落地页**、**个人品牌**（主页/简历/名片/作品集）。
- 面向人群：创业者、产品经理、设计师、内容创作者、超级个体。

### 4. cnb hello-cnb — CNB 云原生构建入门闯关 ✅已抓
- 来源：https://cnb.cool/cnb/tutorial/hello-cnb
- CNB 平台入门闯关仓库，**7 关 21 任务**：个人信息 → 仓库设置 → 流水线配置（Push/PR/Tag/Web trigger）→ 云原生开发（浏览器内 VS Code）→ Docker 制品 → 任务集 → **NPC & 知识库**。
- Level 7 关键：开启仓库知识库（AI 自动索引代码，在 Issue/PR 给上下文感知回答）、创建 NPC（自定义 AI 助手，自动评审代码/总结 PR/回答问题）。
- 通关奖励「天才程序员」身份 + 666 AI Credits/月。体现「云原生构建 + AI 辅助开发」闭环。

### 5. AI 开发主机升级方案分析报告 ✅已抓
- 来源：https://agent.my.cn/mos/1709d3d223b1490d89735e7b26924a6e/e3089c1123c3123cdcb66570020fc511
- 现状：i7-9700 + 15.9GB RAM（可用仅 6.3GB）+ GTX 1660Ti 4GB，**显存墙 + 内存墙**双重瓶颈，跑不动 7B 以上模型。
- 推荐：**RTX 3060 12GB + 32GB DDR4**（约 3143–3348 元），可稳定跑 7B–12B 稠密 / 35B MoE（CPU 卸载），兼顾图像生成、LoRA 微调、编码辅助。
- 对比：RTX 4060（8GB，架构新但显存小易 OOM）、RTX 3070 二手（需非官方改装，有风险）。
- 短期优化：Q4_K_M 量化、MTP 多 Token 预测、xFormers 算子优化。

### 6. WSL Ubuntu Jammy 镜像索引页 ✅已抓
- 来源：https://cloud-images.ubuntu.com/wsl/jammy/20250318/
- 这是 **Ubuntu 22.04 LTS 的 WSL 镜像索引页**（日期 20250318），提供 amd64 / arm64 的 `rootfs.tar.gz`（约 325M / 309M）与 manifest，以及 MD5/SHA256 校验和、unpacked/ 目录。
- 用途：获取特定日期的稳定 WSL Ubuntu 镜像（避免跟随 latest 漂移）。

### 7. Vue.js 创建应用（官方指南） ✅已抓
- 来源：https://cn.vuejs.org/guide/essentials/application.html
- 每个 Vue 应用通过 `createApp()` 创建**应用实例**；传入的对象即**根组件**（其余组件为其子组件）。
- 调用 `.mount(容器)` 后才渲染；容器元素自身**不算**应用一部分；根组件可从 `./App.vue` 单文件组件导入。
- 支持应用级配置 `.config`（如 `errorHandler`）与**多个应用实例共存**（各自独立作用域）。

### 8. 千问 AI 平台 Token Plan（个人版） ⚠️需登录
- 来源：https://platform.qianwenai.com/home/billing/subscription/token-plan-individual
- 通义千问的 Token 套餐页面；**需登录**才能使用完整服务（未登录仅见导航）。
- 可见能力入口：首页 / API Keys / 模型体验 / 模型生产 / Agent 开发(Beta) / 用量分析（Token Plan、按量付费）/ 账单 / 设置。反映其提供 API Key、Agent 开发、Token 套餐与按量付费。

## 关联

- 来源索引：[[topics/browser-bookmarks]]（AI 与大模型主题共 8 条，本页为逐条精编）
- 项目体系：[[entities/project-fullstack-admin]]、[[concepts/curated-opensource-projects]]
- 其他收藏中的 AI 工具入口见：[[concepts/curated-other-favorites]]

## 引用来源

- 各 URL 见上文，核心 8 篇抓取于 2026-10-05（千问 Token Plan 需登录，仅记录导航结构）
- 原始收藏：[[90-待整理与临时笔记/favorites_2026_10_5]]

## 变更记录

- 2026-10-05：Ingest「AI 与大模型」主题 8 条。逐条抓取 7 篇并提炼要点（OpenCode 规则 / AGENTS.md 编写 / WeaveFox / cnb hello-cnb / AI 主机升级 / WSL 镜像 / Vue 应用）；千问 Token Plan 因登录墙仅记录导航结构。
