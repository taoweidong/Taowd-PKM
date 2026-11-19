---
title: Python 语法基础
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 语法基础
aliases:
  - Python 语法
  - Python 基础语法
source: 网络资料整理
---

# Python 语法基础

> [!摘要] 摘要
> 本文聚焦 Python 的**语言语法层**：从变量、运算符、控制流、函数、数据结构到迭代器/生成器、异常与注解，讲清每一块在**当前版本（Python 3.15 为稳定主线）下的正确写法**。适合刚入门 Python、需要快速补齐语法地基，或从旧版本迁移、想确认哪些语法已随版本变化（如 `match/case`、PEP 695 类型参数、PEP 798 解包推导式、注解延迟求值）的读者。结构按「最新动态 → 基础概念 → 核心机制 → 实践步骤 → 最佳实践与常见坑 → 速查 → 资源 → 关联笔记」展开，是 [[Python-从入门到精通]] 中「入门篇」的语法子集。

## 一、最新动态（截至 2026-11）

语法基础层面的版本事实如下，全部来自调研文件，版本号与日期以官方发布页为准：

- **当前最新稳定版是 Python 3.15**（首发于 **2026-10-09**，最新补丁 **3.15.2** 于 **2026-10-25** 作为紧急安全发布）。**Python 3.16 处于预发布阶段**（`3.16.0a2`，2026-11-10）。
- **3.15 对语法层的直接影响**：新增 **PEP 798 解包推导式**，列表/集合/字典推导式与生成器表达式可使用 `*`、`**` 解包；新增内置 **`frozendict`（PEP 814）**、**`sentinel`（PEP 661）**；**UTF-8 成为默认编码（PEP 686）**。
- **关键语法的引入版本**：`match/case` 结构式匹配自 **3.10** 引入；**PEP 695 类型参数语法**（`def f[T](x: T)`）自 **3.12** 引入，**3.13** 引入 `TypeAlias` 简化；**3.14** 起注解改为延迟求值（PEP 649/749）。
- **弃用提醒**：**3.14 起 `from __future__ import annotations` 被标记弃用**，新代码应逐步移除该导入；官方明确不会在 3.13（EOL 2029）到期前移除。**3.15 起生成器 `throw(type, exc, tb)` 旧签名弃用**，改用单参数 `throw(exc)` / `athrow(exc)`。**3.14 起 `functools.partial` 变为方法描述符**，作为方法/装饰器使用时需用 `staticmethod()` 包装以保持旧行为。

| 语法特性 | 引入/变更版本 | 对应 PEP |
| --- | --- | --- |
| `match` / `case` | 3.10 | PEP 634–636 |
| 类型参数语法 `def f[T](x: T)` | 3.12 | PEP 695 |
| `type X = ...` 别名 | 3.12 / 3.13 简化 | PEP 695 |
| 注解延迟求值 | 3.14 | PEP 649 / 749 |
| `functools.partial` 方法描述符 | 3.14 | 行为变更 |
| `*`、`**` 解包推导式 | 3.15 | PEP 798 |
| `frozendict`、`sentinel` | 3.15 | PEP 814 / 661 |
| UTF-8 默认编码 | 3.15 | PEP 686 |

## 二、基础概念

- **动态、强类型语言**：变量无需声明类型，但对象自带类型；类型在运行期确定。类型注解（`x: int`）只是**静态提示**，不改变运行期行为。
- **缩进即语法**：代码块不使用括号或花括号，靠缩进分组。缩进必须一致（推荐 4 空格），重命名或搬移代码时最容易出错的就是缩进层级。
- **鸭子类型**：对象以行为而非继承被使用，`duck typing` 贯穿整个生态，与类型注解互补而非对立。
- **一切皆对象**：函数、类、模块、代码块都是对象，可赋值、可传递、可返回；变量本质是**名字绑定到对象的引用**，不是存储值的盒子。
- **解释执行与运行模型**：Python 默认解释执行，GIL（全局解释器锁）限制同一进程内同时执行字节码的线程数。语法学习阶段先建立这一心智模型，后续并发与性能主题才不突兀。
- **命名规则**：标识符由字母、数字、下划线组成，不能以数字开头；区分大小写。约定俗成：`snake_case` 用于变量/函数/模块，`CamelCase` 用于类。

## 三、核心机制

### 变量、赋值与运算符

赋值是**绑定**而非拷贝；对可变对象（`list`、`dict`、`set`）做赋值或传参时，传递的是同一引用。

```python
a = 10
b = a            # b 与 a 指向同一个 int 对象
lst = [1, 2, 3]
ref = lst
ref.append(4)    # lst 同步变成 [1, 2, 3, 4]
```

