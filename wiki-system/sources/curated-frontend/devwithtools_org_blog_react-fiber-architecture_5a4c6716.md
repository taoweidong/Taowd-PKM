---
source: "https://devwithtools.org/blog/react-fiber-architecture"
title: "React Fiber Architecture & Reconciliation Internals (2026 Guide) | DevWithTools"
fetched_at: "2026-10-06 12:33"
---

ReactJuly 20, 2026·22 min read·By [Keyur Patel](/about/keyur-patel)

You call `setState`. React re-renders your component. The DOM updates. It feels instant. But what actually happens between your state change and the pixels changing on screen? How does React know WHICH components to re-render? How does it update 10,000 list items without dropping a frame? And how can it pause a render mid-way through to handle a more urgent user interaction?

The answer to all of these is **Fiber** — React's internal rendering engine, introduced in React 16 and the foundation for every concurrent feature since (Suspense, transitions, streaming SSR). Most React developers never need to know Fiber exists. But understanding it transforms how you think about performance, re-renders, keys, and why certain patterns are fast while others aren't.

This guide takes you inside React's engine: the fiber tree structure, how reconciliation diffs the old and new trees, the two-phase render/commit cycle, priority lanes, time slicing, and how concurrent features like `startTransition` actually work at the implementation level.

## The Problem: Why the Old Reconciler Broke Down

Before React 16, the reconciler used a recursive, stack-based approach. When you called setState, React would synchronously walk the entire component tree — calling render functions, diffing results, and updating the DOM — all in one uninterruptible pass.

stack-reconciler.js
    
    
    function reconcile(element) {
      const component = createComponent(element)
      const rendered = component.render()  // Recursively process ALL children synchronously  for (const child of rendered.children) {
        reconcile(child)  // Can't stop here — call stack owns us  }
      updateDOM(component)
    }// Problem: if tree has 10,000 nodes → 200ms+ blocked
    // Result: jank, dropped frames, unresponsive UI

The fundamental issue: JavaScript is single-threaded. The call stack can't be paused. Once you start recursing through 10,000 components, you can't stop until it's done.

Stack Reconciler (Old)

Render A

→

Render B

→

Render C

→

Render D

→

Render E

⚠️ Blocks for 200ms — can't pause

Fiber Reconciler (New)

Fiber A

Fiber B

⏸ Yield

Fiber C

Fiber D

✓ 5ms slices — yields to browser between

## What Is a Fiber Node?

A fiber is a plain JavaScript object that represents a unit of work. Every component instance, DOM element, and fragment in your app has a corresponding fiber. Together, they form a tree connected by three pointers: `child`, `sibling`, and `return` (parent).

Fiber Node Structure

Identity

tag: FunctionComponent

type: MyComponent

key: "item-42"

stateNode: DOM element

Tree Pointers

child: first child fiber

sibling: next sibling

return: parent fiber

alternate: twin tree

Work Data

pendingProps: new props

memoizedState: hooks

flags: Update | Place

lanes: SyncLane

### Fiber Tree as Linked List

App

child

Header

sibling

Main

sibling

Footer

child

Article

sibling

Sidebar

child (down) sibling (right) return (up to parent)

Traversal: go to child → then sibling → then return to parent's sibling. This makes the tree iterable without recursion.

## The Two Phases: Render and Commit

React splits its work into two distinct phases with very different rules:

Phase 1: Render⏸ Interruptible

Call components

Build fiber tree

Diff old vs new

Mark effects

Pure computation

Can pause

Phase 2: Commit🔒 Synchronous

Apply DOM changes

Call refs

useLayoutEffect

useEffect (async)

Side effects

Cannot interrupt

✓ Screen Updated

The key insight: your component function might be called and then **thrown away** (if a higher-priority update interrupts). That's why render functions must be pure — no side effects. Side effects belong in `useEffect` (which runs after commit).

## Reconciliation: The Diffing Algorithm

Reconciliation is how React determines the minimum set of DOM operations needed. Comparing two arbitrary trees is O(n³) — unusable for UIs. React uses two heuristics to bring it to O(n):

