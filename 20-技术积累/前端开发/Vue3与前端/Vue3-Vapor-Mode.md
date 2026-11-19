---
title: Vue3-Vapor-Mode
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - Vapor-Mode
  - 编译优化
  - 性能优化
aliases:
  - Vue3 Vapor Mode
  - Vapor 模式
source:
  - 网络资料整理
---

# Vue3-Vapor-Mode

> [!summary] 摘要
> **Vue3 Vapor Mode** 是 Vue 单文件组件（SFC）的**全新编译模式**：在编译期把模板直接转换为命令式 DOM 操作，**跳过虚拟 DOM（VDOM）diff**，目标是**降低基线包体积、提升渲染与更新性能**。它是 **100% opt-in（完全可选）** 的特性，随 **Vue 3.6 RC** 功能完成，截至 2026-11 仍处 **RC 阶段、未进入稳定版**，官方建议仅用于**性能敏感页面的局部实现**或**小型新应用**。本文给出 Vapor 的定位、编译机制、启用方式、可运行示例与高频坑位，供 [[Vue3与前端-从入门到精通]] 体系下的深入查阅。

## 一、最新动态（截至 2026-11）

- **Vue 进入「双轨」时代**：稳定线仍是 **Vue 3.5.45**（2026-11-05 发布）；**Vue 3.6** 已进入 RC（调研文件记载其功能完成里程碑为 **`3.6.0-rc.1`，2026-07-17**），核心变化正是 **Vapor Mode 功能完成** 与 **基于 alien-signals 的响应式系统大重构**。RC 版本号会持续迭代，最新 RC 号以官方仓库为准。
- **Vapor 仍非稳定版**：Vapor 与 VDOM 可共存，但属于 100% 可选的新编译模式；**截至 2026-11 仍未进入稳定版**，官方建议仅在**性能敏感页面局部使用**或**小型新应用整体使用**，不建议生产大规模采用。
- **性能声明**：官方称第三方基准中 Vapor 达到与 **Solid / Svelte 5 同级**的性能。
- **元框架接入**：**Nuxt 4.6.0**（2026-10-05）以 **interop 模式**支持 Vue Vapor——根保持 VDOM，组件/页面用 `<script setup vapor>` 单独开启，要求 **Vue `^3.6.0-rc.2` 或更高**。
- **生态背景**：与 Vapor 同期，Vue 生态集体升主版本（Vue Router 5、Pinia 4、Vite 8、Vitest 5）。Vapor 的收益（去掉 VDOM 运行时）与 Vite 8 / Rolldown 的构建提速是两条并行的优化主线。

> [!warning] 版本口径
> 上述版本号与日期均来自调研基线（截至 2026-11）。Vapor 处于 RC 阶段，正式版发布时间与细节**以官方仓库/官方文档为准**，生产项目当前应锁定 Vue 3.5.x 稳定版。

## 二、基础概念

**Vapor Mode 是什么。** 传统 Vue SFC 编译后生成渲染函数，运行时把 VNode 组织成 Block Tree，用 PatchFlags 缩小 diff 范围，再通过 `patch` 更新真实 DOM。Vapor 改变了这条路径：编译器直接生成**针对真实 DOM 的命令式操作**，**不再构建 VNode、不再做 VDOM diff**，从源头省掉 diff 开销与 VDOM 运行时，从而降低基线包体积。

**关键心智模型：**

- **编译期优化**：模板 → 直接 DOM 操作，跳过 VDOM diff；性能来自「少一层抽象」而非「更快的 diff」。
- **100% opt-in**：Vapor 不是默认模式，只有显式声明的组件才走 Vapor 编译，其余组件仍走 VDOM，二者可共存。
- **组合式 API 是唯一选择**：**Vapor 不支持 Options API**，只能使用 `<script setup>` 风格。
- **与 VDOM 互操作**：可在 VDOM 应用中混用 Vapor 组件（需插件），也可在 Vapor 应用中混用 VDOM 组件（但会引入 VDOM 运行时，抵消包体积收益）。

**三种启用写法：**

- `<script setup vapor>`：在组合式脚本块上声明，最常用；
- `<script vapor>`：等价于 `<script setup vapor>`；
- `<template vapor>`：对整个 SFC 启用 Vapor 编译。

## 三、核心机制

**1. 编译期 DOM 操作，跳过 diff。** Vapor 编译器把模板静态结构与动态绑定拆解为一系列对真实节点的创建、插入、属性/事件设置与更新指令。因为没有 VNode，也就没有 `patch`、PatchFlags 与 Block Tree 这一层运行时开销；组件更新通过**细粒度响应式**精确定位需要改动的 DOM 节点。

