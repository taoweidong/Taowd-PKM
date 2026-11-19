---
title: Vue3响应式系统原理
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - 响应式
  - 核心原理
aliases:
  - Vue3 响应式系统原理
source:
  - 网络资料整理
---

# Vue3响应式系统原理

> [!摘要] 摘要
> 本文系统讲解 Vue3 响应式系统的实现原理与工程用法：从 **Proxy 拦截**、**依赖收集（`track`）/ 触发（`trigger`）** 到 `ref` / `reactive` / `computed` / `watch` / `effect` / `effectScope` 的运行机制，并覆盖 Vue 3.5 与 3.6 的响应式重构要点。定位为 [[Vue3与前端-从入门到精通]] 中「进阶篇 · 核心机制」的深入展开，是理解组件渲染、性能优化与 Vapor Mode 的基础。建议先掌握 `<script setup>` 基本用法后再阅读本文。

## 一、最新动态（截至 2026-11）

以下版本与变化均来自调研基线，正式版时间与细节以官方仓库为准。

- **稳定线为 Vue 3.5.45（2026-11-05 发布）**，是 3.5 系列的最新补丁。Vue 3.5 对响应式核心做了一次重要重构：追踪结构改用 **version counting（版本计数）+ doubly-linked list tracking（双向链表跟踪）**，并优化了数组追踪；官方称内存占用与深度数组更新性能显著改善（社区资料提及内存最高下降约 56%）。
- **Vue 3.6 已进入 RC**（调研记录为 `3.6.0-rc.1`，2026-07-17）。3.6 的核心变化之一是 **`@vue/reactivity` 基于 alien-signals 大幅重构**，进一步提升性能与内存占用，并与 **Vapor Mode** 共同构成 3.6 的技术主线。**截至 2026-11 仍非稳定版**。
- **核心 API 保持稳定**：`reactive` / `ref` / `computed` / `watch` / `effect` / `effectScope` 仍是基座。Vue 3.5 起新增与响应式相关的能力：
  - `onEffectCleanup`：效果清理回调；
  - `watch` 暂停 / 恢复：`ReactiveEffect`、`EffectScope`、`WatchHandle` 支持 pause / resume；
  - `getCurrentWatcher`、`onWatcherCleanup`；
  - `onScopeDispose` 新增 `failSilently` 参数；
  - `watch` 的 `deep` 支持传数字控制深度。
- **生态背景**：响应式是 Vapor Mode 的底座，而 Vapor 截至 2026-11 仍处 RC、属 100% opt-in，生产项目建议锁定 Vue 3.5.x 稳定版。