1

**Type comparison:** Elements of different types produce entirely different trees. `<div>` → `<span>` = unmount entire subtree and rebuild.

2

**Keys for identity:** Same key = same element even if position changed. React moves the DOM node instead of destroying and recreating.

### Four Reconciliation Scenarios

UPDATE

Same type, different props

Old: <button class="blue">

New: <button class="red">

→ Keep DOM node, patch attribute

REPLACE

Different type

Old: <div><Counter /></div>

New: <span><Counter /></span>

→ Destroy tree + state, mount fresh

REORDER

List with keys

Old: [a, b, c]

New: [c, a, b]

→ Move DOM nodes, keep state

REBUILD

List without keys (index match)

Insert at [0]: [new, a, b, c]

Indices shift: all "changed"

→ Rebuilds ALL items (expensive!)

keys-example.jsx
    
    
    // ❌ Index as key — breaks on reorder/insert
    {items.map((item, i) => <Item key={i} data={item} />)}
    // ✓ Stable unique ID — correct reconciliation
    {items.map(item => <Item key={item.id} data={item} />)}

## Priority Lanes: Not All Updates Are Equal

React assigns every update a **lane** — a bitmask representing its priority. Higher-priority updates are processed first. Lower-priority work can be interrupted.

React Priority Lanes

SyncLane

click, keydown

Highest

InputContinuousLane

mousemove, scroll

High

DefaultLane

setState in effects

Normal

TransitionLane

startTransition

Low

IdleLane

offscreen content

Lowest

startTransition-example.jsx
    
    
    function SearchPage() {
      const [query, setQuery] = useState('')
      const [results, setResults] = useState([])
    
      function handleInput(e) {// URGENT (SyncLane) — input responds instantly
        setQuery(e.target.value)
    // LOW PRIORITY (TransitionLane) — interruptible
        startTransition(() => {
          setResults(filterLargeDataset(e.target.value))
        })
      }
    }

## The Work Loop: Time Slicing in Action

The heart of Fiber is the work loop — an iterative loop that processes one fiber at a time and yields control back to the browser between frames (~5ms slices).

work-loop.js
    
    
    function workLoopConcurrent() {// Process fibers one at a time — can pause between any two
      while (workInProgress !== null && !shouldYield()) {
        workInProgress = performUnitOfWork(workInProgress)
      }
    }
    
    function shouldYield() {// Used ~5ms? Give browser a chance to paint + handle events
      return performance.now() >= deadline
    }
    
    function performUnitOfWork(fiber) {// 1. Call component function, diff children
      const next = beginWork(fiber)
      if (next) return next    // Process child next
    // 2. No children — complete and move to sibling/parent
      return completeUnitOfWork(fiber)
    }

Time Slicing Visualization (16ms frame budget)

Frame 1

React (5ms)

Paint

Idle

Frame 2

React (5ms)

Event

Paint

Idle

Frame 3

React (5ms)

Paint

Commit!

Idle

Each frame: React works ~5ms, then yields. Browser paints smoothly at 60fps. No jank.

## Performance Implications You Can Act On

⚡

#### Bail out with React.memo

If props haven't changed, React skips the entire subtree. No render call, no diffing, no work.

🔑

#### Stable keys prevent remounting

Wrong keys = destroy + rebuild DOM nodes + lose state. Correct keys = reuse fibers, move DOM nodes.

📍

#### Move state down, reduce scope

When a fiber re-renders, ALL children re-render by default. Lower state = smaller blast radius.

🚀

#### startTransition for heavy work

Wrap expensive setState in startTransition. React processes it at low priority — typing stays smooth.

🧪

#### Render must be pure

In concurrent mode, your component might render multiple times or be discarded. Side effects = bugs.

## Common Mistakes

1

Side effects in render body

Move to useEffect. Render can be called multiple times or discarded in concurrent mode.

2

Array index as key for dynamic lists

Use stable unique IDs. Index-as-key causes full rebuilds on insert/reorder.

3

Changing component type conditionally

Same position, different type = unmount + remount. Use same component with different props instead.

4