**2. 基于 alien-signals 的响应式换芯。** Vue 3.6 对 `@vue/reactivity` 做了基于 **alien-signals** 的重大重构，这是 Vapor 性能与内存改善的底层支撑，也是 3.6 的主要技术变化之一。Vapor 组件的依赖追踪更细粒度，更新只触发真正受影响的节点。

**3. 事件委托（Vapor 特有）。** Vapor 会把符合条件的事件**委托到 `document`**。这带来一个行为差异：**若某个祖先调用了 `stopPropagation()`，委托处理函数不会触发**。绕过委托、直接绑定元素的方式有 `@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"`。

**4. 自定义指令接口不同。** VDOM 中指令接口为 `{ mounted, updated, unmounted, ... }`；**Vapor 中接口为**：

```typescript
type VaporDirective = (
  node: Node,
  value?: () => any,
  argument?: unknown,
  modifiers?: Record<string, boolean>
) => (() => void) | void
```

`value` 是**响应式 getter**，可用 `watchEffect` 建立响应式效果，并可返回清理函数（卸载时自动释放）。

**5. 插槽行为差异。** Vapor 中 **`slots.default()` 不是无副作用的「试运行」**：调用会**真实执行渲染逻辑**（创建 Block、注册响应式 effect、在 hydration 时占用 SSR DOM）。因此不要用它「探测」输出来决定是否渲染 fallback，应交由模板 `<slot />` 渲染。

**6. 不支持 / 不适用清单。** Vapor 不支持：**Options API**、`app.config.globalProperties`、`@vue:xxx` 元素级生命周期事件、`v-memo`；`getCurrentInstance()` 返回 **`null`**；组件模板 ref 不暴露 `$el` / `$props` / `$attrs` / `$slots` / `$refs`。

**7. 互操作机制。** 纯 Vapor 应用用 `createVaporApp()`，避免引入 VDOM 运行时；在 VDOM `createApp()` 中混用 Vapor 组件需安装 `vaporInteropPlugin`；反之 Vapor 应用用 VDOM 组件同样需要该插件，但会引入 VDOM 运行时。官方建议**分区使用，避免深层混合嵌套**。

## 四、实践步骤（含代码/命令示例）

**1. 安装 Vue 3.6 RC（Vapor 的前置条件）。**

```bash
# 安装 Vue 3.6 RC（Vapor Mode 随 3.6 提供）
npm install vue@3.6.0-rc.1
# 确认实际安装版本
npm ls vue
```

> [!info] 版本提示
> 具体 RC 版本号以安装时 npm 的 `rc` 标签为准；若仓库中 RC 已迭代，请替换为最新可用 RC，避免直接写死过期版本。

**2. 创建纯 Vapor 应用（推荐用于新小应用）。**

```typescript
// main.ts
import { createVaporApp } from 'vue'
import App from './App.vue'

// 纯 Vapor 应用：不引入 VDOM 运行时，基线包体积显著下降
createVaporApp(App).mount('#app')
```

```vue
<!-- App.vue -->
<script setup vapor>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <button @click="count++">点击次数：{{ count }}</button>
</template>
```

**3. 在 VDOM 应用中局部混用 Vapor 组件。**

```typescript
// main.ts（VDOM 应用，混用 Vapor 组件）
import { createApp, vaporInteropPlugin } from 'vue'
import App from './App.vue'

createApp(App).use(vaporInteropPlugin).mount('#app')
```

```vue
<!-- 局部性能敏感组件：仅此组件走 Vapor 编译 -->
<script setup vapor>
import { ref, computed } from 'vue'

const keyword = ref('')
const items = ref(['Vue3 Vapor', 'alien-signals', 'Rolldown'])

const filtered = computed(() =>
  items.value.filter((t) => t.toLowerCase().includes(keyword.value.toLowerCase()))
)
</script>

<template>
  <input v-model="keyword" placeholder="过滤列表" />
  <ul>
    <li v-for="item in filtered" :key="item">{{ item }}</li>
  </ul>
</template>
```

**4. 在 Nuxt 4.6 中开启 Vapor（interop 模式）。**

```yaml
// nuxt.config.ts（示意：Nuxt 4.6 以 interop 模式支持 Vapor）
export default defineNuxtConfig({
  compatibilityDate: '2026-11-19',
  // 根保持 VDOM；在组件/页面中单独使用 <script setup vapor> 开启
})
```

