---
title: Python-从入门到精通
date: 2026-11-18
updated: 2026-11-18
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 工程化
  - 入门到精通
aliases:
  - Python 技术语言与工程化全景
  - Python 全景笔记
source: https://docs.python.org/3.15/whatsnew/3.15.html
---

# Python-从入门到精通

> [!summary] 摘要
> 本文系统梳理 Python 语言演进（3.13–3.15）与工程化生态，覆盖从入门语法、环境与依赖管理，到异步/类型/测试等进阶实践，再到并发架构与生产落地的精通路径。适合刚接触 Python 的初学者、需要做版本选型与工程标准化的开发者，以及关注自由线程、子解释器等前沿特性的技术决策者。结构按「最新动态 → 入门 → 进阶 → 精通 → 速查 → 资源 → 关联笔记」展开。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 下表仅收录可从官方文档确认的版本与更新点，来源见「六、学习资源」。

| 版本/组件 | 发布时间 | 关键更新点 | 来源 |
|-----------|----------|-----------|------|
| Python 3.15.2 | 2026-10-25（3.15.0 为 2026-10-09） | PEP 810 显式延迟导入（`lazy` 软关键字）、PEP 814 `frozendict`、PEP 661 `sentinel`、PEP 798 解包推导式、PEP 799 `profiling` 包与 Tachyon 采样 profiler、PEP 803 自由线程稳定 ABI（abi3t）、PEP 831 默认帧指针；默认编码改为 UTF-8（PEP 686） | [Python 3.15 What's new](https://docs.python.org/3.15/whatsnew/3.15.html) |
| Python 3.14.10 | 稳定线主力（3.14.0 为 2025-10-07） | PEP 649/749 注解延迟求值（新增 `annotationlib`）、PEP 734 标准库子解释器（`concurrent.interpreters`、`InterpreterPoolExecutor`）、PEP 750 模板字符串（t-string）、PEP 768 安全外部调试接口 `sys.remote_exec`、PEP 784 `compression.zstd`、asyncio 内省 CLI；自由线程由实验转正式支持；3.14.5 起 GC 回退为分代 GC | [Python 3.14 What's new](https://docs.python.org/3.14/whatsnew/3.14.html) |
| Python 3.13.18 | 2024-10-07 起的稳定分支 | 实验性自由线程（PEP 703，独立可执行文件如 `python3.13t`）、实验性 JIT（PEP 744）、新交互式 REPL、默认彩色 traceback、PEP 667 `locals()` 语义、PEP 696 类型参数默认值、PEP 705 `ReadOnly`、PEP 742 `TypeIs`；移除 PEP 594 的 19 个“死电池”模块 | [Python 3.13 What's new](https://docs.python.org/3.13/whatsnew/3.13.html) |
| PEP 779 | 2025-06-16 通过 | 定义自由线程 Python 的“受支持状态”标准（第二阶段要求），自 3.14 起自由线程构建为官方支持但可选，无弃用计划不会移除 | [PEP 779](https://peps.python.org/pep-0779/) |
| NumPy 2.5.4 | 2.5.0 为 2026-06-21，2.5.4 为 2026-10-10 | 2.4.2 起支持 Python 3.11–3.14；与 pandas 3.0 构成当前数据处理栈基础 | [NumPy Releases](https://numpy.org/news/) |
| pandas 3.0.0 | 2026-01-21（major） | 默认使用专用字符串数据类型、全面启用 Copy-on-Write（移除 `SettingWithCopyWarning`）、调整日期时间类型默认解析、引入 `pd.col` 语法初步支持 | [pandas 3.0.0 What's new](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) |
| pytest 9.1.1 | 9.1.0 为 2026-06-13，9.1.1 为 2026-06-19 | fixture 与参数化仍是核心范式，持续改进 unraisable 异常收集等能力 | [pytest Changelog](https://docs.pytest.org/en/latest/changelog.html) |
| uv 0.13.8 | 2026-11-12 | Astral 出品的 Rust 实现依赖/环境管理器，以 `pyproject.toml` + `uv.lock` 为核心，提供 `uv init/add/sync/run`，毫秒级创建虚拟环境 | [uv 0.13.8 Release](https://github.com/astral-sh/uv/releases/tag/0.13.8) |
| Pydantic 2.14 | 2026-10 | 正式支持 Python 3.15（含延迟导入、PEP 747 `TypeForm`）、稳定化 `MISSING` 哨兵、放弃 Python 3.9；是 FastAPI 请求/响应模型核心 | [Pydantic v2.14](https://pydantic.dev/articles/pydantic-v2-14-release) |
| Django 6.0 / 5.2 LTS | 5.2 LTS 为 2025-04-02；6.0 为 2025-12-03 | 5.2 LTS 为生产默认；6.0 引入内置 Tasks 后台任务框架、原生 CSP 中间件、`CompositePrimaryKey` 等 | [Django 6.0 release notes](https://docs.djangoproject.com/en/dev/releases/6.0/) |

> [!warning] 版本选型提醒
> 当前稳定主线为 **Python 3.15**（最新 3.15.2，2026-10-25）与 **3.14**（最新 3.14.10）。新项目建议从 **3.13+** 起步，避免使用已停止支持的 3.9 及更早版本。

## 二、入门篇

### 2.1 基础概念

Python 是一门以**可读性**和**开发效率**著称的通用动态语言，其现代入门核心不是语法细节，而是下面这组概念：

- **语法基础**：掌握 f-string、海象运算符 `:=`、`match/case`、列表/字典/集合推导式、迭代器与生成器、异常处理，是入门的核心。
- **动态与鸭子类型**：对象以行为而非继承被使用，`duck typing` 贯穿整个生态，与后续的类型注解形成互补。
- **代码块靠缩进**：没有括号与花括号，缩进即语法，重命名或移动代码时要注意缩进层级。
- **解释器与运行模型**：理解解释执行、GIL（全局解释器锁）对并发的影响，是后续选型与性能优化的地基。

> [!note] 与 [[Python学习]] 的关系
> 若已具备语法基础，可跳过本篇的语法条目，直接看 2.2 环境准备与 3.1 核心机制；[[编程语言]] 提供了跨语言对比的宏观视角。

### 2.2 环境准备

现代 Python 项目以 **`pyproject.toml`** 为唯一事实来源，环境隔离是第一步。

**标准库 venv（最基础）**

```bash
python -m venv .venv
# 激活（Windows PowerShell）
.venv\Scripts\Activate.ps1
# 激活（macOS / Linux）
source .venv/bin/activate
```

**uv（推荐，新项目主流）**

```bash
uv init            # 生成 pyproject.toml、.python-version、.venv
uv sync            # 按 uv.lock 同步环境
uv run python main.py
```

> [!tip] 选型建议
> 使用标准库 `venv`（`python -m venv .venv`）或 `uv`（`uv init`）创建隔离环境，**避免全局依赖污染**。`uv` 创建虚拟环境的速度比 `venv`/`virtualenv` 快 10–100 倍，且自动管理 `pyproject.toml` 与 `uv.lock`。

### 2.3 第一个实践（含代码示例）

以最小的「项目结构 + 类型注解 + 测试」示例走通完整闭环，体会现代 Python 的开发节奏。

**项目结构**

```text
myproj/
├── pyproject.toml
├── .python-version
├── src/
│   └── myproj/
│       └── calc.py
└── tests/
    └── test_calc.py
```

**核心代码**

```python
from __future__ import annotations


def add(a: int | float, b: int | float) -> int | float:
    """返回两数之和。"""
    return a + b


def describe(items: list[str]) -> str:
    count = len(items)
    return f"共 {count} 项：{', '.join(items)}"
```

> [!note] 注解说明
> `from __future__ import annotations` 让注解延迟成字符串，便于前向引用；Python 3.14 起注解已默认延迟求值（PEP 649/749），该导入在多数场景下可移除，但为兼容旧版本保留更稳妥。

**测试代码**

```python
import pytest

from myproj.calc import add, describe


@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (0.5, 0.5, 1.0), (-1, 1, 0)])
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_describe():
    assert describe(["a", "b"]) == "共 2 项：a, b"
```

**运行**

```bash
uv run pytest -q
```

> [!tip] 第一个实践的要点
> 从一开始就养成三个习惯：**签名加类型注解**、**用 pytest 写断言式测试**、**用 pyproject.toml 声明依赖**。它们会让后续的进阶与生产化少走大量弯路。

## 三、进阶篇

### 3.1 核心机制

**异步入门**

理解事件循环、协程（`async/await`）、`Task` 与 `await`，用 `asyncio.run()` 启动，先掌握单任务再进入并发。

```python
import asyncio


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} 完成"


async def main() -> None:
    # 结构化并发：任一任务失败会自动取消其余任务
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch("A", 0.3))
        tg.create_task(fetch("B", 0.1))
    print("全部完成")


asyncio.run(main())
```

**元编程机制**

掌握装饰器、描述符（`__get__`/`__set__`）、`__new__`/`__init__`、metaclass、`__getattr__`/`__getattribute__`、抽象基类（ABC）与 `@property`、`__slots__` 等数据模型，是写出可维护库与框架的基础。

**类型系统**

```python
from typing import TypeGuard


def is_str_list(value: object) -> TypeGuard[list[str]]:
    return isinstance(value, list) and all(isinstance(x, str) for x in value)
```

现代类型注解由 PEP 695 类型别名、PEP 696 类型参数默认值、PEP 705 `ReadOnly`、PEP 742 `TypeIs`、PEP 747 `TypeForm` 构成基础，配合 [[Python-高级特性]] 与 mypy/pyright 使用。

**工具链**

```bash
uv add requests               # 安装依赖
uv add --dev pytest           # 安装开发依赖
uv run mypy --strict src/     # 静态检查
uv run pyright                # 可选的另一检查器
```

### 3.2 最佳实践

- **类型检查工程化**：使用 `mypy --strict` 或 `pyright` 做静态检查，利用 `Protocol` 定义结构化类型、`TypeGuard`/`TypeIs` 做类型收窄、`@overload` 表达重载、PEP 695 `type` 定义别名。
- **测试最佳实践**：fixture 管理状态与依赖注入、参数化覆盖多输入、使用 `tmp_path` 隔离文件、用 `monkeypatch` 隔离外部行为、将慢测试与单元测试分层。
- **性能优化手段**：关注 pyperformance 基准；合理使用 JIT（3.13+ 实验）、3.14 尾调用解释器（pyperformance 几何平均约 3–5% 提升）、3.15 MSVC 构建的尾调用解释器（Windows 报告约 15–20%）；**优先优化算法与减少对象创建**。
- **依赖与安全**：定期用 `uv`/`pip` 升级依赖并审查漏洞，关注 CVE（如 3.14.10/3.15.2 修复的 ssl `eMudhra` 中间证书 CVE 2026-115557），避免使用已弃用的 API。
- **数据栈实践**：NumPy 2.x 注意 ABI 变化与 `StringDtype`；pandas 3.0 全面 CoW 后无需再担心链式赋值告警，优先用 `.loc`/`.iloc` 与向量化操作替代逐行循环。

> [!note] 并发模型选型
> I/O 密集用 **asyncio**；CPU 密集用 **multiprocessing** / `ProcessPoolExecutor`；线程用于有 GIL 释放的 C 扩展场景；子解释器/自由线程面向真正的多核并行。

### 3.3 常见问题与排查

> [!warning] asyncio 常见陷阱
> - 避免在协程中调用阻塞 I/O（应改用异步库），否则会卡住整个事件循环。
> - 谨慎共享可变状态，跨任务共享时用锁或队列保护。
> - 用 `asyncio.Queue` 做生产者-消费者。
> - 生产环境关闭调试模式，并配置日志与 `ResourceWarning` 检测。
> - 3.14 起可用 `python -m asyncio ps` / `pstree` 内省运行中进程的异步任务与调用树，排查“任务卡住”非常有效。

**依赖与环境问题**

- `ModuleNotFoundError`：先确认 `uv sync` 已执行，或激活了正确的虚拟环境（`.venv`）。
- 环境不一致：以 `uv.lock` 为准执行 `uv sync`，不要混用全局 `pip install`。
- 版本冲突：用 `uv pip tree` / `uv lock` 检查依赖树，避免多个大版本并存。

**类型与运行差异**

- 读取 `__annotations__` 的库在 3.14 延迟注解后可能需要适配：改用 `annotationlib.get_annotations()` 并按 `Format.VALUE` / `FORWARDREF` / `STRING` 读取。
- 迁移期优先使用 `annotationlib` 保持跨版本兼容；`typing_extensions` 提供 `annotationlib` 的部分回填。

## 四、精通篇

### 4.1 架构与设计

**注解体系架构**

3.14 延迟注解改变了运行时注解语义：`dataclasses` 改用 `FORWARDREF` 格式，跨版本库需用 `annotationlib.get_annotations()` 保持兼容。多数旧代码无需修改，但**运行时读取注解的库必须适配**。

**类型系统演进**

PEP 695 类型别名/泛型语法、PEP 696 类型参数默认值、PEP 705 `ReadOnly`、PEP 742 `TypeIs`、PEP 747 `TypeForm` 构成现代类型注解基础，需与 mypy/pyright 及 IDE 深度集成，形成“注解即文档、注解即校验”的架构。

**打包与分发**

以 `pyproject.toml` + 构建后端（setuptools / hatchling / flit-core 等）为核心，`uv`/`pipx`/`uvx` 分离**项目环境**与**全局工具**。注意 3.15 引入 `.start` 包启动配置文件，`.pth` 中的 `import` 行被静默弃用。

```toml
[project]
name = "myproj"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["pydantic>=2.14"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = ["pytest>=9"]
```

### 4.2 生产实践

**Web 生产架构**

- **FastAPI**：以 ASGI + Pydantic 构建高性能 API，依赖注入支持异步、缓存、生成器清理与作用域；高并发下需正确组合 ASGI 服务器（Uvicorn/Hypercorn）与反向代理。
- **Django**：5.2 LTS 为生产默认；6.0 内置 Tasks 后台任务框架与原生 CSP 中间件。
- 轻量定制场景可选 **Flask**。

> [!note] 框架选型
> 高性能 API 选 FastAPI，全栈后台选 Django，轻量定制选 Flask。FastAPI 以 Pydantic 2.x 驱动类型校验与序列化，Pydantic 2.14 已支持 Python 3.15 与延迟导入，详见 [[RESTful-API规范]]。

**性能与可观测架构**

- 3.14 尾调用解释器（Clang 19+，x86-64/AArch64，需配合 PGO）与 3.15 默认帧指针（PEP 831）提升原生栈展开效率。
- 3.15 新增 `profiling.tracing`（原 `cProfile`）与 `profiling.sampling`（Tachyon，最高约 1,000,000 Hz 采样），实现生产级低开销性能分析。

**数据栈生产要点**

- NumPy 2.x：关注 ABI 变化，升级时核对编译扩展的兼容版本。
- pandas 3.0：全面启用 Copy-on-Write，删除 `SettingWithCopyWarning`；日期时间类型默认解析有调整，迁移需回归校验。

**发布与支持周期**

Python 3.13 及以后为**两年完整支持 + 三年安全修复**。需规划版本升级路径，关注各小版本的「Notable changes」（如 3.14.5 增量 GC 回退、3.15.2 import 死锁修复）。

### 4.3 生态与前沿

**PEP 734 子解释器**

3.14 新增 `concurrent.interpreters` 模块，同一进程内运行多个相互隔离的解释器，支持 CSP/Actor 等并发模型与真正多核并行，另有 `concurrent.futures.InterpreterPoolExecutor`。当前限制：启动未优化、内存开销大、跨解释器共享选项少、第三方扩展兼容性不足。

**自由线程生产化**

PEP 703/779 使自由线程在 3.14 起为官方支持但可选的构建。需注意：

- C 扩展需按自由线程重新构建；
- 某些对象被不可变（immortal）化；
- 帧对象跨线程不安全，迭代器不可跨线程共享；
- 3.15 提供 **abi3t** 稳定 ABI，供扩展面向自由线程编译。

单线程性能损耗约 5–10%（3.13 约 40%）。

> [!tip] 前沿落地建议
> 子解释器/自由线程面向多核，但要求扩展隔离与线程安全；GIL 构建仍适合通用场景。选型需结合**工作负载、第三方库支持度与运维复杂度**三者权衡，不要为“并发”而盲目切换。

**PEP 750 模板字符串（t-string）**

`t'...'` 返回 `Template` 对象，区分静态文本与 `Interpolation`，可安全转义 HTML/SQL/Shell、构建日志与自定义 DSL，是安全字符串处理的架构级能力。

```python
import html

name = "<b>陶伟东</b>"
safe = html.escape(t"Hello {name}")  # 基于 t-string 的安全转义
```

**PEP 768 安全调试接口**

`sys.remote_exec(pid, script)` 提供零开销、可安全附加到运行中进程的调试/性能采集接口，通过 `PYTHON_DISABLE_REMOTE_DEBUG`、`-X disable-remote-debug`、`--without-remote-debug` 控制访问。

**语言演进的迁移管理**

- 3.14 起 `forkserver` 成为非 macOS 的 Unix 系统上 `multiprocessing` 默认启动方式；
- `functools.partial` 变为方法描述符；`types.UnionType` 成为 `typing.Union` 别名；
- 3.15 中 UTF-8 成为默认编码、`profile` 模块弃用、`typing.ByteString` 与 `collections.abc.ByteString` 计划在 3.17 移除。

## 五、核心要点速查

1. Python 当前稳定主线为 **3.15**（3.15.2，2026-10-25）；3.14.0 于 2025-10-07、3.13.0 于 2024-10-07 发布。
2. 3.14 三大语言级变化：**PEP 649/749 注解延迟求值、PEP 734 标准库子解释器、PEP 750 模板字符串 t-string**。
3. PEP 750 用 `t'...'` 生成 `Template` 对象，区分静态文本与插值，用于安全转义（HTML/SQL/Shell）与自定义 DSL。
4. 3.15 新增 **PEP 810 显式延迟导入**、**PEP 814 frozendict**、**PEP 661 sentinel**、**PEP 798 解包推导式**、**PEP 831 默认帧指针**。
5. 3.15 默认编码改为 **UTF-8（PEP 686）**，与系统环境无关；可用 `PYTHONUTF8=0` 或 `-X utf8=0` 保留旧行为。
6. 3.14 新增 `annotationlib`，注解按 `VALUE` / `FORWARDREF` / `STRING` 三种格式延迟求值，多数旧代码可继续工作。
7. **自由线程**：3.13 为实验构建，3.14 起正式支持（PEP 779 第二阶段），单线程性能损耗约 5–10%（3.13 约 40%）。
8. 3.13 引入实验性 **JIT（PEP 744）**、PEP 667 定义 `locals()` 语义、全新交互式 REPL 与默认彩色 traceback，并移除 19 个“死电池”模块（PEP 594）。
9. 现代类型注解：PEP 695 类型别名、PEP 696 类型参数默认值、PEP 705 `ReadOnly`、PEP 742 `TypeIs`、PEP 747 `TypeForm`，配合 mypy/pyright。
10. asyncio 结构化并发用 **TaskGroup**；3.14 新增 `python -m asyncio ps / pstree` 内省运行中进程的任务表与调用树。
11. `pyproject.toml` 是项目元数据标准：`[project]` 依赖、`[build-system]` 后端、`[tool.*]` 工具配置，`uv` 以它 + `uv.lock` 管理环境与依赖。
12. **uv 核心命令**：`uv init`、`uv add`、`uv sync`、`uv run`、`uv lock`，虚拟环境创建速度比 `venv`/`virtualenv` 快 10–100 倍。
13. pytest 核心范式为 **fixture + `@pytest.mark.parametrize`**，当前为 9.x 系列（9.1.1，2026-06-19）。
14. NumPy 当前为 2.x（2.5.4，2026-10-10）；**pandas 3.0.0**（2026-01-21）全面启用 Copy-on-Write 并默认专用字符串类型。
15. FastAPI 以 **Pydantic 2.x** 驱动类型校验与序列化，Pydantic 2.14 已支持 Python 3.15 与延迟导入。
16. 性能手段：3.14 尾调用解释器（pyperformance 约 3–5%）、3.15 MSVC 构建约 15–20%、自由线程多核并行、Tachyon 采样 profiler。
17. 3.14.5 起将增量 GC 回退为分代 GC；3.14.10/3.15.2 修复 ssl 证书黑名单 **CVE 2026-115557**。
18. Python 3.13 起支持周期为**两年完整支持 + 三年安全修复**；3.14 起非 macOS 的 Unix 系统 `multiprocessing` 默认启动方式改为 `forkserver`。

## 六、学习资源

**Python 语言官方文档**

- [What's new in Python 3.15（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [What's new in Python 3.14（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [What's New In Python 3.13（Python 官方文档）](https://docs.python.org/3.13/whatsnew/3.13.html)
- [Python documentation by version（python.org 官方版本列表）](https://www.python.org/doc/versions/)
- [PEP 779 – Criteria for supported status for free-threaded Python](https://peps.python.org/pep-0779/)
- [Python experimental support for free threading（Python 官方文档）](https://docs.python.org/3.13/howto/free-threading-python.html)
- [Developing with asyncio（Python 官方文档）](https://docs.python.org/3.11/library/asyncio-dev.html)

**工程化与生态**

- [uv 项目结构与文件（Astral 官方文档）](https://docs.astral.sh/uv/concepts/projects/layout/)
- [About fixtures（pytest 官方文档）](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [NumPy Releases（NumPy 官方）](https://numpy.org/news/)
- [What's new in pandas 3.0.0（pandas 官方）](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html)
- [Django 6.0 release notes（Django 官方文档）](https://docs.djangoproject.com/en/dev/releases/6.0/)
- [Pydantic v2.14: Python 3.15 Support, Lazy Imports, TypeForm & More](https://pydantic.dev/articles/pydantic-v2-14-release)

## 七、关联笔记

- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 装饰器、元编程、类型等高级主题
- [[NodeJS-Express框架笔记]] — 与 Python Web 栈（FastAPI/Django/Flask）对比的 Node.js 方案
- [[RESTful-API规范]] — Web API 设计规范，配合 FastAPI 实践
- [[SQL优化指南]] — 数据处理与性能优化的延伸参考
- [[编程语言]] — 跨语言选型与演进的宏观视角

## 八、变更记录

- 2026-11-18 首次创建
