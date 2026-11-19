---
title: Python 数据类型与内置函数
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 数据类型
  - 内置函数
aliases:
  - Python 数据类型
  - Python 内置函数
source: 网络资料整理
---

# Python 数据类型与内置函数

> [!摘要] 摘要
> 本文系统梳理 Python 的内置数据类型体系与内置函数的使用机制，覆盖数值/序列/集合/映射/布尔等类型的分类与可变性、3.15 新增的 `frozendict` 与 `sentinel` 等新类型，以及 `len`、`enumerate`、`zip`、`map`、`filter`、`sorted` 等高频内置函数的语义与典型用法。配合完整可运行示例、最佳实践与常见坑，帮助读者从「知道有哪些类型和函数」落到「能正确、高效地使用」。定位为 [[Python-从入门到精通]] 体系中「语言基础」层面的入门必修篇，衔接类型注解、函数与作用域等进阶主题。

## 一、最新动态（截至 2026-11）

- **Python 3.15.0（2026-10-09 首发）为当前最新稳定版**，最新维护版 **3.15.2** 于 **2026-10-25** 发布（属紧急安全发布）；3.16 处于预发布阶段（`3.16.0a2`，2026-11-10）。
- **PEP 814：新增内置 `frozendict`**。不可变、**非 `dict` 子类**（直接继承 `object`）；键与值均可哈希时整个对象可哈希；保留插入顺序，但比较**忽略顺序**（`frozendict(x=1, y=2) == frozendict(y=2, x=1)` 为 `True`）。
- **PEP 661：新增内置 `sentinel` 类型**，用于创建唯一哨兵值，语义清晰、可保留标识、可在类型表达式中用 `|` 组合，且可被 pickle。
- **PEP 798：推导式支持解包**。列表/集合/字典推导式与生成器表达式支持 `*`、`**`，等价于嵌套推导式或 `itertools.chain`，如 `[*L for L in lists]`、`{**d for d in dicts}`。
- **3.15 起 `re.match()` / `re.Pattern.match()` 被软弃用**，新增更明确的 `re.prefixmatch()` / `re.Pattern.prefixmatch()`；旧名不会移除。
- **3.15 起 `struct` 的 `'F'` / `'D'` 格式码软弃用**，改用 `'Zf'` / `'Zd'`。
- **`typing.ByteString` / `collections.abc.ByteString` 计划在 Python 3.17 移除**，运行时判断缓冲协议应使用 `isinstance(obj, collections.abc.Buffer)`（3.12 起可用）。
- 来源：[Python 3.15 What's new](https://docs.python.org/3.15/whatsnew/3.15.html)、[Python 3.14 What's new](https://docs.python.org/3.14/whatsnew/3.14.html)、[PEP 814](https://peps.python.org/pep-0814/)、[PEP 661](https://peps.python.org/pep-0661/)。

## 二、基础概念

**内置数据类型**是无需导入即可直接使用的类型，按用途可归为几类：

- **数值**：`int`（任意精度整数）、`float`（IEEE 754 双精度）、`complex`。
- **序列**：`str`、`list`、`tuple`、`range`、`bytes`、`bytearray`、`memoryview`。
- **集合**：`set`、`frozenset`。
- **映射**：`dict`，以及 3.15 新增的 `frozendict`。
- **其他**：`bool`（`True`/`False`，是 `int` 的子类）、`NoneType`（唯一值 `None`）、`ellipsis`（`...`）。

两个核心维度必须分清：

- **可变性（mutability）**：`list`、`dict`、`set`、`bytearray` 可变；`int`、`float`、`complex`、`str`、`tuple`、`frozenset`、`bytes`、`frozendict` 不可变。不可变类型可作字典键、集合元素（元素需可哈希）。
- **可哈希性（hashability）**：可哈希才能作为键或集合成员。`tuple` 在元素均可哈希时可哈希；含可变元素的 `list`/`dict` 不可哈希。`frozendict` 键值均可哈希时整体可哈希。

数值类型还有两条容易忽略的语义：`int` 是**任意精度整数**，不存在其他语言中的整数溢出，超大数可安全参与运算；`bool` 是 `int` 的子类，`True` 可当作 `1`、`False` 当作 `0` 参与算术与排序，因此涉及布尔的逻辑判断应优先用 `is` 而非数值比较。`bytes` 与 `str` 分属二进制与文本两个世界，混用会直接报 `TypeError`。

**内置函数（built-in functions）**是解释器启动即提供、无需导入的函数，如 `len`、`print`、`range`、`sorted`、`isinstance` 等，通过 `builtins` 模块暴露。它们与内置类型共同构成 Python 表达数据的最小工具集，也是「鸭子类型」的实现基础——对象以行为而非继承被使用。

## 三、核心机制

**1. 类型判断与转换**

`isinstance(obj, cls)` 判断实例关系，`issubclass(cls, base)` 判断类继承关系；3.15 下判断「可能是映射」应写 `isinstance(arg, (dict, frozendict))`，或更通用的 `isinstance(arg, collections.abc.Mapping)`。类型转换用 `int()`、`float()`、`str()`、`bytes()`、`bool()`、`list()`、`tuple()`、`set()`、`frozenset()`。

**2. `frozendict` 的机制要点**

`frozendict` 不是 `dict` 的子类，因此**不会**被 `isinstance(x, dict)` 识别为字典；标准库 `copy`、`decimal`、`json`、`marshal`、`pickle`、`pprint`、`xml.etree.ElementTree`、`plistlib`（仅序列化）已更新为可接受它；`eval()`/`exec()` 的 `globals`、`type()` 与 `str.maketrans()` 的 `dict` 参数也接受它。它适合作为不可变的映射配置、缓存键与常量表。

**3. `sentinel` 哨兵机制**

传统写法常用 `None` 或自定义对象作「缺省哨兵」，但 `None` 可能与真实值冲突。`sentinel` 提供语言级唯一哨兵：

```python
MISSING = sentinel('MISSING')  # 3.15 内置，无需导入

def get(data, key, default=MISSING):
    return data[key] if key in data else default

print(get({"a": 1}, "a"))              # 1
print(get({"a": 1}, "b", 0))           # 0
print(get({"a": 1}, "b") is MISSING)  # True：用 is 做身份判断
```

**4. 内置函数的通用机制**

- **长度与遍历**：`len()` 返回元素数或字段数，支持所有有 `__len__` 的对象。
- **带索引遍历**：`enumerate(iterable, start=0)` 同时产出索引与值；`range(stop)` / `range(start, stop, step)` 生成不可变整数序列，节省内存。
- **并行遍历**：`zip(*iterables)` 按最短者截断（`strict=True` 可强制等长）。
- **惰性变换**：`map()`、`filter()`、生成器表达式返回迭代器，需显式 `list()` 才求值。
- **排序**：`sorted()` 返回新列表，`list.sort()` 原地排序；二者均接受 `key`、`reverse`。
- **聚合判断**：`sum`、`min`、`max`、`any`、`all`。
- **属性与反射**：`getattr`、`setattr`、`hasattr`、`vars`、`dir`、`repr`、`object`。

## 四、实践步骤（含代码/命令示例）

**1. 类型判断与映射处理**

```python
from collections.abc import Mapping

data = {"a": 1, "b": 2}
config = frozendict({"host": "localhost", "port": 8080})  # 3.15 内置

print(isinstance(data, Mapping))          # True
print(isinstance(config, (dict, frozendict)))  # True
print(isinstance(config, dict))          # False：frozendict 不是 dict 子类
print(hash(config))                      # 键值均可哈希时可哈希
```

**2. 内置函数组合使用**

```python
students = [("张三", 92), ("李四", 78), ("王五", 85)]

# 按分数降序取前两名
top2 = sorted(students, key=lambda s: s[1], reverse=True)[:2]

# enumerate 带索引遍历
for idx, (name, score) in enumerate(students, start=1):
    print(idx, name, score)

# zip 并行遍历
names = [s[0] for s in students]
scores = [s[1] for s in students]
for name, score in zip(names, scores, strict=True):
    print(f"{name}: {score}")

# map/filter 惰性求值
passed = list(filter(lambda s: s >= 60, scores))
doubled = list(map(lambda x: x * 2, scores))
print(passed, doubled, top2)
```

**3. 3.15 解包推导式**

```python
lists = [[1, 2], [3, 4], [5]]
flat = [*lst for lst in lists]      # 等价于 [x for lst in lists for x in lst]
dicts = [{"a": 1}, {"b": 2}]
merged = {**d for d in dicts}       # {"a": 1, "b": 2}
print(flat, merged)
```

**4. 命令行验证类型**

```bash
python -c "x = frozendict({'a':1}); print(type(x).__mro__)"
python -c "import collections.abc as cabc; print(isinstance(memoryview(b'ab'), cabc.Buffer), isinstance(bytearray(b'ab'), cabc.Buffer))"
```

## 五、最佳实践与常见坑

- **用 `Mapping` 而非 `dict` 做参数判断**：接收外部数据时写 `isinstance(arg, (dict, frozendict))` 或 `collections.abc.Mapping`，避免遗漏 `frozendict` 与第三方映射类型。
- **`dict` 与 `frozendict` 不通用**：`isinstance(x, dict)` 对 `frozendict` 为 `False`；不要把 `frozendict` 直接传给只认 `dict` 的旧库。
- **不要依赖 `None` 作哨兵**：当 `None` 是合法业务值时会冲突，改用 `sentinel` 或自定义 `object()`。
- **注意 `zip` 的截断语义**：默认按最短者截断，容易在并行遍历中静默丢数据；需要等长校验时用 `zip(..., strict=True)`。
- **`map`/`filter`/推导式是惰性的**：忘记 `list()` 会得到迭代器而非结果，调试时先转成列表。
- **`sorted` 与 `list.sort` 别混用**：前者返回新列表，后者原地修改并返回 `None`，`a = b.sort()` 会得到 `None`。
- **警惕 `bool` 是 `int` 的子类**：`True == 1` 为 `True`，用 `is` 判断布尔值、用显式类型判断避免隐式等价带来的逻辑漏洞。
- **3.15 编码与弃用**：默认编码已改为 UTF-8（PEP 686），文件读写仍建议显式传 `encoding="utf-8"` 保证跨版本兼容。

## 六、核心要点速查

1. Python 内置类型可归为数值、序列、集合、映射、布尔/`None` 几类；核心维度是**可变性**与**可哈希性**。
2. 不可变类型（`int`/`str`/`tuple`/`frozenset`/`bytes`/`frozendict`）可作字典键或集合元素。
3. 3.15 新增 **`frozendict`（PEP 814）**：不可变、非 `dict` 子类、比较忽略顺序、可哈希。
4. 3.15 新增 **`sentinel`（PEP 661）**，是语言级唯一哨兵值。
5. 3.15 推导式支持 **`*` / `**` 解包（PEP 798）**。
6. 判断映射优先用 `isinstance(x, (dict, frozendict))` 或 `collections.abc.Mapping`。
7. `isinstance` 判实例、`issubclass` 判类；缓冲协议用 `collections.abc.Buffer`（3.12+）。
8. 高频内置函数：`len`、`enumerate`、`zip`、`map`、`filter`、`sorted`、`reversed`、`sum`、`min`、`max`、`any`、`all`、`getattr`、`setattr`。
9. `zip` 默认按最短截断，`strict=True` 可强制等长；`sorted` 返回新列表，`list.sort` 原地排序。
10. `typing.ByteString` / `collections.abc.ByteString` 计划在 **3.17 移除**，改用 `collections.abc.Buffer`。

## 七、学习资源

- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 内置类型（官方教程）](https://docs.python.org/3/tutorial/datastructures.html)
- [Python 内置函数 reference（官方文档）](https://docs.python.org/3/library/functions.html)
- [collections.abc 抽象基类（官方文档）](https://docs.python.org/3/library/collections.abc.html)
- [PEP 814 – Add a frozendict built-in type](https://peps.python.org/pep-0814/)
- [PEP 661 – Sentinel object](https://peps.python.org/pep-0661/)
- [PEP 798 – Unpacking in comprehensions](https://peps.python.org/pep-0798/)

## 八、关联笔记

- [[Python-从入门到精通]] — 本知识点在 Python 体系中的总览与定位
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 类型系统、装饰器等进阶主题，承接本篇基础

## 九、变更记录

- 2026-11-19：首次创建。