来源：[Vue 发布说明（vuejs.org/about/releases）](https://vuejs.org/about/releases)、[Vue 3.6.0-rc.1 发布说明](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)、[vuejs/core CHANGELOG](https://github.com/vuejs/core/blob/minor/CHANGELOG.md)。

## 二、基础概念

**响应式（Reactivity）** 指：当数据变化时，依赖该数据的逻辑（渲染函数、`computed`、`watch`）能被自动、精准地重新执行，而无需开发者手写命令式更新。Vue3 的心智模型是 **「数据 → 依赖收集 → 触发更新 → 视图」**，框架在「读」与「写」两个方向上做拦截。

几个必须先厘清的角色：

| 概念 | 含义 | 典型 API |
| --- | --- | --- |
| 响应式对象 | 被代理、可被追踪的普通对象 | `reactive()` |
| 引用包装 | 为基本类型提供响应式容器 | `ref()` |
| 派生状态 | 有缓存的计算结果 | `computed()` |
| 副作用 / 效果 | 需要订阅依赖并可重新执行的函数 | `effect()`、`watch()`、渲染函数 |
| 作用域 | 统一收集 / 释放一批效果的容器 | `effectScope()` |

Vue3 用 **Proxy** 替代了 Vue2 的 `Object.defineProperty`，因此可以监听属性的**新增与删除**（`delete` / 新增 key），并能拦截数组的索引与长度变化，解决了 Vue2 的诸多局限。

## 三、核心机制

**1. `reactive`：基于 Proxy 的拦截。** `reactive(obj)` 返回一个 Proxy，拦截对象的 `get` 与 `set`（以及数组、Map/Set 等集合类型）。读取时触发**依赖收集**，写入时触发**派发更新**。

**2. 依赖收集与触发（`track` / `trigger`）。** 每个响应式属性内部维护一个依赖集合；`get` 时把「当前正在执行的效果」登记进去，`set` 时把该属性上登记的所有效果重新调度执行。核心是 `ReactiveEffect`（`effect()` 的底层实现）与调度器（scheduler）。

**3. `ref` 与 `.value` 解包。** `ref` 用一个带 `value` 属性的包装对象承载基本类型，读写 `.value` 时同样走依赖收集/触发；在模板中读取 ref 会自动解包，在脚本中必须显式写 `.value`。

**4. `computed` 的缓存。** `computed` 本质是一个带缓存的 effect：依赖不变时复用上次结果，依赖变化后标记为「脏」，在下一次读取时重新计算。

**5. `watch` 与 `watchEffect`。** `watch` 精确指定监听源，支持 `deep`、`flush: 'pre' | 'post' | 'sync'` 与 3.5 的数字深度；`watchEffect` 立即执行一次并自动追踪依赖，适合「依赖不固定」的场景。

**6. `effectScope`。** 把一组效果统一纳入作用域，作用域销毁时自动 `stop` 所有效果，避免内存泄漏，也常用于组件卸载时的清理。

**7. 批量更新与 `nextTick`。** 同一轮事件循环内的多次写操作会被合并，最终只触发一次更新；`nextTick()` 返回一个 Promise，在更新后的回调中执行。

**8. 版本演进。** Vue 3.5 用**版本计数 + 双向链表**重写追踪结构、优化数组追踪；Vue 3.6 的 `@vue/reactivity` 基于 **alien-signals** 重构，是细粒度响应式（Signals）在 Vue 中的落地。

## 四、实践步骤（含代码/命令示例）

**1. 确认环境与脚手架。**

```bash
node -v   # Vue 官方快速上手要求 Node.js ^22.18.0 || >=24.12.0
npm create vue@latest
npm install
npm run dev
```

**2. 核心 API 最小可运行示例。**

```typescript
import {
  reactive,
  ref,
  computed,
  watch,
  watchEffect,
  effect,
  effectScope,
  onScopeDispose,
} from 'vue'

// reactive：对象响应式
const state = reactive({ count: 0, list: [1, 2, 3] })

// ref：基本类型响应式，脚本中必须 .value
const double = computed(() => state.count * 2)

// watch：精确监听，支持 flush 控制时机
watch(double, (n) => console.log('double 变化：', n), { flush: 'post' })

// watchEffect：立即执行并自动收集依赖
watchEffect(() => console.log('当前 count =', state.count))

// effect：自定义副作用，可手动调度与停止
const myEffect = effect(() => {
  console.log('effect 读取 count：', state.count)
})
myEffect.run()      // 手动执行一次
myEffect.stop()     // 停止该效果，不再被触发

state.count++       // 触发上述所有依赖

// effectScope：批量收集，作用域销毁时自动清理
const scope = effectScope()
scope.run(() => {
  watch(state.count, (n) => console.log('scope 内监听：', n))
})
onScopeDispose(() => scope.stop()) // 通常放在组件 setup 中
```

**3. 自定义 `watch` 深度与清理（3.5 能力）。**

```typescript
// deep 传数字控制深度（3.5+）
watch(state, (val) => console.log('深层变化：', val), { deep: 2 })

// onEffectCleanup：在下次执行前执行上一次的清理
watchEffect((onCleanup) => {
  const timer = setTimeout(() => console.log('执行'), 1000)
  onCleanup(() => clearTimeout(timer))
})
```

## 五、最佳实践与常见坑

- **解构 `reactive` 会丢失响应性。** 解构出的是普通值，不随原对象变化。用 `toRefs` 展开，或直接用 `ref` / `computed`：

```typescript
import { reactive, toRefs } from 'vue'
const state = reactive({ count: 0 })
const { count } = state            // ❌ 丢失响应性
const { count: safeCount } = toRefs(state) // ✅ 保持响应性
```

- **`ref` 忘记 `.value`。** 脚本中读写响应式基本类型必须写 `.value`，模板中才自动解包，是新手最高频的错误。
- **避免无谓的深度响应式。** 大对象或不可变数据用 `shallowRef` / `shallowReactive` 跳过深层代理；第三方实例、图表实例用 `markRaw` 避免被代理，可显著降低开销。
- **不要滥用 deep watch。** `deep: true` 会递归遍历整个对象，开销随数据规模放大；尽量用 `computed` 收敛依赖。
- **副作用要有边界。** `watch` / `watchEffect` 应在组件或 `effectScope` 内创建，确保卸载时被 `stop`；组件外创建的效果要自行管理生命周期。
- **写操作天然批处理。** 同一事件循环内多次修改只会触发一次渲染，调试时注意不要用同步时序误判「没更新」；需要等更新完成用 `nextTick`。
- **关注 3.6 的变更。** `@vue/reactivity` 换芯后性能与内存改善，但 3.6 仍处于 RC，且 Vapor 组件对 `getCurrentInstance`、自定义指令接口等有差异；生产项目升级前应验证依赖兼容性，正式版时间以官方仓库为准。

## 六、核心要点速查

1. Vue3 响应式 = **Proxy 拦截 + 依赖收集（`track`）+ 触发（`trigger`）**，底层是 `ReactiveEffect` / `effect`。
2. `reactive` 用于对象，`ref` 用于基本类型；**模板中 ref 自动解包，脚本中写 `.value`**。
3. `computed` 有缓存，依赖变化才重算；`watch` 精确监听，`watchEffect` 自动追踪依赖并立即执行。
4. `effectScope` 统一收集 / 释放效果，是副作用边界与防泄漏的关键。
5. Vue 3.5 重构为**版本计数 + 双向链表追踪**；Vue 3.6 的 `@vue/reactivity` 基于 **alien-signals** 重构。
6. Vue 3.5 新增 `onEffectCleanup`、`watch` 暂停 / 恢复、`getCurrentWatcher`、`onWatcherCleanup`、`onScopeDispose(failSilently)`、数字深度 `deep`。
7. 同一轮事件循环多次写入只触发一次更新，用 `nextTick` 等待更新完成。
8. 解构 `reactive` 丢响应性，用 `toRefs` 修复；大对象用 `shallowRef` / `shallowReactive`，不可变实例用 `markRaw`。
9. 稳定线 **Vue 3.5.45（2026-11-05）**；Vue 3.6 处于 RC（调研记录 `3.6.0-rc.1`），以官方仓库为准。

## 七、学习资源

- [Vue 官方中文文档 · 响应式基础](https://cn.vuejs.org/guide/reactivity.html)
- [Vue 官方中文文档 · 响应式 API](https://cn.vuejs.org/api/reactivity.html)
- [Vue 官方中文文档 · 计算属性与侦听器](https://cn.vuejs.org/guide/computed.html)
- [Vue 发布说明（版本与 CHANGELOG）](https://vuejs.org/about/releases)
- [vuejs/core 仓库 CHANGELOG](https://github.com/vuejs/core/blob/minor/CHANGELOG.md)
- [Vue 3.6.0-rc.1 发布说明（alien-signals / Vapor）](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)
- [MDN · Proxy（Proxy 拦截机制基础）](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题总览与知识地图
- [[Vue3-组合式API]] — 响应式系统之上的开发范式
- [[前端开发]] — 前端技术整体地图与目录索引

## 九、变更记录

- 2026-11-19：首次创建。
