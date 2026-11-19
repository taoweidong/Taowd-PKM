---
title: Python函数与作用域
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 函数
  - 作用域
aliases:
  - Python 函数与作用域详解
  - Python 函数定义、参数与作用域
source: 网络资料整理
---

# Python函数与作用域

> [!摘要] 摘要
> 本文系统讲解 Python 中**函数的定义与调用、参数绑定规则、作用域（LEGB）、闭包**，以及 Python 3.12–3.15 对函数与注解的演进（PEP 695 类型参数语法、PEP 570 仅位置参数、PEP 649/749 注解延迟求值、`annotationlib`、`functools.partial` 行为变更、生成器 `throw` 新签名）。内容以截至 2026-11 的官方版本事实为骨架，附可运行示例、常见坑与速查清单，适合刚学完基础语法、需要写可维护函数与理解闭包机制的开发者。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 下列版本号与 PEP 状态均来自调研文件所引官方文档，版本以写作当日官方仓库为准。

- **Python 3.15 是当前最新稳定版本**：3.15.0 于 **2026-10-09** 首发，最新补丁 **3.15.2** 于 **2026-10-25** 以「紧急安全发布」形式推出；Python 3.16 处于预发布阶段（`3.16.0a2`，2026-11-10）。
- **注解延迟求值（PEP 649 / PEP 749，自 Python 3.14 起）**：函数、类、模块的注解不再即时求值，而是保存为 `__annotate__`，按需求值。函数注解相关读取因此发生变化，详见「核心机制」。
- **PEP 695 类型参数语法（Python 3.12 引入）**：函数、类、类型别名可直接声明类型参数，并自动获得 `__type_params__` 属性。**该语法下的类型参数不会进入 `globals()` / `locals()`**，这是与普通变量最易混淆的一点。
- **PEP 570 仅位置参数（`/`、`*`）**：函数签名中 `/` 之前为仅位置参数、`*` 之后为仅关键字参数，是函数参数规则的基础，与 keyword-only 语义共同构成现代函数签名。
- **Python 3.14 起 `functools.partial` 变为方法描述符**：把 `partial` 对象当作方法或装饰器使用时行为有变化，需用 `staticmethod()` 包装以保持旧行为。
- **Python 3.15 起生成器 `throw(type, exc, tb)` / `athrow(...)` 旧签名弃用**，改用单参数形式 `throw(exc)` / `athrow(exc)`。

