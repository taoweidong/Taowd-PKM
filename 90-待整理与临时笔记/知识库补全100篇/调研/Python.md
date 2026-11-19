---
title: Python 调研
date: 2026-11-19
updated: 2026-11-19
tags:
  - Python
  - 调研
  - 知识库补全100篇
---

# Python 调研

> 调研范围：Python 方向 16 个知识点的**最新官方支持与关键事实**，截至 **2026 年 11 月**。
> 用途：供后续写作 16 篇详细文档引用。所有版本号、PEP 状态均以官方文档 / 官方仓库为准，来源 URL 附在各条目后。

## 一、主题最新动态（截至 2026-11）

- **Python 3.15 已是当前最新稳定版本**（首发于 **2026-10-09**，最新补丁 **3.15.2** 于 **2026-10-25** 发布，属「紧急安全发布」）。Python 3.16 处于预发布阶段（`3.16.0a2`，2026-11-10）。
- **Python 3.15 的五大亮点**：显式延迟导入（PEP 810）、内置 `frozendict`（PEP 814）、内置 `sentinel`（PEP 661）、**UTF-8 成为默认编码**（PEP 686）、**自由线程构建的稳定 ABI（abi3t，PEP 803）**。库层面新增 `profiling` 包与高频采样性能分析器 **Tachyon**（PEP 799），以及三元组解包语法（PEP 798）。
- **Python 3.14（2025-10-07 首发）的三大亮点**：注解延迟求值（PEP 649 / PEP 749，新增 `annotationlib`）、标准库多解释器（PEP 734，`concurrent.interpreters`）、模板字符串 `t'...'`（PEP 750）。**自由线程构建自 3.14 起「正式受支持」（PEP 779，第二阶段）**，不再是实验特性。
- **弃用/移除节奏收紧**：`typing.ByteString`（自 3.9 弃用）与 `collections.abc.ByteString` **计划在 Python 3.17 移除**，官方推荐的替代是 `collections.abc.Buffer`（运行时）或显式联合类型 `bytes | bytearray | memoryview`（注解）。`typing._UnionGenericAlias`、`profile` 模块等亦在 3.17 移除清单中。**注意：不是 3.14 移除，是 3.17。**
- **并发模型进入新阶段**：`asyncio` 自 3.14 起对自由线程构建有**一等支持**；`concurrent.interpreters` 提供同进程多解释器（进程级隔离 + 线程级开销）；3.15 又补齐 `abi3t`，便于 C 扩展兼容自由线程构建。
- **性能工具链成型**：3.14 的实验性 **JIT**（`PYTHON_JIT=1`，`PEP 774` 解除 LLVM 构建依赖，`PEP 836` 规划）与 3.15 的 **Tachyon 采样分析器**、默认帧指针（PEP 831）、Windows 尾调用解释器（MSVC 18 下 15–20% 加速），共同构成性能优化方向的事实基础。
- **生态版本快速迭代**：FastAPI `0.162.3`（支持 Python 3.15）、Pydantic `2.14`、pandas `3.0.6`（首个支持 3.15 的版本）、pytest `9.1.1`、uv `0.13.7`（0.13.0 起将 Python 3.15 设为默认稳定版）、Poetry `2.3.4`、NumPy `2.5.4`、mypy `2.4`、pyright `1.1.413`。

## 二、版本与关键事实表

