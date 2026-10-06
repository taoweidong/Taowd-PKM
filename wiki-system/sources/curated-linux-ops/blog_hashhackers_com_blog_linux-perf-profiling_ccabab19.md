---
source: "https://blog.hashhackers.com/blog/linux-perf-profiling"
title: "Linux perf: CPU Profiling, Tracing, and Flame Graphs"
fetched_at: "2026-10-06 12:37"
---

Oct 1, 2024 

# Linux perf: CPU Profiling, Tracing, and Flame Graphs

* * *

`perf` is the official Linux performance analysis tool, integrated into the kernel source tree. It provides access to hardware performance counters, software counters, and kernel tracepoints with minimal overhead. Combined with Brendan Gregg’s Flame Graph visualization, it is the most powerful tool for CPU-level performance analysis.

## Installation
    
    
    # Debian/Ubuntu
    apt install linux-tools-$(uname -r) linux-tools-generic
    
    # RHEL/Fedora
    dnf install perf
    
    # Verify
    perf version

## perf stat: Hardware Counters

`perf stat` measures hardware performance counters for a command or PID:
    
    
    # Profile a command
    perf stat ls -la /var
    
    # Extended stats
    perf stat -a sleep 5  # system-wide for 5 seconds
    
    # Specific events
    perf stat -e cycles,instructions,cache-misses,branch-misses ./myapp
    
    # IPC (Instructions Per Cycle) calculation
    perf stat -e cycles,instructions ./myapp
    # IPC = instructions / cycles
    
    # Profile a running process
    perf stat -p $(pgrep nginx) sleep 10
    
    # Output example:
    #  Performance counter stats for 'ls -la /var':
    #       1,234,567  cpu-cycles
    #       2,345,678  instructions  # IPC = 1.90
    #           1,234  cache-misses  # 0.05% miss rate

## perf record and report: CPU Profiling
    
    
    # Sample CPU at 99Hz for 30 seconds
    perf record -g -F 99 -a -- sleep 30
    
    # Sample a specific process
    perf record -g -F 99 -p $(pgrep myapp) -- sleep 30
    
    # Interactive report
    perf report
    
    # Text report
    perf report --stdio | head -50
    
    # Annotate specific function
    perf annotate --symbol=do_page_fault
    
    # Top-like interactive view
    perf top
    perf top -p $(pgrep nginx)  # process-specific

## Flame Graphs

Flame Graphs visualize call stacks, making hot code paths immediately visible:
    
    
    # Install Flame Graph scripts
    git clone https://github.com/brendangregg/FlameGraph.git
    
    # Record with stack frames
    perf record -g --call-graph dwarf -F 99 -p $(pgrep myapp) -- sleep 30
    
    # Generate Flame Graph
    perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > flame.svg
    
    # Open in browser
    firefox flame.svg
    
    # Off-CPU flame graphs (time waiting, not executing)
    perf record -e sched:sched_switch --call-graph dwarf -a -- sleep 30
    perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > off-cpu.svg

## perf trace: System Call Tracing

`perf trace` is a modern alternative to `strace` with less overhead:
    
    
    # Trace a command's syscalls
    perf trace ls /tmp
    
    # Trace a running process
    perf trace -p $(pgrep nginx)
    
    # Trace specific syscalls
    perf trace -e syscalls:sys_enter_write -p 1234
    
    # Summary mode (like strace -c)
    perf trace --summary ./myapp
    
    # Show only slow syscalls
    perf trace --duration 1 ./myapp  # Only syscalls >1ms

## perf Events and Tracepoints
    
    
    # List all available events
    perf list
    
    # List tracepoints
    perf list tracepoint
    
    # Trace kernel scheduler events
    perf record -e sched:sched_wakeup,sched:sched_switch -a -- sleep 5
    perf script
    
    # Trace block I/O
    perf record -e block:block_rq_issue,block:block_rq_complete -a -- sleep 5
    
    # Network events
    perf record -e net:net_dev_xmit,net:netif_receive_skb -a -- sleep 5

## Memory Profiling
    
    
    # Sample memory access events
    perf record -e cache-misses,cache-references -g -p $(pgrep myapp) -- sleep 10
    perf report --sort=dso,sym
    
    # Memory bandwidth measurement
    perf stat -e LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses -a sleep 5
    
    # NUMA memory events (if available)
    perf stat -e node-loads,node-load-misses -a sleep 5

## perf bench: Micro-benchmarks
    
    
    # Memory copy speed
    perf bench mem memcpy
    
    # Memory set speed
    perf bench mem memset
    
    # Scheduling performance
    perf bench sched pipe
    
    # Futex performance
    perf bench futex hash
    perf bench futex wake

## Profiling with Annotations
    
    
    # Record with debug info
    perf record -g --call-graph dwarf -F 99 -p $(pgrep myapp) -- sleep 10
    
    # Annotate a hot function
    perf report --tui
    # Navigate to a function, press 'a' to annotate
    
    # Command-line annotation
    perf annotate --symbol=hash_lookup --stdio

## Continuous Profiling in Production
    
    
    # Low-overhead continuous profiling (1% CPU)
    perf record -g -F 10 -a -o /tmp/perf.data -- sleep 60
    
    # For production, consider:
    # - perf with lower frequency (-F 10 instead of 99)
    # - BPF-based profilers (bpftrace, parca, pyroscope)
    # - eBPF profiling: always-on with <1% overhead

`perf` is an indispensable tool for understanding where CPU time is actually spent. The combination of hardware counters, stack sampling, and Flame Graph visualization makes it possible to find performance bottlenecks that would be invisible to application-level profilers.