常用运算符：算术（`+ - * / // % **`）、比较（`== != < >`，可链式 `1 < x <= 10`）、逻辑（`and or not`）、集合运算（`in`、`not in`）、赋值与增强赋值（`x += 1`）、海象运算符 `:=`（在表达式中赋值，常用于 `while` 中简化读取）。

```python
import math

# 海象运算符：读取并判断
while (chunk := math.sqrt(n)) > 10:
    n = chunk ** 2
```

### 控制流

条件与循环：

```python
score = 88
if score >= 90:
    grade = "A"
elif score >= 60:
    grade = "B"
else:
    grade = "C"

for i in range(5):
    print(i)
```

`match/case`（3.10+）做结构式匹配，匹配的是**值/结构**而非顺序：

```python
command = "start"
match command:
    case "start":
        print("启动")
    case "stop":
        print("停止")
    case ["move", x, y]:      # 列表结构匹配
        print(f"移动到 {x}, {y}")
    case _:
        print("未知命令")
```

### 函数与参数

函数定义用 `def`。参数分隔符决定传参方式：`/` 之前为仅位置参数，`*` 之后为仅关键字参数，这是 PEP 570 的语义基础。

```python
def greet(name, /, *, greeting="你好", punct=True):
    return f"{greeting}{name}{'！' if punct else ''}"
```

- 默认参数应使用**不可变对象**，否则所有调用共享同一对象。
- `*args` 收集位置参数，`**kwargs` 收集关键字参数。
- 3.12+ 可用 PEP 695 泛型语法声明类型参数。

```python
def first[T](items: list[T]) -> T:
    return items[0]
```

### 数据结构与推导式

`list`（有序可变）、`tuple`（有序不可变）、`set`（无序唯一）、`dict`（键值映射，3.7+ 保持插入顺序）是语法层最常用的四种容器。推导式是 Python 表达数据转换的惯用方式：

```python
squares = [x * x for x in range(10) if x % 2 == 0]
keys = {k for k, v in {"a": 1, "b": 2}.items() if v > 1}
pairs = {k: v for k, v in {"a": 1, "b": 2, "c": 3}.items() if v % 2}
```

**3.15（PEP 798）新增解包推导式**，可把多个列表/字典合并进一个推导式，等价于嵌套推导式或 `itertools.chain`：

```python
lists = [[1, 2], [3], [4, 5]]
flat = [*L for L in lists]        # [1, 2, 3, 4, 5]
dicts = [{"a": 1}, {"b": 2}]
merged = {**d for d in dicts}     # {"a": 1, "b": 2}
```

### 迭代器与生成器

`for` 循环遍历的是**可迭代对象**；`iter()` 返回迭代器，`next()` 取下一个值，耗尽抛 `StopIteration`。带 `yield` 的函数是**生成器**，可暂停与恢复，是惰性、低内存处理大序列的基础。

```python
def countdown(n: int):
    while n > 0:
        yield n
        n -= 1

for v in countdown(3):
    print(v)          # 3 2 1
```

`yield from` 委托给另一个可迭代对象；**PEP 479** 规定生成器内部冒出的 `StopIteration` 会转成 `RuntimeError`。

### 异常处理

```python
try:
    value = int("abc")
except ValueError as e:
    print(f"转换失败：{e}")
except (TypeError, KeyError) as e:
    print(f"其他错误：{e}")
else:
    print(f"成功：{value}")
finally:
    print("清理逻辑")
```

**PEP 654（3.11）** 提供异常组与 `except*`；**PEP 765（3.14）** 禁止在 `finally` 中用 `return`/`break`/`continue` 跳出，**3.14 起仅发出 `SyntaxWarning`（不是立即报错）**，语言规范允许未来升级为 `SyntaxError`。

### 注解的延迟求值

**3.14 起（PEP 649/749）函数/类/模块的注解不再即时求值**，而是存为 `__annotate__`，按需求值，且**直接从 `__dict__` 读 `__annotations__` 会静默返回空 `{}`**（不报错、不警告）。运行期需要读注解时应使用：

```python
import annotationlib

annotations = annotationlib.get_annotations(func, format=annotationlib.Format.VALUE)
```

## 四、实践步骤（含代码/命令示例）

**第 1 步：确认版本并准备环境**

```bash
python --version          # 建议 3.13+，当前稳定主线为 3.15
python -m venv .venv       # 标准库创建隔离环境
```

**第 2 步：写一个覆盖核心语法的可运行脚本**