| 版本号 | 发布日期 | 关键变化 | 官方来源 URL |
| --- | --- | --- | --- |
| Python 3.16.0a2（预发布） | 2026-11-10 | 预发布阶段，计划 2027-10-06 首发，PEP 826 | https://www.python.org/downloads/ ；https://www.python.org/getit/windows/ |
| Python 3.15.2 | 2026-10-25 | 3.15 第二个维护版，**紧急安全发布**，约 130 项修复、70 位贡献者；修复 CVE-2026-115557（eMudhra 中间 CA 密钥）与 CVE-2026-114583 | https://www.python.org/downloads/release/python-3152/ |
| Python 3.15.0 | 2026-10-09 | 最新稳定版：PEP 810 延迟导入、PEP 814 `frozendict`、PEP 661 `sentinel`、PEP 686 UTF-8 默认编码、PEP 798 解包推导式、PEP 799 `profiling`/Tachyon、PEP 803 `abi3t`、PEP 831 帧指针 | https://docs.python.org/3.15/whatsnew/3.15.html |
| Python 3.14.10 | 2026-10-25 | 3.14 第十个维护版，**紧急安全发布**（CVE-2026-115557），约 120 项修复、63 位贡献者 | https://www.python.org/downloads/release/python-31410/ |
| Python 3.14.0 | 2025-10-07 | PEP 649/749 注解延迟求值、PEP 734 多解释器、PEP 750 模板字符串、PEP 784 标准库 zstd、`sys.remote_exec`、异步内省 `python -m asyncio` | https://docs.python.org/3.14/whatsnew/3.14.html |
| Python 3.13.18 | 2026-10-25 | 3.13 安全维护版；3.13 首发 2024-10-07，EOL 2029-10（PEP 719） | https://www.python.org/downloads/ ；https://www.python.org/doc/versions/ |
| Python 3.12 | 2023-10-02 | 安全维护期，EOL 2028-10（PEP 693）；PEP 695 类型参数语法、PEP 709 内联推导式 | https://www.python.org/downloads/ |
| Python 3.11.18 | 2026-10-25 | 安全维护版；3.11 首发 2022-10-24，EOL 2027-10（PEP 664）；PEP 654 `except*` | https://www.python.org/downloads/ |
| Python 3.10.22 | 2026-10-01 | **已生命周期结束**（EOL 2026-10-01），最后版本（PEP 619） | https://www.python.org/downloads/ |
| pip 26.3 | 2026-11-02 | 最新 pip；26.0 于 2026-01-31 发布 | http://pypi.org/project/pip/ |
| FastAPI 0.162.3 | 2026-11 | 支持 Python 3.15；锁定 Pydantic 2.14.3 | https://github.com/fastapi/fastapi/releases ；https://fastapi.tiangolo.com/release-notes/ |
| Pydantic 2.14 | 2026-10-07 | 支持 Python 3.15，**放弃 Python 3.9**；`MISSING` 稳定化、延迟导入、`TypeForm`、`frozendict` 支持 | https://pydantic.dev/articles/pydantic-v2-14-release |
| Starlette 1.9.0 | 2026-10/11 | FastAPI 底层 ASGI 框架 | https://github.com/encode/starlette/releases |
| pandas 3.0.0 | 2026-01-22 | 3.x 大版本：默认专用字符串 dtype、统一 CoW 拷贝语义、新日期时间解析默认、初始支持 `pd.col` | https://pandas.pydata.org/docs/whatsnew/v3.0.0.html |
| pandas 3.0.6 | 2026-10 | 3.0.x 补丁版，**首个支持 Python 3.15** 的版本；pandas 3.0 支持 Python 3.11+ | https://pandas.pydata.org/docs/whatsnew/ ；https://pypi.org/project/pandas/ |
| pytest 9.1.0 / 9.1.1 | 2026-06-13 / 2026-11-07 | pytest 9 系列；pygments 成为必需依赖（可用 `--code-highlight=no` 关闭） | https://docs.pytest.org/en/stable/changelog.html ；https://docs.pytest.org/en/stable/announce/release-9.1.0.html |
| uv 0.13.7 | 2026-11-03 | uv 最新；0.13.0（2026-10-09）起将 **Python 3.15 设为默认稳定版** | https://github.com/astral-sh/uv/releases |
| Poetry 2.3.4 | 2026 | Poetry 最新；2.3.0（2026-01-18）、2.1.0（2025-02） | https://python-poetry.org/blog/category/releases |
| NumPy 2.5.4 | 2026-10-10 | NumPy 最新补丁；2.5.0（2026-06-21） | https://numpy.org/news/ |
| mypy 2.4 | 2026-10-01 | 基于 Ruff 解析器的原生解析器、`TypeForm` 支持不再实验、提供 Python 3.14 的 WASM wheel | https://www.mypy-lang.org/ ；https://mypy-lang.blogspot.com/2026/10/mypy-24-released.html |
| pyright 1.1.413 | 2026-08-14 | 最新 pyright | https://github.com/microsoft/pyright/releases |

## 三、分知识点关键事实

### 1. Python 语法基础

- **最新语法事实**：`match`/`case` 结构式匹配自 **3.10** 引入；**3.12** 引入 PEP 695 类型参数语法（`def f[T](x: T)`）；**3.13** 引入 PEP 695 的 `TypeAlias` 简化；**3.14** 注解改为延迟求值（PEP 649/749，见第 12 点）。
- **3.14 起 `from __future__ import annotations` 被标记弃用**，官方明确「不会在 Python 3.13（最后一个无延迟求值注解的版本，EOL 2029）到期前移除」，但新代码应逐步移除该导入。
- **3.15 新增 PEP 798 解包推导式**：列表/集合/字典推导式与生成器表达式支持 `*`、`**` 解包，等价于嵌套推导式或 `itertools.chain`：
  `[*L for L in lists]`、`{**d for d in dicts}`、`(*a async for a in agen())`。
