---
title: 前端与 Vue3 调研
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端
  - Vue3
  - 调研
  - 版本跟踪
---

# 前端与 Vue3 调研

> 调研范围：18 个「前端与 Vue3」方向知识点的**最新官方支持与关键事实**，截至 2026 年 11 月。
> 全部版本号、发布日期、API 变化均来自官方文档 / 官方仓库 / npm / MDN，来源 URL 见各节。
> 用途：供后续写作 18 篇详细文档引用，写作前请以本文为基线，引用时核对官方原文。

## 一、主题最新动态（截至 2026-11）

- **Vue 进入「双轨」时代**：稳定线仍是 **Vue 3.5.45**（2026-11-05 发布）；同时 **Vue 3.6 已进入 RC**（`3.6.0-rc.1`，2026-07-17），其核心是 **Vapor Mode 功能完成** 与 **基于 alien-signals 的响应式系统大重构**。Vapor 与 VDOM 可共存，但属于「100% 可选」的新编译模式，**截至 2026-11 仍未进入稳定版**，官方建议仅用于性能敏感页面的局部使用或小型新应用。
- **Vue 生态集体升主版本**：Vue Router 4 → **5**（过渡版，合并文件路由）、Pinia 2/3 → **4**（ESM-only）、Vite 7 → **8**（Rolldown 统一打包）、Nuxt 4.5 → **4.6**（服务端无关化）。学习 Vue3 需同时掌握「4 时代」的写法与「5 时代」的新入口。
- **构建工具 Rust 化收敛**：Vite 8 用 Rolldown（Rust）取代 esbuild + Rollup 双打包器，配合 Oxc（解析/转译/压缩）与 Lightning CSS，官方称构建提速 **10–30×**，插件兼容 Rollup 的 API。
- **SSR 框架服务端无关化**：Nuxt 4.6 引入 `nuxt/server` 自有导入面与可移植 `RequestEvent`，默认仍由 Nitro 驱动，同时实验性提供 `@nuxt/vite-server`（纯 Vite 构建），为 Nuxt 5 / Nitro v3 铺路；**Nuxt 3 已于 2026-07-31 停止支持（EOL）**。
- **测试体系更现代**：Vitest 发布 **5.0**（性能为主，2026-09-03），要求 Vite ≥ 6.4.0、Node ≥ 22.12.0；Playwright 到 **1.65.1**（2026-11-09），新增 Bun 运行、Python 定位代码等。
- **TypeScript 原生化**：**TypeScript 7.0（Go 原生移植）于 2026-07-08 GA**，官方称比上一代快约 10×，但**不再提供 JS 端编译器 API**；5.x 最新为 **5.9.3**。与 Vue 集成时，Volar / vue-tsc 路线在 TS 7 下需关注兼容性。

## 二、版本与关键事实表

| 项目 | 最新稳定版本 | 发布日期 | 关键变化 | 官方来源 URL |
|------|------------|----------|---------|------------|
| Vue.js (vue) | **3.5.45** | 2026-11-05 | 3.5 系列最新补丁；3.5 首发于 2024-09-03，重构响应式、新增 `onEffectCleanup`、`useId`、`useTemplateRef`、`onUnmount`、Deferred Teleport 等 | https://vuejs.org/about/releases |
| Vue.js (vue) 预发布 | **3.6.0-rc.1** | 2026-07-17 | Vapor Mode 功能完成；`@vue/reactivity` 基于 alien-signals 重构，性能与内存显著改善 | https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1 |
| Vue Router | **5.0.4** | 约 2026-03-19（5.0.0 于 2026-01-29） | 过渡版本，把 `unplugin-vue-router` 文件路由并入核心；对纯 Router 4 用户无破坏性变更；5.0 起 data loaders 为实验特性 | https://router.vuejs.org/guide/migration/v4-to-v5.html |
| Pinia | **4.0.3** | 4.0.0 于 2026-07-14；4.0.3 于 2026-08-12 | 仅技术性破坏：**ESM-only**；需**手动安装 `@vue/devtools-api` v8**；用 Nostics 重写错误与开发警告 | https://github.com/vuejs/pinia/releases/tag/v4.0.0 |
| Vite | **8.0** | 2026-03-12 | Rolldown 单一打包器（10–30× 构建提速），插件兼容 Rollup；Node **20.19+ / 22.12+**，ESM-only；内置 Devtools、`resolve.tsconfigPaths`、`emitDecoratorMetadata`、wasm SSR、控制台转发 | https://vite.dev/blog/announcing-vite8.html |
| Nuxt | **4.6.0** | 2026-10-05 | `nuxt/server` 服务端无关、`appSecret` 与 sessions、基于 fetchdts 的 typed `$fetch`、**Vue Vapor 支持**、Nuxt CLI v4；要求 Node `^22.22.3 \|\| ^24.15.0 \|\| >=26.0.0`；Nuxt 3 EOL 2026-07-31 | https://nuxt.com/blog/v4-6 |
| Vitest | **5.1**（5.0 于 2026-09-03） | 5.1 于 2026-11-01 | 以性能为主；内联 project 共享 Vite server、`fsModuleCache` 稳定、Browser Mode Trace View、`vi.when`、benchmark API 重写、`clearMocks` 默认开启；要求 Vite ≥ 6.4.0、Node ≥ 22.12.0 | https://vitest.dev/blog/vitest-5.html |
| Playwright | **1.65.1** | 2026-11-09 | 支持 Bun 运行（`--bun`）；Chromium 159.0.8154.6 / Firefox 159.0 / WebKit 27.2；inert 属性等待、Cookie 匹配遵循 RFC 6265 | https://github.com/microsoft/playwright/releases |
| TypeScript | **7.0.2**（5.x 最新 5.9.3） | TS 7.0 于 2026-07-08 GA | Go 原生移植，官方称约 10× 提速；**不提供 JS 编译器 API**（`ts.createProgram` 等）；移除 TS 6 全部弃用项；5.9 支持 `import defer` | https://devblogs.microsoft.com/typescript/announcing-typescript-5-9/ |
| Vue Devtools API | **v8** | 随 Vue Router 5 / Pinia 4 升级 | 从 `@vue/devtools-api` 升级，需在依赖中显式安装（影响 Router 5 的 iife 构建、Pinia 4） | https://github.com/vuejs/pinia/releases/tag/v4.0.0 |

