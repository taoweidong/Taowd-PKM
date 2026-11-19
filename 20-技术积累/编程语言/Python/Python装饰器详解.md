---
title: Python 装饰器详解
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 装饰器
  - 元编程
aliases:
  - Python装饰器
  - 装饰器
  - Decorator
source: 网络资料整理
---

# Python 装饰器详解

> [!摘要]
> 装饰器（Decorator）是 Python 中在不修改原函数源码的前提下，为其「附加」额外能力的高阶函数机制，其语法由 **PEP 318** 定义，本质是「类/函数调用」的语法糖。本文从基础概念、运行机制、实践步骤到 3.14/3.15 的版本适配与常见坑，完整梳理装饰器的使用方式与工程要点。适合已掌握 Python 函数与闭包、希望深入元编程与库/框架开发的读者，建议配合 [[Python-从入门到精通]] 的元编程章节一起阅读。

## 一、最新动态（截至 2026-11）

- **Python 3.15 是当前最新稳定版本**（3.15.0 首发于 2026-10-09，最新补丁 **3.15.2** 于 2026-10-25 发布，属紧急安全发布）；Python 3.16 处于预发布阶段（`3.16.0a2`，2026-11-10）。
- **装饰器核心事实未变**：装饰器语法由 **PEP 318** 定义；`functools.wraps` / `functools.update_wrapper` 仍是保留 `__name__`、`__doc__`、`__wrapped__` 的标准做法。
- **3.14 行为变更一：`functools.partial` 成为方法描述符**。把 `partial` 对象当作方法或装饰器使用时，绑定行为有变化，需用 `staticmethod()` 包装以保持旧行为。
- **3.14 行为变更二：注解延迟求值（PEP 649 / PEP 749）**。读取 `__annotations__` 的装饰器（数据校验、序列化、ORM 字段注册等）应改用 `annotationlib.get_annotations(..., format=Format.FORWARDREF)`；否则在 3.14 上从 `__dict__` 直接读 `__annotations__` 会**静默返回空 `{}`**，不报错、不警告，容易让校验逻辑「空转」。
- **常用装饰器仍在演进**：`functools.cached_property`（3.8+）自 **3.13 起支持泛型**；`functools.lru_cache` 继续作为缓存方案的主力。第三方包 `typing_extensions` 提供跨版本兼容的 `Format` 与 `get_annotations`，是迁移期的首选适配层。
- 版本与 PEP 状态均来自 Python 官方文档，详见「七、学习资源」；第三方补丁版本更新频繁，请以写作当日官方发布页为准。

## 二、基础概念

- **定义**：装饰器是一个「接收函数、返回函数」的高阶函数。`@deco` 等价于 `func = deco(func)`，`@deco(参数)` 等价于 `func = deco(参数)(func)`，这正是「类/函数调用」语法糖的含义。
- **能力定位**：装饰器用于日志、计时、缓存、鉴权、参数校验、属性代理、事务与资源管理等横切逻辑，让主干逻辑保持干净。
- **前置知识**：理解函数是一等对象、闭包、作用域、`*args`/`**kwargs`，以及类实例的 `__call__` 协议，才能吃透装饰器。
- **为什么需要 `functools.wraps`**：不加包装时，`wrapper` 会覆盖原函数的 `__name__`、`__doc__` 等，导致反射、调试、文档工具拿到错误信息。`wraps` 会把这些元数据与 `__wrapped__` 一并复制，是装饰器代码的「标配」。

## 三、核心机制

装饰器的运行分三步：

1. **语法展开**：解释器把 `@deco` / `@deco(args)` 改写成函数调用，用被装饰对象作为参数求值。
2. **包装返回**：装饰器函数内部通常返回一个新的包装函数（或类实例），由包装函数负责「前后逻辑 + 调用原函数」。
3. **元数据保留**：通过 `functools.wraps` 把原函数的 `__name__`、`__doc__`、`__module__`、`__qualname__`、`__annotations__` 等复制到包装函数，并设置 `__wrapped__` 指向原函数。

两种典型形态：

- **函数装饰器**：装饰器本身是函数，`@log` 直接包装。
- **带参装饰器**：装饰器是「返回装饰器」的闭包，`@repeat(times=3)` 需要先执行 `repeat(3)` 拿到真正的装饰器再包装。
- **类装饰器**：装饰器是带 `__call__` 的类实例，`__init__` 接收被装饰函数，`__call__` 执行调用逻辑。

## 四、实践步骤（含代码/命令示例）

**1. 基础装饰器**

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"[调用] {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[返回] {func.__name__}")
        return result
    return wrapper


@log
def greet(name: str) -> str:
    return f"hello, {name}"