- **3.14 起 `forkserver` 成为 Unix（非 macOS）上 `multiprocessing` 与 `ProcessPoolExecutor` 的默认启动方式**（原为 `fork`）；Windows/macOS 仍默认 `spawn`。
- **3.14 起 `functools.partial` 变为方法描述符**，需用 `staticmethod()` 包装以保持旧行为；`types.UnionType` 成为 `typing.Union` 的别名。
- **3.14 起增量式垃圾回收**（后于 **3.14.5 回退**为 3.13 的分代式，因生产环境内存压力报告）。
- 来源：https://docs.python.org/3.14/whatsnew/3.14.html ；https://docs.python.org/3.15/whatsnew/3.15.html

### 2. Python 数据类型与内置函数

- **3.15 新增内置 `frozendict`（PEP 814）**：不可变、**非 `dict` 子类**（直接继承 `object`）、可哈希（键值均可哈希时）、保留插入顺序、比较**忽略顺序**（`frozendict(x=1,y=2) == frozendict(y=2,x=1)` 为 `True`）。
  - 已更新为接受 `frozendict` 的标准库：`copy`、`decimal`、`json`、`marshal`、`plistlib`（仅序列化）、`pickle`、`pprint`、`xml.etree.ElementTree`。
  - `eval()`/`exec()` 的 `globals`、`type()` 与 `str.maketrans()` 的 `dict` 参数均接受 `frozendict`。
  - 判断建议：`isinstance(arg, (dict, frozendict))` 或 `isinstance(arg, collections.abc.Mapping)`。
- **3.15 新增内置 `sentinel` 类型（PEP 661）**：用于创建唯一哨兵值，表示简洁、保留标识、可在类型表达式中用 `|` 组合、可在可导入时被 pickle。
- **3.15 起 `re.match()` / `re.Pattern.match()` 被「软弃用」**，新增更明确的 `re.prefixmatch()` / `re.Pattern.prefixmatch()`；旧名不会移除（已沿用 30 余年）。
- **3.15 起 `struct` 的 `'F'`/`'D'` 格式码软弃用**，改用 `'Zf'`/`'Zd'`。
- **`collections.abc.ByteString` / `typing.ByteString` 计划于 Python 3.17 移除**；运行时判断缓冲协议用 `isinstance(obj, collections.abc.Buffer)`（3.12 起）。
- 来源：https://docs.python.org/3.15/whatsnew/3.15.html ；https://docs.python.org/3.14/deprecations/pending-removal-in-3.17.html

### 3. Python 函数与作用域

- **PEP 695 类型参数语法（3.12）**：函数/类/类型别名可声明类型参数，并自动获得 `__type_params__` 属性；该语法下类型参数不进入 `globals()`/`locals()`。
- **PEP 695 消除显式型变声明**，由类型检查器根据类型参数在类中的使用推断协变/逆变/不变。
- **函数注解在 3.14 起延迟求值**：函数/类/模块的注解不再即时求值，而是存为 `__annotate__`，按需求值；不再需要把前向引用写成字符串。`annotationlib.get_annotations(func, format=Format.VALUE|FORWARDREF|STRING)` 提供三种格式（见第 12 点）。
- **PEP 570 仅位置参数（`/`、`*`）**、**PEP 570 之后新增的 keyword-only 语义**均为函数签名基础；3.14 起 `functools.partial` 作为方法描述符的行为变化需注意（见第 1 点）。
- **3.15 起 `generator.throw(type, exc, tb)` / `athrow(...)` 旧签名弃用**，改用单参数 `throw(exc)` / `athrow(exc)`。
- 来源：https://docs.python.org/3.12/whatsnew/3.12.html ；https://docs.python.org/3.14/whatsnew/3.14.html ；https://docs.python.org/3.15/whatsnew/3.15.html

### 4. Python 面向对象编程

- **3.13 引入 `typing.ReadOnly`（PEP 705）**：仅用于 `TypedDict` 项，标记为只读，类型检查器对赋值报错（运行时无检查）。
- **PEP 767**：将 `ReadOnly` 扩展为类属性与协议属性的合法限定符，可与 `ClassVar` 组合使用，并可作为「仅初始化一次」的 flyweight 默认值。**注意与 `__slots__` 冲突**：带类级初始值的只读属性不能进入 `slots`。
- **PEP 644/695**：泛型类、协议、类型别名的现代化；**PEP 649/749 注解延迟求值影响元类行为**——访问类上的 `__annotations__` 会更「惰性」，元类中若自行处理 `__annotate__` 需谨慎（官方文档专门说明）。
- **PEP 768 安全外部调试器接口（3.14）**：`sys.remote_exec(pid, script)` 支持零开销地附着到运行中的进程；可用 `PYTHON_DISABLE_REMOTE_DEBUG`、`-X disable-remote-debug`、`--without-remote-debug` 关闭。
- **`types.UnionType` 在 3.14 成为 `typing.Union` 的别名**，会改变部分行为。
- 来源：https://docs.python.org/3.13/whatsnew/3.13.html ；https://peps.python.org/pep-0705/ ；https://peps.python.org/pep-0767/ ；https://docs.python.org/3.14/whatsnew/3.14.html

