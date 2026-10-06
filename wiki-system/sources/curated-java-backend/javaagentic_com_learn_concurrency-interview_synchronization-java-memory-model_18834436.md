---
source: "https://javaagentic.com/learn/concurrency-interview/synchronization-java-memory-model"
title: "Java Memory Model Explained: happens-before, synchronized vs ReentrantLock | JavaAgentic"
fetched_at: "2026-10-06 12:33"
---

On this page

  * The problem the JMM solves
  * happens-before
  * What synchronized does
  * wait, notify and the guarded block
  * ReentrantLock
  * ReadWriteLock and StampedLock
  * What gets asked



The Java Memory Model is the part of concurrency people skip, and it is the part that explains why correct-looking code fails on a different machine, under a different JIT, or only in production. It answers one question: when is a write made by one thread guaranteed to be visible to another?

## Key Takeaways

  * The JMM has two concerns: **visibility** (does the other thread see my write?) and **ordering** (can operations be reordered?).
  * Without a **happens-before** edge, there is no guarantee at all — not a delay, an absence of any promise.
  * `synchronized` provides mutual exclusion **and** a memory barrier at both entry and exit.
  * Intrinsic locks are **reentrant** , and released automatically on any exit including an exception.
  * `ReentrantLock` adds `tryLock`, timeouts, interruptibility, fairness and multiple conditions.



## The problem the JMM solves#

this may never terminate
    
    
    class Flag {
        private boolean running = true;      // not volatile
     
        void stop() { running = false; }
     
        void loop() {
            while (running) {
                // work
            }
            System.out.println("stopped");
        }
    }

Thread A calls `loop()`, thread B calls `stop()`. In a debugger this terminates. In production with the JIT warmed up it can run forever, because the compiler is permitted to hoist the field read out of the loop:

what the JIT is allowed to produce
    
    
    boolean local = running;      // read once
    while (local) { }             // now an infinite loop

That transformation is legal precisely because there is no happens-before edge between the write in B and the read in A. The compiler optimises as if the code were single-threaded, which is exactly what the JMM permits it to do in the absence of synchronisation.

Two distinct mechanisms cause this. **Visibility** : each core has its own store buffer and caches, so a write may sit in one core's buffer indefinitely. **Reordering** : the compiler, the JIT and the CPU all reorder independent instructions for speed, and only the _single-threaded_ result is guaranteed to be preserved.

## happens-before#

The JMM defines a partial order. If A happens-before B, then everything A did is visible to B and cannot be observed as reordered. The edges you can rely on:

Rule| Guarantee  
---|---  
Program order| Within one thread, each statement happens-before the next  
Monitor lock| Unlocking a monitor happens-before any later locking of **that same** monitor  
Volatile| A write to a volatile field happens-before every later read of it  
Thread start| `t.start()` happens-before anything in `t`  
Thread join| Everything in `t` happens-before `t.join()` returns  
Final field| Correct construction happens-before any thread seeing the reference  
Interrupt| `t.interrupt()` happens-before `t` detects the interrupt  
Transitivity| If A → B and B → C, then A → C  
  
The lock is not only mutual exclusion. Release publishes, acquire subscribes.

The transitivity rule is what makes the model usable in practice: it lets you reason about a chain of ordinary variables published behind a single volatile write or lock release, rather than marking every field.

## What synchronized does#

two forms, same mechanism
    
    
    public synchronized void increment() {        // locks `this`
        count++;
    }
     
    public void increment() {
        synchronized (lock) {                     // locks a private object — preferable
            count++;
        }
    }
     
    public static synchronized void reset() {     // locks Counter.class
        total = 0;
    }

On entry the thread acquires the object's **monitor** and its cached view of memory is invalidated. On exit — normal or exceptional — pending writes are flushed and the monitor is released, creating a happens-before edge with the next acquirer.

Three properties worth stating:

**Reentrant.** A thread already holding a monitor can acquire it again; the JVM keeps a hold count. Without this, any `synchronized` method calling another `synchronized` method on the same object would deadlock instantly.

**Automatically released.** The JVM releases the monitor on any exit path, including a thrown exception. This is the main safety advantage over an explicit lock.

**Not a fair lock.** A waiting thread has no queue position. Under contention, a thread that just released the lock may reacquire it immediately, which is good for throughput and bad for latency outliers.

## wait, notify and the guarded block#

the required shape
    
    
    private final Object lock = new Object();
    private final Queue<Task> queue = new ArrayDeque<>();
     
    public void put(Task t) {
        synchronized (lock) {
            queue.add(t);
            lock.notifyAll();          // wake every waiter
        }
    }
     
    public Task take() throws InterruptedException {
        synchronized (lock) {
            while (queue.isEmpty()) {  // WHILE, never if
                lock.wait();           // releases the monitor, re-acquires on wake
            }
            return queue.poll();
        }
    }

Two rules that are always tested. **`wait()` must be in a loop**, because a thread can wake without a matching `notify` (a spurious wakeup) or because another thread consumed the item first. And **`notifyAll` over `notify`** unless you can prove every waiter is interchangeable — `notify` waking the wrong waiter is a lost-wakeup hang that reproduces once a month.

In modern code you would use a `BlockingQueue` and write none of this. Being able to explain the mechanism is still expected, because it is what `BlockingQueue` is built from.

## ReentrantLock#

