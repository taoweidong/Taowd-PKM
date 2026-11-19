---
title: Python 并发编程（多线程/多进程/协程）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 并发编程
  - 多线程
  - 多进程
  - 协程
aliases:
  - Python 并发编程
  - Python 多线程多进程协程
source: 网络资料整理
---

# Python 并发编程（多线程/多进程/协程）

> [!摘要] 摘要
> 本文系统梳理 Python 并发编程的三条主线——多线程（`threading`）、多进程（`multiprocessing` / `ProcessPoolExecutor`）、协程（`asyncio`）——从基础概念、核心机制到可运行的实战步骤与常见坑。重点说明 **GIL 对三种模型的影响边界**、**截至 2026-11 的版本新变化**（自由线程 PEP 703/779、子解释器 PEP 734、asyncio 对自由线程的一等支持、`multiprocessing` 默认启动方式变更等），并给出选型决策与迁移建议。适合已掌握 Python 基础、需要在实际项目中做并发选型与性能调优的开发者。

## 一、最新动态（截至 2026-11）

- **当前稳定主线为 Python 3.15**（3.15.0 于 2026-10-09 首发，最新补丁 **3.15.2** 于 2026-10-25 发布，属紧急安全发布）；3.16 处于预发布阶段（`3.16.0a2`，2026-11-10）。3.14 维护线最新为 **3.14.10**（2026-10-25，同样为安全发布）。
- **自由线程（可选 GIL，PEP 703）**：3.13 引入实验性构建，**3.14 起「正式受支持」（PEP 779 第二阶段）**，但仍是**可选构建**。3.14 完成 PEP 703 实现（含 C API）并启用 PEP 659 特化自适应解释器，**单线程性能惩罚约 5–10%**；**3.15 起官方 macOS 二进制默认安装自由线程支持**，并新增 **`abi3t` 稳定 ABI（PEP 803）**，便于 C 扩展兼容自由线程构建。
- **标准库多解释器（PEP 734，Python 3.14）**：新增 `concurrent.interpreters` 模块，可在**同进程内**运行多个相互隔离的解释器，实现 CSP/Actor 风格并发与真多核并行，另有 `concurrent.futures.InterpreterPoolExecutor`。其基础是 3.12 的 **PEP 684**（每解释器独立 GIL）。当前限制：解释器启动尚未优化、内存开销较大、跨解释器共享选项少（主要是 `memoryview`）、部分第三方扩展尚未兼容。
- **asyncio（协程）**：**自 3.14 起对自由线程构建有一等支持**，事件循环实现对多线程环境安全；原生任务改用双链表实现，pyperformance 上**快 10–20%**，并支持外部内省。3.14 新增 `python -m asyncio ps PID` 与 `python -m asyncio pstree PID` 查看任务表 / 异步调用树。
- **多线程工具**：3.14 新增 `-X context_aware_warnings`（默认在自由线程构建为 `true`、GIL 构建为 `false`）与 `thread_inherit_context`，使 `catch_warnings` 的警告过滤上下文可被线程 / asyncio 任务继承。
- **多进程**：**3.14 起 Unix（非 macOS）上 `forkserver` 成为 `multiprocessing` 与 `ProcessPoolExecutor` 的默认启动方式**（原为 `fork`）；Windows/macOS 仍默认 `spawn`。**3.15 修复 `multiprocessing.Pool` 回调异常导致的死锁**。
- **3.15 并发相关弃用**：`threading.Condition.notifyAll()`→`notify_all()`、`Event.isSet()`→`is_set()`、`Thread.isDaemon()/setDaemon()`→`daemon` 属性、`Thread.getName()/setName()`→`name`、`currentThread()`→`current_thread()`、`activeCount()`→`active_count()`。

> [!info] 版本说明
> 上述版本号与 PEP 状态均来自 Python 官方文档 / PEP 官方仓库，来源见「七、学习资源」。第三方库补丁更新频繁，实际使用前以写作当日 PyPI / 官方发布页为准。

## 二、基础概念

并发编程的核心是：**在有限资源下让多个任务交替或同时推进，从而掩盖等待、提高吞吐**。Python 提供三种彼此互补的模型，关键区别在于「是否受 GIL 限制」和「切换代价」。