### 5. Python 装饰器详解

- **核心事实**：装饰器是「类/函数调用」语法糖，PEP 318 定义；`functools.wraps` / `functools.update_wrapper` 用于保留 `__name__`/`__doc__`/`__wrapped__`。
- **3.14 行为变更**：`functools.partial` 现在是**方法描述符**，把 `partial` 对象当作方法/装饰器使用时行为有变化，需用 `staticmethod()` 包装保持旧行为。
- **3.14 注解延迟求值对装饰器实现的影响**：读取 `__annotations__` 的装饰器（如数据校验、序列化、ORM 字段注册）应改用 `annotationlib.get_annotations(..., format=Format.FORWARDREF)`，否则可能取到空 dict（`__dict__.get("__annotations__")` 在 3.14 返回 `{}`）。第三方包 `typing_extensions` 提供跨版本兼容的 `Format` 与 `get_annotations`。
- **`functools.cached_property`（3.8+）**、**`functools.lru_cache`** 仍是常用装饰器；3.13 起 `functools.cached_property` 支持泛型。
- 来源：https://docs.python.org/3.14/whatsnew/3.14.html ；https://docs.python.org/3/library/functools.html

### 6. Python 迭代器与生成器

- **PEP 255/380/479**：生成器与 `yield from` 的基础语义；`StopIteration` 在生成器内部会被转为 `RuntimeError`（PEP 479）。
- **3.15 起生成器 `throw(type, exc, tb)` 旧签名弃用**，使用单参数 `throw(exc)`（`athrow(exc)` 同理）。
- **3.15 新增 PEP 798 生成器表达式解包**：`(*L for L in lists)`、异步生成器表达式 `(*a async for a in agen())`。
- **3.15 软弃用 `__index__()`/`__int__()` 返回非 `int`**：未来这些方法必须返回 `int` 的严格子类（`__float__`/`__complex__` 同理），当前在「未来版本移除」清单中。
- **`collections.abc` 迭代协议**：`Iterable`/`Iterator`/`Generator`/`AsyncIterator` 等，配合 `collections.abc.Buffer`（3.12+）做缓冲协议运行时判断。
- 来源：https://docs.python.org/3.15/whatsnew/3.15.html ；https://docs.python.org/3/library/collections.abc.html

### 7. Python 异常处理与日志

- **PEP 654（3.11）**：`BaseExceptionGroup` / `ExceptionGroup` 与 `except*` 子句，异常组递归匹配、未匹配部分继续传播。
- **PEP 765（Python 3.14，Final）**：**禁止在 `finally` 块中使用 `return`/`break`/`continue` 跳出**。3.14 起 CPython 在 AST 构造时发出 **`SyntaxWarning`**（静态分析/编译时可见，执行预编译代码时不重复出现）；语言规范允许未来改为 `SyntaxError`，但尚无明确时间。**写作时务必说明「3.14 只是 SyntaxWarning，不是立即报错」**。
- **3.15 起 `unittest.IsolatedAsyncioTestCase` 弃用**：测试用例方法返回非 `None` 值的行为被弃用。
- **3.15 起 `assertWarns()` / `assertWarnsRegex()` 不再吞掉不匹配的警告**，测试可能开始泄漏此前被屏蔽的警告，需用 warning filters 处理。
- **日志**：标准库 `logging` 的 `logging.warn()` 自 3.3 起弃用，用 `warning()`；`logging` 相关 API 仍属标准库，第三方常用 `structlog`、`loguru`（非官方）。
- 来源：https://peps.python.org/pep-0765/ ；https://peps.python.org/pep-0654/ ；https://docs.python.org/3.15/whatsnew/3.15.html

### 8. Python 文件与 IO 操作

- **PEP 686（Python 3.15）：UTF-8 成为默认编码**，独立于系统环境；`open('flying-circus.txt')` 等未显式指定编码的 I/O 一律按 UTF-8。可用 `PYTHONUTF8=0` 或 `-X utf8=0` 保留旧行为；`encoding='locale'` 可取当前 locale 编码（3.10+）。
  - **写作风险提示**：官方建议始终显式传入 `encoding` 以保证跨版本兼容；可用 `-X warn_default_encoding` 找出受影响代码。
- **PEP 784（Python 3.14）：标准库新增 `compression` 包**，包含 `compression.lzma`、`compression.bz2`、`compression.gzip`、`compression.zlib`（再导出旧模块），以及新增的 **`compression.zstd`**（绑定 Meta 的 zstd 库）。旧模块名**未被弃用**，最早在 3.14 发布 5 年后才会弃用/移除。
  - `tarfile`、`zipfile`、`shutil` 已支持读写 Zstandard 压缩归档。
