---
source: "https://codemia.io/knowledge-hub/path/how_do_i_profile_memory_usage_in_python"
title: "How do I profile memory usage in Python? | Codemia"
fetched_at: "2026-10-06 12:55"
---

Python

Memory Profiling

Programming

Memory Management

Performance Optimization

### How do I profile memory usage in Python?

###### Data Structures & Algorithms practice on Codemia

Step through 300 algorithm problems with animated visualisers that show the data structure changing as the code runs.

[Practice algorithms](/dsa)

[Complexity & Performance](/knowledge-hub/topic/complexity)[Python](/knowledge-hub/topic/python)

## Introduction

Memory profiling in Python is less about one magic tool and more about combining views of your program over time. A script might have high peak memory, a slow leak, or temporary spikes during object creation. If you only check one metric, you may optimize the wrong part. The practical approach is to start with lightweight built-in tools, then move to line-level profiling when you identify suspicious code paths. You should also separate Python-object growth from native-extension memory usage, because NumPy, TensorFlow, and other libraries may allocate outside the Python allocator. This article outlines a repeatable workflow to find, explain, and fix memory issues with minimal guesswork.

## Core Sections

### 1\. Start with `tracemalloc` for allocation hotspots

`tracemalloc` tracks Python memory allocations and can compare snapshots before and after a workload.

python
    
    
    1import tracemalloc
    2
    3tracemalloc.start(25)  # store traceback depth
    4
    5# run workload
    6data = [str(i) * 100 for i in range(200_000)]
    7
    8top = tracemalloc.take_snapshot().statistics("lineno")[:5]
    9for stat in top:
    10    print(stat)

For leak hunting, take two snapshots and compare them:

python
    
    
    1snap1 = tracemalloc.take_snapshot()
    2run_batch()
    3snap2 = tracemalloc.take_snapshot()
    4for stat in snap2.compare_to(snap1, "lineno")[:10]:
    5    print(stat)

This quickly identifies files and lines responsible for net growth.

### 2\. Use process-level monitoring for RSS trends

If memory rises even when `tracemalloc` looks stable, native allocations may be involved. Monitor resident memory size (RSS) from the OS.

python
    
    
    1import os
    2import psutil
    3import time
    4
    5proc = psutil.Process(os.getpid())
    6for _ in range(5):
    7    print(f"RSS MB: {proc.memory_info().rss / (1024**2):.1f}")
    8    time.sleep(1)

Pair this with workload phases so you can correlate spikes with steps like parsing, model inference, or serialization.

### 3\. Line-by-line profiling with `memory_profiler`

When one function is suspicious, instrument it directly.

python
    
    
    1from memory_profiler import profile
    2
    3@profile
    4def transform(rows):
    5    cache = []
    6    for r in rows:
    7        cache.append({"id": r[0], "payload": r[1] * 10})
    8    return cache

Run with:

bash
    
    
    python -m memory_profiler app.py

You get per-line increments, making it obvious whether growth comes from list accumulation, copies, or temporary objects.

### 4\. Fix patterns, then re-measure

Common wins include streaming instead of loading full datasets, replacing large intermediate lists with generators, deleting references sooner, and reusing buffers. For long-running services, verify memory behavior over hours, not seconds. A profile that looks stable for one request may leak across thousands.

A robust loop is: baseline, isolate hotspot, apply one change, benchmark again. Multi-change commits make it hard to prove which fix worked.

### 5\. CI-friendly checks

For critical pipelines, add a regression test that enforces peak-memory budget for representative input sizes. You can measure max RSS in integration tests and fail when growth exceeds expected tolerance. That prevents subtle leaks from shipping unnoticed.

### Validation and production readiness

A reliable implementation should include more than a working snippet. Add a small reproducible dataset or input fixture that exercises expected behavior and edge cases, then codify it in automated tests. Include at least one “happy path,” one malformed input case, and one boundary condition so regressions are caught early. Instrument key steps with structured logs or metrics to make failures diagnosable in runtime environments, not just local development. If performance is relevant, keep a lightweight benchmark that can be rerun after refactors to ensure behavior stays within budget.

Operationally, document assumptions near the code: required library versions, environment variables, timezone/locale expectations, and failure handling strategy. For team workflows, add one integration test that mirrors real usage rather than only unit-level checks. This reduces drift between example code and production behavior. Treat these checks as part of feature completion, because most long-term issues are caused by unvalidated assumptions rather than syntax errors.

## Common Pitfalls

  * Relying only on `sys.getsizeof()` and missing nested or referenced object memory.

  * Assuming all memory appears in `tracemalloc` when native libraries allocate outside Python.

  * Profiling toy inputs that do not reproduce production object lifetimes.

  * Interpreting one-time startup allocations as leaks without steady-state comparison.

  * Applying multiple optimizations at once and losing causal evidence of improvement.




## Summary

Effective Python memory profiling is a layered process: use `tracemalloc` for Python allocation hotspots, RSS monitoring for total process memory, and line-level tools for precise function diagnosis. Treat profiling as an experiment, not a one-shot command. Capture baselines, make focused changes, and validate under realistic workloads. With that workflow, you can distinguish true leaks from normal growth and ship fixes that measurably improve stability and performance.

* * *

###### Related reading

  * [How do I query between two dates using MySQL?](/knowledge-hub/path/how_do_i_query_between_two_dates_using_mysql)
  * [How do I replace weak references when using ARC and targeting iOS 4.0?](/knowledge-hub/path/how_do_i_replace_weak_references_when_using_arc_and_targeting_ios_40)
  * [How do I resize the UIImage to reduce upload image size](/knowledge-hub/path/how_do_i_resize_the_uiimage_to_reduce_upload_image_size)
  * [How do I scale one rectangle to the maximum size possible within another rectangle?](/knowledge-hub/path/how_do_i_scale_one_rectangle_to_the_maximum_size_possible_within_another_rectangle)
  * [How do I properly assert that an exception gets raised in pytest?](/knowledge-hub/path/how_do_i_properly_assert_that_an_exception_gets_raised_in_pytest)
  * [How do I properly assert that an exception gets raised in pytest?](/knowledge-hub/path/how_do_i_properly_assert_that_an_exception_gets_raised_in_pytest_1)
  * [How do I search for a number in a 2d array sorted left to right and top to bottom?](/knowledge-hub/path/how_do_i_search_for_a_number_in_a_2d_array_sorted_left_to_right_and_top_to_bottom)
  * [How do I select an entire row which has the largest ID in the table?](/knowledge-hub/path/how_do_i_select_an_entire_row_which_has_the_largest_id_in_the_table)

[](/courses/dsa_fundamentals)

Course

Intermediate

27 lessons

15 hours

###### DSA Fundamentals

Master algorithmic patterns and data structures through hands-on LeetCode-style problems - from arrays and hashing to dynamic programming and advanced graphs.

[View the course](/courses/dsa_fundamentals)

###### Track what you have practised

A free account saves your progress, solutions and study plan across every problem on Codemia.

##### Data Structures & Algorithms practice on Codemia

Step through 300 algorithm problems with animated visualisers that show the data structure changing as the code runs.

[Practice algorithms](/dsa)
