---
title: Vue3模板与指令进阶
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - 模板
  - 指令
  - Vapor-Mode
aliases:
  - Vue3 模板与指令进阶
source: 网络资料整理
---

# Vue3模板与指令进阶

> [!摘要] 内容与定位
> 本文聚焦 **Vue3 的模板编译机制与指令体系**：从「模板如何变成渲染函数」讲起，系统梳理内置指令（`v-if` / `v-for` / `v-model` / `v-memo` 等）的运行机制、编译期优化（静态提升、PatchFlags、事件缓存、TrustedHTML），再到自定义指令的两种接口（VDOM 与 Vapor），并给出可运行的代码示例与常见坑。它是 [[Vue3与前端-从入门到精通]] 进阶篇中「编译优化」与「模板/指令」两条线的展开，适合已掌握 `<script setup>` 基础、想深入理解 Vue3 渲染性能与指令底层的开发者。

## 一、最新动态（截至 2026-11）

- **稳定基线**：Vue 最新稳定版为 **3.5.45（2026-11-05 发布）**。3.5 系列首发于 2024-09-03，其中编译器新增输出 **TrustedHTML**，有利于在严格 CSP 下安全渲染。
- **3.6 进入 RC**：**Vue 3.6.0-rc.1（2026-07-17）** 的 **Vapor Mode 功能集已完成**，并把 `@vue/reactivity` 换为基于 **alien-signals** 的实现。**Vapor 与 VDOM 可共存，但属于 100% 可选的新编译模式，截至 2026-11 仍未进入稳定版**，官方建议仅用于性能敏感页面的局部使用或小型新应用。
- **`v-memo` 的 Vapor 兼容性**：**Vapor Mode 目前不支持 `v-memo`**，这是从 VDOM 迁移到 Vapor 时最容易踩到的指令差异。
- **`v-model` 的演进**：3.4 起引入 `v-model` 参数与多模型（`v-model:title`、`v-model:[dynamicArg]`）；3.5 修复了 `.trim` 与 `.number` 组合等行为细节。
- **自定义指令接口分叉**：VDOM 沿用 `{ mounted, updated, unmounted, ... }` 生命周期对象；**Vapor 的指令接口不同**，见「核心机制」。
- **事件委托（Vapor 特有）**：Vapor 会把符合条件的事件委托到 `document`，因此祖先调用 `stopPropagation()` 会导致委托处理不触发；`@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"` 可绕过委托直接绑定元素。