> 说明：上表发布日期取自官方发布说明 / npm / 仓库标签；部分补丁版本日期以 changelog 为准，写作时请回源核对。

## 三、分知识点关键事实

### 1. Vue3 响应式系统原理

- **3.5 重构（当前稳定基线）**：响应式核心改用 **version counting（版本计数）+ doubly-linked list tracking（双向链表跟踪）** 重写追踪结构，并优化数组追踪；官方称内存占用与深度数组更新性能显著改善（社区资料提及内存最高下降约 56%）。
- **3.6 再重构**：`@vue/reactivity` 基于 **alien-signals** 大幅重构，进一步提升性能与内存占用，是 3.6 的主要技术变化之一。
- **核心 API 稳定**：`reactive` / `ref` / `computed` / `watch` / `effect` / `effectScope` 仍是基座；3.5 起新增：
  - `onEffectCleanup`（效果清理回调）；
  - `watch` 暂停 / 恢复：`ReactiveEffect`、`EffectScope`、`WatchHandle` 支持 pause/resume；
  - `getCurrentWatcher`、`onWatcherCleanup`；
  - `onScopeDispose` 新增 `failSilently` 参数；
  - `watch` 的 `deep` 支持传数字控制深度。
- **关键内部机制**：依赖收集（`track`）与触发（`trigger`）、`Proxy` 拦截（reactive）、`ref` 的 `.value` 解包、批量更新（nextTick 合并）。
- 来源：https://vuejs.org/about/releases ；https://github.com/vuejs/core/blob/minor/CHANGELOG.md ；https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1

### 2. Vue3 组合式 API（Composition API）详解

- **状态**：自 Vue 3.0 起稳定；`<script setup>` 是官方推荐的编写风格。3.5 起 **reactive props 解构默认开启**（`reactive props destructure`）。
- **生命周期**：`onMounted` / `onUpdated` / `onUnmounted` 等；3.5 新增 **`app.onUnmount()`**（应用级卸载回调）。
- **模板引用**：3.5 新增 **`useTemplateRef()`**，用于获取模板 ref。
- **副作用与清理**：`watchEffect`、`watch`、`onEffectCleanup`、`onWatcherCleanup`、`getCurrentWatcher`；`watch` 支持暂停 / 恢复。
- **依赖注入**：`provide` / `inject`；**`getCurrentInstance()` 在 Vapor 组件中返回 `null`**，属重要差异。
- **与 Options API 关系**：长期并存；但 **Vapor Mode 不支持 Options API**，组合式 API 是 Vapor 的唯一选择。
- 来源：https://vuejs.org/about/releases ；https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1

### 3. Vue3 模板与指令进阶

- **内置指令**：`v-if` / `v-else-if` / `v-else`、`v-for`、`v-bind` / `:`、`v-on` / `@`、`v-model`、`v-show`、`v-html`、`v-text`、`v-once`、`v-memo`、`v-pre`、`v-cloak`。
- **`v-memo`**：缓存子树，优化长列表更新；**注意 Vapor Mode 目前不支持 `v-memo`**。
- **`v-model` 演进**：3.4 引入 `v-model` 参数与多模型（`v-model:title`、`v-model:[dynamicArg]`）；3.5 修复 `.trim` 与 `.number` 组合的 `$el` 等行为。
- **自定义指令**：
  - VDOM 中接口为 `{ mounted, updated, unmounted, ... }`；
  - **Vapor 中接口不同**：`(node, value?: () => any, argument?, modifiers?) => (() => void) | void`，`value` 是响应式 getter，可用 `watchEffect` 建立响应式效果，可返回清理函数。
