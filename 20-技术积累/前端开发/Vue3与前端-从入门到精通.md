---
title: Vue3与前端-从入门到精通
date: 2026-11-18
updated: 2026-11-18
tags:
  - 前端开发
  - Vue3
  - 组合式API
  - Vite
  - 响应式
  - Vapor-Mode
aliases:
  - Vue3 与前端：从入门到精通
  - 现代前端工程与 Vue3 全家桶
source:
  - https://cn.vuejs.org/guide/quick-start.html
  - https://github.com/vuejs/core/blob/main/CHANGELOG.md
  - https://registry.npmjs.org/-/package/vue/dist-tags
---

# Vue3与前端-从入门到精通

> [!summary] 摘要
> 本文定位为**现代前端工程与 Vue3 全家桶**的系统性知识地图：以 [[HTML-CSS布局技巧]] 与构建工具链为工程底座，以 Vue3 的 [[Vue3-组合式API]] 为核心，串联 Vue Router、Pinia、Vite、SSR/SSG、跨端方案与生产实践。适合想从「会写页面」进阶到「能做生产级应用」的前端开发者；结构按 **入门 → 进阶 → 精通** 三段递进，先建立概念与环境，再理解响应式与编译优化机制，最后落到架构、生产与生态前沿，文末附版本速查与学习资源。

## 一、最新动态（截至 2026-11）

> [!info] 版本口径说明
> 下表只收录可核实的发布信息：稳定版取自 npm `latest` 标签，RC 版取自 npm `rc` 标签与官方 CHANGELOG，正文一律以官方文档为准，不做预测性描述。