- **全局解释器锁（GIL）**：CPython 同一时刻只允许一个线程执行 Python 字节码，因此**纯 Python 的多线程无法利用多核做 CPU 并行**，但 GIL 会在 I/O 操作时释放，因此多线程对 I/O 密集任务仍然有效。
- **多线程（`threading`）**：轻量、共享内存、切换成本低；适合 I/O 等待（网络、文件、数据库）和需要共享状态的任务。受 GIL 限制，CPU 密集任务无效。
- **多进程（`multiprocessing`）**：每个进程有独立解释器与 GIL，**可真正利用多核**；代价是进程创建/IPC 开销大、内存不共享，需通过队列、管道、`SharedMemory` 等传递数据。
- **协程（`asyncio`）**：单线程内的协作式并发，由事件循环调度，**切换几乎零开销**；适合大量 I/O 等待（高并发连接、网络服务）。不能直接利用多核，需配合多进程或多线程/多解释器横向扩展。
- **执行器（`concurrent.futures`）**：`ThreadPoolExecutor` / `ProcessPoolExecutor` 提供统一的 `submit` / `map` / `as_completed` 接口，把线程/进程模型封装成任务式 API，是日常最常用的入口。

> [!tip] 一句话选型
> **I/O 密集用 asyncio；需要共享内存的 I/O 密集用线程；CPU 密集用多进程；真多核并行可关注自由线程与子解释器。**

## 三、核心机制

**1. 多线程机制**

`threading` 以线程为调度单位，由 GIL 保证字节码互斥。常用组件：`Thread`、`Lock`/`RLock`、`Condition`、`Event`、`Semaphore`、`Barrier`、`ThreadLocal`。共享可变状态必须加锁保护，否则会出现竞态。

**2. 多进程机制**

`multiprocessing` 为每个任务创建独立进程，各自持有 GIL，从而突破单核限制。进程间通过 `Queue`、`Pipe`、`Manager`、`SharedMemory` 通信。`ProcessPoolExecutor` 是其 Future 风格封装。**注意 3.14 起默认启动方式变化**：Unix（非 macOS）默认由 `fork` 变为 `forkserver`，子进程不再隐式继承父进程内存状态，依赖隐式共享状态的旧代码需要检查。

**3. 协程机制**

`asyncio` 的核心是**事件循环 + 协程 + 任务**。协程函数用 `async def` 定义，`await` 挂起并让出控制权；事件循环在 I/O 就绪时恢复对应协程。`Task` 是协程的并发调度单元，`asyncio.run()` 负责创建并管理事件循环。3.14 起任务内部改用双链表实现，并支持外部内省。

**4. 自由线程与子解释器（前沿）**

自由线程构建移除了 GIL，让多线程真正并行，但要求 C 扩展按自由线程重新构建、帧对象跨线程不安全；子解释器则在同一进程内提供解释器级隔离，兼顾隔离与较低开销。二者均面向多核，但需评估第三方库支持度与运维复杂度。

## 四、实践步骤（含代码/命令示例）

**1. 多线程：线程池执行 I/O 任务**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch(name: str, delay: float) -> str:
    # 模拟 I/O 等待：真实场景下替换为 requests / 数据库调用
    import time
    time.sleep(delay)
    return f"{name} 完成"


def main() -> None:
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(fetch, f"任务{i}", 0.5) for i in range(6)]
        for fut in as_completed(futures):
            print(fut.result())


if __name__ == "__main__":
    main()
```

**2. 多进程：进程池做 CPU 密集计算**

```python
import math
from concurrent.futures import ProcessPoolExecutor


def count_primes(n: int) -> int:
    return sum(1 for i in range(2, n) if math.isqrt(i) ** 2 != i and _is_prime(i))


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        for n, result in zip([5000, 10000, 20000], pool.map(count_primes, [5000, 10000, 20000])):
            print(f"<= {n} 的素数个数：{result}")
```

> [!warning] Windows 注意
> Windows/macOS 默认 `spawn` 启动，被调度的函数**必须可被导入**，因此要放在 `if __name__ == "__main__":` 保护之下，避免无限递归创建子进程。

**3. 协程：asyncio 结构化并发**

```python
import asyncio


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # 模拟 I/O
    return f"{name} 完成"


async def main() -> None:
    # 结构化并发：任一任务失败会自动取消其余任务
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch("A", 0.3))
        tg.create_task(fetch("B", 0.1))
    print("全部完成")


if __name__ == "__main__":
    asyncio.run(main())
```

**4. 线程安全：锁保护共享计数器**

```python
import threading

counter = 0
lock = threading.Lock()


def increment() -> None:
    global counter
    with lock:
        for _ in range(1000):
            counter += 1


threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)  # 10000
```

**5. 环境与依赖准备**

```bash
# 创建隔离环境（推荐 uv，速度远快于 venv）
uv init
uv add  # 按需添加依赖
uv run python main.py