- **3.15 PEP 829：包启动配置文件**：`.pth` 中以 `import ` 开头的行被**静默弃用**；新增 `.start` 文件，用 `pkg.mod:callable` 形式在启动时调用。
- **`pathlib`**：标准路径操作；`shutil.rmtree()` 的 `onerror` 参数自 3.12 弃用，改用 `onexc`。
- 来源：https://docs.python.org/3.15/whatsnew/3.15.html ；https://docs.python.org/3.14/whatsnew/3.14.html

### 9. Python 并发编程（多线程/多进程/协程）

- **PEP 703（自由线程 / 可选 GIL）**：**3.13 引入实验性**，**3.14 起「正式受支持」（PEP 779，第二阶段）**，但仍是可选构建。3.14 完成 PEP 703 的实现（含 C API），启用 **PEP 659 特化自适应解释器**，单线程性能惩罚约 **5–10%**；3.15 起官方 **macOS 二进制默认安装自由线程支持**，并新增 `abi3t`（PEP 803）稳定 ABI。
- **PEP 734（Python 3.14）：标准库多解释器**——新增 `concurrent.interpreters` 模块，可在同进程内运行多个相互隔离的解释器，实现 CSP/Actor 风格并发与真多核并行；另新增 `concurrent.futures.InterpreterPoolExecutor`。限制：解释器启动尚未优化、内存开销较大、对象共享选项少（主要是 `memoryview`）、部分第三方扩展尚未兼容。
- **PEP 684（3.12）**：解释器间已足够隔离，可并行使用（是多解释器并行的基础）。
- **asyncio（协程）**：**自 3.14 起对自由线程构建有一等支持**，事件循环实现对多线程环境安全；原生任务改用双链表实现，pyperformance 上快 10–20%，并支持外部内省。3.14 新增 `python -m asyncio ps PID` 与 `python -m asyncio pstree PID` 查看任务表/异步调用树。
- **多线程工具**：3.14 新增 `-X context_aware_warnings`（默认在自由线程构建为 true，GIL 构建为 false）与 `thread_inherit_context`，使 `catch_warnings` 的警告过滤上下文可被线程/asyncio 任务继承。
- **多进程**：3.14 起 Unix（非 macOS）`forkserver` 为默认启动方式（Windows/macOS 仍为 `spawn`）；3.15 修复 `multiprocessing.Pool` 回调异常导致的死锁。
- **3.15 弃用**：`threading.Condition.notifyAll()`→`notify_all()`、`Event.isSet()`→`is_set()`、`Thread.isDaemon()/setDaemon()`→`daemon` 属性、`Thread.getName()/setName()`→`name`、`currentThread()`→`current_thread()`、`activeCount()`→`active_count()`。
- 来源：https://docs.python.org/3.14/whatsnew/3.14.html ；https://docs.python.org/3.15/whatsnew/3.15.html ；https://docs.python.org/3.14/library/asyncio-threading.html ；https://peps.python.org/pep-0703/

### 10. Python 标准库精要

- **3.15 新增 `profiling` 包（PEP 799）**：`profiling.tracing`（原 `cProfile` 的确定性函数调用追踪）、`profiling.sampling`（新统计采样分析器 **Tachyon**）；`cProfile` 保留为别名，**`profile` 模块被弃用，将在 3.17 移除**。
- **Tachyon（PEP 799）**：采样率最高 **1,000,000 Hz**，零开销、无需改代码、支持按 PID 附着；模式 `--mode wall|cpu|gil|exception`；输出 `--pstats`、`--collapsed`、`--flamegraph`、`--gecko`、`--heatmap`；`--live` 实时 TUI；`--async-aware`；`--opcodes`。
- **3.14 标准库新成员**：`compression.zstd`（PEP 784）、`concurrent.interpreters`（PEP 734）、`annotationlib`（PEP 749）、`string.templatelib`（PEP 750）、`sys.remote_exec`（PEP 768）；`build-details.json` 静态构建信息（PEP 739）。
- **3.15 标准库其他**：`re.prefixmatch()`、`collections.abc.Buffer` 相关、`frozendict` 支持扩展、PEP 829 `.start` 启动文件。
- **3.15 移除/弃用速查**：`profile`→3.17 移除；`bytes_warning`→3.17；`tkinter.Variable.trace_*`（3.14 弃用）→3.17；`webbrowser.MacOSXOSAScript` 弃用→`webbrowser.MacOS`；`encodings.normalize_encoding()` 非 ASCII 编码名弃用→3.17。
- **3.15 起 `os.path.commonprefix()` 弃用**，改用 `os.path.commonpath()`（前者名称误导、且用于路径前缀不安全）。
- 来源：https://docs.python.org/3.15/whatsnew/3.15.html ；https://docs.python.org/3.14/whatsnew/3.14.html

### 11. Python 虚拟环境与包管理

