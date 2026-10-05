---
source: "https://cnb.cool/cnb/tutorial/hello-cnb"
title: "cnb/tutorial/hello-cnb · Cloud Native Build"
fetched_at: "2026-10-05 15:46:10"
---

![logo](/images/favicon.png)

[代码](/cnb/tutorial/hello-cnb)[ISSUE2](/cnb/tutorial/hello-cnb/-/issues)[合并请求1036](/cnb/tutorial/hello-cnb/-/pulls)[云原生构建](/cnb/tutorial/hello-cnb/-/build/logs)[制品](/cnb/tutorial/hello-cnb/-/packages)[洞察](/cnb/tutorial/hello-cnb/-/insights/contributors)[Wiki](/cnb/tutorial/hello-cnb/-/wiki)

main

[分支15](/cnb/tutorial/hello-cnb/-/branches)[Tag1](/cnb/tutorial/hello-cnb/-/tags)

Fork

[![](/users/sixther/avatar/s)](/u/sixther)[段超](/u/sixther)

docs: 关注用户名单轮转，没猫饼移至末位

[fb4f27c7](/cnb/tutorial/hello-cnb/-/commit/fb4f27c794aa2aa8970b7ad41a1d153d9a8fc278)

[38 次提交](/cnb/tutorial/hello-cnb/-/commits/main)

[assets](/cnb/tutorial/hello-cnb/-/tree/main/assets "assets")| |
---|---|---
[.cnb.yml](/cnb/tutorial/hello-cnb/-/blob/main/.cnb.yml ".cnb.yml")| |
[README.en.md](/cnb/tutorial/hello-cnb/-/blob/main/README.en.md "README.en.md")| |
[README.md](/cnb/tutorial/hello-cnb/-/blob/main/README.md "README.md")| |

