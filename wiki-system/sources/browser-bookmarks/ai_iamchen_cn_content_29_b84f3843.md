---
source: "https://ai.iamchen.cn/content/29"
title: "OpenCode 规则详解：AGENTS.md、优先级与自定义指令 - AI开发小站"
fetched_at: "2026-10-05 15:46:08"
---

[ AI使用笔记 ](/category/ainotes "AI使用笔记") 2026-03-24 3556

#  OpenCode 规则详解：AGENTS.md、优先级与自定义指令

# OpenCode 规则详解：AGENTS.md、优先级与自定义指令

如果你刚开始用 OpenCode，或者正准备把现有工作流迁到 OpenCode，那么有一件事最好尽早弄明白: 规则系统到底怎么配。很多人第一次接触时，只知道项目里可以放一个 `AGENTS.md`，但不清楚它和全局规则、`CLAUDE.md`、`opencode.json` 到底是什么关系。

这篇文章就按“教程”的方式来讲清这件事。内容基于 OpenCode 官方 `rules` 页面整理，我们一步一步看懂:

  * `AGENTS.md` 是什么，适合写什么
  * 项目级规则和全局级规则怎么分工
  * OpenCode 如何兼容 Claude Code 的规则文件
  * 规则文件的优先级到底怎么判定
  * 怎么用 `opencode.json` 把规则拆得更清晰、更好维护

## 先搞懂：OpenCode 规则到底是什么

OpenCode 将规则定义为一组“给模型的自定义指令”。最常见的承载文件是项目里的 `AGENTS.md`。它的定位很明确: 不是普通文档，而是会直接影响模型行为的上下文配置。

官方文档给出的信息有两个重点:

  1. `AGENTS.md` 用来描述项目特定的约束、结构和协作方式。
  2. 这些内容会被纳入模型上下文，让模型在编码、导航项目和执行任务时更贴近实际需求。

从使用价值看，`AGENTS.md` 很适合沉淀这些内容:

  * 项目目录结构和模块职责
  * 代码风格和技术栈约束
  * monorepo 的包管理约定
  * 团队共享的开发规则

文档中的示例就展示了一个 SST v3 monorepo 的 `AGENTS.md`，里面包含项目结构、TypeScript 规范和包引用方式。这说明 OpenCode 鼓励把“项目级事实”和“协作级约束”写成清晰规则，而不是每次都靠临时提示重复说明。

如果用一句话概括，`AGENTS.md` 的作用就是: 把“每次都要重复告诉模型的话”，沉淀成项目里的长期规则。

## 第一步：先把 AGENTS.md 建起来

创建规则文件有两种方式。

第一种是运行 `/init`。官方说明中提到，这个命令会扫描项目及其内容，理解项目用途，然后生成一个新的 `AGENTS.md`。如果项目里已经有该文件，`/init` 会尝试在原有基础上进行补充。

第二种是手动编写。对于结构清晰、已有规范沉淀的团队，手动维护通常更可控，因为你可以精确决定哪些内容应该成为模型的长期规则。

官方还有一个很值得注意的建议: 项目中的 `AGENTS.md` 应该提交到 Git。它背后的含义很直接，规则不仅服务当前用户，也服务整个团队的协作一致性。

如果你不知道第一版该写什么，可以优先放这几类内容:

  * 项目结构和目录职责
  * 技术栈和代码规范
  * 团队约定的开发流程
  * 需要模型长期遵守的限制条件

这一步的目标不是“把所有文档都塞进去”，而是先把最关键、最稳定、最常复用的规则写出来。

## 第二步：分清项目级规则和全局级规则

OpenCode 支持从多个位置读取规则文件，不同位置对应不同用途。

### 项目级规则

项目根目录中的 `AGENTS.md` 用来定义项目特定规则。这些规则只会在你位于该目录或其子目录中工作时生效。

这类规则适合放团队共享内容，例如:

  * 仓库结构说明
  * 模块边界
  * 测试约定
  * 提交和协作习惯

### 全局级规则

如果你希望所有 OpenCode 会话都遵循同一套个人偏好，可以使用 `~/.config/opencode/AGENTS.md`。官方文档特别说明，这个文件不会提交到 Git，也不会与团队共享，因此更适合存放个人规则。

