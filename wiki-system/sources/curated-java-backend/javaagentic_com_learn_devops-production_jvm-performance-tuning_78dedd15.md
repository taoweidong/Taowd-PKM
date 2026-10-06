---
source: "https://javaagentic.com/learn/devops-production/jvm-performance-tuning"
title: "JVM Tuning Guide: G1 vs ZGC, GC Logging, JFR and async-profiler | JavaAgentic"
fetched_at: "2026-10-06 12:32"
---

On this page

  * The memory model
  * Collector choice
  * GC logging
  * Profiling
  * Native memory
  * Container-aware settings
  * A tuning method that works
  * What to take away



Most JVM performance work is misdirected because it starts from a guess. The reliable sequence is measure, find the actual bottleneck, change one thing, measure again — and the bottleneck is usually not what anyone expected.

## Key Takeaways

  * Always **measure first**. GC flags applied without evidence usually make things worse.
  * **G1 by default** ; ZGC when GC pause is provably your latency problem.
  * **GC logging is nearly free** — enable it everywhere, permanently.
  * **JFR** is the low-overhead production profiler; **async-profiler** gives the best flame graphs.
  * In containers, size the heap as a **percentage** and remember non-heap memory exists.



## The memory model#

The container limit covers everything, not just the heap. Sizing -Xmx to the limit guarantees an eventual OOMKill.

That diagram explains the most common container incident: a pod with a 1Gi limit and `-Xmx1g` gets OOMKilled, and the heap graph shows nothing wrong — because the heap never overflowed. Metaspace, several hundred threads at 1MB of stack each, and Netty's direct buffers consumed the difference.

## Collector choice#

Collector| Pause| Throughput| Best for  
---|---|---|---  
Serial| High| Low| Tiny heaps, single core  
Parallel| High| Highest| Batch jobs, throughput over latency  
G1| ~50-200ms| High| The default; most services  
ZGC| Under 1ms| Slightly lower| Latency-sensitive, large heaps  
Shenandoah| Under 10ms| Slightly lower| Similar to ZGC  
  
G1 — the sensible default
    
    
    java -XX:+UseG1GC \
         -XX:MaxGCPauseMillis=200 \
         -XX:InitiatingHeapOccupancyPercent=45 \
         -XX:MaxRAMPercentage=75.0 \
         -jar app.jar

ZGC — when GC pause dominates p99
    
    
    java -XX:+UseZGC -XX:+ZGenerational \
         -XX:MaxRAMPercentage=70.0 \
         -jar app.jar

`MaxGCPauseMillis` is a **goal** , not a guarantee. G1 adjusts region counts and young-generation size trying to meet it; setting it unrealistically low (20ms on a 8GB heap) makes G1 shrink the young generation until it collects constantly, which is worse on every axis.

The one flag worth setting almost everywhere: `-Xms` equal to `-Xmx`, or `InitialRAMPercentage` equal to `MaxRAMPercentage`. Heap resizing costs full collections, and in a container you have already reserved the memory.

## GC logging#

always on
    
    
    -Xlog:gc*,safepoint:file=/var/log/gc-%t.log:time,level,tags:filecount=10,filesize=50M

The overhead is negligible and the diagnostic value during an incident is enormous. What to look for:

reading a G1 log
    
    
    [2026-07-26T09:14:03.221+0000] GC(412) Pause Young (Normal) 3210M->1840M(4096M) 42.331ms
                                            │                    │       │      │
                                            │                    │       │      total heap
                                            │                    │       after collection
                                            │                    before collection
                                            collection number

Three patterns tell you what is wrong. **Occupancy after collection climbing steadily** across many cycles is a leak — objects are being retained. **Frequent full collections** (`Pause Full`) mean the heap is too small or fragmented. **Pause times far above the goal** usually mean the young generation is too large or the machine is CPU-starved.

Safepoint logging catches a subtler problem: long time-to-safepoint means a thread was slow to reach a pause point, often due to a long-running counted loop, and that time is invisible in GC pause figures while being very visible to users.

## Profiling#

**JDK Flight Recorder** has around 1% overhead and is safe to run continuously:

continuous JFR
    
    
    java -XX:StartFlightRecording=name=continuous,maxsize=256m,maxage=6h,\
    settings=profile,dumponexit=true,filename=/var/log/app.jfr -jar app.jar
     
    # Dump the current buffer from a running process
    jcmd <pid> JFR.dump name=continuous filename=/tmp/incident.jfr

Open the file in JDK Mission Control and it shows hot methods, allocation by call site, GC timeline, lock contention and I/O — all correlated on one timeline. The allocation view is often the most valuable: excessive garbage creation is a far more common cause of GC pressure than a genuine leak.

**async-profiler** produces better flame graphs and can profile wall-clock time, which JFR does not:

