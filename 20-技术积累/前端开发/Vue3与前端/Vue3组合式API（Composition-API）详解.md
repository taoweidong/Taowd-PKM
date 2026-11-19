---
title: Vue3 组合式 API（Composition API）详解
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - 组合式API
  - 响应式
  - Composition-API
aliases:
  - Vue3 组合式 API 详解
  - Vue3 Composition API 详解
source:
  - 网络资料整理
---

# Vue3 组合式 API（Composition API）详解

> [!摘要] 摘要
> 本文聚焦 Vue3 的**组合式 API（Composition API）**：从它的定义、设计动机与与 Options API 的边界，讲到 `ref` / `reactive` / `computed` / `watch` / 生命周期 / 组合式函数 / `provide`·`inject` 等核心机制，并给出 `<script setup>` 的完整可运行示例、最佳实践与常见坑。版本口径截至 **2026-11**，组合式 API 自 **Vue 3.0** 起稳定，**`<script setup>`** 是官方推荐的编写风格，也是 [[Vue3与前端-从入门到精通]] 中「入门篇」的核心范式。

## 一、最新动态（截至 2026-11）

- **版本口径**：当前稳定线为 **Vue 3.5.45**（2026-11-05 发布）；同时 **Vue 3.6 已进入 RC**（`3.6.0-rc.1`，2026-07-17），核心是 Vapor Mode 功能完成与 `@vue/reactivity` 基于 alien-signals 的响应式大重构。**3.6 仍未进入稳定版**，生产项目应锁定 3.5.x。
- **组合式 API 本身已稳定**：组合式 API 自 **Vue 3.0** 起即为正式稳定能力，**`<script setup>`** 是官方推荐的编写风格，无需等待 3.6。
- **3.5 带来的组合式相关变化**：3.5 首发于 2024-09-03，其中 **reactive props 解构默认开启**（`reactive props destructure`）；新增 **`useTemplateRef()`** 用于获取模板 ref；新增 **`app.onUnmount()`** 应用级卸载回调。
- **3.5 新增的副作用清理 API**：`onEffectCleanup`、`onWatcherCleanup`、`getCurrentWatcher`，且 `watch` / `effect` 支持暂停与恢复。
- **与 Vapor Mode 的关系**：Vapor Mode **不支持 Options API**，组合式 API 是 Vapor 组件的**唯一选择**；`getCurrentInstance()` 在 Vapor 组件中返回 `null`。
- 以上版本号与日期均来自 [vuejs/core 发布说明](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1) 与 [Vue 官方发布页](https://vuejs.org/about/releases)，正式版时间以官方仓库为准。

## 二、基础概念

**组合式 API** 是 Vue3 提供的一套按**逻辑关注点（而不是选项类型）**组织组件代码的写法。Options API 把逻辑拆进 `data` / `methods` / `computed` / `watch` 等分散的选项，而组合式 API 允许把**相关的状态与逻辑聚合到一个 `setup()` 函数中**，更便于按功能抽取复用。

三个关键概念：

- **`setup()` 入口**：组件实例创建前执行，是组合式 API 的入口，返回值或顶层声明的绑定会自动暴露给模板。
- **`<script setup>` 语法糖**：编译器把顶层声明自动绑定到模板，省略了手动 `return`，是**官方推荐的写法**，配合 `lang="ts"` 可获得完整类型推导。
- **组合式函数（Composables）**：把一段可复用逻辑封装为以 `use` 开头的普通函数（如 `useMouse`、`useFetch`），用于替代 mixins，是组合式 API 复用能力的载体。

**与 Options API 的对比**：

| 维度 | Options API | 组合式 API |
| --- | --- | --- |
| 组织方式 | 按选项类型分散（`data`/`methods`/`computed`） | 按逻辑关注点聚合在 `setup` 中 |
| 逻辑复用 | `mixins`，易冲突、来源不清晰 | 组合式函数，可显式传参、类型安全 |
| TypeScript | 类型推导需额外成本 | 原生友好，`defineProps` 可用纯类型声明 |
| 与 Vapor 兼容 | 不支持 | 唯一选择 |

组合式 API 与 Options API **长期并存**，可在同一项目中混用；但新代码、尤其是面向 Vapor 的代码应优先使用组合式 API。

## 三、核心机制

**1. 响应式基座。** 组合式 API 的底层仍是 Vue3 基于 **Proxy** 的响应式系统：读取属性时执行依赖收集（`track`），修改时触发更新（`trigger`），并通过 `effect` / `ReactiveEffect` 把状态与视图副作用关联起来。Vue 3.5 用**版本计数 + 双向链表**重写追踪结构，3.6 起 `@vue/reactivity` 基于 alien-signals 重构，性能与内存进一步改善。

**2. 核心响应式 API。**

- `ref`：包装基本类型，脚本中通过 `.value` 读写，**模板中自动解包**；
- `reactive`：代理对象/数组，直接访问即响应；
- `computed`：带缓存的派生状态，仅在依赖变化时重新计算；
- `watch` / `watchEffect`：观察变化并执行副作用，`watchEffect` 会立即执行一次并自动追踪依赖。

**3. 生命周期。** 组合式版生命周期钩子与 Options API 一一对应：`onMounted`、`onUpdated`、`onUnmounted`、`onBeforeUnmount` 等，必须在 `setup()` 同步上下文中调用。

**4. 组合式函数。** 组合式函数内部调用响应式 API 即可共享响应性；需要访问组件实例时使用 `getCurrentInstance()`，但在 Vapor 组件中它返回 `null`。

**5. 依赖注入。** `provide` / `inject` 用于跨层级传递数据或方法，避免逐层透传 props。

**6. 编译器宏。** `defineProps` / `defineEmits` / `defineModel` / `defineExpose` 是**编译器宏，无需 import**，`<script setup>` 顶层直接使用。

## 四、实践步骤（含代码/命令示例）

**1. 环境准备。**

```bash
# 官方脚手架要求 Node.js ^22.18.0 || >=24.12.0，先核对版本
node -v
npm create vue@latest          # 交互式创建 Vite + Vue3 项目（可选 TypeScript）
npm install
npm run dev                    # 本地开发，默认 http://localhost:5173
```

**2. 最小可运行示例：`<script setup>` + 响应式 + 组合式函数。**

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useMouse } from './composables/useMouse'

