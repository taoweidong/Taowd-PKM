---
title: Python-装饰器详解
date: 2026-11-19
tags: [技术积累, 编程语言, Python, 装饰器, 元编程]
---
# Python-装饰器详解

> [!abstract] 摘要
> 装饰器是"接收函数、返回新函数"的高阶函数，是 Python 元编程的入口，也是框架（Flask 路由、pytest fixture、FastAPI 依赖注入）的核心机制。学完本篇能看懂并手写带参数装饰器、类装饰器，会用 `functools.lru_cache`/`singledispatch` 解决缓存与分发问题，并实现计时器、重试、鉴权、限流四个生产级装饰器。

## 一、概念与原理

装饰器的全部基础是两个语言特性：**函数是一等对象**（可赋值、可传参、可返回）与**闭包**（内层函数记住外层作用域变量）。学习依赖顺序：闭包 → 函数装饰器 → 带参数装饰器 → 类装饰器（母篇见 [[Python-高级特性]]）。

```mermaid
graph LR
    A[函数是一等对象] --> B[高阶函数]
    C[闭包 LEGB + nonlocal] --> B
    B --> D[函数装饰器<br>@语法糖]
    D --> E[带参数装饰器<br>三层嵌套]
    D --> F[类装饰器<br>__call__]
    D --> G[functools 工具<br>wraps/lru_cache/singledispatch]
```

**语法糖等价形式**是理解装饰器的钥匙——`@dec` 只是一行赋值：

```python
@dec
def foo(): ...

# 完全等价于：
def foo(): ...
foo = dec(foo)      # 名字 foo 重新绑定到 dec 返回的新函数
```

`@` 后面的表达式在**函数定义时求值一次**（装饰发生在导入期，不是调用期）；多层装饰器**从下往上**依次应用：`@a @b def f` 等价于 `f = a(b(f))`。

闭包回顾：闭包捕获的是**变量本身**（引用）而非定义时的值，改写外层变量需 `nonlocal`：

```python
def counter():
    count = 0
    def inc():
        nonlocal count      # 没有这句会 UnboundLocalError
        count += 1
        return count
    return inc              # 返回的内层函数携带 count 的引用
```

## 二、核心语法 / API 详解

### 2.1 基本函数装饰器与 functools.wraps

```python
import functools, time

def timer(func):                          # 接收原函数
    @functools.wraps(func)                # 保留原函数元信息（见下）
    def wrapper(*args, **kwargs):         # 用 *args/**kwargs 透传任意参数
        start = time.perf_counter()
        result = func(*args, **kwargs)    # 调用原函数
        cost = time.perf_counter() - start
        print(f"{func.__name__} 耗时 {cost:.4f}s")
        return result                     # 别忘了返回结果
    return wrapper                        # 返回新函数

@timer
def fetch_data(n: int) -> list[int]:
    """模拟取数"""
    return list(range(n))

fetch_data(1000)          # fetch_data 耗时 0.0001s
fetch_data.__name__       # 'fetch_data'（没有 wraps 会变成 'wrapper'）
```

`functools.wraps` 复制 `__name__`、`__qualname__`、`__doc__`、`__module__`、`__annotations__`、`__type_params__`（3.12+），并更新 `__dict__`，同时给 wrapper 加上 `__wrapped__` 指向原函数。

> [!warning] 不写 wraps 的后果
> ① 日志里函数名全部变成 `wrapper`，排查问题困难；② `help()` 文档丢失；③ pytest 等依赖 `__name__` 的工具行为异常；④ 多层装饰叠加时 `__wrapped__` 链断裂。**写装饰器必带 `@functools.wraps(func)`，应成为肌肉记忆。**

### 2.2 带参数的装饰器（三层嵌套）

带参数的装饰器本质是**装饰器工厂**：多包一层接收参数，`@` 语法糖先调用工厂得到真正的装饰器。

```python
def retry(times: int = 3, delay: float = 0.5):
    """第一层：接收装饰器参数"""
    def decorator(func):                  # 第二层：接收函数（真正的装饰器）
        @functools.wraps(func)
        def wrapper(*args, **kwargs):     # 第三层：调用时执行
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise             # 最后一次失败：原样抛出
                    print(f"第 {attempt} 次失败: {e}，{delay}s 后重试")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(times=5, delay=1.0)                # 等价于 fetch = retry(times=5, delay=1.0)(fetch)
def fetch():
    ...
```

记忆口诀：**带参装饰器 = 工厂(参数) → 装饰器(函数) → 包装器(调用)**，比无参装饰器多一层。