print(greet("陶伟东"))
```

**2. 用 `functools.wraps` 保留元数据**

```python
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[调用] {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log
def add(a: int, b: int) -> int:
    """返回两数之和。"""
    return a + b

print(add.__name__, add.__doc__)   # add  返回两数之和。
print(add.__wrapped__)             # 指向原函数
```

**3. 带参数的装饰器**

```python
from functools import wraps


def repeat(times: int):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return deco


@repeat(times=3)
def say(msg: str) -> str:
    print(msg)
    return msg

say("decorator")
```

**4. 类装饰器**

```python
class Trace:
    def __init__(self, func):
        self.func = func
        self.__wrapped__ = func  # 便于 introspect

    def __call__(self, *args, **kwargs):
        print(f"before: {self.func.__name__}")
        return self.func(*args, **kwargs)


@Trace
def mul(a: int, b: int) -> int:
    return a * b

print(mul(3, 4))
```

**5. 内置常用装饰器**

```python
from functools import lru_cache, cached_property

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

class Config:
    @cached_property
    def expensive(self) -> dict:   # 首次访问时计算并缓存，3.13 起支持泛型
        return {"loaded": True}
```

**6. 适配 3.14 延迟注解的装饰器**

```python
import annotationlib          # Python 3.14+ 标准库
from functools import wraps

# 跨版本兼容可用 typing_extensions.get_annotations / Format
def register_fields(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 3.14 起直接读 func.__annotations__ 可能拿到空 dict，
        # 改用 get_annotations 并指定 FORWARDREF 更稳妥
        fields = annotationlib.get_annotations(
            func, format=annotationlib.Format.FORWARDREF
        )
        print("字段:", fields)
        return func(*args, **kwargs)
    return wrapper


@register_fields
def user(name: str, age: int) -> None:
    return None
```

**命令示例（环境准备）**

```bash
python -m venv .venv && source .venv/bin/activate   # macOS/Linux
.venv\Scripts\Activate.ps1                           # Windows PowerShell
uv sync                                               # 按 uv.lock 同步依赖
uv run python demo_decorator.py
```

## 五、最佳实践与常见坑

- **始终用 `functools.wraps`**：除非有意隐藏原函数，否则包装函数一律加 `@wraps`，避免 `__name__`/`__doc__` 丢失导致调试与文档工具异常。
- **保留函数签名**：包装函数用 `*args, **kwargs` 透传，避免写死参数导致装饰器失去通用性；需要精确签名时可配合 `inspect.signature` 或 `functools.wraps` 的 `__wrapped__`。
- **3.14 注解读取坑**：`__dict__.get("__annotations__")` 在 3.14 会静默返回 `{}`。凡是依赖注解做校验/序列化/注册的装饰器，改用 `annotationlib.get_annotations()`，或引入 `typing_extensions` 的跨版本实现；这也是迁移期最常见的「线上空转」故障源。
- **3.14 `partial` 描述符坑**：把 `functools.partial` 对象当作类属性或装饰器使用时，绑定行为改变，需用 `staticmethod(partial(...))` 包裹以维持旧行为。
- **参数校验装饰器的顺序**：多层装饰时注意「外层先执行、内层后执行」，需要控制前置校验与实际执行的先后，避免把校验写到执行之后。
- **不要过度装饰**：装饰器会引入调用链与反射开销，高频热点路径需评估；缓存类装饰器要明确失效策略，避免脏数据。
- **类装饰器的可重复性**：对同一个函数多次应用同一类装饰器要确保幂等，避免 `__wrapped__` 被重复覆盖。

## 六、核心要点速查

1. 装饰器语法由 **PEP 318** 定义，`@deco` 等价于 `func = deco(func)`，`@deco(x)` 等价于 `func = deco(x)(func)`。
2. `functools.wraps` / `functools.update_wrapper` 保留 `__name__`、`__doc__`、`__wrapped__`，是装饰器的标配。
3. 三类形态：函数装饰器、带参装饰器（返回装饰器的闭包）、类装饰器（`__call__`）。
4. 3.14 起 `functools.partial` 是**方法描述符**，作方法/装饰器使用需 `staticmethod()` 包装。
5. 3.14 起注解延迟求值（PEP 649/749），读注解的装饰器改用 `annotationlib.get_annotations(..., format=Format.FORWARDREF)`。
6. `functools.cached_property` 3.8+ 引入，**3.13 起支持泛型**；`functools.lru_cache` 是常用缓存方案。
7. 多装饰器自下而上、由内向外执行，注意执行顺序对校验与日志的影响。
8. 装饰器能力覆盖日志、计时、缓存、鉴权、参数校验、事务与资源管理等横切关注点。

## 七、学习资源

- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 3.14 What's new（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [functools — Function tools（Python 官方标准库文档）](https://docs.python.org/3/library/functools.html)
- [PEP 318 – Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 649 – Deferred Evaluation of Annotations Using Descriptors](https://peps.python.org/pep-0649/)
- [PEP 749 – Annotations for Function and Variable Definitions](https://peps.python.org/pep-0749/)
- [Python documentation by version（python.org 官方版本列表）](https://www.python.org/doc/versions/)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 全景与元编程、版本选型的体系入口
- [[Python-高级特性]] — 装饰器、描述符、元编程等高级主题
- [[Python学习]] — Python 入门与基础学习路径

## 九、变更记录

- 2026-11-19：首次创建。
