---
title: 前端测试（Vitest/Playwright）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - 前端测试
  - Vitest
  - Playwright
aliases:
  - Vitest 与 Playwright 前端测试
source:
  - 网络资料整理
---

# 前端测试（Vitest/Playwright）

> [!摘要] 摘要
> 本文聚焦现代前端（尤其是 Vue3 + Vite 项目）的**测试体系与落地方法**：以 **Vitest** 承担单元 / 组件测试，以 **Playwright** 承担端到端（E2E）测试，两者共同构成「分层测试」的主力组合。内容涵盖版本动态、基础概念、核心机制、从零搭建的完整实践步骤、最佳实践与常见坑，以及核心要点速查。适合从「写完代码靠手测」过渡到「有可回归、可进 CI 的自动化测试」的前端开发者；与 [[Vue3与前端-从入门到精通]] 中的工程化、构建工具链章节配套阅读。

## 一、最新动态（截至 2026-11）

> [!info] 版本口径
> 以下版本号与发布日期来自调研基线（截至 2026-11），写作时请以官方发布说明与 npm 仓库为准。

- **Vitest 已发布 5.0**（2026-09-03），**5.1 于 2026-11-01 发布**，这一轮以**性能**为核心：内联 project 共享 Vite server、`fsModuleCache`（原实验特性，现**稳定**，可跨重跑 / 跨进程复用转换后的模块）、主进程与 worker 往返减少、vm 池复用编译代码并支持 `require(esm)`、安装体积更小。
- **Vitest 5 的破坏性 / 行为变化**：`clearMocks` **默认开启**；未 `await` 的 `resolves` / `rejects` / `toMatchFileSnapshot` **会直接失败**；`expect.poll` 超时会 reject 并传入 `AbortSignal`。运行要求提升为 **Vite ≥ 6.4.0、Node.js ≥ 22.12.0**。
- **Vitest 5 新能力**：Browser Mode 的 **Trace View**（记录每次交互 / 断言 / `page.mark` 的 DOM 快照，可逐步骤回放，支持键盘导航与 watch 实时更新）；`vi.when`（按参数为 spy 定义不同返回值，支持深比较与 `expect.any()`）；**Benchmark API 重写**（`bench` 不再是顶层导入，而是 `test()` 内的 fixture，支持 `compare` / `writeResult` / `from()`）；Locator 报错可显示 **ARIA 树**（`browser.locators.errorFormat`：`html` / `aria` / `all`），locators 默认 `strict`；mock `Temporal`（`@sinonjs/fake-timers` v15.4）；报告与附件统一写入 `.vitest/`。
- **Playwright 最新为 1.65.1**（2026-11-09）：**支持在 Bun 上运行测试**（Bun 自行转译 TS 测试文件，Playwright 不再用 Babel，需加 `--bun` 标志）；浏览器版本为 **Chromium 159.0.8154.6 / Firefox 159.0 / WebKit 27.2**；动作会等待元素脱离 `inert` 状态；Cookie 匹配遵循 **RFC 6265**；Python 侧新增定位器代码（`locator.normalize()`、`page.get_by_ref()`，配合 `aria_snapshot()` 的 `"ai"` 模式）。