- **内置 `venv`**：创建隔离环境的标准方式；`sys.prefix` / `sys.base_prefix` 区分激活/基础环境（3.15 的 C API 也改用 `PyConfig_Get()` 读取，见 PEP 741 后续）。
- **pip 最新 26.3（2026-11-02）**；pip 26.0 于 2026-01-31 发布。
- **uv 0.13.7（2026-11-03）**：**0.13.0（2026-10-09）起将 Python 3.15 设为默认稳定 Python 版本**；uv 是 Astral 出品的 Rust 实现的包/项目/工作流管理器，命令 `uv pip`、`uv add/remove/sync`、`uv run`、`uvx`。
- **Poetry 2.3.4（最新）**：2.3.0（2026-01-18）起 `installer.re-resolve` 默认由 `true` 改为 `false`；2.1.0（2025-02）支持 PEP 621 的替代构建后端（`poetry build` 遵循 `[build-system]`）；2.0（2025-01）起 `poetry lock` 默认 `--no-update`、移除 `poetry shell`（改用 `poetry-plugin-shell`）。
- **PEP 735**：`pyproject.toml` 中的依赖组（dependency groups）标准。
- **PEP 751**：**Python 标准锁文件格式（`pylock.toml`）**，2025-03 被接受，用于可复现安装，人可读、机器生成，安装器消费时无需在安装期做依赖解析。
- **PEP 723**：内联脚本元数据（inline script metadata）。
- **PEP 517 / 518 / 621 / 660**：构建后端、构建系统需求、项目元数据、可编辑安装的标准化基础。
- 来源：https://github.com/astral-sh/uv/releases/tag/0.13.0 ；https://python-poetry.org/blog/category/releases ；https://peps.python.org/pep-0735/ ；https://peps.python.org/pep-0751/

### 12. Python 类型注解与静态检查

- **PEP 484（基础）、PEP 585（3.9 泛型内置化）、PEP 604（3.10 `X | Y` 联合）** 是现代注解的基础；**PEP 695（3.12）** 类型参数语法。
- **PEP 742：`TypeIs`（Python 3.13）**：与 `TypeGuard` 类似但**可在 `if` 与 `else` 两个分支同时收窄类型**，返回 `bool`，输入/输出类型需兼容。
- **PEP 705：`typing.ReadOnly`（3.13）** 用于 `TypedDict` 只读项；**PEP 767** 将 `ReadOnly` 扩展到类/协议属性。
- **PEP 692**：用 `TypedDict` 标注 `**kwargs`（写作时可补充）。
- **PEP 649 / 749（3.14）：注解延迟求值**——函数/类/模块注解不再即时求值，存为 `__annotate__`，按需求值；新增 `annotationlib`，`get_annotations(obj, format=...)` 支持 `Format.VALUE`、`Format.FORWARDREF`、`Format.STRING`。**从 `__dict__` 直接读 `__annotations__` 在 3.14 会返回空 `{}`（不报错、不警告）**，这是最常见的踩坑点（有第三方 lint 工具 `deferlint` 专门检测此类代码）。
- **静态检查工具最新版本**：mypy **2.4**（2026-10-01，基于 Ruff 解析器的原生解析器，`TypeForm` 支持不再实验，提供 Python 3.14 的 WASM wheel）；pyright **1.1.413**（2026-08-14）。
- **`typing.ByteString`（3.9 起弃用）计划 3.17 移除**，`collections.abc.ByteString` 同；注解中建议用 `collections.abc.Buffer` 或显式联合。
- **`typing._UnionGenericAlias`（私有类）** 计划在 3.17 移除，应改用 `typing.get_origin()` / `typing.get_args()`。
- 来源：https://docs.python.org/3.14/whatsnew/3.14.html ；https://peps.python.org/pep-0742/ ；https://peps.python.org/pep-0705/ ；https://peps.python.org/pep-0767/ ；https://www.mypy-lang.org/ ；https://github.com/microsoft/pyright/releases

### 13. Python 单元测试

- **pytest 最新 9.1.1（2026-11-07）**，9.1.0（2026-06-13）；**pygments 成为必需依赖**，输出默认源码高亮，可用 `--code-highlight=no` 关闭；8.4.x 仍为常用稳定线（8.4.2，2025-09-03）。
- **标准库 `unittest`**：`IsolatedAsyncioTestCase`（3.8+）的「测试方法返回非 `None`」行为在 **3.15 弃用**。
- **3.15 起 `assertWarns()` / `assertWarnsRegex()` 不再吞掉不匹配的警告**，测试可能开始泄漏此前被屏蔽的警告，建议用 warning filters 或额外的 `assertWarns*()` 捕获。
- **pytest 9 的弃用/移除**：部分 8.x 行为在 9.1 生效性移除，需参考 Deprecations and Removals 章节更新代码。
- **PEP 751/735 相关**：测试依赖可用标准依赖组管理。
- 来源：https://docs.pytest.org/en/stable/changelog.html ；https://docs.pytest.org/en/stable/announce/release-9.1.0.html ；https://docs.python.org/3.15/whatsnew/3.15.html

