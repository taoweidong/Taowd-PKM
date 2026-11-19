---
title: TypeScript与Vue3集成
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - TypeScript
  - Vue3
  - 类型安全
aliases:
  - Vue3 与 TypeScript 集成
  - Vue3 + TypeScript 类型方案
source: 网络资料整理
---

# TypeScript与Vue3集成

> [!摘要] 摘要
> 本文聚焦 **TypeScript 与 Vue3 的集成**这一知识点：讲清 Vue3 单文件组件（SFC）如何被类型系统理解，`vue-tsc` / Volar 的工作机制，`defineProps` / `defineEmits` / `defineModel` / `defineExpose` 的泛型与运行时声明写法，以及在 Vue 3.5.45 稳定线与 **TypeScript 7.0（Go 原生移植）** 并存的当下，如何搭建可落地、可类型检查的 Vue3 + TS 工程。定位为 [[Vue3与前端-从入门到精通]] 中「类型安全」一节的延伸实操文档，适合已掌握组合式 API、想补齐类型工程能力的开发者。

## 一、最新动态（截至 2026-11）

- **TypeScript 主线进入 7.x**：最新为 **7.0.2**（7.0 于 **2026-07-08 GA**），为 **Go 原生移植**，官方称比上一代快约 **10×**；**5.x 最新为 5.9.3**。
- **TS 7「无 JS 编译器 API」是影响集成的关键变化**：`ts.createProgram`、`ts.createSourceFile`、`ts.forEachChild` 等接口不再可用；采用 TS 6 新默认值，对 TS 6 已弃用项给出**硬错误**。过渡桥接包 **`@typescript/typescript6`**（JS API 兼容的 6.0.x 包装）供依赖 JS API 的生态使用，**TS 7.1 将提供新的、不同的 API**。
- **Volar 生态需验证兼容性**：Vue / Svelte / Astro / MDX 等**基于 Volar 的工作流在 TS 7 下需验证兼容性**，无编译器 API 可能影响类型解析与语言工具链。
- **Vue 侧类型并非完全稳定**：`vue` 的类型定义**可能在小版本之间出现不兼容**（官方说明），建议使用**锁定 minor 的 semver 范围**，并在升级时**手动升级**。
- **Vue 侧当前版本**：稳定线为 **Vue 3.5.45（2026-11-05）**，**Vue 3.6 处于 RC**（`3.6.0-rc.1`，2026-07-17）。集成方案在 3.5 / 3.6 下均可用。
- **Vite 8 对 TS 支持更内建**：Vite 8.0 内置 **`resolve.tsconfigPaths`** 与 **`emitDecoratorMetadata`**，可减少对 `vite-tsconfig-paths`、`vite-plugin-vue-decorators` 等插件的依赖。

> [!warning] 版本口径
> 以上版本号与日期来自调研基线（截至 2026-11 的官方发布说明 / npm / 官方仓库）；补丁版本日期与 TS 7.1 的 API 细节以官方仓库为准。

## 二、基础概念

**1. SFC 与 `<script setup lang="ts">`。** Vue3 用单文件组件（`.vue`，含 `<template>` / `<script>` / `<style>`）组织组件；在 `<script>` 上声明 `lang="ts"` 即开启 TypeScript，是最基本的集成入口：

```vue
<script setup lang="ts">
import { ref } from 'vue'

const count = ref<number>(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

**2. 编译器宏。** `defineProps`、`defineEmits`、`defineModel`、`defineExpose` 是**编译器宏**，由 SFC 编译器处理，**不需要（也不应）从 `vue` 导入**；`defineProps` / `defineEmits` 支持**纯类型声明**写法，编译器据此生成运行时等价声明。

**3. vue-tsc 与 Volar。** Vue 官方包自带类型声明，但**类型检查需要独立工具**：`vue-tsc` 基于 **Volar / `@vue/language-core`**，把 SFC 当作合法的 TypeScript 单元来检查，是 CI 类型门禁的标配。

**4. vueCompilerOptions。** 在 `tsconfig.json` 的 `compilerOptions.vueCompilerOptions` 中可定制语言工具行为（例如 Router 5 的 Volar 插件配置）。

**5. 双通道。** Vue 类型同时服务于编辑器（Volar 提供模板内的类型提示与跳转）与命令行检查（`vue-tsc`），二者共享同一语言服务，这是排查类型问题的基础。

## 三、核心机制

**1. Volar 的虚拟文件模型。** Volar 将 SFC **拆解为多个虚拟 TypeScript 文件**，把 `<script>` 映射为逻辑模块、把 `<template>` 映射为类型安全的渲染函数，因此模板表达式能获得类型推断与检查（组件 props、`ref` 模板引用、`$event` 等）。

**2. vue-tsc 的检查流程。** `vue-tsc` 在标准 tsc 之上接入 Volar 语言服务，遍历 `.vue` 与 `.ts`，能发现普通 tsc 查不出的模板错误，例如给组件传了不存在的 prop、模板误用未定义变量。

**3. `defineProps` 的声明方式。** 推荐**纯类型声明**，编译器自动生成运行时 props 结构；需要运行时校验（默认值、校验器）时用运行时对象声明。**不要在同一处混用两种写法**，否则类型与运行时行为不一致。

```vue
<script setup lang="ts">
const props = defineProps<{
  title: string
  count: number
  items?: string[]
}>()
</script>
```

**4. `defineEmits` 的类型化事件。** 用类型字面量描述事件签名，`emit` 的事件名与参数随之受类型约束：

```vue
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'update:title', value: string): void
  (e: 'submit', payload: { id: number }): void
}>()