| 组件 / 项目 | 版本 | 更新要点 | 来源 |
| --- | --- | --- | --- |
| Vue | 3.5.45（2026-11-05） | npm `latest` 稳定版，修复 hydration、Suspense、KeepAlive、v-model、reactivity 等多处缺陷，为官方 CHANGELOG 顶部条目 | [vuejs/core CHANGELOG](https://github.com/vuejs/core/blob/main/CHANGELOG.md) |
| Vue | 3.6.0-rc.15（rc 标签） | 3.6 处于 RC 阶段：Vapor Mode 功能集已完成，`@vue/reactivity` 基于 alien-signals 重构，性能与内存显著提升；正式版时间以官方文档为准 | [npm vue dist-tags](https://registry.npmjs.org/-/package/vue/dist-tags) |
| Vue Router | 5.5.1 | npm `latest`；导航守卫中的 `next()` 回调自 5.0.3 起标记弃用、改用返回值，持续加入 `definePage`、experimental 路由等能力 | [npm vue-router latest](https://registry.npmjs.org/vue-router/latest) |
| Pinia | 4.1.0 | npm `latest`；Vue 官方状态管理库，主打直观、类型安全、可扩展，同时支持 Composition API 与 Options API | [npm pinia latest](https://registry.npmjs.org/pinia/latest) |
| Vite | 8.3.8 | npm `latest`；Vite 8 由 Rolldown（Rust 打包工具，基于 Oxc）取代 esbuild + Rollup，统一开发与生产工具链，生产构建显著提速 | [npm vite latest](https://registry.npmjs.org/vite/latest) |
| @vitejs/plugin-vue | 6.0.11 | Vue SFC 在 Vite 中的官方插件；peer 兼容 `vue ^3.2.25 \|\| ^3.6.0-rc.15`，兼容 Vite 5/6/7/8 | [npm @vitejs/plugin-vue latest](https://registry.npmjs.org/@vitejs/plugin-vue/latest) |
| Nuxt | 4.6.0（2026-10-05） | 引入 `nuxt/server` 解耦服务端、类型化 `$fetch`、appSecret 与 sessions、Vue Vapor 支持（interop 模式）及新版开发错误页；Nuxt 3 已于 2026-07-31 结束生命周期 | [Nuxt 官方博客 · Nuxt 4.6](https://nuxt.com/blog/v4-6) |

> [!warning] 选型提醒
> 生产项目当前应锁定 **Vue 3.5.x 稳定版**；3.6 的 Vapor Mode 是 100% opt-in，需显式开启，新特性建议先在非核心模块试跑，不要直接在存量项目全局启用。

## 二、入门篇

### 2.1 基础概念

现代前端工程围绕「HTML/CSS 布局 + 工程化 + 构建工具链」展开，Vue3 全家桶是其中最具代表性的体系，包含五个层次：

- **Vue 核心**：以组合式 API（`<script setup>`）为开发范式，底层由 Proxy 重构的响应式系统 + 编译时优化驱动性能。
- **Vue Router**：负责路由与导航守卫。
- **Pinia**：提供类型安全的状态管理。
- **Vite**：当前主流构建工具，Vite 8 起由 Rust 编写的 Rolldown 驱动。
- **SSR/SSG 与跨端**：Nuxt 做服务端渲染/静态生成，uni-app / Taro 做多端复用。

核心心智模型是**「数据 → 响应式 → 视图 → 组件」**：开发者只描述状态与状态到视图的映射，框架负责高效地让视图随状态变化，而不是手写命令式 DOM 操作。这一思想与 [[React-Hooks详解]] 中的「状态驱动视图」一致，但实现路径不同（Vue 是响应式依赖收集，React 是单向数据流 + 重渲染）。

> [!note] 术语对照
> **SFC（单文件组件）**：`.vue` 文件由 `<template>`、`<script>`、`<style>` 三部分组成，是 Vue 组件的标准组织方式，可在官方演练场 [play.vuejs.org](https://play.vuejs.org) 免构建直接体验。

### 2.2 环境准备

- **Node.js 版本**：Vue 官方快速上手要求 **`^22.18.0 || >=24.12.0`**，请先 `node -v` 核对，低版本会导致脚手架与依赖安装异常。
- **推荐脚手架**：使用官方 `create-vue` 生成基于 **Vite + Vue3 + 可选 TypeScript** 的项目：

```bash
# 交互式创建（按提示选择 TypeScript / ESLint / 测试等）
npm create vue@latest
```

- **依赖安装与启动**：

```bash
npm install
npm run dev      # 本地开发，默认 http://localhost:5173
npm run build    # 生产构建
npm run preview  # 预览生产构建产物
```

> [!tip] 上手路径
> 中文文档入口为 [cn.vuejs.org](https://cn.vuejs.org/guide/quick-start.html)，官方给出的「快速上手 → 核心概念 → API → 迁移指南」就是一条完整的系统学习路径，本文的三段结构与之对应。

### 2.3 第一个实践（含代码示例）

下面用一个最小可用的 Todo 组件，覆盖 `<script setup>`、`ref`、`computed`、`watch`、`v-model`、`props/emits` 这几个最高频的入门知识点。

**父组件 `App.vue`：**

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import TodoItem from './components/TodoItem.vue'

// ref 用于基本类型，模板中自动解包
const keyword = ref('')
const todos = ref<string[]>(['学习 Vue3 组合式 API', '配置 Vite 工程化'])

// computed 带缓存的派生状态：只在依赖变化时重新计算
const remaining = computed(() => todos.value.filter((t) => !t.includes('完成')).length)

// watch 处理副作用（这里用控制台观察，实际项目里可能是异步请求或持久化）
watch(remaining, (n) => {
  console.log('剩余待办数量变化：', n)
})

function addTodo(text: string) {
  if (!text.trim()) return
  todos.value.push(text)
}
</script>

<template>
  <div>
    <!-- v-model 双向绑定；Vue 3.4 起支持多个 v-model -->
    <input v-model="keyword" placeholder="输入待办，回车添加" @keyup.enter="addTodo(keyword)" />
    <p>剩余：{{ remaining }}</p>

    <TodoItem
      v-for="(todo, i) in todos"
      :key="todo + i"
      :todo="todo"
      :index="i"
      @toggle="(i) => (todos[i] = todos[i] + '（完成）')"
    />
  </div>
</template>
```

**子组件 `TodoItem.vue`：**

```vue
<script setup lang="ts">
// 编译器宏，无需 import：defineProps / defineEmits / defineModel
const props = defineProps<{ todo: string; index: number }>()
const emit = defineEmits<{ (e: 'toggle', index: number): void }>()
</script>

<template>
  <li>
    <span>{{ props.todo }}</span>
    <button @click="emit('toggle', props.index)">标记完成</button>
  </li>
</template>

<style scoped>
/* scoped 样式只在当前组件生效，实现样式隔离 */
li {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}
</style>
```

> [!note] 入门阶段必须建立的几个「肌肉记忆」
> 1. `ref` 用于基本类型、`reactive` 用于对象，模板中 `ref` 自动解包，脚本里要写 `.value`；
> 2. `defineProps` / `defineEmits` / `defineModel` 是**编译器宏**，不需要导入；
> 3. 组件通信三件套：`props`/`emits`（父子）、`provide`/`inject`（跨层）、`v-model`（双向）；
> 4. 样式隔离优先用 `scoped`，需要更细粒度时用 CSS Modules，配合 [[HTML-CSS布局技巧]] 中的 Flexbox/Grid/容器查询。

## 三、进阶篇

### 3.1 核心机制

**1. 响应式原理。** Vue3 用 **Proxy**（替代 Vue2 的 `Object.defineProperty`）实现响应式，配合**依赖收集（`track` / `trigger`）**与 `ReactiveEffect`/`effect`：读取时记录「谁在用这个属性」，修改时通知对应副作用重新执行。Vue 3.6 起 `@vue/reactivity` 基于 **alien-signals** 重构，性能与内存占用明显改善。

**2. 编译时优化。** Vue3 在编译期做大量静态工作，直接减少运行时虚拟 DOM diff 开销：

- **静态提升（hoistStatic）**：把无动态绑定的节点提升到渲染函数外，只创建一次；
- **Block Tree**：以「动态节点」为锚点把 VNode 组织成区块，缩小 diff 范围；
- **补丁标记（PatchFlags）**：给每个节点标注可跳过的 diff 类型，运行时按标记做定向更新；
- **事件监听缓存**、**`v-memo`**：缓存事件处理函数，或对列表项做条件性跳过更新。

**3. 组件化与逻辑复用。** 以**组合式函数（composables）**按功能组织代码，取代 mixins；遵循官方 Vue Style Guide，避免混用 Options / Composition API、避免不必要的深层响应式。

> [!warning] 响应式丢失的经典原因
> **解构 `reactive` 对象会丢失响应性**：解构出来的属性是普通值，不会随原对象变化。正确做法是用 `toRefs` 展开，或直接使用 `ref` / `computed`：

```typescript
import { reactive, toRefs } from 'vue'

const state = reactive({ count: 0, name: 'vue' })
const { count } = state // ❌ 丢失响应性
const { count: safeCount } = toRefs(state) // ✅ 保持响应性
```

**4. Vue Router 进阶。** 全局 / 路由内 / 组件内**三级导航守卫**；注意 **`next()` 回调自 Vue Router 5.0.3 起已弃用**，应改为**从守卫返回值**（返回 `false`、路径字符串，或抛错）。还需掌握路由懒加载、滚动行为（scrollBehavior）、动态路由与权限控制。

**5. Pinia 进阶。** 组件外使用 store **必须确保 pinia 实例已激活**（先 `app.use(pinia)`，再取 store，否则报错）；`storeToRefs` 用于解包、`$subscribe` 用于订阅变化、SSR 下需注意激活时序，插件可扩展 store 能力，也可用组合式风格定义 store。

**6. 类型安全。** Vue 本身以 TypeScript 编写、官方包自带类型声明；`defineProps` / `defineEmits` 支持**纯类型声明**写法，`create-vue` 可选启用 TS，配合 **vue-tsc** 做类型检查。

### 3.2 最佳实践

- **响应式取舍**：基本类型用 `ref`、对象用 `reactive`；优先用 `computed` 做派生，避免在模板里写复杂表达式或重复计算。
- **副作用边界**：`watch` / `watchEffect` 只放在真正需要的地方，避免不必要的 **deep watch**（会显著放大开销）；`watchEffect` 立即执行一次，适合「自动追踪依赖」的场景，需要精确控制依赖时用 `watch`。
- **列表渲染**：合理使用 `key`（推荐稳定唯一值，不要用数组索引做动态列表的 key），必要时用 `v-memo`。
- **性能优化**：`v-if` 与 `v-show` 按「是否频繁切换」取舍；懒加载路由与组件、虚拟列表处理大列表；手动分块与 tree-shaking 优化打包，详见 [[前端性能优化]]。
- **构建工程化**：Vite 基于原生 ESM 的 dev server 与 Rolldown 生产构建，掌握插件体系、路径别名、环境变量、代码分割与 HMR，构建细节见 [[Webpack配置指南]]（迁移到 Vite/Rolldown 时的核心概念对照）。
- **样式与布局**：现代布局以 Flexbox、Grid、容器查询、CSS 变量为主，Vue 侧用 scoped 样式、CSS Modules 做隔离，见 [[HTML-CSS布局技巧]]。
- **语法风格**：逻辑复用优先 composables，避免无意义的深层 `reactive`，不要在 `<script setup>` 中混用 Options API。

> [!tip] 一个可执行的性能自检清单
> 1. 用 Vue DevTools 的 Profile 看渲染耗时，先定位再优化；2. 检查是否有多余的 deep watch / 重复 computed；3. 检查大列表是否做了虚拟化或懒加载；4. 用构建产物分析（rollup/rolldown 可视化）看 chunk 拆分与重复依赖。

### 3.3 常见问题与排查

| 现象 | 常见原因 | 排查与处理 |
| --- | --- | --- |
| 数据改了视图没更新 | 解构 `reactive` 丢失响应性；解构/展开后未用 `toRefs` | 检查是否用了 `toRefs`；确认数据确实落在响应式对象上 |
| 在 `setup` 里访问 `this` 失败 | `setup` 中没有 `this`（在组件实例创建前执行） | 需要组件实例时用 `getCurrentInstance()`，但多数场景应直接用组合式写法 |
| 组件外调用 store 报错 | 组件外使用 store 时 pinia 实例尚未激活 | 先 `app.use(pinia)` 再取 store；SSR 场景注意激活时序 |
| SSR 水合（hydration）不匹配 | 服务端与客户端渲染结果不一致（时间、随机值、浏览器 API） | 用 `onMounted` 等客户端钩子隔离浏览器专属逻辑，保证首屏一致 |
| KeepAlive 缓存失效 | 组件 `name` 缺失、`include/exclude` 配置不匹配、切换方式不当 | 确保组件有明确的 `name`，核对 `include` / `exclude` 规则 |
| `watch` 回调里重复收集依赖 | 在副作用中又读取了被监听的状态，形成自触发 | 用 `flush: 'post'` 或调整依赖范围，必要时拆成独立 `computed` |

> [!bug] 排查第一原则
> 先区分是**响应式问题**（数据没更新）还是**渲染问题**（数据更新了但视图没变）。前者看依赖收集（是否被 `track`、是否丢响应性），后者看编译优化与 `key`、`v-if/v-show` 使用，用 Vue DevTools 的渲染追踪能快速定位。

## 四、精通篇

### 4.1 架构与设计

**分层组织**是 Vue 大型应用的典型工程结构：

- **组合式函数层**：按「领域能力」而非「组件」组织，一个 composable 只负责一个功能（如 `usePagination`、`useForm`、`useWebSocket`），可被多组件复用，天然替代 mixins。
- **状态层**：Pinia 按业务模块拆分 store，保持 store 的单一职责，配合 `$subscribe` 做副作用与持久化。
- **路由层**：路由表按模块划分，动态路由 + 导航守卫实现权限控制，路由懒加载控制首屏体积。
- **服务层**：统一封装 HTTP 请求、错误处理与类型化响应，SSR 场景下注意数据获取与 hydration 策略。
- **可观测性**：Vue DevTools 贯穿开发、调优与线上问题定位。

> [!note] 设计判断
> 组合式函数关注的是「逻辑复用的边界」，Pinia 关注的是「跨组件共享状态的边界」，路由关注的是「页面与权限的边界」。三层各司其职，避免把状态逻辑写死在组件里、也避免让 composable 直接依赖具体路由实现。

### 4.2 生产实践

- **类型安全**：Vue 官方包自带类型声明，`create-vue` 选 TS，`defineProps`/`defineEmits` 用纯类型声明，CI 中跑 `vue-tsc --noEmit` 做类型门禁。
- **构建与交付**：Vite 8 / Rolldown 下关注 chunk 拆分、代码分割与产物体积；生产构建前做产物分析，避免重复依赖与巨型 chunk。
- **SSR / SSG**：Vue 提供 [`@vue/server-renderer`](https://cn.vuejs.org/)；Nuxt 是主流元框架，默认支持 **SSR / SSG / SPA 多模式**。Nuxt 4.6 起以 **interop 模式支持 Vue 3.6 Vapor**（需 `vue ^3.6.0-rc.2+`），并引入 `nuxt/server` 将服务端 API 与 Nitro/h3 解耦，支持类型化 `$fetch`、appSecret、sessions 与实验性 `@nuxt/vite-server`。
- **渐进式迁移与灰度**：存量 Options API 项目可按组件逐个迁移到 `<script setup>`；新特性（如 Vapor）按模块灰度，降低回归风险。
- **性能基线**：首屏体积、交互响应、长列表与内存占用要建立可量化基线，用 Profile 与构建分析持续回归，相关方法论见 [[前端性能优化]]。

### 4.3 生态与前沿

**1. Vapor Mode（Vue 3.6 RC 特性）。** 新的 SFC 编译模式，**编译期把模板转为直接 DOM 操作、跳过 VDOM diff**，目标是降低基线包体积并提升性能。100% opt-in，仅需在 SFC 的 `<script setup>` 上加 `vapor` 属性（`<script setup vapor>`）即可启用；官方称在第三方基准测试中性能与 Solid、Svelte 5 相当。

**2. VDOM 互操作。** 纯 Vapor 应用用 `createVaporApp()` 可避免引入 VDOM 运行时；在 `createApp()` 中混用 Vapor 与 VDOM 组件需安装 `vaporInteropPlugin`。**Vapor 不支持** Options API、`v-memo`、`getCurrentInstance()`（返回 `null`）、`app.config.globalProperties` 等，官方建议**分区使用、尽量避免深度混合嵌套**。

**3. Vue 3.6 响应式换芯。** 官方 RC 说明指出 3.6 对 `@vue/reactivity` 做了基于 alien-signals 的重大重构，显著改善响应式系统性能与内存；Vapor 组件的**自定义指令接口也不同**——`value` 为响应式 getter，可用 `watchEffect` 建立并在卸载时自动释放。

**4. Vite 8 / Rolldown。** Rolldown 用 Rust 编写，性能与 esbuild 相当、**比 Rollup 快 10-30 倍**，支持 Rollup/Vite 插件 API，带来完整打包模式、更灵活的分块控制、模块级持久缓存与模块联邦；构建工具（Vite）、打包工具（Rolldown）、编译器（Oxc）由同一团队端到端维护，提升技术栈一致性。

**5. 构建工具 Rust 化趋势。** Oxc、Rolldown、esbuild 等 Rust 工具链正统一前端的解析/转换/打包，前端工程化向**端到端同源工具链**收敛，构建性能与一致性成为主赛道。

**6. 响应式收敛趋势（2025-2026）。** 主流框架在性能问题上向**细粒度响应式（Signals）**收敛：Vue Vapor Mode、Svelte 5 Runes、SolidJS Signals、Angular Signals；React 则以 React Compiler 在编译期自动 memoization 对应——各框架路径不同，目标一致。

**7. 跨端方案。**
- **uni-app**：以**编译时为主**，把 Vue SFC 在构建期拆解为各端 DSL；其 UniApp X/UTS 可编译为 Kotlin/Swift/ArkTS 原生代码（App / 鸿蒙端跳过 WebView，已适配鸿蒙）。
- **Taro 3+**：走**运行时方案**，在小程序逻辑层实现轻量 DOM/BOM 模拟 + 自定义 Vue/React renderer，**完整支持 Vue 运行时特性**。
- 选型核心判断：**编译时方案包体更小、端差异靠构建抹平；运行时方案对框架特性支持更完整、更新更及时**，详见 [Taro vs UniApp 横向对比](https://juejin.cn/post/7668120258260140084)。

**8. Vue 4 动向。** 生态已出现对 Vue 4 的前置兼容（vue-router 的 `peerDependencies` 已包含 `^4.0.0`，pinia 当前仍为 `^3.5.11`），但 npm `latest` 仍为 Vue 3.5.45，Vue 4 的正式发布时间与细节以官方文档为准。

> [!warning] 前沿技术的落地姿势
> Vapor Mode、Rolldown、alien-signals 都处于快速演进期。生产环境采用前先确认：依赖生态是否已适配、与现有 VDOM 组件的混合成本、以及可回滚的开关设计（如按模块灰度、按构建配置切换）。

## 五、核心要点速查

1. Vue 最新稳定版 **3.5.45（2026-11-05）**，Vue 3.6 处于 RC 阶段（npm `rc` 标签 3.6.0-rc.15）。
2. Vue3 响应式基于 **Proxy + 依赖收集（track/trigger）+ effect**；Vue 3.6 起 `@vue/reactivity` 基于 alien-signals 重构。
3. 组合式 API 以 `setup` 为入口，**`<script setup>` 是推荐语法糖**，逻辑复用靠**组合式函数（composables）**。
4. `ref` 用于基本类型、`reactive` 用于对象，**模板中 ref 自动解包**，脚本中需 `.value`。
5. `computed` 具备缓存，`watch` / `watchEffect` 用于副作用与异步操作，避免不必要的 deep watch。
6. SFC 由 `<template> + <script> + <style>` 组成；`defineProps` / `defineEmits` / `defineModel` 是**编译器宏**，无需导入。
7. `v-model` 实现双向绑定，**Vue 3.4 起支持多个 v-model**。
8. 组件通信三件套：`props`/`emits`（父子）、`provide`/`inject`（跨层）、`v-model`（双向）。
9. Vue Router 5.x：导航守卫 **`next()` 自 5.0.3 起弃用**，改为从守卫返回值（false / 路径 / 抛错）。
10. Pinia 4.x：组件外使用 store **必须在 pinia 实例激活之后**调用。
11. **Vite 8.3.8** 以 Rolldown 取代 esbuild + Rollup，生产构建显著提速。
12. **@vitejs/plugin-vue 6.0.11** 是 Vue SFC 官方 Vite 插件，兼容 Vite 5/6/7/8。
13. 编译时优化五件套：**静态提升、Block Tree、PatchFlags、事件监听缓存、v-memo**。
14. **Vapor Mode** 编译期直接操作 DOM、跳过 VDOM diff，性能对标 Solid / Svelte 5，需显式 opt-in。
15. SSR/SSG 用 `@vue/server-renderer` 或 Nuxt；**Nuxt 4.6 已支持 Vue Vapor（interop 模式）**。
16. 跨端主流：**uni-app（编译时为主，含鸿蒙原生）** 与 **Taro 3+（运行时方案，完整支持 Vue）**。
17. 类型安全：Vue 原生 TypeScript、官方包自带类型声明，配合 **vue-tsc** 做类型检查。
18. 环境要求：Vue 官方快速上手要求 **Node.js `^22.18.0 || >=24.12.0`**。
19. 2025-2026 前端趋势：**Rust 工具链（Oxc / Rolldown / esbuild）统一构建**，框架向**细粒度 Signals 响应式**收敛。

## 六、学习资源

**Vue 官方文档**

- [Vue 官方中文文档 · 快速上手](https://cn.vuejs.org/guide/quick-start.html)
- [Vue 官方中文文档 · 单文件组件 `<script setup>`](https://cn.vuejs.org/api/sfc-script-setup.html)
- [Vue 核心仓库 CHANGELOG（vuejs/core）](https://github.com/vuejs/core/blob/main/CHANGELOG.md)
- [npm vue dist-tags（latest / rc / beta / alpha）](https://registry.npmjs.org/-/package/vue/dist-tags)
- [Vue 3.6.0-rc.1 发布说明（Vapor Mode / alien-signals）](https://newreleases.io/project/npm/vue/release/3.6.0-rc.1)

**构建与元框架**

- [Vite 官方博客 · Vite 8 Beta：由 Rolldown 驱动](https://cn.vite.dev/blog/announcing-vite8-beta)
- [Nuxt 官方博客 · Nuxt 4.6](https://nuxt.com/blog/v4-6)
- [npm vite latest 版本信息](https://registry.npmjs.org/vite/latest)
- [npm @vitejs/plugin-vue latest 版本信息](https://registry.npmjs.org/@vitejs/plugin-vue/latest)

**Vue Router 与 Pinia**

- [Vue Router 官方文档](https://router.vuejs.org/)
- [npm vue-router latest 版本信息](https://registry.npmjs.org/vue-router/latest)
- [Pinia 官方文档](https://pinia.vuejs.org/zh/)
- [npm pinia latest 版本信息](https://registry.npmjs.org/pinia/latest)

**性能与跨端**

- [Vue 3 性能优化（编译与渲染优化要点）](https://developer.aliyun.com/article/1686132)
- [Taro vs UniApp：多端统一开发框架横向对比](https://juejin.cn/post/7668120258260140084)

## 七、关联笔记

- [[前端开发]] — 前端技术整体地图与目录索引
- [[HTML-CSS布局技巧]] — Flexbox / Grid / 容器查询与样式隔离
- [[Vue3-组合式API]] — 组合式 API 深入与 `<script setup>` 实践
- [[React-Hooks详解]] — 与 Vue 响应式对照学习
- [[前端性能优化]] — 渲染、打包与运行时优化方法论
- [[Webpack配置指南]] — 构建工具配置与向 Vite/Rolldown 迁移对照
- [[JavaScript-ES6新特性]] — Vue3 依赖的语言基础
- [[标签索引]] — 全库标签导航

## 八、变更记录

- 2026-11-18 首次创建