来源：[Vitest 5 发布说明](https://vitest.dev/blog/vitest-5.html)、[Playwright Releases](https://github.com/microsoft/playwright/releases)、[Playwright Release Notes](https://playwright.dev/docs/release-notes)。

## 二、基础概念

**分层测试思想**：按成本与反馈速度划分测试层级，越靠下的层级越快、越廉价，越靠上的层级越接近真实、也越慢。理想的组合是「**单元 / 组件测试兜底绝大多数逻辑，E2E 只守住关键路径**」。

| 层级 | 工具 | 测什么 | 运行环境 | 反馈速度 |
| --- | --- | --- | --- | --- |
| 单元测试 | Vitest | 纯函数、工具、状态逻辑 | Node（无需浏览器） | 最快（毫秒级） |
| 组件测试 | Vitest + @vue/test-utils | 组件渲染、事件、props、emit | jsdom / happy-dom（模拟 DOM） | 快 |
| E2E 测试 | Playwright | 跨页面真实用户流程 | 真实浏览器内核 | 慢 |

**Vitest** 是与 **Vite 原生集成**的测试框架，API 设计对 Jest 用户几乎零迁移成本（`describe` / `it` / `expect` / `vi`），共享同一份 Vite 配置与转换链路，因此对 `.vue` SFC、TS、别名、环境变量等开箱即用，是 Vue3 项目单元 / 组件测试的事实选择。

**Playwright** 是现代 E2E 测试的主流方案：提供**免费并行与分片**、**真实多引擎**（Chromium / Firefox / WebKit）、**多标签与多浏览器上下文**测试，具备自动等待、Trace View、录制脚本（codegen）等能力，近期还侧重 agent 驱动测试方向。

**关键术语**：`fixture`（测试夹具，如 Playwright 的 `page`、Vitest 的 `bench`）；`mock` / `spy`（替换实现或监听调用）；`snapshot`（快照比对）；`locator`（元素定位器，Playwright / Vitest Browser Mode 共用概念）；`trace`（失败现场回放）。

## 三、核心机制

**Vitest 的运行机制**：Vitest 复用 Vite 的**开发服务器与转换管线**，在 Node 的 module runner 中加载并执行测试文件，因此「构建工具怎么解析，测试就怎么解析」，无需额外配置即可处理 `.vue`、TS、路径别名等。Vitest 5 的关键优化是**缓存层**：`fsModuleCache` 稳定后，转换过的模块可在多次重跑、多个进程间复用，显著降低重复转换成本；内联 project 共享 Vite server，减少主进程与 worker 之间的往返。Vitest 还支持 **Browser Mode**（在真实浏览器中跑测试，可视为轻量 E2E，与 Playwright 的 Trace View 能力对应），以及 `projects`（多环境 / 多配置并行）、覆盖率、快照、mock、benchmark 等能力。

**Playwright 的运行机制**：Playwright 通过**浏览器驱动协议**直接操控三套内核，测试运行器负责并行调度、重试、分片与报告。核心是**自动等待**：`getByRole` / `getByLabel` 等定位器不依赖脆弱的 CSS 选择器，断言 `expect(locator).toBeVisible()` 会自动轮询直至条件满足或超时，因此几乎不需要手写 `sleep`。其**隔离模型**是每个测试独享一个 **BrowserContext**（独立 cookie、存储、缓存），可模拟多用户、多标签，避免测试间互相污染；`trace: 'on-first-retry'` 会在重试时录制快照流，配合 Trace Viewer 回放失败现场。

**二者的关系**：Vitest 与 Playwright 并非互斥。Vitest 负责「快」的单元 / 组件 / 浏览器内组件级测试，Playwright 负责「真」的端到端流程；Vitest 的 Browser Mode 与 Playwright 能力有重叠，但定位不同——前者强调与 Vite 同构的开发体验，后者强调跨引擎的真实用户流程与可观测性。

## 四、实践步骤（含代码/命令示例）

### 4.1 安装与配置 Vitest

```bash
# 单元 / 组件测试核心依赖（二选一的 DOM 环境：jsdom 或 happy-dom）
npm install -D vitest @vue/test-utils jsdom
npm install -D happy-dom
```

`vitest.config.ts`：

```typescript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom', // 也可改为 'jsdom'
    globals: true,            // describe/it/expect 全局可用，无需逐个 import
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.{ts,vue}'],
    },
  },
})
```

### 4.2 写一个组件测试

组件 `src/components/Hello.vue`：

```vue
<script setup lang="ts">
import { ref } from 'vue'

const name = ref('Vitest')
</script>

<template>
  <p class="hello">你好，{{ name }}</p>
  <button type="button" @click="name = 'Playwright'">改名</button>
</template>
```

测试 `src/components/Hello.spec.ts`：

```typescript
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Hello from './Hello.vue'

describe('Hello.vue', () => {
  it('渲染初始文案', () => {
    const wrapper = mount(Hello)
    expect(wrapper.text()).toContain('你好，Vitest')
  })

  it('点击按钮后更新文案', async () => {
    const wrapper = mount(Hello)
    await wrapper.get('button').trigger('click')
    expect(wrapper.text()).toContain('你好，Playwright')
  })

  it('可以替换外部模块的实现', () => {
    vi.mock('../api/user', () => ({
      fetchUser: () => Promise.resolve({ name: 'mock-user' }),
    }))
    // 断言被替换的实现被调用
    expect(vi.isMockFunction(vi.fn())).toBe(true)
  })
})
```

`package.json` 中的脚本：

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

```bash
npm run test               # 运行一次并退出
npm run test:watch         # 监听模式，改动即重跑
npx vitest run --coverage  # 输出覆盖率报告
```

### 4.3 安装与配置 Playwright

```bash
npm install -D @playwright/test
npx playwright init           # 生成 playwright.config.ts 与示例测试
npx playwright install        # 下载 Chromium / Firefox / WebKit 内核
npx playwright test           # 运行全部 E2E 测试
npx playwright test --headed  # 显示浏览器窗口，本地调试
npx playwright test --ui      # 可视化调试界面
npx playwright codegen https://example.com   # 录制操作生成测试脚本
```

`playwright.config.ts`：

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
})
```

E2E 测试 `e2e/login.spec.ts`：

```typescript
import { test, expect } from '@playwright/test'