emit('update:title', 'hello') // ✅
// emit('unknown', 1)          // ❌ 类型报错
</script>
```

**5. `defineModel` 与 `defineExpose`。** `defineModel` 让多模型双向绑定获得类型支持；`defineExpose` 显式声明暴露给父组件模板 ref 的成员，二者都是类型安全的宏：

```vue
<script setup lang="ts">
const model = defineModel<string>({ required: true })
const internal = ref(0)

defineExpose({ internal })
</script>
```

**6. 泛型组件。** Vue 3.3 起支持泛型 SFC，用 `<script setup lang="ts" generic="T extends ...">` 配合 `defineProps`，实现类型安全的可复用组件。

**7. TS 7 对机制的影响。** TS 7 不再暴露 JS 编译器 API，依赖 `ts.*` 的语言工具与解析类插件需重新适配。Vue / Volar 生态在 TS 7 下需**实际验证**；若工具链暂不兼容，可退回 **5.x 线（5.9.3）**，或使用桥接包 **`@typescript/typescript6`** 保留 JS API 兼容，等待 TS 7.1 的新 API 落地。

## 四、实践步骤（含代码/命令示例）

**1. 环境核对。** 先确认 Node 版本满足 Vue 官方要求：

```bash
node -v
# Vue 官方快速上手要求 ^22.18.0 || >=24.12.0
```

**2. 创建 TS 项目。** 用官方 `create-vue` 脚手架，交互式选择 TypeScript：

```bash
npm create vue@latest
cd your-project
npm install
npm run dev        # 开发，默认 http://localhost:5173
npm run build      # 生产构建
```

**3. 类型检查命令。** `create-vue` 生成的 TS 项目默认含类型检查脚本，CI 中直接调用：

```bash
npm run type-check   # 通常为 vue-tsc --noEmit
```

**4. tsconfig 关键配置。** 至少覆盖源码目录并配置路径别名，保证 `vue-tsc` 正常工作：

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "jsx": "preserve",
    "noEmit": true,
    "types": ["vite/client"],
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.vue"],
  "exclude": ["node_modules", "dist"]
}
```

**5. Vite 侧别名解析（Vite 8）。** Vite 8 内置 tsconfig paths 解析，可在 `vite.config.ts` 中开启，免去 `vite-tsconfig-paths` 插件：

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    tsconfigPaths: true, // Vite 8 内置，默认关闭，有性能成本
  },
})
```

**6. 一个完整的类型安全组件。** 综合展示 `defineProps`、`defineEmits`、`defineModel`、`defineExpose`：

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{ label: string; items: string[] }>()
const emit = defineEmits<{ (e: 'select', index: number): void }>()
const model = defineModel<string>({ required: true })
const selected = ref<number>(-1)

const summary = computed(() => `${props.label}（${props.items.length} 项）`)

function onClick(index: number) {
  selected.value = index
  emit('select', index)
  model.value = props.items[index]
}

defineExpose({ selected, summary })
</script>

<template>
  <div>
    <span>{{ summary }}</span>
    <input v-model="model" />
    <ul>
      <li v-for="(item, i) in items" :key="i" @click="onClick(i)">{{ item }}</li>
    </ul>
  </div>
</template>
```

**7. 类型安全的 composable。** 用泛型与显式返回类型约束，避免类型丢失：

```typescript
import { ref, computed, type Ref } from 'vue'

export function useCounter(initial: number) {
  const count: Ref<number> = ref(initial)
  const double = computed(() => count.value * 2)
  const inc = () => count.value++
  return { count, double, inc }
}
```

## 五、最佳实践与常见坑

**最佳实践**

