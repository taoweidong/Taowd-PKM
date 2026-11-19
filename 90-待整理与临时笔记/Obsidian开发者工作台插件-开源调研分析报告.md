---
title: Obsidian 开发者个人工作台插件 — 开源调研分析报告
date: 2026-11-18
tags:
  - 项目/obsidian工作台
  - 调研报告
  - obsidian/插件开发
status: 调研完成-待立项
---

# Obsidian 开发者个人工作台插件 — 开源调研分析报告

> [!abstract] 一句话结论
> 深挖 11 个首页/仪表盘类插件后确认：**无一提供常驻侧边栏工作台**（Hearth 的侧边栏诉求 #492 仍是 feature request）。「最近编辑 × 标签共现导航 × 常驻侧边栏」组合是市场空缺。但注意：Hearth 已内置 Terminal(htop) 设计语言、StartPage 已实现 mtime 混排——差异化不能只押"科技风"或"最近编辑"单点，要押**组合与垂直场景**。视觉上应融入 Style Settings 事实标准生态，而非对抗。

**产品目标**：面向软件开发人员的个人工作台。快捷查看近期编辑文件、标签聚合等；界面炫酷、科技风、内容一目了然。

调研时间：2026-11-18，star 数/许可证/活跃度经 GitHub 核实。

---

## 一、开源竞品全景

### 1.1 仪表盘 / 首页 / 工作台类