- **模板编译**：编译期做静态提升、补丁标记（patch flag）、事件缓存、`TrustedHTML`（3.5 编译器输出自动生成，利于严格 CSP）。
- **事件委托（Vapor 特有）**：Vapor 把符合条件的事件委托到 `document`；若祖先调用 `stopPropagation()`，委托处理函数不会触发；`@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"` 形式绕过委托。
- 来源：https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1 ；https://github.com/vuejs/core/blob/v3.5.45/CHANGELOG.md

### 4. Vue Router 4 详解

- **现状**：知识点名为「Router 4」，但当前最新为 **Vue Router 5**。Router 5 是**过渡版本**，把 `unplugin-vue-router` 的**基于文件的路由**合并进核心包。
- **对 Router 4 用户**：若未使用 `unplugin-vue-router`，**无破坏性变更**，`pnpm update vue-router@5` 即可。
- **Router 5 新入口 / 导出**：
  - `vue-router/vite`（Vite 插件，替代 `unplugin-vue-router/vite`）；
  - `vue-router/unplugin`（Webpack / Rollup / esbuild 及工具函数）；
  - `vue-router/auto-routes`（生成的路由）；
  - `vue-router/experimental`（data loaders，含 `pinia-colada` loader）；
  - `vue-router/volar/sfc-typed-router`、`vue-router/volar/sfc-route-blocks`（Volar 插件）。
- **实验特性**：**查询参数默认可选**（`experimental: Query params are optional by default`）、data loaders、路由 JSON schema、`definePage({ name })`。
- **面向未来**：**Vue Router 6 将是 ESM-only 并移除已弃用 API**，v5 为过渡准备期；iife 构建不再内置 `@vue/devtools-api`（升级到 v8，无 IIFE 构建）。
- **核心 API**：`createRouter` / `createWebHistory` / `createWebHashHistory`、路由守卫（`beforeEach` / `beforeEnter` / `beforeRouteUpdate`）、`useRoute` / `useRouter`、`<RouterLink>` / `<RouterView>`、`<Suspense>` + 异步组件。
- 来源：https://router.vuejs.org/guide/migration/v4-to-v5.html ；https://github.com/vuejs/router/releases

### 5. Pinia 状态管理详解

- **版本**：当前最新 **Pinia 4.0.3**（4.0.0 于 2026-07-14 发布）。**Vuex 已进入维护模式，新代码不应再使用**。
- **Pinia 4 的破坏性变更（仅技术性）**：
  - **ESM-only**（CJS 支持被移除）；
  - **必须手动安装 `@vue/devtools-api`（v8）**，以保持包体积小并降低供应链风险；
  - 用 **Nostics** 重写错误与开发警告，便于人与 AI 代理定位问题。
- **4.x 新特性**：`storeToRefs` 优雅跳过 nullish 值、无效属性诊断、插件中错误值诊断、导出 `piniaSymbol`、使用现代 `Object.hasOwn`。
- **核心 API**：`defineStore(id, options)` 或 `defineStore(id, setup)`、`state` / `getters` / `actions`、`storeToRefs`、`mapState` / `mapActions`、插件（持久化、订阅）、Devtools 集成、SSR 适配（hydration 时替换 reactive Set/Map 而非合并）。
- **体积**：官方称约 **1.5 KB**。
- 来源：https://github.com/vuejs/pinia/releases/tag/v4.0.0 ；https://pinia.vuejs.org/

### 6. Vite 构建工具原理与配置

- **版本**：**Vite 8.0**（2026-03-12）。这是自 Vite 2 以来最重要的架构变化。
- **核心架构**：**Rolldown 作为唯一、统一、基于 Rust 的打包器**，取代「esbuild（开发）+ Rollup（生产）」双打包器；配合 **Oxc**（转译 / 压缩）与 **Lightning CSS**（CSS 压缩）。官方称构建提速 **10–30×**，且保持对 Rollup 插件 API 的兼容，多数现有 Vite 插件可直接工作。
- **Node 要求**：**Node.js 20.19+、22.12+**（与 Vite 7 相同），保证默认支持 `require(esm)`，Vite 以 ESM-only 包分发。
- **Vite 8 新特性**：
  - `devtools` 选项启用 **Vite Devtools**；
  - `resolve.tsconfigPaths: true` 内置 **tsconfig paths 别名解析**（默认关闭，有性能成本）；
  - 内置 `emitDecoratorMetadata` 支持（无需外部插件）；
  - **wasm SSR**：`.wasm?init` 导入在 SSR 环境可用；
  - **浏览器控制台转发**：`server.forwardConsole`，检测到 coding agent 时自动开启；
  - **`@vitejs/plugin-react` v6**：用 Oxc 做 React Refresh 转译，移除 Babel 依赖；提供 `reactCompilerPreset`。
