---
title: Python-生成器与迭代器
date: 2026-11-19
tags: [技术积累, 编程语言, Python, 生成器, 迭代器]
---
# Python-生成器与迭代器

> [!abstract] 摘要
> 迭代器协议是 Python `for` 循环、解包、推导式的底层机制，生成器则是该协议的语法糖，核心价值是**惰性求值**——用恒定内存处理大文件、大集合与无限序列。学完本篇能手写迭代器类与生成器管道，掌握 `yield from`、`send/throw/close`，并用生成器实现日志流式分析器与惰性分页数据管道。

## 一、概念与原理

**可迭代对象（Iterable）**实现 `__iter__()` 返回迭代器；**迭代器（Iterator）**实现 `__next__()`，耗尽时抛 `StopIteration`。`for x in obj` 的底层是先 `iter(obj)` 再反复 `next()` 直到 `StopIteration`。两者关系与数据流向：

```mermaid
graph LR
    A[可迭代对象<br>实现 __iter__] -->|iter() 每次返回新迭代器| B[迭代器<br>实现 __next__]
    B -->|next() 逐个产出| C[消费方<br>for / next / 推导式]
    C -->|耗尽抛 StopIteration| B
    D[生成器函数 yield] -->|调用即返回| B
```

关键区分（易混淆点速查表）：

| 概念 | 协议 | 特点 | 示例 |
|------|------|------|------|
| 可迭代对象 | `__iter__` | 可重复 for，可反复 `iter()` | list/dict/str/文件对象 |
| 迭代器 | `__iter__` + `__next__` | **一次性**，耗尽即空 | 生成器、`map`/`zip`/文件迭代 |
| 生成器 | 含 `yield` 的函数 | 迭代器语法糖，解释器自动实现协议 | `def g(): yield 1` |
| 生成器表达式 | `(x for x in ...)` | 内联生成器，返回迭代器 | `sum(x*x for x in r)` |

母篇 [[Python-高级特性]] 已给出协议全貌，本篇聚焦**惰性求值的工程落地**：数据流过管道的每一站都只处理"当前这一个元素"，内存占用与数据总量无关，只与单元素大小相关。

## 二、核心语法 / API 详解

### 2.1 手写迭代器类（理解协议）

```python
class Countdown:
    def __init__(self, n: int):
        self.n = n
    def __iter__(self) -> "Countdown":   # 迭代器返回自身
        return self
    def __next__(self) -> int:
        if self.n <= 0:
            raise StopIteration          # 耗尽信号，for 会静默捕获
        self.n -= 1
        return self.n + 1

list(Countdown(3))   # [3, 2, 1]
```

> [!tip] 生成器是协议的语法糖
> 手写类要用实例变量保存状态，繁琐且易错。下面这个生成器函数与上面完全等价——解释器自动帮你实现了 `__iter__`/`__next__` 与局部状态保存：

```python
def countdown(n: int):
    while n > 0:
        yield n        # 暂停点：产出值并挂起，下次 next() 从这里恢复
        n -= 1

gen = countdown(3)     # 调用不执行函数体，返回生成器对象
next(gen), next(gen)   # (3, 2)
```

### 2.2 yield from 与生成器管道

`yield from iterable` 委托给子可迭代对象，逐个透传值（等价于 `for x in sub: yield x`，还透传 `send/throw`，是协程委派的历史基础）：

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)     # 递归委托：把子生成器的值逐个产出
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

**惰性管道**是生成器最经典的用法——每站都是生成器，元素逐个流过整条管道：

```python
def read_lines(path):                       # 站 1：逐行读
    with open(path, encoding="utf-8") as f:
        yield from f                        # 文件对象本身就是迭代器

def filter_lines(lines, keyword):           # 站 2：过滤
    return (ln for ln in lines if keyword in ln)

def parse(lines):                           # 站 3：解析
    return (ln.strip().split(",", 1) for ln in lines)

# 只有真正迭代 results 时，数据才流过整条管道
lines = read_lines("big.log")
errors = filter_lines(lines, "ERROR")
results = parse(errors)
for ts, msg in results:
    print(ts, msg)
```

### 2.3 生成器表达式 vs 列表推导

```python
squares_list = [x * x for x in range(10_000_000)]   # 立即物化：约 400MB 内存
squares_gen   = (x * x for x in range(10_000_000))  # 惰性：几乎 0 内存

sum(x * x for x in range(1000))    # 函数唯一实参时可省一层括号
total = sum(squares_gen)           # 消费后生成器耗尽——一次性
```

> [!warning] 迭代器是一次性的
> 生成器、`map`、`zip`、文件对象只能消费一遍，第二次迭代得到空结果且不报错——这是"数据神秘消失"的头号原因。需要多次消费时用 `list()` 物化，或用 `itertools.tee` 复制。

### 2.4 惰性求值与内存实测

大文件逐行读是教科书场景：文件对象天然是迭代器，逐行产出，内存占用恒定：