比如，你可以把这类偏好放在全局文件里:

  * 个人常用的回答风格
  * 习惯性的代码审查关注点
  * 固定的调试流程

教程里最容易搞混的一点就是: 哪些内容该放项目里，哪些内容该放全局里。一个简单判断标准是:

  * 会影响整个团队协作的，放项目级 `AGENTS.md`
  * 只代表你个人习惯的，放 `~/.config/opencode/AGENTS.md`

这样分开后，规则会更清晰，也更不容易在团队里引入“只有你自己才需要”的偏好。

## 第三步：如果你从 Claude Code 迁移，要知道这层兼容回退

对于从 Claude Code 迁移过来的用户，OpenCode 提供了兼容回退方案。也就是说，当 OpenCode 找不到对应的 `AGENTS.md` 配置时，它还能识别 Claude Code 体系里的约定文件。

官方列出的回退来源包括:

  * 项目规则: 项目目录中的 `CLAUDE.md`
  * 全局规则: `~/.claude/CLAUDE.md`
  * 技能目录: `~/.claude/skills/`

如果你希望彻底关闭这套兼容能力，可以设置以下环境变量:

bash 复制


    export OPENCODE_DISABLE_CLAUDE_CODE=1
    export OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1
    export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1


这里要注意，兼容机制的定位是“回退”，不是主路径。只要 OpenCode 自己的规则文件存在，它们会优先生效。

如果你正在做迁移，比较稳妥的做法通常是:

  1. 先保留现有 `CLAUDE.md` 和 `~/.claude/skills/`
  2. 再逐步把核心规则迁到 `AGENTS.md`
  3. 等 OpenCode 规则稳定后，再决定是否关闭 Claude Code 兼容

这样迁移成本更低，也不容易因为一次性切换而丢掉原有规则。

## 第四步：一定要搞懂规则优先级

官方文档把规则查找顺序写得非常清楚。OpenCode 启动后，会按以下顺序寻找规则文件:

  1. 本地文件，从当前目录向上遍历查找 `AGENTS.md` 和 `CLAUDE.md`
  2. 全局文件 `~/.config/opencode/AGENTS.md`
  3. Claude Code 全局文件 `~/.claude/CLAUDE.md`，前提是兼容性未被禁用

这套优先级可以帮助我们快速理解两个常见问题。

第一，`AGENTS.md` 和 `CLAUDE.md` 不是同级叠加关系。文档明确指出，在同一类别里，第一个匹配的文件优先。如果项目里同时存在 `AGENTS.md` 和 `CLAUDE.md`，最终只会使用 `AGENTS.md`。

第二，OpenCode 自己的全局规则也优先于 Claude Code 的全局规则。也就是说，如果你已经配置了 `~/.config/opencode/AGENTS.md`，那么 `~/.claude/CLAUDE.md` 不会成为更高优先级的来源。

这意味着在迁移过程中，最稳妥的方式通常是:

  * 先把团队规则集中到项目级 `AGENTS.md`
  * 再把个人偏好写入 `~/.config/opencode/AGENTS.md`
  * 最后只把 Claude Code 文件视作兼容兜底

如果你只记一个结论，那就是: 同一层级里不要假设多个规则文件会同时叠加，OpenCode 会优先选择第一个匹配项。

## 第五步：学会用 opencode.json 拆分规则

如果团队已经有成熟的规范文件，没必要把所有内容都复制进 `AGENTS.md`。OpenCode 提供了一个更灵活的方式: 在 `opencode.json` 或 `~/.config/opencode/opencode.json` 中使用 `instructions` 字段，引用额外的指令文件。

官方示例说明，`instructions` 支持以下几类来源:

  * 本地 Markdown 或说明文档，例如 `CONTRIBUTING.md`
  * 多个目录下的规则文件，例如 `docs/guidelines.md`
  * glob 模式，例如 `.cursor/rules/*.md` 或 `packages/*/AGENTS.md`
  * 远程 URL

一个典型示例如下:

json 复制


    {
      "$schema": "https://opencode.ai/config.json",
      "instructions": [
        "CONTRIBUTING.md",
        "docs/guidelines.md",
        ".cursor/rules/*.md"
      ]
    }


如果使用远程 URL，官方文档说明抓取超时时间为 5 秒。另一个很重要的点是，这些外部指令文件不会替代 `AGENTS.md`，而是与它合并使用。

这让 OpenCode 的规则体系更适合大型项目，因为你可以把稳定规范拆分到多个文件中，避免单个 `AGENTS.md` 变得臃肿。

对 monorepo 来说，这一步尤其重要。因为一旦包很多、规范很多，单个 `AGENTS.md` 很快就会变得又长又难维护，而 `instructions` \+ glob 能把规则按目录、按职责拆开。

## 第六步：别误会，OpenCode 不会自动解析 AGENTS.md 里的引用

不会。官方在“引用外部文件”一节里专门强调，OpenCode 不会自动解析 `AGENTS.md` 中写到的文件引用。

如果你确实希望模型按需读取外部规则，官方给出了两种思路:

  1. 优先使用 `opencode.json` 的 `instructions`
  2. 在 `AGENTS.md` 中显式写出读取策略，让模型在遇到文件引用时按需加载

文档里的示例非常强调“按需”这个原则，包括:

  * 不要预先加载所有引用
  * 已加载内容应视为覆盖默认行为的强制指令
  * 必要时继续递归跟进引用

这个设计很实用，因为它避免了在项目一开始就把大量无关规则塞进上下文，减少噪音，也更利于复杂仓库中的任务分流。

换句话说，如果你在 `AGENTS.md` 里写了“请参考某个文件”，OpenCode 本身不会替你自动展开它。更推荐的做法，还是把外部规则通过 `opencode.json` 的 `instructions` 明确接进来。

## 一套更容易落地的配置思路

基于官方页面内容，可以整理出一套很实用的落地思路。

对于普通项目:

  * 在项目根目录维护一份清晰的 `AGENTS.md`
  * 把团队统一规范提交到 Git
  * 把个人偏好留给 `~/.config/opencode/AGENTS.md`

对于正在从 Claude Code 迁移的项目:

  * 短期内可以保留 `CLAUDE.md` 和 `~/.claude/skills/` 作为回退
  * 中长期建议逐步转向 OpenCode 自己的规则入口

对于 monorepo:

  * 优先考虑 `opencode.json` \+ glob 模式
  * 把共享标准拆到多个可复用文件中
  * 用 `packages/*/AGENTS.md` 之类的方式组织包级规则

官方文档还特别提到，在 monorepo 或具有共享标准的项目中，`opencode.json` 配合 glob 模式通常比手动在 `AGENTS.md` 中逐条声明更易维护。这一点很值得直接采纳。

如果你想直接照着做，可以用下面这套最小实践:

  1. 在项目根目录建立并维护 `AGENTS.md`
  2. 把个人偏好写进 `~/.config/opencode/AGENTS.md`
  3. 如果是迁移项目，先把 `CLAUDE.md` 当回退，不急着删除
  4. 规则开始变多后，用 `opencode.json` 的 `instructions` 做拆分
  5. monorepo 优先采用 glob 组织方式，而不是把所有规则都堆在一个文件里

## 总结：把规则写成工程资产，而不是临时提示

OpenCode 的规则系统并不只是一个“提示词文件”机制，它实际上定义了模型如何理解项目、如何继承团队规范，以及如何兼容已有的 Claude Code 工作流。

如果只记住最关键的几点，可以抓住下面这条主线:

  * 用 `AGENTS.md` 承载项目级规则
  * 用 `~/.config/opencode/AGENTS.md` 承载个人级规则
  * 把 `CLAUDE.md` 看作迁移期的兼容回退
  * 用 `opencode.json` 的 `instructions` 做模块化扩展
  * 在复杂项目里优先选择可维护、可复用、按需加载的规则组织方式

这样配置后，OpenCode 会更容易理解你的仓库结构、团队约束和工作习惯，规则也会从“零散提示”变成真正可维护的工程资产。

感谢阅读，如果这篇文章对你有帮助，欢迎继续浏览同栏目内容。