### 2.3 类装饰器

类实现 `__call__` 后实例可像函数一样调用，适合**带状态**的装饰（计数器、注册器）。类装饰器还能直接装饰"类"本身（如 `dataclasses.dataclass`、单例）：

```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)   # 类版 wraps
        self.func, self.count = func, 0
    def __call__(self, *args, **kwargs):
        self.count += 1                        # 状态存在实例上
        print(f"调用 #{self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hi(): ...

# 带参数的类装饰器：__init__ 收参数，__call__ 收函数
class RateLimit:
    def __init__(self, qps: float): self.qps = qps
    def __call__(self, func): ...
```

### 2.4 functools.lru_cache 与 singledispatch 实战

```python
from functools import lru_cache, cache, singledispatch

@lru_cache(maxsize=128, typed=False)   # maxsize=None 等价 @cache；typed=True 时 1 与 1.0 分开缓存
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(200)            # 瞬时完成；参数必须可哈希
fib.cache_info()    # CacheInfo(hits=198, misses=201, maxsize=128, currsize=128)
fib.cache_clear()   # 测试时清空

@singledispatch                          # 按第一个参数的类型在运行时分发
def to_str(arg) -> str:
    return str(arg)                      # 注册为 object 的兜底实现

@to_str.register
def _(arg: int) -> str:                  # 带注解自动注册 int
    return f"整数 {arg}"

@to_str.register(list)
def _(arg: list) -> str:                 # 不写注解就显式传类型
    return "、".join(map(str, arg))

to_str(42); to_str([1, 2])   # '整数 42'；'1、2'
to_str.dispatch(float)       # 查看某类型将选用的实现
```

## 三、实战案例

三个可运行的完整装饰器（Python 3.12+，零第三方依赖）。保存为 `decorators_demo.py` 直接 `python decorators_demo.py` 运行。

```python
"""decorators_demo.py — 计时器 / 重试 / 接口鉴权三个生产级装饰器"""
import functools, time, hashlib, hmac

# ---------- 1. 计时器：区分成功/失败，结果可被外部读取 ----------
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:                                   # 失败也计时
            cost = time.perf_counter() - start
            print(f"[timed] {func.__name__} 耗时 {cost:.4f}s")
    return wrapper

# ---------- 2. 重试：指数退避 + 指定异常类型 ----------
def retry(times=3, delay=0.2, backoff=2.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise                      # 保留原始 traceback
                    print(f"重试 {attempt}/{times - 1}，等待 {wait:.2f}s")
                    time.sleep(wait)
                    wait *= backoff                # 指数退避
        return wrapper
    return decorator

# ---------- 3. 接口鉴权：校验 HMAC 签名（模拟 API 网关） ----------
class require_auth:
    def __init__(self, secret: bytes):
        self.secret = secret
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(request: dict, *args, **kwargs):
            sign = request.pop("sign", "")
            payload = repr(sorted(request.items())).encode()
            expect = hmac.new(self.secret, payload, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sign, expect):     # 恒定时间比较，防时序攻击
                raise PermissionError("签名校验失败")
            return func(request, *args, **kwargs)
        return wrapper

@timed
@retry(times=3, delay=0.1, exceptions=(ConnectionError,))
def flaky_fetch(url: str) -> str:
    import random
    if random.random() < 0.6:
        raise ConnectionError(f"{url} 超时")
    return f"{url} 的数据"

@require_auth(secret=b"my-secret-key")
def create_order(request: dict) -> dict:
    return {"ok": True, "item": request.get("item")}

if __name__ == "__main__":
    print(flaky_fetch("https://api.example.com/data"))
    req = {"user": "tao", "item": "book", "sign": "bad-sign"}
    try:
        create_order(req)
    except PermissionError as e:
        print("鉴权失败:", e)
```

预期输出（随机）：`flaky_fetch` 可能重试 1-2 次后成功；`create_order` 抛出鉴权失败。

## 四、动手练习

1. **热身**：写一个 `@count_calls` 装饰器，记录函数被调用次数，访问 `func.calls` 可读取次数。提示：闭包里用字典存状态，或用类装饰器。
2. **基础**：写 `@deprecated(reason)` 带参装饰器，调用时用 `warnings.warn` 打印弃用警告。提示：`import warnings; warnings.warn(msg, DeprecationWarning, stacklevel=2)`。
3. **进阶**：写 `@cache_result` 装饰器，按参数缓存返回值（自己实现，不用 lru_cache），要求支持 `cache_result.clear()` 手动清空。提示：`wrapper.cache = {}` 把字典挂在 wrapper 上。
4. **挑战（限流装饰器）**：实现 `@rate_limit(max_calls=5, per_seconds=1.0)`——滑动窗口限流，1 秒内最多调用 5 次，超出则阻塞等待或抛 `RuntimeError`。
   提示：用 `collections.deque` 存最近调用时间戳；`nonlocal` 或挂载属性维护队列；进 wrapper 时先清理过期时间戳，再判断长度。

