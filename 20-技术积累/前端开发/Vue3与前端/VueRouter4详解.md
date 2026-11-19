---
title: Vue Router 4 详解
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - Vue Router
  - 路由
  - 导航守卫
aliases:
  - Vue Router 4 详解
  - Vue Router 4 与 Router 5 迁移
source: 网络资料整理
---

# Vue Router 4 详解

> [!摘要] 摘要
> 本文系统讲解 Vue 3 官方路由库 **Vue Router 4**：从它在整个 Vue3 全家桶中的定位出发，梳理基础概念、内部核心机制（匹配、守卫、导航解析、数据获取），再给出可直接运行的安装、配置、动态路由与守卫代码示例，最后汇总最佳实践与常见坑。**需要特别说明：知识点名为「Router 4」，但截至 2026-11 官方最新已是过渡版 Vue Router 5**，本文以 Router 4 的核心 API 为主干，同时明确标注向 Router 5 的演进路径与差异，便于既有项目平滑迁移。本文是 [[Vue3与前端-从入门到精通]] 体系下「路由层」的深入展开。

## 一、最新动态（截至 2026-11）

- **Vue Router 已由 4 进入 5**：调研文件记载 **Vue Router 5.0.0 于 2026-01-29 发布**，最新 **5.0.4** 约 2026-03-19；主题总览文档记载 npm `latest` 为 **5.5.1**。**Router 5 是过渡版本**，把 `unplugin-vue-router` 的**基于文件的路由**能力合并进核心包。版本细节以官方仓库为准。
- **对纯 Router 4 用户无破坏性变更**：只要项目**未使用 `unplugin-vue-router`**，`pnpm update vue-router@5` 即可升级，原有写法继续可用。
- **Router 5 新增入口 / 导出**：
  - `vue-router/vite`：Vite 插件，替代原 `unplugin-vue-router/vite`；
  - `vue-router/unplugin`：供 Webpack / Rollup / esbuild 使用及工具函数；
  - `vue-router/auto-routes`：由插件生成的路由；
  - `vue-router/experimental`：实验特性，含 **data loaders**（以及 `pinia-colada` loader）；
  - `vue-router/volar/sfc-typed-router`、`vue-router/volar/sfc-route-blocks`：Volar 插件，提供 SFC 类型化路由与路由块支持。