const keyword = ref('')
const todos = ref<string[]>(['学习 Vue3 组合式 API', '配置 Vite 工程化'])

// computed：带缓存的派生状态
const remaining = computed(() => todos.value.length)

// watch：副作用（可控制深度，3.5 起 deep 支持传数字）
watch(remaining, (n) => console.log('剩余待办：', n))

// 组合式函数：把鼠标位置逻辑抽离复用
const { x, y } = useMouse()

onMounted(() => console.log('组件已挂载'))
onUnmounted(() => console.log('组件已卸载'))

function addTodo() {
  if (!keyword.value.trim()) return
  todos.value.push(keyword.value)
  keyword.value = ''
}
</script>

<template>
  <input v-model="keyword" placeholder="输入待办，回车添加" @keyup.enter="addTodo" />
  <p>剩余：{{ remaining }}，鼠标：{{ x }}, {{ y }}</p>
  <ul>
    <li v-for="(todo, i) in todos" :key="todo + i">{{ todo }}</li>
  </ul>
</template>
```

**3. 组合式函数示例 `useMouse.ts`（演示响应性共享）。**

```typescript
import { ref, onUnmounted } from 'vue'

export function useMouse() {
  const x = ref(0)
  const y = ref(0)
  const update = (e: MouseEvent) => {
    x.value = e.clientX
    y.value = e.clientY
  }
  window.addEventListener('mousemove', update)
  onUnmounted(() => window.removeEventListener('mousemove', update))
  return { x, y }
}
```

**4. 依赖注入示例。**

```vue
<script setup lang="ts">
import { provide, inject, ref, type InjectionKey } from 'vue'