```python
"""语法基础综合示例：变量、数据结构、函数、生成器、异常。"""

def safe_divide(a: float, b: float) -> float:
    """带异常处理的除法。"""
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b


def fib(limit: int):
    """生成不超过 limit 的斐波那契数列。"""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


def main() -> None:
    numbers = [x * x for x in range(5)]
    print("平方：", numbers)
    print("斐波那契：", list(fib(10)))

    try:
        print("结果：", safe_divide(10, 0))
    except ValueError as exc:
        print("已捕获：", exc)


if __name__ == "__main__":
    main()
```

运行：

```bash
python syntax_basics.py
```

**第 3 步：用静态检查确认语法与注解无误**

```bash
uv run mypy --strict syntax_basics.py    # 或 python -m mypy --strict syntax_basics.py
```

## 五、最佳实践与常见坑

- **不要在 `finally` 中写 `return/break/continue`**：3.14 起是 `SyntaxWarning`，属于明确的未来移除方向，应主动改写。
- **谨慎使用 `from __future__ import annotations`**：已被标记弃用，新代码在 3.14+ 可直接移除；但为兼容 3.13 及更早版本，迁移期可暂留。
- **不要直接读 `__annotations__`**：3.14+ 会静默返回 `{}`，依赖注解的库（数据校验、序列化、ORM 字段注册）应改用 `annotationlib.get_annotations(..., format=Format.FORWARDREF)` 或 `typing_extensions` 的跨版本实现。
- **避免可变默认参数**：`def f(items=[])` 会让所有调用共享同一个列表，改为 `None` 并在函数体内初始化。
- **区分 `==` 与 `is`**：`==` 比较值，`is` 比较对象身份；判断单例（如 `None`、小整数、字符串驻留）用 `is`。
- **`frozendict` 不是 `dict` 子类**（3.15 PEP 814）：判断时应写 `isinstance(arg, (dict, frozendict))` 或 `isinstance(arg, collections.abc.Mapping)`，不要写成 `isinstance(arg, dict)`。
- **优先用推导式而非逐行 `append`**：语义更清晰、通常更快；大数据集用生成器表达式保持惰性。
- **异常处理要具体**：不要裸 `except:`，捕获过宽会掩盖真实错误；清理逻辑放入 `finally`。
- **版本时效性**：本文版本信息截至 2026-11，第三方与补丁版本更新频繁，落地时以写作当日的官方发布页为准。

## 六、核心要点速查

1. Python 3.15 是当前稳定主线（3.15.0 于 2026-10-09，3.15.2 于 2026-10-25）；3.16 处于预发布（`3.16.0a2`，2026-11-10）。
2. 缩进即语法，标识符区分大小写，变量是「名字绑定对象」的引用。
3. `match/case` 自 3.10 引入，做的是值/结构匹配。
4. PEP 695 类型参数语法（`def f[T](x: T)`）自 3.12 引入。
5. 函数参数用 `/`（仅位置）与 `*`（仅关键字）分隔；默认参数避免可变对象。
6. 3.15（PEP 798）支持解包推导式：`[*L for L in lists]`、`{**d for d in dicts}`。
7. 3.15 新增内置 `frozendict`（PEP 814）与 `sentinel`（PEP 661）；`frozendict` 不是 `dict` 子类。
8. 3.15（PEP 686）默认编码为 UTF-8，与系统环境无关。
9. 3.14（PEP 649/749）注解延迟求值，直接读 `__annotations__` 会返回空 `{}`，应改用 `annotationlib`。
10. 3.14 起 `from __future__ import annotations` 弃用；`functools.partial` 变为方法描述符。
11. PEP 765（3.14）：`finally` 中禁止 `return/break/continue`，当前仅 `SyntaxWarning`。
12. 3.15 生成器 `throw()` 旧三参数签名弃用，改用单参数 `throw(exc)`。

## 七、学习资源

**官方文档（权威事实来源）**

- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 3.14 What's new（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Python 3.13 What's new（Python 官方文档）](https://docs.python.org/3.13/whatsnew/3.13.html)
- [The Python Language Reference（语言参考）](https://docs.python.org/3/reference/)
- [Python documentation by version（python.org 官方版本列表）](https://www.python.org/doc/versions/)
- [PEP 695 – Generic function and type syntax（PEP 原文）](https://peps.python.org/pep-0695/)
- [PEP 649 / PEP 749 – Deferred evaluation of annotations（PEP 原文）](https://peps.python.org/pep-0649/)

## 八、关联笔记

- [[Python-从入门到精通]] — 本知识点所属的主题总览，串联入门到精通的完整路径
- [[Python学习]] — Python 入门与基础学习路径，与本文语法部分互补

## 九、变更记录

- 2026-11-19：首次创建。
