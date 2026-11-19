---
title: Python面向对象编程
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 面向对象
  - 元类与描述符
aliases:
  - Python OOP
  - Python 面向对象
source: 网络资料整理
---

# Python面向对象编程

> [!摘要] 摘要
> 本文系统梳理 Python 面向对象编程（OOP）的知识体系与落地方法，覆盖类与对象、继承与多态、属性管理（`__slots__`/`@property`/描述符）、抽象基类与数据类、元类等核心机制，并结合截至 2026-11 的语言演进（PEP 705/767 只读限定、PEP 649/749 注解延迟求值对元类与装饰器的影响）说明新版本下的写法变化。面向已掌握 Python 基础语法、希望把 OOP 写规范、写可维护的开发者，结构按「最新动态 → 基础概念 → 核心机制 → 实践步骤 → 最佳实践 → 速查 → 资源 → 关联笔记」展开。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本与 PEP 状态均来自官方文档，关键版本号以官方发布页为准。

- **Python 3.15 是当前最新稳定版本**：`3.15.0` 于 **2026-10-09** 首发，最新补丁 **`3.15.2`** 于 **2026-10-25** 发布（紧急安全发布）；`3.16.0a2` 处于预发布阶段（2026-11-10，计划 2027-10-06 首发）。**3.14.0** 于 **2025-10-07** 发布，当前维护版为 `3.14.10`。
- **只读属性限定符扩展（PEP 767）**：`typing.ReadOnly` 由 **PEP 705** 在 **Python 3.13** 引入时仅用于 `TypedDict` 项；**PEP 767** 将其扩展为**类属性与协议属性的合法限定符**，可与 `ClassVar` 组合使用，并可作为「仅初始化一次」的 flyweight 默认值。**注意与 `__slots__` 冲突**：带类级初始值的只读属性不能进入 `slots`。
- **注解延迟求值影响元类行为（PEP 649/749，Python 3.14）**：类与函数的注解不再即时求值，而是存为 `__annotate__` 按需取值。元类中若自行处理 `__annotations__`，需注意其变得更「惰性」；**直接从 `__dict__` 读 `__annotations__` 在 3.14 会静默返回空 `{}`**。
- **类型系统现代化**：**PEP 644/695** 推进泛型类、协议、类型别名的现代化；**`types.UnionType` 在 3.14 成为 `typing.Union` 的别名**，会改变部分行为，编写泛型类与协议时需留意。
- **安全调试接口（PEP 768，Python 3.14）**：`sys.remote_exec(pid, script)` 支持零开销地附着到运行中的进程，便于排查动态对象、元类等运行时行为；可用 `PYTHON_DISABLE_REMOTE_DEBUG`、`-X disable-remote-debug` 关闭。
- **生态与工具**：mypy **2.4**（2026-10-01）、pyright **1.1.413**（2026-08-14），均可对 OOP 的泛型与 `Protocol` 做静态检查，建议与 IDE 深度集成。

## 二、基础概念

- **类与对象**：类是蓝图（模板），对象是按蓝图创建的实例。`class` 关键字定义类，`__init__` 负责初始化实例状态。
- **封装**：以约定区分「公开」与「内部」：单下划线 `_name` 表示受保护、双下划线 `__name` 触发**名称改写**（`_类名__name`）以减少子类意外覆盖。Python 不强制访问控制，靠约定与 `@property` 保护数据。
- **继承与多态**：子类复用父类行为，并可覆写方法；Python 采用**鸭子类型**——对象以行为被使用，而非依赖继承关系。
- **特殊方法（dunder）**：以双下划线包裹的方法（如 `__init__`、`__len__`、`__repr__`、`__eq__`）定义对象的内建行为，是 Python 数据模型的核心。
- **类属性与实例属性**：类属性存于类命名空间，被所有实例共享；实例属性存于实例 `__dict__`，各实例独立。
- **描述符**：实现了 `__get__`/`__set__`/`__delete__` 的对象；`@property`、`__slots__` 底层都依赖描述符机制。

## 三、核心机制

**属性查找与 MRO**

Python 按「实例 → 类 → 基类」顺序查找属性，多继承时使用 **C3 线性化（MRO）** 决定顺序，可用 `Class.mro()` 查看。

```python
class A:
    def who(self):
        return "A"

class B(A):
    pass

class C(A):
    def who(self):
        return "C"

class D(B, C):
    pass

print([c.__name__ for c in D.mro()])  # ['D', 'B', 'C', 'A', 'object']
print(D().who())                       # C
```

**`__new__` 与 `__init__`**

`__new__` 负责**创建**对象（返回实例），`__init__` 负责**初始化**。不可变对象、单例、元类常重写 `__new__`。

**属性管理三件套**

- `@property`：把方法变成可读写属性，配合 `@x.setter` 做受控访问。
- `__slots__`：禁止实例拥有 `__dict__`，节省内存并防止动态加属性；**与带类级初始值的只读属性冲突**（PEP 767）。
- `__getattr__`/`__getattribute__`/`__setattr__`：在查找/赋值前后做拦截，适合懒加载、校验。

**抽象基类与数据类**

`abc.ABC` + `@abstractmethod` 定义接口契约；`@dataclass` 自动生成 `__init__`/`__repr__`/`__eq__`，是纯数据载体的现代写法。

**元类**

元类是「创建类的类」，默认是 `type`。典型用途：注册子类、校验类定义、注入方法。`class Meta(type)` 后在类定义中写 `metaclass=Meta`。

**类型注解对 OOP 的影响**

泛型类用 PEP 695 语法 `class Box[T]:`；`Protocol` 定义结构化类型；只读属性用 `typing.ReadOnly`（PEP 705/767）。

## 四、实践步骤（含代码/命令示例）