const theme = ref<'light' | 'dark'>('light')
provide<InjectionKey<typeof theme>>('theme', theme)
</script>
```

子组件中 `const theme = inject<typeof theme>('theme')` 即可取用，无需逐层传 props。

## 五、最佳实践与常见坑

- **ref 与 reactive 分清**：基本类型用 `ref`，对象/数组用 `reactive`；脚本里 `ref` 要写 `.value`，模板里自动解包。
- **不要解构 reactive**：解构会丢失响应性，应使用 `toRefs` 或改用 `ref` / `computed`。
- **派生状态用 computed**：避免在模板里写复杂表达式或重复计算。
- **控制副作用边界**：`watch` / `watchEffect` 只放在必要处，谨慎使用 deep watch；需要精确控制依赖时用 `watch`，需要自动追踪时用 `watchEffect`。
- **及时清理副作用**：事件监听、定时器、订阅等在 `onUnmounted` 中释放；3.5 的 `onEffectCleanup` / `onWatcherCleanup` 可配合 `watch` 做清理。
- **列表 key 用稳定唯一值**：不要用数组索引作为动态列表的 key。
- **不要在 `<script setup>` 中混用 Options API**，保持单一范式。
- **组合式函数避免隐式依赖组件实例**：尽量只依赖传入的参数与响应式 API，减少对 `getCurrentInstance()` 的依赖（Vapor 中它返回 `null`）。
- **组件外使用 store / 注入**：如 Pinia 需先 `app.use(pinia)` 激活实例，再取 store。
- **类型安全**：优先用 `defineProps<{...}>()`、`defineEmits<{...}>()` 的纯类型写法，配合 `vue-tsc --noEmit` 做类型门禁。

**常见问题速查**：

| 现象 | 常见原因 | 处理 |
| --- | --- | --- |
| 数据改了视图不更新 | 解构 `reactive` 丢失响应性 | 用 `toRefs` 或改用 `ref` / `computed` |
| 在 `setup` 里访问 `this` 失败 | `setup` 执行于实例创建前，无 `this` | 直接用组合式写法，需要实例时用 `getCurrentInstance()` |
| `watchEffect` 重复触发 | 副作用中读取了被监听状态，形成自触发 | 拆成独立 `computed`，或用 `watch` 精确指定依赖 |
| 定时器/事件未释放 | 缺少清理逻辑 | 在 `onUnmounted` 中移除，或用 `onEffectCleanup` |
| 组件外取 store 报错 | pinia 实例尚未激活 | 先 `app.use(pinia)` 再取 store |

## 六、核心要点速查

1. 组合式 API 自 **Vue 3.0** 起稳定，`<script setup>` 是官方推荐写法。
2. 响应式基座：**Proxy + 依赖收集（track/trigger）+ effect**；3.5 重写追踪结构，3.6 基于 alien-signals 重构。
3. `ref` 用于基本类型（脚本 `.value`、模板自动解包），`reactive` 用于对象。
4. `computed` 带缓存，`watch` / `watchEffect` 负责副作用，避免无谓的 deep watch。
5. 生命周期钩子：`onMounted` / `onUpdated` / `onUnmounted` 等；3.5 新增 `app.onUnmount()`。
6. 模板引用：3.5 新增 `useTemplateRef()`。
7. 副作用清理：3.5 新增 `onEffectCleanup` / `onWatcherCleanup` / `getCurrentWatcher`，`watch` 可暂停/恢复。
8. 依赖注入：`provide` / `inject`；`getCurrentInstance()` 在 Vapor 组件中返回 `null`。
9. 编译器宏 `defineProps` / `defineEmits` / `defineModel` **无需 import**。
10. **Vapor Mode 不支持 Options API**，组合式 API 是其唯一选择；3.6 仍为 RC，生产建议锁定 3.5.x。

## 七、学习资源

- [Vue 官方中文文档 · 组合式 API 简介](https://cn.vuejs.org/guide/extras/composition-api-faq.html)
- [Vue 官方中文文档 · `<script setup>`](https://cn.vuejs.org/api/sfc-script-setup.html)
- [Vue 官方发布与版本说明](https://vuejs.org/about/releases)
- [vuejs/core 仓库 CHANGELOG](https://github.com/vuejs/core/blob/main/CHANGELOG.md)
- [Vue 3.6.0-rc.1 发布说明（Vapor Mode / alien-signals）](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)
- [Vue 官方中文文档 · 组合式函数（Composables）](https://cn.vuejs.org/guide/reusability/composables.html)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题的体系总览，定位组合式 API 在 Vue3 全家桶中的位置
- [[前端开发]] — 前端技术整体地图与目录索引
- [[React-Hooks详解]] — 与 Vue 组合式函数、响应式对照学习
- [[前端性能优化]] — 渲染、打包与运行时优化方法论
- [[HTML-CSS布局技巧]] — 组件内样式与布局基础
- [[Webpack配置指南]] — 构建工具配置与向 Vite/Rolldown 迁移对照
- [[JavaScript-ES6新特性]] — Vue3 组合式 API 依赖的语言基础
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