- **锁定 `vue` 的 minor 版本**：官方类型可能小版本间不兼容，依赖声明写成锁定 minor 的 semver 范围，升级时**手动升级并跑 `vue-tsc`**。
- **类型检查进 CI**：流水线执行 `vue-tsc --noEmit`，把模板与脚本的类型错误挡在合并前。
- **优先纯类型声明**：`defineProps` / `defineEmits` 优先用类型字面量写法，编译器自动生成运行时等价物，减少重复维护。
- **纯类型导入用 `import type`**：区分类型导入与值导入，避免歧义。
- **Vite 8 优先用内置能力**：路径别名用 `resolve.tsconfigPaths`，装饰器元数据用 `emitDecoratorMetadata`，减少第三方插件。

**常见坑**

- **TS 7 下工具链不兼容**：`vue-tsc` / Volar 若出现类型解析异常，先确认工具链是否已适配 TS 7；必要时退回 **TS 5.9.3** 或使用 **`@typescript/typescript6`** 桥接，不要在生产项目上盲升。
- **混用 `defineProps` 的两种声明**：同一宏内同时写类型声明与运行时声明，会导致类型与校验不一致，应二选一。
- **误以为「有 TS 就自动检查模板」**：`.vue` 的类型错误**不会**被普通 `tsc` 检查到，必须用 `vue-tsc`，否则模板里传错 props 也能通过。
- **模板里写复杂 TS**：模板表达式只支持有限语法，复杂逻辑应放到 `<script setup>` 的函数或 `computed` 中。
- **解构 `reactive` 丢响应性**：`const { count } = reactive({ count: 0 })` 会失去响应性，用 `toRefs` 或 `ref` / `computed`。
- **Vapor 场景差异**：Vue 3.6 Vapor（RC）下 `getCurrentInstance()` 返回 `null`，模板 ref 不暴露 `$el` / `$props` / `$attrs` / `$slots` / `$refs`，类型推导路径与 VDOM 不同，需单独验证。

## 六、核心要点速查

1. Vue3 + TS 入口为 `<script setup lang="ts">`，`vue` 官方包自带类型声明。
2. **TS 主线 7.0.2**（Go 原生、2026-07-08 GA），**5.x 最新 5.9.3**；TS 7 **无 JS 编译器 API**。
3. TS 7 采用 TS 6 新默认值并对弃用项给硬错误；过渡用 **`@typescript/typescript6`**，**TS 7.1** 提供新 API。
4. 类型检查用 **`vue-tsc`**（基于 Volar / `@vue/language-core`），模板错误只有它能查出。
5. **Volar** 把 SFC 拆为虚拟 TS 文件，实现模板内类型推断与跳转。
6. `defineProps` / `defineEmits` / `defineModel` / `defineExpose` 是**编译器宏，无需导入**。
7. 优先用**纯类型声明**写宏，编译器自动生成运行时声明。
8. **Vue 类型可能小版本不兼容**，锁定 minor 范围，升级时手动升级并跑 `vue-tsc`。
9. 泛型组件用 `<script setup lang="ts" generic="...">`。
10. **Vite 8** 内置 `resolve.tsconfigPaths` 与 `emitDecoratorMetadata`。
11. 纯类型导入用 `import type`；`vue-tsc --noEmit` 进 CI 做类型门禁。
12. Vapor（Vue 3.6 RC）下 `getCurrentInstance()` 返回 `null`，类型推导路径不同，生产采用前需验证。

## 七、学习资源

**官方与权威**

- [Vue 官方中文文档 · 快速上手](https://cn.vuejs.org/guide/quick-start.html)
- [Vue 官方中文文档 · 单文件组件 `<script setup>`](https://cn.vuejs.org/api/sfc-script-setup.html)
- [Vue 核心仓库 CHANGELOG（vuejs/core）](https://github.com/vuejs/core/blob/main/CHANGELOG.md)
- [Vue 3.6.0-rc.1 发布说明（Vapor Mode / alien-signals）](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)
- [TypeScript 官方博客（版本与发布说明）](https://devblogs.microsoft.com/typescript/)
- [TypeScript 5.9 发布说明](https://devblogs.microsoft.com/typescript/announcing-typescript-5-9/)

**构建与工具链**

- [Vite 官方博客 · Vite 8：由 Rolldown 驱动](https://vite.dev/blog/announcing-vite8.html)
- [Vue Router 官方迁移指南 · v4 到 v5](https://router.vuejs.org/guide/migration/v4-to-v5.html)

**Vue Router 与 Pinia**

- [Vue Router 官方文档](https://router.vuejs.org/)
- [Pinia 官方文档（中文）](https://pinia.vuejs.org/zh/)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本知识点所属的体系总览，类型安全是其「进阶 / 生产实践」的一部分
- [[Vue3-组合式API]] — `<script setup>` 与组合式 API 基础，是理解类型宏的前提
- [[JavaScript-ES6新特性]] — TypeScript 所依赖的语言基础
- [[前端开发]] — 前端技术整体地图与目录索引

## 九、变更记录

- 2026-11-19：首次创建。