### 14. Python 性能优化

- **自由线程（PEP 703）**：3.13 实验性 → **3.14 正式受支持**（PEP 779 第二阶段）；3.14 完成实现并启用 PEP 659 特化自适应解释器，单线程惩罚约 **5–10%**；3.15 官方 macOS 二进制默认安装自由线程、提供 `abi3t`（PEP 803）。**注意：自由线程构建目前不支持 JIT。**
- **JIT 编译器**：3.13 引入实验性；**3.14 官方 macOS/Windows 二进制包含实验性 JIT**（`PYTHON_JIT=1`，或 `--enable-experimental-jit=yes-off`）；典型性能影响**从慢 10% 到快 20%**；`sys._jit.is_available()` / `sys._jit.is_enabled()`；**PEP 774**（3.14）移除 JIT 构建对 LLVM 的依赖，**PEP 836** 规划支持 JIT 并目标 3.17 前在自由线程构建上相对解释器提升至少 20%。
- **尾调用解释器（3.14，opt-in）**：`--with-tail-call-interp`，Clang 19+，x86-64/AArch64；pyperformance 几何平均 **3–5% 加速**；3.15 起 MSVC 18（VS 2026）上尾调用解释器带来 **15–20%** 加速（AMD Ryzen 7 5800X 上）。
- **Tachyon 采样分析器（3.15，PEP 799）**：最高 **1,000,000 Hz**、零开销、支持附着运行中进程；`--mode wall/cpu/gil/exception` 是并发/GIL 调优的关键工具。
- **PEP 831（3.15）**：默认启用帧指针，加速原生栈回溯，利于系统分析器/调试器/eBPF 观测。
- **PEP 768（3.14）**：`sys.remote_exec()` 零开销安全调试接口，支持不重启附着分析生产进程。
- **gc**：3.14 引入增量式 GC（`gc.collect(1)` 语义变化），但 **3.14.5 因生产内存压力回退**为分代式——**写作时不要将「增量 GC」当作 3.14 的稳定特性描述**。
- **通用建议事实**：`-X importtime`（3.7+，3.14 起支持 `=2` 显示已缓存模块的 `cached`）、`pyperformance` 基准、`functools.lru_cache`、避免不必要的对象拷贝。
- 来源：https://docs.python.org/3.14/whatsnew/3.14.html ；https://docs.python.org/3.15/whatsnew/3.15.html ；https://peps.python.org/pep-0774/ ；https://peps.python.org/pep-0836/

### 15. Python Web 开发（FastAPI）

- **FastAPI 最新 0.162.3（2026-11）**：**新增对 Python 3.15 的支持**（PR #16727）；锁定依赖 **Pydantic 2.14.3**（PR #16728）；0.162.0 于 2026-11 前后发布。
- **FastAPI 底层依赖 Starlette 1.9.0（2026-10/11）**（ASGI 框架）、Pydantic v2。
- **Pydantic 2.14（2026-10-07）**：**支持 Python 3.15，放弃 Python 3.9**；`MISSING` 哨兵稳定化（字段未提供时序列化排除）；支持 **PEP 810 延迟导入**（跨模块模型引用更省启动时间）；支持 **`TypeForm`**；支持 **`frozendict`（PEP 814）**，校验与序列化等同普通 `dict`；`create_model()` 新增 `__namespace__` 参数（`__validators__` 将在 v3 弃用）。
- **Pydantic 版本线**：v2.13.0（2026-04-13）、v2.13.5（pypi）；`pydantic.v1` 命名空间匹配 1.10.26（支持 Python 3.14）；v2.14.3 为 FastAPI 当前锁定版本。
- **FastAPI 特性（写作常用事实）**：基于标准 Python 类型注解的自动请求校验、自动 OpenAPI/Swagger UI 文档、原生 `async`/`await` 支持（性能关键路径用 async，阻塞 I/O 用 `def` 让 FastAPI 在线程池执行）。
- **FastAPI 与 Python 3.15**：0.162.3 起官方支持 3.15，写作时可明确「截至 2026-11，FastAPI 已支持 Python 3.15」。
- 来源：https://github.com/fastapi/fastapi/releases ；https://fastapi.tiangolo.com/release-notes/ ；https://pydantic.dev/articles/pydantic-v2-14-release ；https://pypi.org/project/pydantic/

### 16. Python 数据处理与分析（Pandas）