- **实验特性**：查询参数默认可选（`experimental: Query params are optional by default`）、data loaders、路由 JSON schema、`definePage({ name })`。
- **导航守卫写法调整**：`next()` 回调自 **Router 5.0.3 起标记弃用**，官方建议改为**从守卫函数返回值**（返回 `false`、路径字符串，或抛出错误）。
- **面向 Router 6**：**Vue Router 6 将是 ESM-only 并移除已弃用 API**，v5 正是过渡准备期；同时 **iife 构建不再内置 `@vue/devtools-api`**（该包升级到 v8，已无 IIFE 构建），依赖 IIFE 产物的项目需留意。
- 来源：[Vue Router 官方迁移指南 v4 → v5](https://router.vuejs.org/guide/migration/v4-to-v5.html)、[vuejs/router Releases](https://github.com/vuejs/router/releases)。

## 二、基础概念

- **定位**：Vue Router 是 Vue 3 的官方路由库，负责**页面路径与组件的映射**、**地址栏与浏览器历史同步**、**导航拦截与权限控制**、**页面级数据获取与滚动恢复**，是 SPA（单页应用）的骨架。它与 Pinia（状态）、Vite（构建）并列为 Vue3 全家桶三大基础件。
- **路由三要素**：**路径（path）**、**组件（component）**、**命名（name）**。路径决定 URL，组件决定渲染内容，name 用于编程式导航与命名路由。
- **两种历史模式**：
  - `createWebHistory()`：使用 HTML5 History API，URL 为 `/about` 这类**干净路径**，需要服务端配置回退到 `index.html`；
  - `createWebHashHistory()`：使用 `#` 哈希，URL 形如 `/#/about`，**无需服务端额外配置**，适合静态托管。
- **两个核心对象**：`router`（路由器实例，负责导航与守卫）与 `route`（当前路由对象，含 `path`、`params`、`query`、`matched` 等）。`useRouter()` 取路由器、`useRoute()` 取当前路由，且 `route` 是**响应式**的。
- **两个核心组件**：`<RouterLink>`（渲染链接、带路由高亮，替代 `<a>`）与 `<RouterView>`（路由出口，渲染匹配到的组件）。
- **路由表结构**：以「路由记录（route record）」数组组织，支持**嵌套路由**（`children`）与**动态路由**（`/user/:id`），二者是权限控制与模块化组织页面的基础。
- **导航类型**：**声明式**（`<RouterLink>`）与**编程式**（`router.push` / `router.replace` / `router.go`）。

## 三、核心机制

**1. 匹配与渲染。** `createRouter` 内部用**匹配器（matcher）**把路由表编译为匹配函数，每次导航时用当前 URL 找出匹配的路由记录，生成「路由对象」并写入当前路由；`<RouterView>` 依据匹配结果渲染对应组件。`matched` 数组保留了从父到子的整条匹配链，是嵌套路由与布局组件能正确嵌套渲染的关键。

**2. 三级导航守卫与执行顺序。** 守卫是实现权限、埋点、数据预取的官方机制，按以下顺序依次触发：

1. 组件内 `beforeRouteLeave`（当前组件要离开时）
2. 全局 `beforeEach`
3. 路由记录内 `beforeEnter`
4. 组件内 `beforeRouteUpdate`（复用组件、参数变化时）/ `beforeRouteEnter`（首次进入时）
5. 全局 `afterEach`（无返回值，负责收尾）

Router 5.0.3 起 `next()` 弃用，推荐用**返回值**控制流程：返回 `false` 中止、返回路径字符串重定向、抛错终止，`afterEach` 不受此约束。

**3. 导航解析与重定向。** 导航是**异步**过程：`push` 会先经过守卫链，全部放行后才真正更新地址栏与组件；过程中可用 `router.beforeEach` 做登录校验，用 `redirect` / 返回路径做重定向。`router.resolve()` 可在不触发导航的情况下做路径解析。

**4. 数据获取。** 两种主流方式：**组件内 `onMounted` / `watch`** 自行请求，或 **`<Suspense>` + 异步组件** 让路由切换等待异步组件就绪（`<RouterView>` 外层包 `<Suspense>` 即可）。Router 5 的 **data loaders** 把「路由 → 数据」声明式绑定（实验特性，入口 `vue-router/experimental`）。

**5. 文件路由（Router 5 核心变化）。** Router 5 将原 `unplugin-vue-router` 的文件路由并入核心，按目录结构自动生成路由（`vue-router/auto-routes`），免除手写路由表；仍需要手工配置时用 `vue-router/vite` 插件。

**6. 懒加载与代码分割。** 路由组件写成动态导入（`component: () => import('@/views/About.vue')`）即可按路由拆分 chunk，是控制首屏体积最直接的手段。

## 四、实践步骤（含代码/命令示例）

**1. 安装（Router 4 / 5 均可）：**

```bash
# Router 4 用户保持原依赖；新项目直接装 5
npm install vue-router@5
# 或 pnpm / yarn
pnpm add vue-router@5
```

**2. 创建路由并挂载应用。** `src/router/index.ts`：

```typescript
import { createRouter, createWebHistory } from 'vue-router'

// 路由懒加载：按路由切分 chunk
const Home = () => import('@/views/Home.vue')
const User = () => import('@/views/User.vue')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    // 动态路由：/user/123
    { path: '/user/:id', name: 'user', component: User,
      props: true },
    // 重定向与 404 兜底
    { path: '/old', redirect: '/' },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: Home },
  ],
  // 滚动行为：切页回到顶部
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
```

**3. 在入口挂载并声明出口。** `src/main.ts` 与 `App.vue`：

```typescript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

```vue
<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav>
    <RouterLink to="/">首页</RouterLink>
    <RouterLink to="/user/1">用户页</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>
```

**4. 组件内使用路由与编程式导航：**

```vue
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// route.params.id / route.query.page 均为响应式
console.log('当前用户 ID：', route.params.id)

function goDetail(id: number) {
  router.push({ name: 'user', params: { id } })
}
</script>
```

**5. 全局前置守卫（推荐用返回值写法）：**

```typescript
router.beforeEach((to, from) => {
  const loggedIn = Boolean(localStorage.getItem('token'))
  // 未登录访问受保护页面 → 返回重定向路径
  if (to.meta.requiresAuth && !loggedIn) {
    return { name: 'home', query: { redirect: to.fullPath } }
  }
  return true // 放行
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - 站点` : '站点'
})
```

**6. 启用 Router 5 文件路由（替代手写路由表）：**

```bash
npm install vue-router@5
```

```typescript
// vite.config.ts —— 用 vue-router/vite 替代 unplugin-vue-router/vite
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueRouter from 'vue-router/vite'

export default defineConfig({
  plugins: [vue(), vueRouter()],
})
```

```typescript
// src/router/index.ts —— 直接引用自动生成的路由
import { createRouter, createWebHistory } from 'vue-router'
import { autoRoutes } from 'vue-router/auto-routes'

export default createRouter({
  history: createWebHistory(),
  routes: autoRoutes,
})
```

**7. 类型安全（配合 Volar 插件）：**

```bash
npm install -D vue-router/volar/sfc-typed-router
```

在 `vueCompilerOptions` 中启用后，`<RouterLink>` 的 `to` 与 `useRoute()` 的跳转目标可获得类型提示。

## 五、最佳实践与常见坑

**最佳实践：**

- **按模块拆分路由表**，页面组件一律**懒加载**，用 `createWebHistory` 时同步配置服务端回退，避免刷新 404。
- **权限统一收口到全局 `beforeEach`**，组件内守卫只处理该页专属逻辑；**用返回值**而非 `next()`，面向 Router 5/6 提前对齐。
- **参数用 `name` + `params` 导航**而非拼字符串，避免路径拼接与转义问题；动态路由加 `props: true` 可让组件直接收到参数。
- **滚动恢复交给 `scrollBehavior`**（保留滚动位置、切页回顶），不要用组件内手动操作 `scrollTo`。
- **数据获取优先 `<Suspense>`** 或路由级 data loader，避免在切换瞬间出现空白闪烁。
- **升级到 Router 5 前确认**：未使用 `unplugin-vue-router` 则无破坏性变更；使用 IIFE 构建的需评估 `@vue/devtools-api` 变更。

**常见坑：**

| 现象 | 常见原因 | 处理 |
| --- | --- | --- |
| 刷新页面 404 | 使用 `createWebHistory` 但服务端未配置 SPA 回退 | 配置 Nginx `try_files $uri $uri/ /index.html`，或改用 `createWebHashHistory` |
| 数据更新了视图不刷新 | 组件内直接改 `route.params`（路由对象只读） | 用 `watch(() => route.params.id, ...)` 监听后重新请求数据 |
| 守卫里 `next()` 失效/告警 | Router 5.0.3 起 `next()` 已弃用 | 改为从守卫函数返回 `true` / `false` / 路径 |
| 动态路由参数丢失 | 用字符串路径跳转，参数需自行拼接 | 改用 `{ name: 'user', params: { id } }` |
| `useRoute()` 拿到旧值 | 未等导航完成就读取新路由 | 在 `afterEach` 或 `watch` 中处理，或 `await router.isReady()` 后再取 |
| 组件被复用、`onMounted` 不触发 | 同一路由记录只切换参数（`beforeRouteUpdate` 场景） | 监听 `route.params` 变化重新加载数据 |

## 六、核心要点速查

1. **版本口径**：Router 4 仍是大量存量项目的主干；截至 2026-11 官方最新为 **Router 5**（5.0.0 于 2026-01-29，调研文件记载 5.0.4；总览文档 npm `latest` 为 5.5.1），Router 5 为过渡版，**Router 6 将 ESM-only 并移除弃用 API**。
2. **对纯 Router 4 用户无破坏性变更**，`pnpm update vue-router@5` 即可。
3. **核心 API**：`createRouter` / `createWebHistory` / `createWebHashHistory`，组件 `<RouterLink>` / `<RouterView>`，组合式 `useRouter` / `useRoute`。
4. **守卫三级体系**：全局 `beforeEach` / `afterEach`、路由内 `beforeEnter`、组件内 `beforeRouteLeave` / `beforeRouteUpdate` / `beforeRouteEnter`。
5. **守卫写法**：`next()` 自 **5.0.3 起弃用**，改用**返回值**（`false` / 路径 / 抛错）。
6. **Router 5 新入口**：`vue-router/vite`、`vue-router/unplugin`、`vue-router/auto-routes`、`vue-router/experimental`、两个 Volar 插件。
7. **实验特性**：查询参数默认可选、data loaders、路由 JSON schema、`definePage({ name })`。
8. **滚动恢复**靠 `scrollBehavior`；**首屏优化**靠路由懒加载（动态 `import`）。
9. **`route` 是响应式但只读**，不要直接改，改由导航触发。
10. **IIFE 构建**不再内置 `@vue/devtools-api`（已升级 v8），相关项目需单独确认。

## 七、学习资源

- [Vue Router 官方文档](https://router.vuejs.org/)
- [Vue Router 官方迁移指南 · v4 到 v5](https://router.vuejs.org/guide/migration/v4-to-v5.html)
- [vuejs/router 仓库 Releases（版本与变更）](https://github.com/vuejs/router/releases)
- [vuejs/router 仓库（源码与 issue）](https://github.com/vuejs/router)
- [npm vue-router latest 版本信息](https://registry.npmjs.org/vue-router/latest)
- [Vue 官方中文文档 · 快速上手](https://cn.vuejs.org/guide/quick-start.html)
- [Vue 官方中文文档 · RouterLink / RouterView API](https://cn.vuejs.org/api/built-in/components/RouterLink.html)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题所在体系总览，路由层的定位与全局版本口径
- [[Vue3-组合式API]] — `useRouter` / `useRoute` 与 `<script setup>` 的组合式写法基础
- [[前端开发]] — 前端技术整体地图与目录索引
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