- **安装体积**：Vite 8 比 Vite 7 大约 **15 MB**（lightningcss ~10 MB + Rolldown ~5 MB）。
- **迁移**：内置兼容层自动把 `esbuild` / `rollupOptions` 配置转换为 Rolldown / Oxc 等价物，多数项目无需改配置；官方建议大项目先切 `rolldown-vite`（Vite 7 上）再升级 Vite 8。
- **前瞻**：Full Bundle Mode（实验，dev 启动快 3×、整页重载快 40%、网络请求少 10×）、Raw AST 传输、原生 MagicString 变换、Environment API 稳定化；插件目录 **registry.vite.dev**。
- 来源：https://vite.dev/blog/announcing-vite8.html ；https://cn.vitejs.dev/blog/announcing-vite8

### 7. Vue3 组件设计模式

- **组件通信**：`props` 下行、`emits` 上行、`provide` / `inject` 跨层级、`expose` 暴露实例、`v-model` 双向绑定（支持多模型与参数）。
- **插槽（Slots）**：默认插槽、具名插槽、作用域插槽；**Vapor 中 `slots.default()` 不是无副作用的「试运行」**，调用会真实执行渲染逻辑（创建 Block、注册响应式 effect、在 hydration 时占用 SSR DOM），应交由模板 `<slot />` 渲染。
- **组合式函数（Composables）**：自定义可复用逻辑单元，配合 `getCurrentInstance`（Vapor 中返回 `null`）与依赖注入。
- **容器型组件**：`<Teleport>`（3.5 新增 **Deferred Teleport**，可延迟挂载点、支持放入 `<Transition>`）、`<Suspense>`（异步依赖 + 嵌套 Suspense）、`<KeepAlive>`（3.5.45 修复克隆 vnode 的 pruned 组件卸载）。
- **自定义元素**：3.5 扩展 `defineCustomElement()`，新增 `useHost()`、`useShadowRoot()` 便于访问宿主与 shadow root。
- **混入与高阶组件**：Options API 的 `mixins` 不推荐用于新代码；高阶组件可用组合式函数替代。
- **设计模式清单**：受控/非受控、容器/展示、组合优于继承、无头（headless）组件、原子/分子/组织分层。
- 来源：https://vuejs.org/about/releases ；https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1

### 8. Vue3 性能优化实践

- **框架侧**：
  - **3.5 响应式重构**（版本计数 + 双向链表 + 数组追踪优化）带来内存与更新性能提升；
  - **3.6 alien-signals 重构**进一步优化；
  - **Vapor Mode**：减少基线包体积，第三方基准显示与 Solid / Svelte 5 同级性能；
  - **懒 hydration（lazy hydration）**、`data-allow-mismatch`（SSR）、`useId()` 优化 SSR DOM 一致性。
- **模板侧**：`v-memo` 缓存长列表子树（Vapor 不支持）；避免不必要的 `v-if` + `v-for` 同层；静态内容用 `v-once` / `v-pre`。
- **状态侧**：`shallowRef` / `shallowReactive` 跳过深层代理；`markRaw` 避免对象被响应式化；`toRefs` 精确依赖；按需使用 `computed`。
- **渲染侧**：合理的 `key`；组件异步化 + `<Suspense>` 拆包；`<KeepAlive>` 缓存；避免大组件无谓重渲染。
- **构建侧**：借助 Vite 8 / Rolldown 的代码分割、Tree Shaking、模块级持久缓存；压缩与资源提示（preload / preconnect / prefetch）。
- **度量**：关注 **Core Web Vitals**（LCP / INP / CLS，见第 15 点）。
- 来源：https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1 ；https://vite.dev/blog/announcing-vite8.html

### 9. Vue3 服务端渲染与 Nuxt

- **SSR 基础**：Vue 官方提供 `@vue/server-renderer`，`createSSRApp` + `renderToString` / `renderToNodeStream`；hydration 需保证服务端/客户端 DOM 一致，可用 `useId()`、`app.config.idPrefix` 管理 ID，`data-allow-mismatch` 容忍部分不一致。
- **Nuxt 版本**：**Nuxt 4.6.0**（2026-10-05），**Nuxt 3 已于 2026-07-31 EOL**，无 3.x 同步版本。
- **Nuxt 4.6 关键能力**：
  - **`nuxt/server`**：新的服务端导入面，提供 `defineEventHandler`、`getQuery`、`readValidatedBody`、session 等；类型面向**可移植 `RequestEvent`**（`event.req` / `event.url` / `event.res` / `event.context`），默认仍由 Nitro + h3 实现，代码不再直接依赖 h3 / nitropack；
  - **`@nuxt/vite-server`**（实验）：纯 Vite + Vite Environment API 构建服务端，可产出 SPA / SSR / Web 标准 fetch handler / 全静态输出；**默认仍是 Nitro**；
  - **`appSecret` 与 sessions**：`runtimeConfig.appSecret`（`NUXT_APP_SECRET`）为根密钥，`deriveSecret(purpose)` 派生；session 用 **iron** 封存到 cookie，无需服务端存储；
  - **typed `$fetch` / `useFetch`**：基于 **fetchdts** 重建，解决路由多时 **TS2589 实例化过深**，类型成本随调用点而非路由数增长（3000 路由场景实例化从 71,875,148 降至 101,678，峰值内存 946 MB → 140 MB）；
  - **Vue Vapor 支持**：interop 模式，根保持 VDOM，组件/页面用 `<script setup vapor>` 开启，要求 **Vue `^3.6.0-rc.2` 或更高**；
  - **Nuxt 5 特性提前可用**：`future.compatibilityVersion: 5` 一键开启（typed pages、typed $fetch、大小写敏感路由等）；
  - 性能：`@nuxt/kit` 安装体积 6.4 MB → 2.1 MB（-67%），构建提速约 11–18%，300 个 `<NuxtLink>` 的 SSR 吞吐 110 → 140 req/s（+26%）；
  - Node 要求：**`^22.22.3 || ^24.15.0 || >=26.0.0`**。
