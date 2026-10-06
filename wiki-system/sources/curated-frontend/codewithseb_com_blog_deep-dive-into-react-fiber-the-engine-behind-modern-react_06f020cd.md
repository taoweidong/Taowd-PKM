---
source: "https://codewithseb.com/blog/deep-dive-into-react-fiber-the-engine-behind-modern-react"
title: "A Deep Dive into React Fiber — The Engine Behind Modern React | Code With Seb"
fetched_at: "2026-10-06 12:33"
---

React Fiber is a complete re-architecture of React’s core reconciliation algorithm designed to overcome the limitations of the old “stack reconciler.” Under the original approach (pre-React 16), updates were processed synchronously in a single depth-first pass through the component tree. Every state change would cause React to walk the entire affected subtree in one go, compute the diff, and update the DOM before returning control. This meant no ability to pause mid-render or change priorities: a heavy update (e.g. filtering a large list) would block the main thread, causing janky animations and unresponsive input. As one blogger explains, “React couldn’t pause mid-render…Browser main thread got blocked…Laggy inputs, janky scroll, and UI freezes”. All updates were treated equally urgent, so user interactions (like typing) could get stuck behind expensive renders. These limitations motivated Fiber: React Fiber “rewrites the reconciliation algorithm…to take advantage of scheduling” so that work can be paused, prioritized, and spread over multiple frames.

In Fiber, the component tree is reimplemented as a linked list of “fiber” nodes, each representing a unit of work (like a stack frame). Unlike the old stack-based approach, Fiber can interrupt a render, yield control back to the browser, and resume later. In essence, Fiber allows React to “[pause] work and come back to it later,” “[assign] priority to different types of work,” “[reuse] previously completed work,” and even “abort work if it’s no longer needed”

In summary, the Stack reconciler was synchronous and could not break work into chunks or handle new priorities, whereas Fiber’s linked-list structure and scheduler enable incremental, interruptible updates and advanced features. As one source notes, “React doesn’t currently take advantage of scheduling in a significant way… Overhauling React’s core algorithm to take advantage of scheduling is the driving idea behind Fiber”. Fiber effectively reimplements the call stack: you can think of each fiber as a “virtual stack frame” that React keeps in memory and can execute “however (and whenever) you want”. This change in architecture is crucial for supporting modern features like Concurrent React, Suspense, and automatic batching.

* * *

# Fiber Node Structure

Under the hood, each fiber is a JavaScript object containing all information about one component and its place in the tree. Key fields in a fiber include its component type and key (copied from the React element), child/sibling/return pointers, and various props/state fields. Concretely:

  * `type` and `key`: Describe the component type (function or class for composites, string for host elements) and reconciliation key.
  * `child` and `sibling`: Pointers forming a linked-list structure for the tree. The `child` field points to the first child fiber (i.e. the element returned by this component’s render), and each child’s sibling points to the next child. (This left-child/right-sibling representation makes the fiber tree easy to traverse one node at a time.) For example, given `Parent` with children `` and ``, the Parent fiber’s `child` points to `Child1`, and `Child1.sibling` points to `Child2`.
  * `return`: Points to the parent fiber (the “return address” of this stack frame). When a component finishes rendering its subtree, React uses `return` to go back to the parent.
  * `stateNode`: References the local instance (for class components) or the DOM node (for host components). This links the fiber to the actual UI elements.
  * `pendingProps` and `memoizedProps`: The new props being applied (`pendingProps`) versus the last rendered props (`memoizedProps`). When they match, React can skip re-rendering that subtree — this is the exact mechanism that [React Compiler's automatic memoization](/blog/react-compiler-deep-dive-automatic-memoization-guide) leverages at build time.
  * `pendingWorkPriority`: A numeric priority indicating how urgent this update is. Higher numeric values mean lower priority (0 means no work). React’s scheduler uses this field to decide which fibers to work on first.
  * `alternate`: A pointer to the alternate fiber (the other “version” of this component). React keeps two copies of each fiber (current and work-in-progress) and swaps them at commit. The `alternate` field links these two. At most two fibers exist per component: the current, flushed fiber and the work-in-progress fiber. The alternate of the current is the work-in-progress, and vice versa. This double-buffering allows React to build a new tree without clobbering the committed one.

All together, a fiber holds its identity (type, key), tree structure (child, sibling, return), input props, state, output (e.g. DOM node), and scheduling metadata. One author summarizes: “A Fiber is a plain JS object, a unit of work representing one component in the tree. Each fiber contains: 
  * Component type
  * Props and state
  * Links to child/parent/sibling fibers

A pointer to its DOM node; Effects queued for commit”. Compared to the old stack reconciler’s opaque call stack, this explicit object graph lets React pause in the middle of work, inspect or rewind it, and resume later. 

# Render & Commit Phases

React’s update process splits into two distinct phases: the render (reconciliation) phase and the commit phase. In the render phase, React traverses the fiber tree without touching the DOM, computing changes. In the commit phase, React applies those changes to the DOM (and runs lifecycle hooks) synchronously.