> [!success]- 练习 4 参考答案要点
> 核心结构：`@functools.wraps(func)`；`wrapper.calls = deque()` 保存时间戳；进入时 `now = time.monotonic()`，先 `while calls and calls[0] <= now - per_seconds: calls.popleft()` 清理窗口外记录；若 `len(calls) >= max_calls` 则 `sleep(per_seconds - (now - calls[0]))` 后重试（阻塞式）或直接 `raise RuntimeError("触发限流")`（拒绝式，可用参数 `block=True/False` 切换）；放行前 `calls.append(time.monotonic())`。关键点：① 用 `time.monotonic()` 而非 `time.time()`（后者会被系统调钟干扰）；② 挂在 wrapper 上的状态使同一装饰器实例对同一函数全局生效；③ 多线程场景需再加 `threading.Lock` 保护 deque（见 [[Python-并发编程实战]]）。

## 五、常见坑与 FAQ

> [!warning] 忘记返回结果
> `wrapper` 里调用了 `func(*args, **kwargs)` 却没写 `return`，装饰后的函数永远返回 `None`——这是初学者最高频的装饰器 bug。口诀：**透传参数、透传返回值**。

> [!warning] 装饰器在导入期执行，实例属性共享
> 类装饰器把状态存在实例上时，被装饰的函数只有一份实例，所有调用方共享同一状态（计数、缓存、限流窗口都是全局的）。若需要"每个调用方独立"，应把状态放到参数或对象上传递，而不是依赖装饰器实例。

> [!tip] lru_cache 的坑：参数必须可哈希、别缓存可变/带副作用函数
> `@lru_cache` 用 `(args, kwargs)` 做字典键，`list` 参数直接 `TypeError`；缓存含随机数、时间、数据库查询的函数会返回过期结果。另外缓存对象会延长生命周期（内存泄漏隐患），长驻服务记得设置 `maxsize` 或定期 `cache_clear()`。

> [!tip] 什么时候用类装饰器 vs 闭包装饰器
> 需要跨调用**维护状态**（计数、注册表）或**支持带参继承复用**时用类；纯"前后包一层"的逻辑（计时、日志、重试）用闭包更简洁。标准库装饰器 `@property`、`@staticmethod`、`@functools.cache`、`@singledispatch` 各有专用语法，优先复用而不是自造。

## 六、自检清单

- [ ] 能默写 `@dec` 的等价赋值形式，并解释多层装饰器从下往上应用
- [ ] 能解释闭包 late binding 问题及 `lambda i=i` 的修复原理
- [ ] 写装饰器时习惯性加 `@functools.wraps(func)`，并说出它复制哪些属性
- [ ] 能不查资料写出三层嵌套的带参装饰器（如 retry）
- [ ] 知道 `lru_cache` 的参数要求（可哈希）与 `cache_info`/`cache_clear` 用法
- [ ] 理解 `singledispatch` 按第一个参数类型分发、MRO 回退到 object 兜底
- [ ] 能说出"闭包装饰器 vs 类装饰器"的选择标准（是否需要跨调用状态）
- [ ] 用 `hmac.compare_digest` 而不是 `==` 做签名比较的原因说得清

## 七、关联笔记与参考

**关联笔记**：[[Python-高级特性]]（母篇：闭包与元编程全景）、[[Python-生成器与迭代器]]（同为函数式抽象，`contextmanager` 用生成器实现装饰器）、[[Python-类型注解实战]]（用 `ParamSpec` 给装饰器加精确类型）、[[Python-并发编程实战]]（装饰器内加锁保证线程安全）、[[Python-从入门到精通路线]]（装饰器属阶段三"高级"）。

**参考资料**：

1. [functools — 官方文档（wraps/lru_cache/singledispatch）](https://docs.python.org/3/library/functools.html)
2. [PEP 318 — Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
3. [Primer on Python Decorators — Real Python](https://realpython.com/primer-on-python-decorators/)
4. [functools.wraps 源码（WRAPPER_ASSIGNMENTS）](https://github.com/python/cpython/blob/main/Lib/functools.py)