- 来源：https://nuxt.com/blog/v4-6

### 10. Vue3 Vapor Mode

- **定位**：Vue SFC 的**新编译模式**，目标是**降低基线包体积并提升性能**；**100% opt-in**（完全可选）。
- **状态**：**Vue 3.6 RC 中 Vapor 功能已完成（feature-complete）**；官方建议使用场景：现有应用中**局部**实现性能敏感页面，或**小型新应用**整体使用。**截至 2026-11 仍处 RC，非稳定版**，不建议生产大规模采用。
- **能力**：支持**仅模板的 SFC** 与使用 `<script setup>` 的 SFC；**不支持 Options API**。
- **启用方式**：
  - `<script setup vapor>`；
  - `<script vapor>`（等价于 `<script setup vapor>`）；
  - `<template vapor>`（对整个 SFC 启用 Vapor 编译）。
- **创建应用与互操作**：
  - 纯 Vapor：`createVaporApp(App)`，避免引入 VDOM 运行时，基线包体积大幅下降；
  - 在 VDOM `createApp()` 中用 Vapor 组件：安装 `vaporInteropPlugin`；
  - Vapor 应用中用 VDOM 组件也需该插件（但会引入 VDOM 运行时，抵消包体积收益）；官方建议**分区使用，避免深层混合嵌套**。
- **不支持 / 不适用**：Options API、`app.config.globalProperties`、`getCurrentInstance()` 返回 `null`、`@vue:xxx` 元素级生命周期事件、`v-memo`、组件模板 ref 不暴露 `$el` / `$props` / `$attrs` / `$slots` / `$refs`。
- **重要使用注意**：
  - **事件委托与 `stopPropagation()`**：Vapor 把合格事件委托到 `document`，若祖先调用 `stopPropagation()`，委托处理不会执行；`@[event]`、`v-bind="{ onClick }"`、`v-on="{ click }"` 绕过委托直接绑定元素。
  - **`slots.default()` 不是安全试运行**：调用会真实执行渲染逻辑，勿用其「探测」输出来决定是否渲染 fallback。
  - **自定义指令接口不同**：`(node, value?: () => any, argument?, modifiers?) => (() => void) | void`，`value` 为响应式 getter，可用 `watchEffect` 并在卸载时自动释放。
- **性能声明**：官方称第三方基准中 Vapor 达到与 **Solid / Svelte 5 同级**的性能。
- 来源：https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1

### 11. TypeScript 与 Vue3 集成

- **TypeScript 版本**：**7.0.2** 为最新主线（Go 原生移植，2026-07-08 GA，官方称约 10× 提速）；**5.9.3** 为 5.x 最新。
- **TS 7 关键事实（影响集成）**：
  - **不提供 JS 端编译器 API**（无 `ts.createProgram`、`ts.createSourceFile`、`ts.forEachChild` 等）；
  - 采用 TS 6 的新默认值，对 TS 6 已弃用的 flag 与构造给出**硬错误**；
  - 过渡桥接包 **`@typescript/typescript6`**（JS API 兼容的 6.0.x 包装）供仍依赖 JS API 的生态使用；**TS 7.1 将提供新的、不同的 API**；
  - Vue/Svelte/Astro/MDX 等基于 Volar 的工作流在 TS 7 下需验证兼容性（无编译器 API 可能影响部分工具链）。
- **Vue 侧类型**：`vue` 的类型定义可能在小版本间出现不兼容（官方说明）；建议用锁定 minor 的 semver 范围并在升级时手动升级。
- **Vue + TS 工具链**：`vue-tsc`（基于 Volar / `@vue/language-core`）做类型检查；`vueCompilerOptions`（如 Router 5 的 Volar 插件配置）定制语言工具；`<script setup lang="ts">`；`defineProps` / `defineEmits` / `defineModel` / `defineExpose` 的泛型与运行时声明。
- **Vite 8 对 TS 的支持**：内置 `resolve.tsconfigPaths` 与 `emitDecoratorMetadata`，减少对 `vite-tsconfig-paths`、`vite-plugin-vue-decorators` 等插件的依赖。
- 来源：https://devblogs.microsoft.com/typescript/ ；https://vite.dev/blog/announcing-vite8.html ；https://router.vuejs.org/guide/migration/v4-to-v5.html