**1. 定义类并实例化**

```python
class Account:
    bank = "示例银行"          # 类属性

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner     # 实例属性
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("存款必须为正数")
        self._balance += amount

    def __repr__(self) -> str:
        return f"Account({self.owner!r}, {self._balance})"


acc = Account("陶伟东", 100.0)
acc.deposit(50.0)
print(acc.balance, acc)        # 150.0 Account('陶伟东', 150.0)
```

**2. 继承与多态**

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """返回面积，子类必须实现。"""


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2


def describe(shape: Shape) -> str:
    return f"面积 = {shape.area():.2f}"


print(describe(Circle(2.0)))   # 面积 = 12.57
```

**3. 使用 `__slots__` 与 dataclass**

```python
from dataclasses import dataclass


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


@dataclass(frozen=True)
class Label:
    text: str
    score: int = 0
```

**4. 元类：自动注册子类**

```python
class Registry(type):
    _registry: dict[str, type] = {}

    def __new__(mcs, name: str, bases: tuple, ns: dict) -> type:
        cls = super().__new__(mcs, name, bases, ns)
        if bases:                      # 跳过基类本身
            mcs._registry[name] = cls
        return cls


class Base(metaclass=Registry):
    pass


class Alpha(Base):
    pass


print(Registry._registry)            # {'Alpha': <class 'Alpha'>}
```

**5. 运行与验证**

```bash
python -c "from myproj.account import Account; a=Account('陶伟东'); print(a)"
# 或创建虚拟环境并跑测试
python -m venv .venv
# .venv\Scripts\Activate.ps1       # Windows PowerShell
uv run pytest -q                   # 若使用 uv
```

## 五、最佳实践与常见坑

- **`__init__` 不返回值**：它应返回 `None`，构造返回值交给 `__new__`；误写返回值会抛 `TypeError`。
- **不要使用可变默认参数**：`def f(items=[])` 的默认值在函数定义时创建且被所有调用共享，应写 `items: list = None` 再在内部 `items = [] if items is None else items`。
- **MRO 与菱形继承**：多继承时务必用 `super()` 而非直接调用父类方法，否则顺序错误或重复初始化；用 `Class.mro()` 复核。
- **`__slots__` 的边界**：声明 `__slots__` 后实例不能动态加属性；**带类级初始值的只读属性（PEP 767）不能进入 `slots`**，否则报错。
- **注解延迟求值的隐性坑（3.14 起）**：从 `__dict__` 直接读 `__annotations__` 会静默得到空 `{}`，不报错不警告。需要运行时读取注解的装饰器、ORM、序列化逻辑应改用 `annotationlib.get_annotations(obj, format=annotationlib.Format.FORWARDREF)`，或用 `typing_extensions` 的跨版本实现；`dataclasses` 自身已改用 `FORWARDREF`。
- **`from __future__ import annotations` 已弃用但未移除**：3.14 起标注为弃用，官方表示不会在 3.13（EOL 2029）到期前移除；新代码应逐步移除该导入，但不要写成「已不可用」。
- **私有属性靠约定**：`__name` 只是名称改写，并非真正私有，仍可从外部以 `_类名__name` 访问；真正防护靠 `@property` 与封装。
- **避免把可变状态放类属性**：类属性被所有实例共享，可变对象易引发跨实例污染，应放在实例属性中。
- **静态检查**：用 `mypy --strict` 或 `pyright` 检查泛型类与 `Protocol`，让「注解即文档、注解即校验」。

## 六、核心要点速查

1. 类是模板，对象是实例；`__init__` 只做初始化，`__new__` 负责创建。
2. 属性查找遵循「实例 → 类 → 基类」，多继承由 **C3 线性化（MRO）** 决定顺序。
3. `@property` 实现受控访问；`__slots__` 禁止实例 `__dict__`、节省内存。
4. `abc.ABC` + `@abstractmethod` 定义接口；`@dataclass` 自动生成样板方法。
5. 元类是「创建类的类」，默认是 `type`，常用于注册、校验、注入。
6. **PEP 705/767**：`typing.ReadOnly` 从 `TypedDict` 项扩展到类/协议属性，**与 `__slots__` 冲突**。
7. **PEP 649/749（3.14）**：注解延迟求值，类上 `__annotations__` 更惰性；直接读可能得空 `{}`，应使用 `annotationlib`。
8. **PEP 644/695** 推进泛型类、`Protocol`、类型别名现代化；`types.UnionType` 在 3.14 成为 `typing.Union` 别名。
9. **PEP 768（3.14）**：`sys.remote_exec(pid, script)` 提供安全外部调试接口。
10. 当前稳定主线为 **Python 3.15**（`3.15.0` 2026-10-09，`3.15.2` 2026-10-25）；版本细节以官方发布页为准。

## 七、学习资源

- [What's new in Python 3.15（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [What's new in Python 3.14（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Python documentation by version（python.org 官方版本列表）](https://www.python.org/doc/versions/)
- [PEP 705 – ReadOnly TypedDict items](https://peps.python.org/pep-0705/)
- [PEP 767 – ReadOnly for class and protocol attributes](https://peps.python.org/pep-0767/)
- [PEP 695 – Type parameter syntax（泛型类语法）](https://peps.python.org/pep-0695/)
- [PEP 768 – Secure external debugger interface](https://peps.python.org/pep-0768/)
- [Python data model（数据模型官方文档）](https://docs.python.org/3/reference/datamodel.html)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 语言与工程化全景，本知识点的体系入口
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 元编程、装饰器、描述符等进阶主题
- [[Python-类型注解实战]] — 泛型类、Protocol 与 ReadOnly 的静态检查实践

## 九、变更记录

- 2026-11-19：首次创建。
