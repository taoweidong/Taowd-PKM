---
title: Python迭代器与生成器
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 迭代器
  - 生成器
aliases:
  - Python 迭代器与生成器深入
  - Python 迭代协议与 yield 机制
source: 网络资料整理
---

# Python迭代器与生成器

> [!摘要]
> 本文系统梳理 Python 的**迭代协议、迭代器对象、生成器函数与生成器表达式**，并给出可直接运行的实战代码与避坑要点。迭代器与生成器是 Python 惰性求值的核心机制：它支撑了 `for` 循环、推导式、文件与网络流的流式处理、异步迭代，也是协程与上下文管理的重要基础。内容以 **Python 3.15**（3.15.0 于 2026-10-09 发布，3.15.2 于 2026-10-25 发布）为基准，涵盖 3.15 新增的生成器 `throw(exc)` 新签名与 PEP 798 生成器表达式解包。适合已掌握 Python 基础语法、希望理解底层执行模型并写出更高效代码的开发者。

## 一、最新动态（截至 2026-11）

- **当前稳定主线为 Python 3.15**：3.15.0 于 **2026-10-09** 发布，最新维护版 **3.15.2** 于 **2026-10-25** 发布（属「紧急安全发布」）；**Python 3.16** 处于预发布阶段（`3.16.0a2`，2026-11-10）。版本号以官方发布页为准。
- **3.15 生成器 `throw()` 旧签名弃用**：`generator.throw(type, exc, tb)` / `athrow(...)` 的旧三参数签名被弃用，改用单参数 **`throw(exc)`** / **`athrow(exc)`**。新代码应直接传异常实例。
- **3.15 新增 PEP 798 生成器表达式解包**：生成器表达式支持 `*` 解包，例如 `(*L for L in lists)`，异步生成器表达式同样支持 `(*a async for a in agen())`，等价于嵌套推导式或 `itertools.chain`。
- **3.15 软弃用 `__index__()` / `__int__()` 返回非 `int`**：未来这些方法必须返回 `int` 的严格子类（`__float__` / `__complex__` 同理），当前列入「未来版本移除」清单。涉及自定义数值类型与迭代协议实现时需注意。
- **迭代协议基础设施稳定**：`collections.abc` 中的 `Iterable` / `Iterator` / `Generator` / `AsyncIterator` 等协议沿用不变；`collections.abc.Buffer`（3.12 起）可用于缓冲协议的运行时判断，与迭代场景常配合使用。
- **基础语义来源**：生成器与 `yield from` 的语义由 **PEP 255 / PEP 380** 奠定，**PEP 479** 规定 `StopIteration` 在生成器内部会被转为 `RuntimeError`。