# 或使用标准库 venv
python -m venv .venv
```

## 五、最佳实践与常见坑

- **按负载选型，不要为「并发」而并发**：CPU 密集任务用多线程会因 GIL 而无效甚至更慢；I/O 密集任务用多进程则徒增进程与 ICPC 开销。
- **协程中不要阻塞**：在协程内调用 `time.sleep()`、同步 `requests`、同步数据库驱动会卡住整个事件循环。改用 `asyncio.sleep`、`httpx.AsyncClient`、异步驱动；确需阻塞调用时，用 `asyncio.to_thread()` 或 `run_in_executor` 交给线程池。
- **线程共享状态必须加锁**：读写共享变量、缓存、连接池都要用 `Lock`/`RLock` 或线程安全容器保护；`ThreadLocal` 可避免部分竞态，但不要跨线程依赖。
- **进程池与启动方式**：3.14 起 Unix（非 macOS）默认 `forkserver`，依赖 `fork` 隐式共享状态的代码需回归验证；被调度函数须可导入，入口加 `if __name__ == "__main__":` 保护。
- **await 不要泄漏**：创建的 `Task` 若未被 `await`/收集，异常可能被静默吞掉；优先用 `TaskGroup`、`asyncio.gather`，生产环境开启异常传播。
- **遵守 3.15 弃用 API**：把 `notifyAll()`、`isSet()`、`isDaemon()`、`getName()`、`currentThread()`、`activeCount()` 迁移到 `notify_all()`、`is_set()`、`daemon`、`name`、`current_thread()`、`active_count()`。
- **自由线程/子解释器落地要评估**：自由线程构建需 C 扩展重编译、单线程约 5–10% 性能代价；子解释器内存开销大、共享选项少。先用 Tachyon（3.15，PEP 799）定位真实瓶颈再决定是否切换。
- **可观测与调试**：用 `python -m asyncio ps / pstree <PID>` 内省运行中进程的异步任务；多进程问题留意回调异常可能引发死锁（3.15 已修复一例）。

## 六、核心要点速查

1. **GIL 边界**：多线程无法做纯 Python 的 CPU 并行；多进程可多核并行；协程是单线程内协作式并发。
2. **选型公式**：I/O 密集→asyncio；共享内存 I/O→threading；CPU 密集→multiprocessing；真多核并行→自由线程/子解释器。
3. **`concurrent.futures` 统一入口**：`ThreadPoolExecutor` 与 `ProcessPoolExecutor` 提供 `submit/map/as_completed`。
4. **结构化并发**：`asyncio.TaskGroup` 自动管理任务生命周期与异常传播。
5. **版本事实**：Python 3.15.2（2026-10-25）为最新稳定补丁；3.14.10（2026-10-25）为稳定线主力。
6. **自由线程**：PEP 703，3.13 实验、3.14 起正式受支持（PEP 779 第二阶段），可选构建，单线程约 5–10% 代价，3.15 提供 `abi3t`。
7. **子解释器**：PEP 734（3.14）`concurrent.interpreters` + `InterpreterPoolExecutor`，进程级隔离 + 线程级开销。
8. **asyncio 3.14**：对自由线程有一等支持；任务双链表快 10–20%；新增 `python -m asyncio ps/pstree`。
9. **multiprocessing 3.14**：Unix（非 macOS）默认启动方式由 `fork` 改为 `forkserver`；3.15 修复 `Pool` 回调死锁。
10. **3.15 弃用**：`notifyAll`/`isSet`/`isDaemon`/`getName`/`currentThread`/`activeCount` 等旧名迁移到新 API。

## 七、学习资源

**官方文档**

- [Python 3.15 What's New（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 3.14 What's New（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Python 3.13 What's New（Python 官方文档）](https://docs.python.org/3.13/whatsnew/3.13.html)
- [concurrent.futures — Thread and Process Pool Executors（官方库文档）](https://docs.python.org/3/library/concurrent.futures.html)
- [threading — Thread-based Concurrency（官方库文档）](https://docs.python.org/3/library/threading.html)
- [multiprocessing — Process-based Concurrency（官方库文档）](https://docs.python.org/3/library/multiprocessing.html)
- [Developing with asyncio（官方库文档）](https://docs.python.org/3.11/library/asyncio-dev.html)

**PEP 与前沿特性**

- [PEP 703 – Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/)
- [PEP 779 – Criteria for supported status for free-threaded Python](https://peps.python.org/pep-0779/)
- [PEP 734 – Adding Sub-interpreters from the Standard Library](https://peps.python.org/pep-0734/)
- [Python experimental support for free threading（官方文档）](https://docs.python.org/3.13/howto/free-threading-python.html)

## 八、关联笔记

- [[Python-从入门到精通]] — 本知识点在 Python 体系中的全景定位与总览
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 装饰器、元编程、类型等进阶主题
- [[Python-asyncio异步编程]] — asyncio 协程的深入专题
- [[Java-并发编程笔记]] — 与 Java 并发模型（线程/锁/容器）的横向对比
- [[编程语言]] — 跨语言并发模型的宏观视角

## 九、变更记录

- 2026-11-19：首次创建。
