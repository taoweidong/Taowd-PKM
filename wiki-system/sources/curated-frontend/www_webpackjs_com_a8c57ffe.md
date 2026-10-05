---
source: "https://www.webpackjs.com/"
title: "webpack | webpack中文文档 | webpack中文网"
fetched_at: "2026-10-05 15:32:12"
---

#  构建你的

assets  scripts

静态资源 .png .css .jpg .js 模块依赖 .jpg .png .sass .sass .js .sass .cjs .hbs .js

## 编写代码

**src/index.js**


     import bar from './bar.js';

    bar();

**src/bar.js**


     export default function bar() {

    }

## 构建

**[不使用配置](https://youtu.be/3Nv9muOkb6k?t=21293)** 或提供自定义的 **webpack.config.js**


     const path = require('path');

    module.exports = {
      entry: './src/index.js',
      output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
      },
    };

**page.html**


     <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        ...
      </head>
      <body>
        ...

      </body>
    </html>

在控制台运行 `webpack` 命令，生成 `bundle.js`。

## 深入学习

**[快速开始](/guides/getting-started)**部分在** 指南**章节，如果有兴趣深入学习，可以查阅 **[概念](/concepts)** 章节，以了解 webpack 的核心概念以及底层实现。
