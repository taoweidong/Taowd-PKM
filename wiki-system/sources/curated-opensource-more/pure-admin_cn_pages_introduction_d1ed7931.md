---
source: "https://pure-admin.cn/pages/introduction/"
title: "介绍 | Pure Admin 官方文档"
fetched_at: "2026-10-05 15:37:11"
---

[ Max-Js 版本  ](https://pure-admin.cn/pages/service/#max-js-版本) [ Max-Ts 版本  ](https://pure-admin.cn/pages/service/#max-ts-版本)

目录

# ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAABGpJREFUSA3tVVtoXFUU3fvOI53UlmCaKIFmwEhsE7QK0ipFEdHEKpXaZGrp15SINsXUWvBDpBgQRKi0+KKoFeJHfZA+ED9KKoIU2gYD9UejTW4rVIzm0VSTziPzuNu1z507dibTTjL4U/DAzLn3nL3X2o91ziX6f9wMFdh6Jvbm9nNSV0msViVO6tN1Rm7NMu2OpeJ9lWBUTDxrJbYTS0hInuwciu9eLHlFxCLCZEk3MegsJmZ5K/JD6t7FkFdEvGUo1g7qJoG3MHImqRIn8/nzY1K9UPKKiJmtnUqHVE3Gbuay6vJE/N2FEmuxFjW2nUuE0yQXRRxLiTUAzs36zhZvOXJPdX850EVnnLZkB8prodQoM5JGj7Xk2mvC7JB8tG04Ef5PiXtG0UtxupRQSfTnBoCy554x18yJHI6I+G5Eru4LHmPJZEQsrvPUbMiA8G/WgMK7w7I+ez7++o2ANfbrjvaOl1tFMs+htG3IrZH9/hDX1Pr8Tc0UvH8tcX29KzAgIGcEkINyW5BF9x891hw6VYqgJHEk0huccS7vh3C6gTiODL+26huuBtbct8eZnqLML8PkxGYpuPZBqtqwkSjgc4mB5gbgig5i+y0UDK35LMxXisn9xQtK+nd26gTIHsHe/oblK/b29fUmN/8Y+9jAQrnBp56m1LcDlDp9irKTExSKduXJVWSqdBMA08pEJnEIOB3FPPMybu/oeV8zFeYN3xx576Q6RH+VmplE4ncQV5v+5rzSoyOU7PuEAg8g803PwBJ0CExno/jcMbN8tONYeOmHiuUNryvm3fRUy4tMPVLdAGkUhNWuggGrJcXPv+ouCjz0MKUHz1J2/E8IC9nqTabcxgaBYM0hPhD5Y65FsbxRQKxCQrDjDctW7PUM3HuZunFyifSAqEfuzCp48Il24luWUWZoyJCaPR82jE0+kFA643wRFVni4RYSq3ohJO2pZ7B5dO4xkDWbEpossJPLSrPjYID8rS2UHTlvyNxqIGsg674XJJ7vnh5L7PNwC4hh2sjCI96mzszOTpxLF0T7l88Yz7lAuK6OnL8gXLOnTvpzSb22YG8W7us3jSebFHeeqnXRG1vt+MoUM84LQIBmMsCTAcOauTh0T0l0neQK7m2bLMt2mGxU3HYssS0J2cdv5wljlPsrIuZLAG/2DOZIXgCYT8uMGZN+e2kSirfxZOPCsC0f24nTZzspnVn9VePS1Z5vubmAGGXG8ZFno9Hel0yfA5ZPhF7Dh972BQJ2qCpgH67lmWtBYbvk6sz02wjky2vXyz0XErP/kFB619js1BtwfOV4OPRqOQBjy3Qbk18vigUPPSD5ceHnwck7W9bhAqZdd7SuG7w4/P2F/GaJh8c7e9qgow+Q7cGBo+98WsLkuktFqiZabtXuQTu/Y5ETbR0v7tNSFnvrmu6pjdoan2KjMu8q/Hmj1EfCO2ZGfEIbIXKUlw8qaX9/b2oeSJmFksSeT/Fn0V3nSypChh4Gjh74ybO9aeZ/AN2dwciu2/MhAAAAAElFTkSuQmCC)介绍

[vue-pure-admin (opens new window)](https://github.com/pure-admin/vue-pure-admin) 是一款开源完全免费且开箱即用的中后台管理系统模版。完全采用 `ECMAScript` 模块（`ESM`）规范来编写和组织代码，使用了最新的 `Vue3`、`Vite`、`Element-Plus`、`TypeScript`、`Pinia`、`Tailwindcss` 等主流技术开发

## # 在线预览

  * [vue-pure-admin 完整版 (opens new window)](https://pure-admin.github.io/vue-pure-admin/#/login)
  * [vue-pure-admin-max 版 (opens new window)](https://pure-admin.github.io/vue-pure-admin-max/#/login)
  * [pure-admin-thin 精简版 (opens new window)](https://pure-admin-thin.netlify.app/#/login)
  * [max-ts 版 (opens new window)](https://xiaoxian521.github.io/thin-max-ts-i18n/#/login)
  * [max-js 版 (opens new window)](https://xiaoxian521.github.io/thin-max-js-i18n/#/login)

## # 完整版本

  * [点我查看完整版本 (opens new window)](https://github.com/pure-admin/vue-pure-admin)

## # 精简版本（提供国际化和非国际化两个版本）

精简版是基于 [vue-pure-admin (opens new window)](https://github.com/pure-admin/vue-pure-admin) 提炼出的架子，包含主体功能，更适合实际项目开发，打包后的大小在全局引入 [element-plus (opens new window)](https://element-plus.org) 的情况下仍然低于 `2.3MB`，并且会永久同步完整版的代码。开启 `brotli` 压缩和 `cdn` 替换本地库模式后，打包大小低于 `350kb`

  * [点我查看国际化精简版 (opens new window)](https://github.com/pure-admin/pure-admin-thin/tree/i18n)
  * [点我查看非国际化精简版 (opens new window)](https://github.com/pure-admin/pure-admin-thin)

## # `js` 版本

  * [点我查看 js 版本](/pages/service/#js-版本)

## # `max` 版本

  * [点我查看 max 版本](/pages/service/#max-版本)

## # `max-ts` 版本

  * [点我查看 max-ts 版本](/pages/service/#max-ts-版本)

## # `max-js` 版本

  * [点我查看 max-js 版本](/pages/service/#max-js-版本)

## # 微前端版本

  * [点我查看微前端版本 (opens new window)](https://github.com/pure-admin/pure-admin-micro)

## # Nodejs 后端

平台提供一套 `node`、`mysql` 版本的后端代码，内置各种接口示例和 `jwt token` 以及 `websocket`，可供学习参考

  * [点我查看 nodejs 后端代码 (opens new window)](https://github.com/pure-admin/pure-admin-backend)

## # Tauri 版本

`tauri` 比 `electron` 更强，[tauri 与 electron 的对比 (opens new window)](https://www.cnblogs.com/Grewer/p/12789261.html)
如果没有安装 `tauri` ，请阅读 [tauri 中文官方文档 (opens new window)](https://tauri.app/zh/)

  * [点我查看 Tauri 版 (opens new window)](https://github.com/pure-admin/tauri-pure-admin)

## # Electron 版本

  * [点我查看 Electron 版 (opens new window)](https://github.com/pure-admin/electron-pure-admin)

## # 配套视频

  * **教程**

<https://www.bilibili.com/video/BV1kg411v7QT/>[ (opens new window)](https://www.bilibili.com/video/BV1kg411v7QT/)

  * **UI 设计**

<https://www.bilibili.com/video/BV17g411T7rq>[ (opens new window)](https://www.bilibili.com/video/BV17g411T7rq)

## # 浏览器支持

本地开发推荐使用 `Chrome`、`Edge`、`Firefox` 浏览器，作者常用的是最新版 `Chrome` 浏览器
实际使用中感觉 `Firefox` 在动画上要比别的浏览器更加丝滑，只是作者用 `Chrome` 已经习惯了，看个人爱好选择吧
更详细的浏览器兼容性支持请看 [Vue 支持哪些浏览器？ (opens new window)](https://cn.vuejs.org/about/faq.html#what-browsers-does-vue-support) 和 [Vite 浏览器兼容性 (opens new window)](https://cn.vitejs.dev/guide/build#browser-compatibility)

[![ Edge](/img/support/edge_48x48.png) (opens new window)](http://godban.github.io/browsers-support-badges/)
IE | [![ Edge](/img/support/edge_48x48.png) (opens new window)](http://godban.github.io/browsers-support-badges/)
Edge | [![Firefox](/img/support/firefox_48x48.png) (opens new window)](http://godban.github.io/browsers-support-badges/)
Firefox | [![Chrome](/img/support/chrome_48x48.png) (opens new window)](http://godban.github.io/browsers-support-badges/)
Chrome | [![Safari](/img/support/safari_48x48.png) (opens new window)](http://godban.github.io/browsers-support-badges/)
Safari
---|---|---|---|---
不支持 | 最后两个版本 | 最后两个版本 | 最后两个版本 | 最后两个版本

## # 维护者

[xiaoxian521 (opens new window)](https://github.com/xiaoxian521)、[Ten-K (opens new window)](https://github.com/Ten-K)

## # 问题反馈

发送问题至平台唯一网易邮箱账号 `[[email protected]](/cdn-cgi/l/email-protection)`

## # 解答微信群

[点我查看解答微信群](/pages/service/#解答微信群)

上次更新: 2026/07/25, 03:37:13

[快速开始](/pages/start/)

[快速开始](/pages/start/)→

[最近更新](/archives/)


[更多文章>](/archives/)