```python
# 方式 A（坏）：f.readlines() / list(f) 一次性载入 10GB 文件 → 内存爆炸
# 方式 B（好）：for line in f:           逐行流式 → 内存占用恒定（单行大小）
```

用 `tracemalloc` 实测内存差异（Python 3.12+，可直接运行）：

```python
import tracemalloc

tracemalloc.start()
data = [x * x for x in range(5_000_000)]        # 列表推导
print("列表推导峰值:", tracemalloc.get_traced_memory()[1] / 1e6, "MB")   # ≈ 320 MB
tracemalloc.reset_peak()

gen = (x * x for x in range(5_000_000))          # 生成器表达式
first = next(gen)
print("生成器峰值:", tracemalloc.get_traced_memory()[1] / 1e6, "MB")     # < 0.5 MB
```

典型实测结论：`range(5_000_000)` 规模下，列表推导峰值约 300-400MB，生成器不足 1MB——**内存差 3 个数量级**，代价是生成器不能随机访问、只能单遍消费。

### 2.5 send / throw / close 与协程雏形

`yield` 是表达式，可通过 `send()` 双向通信（PEP 342），这是 asyncio 协程的历史雏形（现代协程见 [[Python-asyncio异步编程]]）：

```python
def averager():
    total, count = 0.0, 0
    average = None
    while True:
        value = yield average            # 接收 send 传入的值
        if value is None:                # next() 恢复时 yield 返回 None
            continue
        total += value
        count += 1
        average = total / count

avg = averager()
next(avg)              # 预激（prime）：推进到第一个 yield
avg.send(10)           # 10.0
avg.send(20)           # 15.0
```

三个控制方法：`gen.send(v)` 恢复执行并让 `yield` 表达式返回 `v`；`gen.throw(exc)` 在暂停处抛入异常；`gen.close()` 发送 `GeneratorExit` 终止生成器（垃圾回收时自动调用，清理逻辑请放 `try/finally`）。

## 三、实战案例

**日志文件流式分析器**（Python 3.12+，零依赖）：对任意大小的日志做"逐行读 → 过滤 → 解析 → 聚合"四段惰性管道，内存恒定。生成 `app.log` 后运行 `python log_analyzer.py app.log`。

```python
"""log_analyzer.py — 生成器管道实现的大日志流式分析器"""
import sys
from collections import Counter
from itertools import islice

def read_lines(path: str):                       # 站 1：惰性逐行读
    with open(path, encoding="utf-8") as f:
        yield from f                             # 委托给文件迭代器

def parse(lines):                                # 站 2：解析 "级别,消息"
    for ln in lines:
        parts = ln.strip().split(",", 1)
        if len(parts) == 2:
            yield parts[0], parts[1]

def by_level(parsed, level: str):                # 站 3：按级别过滤
    return (msg for lv, msg in parsed if lv == level)

def top_errors(errors, n: int = 5):              # 站 4：聚合（终端物化）
    counter = Counter(msg.split(":")[0] for msg in errors)
    return counter.most_common(n)

def analyze(path: str) -> list[tuple[str, int]]:
    lines = read_lines(path)
    parsed = parse(lines)
    errors = by_level(parsed, "ERROR")
    return top_errors(errors)                    # 只有这里才真正开始消费

if __name__ == "__main__":
    # 生成 100 万行演示日志（约 30MB）
    with open("app.log", "w", encoding="utf-8") as f:
        for i in range(1_000_000):
            lv = ("INFO", "WARNING", "ERROR")[i % 7 == 0 and 2 or (i % 3 == 0)]
            f.write(f"{lv},service{i % 10}: 第{i}号请求处理完成\n" if lv != "ERROR"
                    else f"ERROR,service{i % 10}: timeout after 30s\n")

    import tracemalloc, time
    tracemalloc.start()
    t0 = time.perf_counter()
    for msg, cnt in analyze("app.log"):
        print(f"{cnt:>8} 次 | {msg}")
    cost = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1] / 1e6
    print(f"耗时 {cost:.2f}s，峰值内存 {peak:.1f}MB（日志越大内存不变）")
```

典型输出：100 万行日志、峰值内存约 10-20MB（主要是 Counter），而把文件整体 `readlines()` 需要数百 MB。管道中间站全部惰性，只有终端聚合器物化必需的最小数据。

## 四、动手练习

1. **热身**：不运行代码，说出 `g = (x for x in range(3)); list(g); list(g)` 的输出并解释。提示：迭代器一次性。
2. **基础**：实现生成器 `chunked(iterable, size)`，把任意可迭代对象按 size 切块：`list(chunked(range(7), 3)) == [[0,1,2],[3,4,5],[6]]`。提示：`itertools.islice` + 循环。
3. **进阶**：实现无限素数生成器 `primes()`，并用 `itertools.islice(primes(), 10)` 取前 10 个。提示：埃氏筛 + 字典记录"下一个合数"，或对每个候选数只除以已产出的素数。
4. **挑战（惰性分页数据管道）**：实现 `paged(items, page_size)`——返回一个生成器，每次 `next()` 产出一"页"（列表）；再实现 `page_reader(path, page_size)` 组合 `read_lines` 做到：逐页读取大文件，每次只在内存中保留一页数据，支持 `for page in page_reader(...)` 且随时 `break` 不读完整个文件。
   提示：分页器内部维护缓冲列表，缓冲满 `page_size` 条就 `yield` 出去；文件版把生成器接在文件迭代器后面，`break` 时生成器被 `close()`，`with` 块随 `finally` 关闭文件。

