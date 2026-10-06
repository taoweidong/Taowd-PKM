---
source: "https://rubel.dev/blog/deep-dive-into-the-reconciliation-algorithm-fiber-and-phases"
title: "Deep Dive into the Reconciliation Algorithm: Fiber and Phases | Mahamudul Hasan Rubel"
fetched_at: "2026-10-06 12:33"
---

[Lesson **1** of the **Advanced React: Performance, Architecture & Patterns** course](/courses/advanced-react-performance-architecture-patterns)

Previously in this course, we touched upon the high-level benefits of the Virtual DOM in [Understanding the Virtual DOM and React Performance](/blog/understanding-the-virtual-dom-and-react-performance). In this lesson, we are going under the hood to dissect the engine that makes those updates possible: the **React Fiber** architecture.

To build high-performance applications, you must move beyond thinking of React as a simple "render function." You need to understand how React schedules work, why it splits its lifecycle into specific phases, and how it manages the tree structure during updates.

## The Fiber Tree: From Recursion to Linked List

Before React 16, the reconciliation process was synchronous and recursive. Once React started updating the component tree, it couldn't stop until it reached the leaves. If a tree was deep or complex, this blocked the main thread, leading to dropped frames and a sluggish UI.

React Fiber introduced a new internal data structure: the **Fiber node**. Instead of a simple recursive tree, React now maintains a linked list of nodes.

Each Fiber node represents a unit of work. It contains:

  * **`stateNode`** : The actual DOM element or class component instance.
  * **`child`, `sibling`, `return`**: Pointers that form the structure, allowing React to "walk" the tree in any direction and, crucially, pause its progress.
  * **`alternate`** : A pointer to the node's counterpart in the _other_ tree (current vs. work-in-progress).



By turning the reconciliation process into a linked list, React can pause, discard, or prioritize individual units of work. If a high-priority update (like a user click) comes in, React can pause the current work, process the click, and resume the reconciliation later.

## The Two Phases: Render and Commit

The reconciliation algorithm is split into two distinct phases. Understanding the boundary between them is critical for debugging performance issues.

### 1\. The Render Phase (Asynchronous)

This phase is where the magic happens. React calls your components, compares the result with the previous output, and determines what changed.

Crucially, this phase is **pure**. React can execute this phase multiple times, pause it, or even throw it away if a newer update supersedes it. Because it is asynchronous and potentially interruptible, you should never trigger side effects (like API calls or DOM mutations) directly in your render logic.

### 2\. The Commit Phase (Synchronous)

Once React has finished calculating the "diff," it enters the commit phase. This is where the changes are applied to the real DOM.

This phase is **synchronous** and cannot be interrupted. React performs the necessary DOM operations (inserting, updating, or deleting nodes) in one go to ensure the user doesn't see a partially updated UI.

## Worked Example: Visualizing the Update

Consider a simple counter component. When the state updates, React creates a "work-in-progress" tree based on the existing Fiber nodes.
    
    
    JAVASCRIPT
    
    
    // A conceptual look at how a Fiber node update triggers reconciliation
    function updateCounter() {
      // 1. Render Phase: React compares the old Fiber node with the new one
      const newFiber = reconcileChildren(currentFiber, nextProps);
      
      // 2. Schedule: React marks the fiber as having an "Effect" (e.g., Update)
      newFiber.flags |= Update;
      
      // 3. Commit Phase: React walks the list of fibers with flags and updates the DOM
      commitWork(newFiber);
    }

When you call `setState`, React doesn't immediately touch the DOM. It schedules an update on the Fiber node. The reconciliation algorithm traverses the tree, compares the "current" tree with the "work-in-progress" tree, and creates a "list of effects." Only when it reaches the commit phase does it apply those effects to the browser.

## Hands-on Exercise: Identifying Phase Boundaries

In your current project, open your main application component. Add a `console.log` inside your component body and another inside a `useLayoutEffect`.

  1. **Observe the render phase:** Every time the state updates, your component body logs. This is the **render phase**.
  2. **Observe the commit phase:** The `useLayoutEffect` logs _after_ the DOM has been updated but _before_ the browser paints.
  3. **Question:** Why might putting a heavy calculation in your component body be more harmful than putting it in `useLayoutEffect`?



_Hint: Consider that the render phase can be called multiple times, while the commit phase is the final, non-interruptible step._

## Common Pitfalls

  * **Side Effects in Render:** Never perform network requests or modify global variables directly in your function component body. Since the render phase can be interrupted or restarted, your side effects might run multiple times, leading to inconsistent state.
  * **Blocking the Main Thread:** Even though Fiber is "asynchronous," it still runs on the main thread. If you perform heavy CPU-bound tasks during the render phase, you will still block user interactions.
  * **Ignoring Keys:** When lists are involved, the reconciliation algorithm depends on keys to identify which elements changed. As discussed in [React Reconciliation: Why Keys Are Critical for List Rendering](/blog/react-reconciliation-why-keys-are-critical-for-list-rendering), using index as a key is a common mistake that forces React to re-render unnecessary nodes.



## Recap

The React Fiber architecture is the engine that allows React to be performant at scale. By splitting the work into a Render phase (asynchronous, pure) and a Commit phase (synchronous, side-effect heavy), React ensures your UI remains responsive even during complex state updates. Remember: keep your render logic pure, and leverage the commit phase for necessary DOM interactions.

Up next: We will look at how to use the browser's performance tools to visualize these phases in action: **Profiling with React DevTools.**

Work with me

### [Headless WordPress + Next.js Frontend DevelopmentKeep WordPress for content, get a lightning-fast Next.js frontend. The best of both worlds — familiar editing, modern speed.From $450](/services/headless-wordpress-nextjs-frontend-development)### [React & Next.js Dashboard / Admin UI DevelopmentA clean, data-rich dashboard UI in React or Next.js — charts, tables, and real-time data that your users will actually enjoy using.From $300](/services/react-nextjs-dashboard-admin-ui-development)

[ Back to Blog](/blog)