what synchronized cannot do
    
    
    private final ReentrantLock lock = new ReentrantLock();
     
    public boolean transfer(Account to, BigDecimal amount) throws InterruptedException {
        // 1. Give up rather than wait forever — the standard deadlock defence.
        if (!lock.tryLock(100, TimeUnit.MILLISECONDS)) {
            return false;
        }
        try {
            // 2. Multiple condition variables on one lock.
            while (balance.compareTo(amount) < 0) {
                sufficientFunds.await();          // a separate wait-set from `notFull`
            }
            balance = balance.subtract(amount);
            return true;
        } finally {
            lock.unlock();      // MANDATORY — the JVM will not do this for you
        }
    }

| `synchronized`| `ReentrantLock`  
---|---|---  
Release| Automatic on any exit| **Manual, in`finally`**  
`tryLock`| No| Yes, with optional timeout  
Interruptible acquire| No| `lockInterruptibly()`  
Fairness| No| Optional (`new ReentrantLock(true)`)  
Condition variables| One per object| Many per lock  
Lock across methods| No| Yes  
Uncontended speed| Same| Same  
  
The `finally` requirement is the reason to prefer `synchronized` by default. A path that returns or throws before `unlock()` leaks the lock permanently, and the resulting hang gives no clue where the lock was acquired.

Fairness deserves a caveat: a fair lock hands ownership to the longest-waiting thread, which removes starvation but can cut throughput by an order of magnitude, because it prevents barging and forces a context switch on every handoff. Use it only when starvation is an observed problem.

## ReadWriteLock and StampedLock#

many readers, one writer
    
    
    private final ReadWriteLock rw = new ReentrantReadWriteLock();
     
    public Config read() {
        rw.readLock().lock();
        try { return current; } finally { rw.readLock().unlock(); }
    }
     
    public void write(Config c) {
        rw.writeLock().lock();
        try { current = c; } finally { rw.writeLock().unlock(); }
    }

A `ReadWriteLock` allows concurrent readers but excludes them during a write. It only pays off when reads greatly outnumber writes **and** the critical section is long enough to amortise the extra bookkeeping — for a short read, the lock overhead exceeds the work and a plain `synchronized` block is faster.

`StampedLock` (Java 8) adds an **optimistic read** : take a stamp, read the fields, then validate that no write intervened. If validation fails, fall back to a real read lock. It is the fastest option for read-dominated data, and it is not reentrant and does not support conditions — so it is easy to misuse.

optimistic read
    
    
    long stamp = sl.tryOptimisticRead();
    double x = this.x, y = this.y;        // may be torn
    if (!sl.validate(stamp)) {            // a writer intervened
        stamp = sl.readLock();
        try { x = this.x; y = this.y; } finally { sl.unlockRead(stamp); }
    }

For most application code the correct answer is none of these: use an immutable object published through a `volatile` field, and replace it wholesale on change. No lock, no contention, and the final-field guarantee does the rest.

## What gets asked#

"What does `synchronized` do?" — and the complete answer is _mutual exclusion plus a memory barrier that establishes happens-before_. Then: `synchronized` versus `ReentrantLock`; why `wait` must be in a `while` loop; and what happens-before means. If you can produce the non-terminating loop example and explain that the JIT is permitted to hoist the read, you have demonstrated the model rather than recited the vocabulary.

## Frequently Asked Questions

What does happens-before actually mean?

It is an ordering guarantee between two actions, not a statement about wall-clock time. If action A happens-before action B, then everything A wrote is visible to B, and the compiler and CPU may not reorder them in a way B could observe. Without a happens-before edge between two threads, there is no guarantee that one ever sees the other writes — not merely a delay, but no guarantee at all.

Is synchronized only about mutual exclusion?

No, and this is the half most answers miss. Entering a monitor invalidates the thread cached view so subsequent reads see main memory, and exiting flushes writes and establishes a happens-before edge with the next thread to enter. It also prevents the compiler and CPU from reordering across the boundary. A lock that only provided mutual exclusion would still let two threads see different values.

When should I use ReentrantLock instead of synchronized?

When you need something synchronized cannot express: tryLock with a timeout, an interruptible acquire, fairness, several condition variables on one lock, or a lock acquired in one method and released in another. Otherwise use synchronized — it is simpler, it cannot leak a lock because the JVM releases it on exit, and since biased and thin locking it is essentially as fast when uncontended.

## Related tutorials

  * [Threads: Lifecycle, Creation and What One CostsThe six thread states and what moves between them, why calling run() directly is a no-op, what a platform thread actually costs in memory and switching, and the interrupt protocol done properly.](/learn/concurrency-interview/thread-lifecycle-creation)
  * [volatile, Atomics and the Visibility ProblemWhat volatile guarantees and what it does not, why count++ is broken even when volatile, how compare-and-swap works, when LongAdder beats AtomicLong, and the double-checked locking idiom.](/learn/concurrency-interview/volatile-atomics-visibility)
  * [ExecutorService and Thread-Pool SizingHow ThreadPoolExecutor decides whether to queue or grow, why newFixedThreadPool can exhaust the heap, sizing pools from measurements with Little law, and shutting down without losing work.](/learn/concurrency-interview/executor-service-thread-pools)
  * [CompletableFuture and Async CompositionComposing async work without blocking: thenApply versus thenCompose, which thread runs each stage, combining with allOf and anyOf, timeouts, and how exceptions propagate through a chain.](/learn/concurrency-interview/completablefuture-async-patterns)