| 项目 | 许可证 | 热度 | 状态 | 形态 | 与需求的距离 |
|------|--------|------|------|------|--------------|
| [Hearth](https://github.com/ondreu/Hearth) | MIT | 242★ | **极活跃**（2026-11 仍日更） | 原生卡片网格，40+ 卡片拖拽，26 个集成（Git/Jira/Dataview…） | **最强竞品**。但最近文件按"打开"计；Git 仅浅集成；通用风格，无开发者定位 |
| [Dashboard navigator](https://github.com/drbap/dashboard-navigator-for-obsidian) | MIT | 260★ | **已归档，2026-03 下架** | 原生视图：最近创建/修改分组、标签组合导航、库统计 | 功能上最接近本需求，**它的退场留下了细分空白**；MIT 许可可研究借鉴 |
| [Homepage](https://github.com/mirnovov/obsidian-homepage) | MIT | 743★ | 活跃 | 只负责"启动时打开某笔记/工作区"，不渲染数据 | 无面板能力；可借鉴启动接管时机与命令钩子 |
| [Home tab](https://github.com/olrenso/obsidian-home-tab) | MIT | 377★ | **README 声明停止维护**（2024-10） | 浏览器式新标签页：搜索 + starred + recent | 无标签聚合/任务；代码块嵌入组件的交互可借鉴 |
| [StartPage](https://github.com/kuzzh/obsidian-startpage) | MIT | 37★ | 活跃（中文作者） | 库统计、置顶、最近访问+修改智能排序 | 覆盖部分诉求，但无标签维度、无开发者工具链 |
| [Dashboard++](https://github.com/TfTHacker/DashboardPlusPlus) | MIT | 1.2k★ | 示例库停更 | **非插件**：markdown 首页 + CSS + Dataview | 证明需求量大；DIY 路线的代表 |
| 其他 | — | — | — | [Harbor Tab](https://github.com/Moyf/harbor-tab)（8★活跃）、[Dashboards](https://github.com/kevinmcaleer/obsidian-dashboards)（7★，YAML 代码块网格）、[Home Launcher](https://github.com/soulbits-vibe/obsidian-home-launcher)（命令按钮 launcher） | 各占一角，均未做深 |

### 1.2 最近文件 / 标签 / 开发者工作流类

| 项目 | 许可证 | 热度 | 状态 | 覆盖度与可复用点 |
|------|--------|------|------|------------------|
| [Recent Files](https://github.com/tgrosinger/recent-files-obsidian) | **GPL-3.0** | 532★ | 活跃 | 只管最近**打开**，非编辑；侧边栏 ItemView 工程范式可学，**代码勿抄（GPL 传染）** |
| [Tag Wrangler](https://github.com/pjeby/tag-wrangler) | ISC | 937★ | 活跃 | 标签重命名/合并 + Tag Page 约定；**对外暴露事件接口，可直接集成**（本库已安装） |
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) | MIT | 9.4k★ | **实质维护模式**，继任者 Datacore 仍 WIP | 查询能实现两大诉求，但困在笔记阅读视图、不能常驻侧边栏、大库多查询拖慢启动 |
| [Projects](https://github.com/obsmd-projects/obsidian-projects) | Apache-2.0 | 1.9k★ | **2025-07 已归档** | 不可依赖；"数据源抽象 + 多视图"架构仅作设计参考 |
| [obsidian-git](https://github.com/Vinzent03/obsidian-git) | MIT | 12.3k★ | 活跃 | 开发者常驻侧边栏视图的最佳范本（本库已安装，自动备份中） |
| [obsidian-tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) | MIT | 4.1k★ | 活跃 | "聚合视图 + 勾选双向写回"范本（本库已安装） |
| [checklist](https://github.com/delashum/obsidian-checklist-plugin) | MIT | ~500★ | 低频维护 | 按标签聚合 TODO 的侧边栏，形态最接近工作台 |
| [tagfolder](https://github.com/vrtmrz/obsidian-tagfolder) | MIT | 354★ | 活跃 | 标签渲染成虚拟文件夹树，标签聚合视图直接参考 |

### 1.3 DIY 路线（Homepage + Dataview + Tasks + CSS）的痛点

社区主流做法是手工拼仪表盘笔记，典型板块：快捷链接、今日任务、活跃项目表、最近编辑（`SORT file.mtime DESC LIMIT 5`）、库统计。痛点：

1. 只能作为笔记在阅读视图渲染，**无法常驻侧边栏**，切文件即丢失；
2. 查询膨胀拖慢启动，语法脆弱、静默失效；
3. 死链与过滤条件漂移，维护成本高；
4. 依赖插件堆叠，且 Dataview 本身进入维护模式，社区已在讨论向 Bases/Datacore 迁移。

> [!tip] 结论
> DIY 路线的痛点恰好是原生插件的价值主张：**常驻、零查询语法、实时刷新、开箱即用**。

---

## 二、差异化定位

**不做**：又一个通用首页/卡片网格（Hearth 已做到极致且日更）；不替代 Dataview 查询引擎；不承载部署/编排类重逻辑。

**做**：开发者的「知识驾驶舱」——

- **常驻侧边栏 + 主区大屏双形态**：11 个竞品全部只有主区形态，这是最硬的差异化（侧边栏天然绕开"抢占新标签"事故雷区）；
- **标签共现导航**：dashboard-navigator 的独门功能（主标签→次级标签，Shift AND / Ctrl 排除），随其下架而绝迹，Bases 也替代不了；
- **最近编辑 ≠ 最近打开**：以 `mtime` 为第一排序维度。注意 StartPage 已做 mtime+访问时间混排，此点须与标签交叉过滤绑定才有区分度；
- **开发者工具链钩子**（后期可选）：git 状态、任务聚合、Tag Wrangler 事件、命令 launcher；
- **科技风视觉识别**：Hearth 已有 Terminal(htop) 设计，纯"终端风"不再是独占卖点；我们的视觉押注是「驾驶舱遥测」整体信息设计（状态条+编辑脉冲+等宽数据列），且通过 Style Settings 生态分发皮肤预设（见 4.7）。

---

## 三、技术可行性（官方 API 核对结论）

| 能力 | API | 公开性 | 结论 |
|------|-----|--------|------|
| 最近打开文件 | `workspace.getLastOpenFiles()` | ✅ 公开（最近 10 个） | 可作辅助维度 |
| 最近打开文件（长列表） | `workspace.getRecentFiles()` | ❌ **内部 API，d.ts 未收录** | 慎用，不作核心依赖 |
| 最近**编辑** | `vault.getMarkdownFiles()` + `TFile.stat.mtime` 排序；`vault.on('modify')` 增量更新 | ✅ 公开 | **核心路径，自建轻量索引** |
| 标签索引 | `metadataCache.getTags()` | ❌ undocumented（社区惯用） | 优先公开路径：`getAllTags(cache)` + `metadataCache.on('changed')` 自建索引 |
| 自定义视图 | `ItemView` + `registerView()` + `getLeaf()` | ✅ 公开 | 侧边栏/主区标签页均可 |
| 主题融合 | Obsidian CSS 变量（`--background-primary` 等） | ✅ | 科技风皮肤叠加在宿主变量之上，随明暗主题降级 |

> [!warning] 架构红线
> 核心功能只依赖公开 API + 自建索引，**不绑死 Dataview**（维护模式风险）；undocumented API 只作渐进增强，失效时自动降级。

**推荐架构（精简）**：TypeScript + 原生 ItemView（无重型前端框架），三层：

1. **数据层**：mtime 索引 + 标签索引，事件驱动增量刷新，防抖；
2. **视图层**：侧边栏速览视图 + 主区仪表盘视图，共享同一数据层；
3. **集成层**（可选、渐进）：Tag Wrangler 事件、obsidian-git 状态、Tasks 聚合。

实施阶段：M1 最近编辑 + 标签聚合侧边栏（核心闭环）→ M2 主区科技风仪表盘 + 置顶/搜索 → M3 开发者集成。不预先细化到代码层级。

---

## 四、视觉设计方向：科技风 × 一目了然

设计立场：这不是"给仪表盘套个黑壳"，而是把开发者的世界语汇——**终端、遥测、git 状态、时间线**——变成视觉语言。参照 frontend-design 流程先定 token 系统，再自查去模板化。

### 4.1 概念：「驾驶舱遥测」（Cockpit Telemetry）

把 vault 当作一台正在运行的系统：编辑是心跳，标签是子系统，任务是告警。一眼读到的不是"文件列表"，而是**系统状态**。

### 4.2 色彩 token（深色皮肤为主，浅色自动降级）

| Token | Hex | 角色 |
|-------|-----|------|
| `deck` | `#0A0E1A` | 深空蓝底（非纯黑，带蓝相，区别于通用 near-black） |
| `panel` | `#111827` | 面板层，与底色形成微弱层次 |
| `scan` | `#22D3EE` | 青色主 accent：数据、导航、选中态 |
| `pulse` | `#F59E0B` | 琥珀副 accent：时间、热度、需要注意的事 |
| `ok` / `alert` | `#34D399` / `#F87171` | 语义色：git 干净/任务完成 vs 冲突/逾期 |
| `ink` | `#E2E8F0` | 主文字，冷灰白 |

双 accent（青=空间/导航，琥珀=时间/热度）而非"近黑+单一荧光色"的套路；语义色只用于状态，不做装饰。

### 4.3 字体

- UI 文字：沿用宿主 `--font-interface`（尊重用户主题，不强行注入）；
- **数据一律等宽**（`--font-monospace`，推荐 JetBrains Mono）：mtime、计数、标签计数、分支名——这是开发者仪表的母语，数字对齐即信息；
- 层级靠字号/字重差（大数字 + 小标签），不靠全大写 eyebrow、不靠中点串 meta。

### 4.4 布局：信息 hierarchy 固定，左对齐，列表优先于卡片

```
┌──────────────────────────────────────────────┐
│ ● 在线  今日编辑 12   待办 3   main ✓        │ ← 状态条：一行读完系统状态
├──────────────────────────────────────────────┤
│ ▁▂▅▇▃▂▁▁▃▆▇▅▂  近 14 天编辑脉冲              │ ← 记忆点：活动 sparkline
├───────────────────────────┬──────────────────┤
│ 最近编辑                  │ 标签             │
│ 14:32 插件方案.md  #project│ #project    24   │
│ 11:07 PG索引.md    #db     │ #db         17   │
│ 昨天  周报.md      #work   │ #ai         12   │
│ …（等宽时间列对齐）        │ （点击即过滤左列）│
├───────────────────────────┴──────────────────┤
│ ⌘ 快捷入口：日记 / 新建 / 搜索 / git 提交     │
└──────────────────────────────────────────────┘
```

- **一目了然的三条规则**：① 状态条永远在最上，数字大、标签小；② 最近编辑默认 10 条内不滚动，时间列等宽对齐形成"扫描节奏"；③ 标签带计数，点击即交叉过滤，无二级页面。
- 用**分隔线与行**组织信息，不用清一色圆角卡片 + 软阴影（SaaS 卡片套路）；层级靠排版，不靠装饰。

### 4.5 动效：克制，只服务注意力

- 唯一编排时刻：视图打开时状态条数字滚动到位 + sparkline 从左向右描线，一次完成；
- 其余动效只响应用户动作（点击标签的过滤过渡、置顶的位置移动）；
- 编辑发生时对应行短暂亮起琥珀色（遥测感），不做常驻呼吸灯/粒子背景；
- 尊重 `prefers-reduced-motion`；所有动效可一键关闭（Obsidian 性能敏感）。

### 4.6 去模板化自查

- ❌ 近黑 + 单一荧光绿 → ✅ 深空蓝 + 青/琥珀双 accent + 语义色；
- ❌ 同质圆角卡片网格（Hearth 及 SaaS 套路）→ ✅ 行式列表 + 分隔线 + 等宽数据列；
- ❌ 全大写 eyebrow、中点 meta 串、每行 hover 浮起 → ✅ 数据用等宽字体承载，动效只响应动作；
- ✅ 大胆只花在一处：**编辑脉冲 sparkline**，其余安静克制。

### 4.7 生态融入策略（主题调研后的修正）

社区事实标准已核实：**Style Settings**（2.6k★，286 万下载）是外观定制基建，Border/AnuPpuccin 等主流主题的功能几乎全由它驱动。工作台皮肤的正确做法：

1. **默认皮肤只消费官方 CSS 变量**（`--background-primary`、`--interactive-accent`、`--font-monospace` 等），选择器限定在自己视图容器类下 → 自动适配用户明暗主题，不污染全局；
2. **「驾驶舱」科技风作为 class-toggle 预设叠加**，而非强制外观；全部视觉参数（强调色、密度、霓虹开关、动效开关）在自带 `styles.css` 里用 `/* @settings */` YAML 声明，onload 时触发 `parse-style-settings` → 用户在 Style Settings 面板里直接调；
3. 借鉴 **Minimal Theme Settings** 的"皮肤预设下拉 + 热键循环切换"，比裸 CSS 变量面板更一目了然；
4. 沉浸模式复用 **Hider** 公开的 `.hider-*` body 类契约，不自造隐藏逻辑；
5. 文件图标参考 Iconize 机制但**不硬依赖**（该插件已宣布停止维护）。

---

## 五、首页类插件深度对比（第二轮深挖）

### 5.1 功能点对比矩阵

| 项目 | 最近打开 | 最近编辑mtime | 标签聚合 | 搜索 | 固定收藏 | 任务聚合 | 常驻侧边栏 | 主区视图 | 移动端 | 自定义布局 | 零依赖 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Homepage | ✗ | ✗ | ✗ | ✗ | 部分(pin标签) | ✗ | ✗ | ✓(开笔记) | ✓ | ✗(内容自理) | ✓ |
| Home tab | ✓ | ✗ | ✗ | ✓(名+类型) | ✓(starred已失效) | ✗ | ✗ | ✓ | 部分 | ✗ | ✓ |
| new-tab-default-page | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓(开笔记) | ✓ | ✗ | ✓ |
| **Hearth** | ✓ | 部分(热力图) | 部分(#搜索无面板) | ✓(全文+FM+命令) | ✓ | ✓(Kanban写回) | **✗** | ✓ | ✓ | ✓(自由网格) | ✓ |
| **StartPage** | ✓ | **✓(混排)** | ✗ | ✓(模糊) | ✓(pin+拖拽) | ✗ | **✗** | ✓ | ✓ | 部分 | ✓ |
| Harbor Tab | ✓ | ✗ | ✗ | ✓(名+标题跳转) | ✓(bookmarks) | ✗ | ✗ | ✓ | ✓ | 部分 | ✓ |
| Home Launcher | ✓ | ✗ | 部分 | ✓(全文+Omnisearch可选) | ✓ | ✗ | ✗ | ✓ | ✓ | 部分 | ✓ |
| Dashboards(mcaleer) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓(代码块) | ✓ | ✓(12列网格) | ✗ |
| **dashboard-navigator** | ✓ | ✓(分列) | **✓(共现导航)** | ✓(高级语法) | ✓ | ✗ | **✗** | ✓ | ✓ | 部分 | ✓ |
| Panda-995 模板 | ✗ | ✓ | ✓(标签云) | ✗ | ✗ | ✗ | ✗ | ✓(笔记) | ✓ | ✗ | ✗(需Dataview) |

**关键空位：全表"常驻侧边栏"一列皆 ✗。**

### 5.2 经典之所以经典

- **Homepage**（743★）：把"启动打开什么"一件事做到极致且零侵入——不造视图、不锁内容，与任何内容方案正交组合，成为所有仪表盘教程的默认底座；
- **Home tab**（377★）：第一个把"浏览器新标签页"心智（搜索框+收藏网格）完整搬进 Obsidian，键盘流交互树立品类 UX 标杆，停更后由官方授权的 Harbor Tab 续命；
- **Hearth**（242★，日更）：卡片自由网格 + 40 种卡 + 26 集成自动探测 + 移动端宽度阈值重排，一站式吃掉三类场景，是当前品类天花板；已有 Classic/Material3/Terminal(htop) 三套设计语言。

### 5.3 最值得抄的 5 个功能点

1. **StartPage 的 mtime+访问时间混排** + 相对时间每分钟刷新 + 事件驱动智能刷新（防抖、判断是否需刷新）——直接命中核心需求且移动端已验证；
2. **dashboard-navigator 的标签共现导航**（主标签→次级标签，Shift AND / Ctrl 排除，按频率排序）——全品类独一份，260★ 的立身之本；
3. **Hearth 的宽度阈值重排**（按实测宽度而非平台判断）——常驻侧边栏天然窄，此机制原样复用；
4. **Harbor 的标题级搜索跳转** + Home Launcher 的"结果自解释"（H1/命中段落/摘录）；
5. **pin 体系多入口**（右键+文件树菜单+拖拽排序）且**一键导入核心 Bookmarks**——不自建收藏孤岛。

### 5.4 最该避开的 3 个坑（竞品 issues 实证）

1. **抢占新标签/启动时机是事故高发区**：Home tab 与 Surfing 互斥；Homepage 的 openWhenEmpty 标志卡死 + 裸 catch 静默失败 + 移动端闪烁（#149/#142/#134）。→ 侧边栏形态天然绕开；主区视图的替换行为必须可关、失败显式报错并复位状态；
2. **实时刷新的性能与状态陷阱**：Hearth 的 Pet 卡 DOM 重建内存泄漏（#479）、卡内编辑触发整板刷新（#475）、侧栏伸缩闪烁（#462）、启动时设置不生效（#439）。→ 细粒度局部更新 + 防抖、编辑态冻结刷新、设置加载完成后再首渲；
3. **单人宽功能面 + 官方蚕食 = 死亡螺旋**：dashboard-navigator 作者自述倦怠 + 担忧 Bases 覆盖定位，两度归档终下架（issue #20）；Home tab 因核心 Starred→Bookmarks 变更无人修而收藏失效。→ 功能面收敛在开发者垂直场景，收藏直接读核心 Bookmarks API，对第三方插件 API 做防御性探测（Homepage #152 同款教训）。

---

## 六、主题/外观生态调研（第二轮）

### 6.1 外观定制类经典插件

| 项目 | 许可证 | 热度 | 状态 | 核心功能点 | 优点 | 缺点/局限 |
|------|--------|------|------|-----------|------|-----------|
| [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) | GPL-3.0 | 2.6k★/286万下载 | 转入 community-archive，低频维护 | CSS 内 `@settings` YAML 声明设置项；class-toggle/变量滑杆/双色 themed-color；扫描 themes/snippets/plugins 三目录 | **事实标准**，插件注册零成本（styles.css + 触发事件） | GPL 勿抄代码；已有 Style Tuner 等兼容替代品分流 |
| [Minimal Theme Settings](https://github.com/kepano/obsidian-minimal-settings) | MIT | 826★/190万下载 | 活跃 | 14 种配色预设、热键循环切换、焦点模式 | "主题+配套设置插件"模式范本，预设下拉比裸变量面板直观 | 绑定 Minimal 主题 |
| [Hider](https://github.com/kepano/obsidian-hider) | MIT | 592★ | 活跃 | body 类开关隐藏 ribbon/标签栏/状态栏；公开 `.hider-*` 类契约 | 沉浸模式可直接复用契约 | 功能单一 |
| [Iconize](https://github.com/FlorianWoelki/obsidian-iconize) | MIT | 1.4k★/231万下载 | **已宣布停止维护** | 图标包+自定义 SVG+规则匹配+frontmatter | 文件图标机制成熟 | 不宜硬依赖 |
| [Banners](https://github.com/noatpad/obsidian-banners) | — | 36万下载 | 低频 | 头图存 frontmatter、拖拽定位 | 数据与视图分离的范本 | 与工作台关联弱 |

### 6.2 科技风/开发者向主题

| 主题 | 数据 | 要点 |
|------|------|------|
| [Minimal](https://github.com/kepano/obsidian-minimal) | MIT 5.7k★ 活跃 | 极简+多配色，生态最完整 |
| [Border](https://github.com/Akifyss/obsidian-border) | MIT 2.5k★ 活跃 | 卡片化 UI；**预设以 Style Settings 导入代码分发——皮肤即配置** |
| [AnuPpuccin](https://github.com/AnubisNekhet/AnuPpuccin) | GPL 3.5k★ **停更** | Catppuccin 调色板；README 明言"无 Style Settings 只剩一小半功力" |
| [Blue Topaz](https://github.com/PKM-er/Blue-Topaz_Obsidian-css) | MIT 1.7k★ 活跃 | 中文社区经典，TIPS 示例库教学 |
| [Terminal](https://github.com/zcysxy/Obsidian-Terminal-Theme) | MIT 98★ 仅深色 | 最贴开发者风：单色绿+Fira Code、`$` 提示符、vim-airline 状态栏；**缺点：不优化插件 UI** |
| [Cybertron](https://github.com/nickmilo/Cybertron) | **无许可证** 137★ | Synthwave 霓虹；不宜复用代码 |

> [!tip] 结论
> 赛博/终端风主题存在但小众且多停更；主流高星主题证明"炫酷"靠**霓虹强调色 + 分区层次 + 等宽字体点缀**，而非全局单色。这与我们 4.2 的双 accent 方案互相印证。Terminal 主题"不优化插件 UI"的缺口，正是工作台自带科技风皮肤的价值。

---

## 七、风险与边界

| 风险 | 应对 |
|------|------|
| Hearth 日更迭代，可能补齐侧边栏与开发者功能 | 差异化押"侧边栏 + 标签共现 + 开发者垂直场景"组合，保持小快灵 |
| 官方 Bases 蚕食仪表盘定位（dashboard-navigator 死因之一） | 押 Bases 不做的能力：常驻侧边栏、标签共现导航、任务写回、工具链钩子 |
| undocumented API 随版本失效 | 核心只走公开 API；增强功能带降级 |
| GPL 代码传染（Recent Files、Style Settings、Workspaces Plus） | 只学范式不抄代码；可借鉴代码限 MIT/ISC/Apache（dashboard-navigator、tagfolder、tag-wrangler、StartPage） |
| 大库性能（本库数千笔记、60% 空占位） | mtime 排序 + 增量索引 + LIMIT；细粒度局部刷新 + 防抖（Hearth #475/#479 教训） |
| 抢占新标签/启动时机事故 | 侧边栏为主形态；主区替换可关、失败显式报错（Homepage #149 教训） |
| 第三方插件 API 变更即崩（Hearth Git 卡 #464） | 集成层防御性探测 + 优雅降级，核心功能零硬依赖 |
| Dataview 生态迁移期（Bases/Datacore） | 不依赖任何查询引擎，天然免疫 |

## 八、下一步

设计方案已成稿：[[Obsidian开发者工作台插件-设计方案]]（汇聚各开源插件核心功能点，F1-F12 均标注来源与优先级）。

1. 确认立项与插件名（暂名 **DevDeck / 开发驾驶舱**）；
2. M1 范围评审：最近编辑（mtime 混排）+ 标签共现导航 + 常驻侧边栏 + 科技风皮肤（Style Settings `@settings` 接入）；
3. 需要时再出技术选型评估（原生 DOM vs Svelte vs React：Obsidian 社区三种范式并存，属独立决策点）。

## 附：主要来源

- [Hearth](https://github.com/ondreu/Hearth) · [dashboard-navigator](https://github.com/drbap/dashboard-navigator-for-obsidian)（[下架记录](https://www.moritzjung.dev/obsidian-stats/plugins/dashboard-navigator/)）· [Homepage](https://github.com/mirnovov/obsidian-homepage) · [Home tab](https://github.com/olrenso/obsidian-home-tab) · [StartPage](https://github.com/kuzzh/obsidian-startpage) · [Dashboard++](https://github.com/TfTHacker/DashboardPlusPlus)
- [Recent Files](https://github.com/tgrosinger/recent-files-obsidian) · [Tag Wrangler](https://github.com/pjeby/tag-wrangler) · [Dataview](https://github.com/blacksmithgu/obsidian-dataview) · [Projects 停更公告](https://forum.obsidian.md/t/development-for-projects-plugin-needed/101089) · [obsidian-git](https://github.com/Vinzent03/obsidian-git) · [obsidian-tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) · [checklist](https://github.com/delashum/obsidian-checklist-plugin) · [tagfolder](https://github.com/vrtmrz/obsidian-tagfolder)
- [obsidian-api（官方 d.ts）](https://github.com/obsidianmd/obsidian-api) · [官方 CSS 变量参考](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables) · [Dashboard DIY 论坛方案](https://forum.obsidian.md/t/dashboard-a-simple-organization-and-navigation-method-for-obsidian-vaults/33197) · [Dataview 替代栈讨论](https://medium.com/@lennart-dde/obsidian-is-changing-the-new-plugin-stack-replacing-dataview-8084da60db2e)
- 第二轮深挖：[dashboard-navigator 归档原因 issue #20](https://github.com/drbap/dashboard-navigator-for-obsidian/issues/20) · [Hearth issues](https://github.com/ondreu/Hearth/issues) · [Homepage issues](https://github.com/mirnovov/obsidian-homepage/issues) · [Home tab fork 授权 #65](https://github.com/olrenso/obsidian-home-tab/issues/65) · [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) · [Minimal Theme Settings](https://github.com/kepano/obsidian-minimal-settings) · [Hider](https://github.com/kepano/obsidian-hider) · [Iconize](https://github.com/FlorianWoelki/obsidian-iconize) · [Terminal 主题](https://github.com/zcysxy/Obsidian-Terminal-Theme) · [Border](https://github.com/Akifyss/obsidian-border) · [AnuPpuccin](https://github.com/AnubisNekhet/AnuPpuccin) · [Blue Topaz](https://github.com/PKM-er/Blue-Topaz_Obsidian-css)