---
title: JavaScript 核心（闭包/原型/异步）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 前端开发
  - JavaScript
  - 闭包
  - 原型链
  - 异步
  - 事件循环
aliases:
  - JavaScript 核心：闭包 / 原型 / 异步
  - JS 核心三件套
source:
  - 网络资料整理
---

# JavaScript 核心（闭包/原型/异步）

> [!摘要] 摘要
> 本文是 [[Vue3与前端-从入门到精通]] 体系中的**语言地基**篇：围绕 JavaScript 三大底层机制——**闭包（Closure）**、**原型链与继承**、**异步与事件循环**展开，并延伸到模块系统（ESM / CommonJS）。目标是让读者在进入 Vue3 响应式、组合式 API 与组件通信之前，先建立对作用域、对象模型与异步调度的正确心智模型。内容以 MDN 官方文档为准，版本与生态动态截至 **2026-11**，可直接用于复习、面试准备与代码排错。

## 一、最新动态（截至 2026-11）

JavaScript 语言本身由 ECMAScript 规范推进，无单一"版本号"可引用，具体标准版本与时间以 [tc39/ecma262](https://tc39.es/ecma262/) 官方仓库为准。与本文直接相关的生态变化如下：

- **ES Modules 成为事实标准**：ESM（`import` / `export`）是浏览器与 Node 的官方模块标准，具备静态分析、Tree Shaking 能力；CommonJS 为同步加载的历史方案。现代工程（含 Vite 8）均以 ESM 为基线。
- **`require(esm)` 已默认可用**：Node 默认支持以 `require()` 加载 ESM，Vite 8 的 ESM-only 分发与运行依赖此能力，Node 要求 **20.19+ / 22.12+**。
- **顶层 `await` 与动态 `import()`**：模块顶层可直接 `await`，配合动态 `import()` 实现按需加载与代码分割，是当前异步加载的主流写法。
- **`Temporal` API 持续推进**：更现代的日期时间 API，Vitest 5 的 fake timers（`@sinonjs/fake-timers`）已**默认模拟 `Temporal`**，测试中需注意其行为。
- **`import defer`**：延迟模块求值的新语法，**TypeScript 5.9 已支持**，用于把副作用执行推迟到模块加载完成之后。
- **构建工具 Rust 化**：Vite 8 以 Rolldown（Rust）取代 esbuild + Rollup，配合 Oxc、Lightning CSS，官方称构建提速 10–30×；这些工具链都以原生 ESM 与 `require(esm)` 为前提，因此掌握 ESM 语义变得更重要。

> [!info] 口径说明
> 以上版本与特性日期取自官方文档 / 官方仓库，写作时已核对；个别规范项（如 `Temporal` 的最终落地细节）以官方仓库为准，不在此做预测性描述。

## 二、基础概念

**1. 闭包（Closure）**：函数与其**声明时所在的词法环境**的组合。即使外层函数已经执行结束，内部函数仍能访问并"记住"外层作用域中的变量。闭包是数据封装、私有变量、模块模式与回调/高阶函数的基础。

**2. 原型与原型链**：JavaScript 是**基于原型的继承**语言。每个对象有一个内部 `[[Prototype]]`（通过 `__proto__` 或 `getPrototypeOf` 访问），属性查找沿原型链逐级向上，直到 `Object.prototype` 的末端。

**3. 异步与事件循环**：JavaScript **单线程**，通过**事件循环（Event Loop）**调度任务。任务（Task）与微任务（Microtask）分属不同队列：**每执行完一个宏任务后，会把整个微任务队列清空，再执行下一个宏任务**，因此 `Promise` 回调总先于 `setTimeout(..., 0)`。

**4. 模块系统**：ES Modules 为官方标准（静态分析、Tree Shaking、动态只读引用）；CommonJS 同步加载、输出值拷贝；AMD / UMD / IIFE 属历史方案，现代工程以 **ESM 为主**。

## 三、核心机制

### 3.1 闭包：作用域与生存期

闭包的本质是**函数捕获了定义时的词法环境**。变量不会因外层函数返回而被回收，只要闭包仍被引用，它所依赖的变量就一直存活。这一特性可用于：

- **私有变量与封装**：用函数作用域模拟私有状态，外部无法直接访问；
- **模块模式**：在无 ESM 的环境中封装状态，仅暴露接口；
- **高阶函数与回调**：`map` / `filter` / 事件回调都依赖闭包传递上下文。

### 3.2 原型链与继承

- **原型查找**：读取属性时先查自身，再沿 `[[Prototype]]` 逐级向上。
- **`Object.create(proto)`**：以指定原型创建对象，是理解原型链最直接的方式。
- **`class` / `extends` / `super`**：语法糖，底层仍是原型链。
- **注意**：`null` 原型对象（`Object.create(null)`）没有继承任何方法，适合做纯净字典；`Symbol.iterator` 决定对象能否被 `for...of` 展开。

### 3.3 事件循环与异步

- **调用栈 → 微任务队列 → 宏任务队列**：同步代码进入调用栈；`Promise.then` 等进入微任务队列；`setTimeout` / I/O 等进入宏任务队列。
- **关键规则**：执行完一个宏任务后**清空整个微任务队列**，因此即使微任务里又产生微任务，也会在下一个宏任务之前全部执行完。
- **`async/await`**：基于 Promise 的语法糖，用 `try/catch` 处理错误；并行用 `Promise.all`；可用 `AbortController` 取消 `fetch`。

### 3.4 模块系统差异

ESM 的导入是**命名引用**（live binding），导出可被 Tree Shaking；CommonJS 的 `require` 是**同步求值后返回值的拷贝**，两者混用可能导致同一包出现两份实例（dual-package hazard）。

## 四、实践步骤（含代码/命令示例）

### 4.1 验证闭包：计数器与私有变量

```javascript
function createCounter() {
  let count = 0; // 被闭包捕获，外部无法直接访问
  return {
    inc() { count += 1; return count; },
    get() { return count; },
  };
}

const counter = createCounter();
console.log(counter.inc()); // 1
console.log(counter.inc()); // 2
console.log(counter.get());  // 2
```

### 4.2 原型链与 class 继承

```javascript
// 用 Object.create 手动建立原型链
const proto = { greet() { return 'hi'; } };
const obj = Object.create(proto);
console.log(obj.greet());        // hi
console.log(Object.getPrototypeOf(obj) === proto); // true

// class 语法糖：extends / super
class Animal {
  constructor(name) { this.name = name; }
  speak() { return `${this.name} 发声`; }
}

class Dog extends Animal {
  speak() { return `${super.speak()}：汪汪`; } // super 调用父类方法
}

console.log(new Dog('旺财').speak()); // 旺财 发声：汪汪

// 纯净字典：无原型，避免与内置属性冲突
const map = Object.create(null);
map['hasOwnProperty'] = 'safe'; // 不会命中原型上的同名方法
```

### 4.3 验证事件循环：微任务先于宏任务

```javascript
console.log('1 同步');

setTimeout(() => console.log('4 setTimeout'), 0);

Promise.resolve().then(() => {
  console.log('3 Promise 微任务');
  Promise.resolve().then(() => console.log('微任务中再产生的微任务'));
});

console.log('2 同步');

// 运行结果顺序：
// 1 同步 → 2 同步 → 3 Promise 微任务 → 微任务中再产生的微任务 → 4 setTimeout
```

### 4.4 async/await 与错误处理、取消请求

```javascript
async function loadUser(id) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 3000);
  try {
    const res = await fetch(`/api/users/${id}`, { signal: controller.signal });
    if (!res.ok) throw new Error(`请求失败：${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

// 并行：用 Promise.all 并发执行，避免串行等待
async function loadBoth(id) {
  const [user, posts] = await Promise.all([
    loadUser(id),
    fetch(`/api/posts/${id}`).then((r) => r.json()),
  ]);
  return { user, posts };
}
```

### 4.5 ESM 模块与命令行验证

```javascript
// math.js
export const add = (a, b) => a + b;
export default (a, b) => a * b;

// main.js
import multiply, { add } from './math.js';
console.log(add(2, 3), multiply(2, 3)); // 5 6
```

```bash
# 在 Node 中以 ESM 运行（package.json 设置 "type": "module" 后可直接 node main.js）
node main.js

# 直接运行单文件模块（无需配置 type 字段）
node --input-type=module -e "import { add } from './math.js'; console.log(add(1, 2))"

# 查看当前 Node 版本是否满足 Vite 8 等工具链要求
node -v   # 需要 20.19+ 或 22.12+
```

## 五、最佳实践与常见坑

- **闭包内存泄漏**：不再使用的闭包应及时解除引用（如移除监听、置空引用），避免外层作用域变量被长期持有。
- **`var` 与循环闭包**：`var` 无块级作用域，经典坑是循环中闭包捕获同一变量；改用 `let` 或用 `forEach` / IIFE 隔离作用域。
- **`this` 指向**：普通函数的 `this` 取决于调用方式，箭头函数不绑定自己的 `this`，直接继承词法上下文，按需选择。
- **原型污染**：不要随意修改 `Object.prototype`；做纯字典优先 `Object.create(null)`。
- **`class` 字段与继承顺序**：`super()` 必须在访问 `this` 之前调用；静态字段与继承的语义需留意，避免在构造前误用 `this`。
- **异步顺序陷阱**：不要假设 `setTimeout` 早于 `Promise` 回调执行；`await` 后是微任务语义，多个 `await` 之间会插入微任务，注意执行时序。
- **未捕获的 Promise 错误**：`async` 函数中抛出的错误不会自动被外层 `try/catch` 捕获（除非被 `await`），务必用 `try/catch` 或 `unhandledrejection` 兜底。
- **模块格式混用**：同一包同时提供 CJS 与 ESM 可能产生两份实例，导致状态、单例失效；发布时优先选择单一模块格式。

## 六、核心要点速查

1. **闭包** = 函数 + 声明时的词法环境，是封装与私有变量的实现基础。
2. **原型链**：属性沿 `[[Prototype]]` 逐级向上查找，`class` / `extends` / `super` 是原型继承的语法糖。
3. **`Object.create(null)`** 创建无原型对象，适合做纯净字典，避免原型污染。
4. **事件循环**：单线程调度，宏任务与微任务分队列；**每个宏任务后清空整个微任务队列**。
5. **`Promise` 回调总先于 `setTimeout(..., 0)`**，因为微任务优先级高于宏任务。
6. **`async/await`** 基于 Promise：`try/catch` 处理错误、`Promise.all` 并行、`AbortController` 取消请求。
7. **ESM**：命名引用 + 静态分析 + Tree Shaking，为现代标准；**CommonJS** 同步加载、返回值拷贝。
8. **模块顶层 `await`** 与动态 `import()` 支持按需加载与代码分割。
9. **`require(esm)`** Node 默认支持，是 Vite 8 等 ESM-only 工具链的运行前提。
10. **避免** `var` 循环闭包、随意改 `Object.prototype`、忽略未捕获的 Promise 错误。

## 七、学习资源

**官方文档**

- [MDN · 闭包（Closures）](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures)
- [MDN · 继承与原型链（Inheritance and the prototype chain）](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)
- [MDN · 事件循环（Event loop）](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/EventLoop)
- [MDN · JavaScript 模块（Modules）](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Modules)
- [tc39 · ECMAScript 语言规范](https://tc39.es/ecma262/)

**规范与生态**

- [Node.js 官方文档](https://nodejs.org/zh-cn/docs)
- [Vite 8 发布说明（Rolldown / ESM-only）](https://vite.dev/blog/announcing-vite8.html)

## 八、关联笔记

- [[Vue3与前端-从入门到精通]] — 本主题在体系中的位置与整体地图
- [[前端开发]] — 前端技术整体地图与目录索引
- [[标签索引]] — 全库标签导航

## 九、变更记录

- 2026-11-19：首次创建。