> 版本口径以官方仓库为准：[vuejs/core CHANGELOG](https://github.com/vuejs/core/blob/main/CHANGELOG.md)、[Vue 3.6.0-rc.1 发布说明](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)、[npm vue dist-tags](https://registry.npmjs.org/-/package/vue/dist-tags)。

## 二、基础概念

**模板（Template）** 是 Vue 组件中描述「状态 → 视图」映射的声明式部分。开发者不直接操作 DOM，而是写 `<template>`，由编译器在构建期（或运行时内联编译）转成可重复执行的渲染函数。这一「声明式 + 编译期优化」的组合是 Vue3 性能的底座。

**指令（Directive）** 是以 `v-` 为前缀的特殊属性，用于在模板中表达**逻辑、绑定、复用与性能控制**。Vue3 的内置指令按用途可分为四类：

| 类别 | 指令 | 作用 |
|------|------|------|
| 条件渲染 | `v-if` / `v-else-if` / `v-else`、`v-show` | 控制节点是否渲染或显示 |
| 列表渲染 | `v-for` | 遍历数组/对象/数字生成列表 |
| 绑定与事件 | `v-bind` / `:`、`v-on` / `@`、`v-model` | 绑定属性、监听事件、双向绑定 |
| 性能与转义 | `v-html`、`v-text`、`v-once`、`v-memo`、`v-pre`、`v-cloak` | 原始 HTML 渲染、节点缓存、跳过编译、隐藏未编译模板 |

> [!note] 关键心智模型
> **编译期做静态工作，运行期只做必要的动态工作**：能提前确定的内容（静态节点、不变的事件处理函数）在编译阶段处理掉，运行时只对带动态绑定的节点做定向 diff。理解这一点，才能判断「为什么 `v-memo` 有效」「为什么 `v-if` 比 `v-show` 更省初始开销」。

## 三、核心机制

### 1. 编译期优化四件套

Vue3 编译器对模板做的主要优化：

- **静态提升（hoistStatic）**：把没有动态绑定的节点提升到渲染函数之外，只创建一次，避免每次重渲染都重新创建 VNode。
- **Block Tree**：以动态节点为锚点组织 VNode 区块，把 diff 范围收敛到动态子树。
- **补丁标记（PatchFlags）**：给每个节点标注可跳过的 diff 类型，运行时按标记做定向更新，避免无谓的整棵子树对比。
- **事件监听缓存**：缓存事件处理函数，避免每次渲染产生新的函数引用而触发子组件更新。

3.5 起编译器输出**自动生成 TrustedHTML**，让模板输出在严格 CSP 环境下仍能安全工作，减少手动转义成本。

### 2. 条件与列表指令的机制差异

- **`v-if`**：真正的**条件渲染**，为 `false` 时节点从渲染树中**不存在**，切换有创建/销毁开销，适合「很少切换」的场景。
- **`v-show`**：始终渲染，仅通过 CSS `display` 控制可见，切换开销小，适合「频繁切换」。
- **`v-for`**：基于源码顺序生成列表；**`v-if` 与 `v-for` 同层时，`v-if` 优先级在 Vue3 中低于 `v-for`**，且无法访问 `v-for` 变量，应改用计算属性预先过滤，或调整书写顺序。

### 3. `v-model` 的演进

3.4 起 `v-model` 支持**参数与多模型**，一个组件可同时双向绑定多个状态；3.5 修复了修饰符组合的行为问题。其本质仍是 `:value` + `@input` 的语法糖，只是编译器做了统一封装。

### 4. `v-memo`

`v-memo` 缓存列表项子树，仅当依赖变化时才重新渲染该子树，是长列表更新的常用优化。**注意 Vapor Mode 目前不支持 `v-memo`**，在 Vapor 组件中使用会失效。

### 5. 自定义指令的两种接口

**VDOM 接口**（稳定线写法）：

```typescript
export interface Directive<EL, V = any> {
  // 生命周期钩子，el 为绑定元素
  mounted?(el: EL, binding: DirectiveBinding<V>, vnode: VNode)
  updated?(el: EL, binding: DirectiveBinding<V>, vnode: VNode, prevVNode: VNode)
  unmounted?(el: EL, binding: DirectiveBinding<V>, vnode: VNode)
}
```

**Vapor 接口**（3.6 RC，接口不同）：

```typescript
// value 是响应式 getter，可用 watchEffect 建立响应式效果，返回清理函数
type VaporDirective = (
  node: Node,
  value?: () => any,
  argument?: any,
  modifiers?: any
) => (() => void) | void
```

Vapor 中 `value` 为响应式 getter，适合用 `watchEffect` 建立响应式逻辑，并在卸载时自动释放副作用。

## 四、实践步骤（含代码/命令示例）

**1. 环境准备**：核对 Node 版本后创建项目。

```bash
node -v          # Vue 官方快速上手要求 Node ^22.18.0 || >=24.12.0
npm create vue@latest
npm install
npm run dev      # 默认 http://localhost:5173
```

**2. 自定义指令（VDOM 写法）**：以自动聚焦与高亮为例。

```vue
<script setup lang="ts">
// v-focus：元素挂载后自动聚焦
const vFocus = {
  mounted(el: HTMLElement) {
    el.focus()
  },
}

// v-highlight：按传入颜色设置背景，卸载时无需手动清理
const vHighlight = {
  mounted(el: HTMLElement, binding: { value: string }) {
    el.style.background = binding.value
  },
}
</script>

<template>
  <input v-focus v-highlight="'#fff3cd'" />
</template>
```

**3. `v-memo` 优化长列表**：

```vue
<script setup lang="ts">
import { ref } from 'vue'
const list = ref(Array.from({ length: 500 }, (_, i) => `第 ${i + 1} 项`))
</script>

<template>
  <div v-for="(item, index) in list" :key="item">
    <!-- 仅当 item 或 index 变化时才重渲染该子树 -->
    <span v-memo="[item, index]">{{ item }}</span>
  </div>
</template>
```

**4. 多模型 `v-model`**：

```vue
<script setup lang="ts">
defineProps<{ title: string; content: string }>()
defineEmits<{ (e: 'update:title', v: string): void; (e: 'update:content', v: string): void }>()
</script>

<template>
  <!-- 3.4+ 支持多个 v-model，组件内部用 props / emit 实现 -->
  <input v-model:title="title" v-model:content="content" />
</template>
```

**5. Vapor 自定义指令**：`value` 为响应式 getter。

```vue
<script setup vapor>
import { watchEffect } from 'vue'

const vAutoSize = (node: HTMLElement, value?: () => string) => {
  const stop = watchEffect(() => {
    const size = value?.()
    if (size) node.dataset.size = size
  })
  return stop // 返回清理函数，卸载时自动释放
}
</script>

<template>
  <div v-auto-size="() => width"></div>
</template>
```

## 五、最佳实践与常见坑

- **`v-if` 与 `v-show` 按切换频率取舍**：少切换用 `v-if`（省初始开销），频繁切换用 `v-show`（省创建/销毁）。
- **`v-for` 必须给稳定的 `key`**：优先用业务唯一值，**不要用数组索引做动态列表的 key**，否则会导致状态错位与多余更新。
- **避免 `v-if` 与 `v-for` 同层**：改用 `computed` 预先过滤列表，语义更清晰、性能更好。
- **`v-memo` 仅用于 VDOM**：Vapor Mode 不支持 `v-memo`；同时注意依赖数组要完整，漏写依赖会导致缓存不更新。
- **慎用 `v-html`**：它会把内容按原始 HTML 插入，是 XSS 的常见入口；用户输入必须先转义或消毒，优先用默认转义的插值 `{{ }}`。
- **`v-pre` 与 `v-cloak` 的适用场景**：需要原样输出大段非 Vue 语法（如代码示例、`{{ }}` 字面量）时用 `v-pre` 跳过编译；用于隐藏尚未编译完成的模板、避免首屏闪烁时用 `v-cloak` 配合 CSS `[v-cloak]{display:none}`。
- **Vapor 事件委托的坑**：祖先调用 `stopPropagation()` 会让委托到 `document` 的处理函数不执行；需要绕过委托时用 `@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"` 直接绑定元素。
- **Vapor 中 `slots.default()` 不是无副作用试运行**：调用会真实执行渲染逻辑（创建 Block、注册响应式 effect、在 hydration 时占用 SSR DOM），不要把渲染逻辑写进「探测」分支，应交由模板 `<slot />` 渲染。
- **自定义指令要写清理逻辑**：VDOM 用 `unmounted`，Vapor 返回清理函数；否则在长会话应用中会积累副作用造成内存泄漏。

> [!warning] 迁移到 Vapor 前先盘点
> 存量组件里凡是依赖 `v-memo`、模板 ref 的 `$el`、`app.config.globalProperties`、`@vue:xxx` 元素级生命周期事件的写法，在 Vapor 中都不支持或行为不同。建议先按模块灰度，确认依赖生态已适配后再扩大范围。

## 六、核心要点速查

1. Vue 最新稳定版 **3.5.45（2026-11-05）**，**3.6.0-rc.1** 处于 RC，Vapor 功能已完成但**未进入稳定版**。
2. 模板编译优化四件套：**静态提升、Block Tree、PatchFlags、事件监听缓存**；3.5 编译器输出** TrustedHTML**，利于严格 CSP。
3. **`v-if`** 控制渲染、**`v-show`** 控制显示；按切换频率取舍。
4. **`v-for`** 必须配**稳定唯一 `key`**，不要用索引做动态列表 key；`v-if` 与 `v-for` 不要同层。
5. **`v-model`** 3.4 起支持**参数与多模型**（`v-model:title`），本质是 `:value` + `@input` 的语法糖。
6. **`v-memo`** 缓存长列表子树，**Vapor Mode 不支持**。
7. 内置指令：`v-if/v-else-if/v-else`、`v-for`、`v-bind/:`、`v-on/@`、`v-model`、`v-show`、`v-html`、`v-text`、`v-once`、`v-memo`、`v-pre`、`v-cloak`。
8. 自定义指令：**VDOM** 用 `mounted/updated/unmounted` 生命周期对象；**Vapor** 用 `(node, value?, argument?, modifiers?)` 且 `value` 是响应式 getter，返回清理函数。
9. **Vapor 事件委托**：祖先 `stopPropagation()` 会拦截委托；`@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"` 可绕过。
10. **`v-html` 需转义/消毒**，用户输入避免直接插入，防 XSS。

## 七、学习资源

- [Vue 官方中文文档 · 模板语法](https://cn.vuejs.org/guide/template-syntax.html)
- [Vue 官方中文文档 · 自定义指令](https://cn.vuejs.org/guide/reusability/custom-directives.html)
- [Vue 官方中文文档 · 性能优化（编译与渲染）](https://cn.vuejs.org/guide/best-practices/performance.html)
- [vuejs/core CHANGELOG](https://github.com/vuejs/core/blob/main/CHANGELOG.md)
- [Vue 3.6.0-rc.1 发布说明（Vapor Mode / alien-signals）](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)
- [npm vue dist-tags（latest / rc / beta / alpha）](https://registry.npmjs.org/-/package/vue/dist-tags)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题总览，模板与指令是其中进阶篇的展开
- [[前端开发]] — 前端技术整体地图与目录索引
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