```vue
<!-- pages/counter.vue（Nuxt 页面，单独开启 Vapor） -->
<script setup vapor>
const count = ref(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

> [!note] 混用边界
> `vaporInteropPlugin` 的导入路径与导出名请以所安装 Vue 3.6 RC 的官方包为准；官方建议**按模块分区**，避免 Vapor 与 VDOM 组件在深层嵌套中互相包裹。

## 五、最佳实践与常见坑

**推荐做法：**

1. **小应用整体 Vapor、大应用局部 Vapor**：新小项目可用 `createVaporApp()` 享受完整收益；存量大项目只挑性能敏感页面/组件用 `<script setup vapor>` 灰度。
2. **优先组合式 API**：Vapor 不支持 Options API，用 `<script setup>` + composables 组织逻辑。
3. **避免深层混合嵌套**：Vapor 与 VDOM 组件分区使用，减少互操作插件的运行时开销。
4. **用构建产物验证收益**：用 Vite/Rolldown 的构建分析对比启用前后的基线包体积，避免「感觉更快」但没有数据支撑。

**常见坑：**

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 事件不触发 / 被 `stopPropagation()` 影响 | Vapor 事件委托到 `document` | 用 `@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"` 绕过委托 |
| `slots.default()` 执行后组件异常或 SSR 水合不一致 | 它不是试运行，会真实渲染并占 DOM | 改用模板 `<slot />`，不要在脚本中探测输出 |
| `getCurrentInstance()` 返回 `null` | Vapor 不支持该 API | 改用 `inject` / `provide` 或组合式函数传参 |
| 自定义指令不生效或清理时机不对 | Vapor 指令接口与 VDOM 不同 | 使用 `(node, value?, argument?, modifiers?)` 签名，`value` 用 `watchEffect` |
| 使用 `v-memo` 无效 | Vapor 暂不支持 `v-memo` | 改用稳定的 `key` 或拆分组件 |
| Options API / `app.config.globalProperties` 失效 | Vapor 不支持 | 迁移到 `<script setup>`，改用其他扩展点 |
| 模板 ref 取不到 `$el` / `$props` / `$attrs` | Vapor 不暴露这些实例属性 | 通过 `useTemplateRef()` 等组合式方式获取引用 |

## 六、核心要点速查

1. **定位**：Vapor 是 Vue SFC 的**新编译模式**，编译期直接操作 DOM、**跳过 VDOM diff**，降低基线包体积、提升性能。
2. **状态**：随 **Vue 3.6 RC** 功能完成（里程碑 `3.6.0-rc.1`，2026-07-17），**截至 2026-11 仍处 RC、非稳定版**。
3. **响应式底座**：Vue 3.6 `@vue/reactivity` 基于 **alien-signals** 重构，是 Vapor 性能的底层支撑。
4. **启用**：`<script setup vapor>`、`<script vapor>`、`<template vapor>` 三选一，**100% opt-in**。
5. **纯 Vapor 入口**：`createVaporApp(App)`，不引入 VDOM 运行时。
6. **互操作**：`createApp()` 混用 Vapor 组件需 `vaporInteropPlugin`；建议分区使用。
7. **不支持**：Options API、`v-memo`、`app.config.globalProperties`、`@vue:xxx` 元素级生命周期、模板 ref 的 `$el`/`$props`/`$attrs`/`$slots`/`$refs`；`getCurrentInstance()` 返回 `null`。
8. **事件委托**：合格事件委托到 `document`，祖先 `stopPropagation()` 会使委托处理不触发，可用 `@[event]` 等绕过。
9. **插槽**：`slots.default()` 会真实渲染，不是试运行。
10. **指令**：Vapor 指令接口为 `(node, value?, argument?, modifiers?) => (() => void) | void`，`value` 为响应式 getter。
11. **性能**：官方称第三方基准中 Vapor 与 **Solid / Svelte 5** 同级。
12. **落地**：小应用整体用、大应用局部灰度，生产仍锁定 Vue 3.5.x 稳定版。

## 七、学习资源

**官方与版本源**

- [Vue 3.6.0-rc.1 发布说明（Vapor Mode / alien-signals）](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)
- [Vue 核心仓库 CHANGELOG（vuejs/core）](https://github.com/vuejs/core/blob/main/CHANGELOG.md)
- [npm vue dist-tags（latest / rc / beta / alpha）](https://registry.npmjs.org/-/package/vue/dist-tags)
- [Vue 官方文档](https://cn.vuejs.org/)

**元框架接入**

- [Nuxt 官方博客 · Nuxt 4.6（含 Vue Vapor interop 支持）](https://nuxt.com/blog/v4-6)

**构建与性能**

- [Vite 官方博客 · Vite 8：由 Rolldown 驱动](https://cn.vite.dev/blog/announcing-vite8)
- [Vue 3 性能优化（编译与渲染优化要点）](https://developer.aliyun.com/article/1686132)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题的总览与知识地图，定位与选型提醒见其中「生态与前沿」章节
- [[前端开发]] — 前端技术整体地图与目录索引
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