> [!success]- 练习 4 参考答案要点
> `def paged(items, page_size): buf = []; for x in items: buf.append(x); if len(buf) == page_size: yield buf; buf = []; if buf: yield buf` ——三个关键点：① 循环内缓冲满即产出，产出的是**新列表**（或直接 yield 后新建，避免外部修改影响内部状态）；② 结束后残留不满一页的缓冲也要补发；③ `page_reader` 组合时利用生成器被 `close()` 会触发 `GeneratorExit` → `finally` → 文件自动关闭的特性，因此 `for page in page_reader(...)` 中途 `break` 不会泄漏文件句柄。若想更稳，可在 `page_reader` 里显式 `try/finally: src.close()`。进阶方向：把 `page_size` 改成带参数的装饰器（见 [[Python-装饰器详解]] 练习 4）形成"页大小策略"可插拔。

## 五、常见坑与 FAQ

> [!warning] 生成器只能消费一遍
> `gen = read_lines(path)` 之后 `sum(len(g) for g in gen)` 再 `analyze(gen)`，第二次得到空结果。迭代器协议决定了"耗尽即空"。要么物化成 list，要么把"创建生成器"封装成函数每次调用新建。

> [!warning] 生成器函数体在调用时不会执行
> `g = countdown(3)` 只创建对象，函数体一行都没跑；第一次 `next(g)` 才开始执行到 `yield`。这意味着"调用生成器函数"不产生任何副作用，副作用推迟到消费时——调试时容易误判执行时机。

> [!tip] StopIteration / GeneratorExit 属于 BaseException 而非 Exception
> 官方刻意让它们不继承 `Exception`，防止被 `except Exception` 意外吞掉、破坏迭代协议（详见 [[Python-上下文管理器与异常处理]] 的异常体系）。在生成器里写 `except Exception` 一般不会拦住它们，但也**不要在生成器内部显式捕获 `StopIteration`**（PEP 479：生成器内 `StopIteration` 冒泡会被转成 `RuntimeError`）。

> [!tip] 什么时候该用列表推导而不是生成器
> ① 需要多次遍历或随机访问；② 数据量小（几百条以内），物化开销可忽略；③ 需要结果可复用、可 `len()`、可索引。生成器适合一次性流式消费的大数据/无限序列。拿不准时先列表推导，出现内存瓶颈再改惰性（改动通常只是把 `[]` 换成 `()` 并重排消费逻辑）。

## 六、自检清单

- [ ] 能说清可迭代对象与迭代器的区别（`__iter__` 返回新迭代器 vs 迭代器返回自身）
- [ ] 能手写一个满足协议的迭代器类，再改写成等价生成器函数
- [ ] 理解 `for` 循环底层是 `iter()` + 反复 `next()` + 捕获 `StopIteration`
- [ ] 能搭建"读 → 过滤 → 解析 → 聚合"四段惰性管道并说出哪一站物化
- [ ] 用 `tracemalloc` 亲自对比过列表推导与生成器的内存峰值
- [ ] 知道 `send` 需要先 `next()` 预激、`close()` 触发 `GeneratorExit`
- [ ] 遇到"第二次遍历为空"能立刻定位到迭代器一次性问题
- [ ] 知道 PEP 479（生成器内 StopIteration → RuntimeError）

## 七、关联笔记与参考

**关联笔记**：[[Python-高级特性]]（母篇：迭代器协议与协程概览）、[[Python-装饰器详解]]（`contextmanager` 用生成器实现上下文管理器）、[[Python-asyncio异步编程]]（async/await 是生成器暂停/恢复机制的直系后代）、[[Python-上下文管理器与异常处理]]（`StopIteration`/`GeneratorExit` 的异常层次）、[[Python-从入门到精通路线]]（生成器属阶段三）。

**参考资料**：

1. [Functional Programming HOWTO — 生成器章节（官方）](https://docs.python.org/3/howto/functional.html)
2. [Python 语言参考 — yield 表达式（send/throw/close）](https://docs.python.org/3/reference/expressions.html#yieldexpr)
3. [PEP 380 — yield from 语法](https://peps.python.org/pep-0380/)
4. [itertools — 官方文档（管道工具）](https://docs.python.org/3/library/itertools.html)
5. [tracemalloc — 官方文档（内存测量）](https://docs.python.org/3/library/tracemalloc.html)
