---
title: CSS 现代布局（Flex/Grid）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - CSS
  - Flexbox
  - CSS Grid
  - 布局
aliases:
  - CSS 现代布局
  - Flex 与 Grid 布局
source:
  - 网络资料整理
---

# CSS 现代布局（Flex/Grid）

> [!摘要] 摘要
> 本文是 [[Vue3与前端-从入门到精通]] 体系中「样式与布局」这一层的落地文档，系统讲解 CSS 现代布局的两大主力——**Flexbox（一维布局）**与 **CSS Grid（二维布局）**，并覆盖容器查询、`:has()`、逻辑属性等 2026 年的主流趋势。目标是读完后能独立完成导航栏、卡片流、整页栅格与自适应组件四类常见结构的编写，并清楚两者的选型边界与常见坑。

## 一、最新动态（截至 2026-11）

CSS 布局的核心能力早已进入「广泛可用」阶段，近两年的变化集中在**响应式粒度从视口下沉到组件**，以及选择器与语法的现代化：

- **Grid 布局**：Widely available，Baseline 基线日期 **2017-10-17**，属于可放心使用的成熟能力。
- **Container Queries（容器查询）**：Widely available，Baseline 基线日期 **2023-02-14**。组件开始能根据自身容器而非视口尺寸响应。
- **Subgrid（子网格）**：Widely available，Baseline 基线日期 **2023-09-15**，子网格可继承父网格的轨道定义。
- **Style queries（`@container style()`）**：较新能力，**2026 年 5 月成为 Baseline Newly Available**（Chrome 111+、Safari 18+、Firefox 151+）。不支持的浏览器会**整体跳过该 `@container style()` 块**，因此结构默认值必须写在该规则之外。
- **现代趋势**：容器查询把响应式从「视口」转向「组件」；`:has()` 选择器（父选择器/关系选择器）、CSS 嵌套、`aspect-ratio`、`gap`、逻辑属性（`inline-*` / `block-*`）已成为日常写法。

> [!info] 口径说明
> 以上日期与浏览器支持均来自调研基线文件，截至 **2026-11**；CSS 能力无独立版本号，落地时以 [MDN 兼容性数据](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Flexbox) 为准。

## 二、基础概念

**核心心智模型：布局就是「在容器内如何分配空间」。** 现代布局不再依赖 `float`、`position` 硬拼，而是用两种正交的模型：

- **Flexbox（弹性盒）**：**一维**布局，只沿**一条轴**（行或列）分配空间与对齐。适合导航栏、工具栏、按钮组、卡片流等「线性排列 + 弹性伸缩」的场景。
- **CSS Grid（网格）**：**二维**布局，同时控制**行与列**两个维度，可精确定义行轨道、列轨道与区域。适合整页骨架、仪表盘、相册、复杂卡片矩阵等二维结构。

两者不是替代关系，而是**配合使用**：Grid 负责页面级骨架与二维分区，Flex 负责区块内部的线性排列。

| 维度 | Flexbox | CSS Grid |
| --- | --- | --- |
| 布局维度 | 一维（单轴） | 二维（行 + 列） |
| 核心属性 | `flex-direction`、`justify-content`、`align-items`、`flex` | `grid-template-columns`、`grid-template-rows`、`grid-template-areas` |
| 典型场景 | 导航、工具栏、卡片流 | 整页、栅格、复杂二维结构 |
| 弹性来源 | 项目自身的 `flex` 三要素 | 轨道尺寸（`fr`、`auto`、`minmax()` 等） |

## 三、核心机制

### 3.1 Flexbox 的弹性三要素

容器设 `display: flex` 后，子项沿主轴排列。子项的空间分配由 `flex` 简写决定，它是 **`flex-grow`（放大比例）、`flex-shrink`（收缩比例）、`flex-basis`（初始基准尺寸）** 三者的组合：

```css
/* 容器：确定主轴方向、对齐与间距 */
.toolbar {
  display: flex;
  flex-direction: row;        /* 主轴方向：row / column */
  justify-content: space-between; /* 主轴对齐：start/center/space-between… */
  align-items: center;        /* 交叉轴对齐：center/stretch/baseline… */
  gap: 12px;                  /* 子项之间间距，无需再写 margin */
}

/* 子项：决定各自在剩余空间里的伸缩 */
.toolbar .grow { flex: 1; }              /* 占满剩余空间 */
.toolbar .fixed { flex: 0 0 120px; }    /* 不放大、不收缩、基准 120px */
```

关键机制：`flex-grow` 只分配**剩余空间**；空间不足时按 `flex-shrink` 收缩；`flex-basis` 是计算的起点，默认 `auto` 表示取内容尺寸。

### 3.2 Grid 的轨道与区域

容器设 `display: grid` 后，用 `grid-template-*` 定义轨道，用 `grid-column` / `grid-row` 或命名区域把项目放进格子：

```css
.page {
  display: grid;
  grid-template-columns: 240px 1fr;   /* 固定侧栏 + 弹性主内容 */
  grid-template-rows: auto 1fr auto;  /* 头部、主体、页脚 */
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer  footer";
  gap: 16px;
}
.page > .header  { grid-area: header; }
.page > .sidebar { grid-area: sidebar; }
.page > .main    { grid-area: main; }
.page > .footer  { grid-area: footer; }
```

**`fr` 是「份数」不是长度**：`1fr 2fr` 表示按 1:2 分配可用空间。配合 `minmax(min, max)`、`repeat()` 可实现自适应栅格：

```css
.cards {
  display: grid;
  /* 每列最小 240px，随容器自动增列，最多 4 列 */
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
```

### 3.3 容器查询：从视口到组件