### 12. JavaScript 核心（闭包/原型/异步）

- **闭包（Closure）**：函数与其声明时所在的词法环境的组合；即使外层函数已执行完毕，闭包仍能访问外层作用域变量，是数据封装与私有变量的实现基础（MDN）。
- **原型链与继承**：JS 基于原型的继承；`Object.create`、`class extends`、`super`、原型链查找；注意 `null` 原型对象、`Symbol.iterator` 等。
- **异步与事件循环**：JS 单线程，依赖**事件循环（event loop）**；任务（task）与微任务（microtask）队列，**每执行完一个任务后会清空整个微任务队列**再执行下一个任务，因此 `Promise` 回调总是先于 `setTimeout(..., 0)`；`async/await` 基于 Promise，用 `try/catch` 处理错误，并行用 `Promise.all`，可用 `AbortController` 取消 `fetch`。
- **模块系统**：ES Modules 为浏览器/官方标准（静态分析、Tree Shaking、动态只读引用）；CommonJS 同步加载、输出值拷贝；AMD / UMD / IIFE 属历史方案。
- **新趋势**：`Temporal` API（Vitest 5 的 fake timers 已默认模拟 `Temporal`）；`import defer`（TS 5.9 支持，延迟模块求值）；顶层 `await`、`require(esm)`（Node 默认支持，Vite 8 依赖此能力）。
- 来源：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures ；https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Inheritance_and_the_prototype_chain ；https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/EventLoop

### 13. CSS 现代布局（Flex/Grid）

- **Flexbox（弹性盒）**：一维布局，`display: flex`、`flex-direction`、`justify-content`、`align-items`、`flex-grow/shrink/basis`、`gap`；适合导航、工具栏、卡片流等。
- **CSS Grid（网格）**：二维布局，`display: grid`、`grid-template-columns/rows`、`grid-template-areas`、`grid-column/row`、`gap`；适合整页与复杂二维结构。
- **Baseline 兼容状态**：
  - **Grid**：Widely available（Baseline 2017-10-17）；
  - **Container Queries**：Widely available（Baseline 2023-02-14）；
  - **Subgrid**：Widely available（Baseline 2023-09-15）；
  - **Style queries（`@container style()`）**：较新，**2026 年 5 月成为 Baseline Newly Available**（Chrome 111+、Safari 18+、Firefox 151+）；不支持的浏览器会跳过该 `@container style()` 块，应把结构默认值写在外面。
- **现代趋势**：容器查询把响应式从「视口」转向「组件」（组件根据容器而非视口响应）；`:has()` 选择器；CSS 嵌套；`aspect-ratio`、`gap`、逻辑属性（`inline-*` / `block-*`）。
- 来源：https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Flexbox ；https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Grids

### 14. 前端工程化与模块化

- **模块化规范**：ES Modules（标准，`export` / `import`，静态分析支持 Tree Shaking）、CommonJS（`module.exports` / `require`，同步）、AMD（`define` / `require[]`）、UMD（跨环境）、IIFE（传统 `<script>`）。现代以 **ESM 为主**。
- **构建工具**：
  - **Vite 8**：开发期原生 ESM + Rolldown 预打包，生产用 Rolldown 打包，Node 20.19+/22.12+，ESM-only；
  - **Webpack**：复杂组件库、深度定制，生态成熟但配置复杂、构建较慢；
  - **Rollup**：适合发布精简的库（ESM/UMD 输出），常与 Vite（库模式）配合。
- **转译/压缩链**：Oxc（解析/转译/压缩）、Lightning CSS（CSS 压缩）、Babel（部分工具链仍使用，如 `@rolldown/plugin-babel`）。
- **工程化能力**：代码分割、Tree Shaking、模块级持久缓存、Source Map、环境 API、包管理（npm / pnpm / yarn）、Monorepo（Nx / Turborepo / Bazel）、依赖治理（锁定 minor、避免 dual-package hazard）。
- **注意**：Node 的 `type` 字段决定 `.js` 解释方式，发布**单一模块格式**（CJS 或 ESM）通常更佳；同时加载 CJS 与 ESM 可能导致同一包出现两份实例。
- 来源：https://vite.dev/blog/announcing-vite8.html ；https://webpack.js.org/concepts/module-federation ；https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Modules

### 15. 前端性能优化体系

- **核心指标（Core Web Vitals，2026 阈值）**：
  - **LCP（Largest Contentful Paint）**：好 ≤ 2.5s；2.5s–4.0s 待改进；> 4.0s 差；
  - **INP（Interaction to Next Paint）**：好 ≤ 200ms；**2024-03-12 起取代 FID**（FID 于 2024-09-09 从 CrUX / PageSpeed Insights 移除）；**INP 是唯一的交互性指标**；
  - **CLS（Cumulative Layout Shift）**：好 ≤ 0.1；0.1–0.25 待改进；> 0.25 差；
  - 评估取**真实用户数据（CrUX）的 75 分位**，在**页面级与源级**评估。