async-profiler
    
    
    ./profiler.sh -d 60 -e cpu -f /tmp/cpu.html <pid>
    ./profiler.sh -d 60 -e alloc -f /tmp/alloc.html <pid>
    # Wall clock includes time blocked on I/O — usually where the time actually goes
    ./profiler.sh -d 60 -e wall -t -f /tmp/wall.html <pid>

For a typical Spring service, the wall-clock profile is the revealing one. CPU profiles show the JVM mostly idle because the service is waiting on a database or another service, and the flame graph of _waiting_ is what points at the real bottleneck.

## Native memory#

Native Memory Tracking
    
    
    java -XX:NativeMemoryTracking=summary -jar app.jar
    jcmd <pid> VM.native_memory summary
    
    
    Total: reserved=2560MB, committed=1180MB
    -   Java Heap (reserved=1024MB, committed=768MB)
    -       Class (reserved=280MB, committed=92MB)     # metaspace
    -      Thread (reserved=412MB, committed=412MB)    # 400 threads x ~1MB
    -        Code (reserved=250MB, committed=48MB)
    -  Compiler, GC, Internal, Symbol ...

That thread figure is a common surprise. A service with a large Tomcat pool plus several executors easily reaches 400 threads, which is 400MB of stack reservation before any application data exists. Reducing pool sizes or moving to virtual threads reclaims it.

## Container-aware settings#

production JVM flags
    
    
    java -XX:MaxRAMPercentage=75.0 \
         -XX:InitialRAMPercentage=75.0 \
         -XX:+UseG1GC \
         -XX:+ExitOnOutOfMemoryError \
         -XX:+HeapDumpOnOutOfMemoryError \
         -XX:HeapDumpPath=/var/log/heapdump.hprof \
         -Xlog:gc*:file=/var/log/gc.log:time:filecount=5,filesize=20M \
         -Djava.security.egd=file:/dev/./urandom \
         -jar app.jar

`ExitOnOutOfMemoryError` matters in Kubernetes. Without it, heap exhaustion leaves the JVM alive but useless — failing every request while a liveness probe that only checks the context still passes. Exiting lets the orchestrator restart it.

`HeapDumpOnOutOfMemoryError` gives you the evidence, but write it to a mounted volume; a dump written to the container filesystem disappears with the container.

## A tuning method that works#

Change **one thing at a time** , and measure the same workload before and after. Tuning several flags together makes it impossible to attribute an improvement, and JVM flags interact in non-obvious ways.

Measure the metric that matters to users — p99 latency, or throughput at a fixed latency budget — not GC pause time in isolation. A change that halves pause frequency while raising p99 is not an improvement.

And before touching a single flag, check the obvious: an N+1 query, a missing index, a synchronous call that could be parallel, or a cache that is not being hit. Application-level problems dwarf GC tuning in almost every service, and no collector configuration fixes a query that runs a thousand times per request.

## What to take away#

Measure before you tune, and check for application-level problems first. Use G1 with a realistic pause goal, size the heap as a percentage of the container limit, and set `-Xms` equal to `-Xmx`. Leave GC logging and JFR on permanently — the cost is negligible and having the data during an incident is what makes diagnosis possible.

## Frequently Asked Questions

Which garbage collector should I use?

G1 unless you have a specific reason otherwise — it is the default and balances throughput against pause time well. Move to ZGC when p99 latency is dominated by GC pauses and you have the heap to spare, since ZGC keeps pauses under a millisecond regardless of heap size. Parallel remains best for batch jobs where throughput is all that matters.

How much heap should I give a service?

Enough that steady-state occupancy after a full GC sits around 30-50% of the heap. Too small and you collect constantly; too large and full collections take longer and you waste memory that would serve better as page cache. Measure occupancy after GC rather than guessing.

Is a memory leak always a heap problem?

No, and assuming so wastes time. Native memory — direct byte buffers, thread stacks, metaspace, mapped files — sits outside the heap and is a common cause of container OOMKills with a perfectly healthy heap graph. Use Native Memory Tracking to see the whole process.

## Related tutorials

  * [Database Migrations with FlywaySchema changes you can deploy safely: Flyway naming and ordering, repeatable migrations, baselining an existing database, and expand-and-contract for zero downtime.](/learn/devops-production/database-migrations-flyway)
  * [Load Testing & Capacity PlanningFinding your limits before users do: the five load test types, writing k6 and Gatling scenarios, the metrics that matter, and turning results into a capacity plan.](/learn/devops-production/load-testing-capacity-planning)
  * [Production-Grade Application ConfigurationConfiguration that survives production: the 12-factor principles applied to Java, property precedence, fail-fast validation, feature flags, and graceful shutdown done properly.](/learn/devops-production/production-application-configuration)
  * [Disaster Recovery & High AvailabilityPlanning for failure: defining RPO and RTO honestly, replication trade-offs, multi-region topologies and their costs, DNS failover, and testing recovery before you need it.](/learn/devops-production/disaster-recovery-high-availability)


