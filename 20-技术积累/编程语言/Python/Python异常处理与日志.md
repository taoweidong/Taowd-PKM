---
title: Python 异常处理与日志
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 异常处理
  - 日志
aliases:
  - Python 异常与日志
  - Python 错误处理与日志
source: 网络资料整理
---

# Python 异常处理与日志

> [!摘要] 摘要
> 本文系统讲解 Python 的异常处理体系（`try/except/else/finally`、异常链、异常组、自定义异常）与标准库 `logging` 日志体系（Logger、Handler、Formatter、级别与轮转）的完整用法，并给出可直接落地的代码模板。版本与 PEP 信息以官方文档为准、截至 2026-11，适合需要把错误处理与日志从「能跑」提升到「可排障、可观测」的开发者。结构按「最新动态 → 基础概念 → 核心机制 → 实践步骤 → 最佳实践 → 速查 → 资源 → 关联笔记」展开。

## 一、最新动态（截至 2026-11）

- 当前稳定主线是 **Python 3.15**：3.15.0 于 **2026-10-09** 首发，最新补丁 **3.15.2** 于 **2026-10-25** 发布（属紧急安全发布）；3.14 线最新为 **3.14.10**。
- **PEP 654（Python 3.11）**：引入 `BaseExceptionGroup` / `ExceptionGroup` 与 `except*` 子句，异常组支持**递归匹配**，未匹配的异常继续向上传播。
- **PEP 765（Python 3.14，Final）**：禁止在 `finally` 块中使用 `return` / `break` / `continue` 跳出。**3.14 起 CPython 仅在 AST 构造时发出 `SyntaxWarning`**（静态分析/编译时可见，执行预编译代码时不重复出现），**并非立即报错**；语言规范允许未来改为 `SyntaxError`，但尚无明确时间。
- **Python 3.15 相关**：`unittest.IsolatedAsyncioTestCase` 的「测试方法返回非 `None`」行为被弃用；`assertWarns()` / `assertWarnsRegex()` **不再吞掉不匹配的警告**，测试可能开始泄漏此前被屏蔽的警告，需用 warning filters 处理。
- **日志**：标准库 `logging` 的 `logging.warn()` 自 **Python 3.3** 起弃用，应改用 `warning()`；`logging` API 仍属标准库能力，社区常用第三方结构化日志库 `structlog`、`loguru`（均为非官方）。
- 来源：[PEP 654](https://peps.python.org/pep-0654/)、[PEP 765](https://peps.python.org/pep-0765/)、[Python 3.15 What's new](https://docs.python.org/3.15/whatsnew/3.15.html)。第三方库补丁版本更新频繁，具体版本以写作当日 PyPI / 官方发布页为准。

## 二、基础概念

- **异常（Exception）**：程序运行时偏离正常流程的错误事件，可由 `raise` 主动抛出，也可由解释器自动抛出。Python 的异常是对象，继承自 `BaseException`。
- **异常继承体系**：`BaseException` 为根；常用的分支是 `Exception`（所有普通异常，业务代码应捕获的）；`SystemExit`、`KeyboardInterrupt`、`GeneratorExit` 属控制流类，不应被业务 `except Exception` 捕获。
- **栈追踪（Traceback）**：异常发生时解释器打印从调用入口到出错点的调用栈，是排障的第一手线索。
- **异常链（Exception chaining）**：`__context__`（处理旧异常时抛出新异常的隐式上下文）、`__cause__`（`raise X from Y` 设定的显式因果）、`__traceback__`（异常对象自身的栈）。
- **警告（Warning）**：与异常不同，警告用于提示潜在问题而不中断执行，由 `warnings` 模块管理，默认不抛出。
- **日志（Logging）**：把运行过程与事件写入指定输出（控制台、文件、远程）的可观测机制，核心由 **日志器 Logger → 处理器 Handler → 格式器 Formatter** 三层构成。
- **异常处理与日志的关系**：异常负责「中断并上报错误」，日志负责「持续记录过程与上下文」。生产代码的标准动作是：**记录日志 → 按需要转换/重新抛出 → 在边界统一处理**。

## 三、核心机制

### 3.1 try 语句的完整形态

```python
try:
    risky()                  # 可能出错的代码
except ValueError as e:      # 只捕获 ValueError，并绑定 e
    handle(e)
except (OSError, RuntimeError) as e:   # 元组形式捕获多种类型
    handle(e)
except Exception:            # 兜底：捕获普通异常
    handle()
else:
    # 未发生任何异常时执行，适合放“成功”后的校验
    pass
finally:
    # 无论是否发生异常都会执行，适合释放资源
    cleanup()
```

匹配规则：`except` 按声明顺序**从上到下**匹配，子类应写在父类之前；未被捕获的异常沿调用栈向上传播，直至解释器。

### 3.2 异常链与重新抛出

```python
def load() -> None:
    try:
        data = read_raw()
    except KeyError as exc:
        # 显式因果：__cause__ 指向 exc，traceback 中显示
        # "The above exception was the direct cause of the following exception"
        raise RuntimeError("读取配置失败") from exc
```

- 在 `except` 块内使用**裸 `raise`** 可重抛当前异常并完整保留原始 traceback。
- `raise X from None` 可抑制隐式上下文显示，避免 traceback 被旧异常噪声干扰。

### 3.3 异常组（PEP 654，Python 3.11+）

异常组用于在一次操作中聚合多个异常（如并发任务批量失败）：

```python
try:
    run_tasks()      # 内部可能把多个异常聚合为 ExceptionGroup
except* ValueError as eg:
    print("值错误:", eg.exceptions)
except* TimeoutError as eg:
    print("超时:", eg.exceptions)
# 未被任何 except* 匹配的异常会继续向上传播
```

`except*` 按类型**递归**匹配组内异常，每次只处理匹配到的那一类。`BaseExceptionGroup` 可包含非 `Exception` 子类（如 `KeyboardInterrupt`），`ExceptionGroup` 只包含 `Exception` 子类。

### 3.4 自定义异常

```python
class ServiceError(Exception):
    """业务基础异常。"""

    def __init__(self, message: str, code: int = 500) -> None:
        super().__init__(message)
        self.code = code


class NotFoundError(ServiceError):
    """资源不存在。"""
```

设计要点：异常层级从业务基类派生，便于用 `except ServiceError` 统一兜底；`__init__` 中保留错误码等上下文，供日志与接口层使用。

### 3.5 logging 核心模型

- **Logger**：命名分层，`logging.getLogger("app.db")`，点号表达层级，父级可聚合子级的记录。
- **Handler**：决定输出去向，如 `StreamHandler`（控制台）、`RotatingFileHandler`（按大小轮转的文件）。
- **Formatter**：定义输出格式，如时间、级别、模块、消息。
- **级别**：`DEBUG < INFO < WARNING < ERROR < CRITICAL`；Logger 与 Handler 各有最低阈值，最终生效值取两者中**更严格**的一个。

### 3.6 警告机制（warnings）

`warnings.warn(msg, category, stacklevel=2)` 用于发出告警；`warnings.filterwarnings` 控制显示与升级策略，例如把弃用告警升级为异常：

```python
import warnings

warnings.filterwarnings("error", category=DeprecationWarning)
```

## 四、实践步骤（含代码/命令示例）

### 4.1 最小可用的异常处理 + 日志闭环

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("app.calc")


def divide(a: float, b: float) -> float:
    try:
        result = a / b
    except ZeroDivisionError:
        log.error("除数为零: a=%s b=%s", a, b, exc_info=True)
        raise
    log.debug("divide(%s, %s) = %s", a, b, result)
    return result
```

> [!tip] 要点
> 在 `except` 里**先记录日志、再 `raise`**，既保留可排查的上下文，又让调用方仍能感知失败。

### 4.2 结构化日志与文件轮转

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app.service")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s %(name)s %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(formatter)

file_handler = RotatingFileHandler(
    "app.log", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)
logger.propagate = False   # 避免向父级重复输出

logger.info("服务启动")
logger.warning("连接池使用率接近上限: %s%%", 85)
```

### 4.3 自定义异常 + 统一转换

```python
class ApiError(Exception):
    def __init__(self, message: str, code: int = 500) -> None:
        super().__init__(message)
        self.code = code


def call_remote(payload: dict) -> dict:
    try:
        return remote_call(payload)
    except TimeoutError as exc:
        raise ApiError("下游超时", code=504) from exc
    except OSError as exc:
        raise ApiError("网络异常", code=502) from exc
```

### 4.4 命令行验证

```bash
# 直接运行，观察日志与 traceback
python -m app.service

# 提升日志级别到 DEBUG
python -c "import logging; logging.basicConfig(level=logging.DEBUG); import app.service"

# 把弃用告警升级为异常，便于定位旧 API 用法
python -W error::DeprecationWarning app/main.py
```

## 五、最佳实践与常见坑

**最佳实践**

- **捕获具体异常，不滥用 `except Exception`**：兜底放在最后，且务必记录或重抛，否则会吞掉真实错误。
- **用 `logging` 而非 `print`**：`print` 无级别、无时间戳、无法按环境分流；`logging` 可随环境调整级别与输出。
- **日志使用惰性格式化**：`log.debug("x=%s", x)` 优于 `log.debug(f"x={x}")`，低级别不输出时避免无谓计算。
- **异常信息带上下文**：附上关键入参、ID 等，但不要记录密码、令牌等敏感信息。
- **异常组 + `except*` 处理并发批量失败**，避免单个任务失败导致整批结果丢失。
- **自定义异常保持层级稳定**，为未来扩展留空间，便于调用方按基类统一捕获。
- **异步场景注意异常传播**：`TaskGroup` 会把子任务异常聚合为 `ExceptionGroup`，应配合 `except*` 处理。

**常见坑**

- **`finally` 中的 `return` / `break` / `continue`**：**Python 3.14 起仅产生 `SyntaxWarning`（PEP 765，Final），不是立即报错**，但会掩盖 `try` 块中的异常，语言规范允许未来升级为 `SyntaxError`。正确做法是先保存结果，再在 `finally` 之外返回。
- **裸 `except:`**：会连 `SystemExit`、`KeyboardInterrupt` 一起吞掉，属于典型反模式。
- **`except` 块内忘记 `raise`**：异常被静默吞掉，故障难以发现。
- **在 `except` 中操作已失效的资源**：例如已关闭的对象，应记录后重抛，避免引发二次异常。
- **日志重复输出**：子 Logger 默认 `propagate = True`，若父级也挂了 Handler 会打印两遍；配置层级时需明确是否传播。
- **`logging.warn()` 已弃用**：自 Python 3.3 起应使用 `warning()`，迁移老代码时顺手替换。
- **测试中泄漏警告**：Python 3.15 起 `assertWarns()` / `assertWarnsRegex()` 不再吞掉不匹配的警告，可能让此前被屏蔽的告警浮出，需用 warning filters 或补充 `assertWarns*()` 捕获。
- **把警告一律当异常**：`warnings` 默认不中断执行，只有在需要严格约束时才用 `filterwarnings` 升级，不要在所有环境都设为 `error`。

## 六、核心要点速查

1. 异常继承体系：`BaseException` → `Exception`；`SystemExit` / `KeyboardInterrupt` / `GeneratorExit` 属控制流，业务代码不应捕获。
2. `try` 四要素：`except`（处理）/ `else`（无异常时）/ `finally`（必执行，资源释放）。
3. 异常链三属性：`__context__`（隐式）、`__cause__`（`raise X from Y`）、`__traceback__`。
4. `except` 按声明顺序匹配，子类在前、父类在后；未捕获则沿调用栈向上传播。
5. **PEP 654（3.11）**：`BaseExceptionGroup` / `ExceptionGroup` + `except*` 递归匹配，未匹配部分继续传播。
6. **PEP 765（3.14，Final）**：`finally` 内 `return/break/continue` 目前**仅 `SyntaxWarning`，非立即报错**，但应避免。
7. 自定义异常：从业务基类派生，`__init__` 中保留错误码等上下文，便于统一捕获与日志。
8. `logging` 三层：Logger（分层命名）→ Handler（输出去向，如 `RotatingFileHandler`）→ Formatter（格式）。
9. 级别递增：`DEBUG < INFO < WARNING < ERROR < CRITICAL`；最终级别取 Logger 与 Handler 的较严格者。
10. 生产动作模板：**记录日志 → 转换/重新抛出 → 在边界统一处理**。
11. 日志用惰性格式化 `log.debug("x=%s", x)`，避免低级别无谓计算。
12. `logging.warn()` 自 Python 3.3 弃用，改用 `warning()`。
13. Python 3.15：`assertWarns()` 不再吞掉不匹配警告；`IsolatedAsyncioTestCase` 返回非 `None` 被弃用。

## 七、学习资源

- [PEP 654 – Exceptions and Exception Groups](https://peps.python.org/pep-0654/)
- [PEP 765 – Disallow return/break/continue in finally blocks](https://peps.python.org/pep-0765/)
- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 3.14 What's new（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [The logging module – Tutorial（Python 官方文档）](https://docs.python.org/3/library/logging.html)
- [The warnings module（Python 官方文档）](https://docs.python.org/3/library/warnings.html)
- [Python 官方版本列表（python.org）](https://www.python.org/doc/versions/)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 技术全景总览，定位本知识点在体系中的位置
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 装饰器、元编程、类型等进阶主题
- [[编程语言]] — 跨语言异常与错误处理的宏观对比视角

## 九、变更记录

- 2026-11-19：首次创建。