test('登录成功后展示用户名', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('账号').fill('admin')
  await page.getByLabel('密码').fill('123456')
  await page.getByRole('button', { name: '登录' }).click()
  await expect(page.getByText('欢迎，admin')).toBeVisible()
})
```

### 4.4 接入 CI

```yaml
# .github/workflows/test.yml
name: test
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npx vitest run --coverage

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
```

## 五、最佳实践与常见坑

**分层与取舍**

- 把 80% 的用例放在单元 / 组件层：逻辑、计算、渲染行为由 Vitest 快速覆盖；E2E 只保留「登录 → 下单 → 支付」这类**跨页面、跨模块的关键业务路径**。全量 E2E 会让 CI 又慢又脆。
- 组件测试只验证「用户能看到 / 能操作的结果」（文案、class、事件效果），**不要断言内部实现细节**（如私有变量、内部函数调用次数），否则重构会带崩测试。

**Vitest 专属坑**

- **版本门槛**：Vitest 5 要求 **Vite ≥ 6.4.0、Node ≥ 22.12.0**，升级前先核对依赖，否则安装或运行直接报错。
- **`clearMocks` 默认开启**（Vitest 5）：`beforeEach` 中若仍手动清 mock，注意与默认行为叠加；依赖 mock 残留来「兜底」的用例会失效。
- **断言必须 `await`**：未 `await` 的 `resolves` / `rejects` / `toMatchFileSnapshot` 在 Vitest 5 中会**直接失败**，这是把「偶发通过」变成「稳定失败」的常见原因，修正方式是补 `await`。
- **DOM 环境选择**：`jsdom` 更接近浏览器、兼容性好但略慢；`happy-dom` 更快、更省资源。对兼容性敏感的组件测试优先 `jsdom`，追求速度可 `happy-dom`。
- **异步更新要等**：Vue 的更新是异步的，`trigger('click')` 后必须 `await`，必要时用 `flushPromises()` 或 `nextTick()` 再断言。
- **快照别滥用**：快照只适合「结构稳定、用于防回归」的输出；频繁改动的组件会陷入「快照天天更新、失去意义」的循环，这类场景改用显式断言。

**Playwright 专属坑**

- **定位器优先级**：优先 `getByRole` → `getByLabel` → `getByText` → `getByTestId`，最后才是 CSS / XPath。语义化定位既抗样式调整，又天然享受无障碍（ARIA）语义。
- **不要手写等待**：避免 `page.waitForTimeout(1000)` 这类固定等待，一律用定位器 + 自动等待的断言（`expect(...).toBeVisible()`），否则在慢机器上必然超时、在快机器上浪费时间。
- **开启隔离，避免共享状态**：每个测试用独立 `BrowserContext`，不要跨用例复用同一个 `page` 或登录态；依赖登录态的用例用存储态（`storageState`）或在用例内自建。
- **trace 按需开启**：`trace: 'on-first-retry'` 比 `'always'` 更省开销，失败时仍能拿到完整回放；需要排查偶发问题时再临时改为 `'always'`。
- **浏览器内核版本随包**：升级 `@playwright/test` 会附带新内核版本，CI 必须执行 `npx playwright install --with-deps`，否则缺少系统依赖或内核不匹配。
- **`webServer` 复用**：本地调试设 `reuseExistingServer: true`（或上面的 `!process.env.CI`），避免端口被占用导致失败。

**通用建议**：测试与实现同步修改，CI 中设类型与测试双重门禁；测试失败先看「是断言写错、环境问题，还是真的回归」，不要急于改断言。

## 六、核心要点速查

1. **分层定位**：Vitest 负责单元 / 组件测试（与 Vite 同构、API 近似 Jest、与 Vue 深度集成）；Playwright 是现代 E2E 默认，提供免费并行/分片与真实多引擎。
2. **版本基线（截至 2026-11）**：Vitest **5.0**（2026-09-03，**5.1** 于 2026-11-01）；Playwright **1.65.1**（2026-11-09）。
3. **Vitest 5 要求**：**Vite ≥ 6.4.0、Node ≥ 22.12.0**。
4. **Vitest 5 关键变化**：`fsModuleCache` 稳定、内联 project 共享 Vite server、Browser Mode **Trace View**、`vi.when`、Benchmark API 重写、Locator 报错可显示 ARIA 树。
5. **Vitest 5 行为变化**：`clearMocks` **默认开启**；未 `await` 的 `resolves` / `rejects` / `toMatchFileSnapshot` **直接失败**。
6. **Playwright 1.65.1 关键变化**：**支持 Bun 运行（需 `--bun`）**；Chromium 159.0.8154.6 / Firefox 159.0 / WebKit 27.2；动作等待元素脱离 `inert`；Cookie 匹配遵循 RFC 6265。
7. **Vitest 组件测试三件套**：`mount` + `@vue/test-utils` + DOM 环境（`jsdom` / `happy-dom`），异步断言务必 `await`。
8. **Playwright 定位器优先级**：`getByRole` > `getByLabel` > `getByText` > `getByTestId` > CSS/XPath。
9. **Playwright 自动等待**：用 `expect(locator).toBeVisible()` 轮询，禁止固定 `sleep`。
10. **隔离模型**：Playwright 每个用例独享 `BrowserContext`；Vitest 避免用例间共享可变状态。
11. **观测与重试**：Playwright 用 `trace: 'on-first-retry'` + Trace Viewer 回放失败现场；CI 中设置 `retries` 与 `forbidOnly`。
12. **CI 要点**：`vitest run --coverage` 做单元门禁；`npx playwright install --with-deps` 后再跑 E2E。

## 七、学习资源

**Vitest**

- [Vitest 官方文档](https://vitest.dev/)
- [Vitest 5 发布说明（性能与破坏性变更）](https://vitest.dev/blog/vitest-5.html)
- [Vue Test Utils 官方文档（组件测试挂载与断言）](https://test-utils.vuejs.org/)
- [Vitest 配置参考](https://vitest.dev/config/)

**Playwright**

- [Playwright 官方文档](https://playwright.dev/)
- [Playwright Release Notes（版本与浏览器内核对应）](https://playwright.dev/docs/release-notes)
- [Playwright Releases（GitHub 发布记录）](https://github.com/microsoft/playwright/releases)
- [Playwright 测试教程（含定位器与断言最佳实践）](https://playwright.dev/docs/writing-tests)
- [Playwright Trace Viewer（失败回放）](https://playwright.dev/docs/trace-viewer)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题总览，前端测试在 Vue3 工程体系中的位置
- [[前端开发]] — 前端技术整体地图与目录索引
- [[Vue3组合式API（Composition-API）详解]] — 被测组件的逻辑基础，组件测试的直接对象
- [[Vite构建工具原理与配置]] — Vitest 与 Vite 同构运行，理解构建链路有助于配置测试
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