- **加载优化**：关键渲染路径、资源提示（`rel=preconnect` / `dns-prefetch` / `preload` / `prefetch`）、压缩（gzip / Brotli / Zopfli）、HTTP/2、CDN、按需加载（`loading="lazy"`，但 **LCP 图片不得延迟**，可用 `fetchpriority="high"`）、CSS 异步加载避免阻塞渲染、保持 JS 体积最小。
- **运行时优化**：长任务拆分、`requestIdleCallback`、避免布局抖动、虚拟列表、合理事件节流、感知性能（加载指示、骨架屏、尺寸匹配的占位避免 CLS）。
- **度量工具**：Performance Web API（Performance Timeline / Navigation Timing / User Timing / Resource Timing）、Lighthouse（实验室工具）、CrUX（真实用户）、Chrome DevTools。
- 来源：https://mdn.org.cn/en-US/docs/Learn/Performance/Web_Performance_Basics ；https://web.dev/articles/vitals

### 16. Web 安全基础（XSS/CSRF）

- **XSS（跨站脚本）**：攻击者通过网站把客户端脚本注入其他用户浏览器；因注入代码来自可信站点，可窃取 cookie 等并冒充用户。分为：
  - **反射型 XSS**：用户输入经服务器**未修改直接回显**并显示；
  - **持久型 XSS**：恶意脚本**存储**在站点，稍后原样显示给其他用户执行；
  - **基于 DOM 的 XSS**：前端脚本不安全地将数据写入 DOM。
- **XSS 防护**：对输出做**编码 / 清理**；使用 **CSP（Content-Security-Policy）**——基于 **nonce 或 hash** 的 `script-src` 指令确保只有带正确 nonce/hash 的脚本可执行，禁止内联脚本与 `eval()`，`object-src 'none'`、`base-uri 'none'`，并可用 `frame-ancestors` 防点击劫持、`upgrade-insecure-requests` 防 MITM；Vue 3.5 编译器输出自动生成 **TrustedHTML**，利于严格 CSP。
- **CSRF（跨站请求伪造）**：攻击者诱导用户/浏览器从恶意站点向目标站点发起 HTTP 请求，请求携带用户凭证，服务器误以为是用户本意而执行有害操作（如转账）。
- **CSRF 防护**：**CSRF token**（同步器 / 双重提交）、**SameSite Cookie**（`SameSite=Lax/Strict`）、校验 `Origin` / `Referer`、关键操作要求二次验证。
- 来源：https://developer.mozilla.org/zh-CN/docs/Web/Security/Attacks/XSS ；https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF ；https://mdn.org.cn/en-US/docs/Web/Security/Practical_implementation_guides/CSP

### 17. 前端测试（Vitest/Playwright）

- **Vitest 5**（2026-09-03 发布，5.1 于 2026-11-01）：
  - 以**性能**为主：内联 project 共享 Vite server、`fsModuleCache`（原 experimental，现稳定，跨重跑/跨进程复用转换后的模块）、主进程与 worker 往返减少、vm 池复用编译代码并支持 `require(esm)`、Browser Mode 预打包运行时并自适应开启会话、安装体积更小；
  - **Trace View**（Browser Mode）：记录每次交互/断言/`page.mark` 的 DOM 快照，可逐步骤回放，支持键盘导航与 watch 实时更新；
  - **`vi.when`**：为 spy 定义按参数（深比较、支持 `expect.any()`）返回不同值；
  - **Benchmark API 重写**：`bench` 不再是顶层导入，而是 `test()` 内的 fixture，支持 `compare` / `writeResult` / `from()`、自定义 provider；
  - **Locator 报错显示 ARIA 树**：`browser.locators.errorFormat`（`html` / `aria` / `all`），locators 默认 **strict**（`locators.exact` 默认启用）；
  - **mock `Temporal`**（`@sinonjs/fake-timers` v15.4）；
  - **更严格的断言**：未 await 的 `resolves` / `rejects` / `toMatchFileSnapshot` 会**失败**；`expect.poll` 超时会 reject 并传入 `AbortSignal`；
  - **`clearMocks` 默认开启**；
  - 报告与附件统一写入 `.vitest/`；HTML 报告支持 `singleFile` 自包含输出；
  - **要求 Vite ≥ 6.4.0、Node.js ≥ 22.12.0**。
- **Playwright**（**1.65.1**，2026-11-09）：
  - **支持在 Bun 上运行测试**：Bun 自行转译 TS 测试文件，Playwright 不再用 Babel，需 `--bun` 标志；
  - 浏览器版本：**Chromium 159.0.8154.6 / Firefox 159.0 / WebKit 27.2**；
  - 定位器代码（Python `locator.normalize()` + `page.get_by_ref()`，配合 `aria_snapshot()` 的 `"ai"` 模式）；
  - 动作等待元素非 `inert`；Cookie 匹配遵循 **RFC 6265**。