Defining components inside render

New function ref each render = new 'type' = unmount entire subtree. Define at module level.

5

Synchronous heavy computation in setState

Wrap in startTransition to allow interruption by urgent user interactions.

## Frequently Asked Questions

What is React Fiber?

React Fiber is the internal reconciliation engine introduced in React 16. It replaced the old stack-based reconciler with an incremental, pausable rendering architecture. Each component instance is represented as a 'fiber' node in a linked-list tree. This structure allows React to pause work, prioritize updates, and resume rendering without blocking the main thread.

What is reconciliation in React?

Reconciliation is the algorithm React uses to determine what changed between the previous render and the current render. It compares the old fiber tree (current) with the new one (workInProgress), identifies differences, and produces a minimal set of DOM mutations. This 'diffing' process uses heuristics like same-type comparison and keys to avoid O(n³) tree comparison.

Why did React move from Stack to Fiber?

The old stack reconciler processed the entire component tree synchronously in one pass. If the tree was large (thousands of components), this blocked the main thread for hundreds of milliseconds — causing dropped frames, janky animations, and unresponsive UIs. Fiber splits work into small units that can be paused and resumed, keeping the UI responsive even during heavy renders.

What is a fiber node?

A fiber node is a JavaScript object representing a unit of work — it corresponds to a component instance, a DOM element, or a React fragment. Each fiber stores: the component type, props, state, a pointer to its parent/child/sibling fibers, effect flags (what DOM changes are needed), and priority lane information. The fiber tree is a linked list traversed via child, sibling, and return pointers.

What are priority lanes in React?

Lanes are React's priority system for scheduling updates. Different updates get different priority: user input (click, type) gets the highest priority (SyncLane), transitions get lower priority (TransitionLane), and Suspense/offscreen work gets the lowest. React processes higher-priority lanes first and can interrupt lower-priority work to handle urgent updates immediately.

What is the difference between render phase and commit phase?

The render phase builds the new fiber tree by calling component functions and diffing — this is pure computation with no side effects and can be paused/interrupted. The commit phase applies the computed changes to the actual DOM — this is synchronous and cannot be interrupted (to avoid showing partial UI updates). Effects (useEffect) run after the commit phase.

How do keys help reconciliation?

Keys tell React which items in a list correspond to which items in the previous render. Without keys, React matches by index — if you insert an item at the beginning, every item shifts index and React thinks they all changed (expensive). With keys, React matches by identity — it knows 'item-42' moved from position 3 to position 4 and simply moves the DOM node.

What is concurrent rendering?

Concurrent rendering is React's ability to work on multiple versions of the UI simultaneously. React can start rendering a new state, pause if something more urgent comes in (user typing), handle the urgent work first, then resume or discard the previous work. This is enabled by Fiber's pausable architecture and features like startTransition, useDeferredValue, and Suspense.

## Related Articles & Tools

[How AI Coding Agents WorkComplex systems under the hood — similar deep-dive into AI agent architecture.](/blog/how-ai-coding-agents-work)[JavaScript Minification GuideBundle optimization and performance — the other side of React performance.](/blog/javascript-minification-guide)[Caching ExplainedPerformance optimization at every layer — from browser to server.](/blog/caching-explained)

## Conclusion

Fiber transformed React from a simple view library into a sophisticated rendering engine that can pause work, prioritize interactions, and update complex UIs without dropping frames. The key ideas: fiber nodes as a pausable linked-list tree, two-phase render/commit, double buffering, and priority lanes for scheduling.

You don't need to know Fiber internals to use React well. But understanding them explains WHY certain practices matter: why keys are important (reconciliation identity), why render must be pure (interruptible), why startTransition exists (lane scheduling), and why React.memo works (subtree bailout in the render phase).

The practical takeaway: React's performance ceiling is higher than most developers realize. If your app is slow, it's rarely React's reconciler — it's unnecessary re-renders (fix with memoization), wrong key usage (fix with stable IDs), or synchronous heavy computation (fix with startTransition). Understanding Fiber tells you exactly where to look.

[← Back to Blog](/blog)