- **pandas 3.0.0（2026-01-22 发布公告）**：3.x 大版本，主要变化：
  - **默认使用专用字符串数据类型（dedicated string dtype）**；
  - **统一 Copy-on-Write（CoW）拷贝/视图语义**，**取消 `SettingWithCopyWarning`**；
  - **日期时间类数据的新默认解析（new default resolution for datetime-like data）**；
  - **初始支持新的 `pd.col` 语法**（表达式式列操作）。
- **pandas 3.0.6（2026-10）**：3.0.x 补丁版，**首个支持 Python 3.15 的版本**；**pandas 3.0 支持 Python 3.11 及以上**。
- **版本节奏**：3.0.2（2026-03-30，含 `Series.case_when()` 对 `pd.col()` 的支持）、3.0.3（2026-05）、3.0.4（2026-06）、3.0.6（2026-10）。
- **升级风险**：3.0 含**可能的破坏性变更**（字符串 dtype、CoW、日期时间解析默认），从 2.x 升级需重点核对；安装建议 `python -m pip install --upgrade pandas==3.0.*` 或 conda-forge。
- **配套生态**：NumPy 2.5.4（2026-10-10，2.5.0 于 2026-06-21）；`pyarrow`、`polars`、`duckdb` 等为常用替代/加速方案（自由线程构建下 `pyarrow`/`pandas` 已发布 cp314t/cp315t wheel）。
- 来源：https://pandas.pydata.org/docs/whatsnew/v3.0.0.html ；https://pandas.pydata.org/docs/whatsnew/ ；https://mail.python.org/archives/list/pandas-dev@python.org/message/PC6CXKXRGEKSESUODN5VJ2PFH3U6B6CF/

## 四、写作要点与风险提示

### 写作要点

1. **以「版本 + PEP」为骨架**：每个知识点尽量给出引入版本号与对应 PEP，便于读者追溯官方依据（如装饰器→PEP 318/PEP 649；异常组→PEP 654；`finally` 跳转→PEP 765；多解释器→PEP 734）。
2. **突出「截至 2026-11 的最新版本」**：Python 3.15（3.15.2）、FastAPI 0.162.3、Pydantic 2.14、pandas 3.0.6、pytest 9.1.1、uv 0.13.7、Poetry 2.3.4、NumPy 2.5.4、mypy 2.4、pyright 1.1.413。
3. **并发与性能部分必须区分「正式支持 / 实验 / opt-in」**：自由线程（3.14 正式支持但可选构建）、JIT（实验性，自由线程不支持）、尾调用解释器（opt-in）、Tachyon（3.15 正式）。
4. **强调生态对新版本的跟进状态**：FastAPI 0.162.3、pandas 3.0.6、Pydantic 2.14 均已支持 Python 3.15，可作为「已可上生产」的判据；uv 0.13.0 起默认 Python 3.15。

### 风险提示（务必在文档中说明）

- **`typing.ByteString` 的移除版本是 Python 3.17，不是 3.14**：3.12（PEP 688）弃用 `collections.abc.ByteString` 与 `bytes` 简写，3.9 弃用 `typing.ByteString`，两者均**计划在 3.17 移除**。写作时避免写成「3.14 已移除」，并给出替代 `collections.abc.Buffer`。
- **PEP 765（`finally` 中 `return/break/continue`）在 3.14 只产生 `SyntaxWarning`**，并非立即报错；是否升级为 `SyntaxError` 官方「留待未来」。
- **注解延迟求值（PEP 649/749）是最常见的隐性破坏点**：3.14 起直接从 `__dict__` 读 `__annotations__` 会静默返回空 `{}`，不报错不警告，可能导致数据类/校验/序列化逻辑在生产中「空转」。需改用 `annotationlib.get_annotations()` 或 `typing_extensions` 的跨版本实现。
- **`from __future__ import annotations` 已弃用但尚未移除**：官方表示不会在 3.13（EOL 2029）到期前移除；新代码应开始移除，但不要在文档中写成「已不可用」。
- **Python 3.14 的「增量 GC」在 3.14.5 已回退**：不要将增量式 GC 作为 3.14 的稳定特性描述。
- **`forkserver` 默认启动方式变化（3.14，Unix 非 macOS）**：可能影响依赖 `fork` 隐式共享状态的 `multiprocessing` / `ProcessPoolExecutor` 代码，需提示读者检查。
- **版本信息时效性**：本调研数据截至 2026-11，第三方库补丁版本更新频繁，写作时建议在文档中标注「版本以写作当日 PyPI/官方发布页为准」。
- **来源权威性**：所有关键版本与 PEP 状态均来自 python.org、docs.python.org、peps.python.org、pydantic.dev、pandas.pydata.org、pytest.org、github.com（astral-sh/uv、python-poetry、microsoft/pyright、mypy-lang）等官方来源；第三方聚合页（如 newreleases.io）仅用于交叉验证版本号，不作为引用主源。