来源：[Python 3.15 What's new](https://docs.python.org/3.15/whatsnew/3.15.html)、[Python 3.14 What's new](https://docs.python.org/3.14/whatsnew/3.14.html)、[Python 3.12 What's new](https://docs.python.org/3.12/whatsnew/3.12.html)。

## 二、基础概念

**函数**是 Python 中组织代码、复用逻辑与封装行为的第一手段，也是一等对象：可以赋值、作为参数传递、作为返回值返回、放进容器。

- **定义与调用**：`def name(params):` 定义，`name(args)` 调用。`return` 显式返回值；无 `return` 时返回 `None`。函数体是**缩进块**，缩进即语法边界。
- **参数**：形参（定义处）与实参（调用处）按位置或关键字绑定，支持默认值、`*args` 收集位置参数、`**kwargs` 收集关键字参数。
- **作用域**：函数内部创建的变量只在该函数内可见，函数不能直接「看到」外部同名变量——这正是作用域规则要解决的问题。
- **闭包**：内层函数携带对外层函数变量的引用，即使外层函数已返回，这些变量仍可被内层函数访问。
- **命名空间**：作用域的实现机制是命名空间，Python 通过 `locals()`、`globals()`、`nonlocal` 与闭包单元格（cell）共同管理名字查找。

## 三、核心机制

### 3.1 参数绑定规则

Python 的参数绑定按「位置、关键字、默认值、收集参数」组合完成，签名由 PEP 570 奠定基础：

```python
def greet(name, /, *, title="先生", tags=None):
    # name 为仅位置参数；title、tags 为仅关键字参数
    return f"{title} {name}"
```

- `/` 左侧参数只能按位置传，避免调用方用关键字误传；
- `*` 右侧参数只能按关键字传，可提高可读性并防止拼写错误被静默忽略；
- 可变参数：`def f(*args, **kwargs)` 分别收集位置实参与关键字实参。

### 3.2 作用域与 LEGB

Python 的名字查找遵循 **LEGB** 规则：**Local → Enclosing → Global → Built-in**，从内向外逐层查找，找到即停。

- **Local**：函数内部局部作用域，`locals()` 可查看；
- **Enclosing**：外层函数作用域，仅在嵌套函数中可见；
- **Global**：模块级作用域，`globals()` 可查看；
- **Built-in**：内置名字（`len`、`print` 等）。

修改外层作用域的变量必须显式声明：`global` 指向模块级变量，`nonlocal` 指向外层函数变量。**声明只是让赋值指向外层命名空间，不会改变查找顺序。**

### 3.3 函数对象与注解

函数对象自带若干属性：`__name__`、`__doc__`、`__module__`、`__annotations__`、`__wrapped__` 等。`functools.wraps` / `functools.update_wrapper` 用于在装饰器中保留这些元信息。

**注解延迟求值（PEP 649/749，3.14 起）**：函数/类/模块的注解不再即时求值，而是存为 `__annotate__`，按需求值。因此 3.14 起**直接从 `__dict__` 读取 `__annotations__` 可能返回空 `{}`（不报错、不警告）**，读取注解的库应改用 `annotationlib.get_annotations()`：

```python
import annotationlib

def add(a: int, b: int) -> int:
    return a + b

ann = annotationlib.get_annotations(add, format=annotationlib.Format.VALUE)
# {'a': int, 'b': int, 'return': int}
```

`format` 支持 `Format.VALUE`（求值后返回）、`Format.FORWARDREF`（前向引用转为特殊对象）、`Format.STRING`（返回字符串）。第三方包 `typing_extensions` 提供跨版本兼容实现。

### 3.4 类型参数语法（PEP 695，3.12）

```python
def first[T](items: list[T]) -> T:
    return items[0]
```

类型参数 `T` 是函数签名的一部分，**不会进入 `globals()` / `locals()`**，且不再需要显式声明协变/逆变，由类型检查器根据使用方式推断。

### 3.5 生成器函数与 throw

含 `yield` 的函数返回生成器，调用时不立即执行，而是每次 `next()` 推进到下一个 `yield`。`throw()` 用于向生成器内部注入异常。**3.15 起旧的三参数签名 `throw(type, exc, tb)` 弃用，改用单参数 `throw(exc)`。**

## 四、实践步骤（含代码示例）

**示例 1：多种参数形式**

```python
def build_profile(name, /, *, age=18, roles=(), **meta):
    """演示仅位置、仅关键字、默认值与 **kwargs。"""
    profile = {"name": name, "age": age, "roles": list(roles)}
    profile.update(meta)
    return profile

print(build_profile("陶伟东", age=30, roles=["dev"], city="杭州"))
```

**示例 2：作用域与 global / nonlocal**

```python
counter = 0  # 模块级（Global）

def make_counter():
    total = 0  # Enclosing

    def incr(step=1):
        global counter
        nonlocal total
        counter += 1        # 修改全局
        total += step       # 修改外层函数变量
        return total

    return incr

c = make_counter()
c(); c(5)
print(counter, "全局累加：", counter)
```

**示例 3：闭包工厂（注意延迟绑定坑）**

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor   # 捕获外层 factor（cell 变量）

    return multiply

times3 = make_multiplier(3)
print(times3(10))  # 30
```

**示例 4：类型参数与注解延迟求值**

```python
from __future__ import annotations

def describe[T](value: T) -> str:
    return f"值：{value!r}（类型 {type(value).__name__}）"

import annotationlib
print(annotationlib.get_annotations(describe, format=annotationlib.Format.STRING))
```

**示例 5：生成器注入异常**

```python
def stream():
    try:
        yield 1
        yield 2
    except ValueError as exc:
        yield f"捕获：{exc}"

g = stream()
print(next(g))          # 1
g.throw(ValueError("出错"))   # 3.15 起用单参数形式
```

**验证命令**：可用 `python -m py_compile` 或测试运行：

```bash
python -m py_compile Python函数与作用域_demo.py   # 仅做语法检查
```

## 五、最佳实践与常见坑

- **可变默认参数是经典陷阱**：`def f(items=[])` 的默认值在函数定义时创建并被所有调用共享，应写成 `def f(items=None): items = items or []`。
- **不要随意用 `global`/`nonlocal` 掩盖作用域问题**：优先通过参数传递、返回值或封装对象来共享状态；确需修改外层变量时再声明。
- **闭包延迟绑定**：在循环中定义闭包并返回，内层函数引用的循环变量会指向循环结束后的值，需用默认参数「立即绑定」：`lambda i=i: ...`。
- **3.14 起直接读 `__annotations__` 可能拿到空 `{}`**：校验、序列化、ORM 字段注册等运行时读取注解的逻辑，应改用 `annotationlib.get_annotations()`，否则可能「空转」而不报错。
- **`functools.partial` 作为方法/装饰器的行为变化（3.14 起）**：`partial` 变为方法描述符，用其做方法或装饰器时需 `staticmethod()` 包装以保持旧行为。
- **生成器 `throw` 签名**：3.15 起使用单参数 `throw(exc)`，旧三参数形式已弃用。
- **类型参数不要当普通变量**：PEP 695 的类型参数不进入 `globals()` / `locals()`，不要在函数体内对其赋值或当作运行时变量。
- **`lambda` 保持短小**：`lambda` 是表达式而非语句，只适合做简单转换，复杂逻辑应写 `def` 以保证可读性与可调试性。

## 六、核心要点速查

1. 函数是**一等对象**，定义用 `def`，`return` 决定返回值，无 `return` 返回 `None`。
2. 参数绑定靠位置与关键字；`/` 左侧仅位置、`*` 右侧仅关键字（PEP 570）。
3. 名字查找遵循 **LEGB**：Local → Enclosing → Global → Built-in。
4. 修改全局用 `global`，修改外层函数变量用 `nonlocal`。
5. 闭包通过 cell 持有外层变量；循环中定义闭包要注意延迟绑定。
6. **可变默认参数**需用 `None` 加内部初始化规避共享。
7. **PEP 695（3.12）**：`def f[T](...)` 类型参数语法，类型参数不进 `locals()`/`globals()`。
8. **PEP 649/749（3.14）**：注解延迟求值，存为 `__annotate__`；读注解用 `annotationlib.get_annotations()`，直读 `__annotations__` 可能得空 `{}`。
9. **3.14 起** `functools.partial` 是方法描述符，作方法/装饰器需 `staticmethod()` 包装。
10. **3.15 起** 生成器 `throw(exc)` 单参数；旧 `throw(type, exc, tb)` 弃用。
11. 3.14 起 `from __future__ import annotations` 被标记弃用（官方表示不会在 3.13 EOL（2029）前移除），新代码可逐步移除。
12. 装饰器场景用 `functools.wraps` 保留 `__name__` / `__doc__` / `__wrapped__`。

## 七、学习资源

- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 3.14 What's new（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Python 3.12 What's new（Python 官方文档）](https://docs.python.org/3.12/whatsnew/3.12.html)
- [The Python language reference（官方语言参考）](https://docs.python.org/3/reference/)
- [The standard type hierarchy（官方文档，含函数/命名空间）](https://docs.python.org/3/reference/datamodel.html)
- [PEP 649 – Deferred evaluation of annotations](https://peps.python.org/pep-0649/)
- [PEP 695 – Syntax for generic functions and types](https://peps.python.org/pep-0695/)
- [PEP 570 – Python positional-only parameters](https://peps.python.org/pep-0570/)
- [annotationlib（Python 官方库文档）](https://docs.python.org/3.14/library/annotationlib.html)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 全景总览，函数与作用域的上游主题
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 装饰器、元编程、类型等函数进阶主题
- [[编程语言]] — 跨语言的函数与作用域对比视角

## 九、变更记录

- 2026-11-19：首次创建。
