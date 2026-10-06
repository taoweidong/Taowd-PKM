---
source: "https://thecodeforge.io/python/python-asyncio-deep-dive/"
title: "Python Concurrency: Python asyncio — 47-Second Freeze"
fetched_at: "2026-10-06 12:47"
---

Advanced 10 min · March 06, 2026 

Python Concurrency — asyncio Deep Dive

# Python asyncio — 47-Second Freeze from Sync Calls

A sync `requests.get()` blocked the event loop for 47s—zero CPU, all coroutines frozen. 

N

Naren Founder & Principal Engineer

20+ years shipping production Python across data and backend systems. Notes here come from systems that actually shipped. 

[ Follow ](https://www.linkedin.com/in/thecodeforge-io-a0676b3b5/)

✓ Production 

production tested

September 26, 2026

last updated

2,085

articles · all by Naren

Before you start⏱ 30 min

  * ✓Deep production experience
  * ✓Understanding of internals and trade-offs
  * ✓Experience debugging complex systems



● Production Incident 🔎 Debug Guide ⚙ Triage Commands

⚡Quick Answer

  * asyncio is Python's single-threaded concurrency library using async/await syntax
  * The Event Loop is the central scheduler — it multiplexes I/O across coroutines without OS threads
  * Coroutines yield control at every `await` point, enabling cooperative multitasking
  * asyncio.gather() runs independent I/O tasks concurrently — total time equals the slowest task, not the sum
  * Blocking the loop with sync calls (requests.get, time.sleep) freezes ALL coroutines — use run_in_executor for sync code
  * For CPU-bound work, use multiprocessing — asyncio cannot bypass the GIL



✦ Definition~90s read

What is Python Concurrency?

Asyncio is a concurrency framework for I/O-bound work running in a single thread. It's not parallelism. It won't make your CPU-bound loops faster. What it does is let you juggle a thousand open network connections without breaking a sweat.

★

Imagine you are a chef in a busy kitchen.

The event loop sits in the middle. It polls file descriptors, schedules coroutines when data arrives, and yields control back to waiting tasks. No threads, no GIL contention — just cooperative multitasking with explicit yield points.

When you call `asyncio.run(`main()`)`, that creates a new event loop, runs ``main()`` as a coroutine, and blocks until done. Inside that loop, every `await` is a handshake: "I'm waiting on something — go run someone else's code while I do." If you forget to await, you get a coroutine object, not execution.

If you block the loop with a ``time.sleep()`` instead of ``asyncio.sleep()``, you freeze the entire show for every other task.

The hard truth: asyncio is powerful, but it demands discipline. One synchronous call to ``requests.get()`` inside a coroutine and your async web server is now serving one request at a time.

Plain-English First

Imagine you are a chef in a busy kitchen. In a synchronous kitchen, you put toast in the toaster and stand motionless staring at it until it pops before you touch anything else. That is a waste of time and the customers notice. In an asyncio kitchen, you put the toast in, set a timer — that is the await — and immediately start grinding coffee beans while the toast browns. You are not growing extra arms, which would be threads. You are just being smart about using the waiting time productively. The event loop is the head chef managing all those timers simultaneously, making sure nothing burns and breakfast reaches the table faster. The moment you drop a heavy cookbook on the floor and spend five minutes picking it up, everyone in the kitchen freezes waiting for you. That cookbook is a blocking call.

asyncio solves a specific and important [scalability](/system-design/scalability-concepts/) problem: how do you handle thousands of concurrent I/O operations without spawning thousands of OS threads? The answer is cooperative multitasking — coroutines voluntarily yield control at await points, allowing a single-threaded [event loop](/javascript/event-loop-javascript/) to multiplex work across all of them efficiently. No thread management, no locking, no context switch overhead from the OS.

The distinction senior engineers must genuinely internalise is that asyncio is concurrency, not parallelism. One thread handles all scheduling. This means any blocking call — a synchronous HTTP request, a CPU-heavy computation, even `time.sleep()` — freezes the entire loop and every coroutine waiting on it. Not some of them. All of them. This is the property that makes asyncio both powerful and dangerous: the performance gains from concurrency and the catastrophic failure mode from a single blocking call live right next to each other in the same codebase.

This guide covers production-grade patterns: orchestrating concurrent tasks with `gather()`, building fault-tolerant batch operations against unreliable dependencies, understanding the timeout and cancellation model deeply enough to use it correctly under pressure, and the operational mistakes I have seen repeatedly bring down async services. The examples are written for [Python](/python/introduction-python/) 3.11+ but the core patterns apply from 3.8 onward.

## Why Your Async Code Freezes for 47 Seconds

asyncio is Python's cooperative concurrency model: a single-threaded event loop that multiplexes I/O-bound tasks by yielding control at explicit await points. The core mechanic is that only one coroutine runs at a time, and it must voluntarily suspend itself before another can proceed. This means any synchronous blocking call — `time.sleep()`, a CPU-bound loop, or a blocking I/O operation — stalls the entire event loop for its full duration. In practice, a single sync call of 47 milliseconds can cascade into a 47-second freeze under load because the loop cannot schedule other coroutines. Use asyncio when your workload is I/O-bound with many concurrent operations (network requests, file reads, database queries) and you need to maximize throughput without the overhead of threads. It is not a solution for CPU-bound work — that requires multiprocessing or thread pools. The real-world impact: a single sync call in a web server's async handler can drop thousands of requests per second.

⚠ The 47-Second Freeze

A single time.sleep(0.047) in an async handler blocks the event loop for 47 seconds under 1000 concurrent requests — each request adds its own delay.

📊 Production Insight

A Redis cache call using redis-py's synchronous client inside an async FastAPI endpoint blocks the event loop for 50ms per request. Under 200 concurrent requests, the last request waits 10 seconds. The fix: always use aioredis or run sync calls in a thread pool executor.

🎯 Key Takeaway

asyncio is cooperative, not preemptive — one blocking call freezes all tasks.

Use asyncio only for I/O-bound work; CPU-bound tasks need threads or processes.

Always verify every library call in your async path is truly non-blocking.

thecodeforge.io

Python Asyncio Deep Dive

## Coroutines and the Event Loop: The Engine Room

A coroutine is a specialised Python generator with async/await syntax. When you define a function with async def, calling it does not execute a single line of the function body — it returns a coroutine object. To actually run it, you must either await it inside another coroutine or schedule it on the event loop via `asyncio.create_task()` or `asyncio.run()`. This is not a convention or a style choice — it is how the object model works.

A common misconception is that async def makes a function asynchronous in some broad sense. It does not. It makes the function coroutine-returning. The function body executes zero lines until the coroutine is awaited or scheduled. Forgetting this distinction leads to one of the most common asyncio bugs in production codebases: creating a coroutine object, not awaiting it, and then wondering why the operation never happened. Python 3.11+ will emit a RuntimeWarning about this, but only if something holds a reference long enough to trigger [garbage collection](/java/garbage-collection-java/) — in high-throughput code where objects are short-lived, this warning is sometimes never emitted.

The event loop is the heartbeat of every asyncio application. It maintains a [queue](/dsa/queue-data-structure/) of ready callbacks, a selector watching registered I/O file descriptors (using epoll on Linux, kqueue on macOS, IOCP on Windows), and a heap of scheduled callbacks ordered by their scheduled time. When a coroutine awaits an I/O operation, it registers a callback with the selector and suspends — control returns to the loop, which picks the next ready callback and runs it. When the OS signals that I/O is complete, the selector delivers the event, the callback is scheduled, and the original coroutine resumes from exactly where it yielded. This entire mechanism happens in a single thread. No OS context switches. No lock contention. No [stack](/dsa/stack-data-structure/) per concurrent operation beyond the coroutine frame itself.

io_thecodeforge/basics.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34
    
    
    import asyncio
    import time
    
    # Production-grade coroutine with proper type hints.
    # Note: calling fetch_service_status() without await returns a coroutine object.
    # Calling it with await runs the body and returns the string result.
    async def fetch_service_status(service_name: str, delay: float) -> str:
        print(f"[io.thecodeforge] Requesting status for {service_name}...")
        # await suspends this coroutine and yields control back to the event loop.
        # The loop is free to run other coroutines during this delay.
        # asyncio.sleep() is non-blocking — it registers a timer callback, not a thread sleep.
        await asyncio.sleep(delay)
        return f"{service_name}: UP"
    
    
    async def main():
        start_time = time.perf_counter()
    
        # SEQUENTIAL ANTI-PATTERN: awaiting independent tasks one at a time.
        # Each await suspends main() until that coroutine finishes.
        # Auth-Service completes, then Payment-Gateway starts. Never concurrent.
        # Total time = sum of all delays = 1.0 + 1.0 = ~2.0 seconds.
        status_a = await fetch_service_status("Auth-Service", 1.0)
        status_b = await fetch_service_status("Payment-Gateway", 1.0)
    
        total_time = time.perf_counter() - start_time
        print(f"Sequential results: {status_a}, {status_b}")
        print(f"Total Sequential Time: {total_time:.2f}s")
        # Output: ~2.00s — we are paying the full cost of both delays in series.
        # The next section shows how gather() eliminates this waste.
    
    
    if __name__ == "__main__":
        asyncio.run(main())

Output

[io.thecodeforge] Requesting status for Auth-Service...

[io.thecodeforge] Requesting status for Payment-Gateway...

Sequential results: Auth-Service: UP, Payment-Gateway: UP

Total Sequential Time: 2.00s

Mental Model

The Event Loop Mental Model

Think of the event loop as a single-threaded task dispatcher backed by an OS-level I/O multiplexer — epoll on Linux, kqueue on macOS. It does not run things in parallel. It runs one thing at a time, very efficiently, with zero idle time between tasks.

  * Each await is a voluntary yield — the coroutine says 'I am waiting on I/O, run something else while I am paused'
  * The loop maintains a selector that monitors all registered I/O file descriptors and a callback heap ordered by scheduled time
  * When I/O completes, the OS notifies the selector, the loop schedules the corresponding callback, and the suspended coroutine resumes
  * No parallel execution ever happens — at any given instant, exactly one coroutine is executing Python bytecode
  * Context switches happen only at await boundaries — never mid-expression, never between two lines in the same function body



📊 Production Insight

Calling a coroutine function without await returns a coroutine object silently — no error, no side effects, nothing.

In production this manifests as operations that appear to run (the call succeeds) but produce no output, write nothing to the database, and send nothing to the network.

Rule: enable PYTHONASYNCIODEBUG=1 or loop.set_debug(True) in staging — it logs unawaited coroutines when they are garbage collected, which is your only warning that this is happening.

🎯 Key Takeaway

A coroutine is inert until scheduled — calling it without await produces a silent no-op with no error in non-debug mode.

The event loop is single-threaded: one blocking call anywhere in a handler freezes every coroutine across the entire process.

Rule: if it is not awaited or scheduled via `create_task()`, it is not running — there is no in-between state.

IfNeed to run a coroutine and wait for its result immediately before doing anything else

→

UseUse await `coroutine()` — suspends the current coroutine until the result is ready, no scheduling overhead

IfNeed to start work now but collect the result later in the same function

→

UseUse asyncio.create_task(`coroutine()`) — schedules the coroutine immediately on the loop, returns a Task handle you can await later

IfNeed to run multiple independent coroutines concurrently and collect all results

→

UseUse asyncio.gather(*coroutines) — schedules all coroutines, waits for all to complete, returns results in input order

IfNeed to bridge callback-based code with async/await, or signal completion from outside the event loop

→

UseUse asyncio.Future — low-level primitive; in application code prefer `create_task()` over raw Futures for clarity

## asyncio.gather() — Orchestrating True Concurrency

When you have independent I/O operations, awaiting them sequentially one by one is leaving performance on the table. If you have three health checks that each take one second, awaiting them in series costs three seconds. Running them with `gather()` costs one second — the duration of the slowest one. That is the entire value proposition of `gather()`, and it is substantial.

asyncio.gather() takes an iterable of coroutines (or awaitables), wraps each one into a Task internally via `create_task()`, and schedules them all onto the event loop simultaneously. It then suspends the calling coroutine until every task completes, and returns a list of results in the same order as the input arguments — regardless of which tasks finished first. This ordering guarantee is important and worth relying on: you can safely unpack results positionally.

One nuance worth understanding: gather() creates tasks at the moment it is called, not at the moment the await resolves. This means all tasks start running as soon as the event loop gets control after the `gather()` call, which is immediately when the caller awaits `gather()`. If you are constructing a list of coroutines before calling `gather()`, those coroutines have not started yet — they are still inert coroutine objects. Only `gather()` turns them into running Tasks.

The performance model is straightforward: gather() converts sequential wait time into concurrent wait time. The total duration is bounded by max(all task durations) rather than sum(all task durations). For workloads involving many small network calls — health checks, fanout requests to [microservices](/java/microservices-interview-questions/), parallel database lookups — this can reduce latency by an order of magnitude.

io_thecodeforge/concurrency.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37
    
    
    import asyncio
    import time
    
    
    async def fetch_service_status(service_name: str, delay: float) -> str:
        print(f"[io.thecodeforge] Requesting status for {service_name}...")
        await asyncio.sleep(delay)
        return f"{service_name}: UP"
    
    
    async def main():
        start_time = time.perf_counter()
    
        # CONCURRENT PATTERN: gather() wraps each coroutine into a Task
        # and schedules all three onto the event loop simultaneously.
        # The loop runs them interleaved: Database yields at its await,
        # Cache runs until its await, Search-Index runs until its await,
        # and so on until all three complete.
        #
        # Total time = max(1.5, 0.5, 1.2) = ~1.5 seconds, not 1.5+0.5+1.2 = 3.2s.
        results = await asyncio.gather(
            fetch_service_status("Database", 1.5),
            fetch_service_status("Cache", 0.5),
            fetch_service_status("Search-Index", 1.2),
            # In production, always include return_exceptions=True.
            # Omitted here for clarity — see the Fault Tolerance section.
        )
    
        total_time = time.perf_counter() - start_time
    
        # Results are in input order regardless of completion order.
        # Cache finished first (0.5s) but results[1] is Cache — positional, guaranteed.
        print(f"Concurrent Results: {results}")
        print(f"Total Concurrent Time: {total_time:.2f}s")
    
    
    asyncio.run(main())

Output

[io.thecodeforge] Requesting status for Database...

[io.thecodeforge] Requesting status for Cache...

[io.thecodeforge] Requesting status for Search-Index...

Concurrent Results: ['Database: UP', 'Cache: UP', 'Search-Index: UP']

Total Concurrent Time: 1.50s

⚠ Default Exception Behaviour in gather() Creates Orphaned Tasks

This is the most consequential gotcha in `gather()` and the one most likely to cause resource leaks in production.

📊 Production Insight

gather() without return_exceptions=True propagates the first exception and abandons remaining tasks — they continue consuming resources with no owner.

In a service making 1000 `gather()` calls per second with a 5% upstream failure rate, the default behaviour creates dozens of orphaned tasks every second.

Rule: in production, always use return_exceptions=True and handle each result in a loop — the extra three lines of inspection code have prevented more incidents than I can count.

🎯 Key Takeaway

gather() converts sequential wait time into concurrent wait time — three 1-second tasks finish in ~1 second, not ~3 seconds.

The results list is always in input order regardless of task completion order — you can safely unpack positionally.

Default exception behaviour silently creates orphaned tasks that leak resources — always use return_exceptions=True in production.

IfHave a fixed, known list of independent coroutines and need all results before proceeding

→

UseUse asyncio.gather(*coroutines, return_exceptions=True) — waits for all, returns ordered results, captures all exceptions

IfNeed to start a background operation and collect its result later in the same function scope

→

UseUse `asyncio.create_task()` — schedules immediately, returns a Task handle, await it whenever you need the result

IfNeed structured concurrency with automatic cancellation of sibling tasks on any failure

→

UseUse asyncio.TaskGroup (Python 3.11+) — if one task raises, all others are cancelled cleanly and ExceptionGroup is raised

IfNeed to add tasks dynamically as they are discovered during processing

→

UseUse a task set with `create_task()` and `asyncio.wait()` — `gather()` requires all coroutines to be specified upfront

thecodeforge.io

Python Asyncio Deep Dive

## Fault Tolerance: Exceptions, Timeouts, and Cancellation

In production, external APIs fail, network partitions happen, and upstream services degrade. The question is not whether these events will occur — it is whether your async code handles them gracefully or cascades them into wider outages.

The two primary tools for fault tolerance in asyncio are gather(return_exceptions=True) for batch resilience and `asyncio.wait_for()` for individual operation timeouts. They address different failure modes and are commonly used together.

gather(return_exceptions=True) is the production standard for any batch operation against multiple dependencies. Instead of letting the first exception short-circuit the entire batch, it captures all exceptions as return values — Exceptions are just results that happen to be error objects. You iterate the results list, check isinstance(result, Exception) for each entry, and handle successes and failures individually. Every task gets a chance to complete. No orphaned tasks. Full visibility into which dependencies failed and which succeeded.

asyncio.wait_for(coroutine, timeout=seconds) enforces a maximum duration on a single coroutine. If the coroutine does not complete within the timeout, asyncio raises TimeoutError and cancels the wrapped coroutine. This is the mechanism for implementing SLAs on individual downstream calls — if your upstream health check should complete in under 3 seconds, wrap it in `wait_for()` with timeout=3.0 and handle TimeoutError explicitly.

Cancellation is where most engineers get tripped up. When `wait_for()` fires, it sends a CancelledError to the wrapped coroutine at its current await point. If the coroutine has cleanup logic that also awaits — closing a database connection, writing an audit log, releasing a lock — that cleanup will only run if it is inside a try/finally block. Code after a cancelled await does not execute. This is cooperative cancellation, and respecting it correctly is what separates async code that is safe from async code that merely appears to work in testing.

io_thecodeforge/resilience.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70
    
    
    import asyncio
    from typing import Any
    
    
    async def api_call(name: str, should_fail: bool = False, delay: float = 0.2) -> str:
        """Simulates an external API call with configurable failure and latency."""
        await asyncio.sleep(delay)
        if should_fail:
            raise RuntimeError(f"Upstream failure in {name}")
        return f"{name}_data"
    
    
    async def main():
        # --- Pattern 1: Defensive Gathering ---
        # return_exceptions=True captures all outcomes.
        # No task is abandoned. Every failure is inspectable.
        tasks = [
            api_call("Payment-API"),
            api_call("Inventory-API", should_fail=True),  # this one will fail
            api_call("Shipping-API"),
        ]
        results: list[Any] = await asyncio.gather(*tasks, return_exceptions=True)
    
        successes = []
        failures = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failures.append((i, result))
                print(f"[FAILED] Task {i}: {result}")
            else:
                successes.append(result)
                print(f"[OK]     Task {i}: {result}")
    
        print(f"\nSucceeded: {len(successes)}, Failed: {len(failures)}")
    
        # --- Pattern 2: Enforcing Timeouts with wait_for ---
        # The slow API takes 2 seconds. Our SLA is 0.5 seconds.
        print("\n--- Timeout enforcement ---")
        try:
            result = await asyncio.wait_for(
                api_call("Slow-Upstream-API", delay=2.0),
                timeout=0.5
            )
        except asyncio.TimeoutError:
            # TimeoutError means the coroutine was cancelled after 0.5 seconds.
            # The downstream call may still be in flight on the remote server —
            # we just stopped waiting for it.
            print("Slow-Upstream-API exceeded 500ms SLA — request cancelled.")
    
        # --- Pattern 3: Protecting cleanup with try/finally ---
        # Cleanup runs even if the coroutine is cancelled mid-execution.
        async def careful_operation() -> str:
            try:
                await asyncio.sleep(5.0)  # this will be cancelled
                return "completed"
            finally:
                # This runs even on CancelledError — use it for cleanup.
                print("[Cleanup] Releasing resources on cancellation.")
    
        print("\n--- Cancellation with cleanup ---")
        task = asyncio.create_task(careful_operation())
        await asyncio.sleep(0.1)  # let the task start
        task.cancel()             # trigger cancellation
        try:
            await task
        except asyncio.CancelledError:
            print("Task was cancelled cleanly.")
    
    
    asyncio.run(main())

Output

[OK] Task 0: Payment-API_data

[FAILED] Task 1: Upstream failure in Inventory-API

[OK] Task 2: Shipping-API_data

Succeeded: 2, Failed: 1

\--- Timeout enforcement ---

Slow-Upstream-API exceeded 500ms SLA — request cancelled.

\--- Cancellation with cleanup ---

[Cleanup] Releasing resources on cancellation.

Task was cancelled cleanly.

Mental Model

Exception Propagation in gather() — Two Modes

gather() has two exception modes that produce fundamentally different behaviours. The difference matters the moment you run it in production against a flaky dependency.

  * Default mode (return_exceptions=False): first exception propagates to the caller, gather resolves, remaining tasks continue running as orphans with no owner
  * Safe mode (return_exceptions=True): all exceptions are captured as return values, no task is abandoned, you inspect each result individually
  * wait_for() raises TimeoutError and cancels the target coroutine at its current await point — cleanup code must be in try/finally
  * CancelledError is a BaseException, not an Exception — catching Exception does not catch it, which is intentional
  * asyncio.shield(coroutine) protects a coroutine from external cancellation — the inner task continues even if the outer scope is cancelled



📊 Production Insight

wait_for() cancels the wrapped coroutine cooperatively — the cancellation is delivered at the next await point inside the coroutine.

If the target coroutine is blocked on a synchronous call (a blocking socket, a CPU loop with no await), it cannot receive the cancellation signal and will not stop.

Rule: every coroutine in a timeout-sensitive path must use only awaitable operations — non-cooperative code cannot be safely cancelled.

🎯 Key Takeaway

return_exceptions=True turns every exception into an inspectable result — this is the production standard for batch resilience against flaky dependencies.

wait_for() enforces SLAs but requires cooperative cancellation — cleanup logic belongs in try/finally, not after the await.

CancelledError is a BaseException — catching Exception in a bare except does not catch it, and that asymmetry is intentional.

## The Golden Rule: Never Block the Event Loop

This is the number one cause of production performance degradation in Python async services, and it is also the most insidious because it does not fail loudly. A blocking call does not raise an exception. It does not log a warning by default. It simply holds the event loop thread for its entire duration, during which every other coroutine in the process is frozen. One synchronous HTTP call taking 200ms freezes 10,000 concurrent connections for 200ms. Under load, these micro-freezes compound into p99 latency spikes that look like intermittent upstream degradation but are entirely self-inflicted.

The most common offenders in codebases I have reviewed: the [requests library](/python/requests-library-python/) (always synchronous, even for simple GET calls), `time.sleep()` used as a delay inside handlers, CPU-heavy operations like image resizing or report generation, and third-party SDK clients that were written before async was widespread. The pattern is usually introduced by someone who understood the application's sync codebase well and did not fully internalise the async execution model.

For unavoidable synchronous code — a legacy library that cannot be replaced, a CPU-intensive operation that has no async equivalent — the correct approach is `loop.run_in_executor()`, which offloads the blocking call to a thread pool and returns an awaitable that the event loop can wait on without blocking itself. The thread pool runs in parallel with the event loop thread. The event loop remains free to process other coroutines while the thread pool handles the blocking work. This adds thread overhead, but it is categorically better than blocking the loop.

For CPU-bound work that needs true parallelism, ProcessPoolExecutor bypasses the GIL by running work in separate processes. The [inter-process communication](/cs-fundamentals/inter-process-communication/) overhead makes this appropriate for coarse-grained work (process this batch) rather than fine-grained work (transform this value).

io_thecodeforge/threading_interop.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56
    
    
    import asyncio
    import time
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    
    
    # This is a synchronous function — it calls time.sleep() which blocks.
    # Calling this directly inside an async handler would freeze the event loop.
    def legacy_report_generator(report_id: str) -> str:
        """Simulates a legacy synchronous library call that cannot be rewritten."""
        time.sleep(2)  # 2-second blocking operation
        return f"Report-{report_id}: generated"
    
    
    def cpu_bound_compression(data: str) -> str:
        """Simulates CPU-intensive work — no I/O, pure computation."""
        # In reality this would be image compression, encryption, ML inference, etc.
        result = sum(ord(c) for c in data * 10000)  # burn some CPU
        return f"Compressed({result})"
    
    
    async def main():
        loop = asyncio.get_running_loop()
    
        # --- Pattern 1: Offload blocking I/O to a thread pool ---
        # ThreadPoolExecutor keeps the event loop free while the thread runs.
        # Other coroutines continue executing during the await.
        print("[1] Offloading blocking sync call to thread pool...")
        with ThreadPoolExecutor(max_workers=4) as thread_pool:
            result = await loop.run_in_executor(
                thread_pool,
                legacy_report_generator,
                "Q4-2026"
            )
        print(f"[1] Result: {result}")
    
        # --- Pattern 2: Offload CPU-bound work to a process pool ---
        # ProcessPoolExecutor creates separate processes with separate GILs.
        # True CPU parallelism — the event loop thread is not blocked.
        print("\n[2] Offloading CPU-bound work to process pool...")
        with ProcessPoolExecutor(max_workers=2) as process_pool:
            result = await loop.run_in_executor(
                process_pool,
                cpu_bound_compression,
                "sensitive_payload_data"
            )
        print(f"[2] Result: {result}")
    
        # --- Pattern 3: The async-native approach (preferred) ---
        # For new code, use async libraries that never block the loop.
        # import httpx
        # async with httpx.AsyncClient(timeout=5.0) as client:
        #     response = await client.get("https://api.thecodeforge.io/data")
        print("\n[3] Async-native approach: use httpx, motor, aiofiles — never requests, pymongo, open()")
    
    
    asyncio.run(main())

Output

[1] Offloading blocking sync call to thread pool...

[1] Result: Report-Q4-2026: generated

[2] Offloading CPU-bound work to process pool...

[2] Result: Compressed(9823400)

[3] Async-native approach: use httpx, motor, aiofiles — never requests, pymongo, open()

⚠ Detecting Event Loop Blocking Before It Reaches Production

Blocking calls are invisible in logs and metrics until they are already causing user-visible latency. These tools make them visible earlier.

📊 Production Insight

A single synchronous `requests.get()` call with a 30-second timeout does not degrade your service — it takes it completely offline for 30 seconds if the upstream is slow.

This is not a performance problem. It is a correctness problem. There is no partial degradation — it is binary.

Rule: add flake8-async or similar linting to your CI pipeline to reject synchronous blocking calls inside async functions before they are merged.

🎯 Key Takeaway

One blocking call in the event loop thread freezes every coroutine in the process — there is no partial degradation, no graceful fallback, just a complete stall.

run_in_executor() is the correct escape hatch for synchronous code that cannot be replaced, but it adds thread overhead — prefer async-native libraries wherever possible.

Rule: if you cannot make it async, move it off the event loop thread entirely.

IfI/O-bound work — network calls, database queries, file reads, message queue polling

→

UseUse asyncio with async-native libraries (httpx, motor, aiofiles, aiokafka) — maximum concurrency with minimum overhead

IfCPU-bound work — image processing, encryption, ML inference, data transformation

→

UseUse multiprocessing or ProcessPoolExecutor to bypass the GIL — asyncio cannot make CPU work concurrent, only I/O

IfLegacy synchronous code that cannot be rewritten to async

→

UseUse loop.run_in_executor(ThreadPoolExecutor, sync_function) — offloads the blocking call to a thread and returns an awaitable

IfMixed I/O and CPU work in the same request path

→

UseUse asyncio for orchestration and all I/O; use run_in_executor with ProcessPoolExecutor for the CPU-intensive segments specifically

## What Is Asyncio — And What It Absolutely Isn't

Asyncio is a concurrency framework for I/O-bound work running in a single thread. It's not parallelism. It won't make your CPU-bound loops faster. What it does is let you juggle a thousand open network connections without breaking a sweat.

The event loop sits in the middle. It polls file descriptors, schedules coroutines when data arrives, and yields control back to waiting tasks. No threads, no GIL contention — just cooperative multitasking with explicit yield points.

When you call `asyncio.run(`main()`)`, that creates a new event loop, runs ``main()`` as a coroutine, and blocks until done. Inside that loop, every `await` is a handshake: "I'm waiting on something — go run someone else's code while I do." If you forget to await, you get a coroutine object, not execution. If you block the loop with a ``time.sleep()`` instead of ``asyncio.sleep()``, you freeze the entire show for every other task.

The hard truth: asyncio is powerful, but it demands discipline. One synchronous call to ``requests.get()`` inside a coroutine and your async web server is now serving one request at a time.

BlockingMistake.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19
    
    
    // io.thecodeforge — python tutorial
    
    import asyncio
    import time
    
    async def fetch_data(url: str) -> str:
        print(f"Fetching {url}")
        # TRAP: This blocks the entire event loop
        time.sleep(2)  # should be asyncio.sleep(2)
        return f"Data from {url}"
    
    async def main():
        urls = ["https://api.service1.com", "https://api.service2.com"]
        tasks = [asyncio.create_task(fetch_data(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(r)
    
    asyncio.run(main())

Output

Fetching https://api.service1.com

Fetching https://api.service2.com

# After 4 seconds total (sequential), not 2 seconds (concurrent)

⚠ Production Trap:

Never use ``time.sleep()``, ``requests.get()``, or any blocking library inside a coroutine. They starve the event loop and make your async code run like synchronous garbage. If you must use blocking code, shove it into a thread with ``asyncio.to_thread()``.

🎯 Key Takeaway

Asyncio is cooperative concurrency in one thread. Blocking the event loop kills concurrency. Await or delegate — there is no third option.

## Asyncio vs Threading: When to Use a Sledgehammer vs a Scalpel

Threading gives you preemptive multitasking. The OS decides when to swap threads. Asyncio gives you cooperative multitasking. You decide when to yield. The difference isn't academic — it dictates what kind of work you can do.

Threading works for I/O and CPU-bound work, but it's expensive. Each thread carries a 1–8 MB stack, and context switching costs real CPU cycles. Worse, Python's GIL means threads don't parallelise CPU work anyway. For 10k concurrent connections, threads will eat your memory. For 10k connections, asyncio eats maybe 10 MB total.

Asyncio shines when you're waiting on something external: a database query, an HTTP response, a file read. While you wait, other coroutines run on the same thread. Zero context switch overhead. No GIL contention. But if you need to parse a 200 MB JSON blob or run a Monte Carlo simulation, asyncio won't help — you still block the loop. That's when you reach for multiprocessing or push work to a task queue.

Rule of thumb: I/O-bound and many concurrent tasks → asyncio. CPU-bound or complex locking → threads or processes. Mixing both? Carefully. You can offload CPU work to a thread pool with ``loop.run_in_executor()``, but you've just added complexity. Choose the right tool from the start.

ThreadVsAsync.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36
    
    
    // io.thecodeforge — python tutorial
    
    import asyncio
    import time
    import threading
    
    # Simulate a 2-second I/O wait (e.g., network request)
    async def fetch_async(url: str) -> str:
        await asyncio.sleep(2)  # non-blocking
        return f"Async data from {url}"
    
    def fetch_threaded(url: str) -> str:
        time.sleep(2)  # blocking
        return f"Thread data from {url}"
    
    async def run_async():
        start = time.perf_counter()
        tasks = [fetch_async(f"site-{i}.com") for i in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start
        print(f"Async: {len(results)} requests in {elapsed:.2f}s")
    
    def run_threaded():
        start = time.perf_counter()
        threads = []
        for i in range(100):
            t = threading.Thread(target=fetch_threaded, args=(f"site-{i}.com",))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        elapsed = time.perf_counter() - start
        print(f"Threaded: 100 requests in {elapsed:.2f}s")
    
    asyncio.run(run_async())
    run_threaded()

Output

Async: 100 requests in 2.01s

Threaded: 100 requests in 2.03s

# Both finish in ~2 seconds, but asyncio uses 1 thread, threaded uses 100

If you need to run a blocking database driver like psycopg2 in an async app, wrap each call in ``asyncio.to_thread()``. It offloads the blocking work to a thread pool without you writing thread management code. But better yet, use an async driver like asyncpg.

🎯 Key Takeaway

Asyncio is for high-concurrency I/O. Threads are for CPU-bound or blocking work you can't avoid. Memory is finite — choose asyncio when you need thousands of concurrent operations.

## Asyncio Best Practices That Save Your Prod Deploy

Most asyncio code breaks in production because devs treat it like threads with async/await syntax. Stop that. Rule one: never mix `asyncio.run()` inside a running event loop — you'll get 'RuntimeError: This event loop is already running' and your service crashes at 3 AM. Use `asyncio.create_task()` instead of low-level `loop.create_task()` when you're inside a coroutine; the high-level API properly handles cleanup on cancellation.

Second: always wrap your main entry point in asyncio.run(`main()`). That function creates a fresh event loop, runs your coroutine, and cleans up all pending tasks. Never call `loop.close()` yourself unless you're writing framework internals. Third: for timeouts, use `asyncio.timeout()` (Python 3.11+) or `asyncio.wait_for()` — never implement your own sleep-polling loop. That's how you get 47-second freezes. Fourth: debug mode is your friend. Set PYTHONASYNCIODEBUG=1 or pass debug=True to `asyncio.run()`. It catches forgotten awaits and slow callbacks.

Fifth: if you're doing CPU-bound work inside a coroutine, you've already lost. Offload to `run_in_executor()` with a ThreadPoolExecutor. The event loop isn't magic — it's an I/O scheduler.

asyncio_best_practices.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24
    
    
    // io.thecodeforge — python tutorial
    
    import asyncio
    import time
    
    async def fetch_data(delay: float) -> str:
        await asyncio.sleep(delay)
        return f"data after {delay}s"
    
    async def main():
        # Use create_task for concurrent execution
        task1 = asyncio.create_task(fetch_data(0.5))
        task2 = asyncio.create_task(fetch_data(1.0))
    
        # Always use asyncio.timeout for timeouts
        try:
            async with asyncio.timeout(2.0):
                results = await asyncio.gather(task1, task2)
                print(results)
        except asyncio.TimeoutError:
            print("Timed out — check your external API")
    
    if __name__ == "__main__":
        asyncio.run(main())

Output

['data after 0.5s', 'data after 1.0s']

⚠ Production Trap:

asyncio.run() creates a new event loop every call. Never call it inside a running loop — use a single entry point at process start.

🎯 Key Takeaway

asyncio.run() once at the top, `create_task()` inside, timeouts on every I/O call.

## Real-World Asyncio: Where It Pays and Where It Chokes

Asyncio shines when you're waiting on I/O — network calls, file reads, database queries, API requests. Think web scrapers hitting a hundred endpoints, or a chat server handling ten thousand connections. Each coroutine yields the CPU while waiting, so one thread handles all of them. That's the sweet spot: high-concurrency I/O where latency dominates, not CPU cycles.

Where does asyncio choke? CPU-bound work. Parsing a 10GB JSON file, image processing, or running ML inference inside a coroutine blocks the event loop. Your 10k connections freeze. Threading or multiprocessing is the right tool there. Also: complex synchronous libraries like some database drivers (looking at you, older MySQL connectors) silently block the loop. Wrap them in `run_in_executor()` or choose an async-native driver.

Real production pattern: [FastAPI](/python/fastapi-basics/) or aiohttp for the web layer, async Redis and asyncpg for data, and a separate multiprocessing pool for heavy lifting. The event loop handles thousands of concurrent I/O tasks; the process pool handles the CPU-bound grunt work. Mix them properly, and you scale to thousands of requests per second on a single box.

real_world_asyncio.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36
    
    
    // io.thecodeforge — python tutorial
    
    import asyncio
    import concurrent.futures
    import json
    
    def parse_large_json(filepath: str) -> dict:
        # CPU-bound — runs in executor
        with open(filepath) as f:
            return json.load(f)
    
    async def fetch_user(api_url: str) -> dict:
        # I/O-bound — native async
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                return await resp.json()
    
    async def main():
        loop = asyncio.get_running_loop()
    
        # Offload CPU work to thread pool
        with concurrent.futures.ThreadPoolExecutor() as pool:
            config_data = await loop.run_in_executor(
                pool, parse_large_json, "config.json"
            )
    
        # I/O work stays in event loop
        users = await asyncio.gather(
            fetch_user("https://api.example.com/user/1"),
            fetch_user("https://api.example.com/user/2"),
        )
        print(f"Config keys: {list(config_data.keys())}")
        print(f"Users: {len(users)}")
    
    asyncio.run(main())

Output

Config keys: ['database', 'port', 'logging']

Users: 2

Use asyncio for I/O concurrency. Use multiprocessing for CPU. Use threading only when forced by legacy libs.

🎯 Key Takeaway

Asyncio is an I/O multiplexer, not a parallel compute engine — pair it with executor pools for CPU work.

## The Inner Workings of Coroutines

Coroutines are not just async functions. Behind the scenes, Python transforms every `async def` into a generator-like object with `__await__` and ``send()`` methods. When you `await` something, the coroutine suspends itself—saving its local state and instruction pointer—then yields control back to the event loop. The event loop holds a reference to that coroutine, waiting for a signal (like a socket becoming readable) to call `send(None)` on it, which resumes execution exactly where it paused. This is fundamentally cooperative: no preemption, no OS thread stack. Every `await` point is a voluntary yield. Understanding this explains why blocking in a coroutine is catastrophic—you aren't giving the loop a chance to call ``send()`` on other waiting coroutines. The loop can only resume one coroutine at a time, in a single thread, but it juggles thousands by never blocking at a resume point. This mechanism is why asyncio achieves concurrency without parallelism: each coroutine is a tiny state machine driven by the loop.

CoroutineInternals.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17
    
    
    // io.thecodeforge — python tutorial
    
    async def demo():
        print("started")
        await asyncio.sleep(1)  # yield to loop
        print("resumed")
    
    # What happens internally:
    # 1. demo() returns a coroutine object
    # 2. loop creates a Task, wrapping it
    # 3. Task.__step() calls coro.send(None)
    # 4. coro runs until 'await', then raises StopIteration
    #    with a 'yield' inside __await__
    # 5. Task captures the yield, registers callback
    # 6. After 1s, callback calls coro.send(None) -> resumes
    print("Coroutine 'demo' is a state machine")
    # Output: started (delayed) resumed

Output

Coroutine 'demo' is a state machine

⚠ Production Trap:

Never store a bare coroutine object. If you don't await it or pass it to a task, the coroutine is garbage collected with a warning. That's a silent leak of your intended work.

🎯 Key Takeaway

Every coroutine is a single-threaded state machine that yields at every await

## A Homemade asyncio.sleep

Built-in `asyncio.sleep(n)` seems like magic, but you can build one from scratch to internalize how the event loop schedules work. The key is a future: an object that signals readiness. When you create a future and call `loop.call_later(seconds, future.set_result, None)`, you schedule a callback to mark the future as done after the delay. Then `await future` suspends the coroutine until that callback fires. Your homemade sleep must return an awaitable that does exactly two things: (1) schedule a callback on the loop with your delay, (2) yield control by awaiting a future that the callback resolves. That's it. No busy waiting, no threads. The event loop holds the timer in its internal heap; when the timer expires, it runs the callback, which marks the future done, which resumes your coroutine. This reveals that asyncio.sleep is a thin wrapper around `loop.call_later` \+ `future`. Understanding this lets you create custom timed waits, cancellable delays, or polling loops that don't block.

HomemadeSleep.pyPYTHON

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17
    
    
    // io.thecodeforge — python tutorial
    
    import asyncio
    
    async def my_sleep(delay):
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        loop.call_later(delay, future.set_result, None)
        await future  # suspend here until callback
    
    async def main():
        print("0")
        await my_sleep(1)
        print("1")
    
    asyncio.run(main())
    # Output: 0  (pause ~1s)  1

Output

0 (pause ~1s) 1

⚠ Production Trap:

Resetting a future with `set_result` more than once raises `InvalidStateError`. Your homemade sleep must create a fresh future each call—never reuse.

🎯 Key Takeaway

asyncio.sleep is just call_later + a future; build it yourself to grasp the event loop's scheduling

● Production incidentPOST-MORTEMseverity: high

### The 47-Second Freeze: How a Single requests.get() Call Locked an Entire Async Service

Symptom

All endpoints on the async API gateway stopped responding simultaneously. CPU utilisation dropped to near zero — the process appeared alive from the outside, consuming memory and holding its port, but completely unable to process any request. No error logs were emitted during the outage. The load balancer health checks began failing after their grace period, triggering cascading failover across three availability zones, which amplified the incident as the remaining healthy gateways absorbed redistributed traffic they were not sized to handle.

Assumption

The team initially suspected database connection pool exhaustion or a DNS resolution hang on the upstream service. Two engineers spent approximately 20 minutes inspecting connection strings, checking network ACLs, and reviewing recent database migrations. None of it was relevant. The database was healthy throughout.

Root cause

A developer had added requests.get('http://internal-service/health') — using the synchronous requests library — inside an async endpoint handler as part of a new observability feature. The upstream service was experiencing degraded performance and was slow to respond, eventually hitting a 47-second TCP timeout before closing the connection. Because `requests.get()` is a blocking call, it held the event loop thread for the full 47 seconds. During that time, the event loop could not schedule any other coroutine. No new requests could be accepted. All in-flight awaitable operations stalled. The process was alive but effectively brain-dead. The real danger here was the silence: no exception was raised, no warning was logged, and the call eventually succeeded from the application's perspective — it just took 47 seconds and took the entire service down with it.

Fix

Replaced `requests.get()` with httpx.`AsyncClient.get()` using await. Added an `asyncio.wait_for()` wrapper with a 3-second timeout to enforce an SLA on the health check. Instrumented event loop latency as a separate Prometheus metric so that blocking calls above 50ms would trigger an alert before manifesting as a user-visible outage. Implemented a flake8-async linter rule in the CI pipeline that flags synchronous blocking calls inside async function definitions — humans forget under deadline pressure, CI does not.

Key lesson

  * Never call synchronous blocking functions inside the event loop thread — one blocked call freezes every coroutine running in that process, not just the one making the call
  * Use async-native libraries for all network I/O in async code paths: httpx instead of requests, motor instead of pymongo, aiofiles instead of the built-in `open()`
  * Enforce linting rules that detect sync blocking calls in async contexts at CI time — code review catches many things but not this class of subtle correctness issue reliably
  * Monitor event loop latency as a first-class metric separate from request latency — a healthy request count combined with near-zero CPU is the operational signature of a blocked event loop, and it needs its own alert



Production debug guideSymptom-driven diagnostics for async Python services in production5 entries

Symptom · 01

Event loop appears frozen — requests queue up but nothing processes, CPU near zero

→

Fix

Check for synchronous blocking calls inside async handlers. Set loop.slow_callback_duration = 0.05 to log callbacks exceeding 50ms. Run loop.set_debug(True) in staging to surface unawaited coroutines and slow callbacks. Use strace on the process to see what system call it is stuck in — a blocking read or connect will be obvious.

Symptom · 02

gather() raises an exception and you suspect remaining tasks were abandoned

→

Fix

Add return_exceptions=True to the `gather()` call and re-run. Inspect the full results list for Exception instances rather than letting the first failure short-circuit. Count `asyncio.all_tasks()` before and after to verify no orphaned tasks remain running after the gather resolves.

Symptom · 03

Memory usage grows steadily over hours and never drops between traffic bursts

→

Fix

Look for uncollected task references. Run `gc.collect()` followed by len(`asyncio.all_tasks()`) to count live tasks. A task count that grows monotonically under load points to fire-and-forget coroutines that were never awaited and have no strong reference holding them accountable — they are running but nobody is collecting their results.

Symptom · 04

TimeoutError raised unexpectedly on operations that should be well within the timeout

→

Fix

Verify the `asyncio.wait_for()` timeout is sufficient for current load conditions. Check if the event loop itself is under contention — timeouts fire relative to event loop scheduling time, not wall clock time. If the loop is busy for 200ms between iterations, a 100ms timeout will fire even if the target operation only needed 50ms of actual work.

Symptom · 05

Connection pool exhausted under moderate load with connections appearing leaked

→

Fix

Verify async connection pool size matches expected concurrency. Check for missing async context manager exits — an unhandled exception inside an async with block that does not propagate cleanly can leave connections checked out permanently. Use the pool's own introspection methods to inspect checked-out versus available counts, and add logging to the pool's release callbacks.

★ asyncio Quick Debug Cheat SheetRapid diagnostics for common asyncio production issues. These are the commands I reach for first when an async service starts behaving unexpectedly.

Event loop blocked — all requests stalling, CPU near zero−

Immediate action

Set slow callback duration to detect and log blocking calls above the threshold

Commands

`python -c "import asyncio; loop=asyncio.get_event_loop(); loop.slow_callback_duration=0.05; print('Monitoring enabled at 50ms threshold')"`

`strace -p $(pgrep -f your_app) -e trace=network,read,write -c`

Fix now

Replace all synchronous I/O calls with async equivalents (httpx, aiofiles, motor). Wrap unavoidable sync code in loop.run_in_executor(None, sync_function) to offload it to a thread pool and free the event loop.

Tasks accumulating — memory growing steadily under load+

Immediate action

Count live tasks and identify unawaited coroutines that were fire-and-forget

Commands

`python -c "import asyncio; print(f'Live tasks: {len(asyncio.all_tasks())}')"`

`python -c "import gc; gc.collect(); print(f'Uncollected garbage objects: {len(gc.garbage)}')"`

Fix now

Ensure every coroutine is either awaited directly or wrapped in `asyncio.create_task()` with the task reference stored in a set or list. Add a done callback to clean up the reference when the task completes: task.add_done_callback(active_tasks.discard).

gather() failing silently — partial results lost with no visible error+

Immediate action

Identify all gather() calls missing return_exceptions=True in the codebase

Commands

`grep -rn 'asyncio.gather(' src/ --include='*.py' | grep -v return_exceptions`

`python -c "import asyncio; help(asyncio.gather)"`

Fix now

Add return_exceptions=True to every `gather()` call in production paths. Iterate the results list and check isinstance(result, Exception) for each entry. Log and handle exceptions individually rather than letting one bad result corrupt the entire batch.

High tail latency (p99) despite low average latency — intermittent spikes under load+

Immediate action

Profile the running process to find slow callbacks causing event loop scheduling delays

Commands

`python -c "import asyncio; loop=asyncio.get_event_loop(); loop.set_debug(True); loop.slow_callback_duration=0.05"`

`py-spy record --pid $(pgrep -f your_app) --output profile.svg --duration 30`

Fix now

Identify slow callbacks from the debug logs. Offload any CPU-heavy operations to a ThreadPoolExecutor or ProcessPoolExecutor via `loop.run_in_executor()`. P99 spikes with healthy p50 is the canonical signature of periodic event loop blocking.

asyncio vs Threading vs Multiprocessing

Dimension| asyncio| threading| multiprocessing  
---|---|---|---  
Concurrency model| Cooperative — coroutines yield voluntarily at await points, single OS thread| Preemptive — OS scheduler switches between threads at arbitrary points| Parallel — separate OS processes, each with its own Python interpreter and GIL  
Best for| High-concurrency I/O: thousands of simultaneous network calls, database queries, WebSocket connections| Legacy synchronous libraries, blocking I/O that cannot be rewritten, integrating with callback-based frameworks| CPU-bound computation: image processing, ML inference, encryption, data transformation that saturates a single core  
Memory overhead| Very low — coroutines are lightweight objects, roughly a few KB each| Moderate — each OS thread has a stack, typically 1-8 MB depending on OS and configuration| High — each process has a separate heap, a copy of imported modules, and its own interpreter state  
GIL interaction| Single thread — the GIL is entirely irrelevant, there is no contention| GIL limits true parallelism — only one thread executes Python bytecode at a time, I/O releases the GIL| Each process has its own GIL — true CPU parallelism across cores, but IPC overhead for data exchange  
Context switch cost| Zero OS overhead — context switches are Python-level coroutine frame swaps at await points| OS kernel context switch — roughly 1-10 microseconds per switch, adds up under high thread counts| OS process switch — roughly 10-100 microseconds plus IPC serialisation overhead for any data passed between processes  
Cancellation support| Cooperative via CancelledError delivered at await points — cleanup code in try/finally runs reliably| No safe cancellation mechanism — you can set daemon=True to kill on process exit but cannot interrupt mid-execution| Terminate the process (abrupt) or send a signal — no cooperative cancellation, cleanup code may not run  
Debugging complexity| Moderate — stack traces span await boundaries, async context is lost across yields, debug mode helps significantly| High — race conditions, deadlocks, and data races are non-deterministic and difficult to reproduce reliably| High — IPC issues, serialisation failures, shared memory races, and zombie processes add significant diagnostic complexity  
Scaling limit| Tens of thousands of concurrent coroutines on a single process with appropriate I/O multiplexing| Hundreds of threads before stack memory and context switch overhead degrades performance noticeably| Limited by the number of physical CPU cores and available memory — inter-process communication becomes the bottleneck  
  
⚙ Quick Reference

10 commands from this guide

File| Command / Code| Purpose  
---|---|---  
io_thecodeforgebasics.py| async def fetch_service_status(service_name: str, delay: float) -> str:| Coroutines and the Event Loop  
io_thecodeforgeconcurrency.py| async def fetch_service_status(service_name: str, delay: float) -> str:| asyncio.gather()  
io_thecodeforgeresilience.py| from typing import Any| Fault Tolerance  
io_thecodeforgethreading_interop.py| from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor| The Golden Rule  
BlockingMistake.py| async def fetch_data(url: str) -> str:| What Is Asyncio  
ThreadVsAsync.py| async def fetch_async(url: str) -> str:| Asyncio vs Threading  
asyncio_best_practices.py| async def fetch_data(delay: float) -> str:| Asyncio Best Practices That Save Your Prod Deploy  
real_world_asyncio.py| def parse_large_json(filepath: str) -> dict:| Real-World Asyncio  
CoroutineInternals.py| async def demo():| The Inner Workings of Coroutines  
HomemadeSleep.py| async def my_sleep(delay):| A Homemade asyncio.sleep  
  
## Key takeaways

1

asyncio is single-threaded concurrency

it excels at I/O-bound tasks with thousands of concurrent operations but provides zero CPU parallelism. For CPU-bound work, the correct tool is multiprocessing.

2

Coroutines are non-blocking

they yield control back to the event loop at every await point. A coroutine object not yet awaited or scheduled executes zero lines of code and produces no side effects.

3

Concurrency versus parallelism

asyncio is concurrent — many things progressing at once on one thread. Multiprocessing is parallel — many things running simultaneously on separate cores. These are different properties solving different bottlenecks.

4

gather(return_exceptions=True) is the production standard for batch operations against flaky dependencies

every task completes, every exception is inspectable, no orphaned tasks leak resources.

5

Prefer async-native libraries in all async code paths

httpx over requests, motor over pymongo, aioredis over redis-py, aiofiles over `open()`. A single synchronous library call can freeze the entire service.

6

One blocking call in the event loop thread freezes every coroutine in the process

instrument event loop latency as a separate metric from request latency, because average latency can look healthy while the loop is periodically freezing.

7

Store a reference to every Task created with `create_task()`

unreferenced tasks can be garbage collected before they complete with no error or warning in non-debug mode.

8

For Python 3.11+, prefer asyncio.TaskGroup over `gather()` for structured concurrency

automatic sibling cancellation on failure and ExceptionGroup handling make it safer by default.

### Common mistakes to avoid

6 patterns

×

#### Calling a coroutine without awaiting it

Symptom

The coroutine function is called and returns immediately with no output, no side effect, and no error raised. The coroutine object is created and garbage collected silently. In Python 3.11+ debug mode, a RuntimeWarning is emitted saying 'coroutine was never awaited' — but only if the garbage collector runs before the program exits, which is not guaranteed under load.

Fix

Always await coroutine calls: result = await `my_coroutine()`. For fire-and-forget patterns where you want to start work without waiting for it, use asyncio.create_task(`my_coroutine()`) and store the returned Task in a set or list. Add a done callback to remove it from the set on completion: task.add_done_callback(active_tasks.discard). Without storing the reference, the Task itself may be garbage collected before it completes.

×

#### Using synchronous libraries inside async handlers

Symptom

Event loop freezes for the full duration of every synchronous call. Under load, p99 latency spikes to the duration of the blocking call while average latency stays deceptively low — because most requests complete fine, only the ones unlucky enough to run while a blocking call is in progress are affected. All concurrent connections stall simultaneously during the freeze, causing correlated timeouts across unrelated requests.

Fix

Replace synchronous libraries with async equivalents: requests becomes httpx, pymongo becomes motor, redis-py becomes aioredis, `open()` becomes aiofiles. For synchronous code that cannot be replaced, wrap it in loop.run_in_executor(None, sync_function) — this offloads the call to Python's default thread pool and returns an awaitable that the event loop can wait on without blocking itself.

×

#### Using gather() without return_exceptions=True in production

Symptom

A single failing coroutine raises an exception that propagates immediately to the caller. The remaining coroutines continue running as orphaned tasks with no owner — they consume database connections, HTTP connections, and memory until they complete or timeout on their own. Under sustained load with any upstream failure rate, orphaned tasks accumulate and connection pools are silently exhausted.

Fix

Always pass return_exceptions=True to `asyncio.gather()` in production paths. Iterate the results list and handle exceptions individually: for i, result in enumerate(results): if isinstance(result, Exception): log_and_handle(i, result). This gives you full visibility into which tasks failed and which succeeded, with no orphaned tasks and no abandoned resources.

×

#### Creating tasks without storing references to them

Symptom

Tasks disappear mid-execution — they are garbage collected because no strong reference exists to keep them alive. The coroutine never completes, writes nothing to the database, sends nothing to the network, and raises no error. This manifests as intermittent missing records or skipped processing steps that are extremely difficult to reproduce because they depend on GC timing.

Fix

Store every Task reference in a set or list for its full lifetime: background_tasks = `set()`; task = asyncio.create_task(`coro()`); background_tasks.add(task); task.add_done_callback(background_tasks.discard). For Python 3.11+, asyncio.TaskGroup provides structured lifecycle management that eliminates this class of bug entirely.

×

#### Using time.sleep() instead of asyncio.sleep() in async code

Symptom

The entire event loop blocks for the sleep duration. Every coroutine in the process freezes. A time.sleep(5) inside a handler makes the entire service unresponsive for 5 full seconds. Load balancer health checks fail, triggering cascading restarts that amplify the incident by resetting all in-flight connections.

Fix

Always use await asyncio.sleep(seconds) in async code. Search the codebase for time.sleep and replace every instance in an async context. If a third-party library internally calls `time.sleep()` and cannot be replaced, wrap the entire call in loop.run_in_executor(None, library_function) to move it to a thread pool where it can block safely without holding the event loop.

×

#### Ignoring CancelledError in cleanup logic after a timeout

Symptom

When a task is cancelled by `wait_for()` timeout, cleanup code that follows the cancelled await statement never executes. Database connections are not closed, file handles are left open, distributed locks are not released, and temporary resources leak. Over hours of production traffic, connection pools are gradually exhausted without a clear explanation in the logs.

Fix

Use try/finally to ensure cleanup always runs regardless of how the coroutine exits: try: result = await `work()`; finally: await `cleanup()`. If the cleanup itself must complete even if the outer scope is cancelled, wrap it in `asyncio.shield()`: try: result = await `work()`; finally: await asyncio.shield(`critical_cleanup()`). The shield prevents the cleanup coroutine from being cancelled along with its parent.

INTERVIEW PREP · PRACTICE MODE

## Interview Questions on This Topic

Q01SENIOR

Explain the starvation problem in an event loop. How does a single block...

Q02SENIOR

What is the difference between await task and asyncio.gather(task)? When...

Q03SENIOR

How would you implement a rate limiter that allows only 5 concurrent cor...

Q04SENIOR

How does the Python GIL interact with asyncio? Does asyncio allow Python...

Q05SENIOR

What is the asyncio.shield() pattern and when would you use it to protec...

Q01 of 05SENIOR

Explain the starvation problem in an event loop. How does a single blocking call affect other unrelated coroutines?

ANSWER

asyncio runs on a single OS thread. The event loop can execute exactly one coroutine at a time — when a coroutine is running Python bytecode, no other coroutine can run. The cooperative nature of the model means every coroutine is expected to yield control at await points so the loop can schedule others. When a coroutine makes a blocking call — a synchronous HTTP request, `time.sleep()`, a CPU-intensive computation, or any call that does not release the thread — it holds the OS thread for the entire duration of that call. The event loop cannot interrupt it. No other coroutine can be scheduled. No new I/O events can be processed. The entire process is effectively frozen. This is starvation: coroutines that are ready to run, that have I/O results waiting for them, sit in the loop's ready queue with no CPU time. They are not waiting on anything external — they are waiting for one coroutine to stop monopolising the thread. The solutions are: replace blocking calls with async equivalents for I/O-bound work; use `loop.run_in_executor()` with a thread pool for unavoidable synchronous code; use ProcessPoolExecutor for CPU-bound work that needs real parallelism. Detecting it in production requires instrumenting event loop latency separately from request latency — a blocked loop shows up as scheduling delay even when the underlying operations would be fast.

Q02 of 05SENIOR

What is the difference between await task and asyncio.gather(task)? When would you use one over the other?

ANSWER

await task suspends the current coroutine until that single task completes and returns its result directly — a bare value, not a list. asyncio.gather(task) wraps the result in a single-element list. For one task, they are functionally equivalent with a minor structural difference. The distinction becomes significant when you have multiple tasks. await task_a followed by await task_b is sequential: task_b does not start until task_a completes. Total time is the sum of both. asyncio.gather(task_a, task_b) schedules both onto the event loop simultaneously when the gather call is made and awaited. Total time is the maximum of both, not the sum. For two 1-second tasks, await-sequentially costs 2 seconds and gather costs 1 second. `gather()` also provides an ordering guarantee: results are returned in the same order as the input arguments regardless of which task finished first. This is safe to rely on and unpack positionally. Use await for single operations or operations that must complete in strict sequence because later operations depend on earlier results. Use `gather()` for independent operations where the results can be processed together after all complete — health checks, fanout requests to microservices, parallel data fetches from independent sources.

Q03 of 05SENIOR

How would you implement a rate limiter that allows only 5 concurrent coroutines to run at a time using asyncio.Semaphore?

ANSWER

asyncio.Semaphore(n) is a counter that allows at most n coroutines to be inside the guarded section simultaneously. When the counter reaches zero, any coroutine attempting to acquire it suspends until another coroutine releases it. The implementation uses async with semaphore: as a context manager, which acquires on entry and releases on exit — even if the coroutine raises an exception or is cancelled, the semaphore is released reliably. Example: sem = asyncio.Semaphore(5). Then in each task: async with sem: result = await `make_api_call()`. You can wrap this in a helper function and pass it to `gather()` with as many tasks as needed — `gather()` will start all of them, but at most 5 will be inside the async with block simultaneously. The rest will be suspended waiting to acquire the semaphore. This pattern is useful for respecting downstream rate limits, preventing thundering herd on shared resources, and controlling memory usage when each concurrent operation holds significant state. One common mistake is creating the semaphore inside the task function — it must be created once and shared across all tasks to have any effect.

Q04 of 05SENIOR

How does the Python GIL interact with asyncio? Does asyncio allow Python to bypass the GIL?

ANSWER

asyncio does not bypass the GIL. It operates within a single OS thread, so there is no GIL contention at all — the GIL is simply irrelevant. The GIL prevents multiple threads from executing Python bytecode simultaneously. asyncio avoids this problem entirely by never using multiple threads for coroutine execution. asyncio achieves concurrency — overlapping I/O wait times — not parallelism. While one coroutine is suspended waiting for a network response, the event loop runs another coroutine. This overlap is real and provides significant throughput gains for I/O-bound workloads. But both coroutines share the same thread and the same GIL, so they never literally execute Python bytecode at the same instant. For true CPU parallelism — running computation on multiple cores simultaneously — asyncio is the wrong tool. The GIL prevents multiple threads from doing this, and asyncio uses only one thread. The correct tool is multiprocessing, which spawns separate OS processes each with their own Python interpreter and their own GIL. Data flows between processes via IPC, which adds serialisation overhead but provides genuine parallel CPU execution. The practical rule: asyncio for I/O-bound concurrency, multiprocessing for CPU-bound parallelism, and ProcessPoolExecutor via `run_in_executor()` when you need both in the same application.

Q05 of 05SENIOR

What is the asyncio.shield() pattern and when would you use it to protect a coroutine from cancellation?

ANSWER

asyncio.shield(coro) wraps a coroutine in a protective layer. When the outer task is cancelled — for example, because a `wait_for()` timeout fired — the inner shielded coroutine continues running to completion rather than being cancelled along with its parent. The use case is critical cleanup or commit operations that must not be interrupted by timeout cancellation. Examples: writing an audit log entry after a request is processed, committing a database transaction that was started before the timeout fired, releasing a distributed lock, or flushing metrics. Without shield: task = asyncio.create_task(`critical_write()`); await asyncio.wait_for(task, 1.0) — if the timeout fires, `critical_write()` is cancelled and may leave partial state. With shield: await asyncio.wait_for(asyncio.shield(`critical_write()`), 1.0) — if the timeout fires, the outer wait raises TimeoutError, but `critical_write()` continues running in the background. The important caveat: shield does not guarantee the result is consumed. The outer coroutine received TimeoutError and stopped waiting. The inner task is still running with no awaiter. Store the inner task reference before shielding and await it in a finally block to handle this correctly. shield is not a simple drop-in — it changes the ownership model of the task and requires careful handling of the orphaned inner task.

01

Explain the starvation problem in an event loop. How does a single blocking call affect other unrelated coroutines?

SENIOR

02

What is the difference between await task and asyncio.gather(task)? When would you use one over the other?

SENIOR

03

How would you implement a rate limiter that allows only 5 concurrent coroutines to run at a time using asyncio.Semaphore?

SENIOR

04

How does the Python GIL interact with asyncio? Does asyncio allow Python to bypass the GIL?

SENIOR

05

What is the asyncio.shield() pattern and when would you use it to protect a coroutine from cancellation?

SENIOR

FAQ · 5 QUESTIONS

## Frequently Asked Questions

01

What is the difference between asyncio and threading in Python?

Threading relies on the OS to schedule and switch between threads. Because of Python's GIL, only one thread executes Python bytecode at a time regardless of how many threads exist — so threading does not provide CPU parallelism for Python code, though it does release the GIL during I/O operations and C extension calls.

asyncio uses a single OS thread with cooperative multitasking. Context switches happen only when a coroutine explicitly yields with await, which means zero OS overhead per switch. The memory footprint is dramatically lower — a coroutine is a few kilobytes; an OS thread stack is typically one to eight megabytes. For high-concurrency I/O workloads, asyncio scales to tens of thousands of concurrent operations where threading would exhaust memory and OS thread limits at a few hundred.

Use asyncio for new high-concurrency I/O code. Use threading when integrating with legacy synchronous libraries via `run_in_executor()` or when a specific library explicitly requires a dedicated thread.

Was this helpful? 

02

When should I use asyncio.create_task() instead of gather()?

Use `asyncio.create_task()` when you want to start a background operation now and collect its result at a later point in the same code path, or when you want fire-and-forget behaviour where you do not need the result at all. The task starts immediately when `create_task()` is called and runs concurrently with whatever the current coroutine does next.

Use `asyncio.gather()` when you have a known list of independent operations and you need all of their results before you can proceed. `gather()` is the right tool for fanout patterns: fetch from all these sources, wait for all results, then process them together.

The practical distinction: create_task() gives you fine-grained control over individual task lifetimes. `gather()` is a convenient all-or-nothing collection mechanism. For structured concurrency in Python 3.11+, TaskGroup combines the control of `create_task()` with the wait-for-all semantics of `gather()` and adds automatic sibling cancellation on failure.

Was this helpful? 

03

Can I use asyncio for CPU-intensive tasks like image processing or ML inference?

No, not directly. asyncio is single-threaded — a CPU-intensive operation running inside the event loop will block the loop for its entire duration, freezing all other coroutines. CPU work does not release the event loop the way I/O does.

For CPU-bound work, use multiprocessing to bypass the GIL and utilise multiple cores. If you need to integrate CPU-bound work into an async application, use loop.run_in_executor(ProcessPoolExecutor, cpu_function, data) — this offloads the CPU work to a separate process and returns an awaitable so the event loop remains free.

The overhead of IPC serialisation makes ProcessPoolExecutor most appropriate for coarse-grained work — process this entire batch — rather than fine-grained per-request work where the IPC cost exceeds the computation time.

Was this helpful? 

04

How do I test async code with pytest?

Use the pytest-asyncio plugin. Install it with pip install pytest-asyncio, then mark test functions with @pytest.mark.asyncio and define them as async def. The plugin manages the event loop lifecycle for each test.

For async fixtures, use @pytest_asyncio.fixture with async def and await inside them normally. Configure the plugin mode in pytest.ini or pyproject.toml: asyncio_mode = auto applies the asyncio mark automatically to all async test functions, removing boilerplate.

For testing timeout and cancellation behaviour specifically, `asyncio.wait_for()` in combination with `asyncio.sleep()` inside test fixtures allows you to simulate slow dependencies. Mock async functions with AsyncMock from unittest.mock rather than MagicMock — AsyncMock returns an awaitable, MagicMock does not and will cause errors when the code under test awaits it.

Was this helpful? 

05

What happens to pending tasks when the event loop closes?

When `asyncio.run()` returns, it cancels all tasks that are still pending and runs the loop briefly to allow them to handle CancelledError. Tasks that have try/finally or async context manager cleanup will execute their cleanup code. Tasks that do not handle CancelledError will have any code after their current await point skipped.

For graceful shutdown where you need all tasks to complete cleanly, implement explicit shutdown logic before returning from `main()`: collect all tasks with `asyncio.all_tasks()`, cancel each one, and then await asyncio.gather(*pending_tasks, return_exceptions=True) to let each task run its cleanup. After this, the loop closes with no orphaned tasks.

For long-running services, wire SIGTERM handling to this shutdown sequence so that Kubernetes pod termination or systemd stop triggers a clean drain rather than an abrupt kill.

Was this helpful? 

N

Naren Founder & Principal Engineer

20+ years shipping production Python across data and backend systems. Notes here come from systems that actually shipped. 

[ Follow ](https://www.linkedin.com/in/thecodeforge-io-a0676b3b5/)

✓ Verified 

production tested

September 26, 2026

last updated

2,085

articles · all by Naren

🔥

###  That's Advanced Python. Mark it forged? 

10 min read · try the examples if you haven't 

[←PreviousPython Performance Optimisation](/python/python-performance-optimisation/)

15 / 17 · Advanced Python 

[NextPython Weak References→](/python/python-weak-references/)