- **定位差异**：Vitest 偏单元/组件测试（与 Vite 同构、API 与 Jest 类似、与 Vue 深度集成）；Playwright 是现代端到端（E2E）默认，提供免费并行/分片、真实多引擎（Chromium/Firefox/WebKit）、多标签多上下文测试，近期侧重 agent 驱动测试。
- 来源：https://vitest.dev/blog/vitest-5.html ；https://github.com/microsoft/playwright/releases ；https://playwright.dev/docs/release-notes

### 18. 前端微前端架构

- **定义**：将一个前端应用拆为多个**可独立开发、独立部署**的子应用，组合成统一用户体验；适合前端体量大（如 10 万+ 行）、多团队、需独立部署、或希望不同子应用用不同框架的团队。
- **不适用场景**：前端小或单体（如 < 5 万行）、单一团队维护、强一致性 UX、对包体积/性能极敏感、团队缺乏分布式前端能力、低延迟敏感场景。
- **主流技术方案**：
  - **Module Federation（Webpack / Rolldown）**：运行时从远端加载模块，容器接口支持 `get` / `init`，`init` 是异步、兼容单参（共享 scope 对象）的调用，用于把远端容器动态接入宿主；支持动态远端容器、依赖共享；Rolldown 亦提供 Module Federation 支持。
  - **运行时组合**：single-spa、Web Components、iframe 沙箱、Import Maps / ESM 动态导入。
  - **构建时组合**：Monorepo + 构建期集成（Nx / Turborepo / Bazel）。
- **关键工程实践**：每个 MFE 独立错误隔离（崩溃不整页白屏，渲染 fallback）；**每个片段的性能预算**（JS 体积、LCP、INP，在 CI 中约束，防止页面载荷随合并持续膨胀）；共享依赖治理；公共 UI / 状态与样式一致性策略；沙箱隔离（样式、全局变量、路由）。
- **架构权衡**：包体积与性能、加载与运行时开销、跨团队协调成本、一致性 vs 独立性；Monorepo 便于原子化跨切面改动与共享 lint/tsconfig，Polyrepo 更贴合组织实际。
- 来源：https://webpack.js.org/concepts/module-federation ；https://docs.aws.amazon.com/prescriptive-guidance/latest/micro-frontends-aws/frameworks-tools.html

## 四、写作要点与风险提示

1. **版本口径必须标注时间**：本文基于 **2026-11** 检索；Vue 3.6 仍为 RC、Vite 8 / Nuxt 4.6 / Vue Router 5 / Pinia 4 / Vitest 5 / Playwright 1.65 / TS 7 均较新。写作时建议在文档开头注明「截至 2026-11」，避免读者误以为是未来稳定版。
2. **「Vue Router 4」知识点要写清演进**：任务知识点名为 Router 4，但**当前最新为 Router 5**。文档应以 Router 4 的核心 API 为主干，同时明确说明 Router 5 是过渡版、对纯 Router 4 用户无破坏性变更、Router 6 将 ESM-only。
3. **Vapor Mode 是最大风险点**：截至 2026-11 **仍处 3.6 RC、非稳定**，且**不支持 Options API / `v-memo` / `getCurrentInstance` / 模板 ref 的 `$el` 等**，事件委托与 `stopPropagation`、`slots.default()`、自定义指令接口均有差异。写作时应明确标注「RC、实验性、官方建议局部或小应用使用」，避免误导读者在生产大规模采用。
4. **TS 7 对工具链的影响**：TS 7 为 Go 原生移植、**无 JS 编译器 API**，可能影响依赖 `ts.*` API 的生态（如 Volar / vue-tsc 路线、类型解析工具）；文中应提示读者验证兼容性，必要时使用 `@typescript/typescript6` 兼容包装或 TS 5.x 线。
5. **Nuxt 3 已 EOL**：涉及 SSR 的文档应默认以 **Nuxt 4.6** 为准，并提示仍在使用 Nuxt 3 的读者升级（2026-07-31 已停止支持）。
6. **破坏性变更要突出**：Pinia 4 的 **ESM-only + 需手动安装 `@vue/devtools-api`**、Vite 8 的 **Rolldown 迁移与约 15 MB 体积增加**、Vitest 5 的 **`clearMocks` 默认开启 / 未 await 断言失败 / 要求 Vite ≥ 6.4.0、Node ≥ 22.12.0**，均为升级时的易踩坑点。
7. **数据需回源核对**：表中补丁版本日期、体积/性能数字（如 56% 内存下降、10–30× 构建提速、Nuxt 性能对比）部分来自官方发布说明或社区转述，写作引用前请以官方原文为准；性能对比数字依赖硬件与场景，不宜绝对化。
8. **来源优先级**：优先使用官方文档与官方仓库（vuejs.org、router.vuejs.org、pinia.vuejs.org、vite.dev、nuxt.com、vitest.dev、playwright.dev、typescriptlang.org、developer.mozilla.org、webpack.js.org、web.dev）；第三方聚合站仅作线索，不作为最终引用。