容器查询让组件**根据自身所处容器的尺寸**切换样式，而非依赖视口：

```css
/* 建立查询上下文：需在父级声明 containment */
.card-wrap {
  container-type: inline-size;
  container-name: card;
}

/* 容器宽度小于 400px 时，卡片改为纵向布局 */
@container card (max-width: 400px) {
  .card { flex-direction: column; }
}
```

这一能力让同一个卡片组件能在侧栏、主栏、弹窗等不同位置自动适配，是组件化时代响应式的关键一步。

## 四、实践步骤（含代码/命令示例）

### 4.1 用 Flexbox 做响应式导航栏

```html
<nav class="nav">
  <span class="brand">站点名</span>
  <ul class="nav__list">
    <li><a href="/">首页</a></li>
    <li><a href="/docs">文档</a></li>
    <li><a href="/about">关于</a></li>
  </ul>
  <button class="nav__menu">菜单</button>
</nav>
```

```css
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 20px;
}
.nav__list {
  display: flex;
  gap: 20px;
  list-style: none;
  margin: 0;
}
/* 窄屏：导航项收缩为可换行，菜单按钮始终靠右 */
@media (max-width: 640px) {
  .nav { flex-wrap: wrap; }
  .nav__list { flex-wrap: wrap; }
}
```

### 4.2 用 Grid 做整页骨架

```css
.layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  min-height: 100vh;
  gap: 16px;
}
@media (max-width: 768px) {
  /* 移动端去掉二维结构，退化为单列堆叠 */
  .layout {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "main"
      "sidebar"
      "footer";
  }
}
```

### 4.3 用容器查询做自适应卡片

```css
.card-wrap {
  container-type: inline-size;
}
.card {
  display: flex;
  gap: 12px;
}
@container (min-width: 380px) {
  .card { flex-direction: row; }   /* 宽容器：横向 */
}
@container (max-width: 379px) {
  .card { flex-direction: column; } /* 窄容器：纵向 */
}
```

### 4.4 快速验证布局

用浏览器 DevTools 的 **Layout** 面板可直观查看 Grid 轨道与 Flex 伸缩；也可将上面的片段放入 [MDN 示例](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Flexbox) 或本地 HTML 直接预览，无需构建工具。

## 五、最佳实践与常见坑

- **选型边界**：线性排列、局部弹性用 Flex；需要同时控制行和列、整页骨架用 Grid。**不要把 Grid 当 Flex 用**（反之亦然），否则对齐逻辑会难以维护。
- **`gap` 取代 `margin`**：Flex/Grid 容器用 `gap` 控制子项间距，无需逐项写 `margin`，且 `gap` 对 `wrap` 换行同样生效。
- **`flex: 1` 与 `min-width: auto` 的坑**：Flex 子项默认 `min-width: auto`，内容较宽时会**撑破**预期尺寸。需要真正收缩时加 `min-width: 0`（或 `min-height: 0`）。
- **Grid 的隐式轨道**：项目超出显式定义的轨道时，浏览器会自动生成隐式行/列。用 `grid-auto-rows` / `grid-auto-columns` 显式控制，避免尺寸失控。
- **`fr` 不是长度单位**：`1fr` 只在**剩余空间**上分配；与固定长度混用时要明确哪个是固定、哪个是弹性。
- **容器查询的降级**：`@container style()` 等新特性在部分浏览器会**整块跳过**，务必把默认结构写在 `@container` 规则之外；`container-type` 会影响子元素尺寸，注意其包含块影响。
- **避免布局抖动**：避免在循环中读写 `offsetWidth` / `getBoundingClientRect()` 等触发强制同步布局的属性。
- **逻辑属性优先**：用 `inline-*` / `block-*`、`margin-inline-start` 等逻辑属性，天然适配 RTL 与多语言，减少方向性硬编码。
- **与 Vue 组件配合**：在 `.vue` 的 `<style scoped>` 中，Flex/Grid 规则仅作用于当前组件，跨组件结构由容器查询或 CSS 变量协调，见 [[Vue3与前端-从入门到精通]] 的样式隔离说明。

## 六、核心要点速查

1. **Flexbox 管一维、Grid 管二维**；页面骨架用 Grid，区块内部用 Flex。
2. Flex 三要素：`flex-grow` / `flex-shrink` / `flex-basis`，`flex` 是其简写。
3. Flex 对齐：主轴 `justify-content`，交叉轴 `align-items`；间距统一用 `gap`。
4. Grid 轨道用 `grid-template-columns/rows`，`fr` 按剩余空间的份数分配，不是长度。
5. 命名区域 `grid-template-areas` + `grid-area` 让二维结构一目了然，便于响应式重排。
6. `repeat(auto-fit, minmax(240px, 1fr))` 是自适应多列卡片的通用写法。
7. 容器查询让组件**依容器而非视口**响应，需先声明 `container-type`。
8. `@container style()` 于 **2026 年 5 月**成为 Baseline Newly Available，默认值必须写在规则外。
9. Flex 子项内容过宽时，加 `min-width: 0` 才能按预期收缩。
10. 优先使用逻辑属性与 `aspect-ratio`、`gap` 等现代特性，减少方向性与尺寸硬编码。

## 七、学习资源

- [MDN · Flexbox 布局（中文）](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Flexbox)
- [MDN · CSS Grid 布局（中文）](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Grids)
- [MDN · 容器查询（中文）](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_containment)
- [MDN · `:has()` 选择器（中文）](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Pseudo-classes/has)
- [web.dev · 现代 CSS 能力速览](https://web.dev/articles/modern-css)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本知识点所属的 Vue3 与前端体系总览
- [[前端开发]] — 前端技术整体地图与目录索引
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