> [!info] 版本依据
> 以上版本与 PEP 状态来自 [Python 3.15 What's new](https://docs.python.org/3.15/whatsnew/3.15.html) 与 [collections.abc 官方文档](https://docs.python.org/3/library/collections.abc.html)。第三方库补丁更新频繁，实际使用以写作当日官方发布页为准。

## 二、基础概念

**可迭代对象（Iterable）与迭代器（Iterator）**是两个不同层次的概念：

- **可迭代对象（Iterable）**：实现了 `__iter__()` 方法，能被 `for` 循环遍历。列表、元组、字典、集合、字符串、文件对象、生成器表达式等都是可迭代对象。
- **迭代器（Iterator）**：同时实现 `__iter__()` 与 `__next__()`，被 `next()` 调用时返回下一个值，没有更多元素时抛出 `StopIteration`。迭代器是**一次性的、有状态的**，遍历结束后即耗尽。

**生成器（Generator）**是创建迭代器的便捷方式，分两种形态：

- **生成器函数**：函数体中含 `yield`，调用后**不立即执行**，而是返回一个生成器对象（本身即是迭代器）。
- **生成器表达式**：把列表推导式的方括号换成圆括号，如 `(x * 2 for x in data)`，得到惰性的生成器对象。

判断与注册协议用 `collections.abc`：

```python
from collections.abc import Iterable, Iterator

print(isinstance([1, 2, 3], Iterable))      # True
print(isinstance([1, 2, 3], Iterator))      # False（列表不是迭代器）
print(isinstance(iter([1, 2, 3]), Iterator) # True
```

异步场景对应 **异步迭代协议**：`__aiter__()` 与 `__anext__()`，配合 `async for` 使用，由 `AsyncIterable` / `AsyncIterator` 定义。

## 三、核心机制

**生成器的惰性执行模型**：

1. 调用生成器函数时，函数体**不会运行**，只是创建生成器对象并保存局部状态。
2. 每次 `next()`（或 `for` 循环、生成器表达式被消费）时，解释器从上一次 `yield` 的位置恢复执行，执行到下一个 `yield` 暂停，返回 `yield` 的值。
3. 再次 `next()` 继续，直到函数执行完毕（或 `return`），解释器抛出 `StopIteration`，迭代结束。

**`yield from`（PEP 380）**：把一个迭代器「委托」给当前生成器，自动逐个产出其元素，并能把子生成器的返回值带回来：

```python
def inner():
    yield 1
    yield 2
    return "内层结果"

def outer():
    result = yield from inner()
    print("收到：", result)
    yield "外层完成"

for item in outer():
    print(item)
# 1
# 2
# 收到： 内层结果
# 外层完成
```

**PEP 479 的边界**：在生成器函数内部，如果 `next()` 调用抛出的 `StopIteration` 没有被捕获，它会被转换为 `RuntimeError`，避免 `StopIteration` 意外逃逸破坏迭代控制流。写自定义迭代器时务必注意。

**3.15 新签名**：`gen.throw(exc)` 从外部向生成器抛出异常，在 `yield` 处被 `try/except` 捕获，可用于中断、取消或注入错误；旧版三参数形式已弃用。

```python
def gen():
    try:
        yield 1
    except ValueError as e:
        print("生成器内捕获：", e)
        return

g = gen()
print(next(g))      # 1
g.throw(ValueError("中断"))   # 生成器内捕获： 中断
print(next(g))      # StopIteration
```

## 四、实践步骤（含代码/命令示例）

**1. 自定义迭代器类**（实现 `__iter__` 与 `__next__`）：

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.n = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for v in Countdown(3):
    print(v)   # 3 2 1
```

**2. 用生成器函数流式处理文件**（避免一次性读入内存）：

```python
def read_lines(path: str, limit: int | None = None):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            yield line
            if limit is not None and limit <= 0:
                return
            limit -= 1

# 用法：只处理前 5 行，其余不读
for line in read_lines("data.txt", limit=5):
    print(line)
```

**3. 生成器表达式 vs 列表推导**：

```python
nums = range(1000000)
total_list = sum([x * x for x in nums])   # 先构造完整列表，占内存
total_gen  = sum(x * x for x in nums)     # 边算边加，几乎零额外内存
```

**4. 惰性管道（逐阶段过滤/映射）**：

```python
def stage_map(src, fn):
    for x in src:
        yield fn(x)

def stage_filter(src, pred):
    for x in src:
        if pred(x):
            yield x

pipeline = stage_filter(
    stage_map(range(1, 101), lambda x: x * x),
    lambda n: n % 6 == 0,
)
print(list(pipeline))   # [6, 12, 18, ...] 的平方值中能被 6 整除的数
```

**5. 异步生成器**（配合 `async for`，注意需 `async def` + `yield`）：

```python
import asyncio

async def async_count(n: int):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main():
    total = 0
    async for v in async_count(3):
        total += v
    print("累计：", total)   # 累计： 3

asyncio.run(main())
```

**6. 验证环境与版本**：

```bash
python --version        # Python 3.15.x
python -c "import sys; print(sys.version)"
```

## 五、最佳实践与常见坑

- **迭代器只能遍历一次**：迭代结束后无法重置。需要多次遍历时，要么重新创建，要么用 `itertools.tee()` 缓存副本，或先转成 `list`。
- **不要在遍历中修改被迭代的集合**：遍历 `list`/`dict` 时增删元素会抛 `RuntimeError` 或产生遗漏元素。需要变更时先复制快照：`for x in list(data):`。
- **生成器不执行即无副作用**：定义生成器函数不会运行代码，只有被消费时才执行。忘记消费（例如忘记 `list(gen())`）会导致逻辑静默不生效。
- **PEP 479 陷阱**：自定义迭代器中不要向调用方泄露未捕获的 `StopIteration`，否则会触发 `RuntimeError`。用 `raise StopIteration` 正常结束是安全的，但不要用 `next()` 的返回值去判断结束。
- **及时 `close()` 释放资源**：生成器持有 `with` 文件句柄等资源时，若提前退出循环，需调用 `gen.close()` 或使用 `contextlib.closing`，否则资源可能延迟释放。
- **谨慎使用 `throw()` 与 `send()`**：3.15 起统一使用单参数 `throw(exc)`；`send(value)` 可用于把值送入生成器（首次须用 `None`），但过度使用会显著增加复杂度，优先用明确的参数传值。
- **性能取舍**：生成器适合「数据量大、按需消费、管道式处理」；数据量小且需多次使用，直接用列表/数组更快。生成器表达式相比列表推导有轻微额外开销，但在内存上优势明显。

> [!warning] 容易忽视的坑
> 生成器是**惰性求值**：如果用 `if gen:` 判断一个生成器对象是否「有数据」，它始终为真（对象存在即真），必须用 `next(gen, default)` 或实际迭代来探测。

## 六、核心要点速查

1. **协议**：可迭代对象实现 `__iter__`，迭代器额外实现 `__next__`，无元素时抛 `StopIteration`。
2. **生成器**：含 `yield` 的函数调用后返回生成器对象，惰性执行、逐次产出，本身就是迭代器。
3. **`yield from`（PEP 380）**：委托子迭代器并带回其返回值，等价于手动 `for` + `yield`。
4. **PEP 479**：生成器内部的 `StopIteration` 会被转为 `RuntimeError`，不要让它逃逸。
5. **3.15 新签名**：`gen.throw(exc)` 单参数，旧三参数 `throw(type, exc, tb)` 已弃用。
6. **PEP 798（3.15）**：生成器表达式支持 `*` 解包，如 `(*L for L in lists)`。
7. **一次性语义**：迭代器遍历完即耗尽，需多次使用要重建或 `itertools.tee()`。
8. **惰性优势**：生成器/生成器表达式适合大文件、流式与管道处理，内存占用远低于列表推导。
9. **异步迭代**：`__aiter__` / `__anext__` + `async for`，生成器用 `async def` + `yield` 定义。
10. **协议注册**：用 `collections.abc` 的 `Iterable` / `Iterator` / `AsyncIterator` 做类型判断与抽象基类注册。

## 七、学习资源

- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [PEP 255 – Simple Generators](https://peps.python.org/pep-0255/)
- [PEP 380 – Syntactical Changes for Yield From](https://peps.python.org/pep-0380/)
- [PEP 479 – Change StopIteration handling inside generators](https://peps.python.org/pep-0479/)
- [PEP 798 – Tuple-unpacking for comprehensions（3.15）](https://peps.python.org/pep-0798/)
- [collections.abc — Abstract Base Classes（Python 官方文档）](https://docs.python.org/3/library/collections.abc.html)
- [Python 官方文档：The Python Language Reference / 迭代器与生成器](https://docs.python.org/3/glossary.html#term-iterator)

## 八、关联笔记

- [[Python-从入门到精通]] — 本知识点在 Python 体系中的定位与全景路线
- [[Python学习]] — Python 入门与基础语法学习路径
- [[Python-高级特性]] — 装饰器、元编程、类型等进阶主题，与迭代器/生成器共同构成高级特性基础

## 九、变更记录

- 2026-11-19：首次创建。