![](https://commit.cool/badge/visit/cnb/tutorial/hello-cnb)

![](https://cnb.cool/cnb/tutorial/hello-cnb/-/git/raw/main/assets/banner.svg)

[CNB 上的那些天才们](https://cnb.cool/cnb/tutorial/genius-chain)

## 这是什么？

这是一个 CNB 平台的入门闯关仓库。你将通过实际操作，逐步解锁 CNB 的各项功能——从设置个人信息到配置流水线，从构建容器镜像到创建 NPC。

每个任务都有明确的目标和验证机制，提交 PR 后流水线会自动检查你的完成情况。

## 参与方式

  1. **新建组织** — 如果你是 CNB 新手，还没有自己的组织，点击右上角「+」→「新建组织」，按照指引创建一个组织。Fork 仓库需要归属到一个组织或个人空间下
  2. **Fork 本仓库** — 点击右上角 Fork 按钮，将仓库 fork 到你的个人空间
  3. **完成任务** — 按关卡顺序完成对应任务
  4. **提交 PR** — 将改动提交到你 fork 的仓库，然后向 [hello-cnb 仓库](https://cnb.cool/cnb/tutorial/hello-cnb) 发起 Pull Request
  5. **等待验证** — CI 流水线会自动验证，结果以评论形式反馈（✅ 通过 / ❌ 未通过）

> 💡 如果当前任务不涉及代码修改（比如只需要设置个人信息），你可以随便加个文件（比如添加一个 `hello.txt` 写下你的名字），只要能提交一个 PR 触发流水线就行。

* * *

## 任务清单

### Level 1：个人信息 ⭐

编号| 任务| 说明| 参考文档
---|---|---|---
1.1| 修改默认用户名| CNB 注册后会分配一个默认用户名（如 `cnb.cwH7BL2BwHA`），前往 [账号设置](https://cnb.cool/profile/account) 修改为一个有辨识度的用户名| 无
1.2| 设置个人签名| 个人签名（Bio）会展示在你的主页上，让其他开发者快速了解你。进入 [个人设置](https://cnb.cool/profile) 填写即可| 无
1.3| 设置个人仓库墙| 仓库墙是你个人主页上的"橱窗"，Pin 上你最得意的项目，让访客一眼看到你的代表作| 无
1.4| 关注指定用户| 关注其他开发者后，你可以在动态中看到他们的最新活动。比如可以关注：[轩](https://cnb.cool/u/valetzx)、[Ar-Sr-Na](https://cnb.cool/u/arsrna)、[Anye](https://cnb.cool/u/Anye)、[幽静森林](https://cnb.cool/u/momo)、[没猫饼](https://cnb.cool/u/leun) 等等| 无
1.5| 关注指定仓库| Star 是对优质仓库的认可。比如 Star 以下仓库：[cnb/feedback](https://cnb.cool/cnb/feedback)、[examples/showcase](https://cnb.cool/examples/showcase)| 无

### Level 2：仓库设置 ⭐

编号| 任务| 说明| 参考文档
---|---|---|---
2.1| 配置保护分支| 保护分支可以防止未经 Review 的代码直接 push 到主分支。在仓库「设置 → 分支保护」中配置。如果你是仓库负责人或管理员，可以同时开启「管理员及负责人可以推送到保护分支」选项，以保证后续闯关更顺利| 无
2.2| 添加开源 LICENSE| 开源许可证声明了代码的使用规则。没有 LICENSE 的代码默认是"保留所有权利"的，加一个标准许可证（如 MIT）才能让别人放心使用你的代码| [Choose a License](https://cnb.cool/110?url=https%3A%2F%2Fchoosealicense.com%2Flicenses%2F)
2.3| 仓库 UI 定制| 通过 `.cnb/settings.yml` 配置文件，你可以自定义仓库页面上 Fork 按钮和云原生开发按钮的描述、悬浮图片等，让仓库更有个性| [UI 定制](https://docs.cnb.cool/zh/repo/settings.html)

### Level 3：流水线配置 ⭐⭐

编号| 任务| 说明| 参考文档
---|---|---|---
3.1| 开启事件自动触发| Fork 的仓库默认不会自动触发云原生构建。需要在仓库「设置 → 云原生构建」中开启「允许事件自动触发」，这样后续的流水线任务才能正常运行| 无
3.2| Push 触发器| 最基础的触发方式，代码推送到指定分支时自动运行流水线，适合持续集成场景| [快速开始](https://docs.cnb.cool/zh/build/quick-start.html)
3.3| Pull Request 触发器| PR 创建或更新时触发，用于自动化代码检查、单元测试、构建验证，是 Code Review 的好帮手| [Pull Request 事件](https://docs.cnb.cool/zh/build/trigger-rule.html#pull-request-shi-jian)
3.4| Tag push 触发器| 推送 Tag 时触发，通常用于发布 Release、构建正式版本的镜像| [Tag 事件](https://docs.cnb.cool/zh/build/trigger-rule.html#tag-shi-jian)
3.5| Web trigger 触发器| 在仓库构建页面手动点击触发，适合需要人工确认后才执行的任务| [页面操作事件](https://docs.cnb.cool/zh/build/web-trigger.html)
3.6| 部署触发器| 通过 `.cnb/tag_deploy.yml` 定义部署环境和审批流程，在 Release 页面一键部署，支持多环境串联和审批机制| [自定义部署](https://docs.cnb.cool/zh/build/deploy.html)

### Level 4：云原生开发 ⭐⭐

编号| 任务| 说明| 参考文档
---|---|---|---
4.1| 使用云原生开发环境| 点击仓库页面的「云原生开发」按钮，即可在浏览器中启动一个完整的开发环境（VS Code），无需在本地安装任何工具| [云原生开发介绍](https://docs.cnb.cool/zh/workspaces/intro.html)
4.2| 配置自定义开发环境| 默认开发环境可能不包含你需要的工具。通过在 `.cnb.yml` 的 `vscode` 事件中指定自定义 Docker 镜像，可以预装特定语言、框架和工具链| [自定义开发环境](https://docs.cnb.cool/zh/workspaces/custom-dev-env.html)
4.3| 配置开发环境预览| 配置 `onlyPreview` 和 `launch` 后，云原生开发环境会自动启动你的 Web 应用并提供在线预览链接，方便实时查看效果| [预览模式配置](https://docs.cnb.cool/zh/workspaces/only-preview.html#ru-he-pei-zhi)

### Level 5：制品管理 ⭐⭐⭐

编号| 任务| 说明| 参考文档
---|---|---|---
5.1| Docker 制品| 通过流水线构建 Docker 镜像并推送到 CNB 内置制品库，实现代码到可部署镜像的自动化。制品库地址格式：`docker.cnb.cool/<slug>/<image-name>`| [Docker 制品](https://docs.cnb.cool/zh/artifact/docker.html)

### Level 6：任务集 ⭐⭐

编号| 任务| 说明| 参考文档
---|---|---|---
6.1| 创建任务集| 任务集（Missions）是 CNB 的轻量项目管理功能，支持创建、分配和追踪工作项。你可以在组织中创建任务集来管理团队的开发计划和 Bug 跟踪| [任务集](https://docs.cnb.cool/zh/missions/intro.html)

### Level 7：NPC & 知识库 ⭐⭐⭐

编号| 任务| 说明| 参考文档
---|---|---|---
7.1| 开启仓库知识库| 开启知识库后，AI 会自动索引你的代码仓库内容，在 Issue 和 PR 中提供更精准的上下文感知回答。在仓库「设置」中一键开启| [知识库](https://docs.cnb.cool/zh/ai/knowledge-base.html)
7.2| 创建并启用 NPC| NPC（Non-Player Character）是 CNB 平台的 AI 智能助手。你可以创建自定义 NPC，它能自动进行代码评审、总结 PR、回答技术问题，甚至根据需求修改代码| [NPC](https://docs.cnb.cool/zh/build/npc.html)

* * *

**共 7 个关卡，21 个任务。** 祝你闯关愉快！

* * *

## 🏆 通关奖励

全部通关者，自动获得 CNB「天才程序员」身份，凭借身份自助领取专属特权：

**【天才程序员专属特权】** ：

**AI Credits** ：666 Credits/月
**有效期** ：永久
**领取方式** ：完成闯关，前往「个人设置-身份认证」自助领取

> 注：特权不叠加，因为叠加后数字就不炫酷了

* * *

## 参考文档

闯关过程中遇到问题，可以随时召唤 NPC 协助，也可以查阅以下文档：

  * [NPC 使用指南](https://cnb.cool/npc/CodeBuddy/-/issues/120) — 了解如何召唤和使用 NPC
  * [CNB 帮助文档](https://docs.cnb.cool/zh/) — CNB 平台官方文档
  * [从 Git 到 AI 编程](https://cnb.cool/whut1/ai-engineering-course) — 开发进阶学习课程

* * *

## 反馈

遇到问题？欢迎在 [cnb/feedback](https://cnb.cool/cnb/feedback) 提 Issue 反馈。

### 赞赏

![](/users/sixther/avatar/s)

[sixther(段超)](/u/sixther)

![](/users/songjiao/avatar/s)

[songjiao(水不绿)](/u/songjiao)

![](/users/youkun/avatar/s)

[youkun(哪堵通临时工)](/u/youkun)

### 简介

通过闯关的方式，探索 CNB 平台的核心功能。完成任务，提交 PR，让 CI 告诉你答案。 Explore CNB's core features through a series of challenges. Complete tasks, submit a PR, and let CI tell you the result.

65.93 MiB

612.82 KiB

[1377 forks](/cnb/tutorial/hello-cnb/-/insights/forks?tabId=current)[168 关注](/cnb/tutorial/hello-cnb/-/stargazers)[15 分支](/cnb/tutorial/hello-cnb/-/branches)[1 Tag](/cnb/tutorial/hello-cnb/-/tags)README

### [Release](/cnb/tutorial/hello-cnb/-/releases)

0

[Tag1](/cnb/tutorial/hello-cnb/-/tags)

### 赞赏

![](/users/sixther/avatar/s)

[sixther(段超)](/u/sixther)

![](/users/songjiao/avatar/s)

[songjiao(水不绿)](/u/songjiao)

![](/users/youkun/avatar/s)

[youkun(哪堵通临时工)](/u/youkun)

### [贡献者](/cnb/tutorial/hello-cnb/-/insights/contributors)

4

![](/users/sixther/avatar/s)

![](/users/songjiao/avatar/s)

![](/users/chunyu/avatar/s)

![](/users/youkun/avatar/s)
