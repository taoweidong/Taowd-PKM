---
source: "https://cloud.tencent.com/developer/article/2600752"
title: "Vue3 响应式原理深度解析：Proxy 实现与依赖收集逻辑-腾讯云开发者社区-腾讯云"
fetched_at: "2026-10-06 12:33"
---

[社区首页](https://cloud.tencent.com/developer) >[专栏](https://cloud.tencent.com/developer/column) >Vue3 响应式原理深度解析：Proxy 实现与依赖收集逻辑

### Vue3 响应式原理深度解析：Proxy 实现与依赖收集逻辑

在这里插入图片描述

面向前端工程师的系统性解析：从设计目标到数据结构、从拦截细节到依赖收集与调度，再到 `ref`、`computed` 与数组、Map/Set 等容器的特殊处理。文章配套一个可运行的精简版响应式系统，帮助在源码级别建立完整心智模型。

#### TL;DR

  * Vue3 使用 `Proxy` \+ `WeakMap` 实现响应式，替代 Vue2 的 `defineProperty`
  * 依赖收集通过 `effect` 执行时的访问轨迹完成，核心是 `track` 与 `trigger`
  * 数据结构：`targetMap: WeakMap<object, Map<key, Set<effect>>>`
  * 细粒度触发：区分 `set`、`add`、`delete` 与数组 `length`、迭代依赖
  * `computed` 基于懒执行的 `effect`，用 `dirty` 标记与调度器缓存结果
  * `ref` 以对象包装原始值，通过 `get/set` 触发依赖
  * 性能关键：只在被访问的键上收集依赖；用 `WeakMap` 避免内存泄漏；按需调度



* * *

#### 设计目标

  * 精准依赖收集：仅对访问过的属性建立依赖，减少无效更新
  * 一致语义：对象、数组、Map/Set 等统一遵循“读时收集、写时触发”
  * 良好可拓展性：支持 `readonly`、`shallow`、`custom scheduler`
  * 可维护性：核心概念内聚，便于调试与定位问题



#### 核心数据结构

复制
    
    
    type EffectFn = (() => any) & { deps?: Set<Set<EffectFn>>; scheduler?: (job: () => void) => void; lazy?: boolean; };
    
    const targetMap = new WeakMap<object, Map<any, Set<EffectFn>>>();
    let activeEffect: EffectFn | null = null;
    const effectStack: EffectFn[] = [];
    
    const ITERATE_KEY = Symbol('iterate');
    const MAP_KEY_ITERATE_KEY = Symbol('map_key_iterate');

#### effect 与依赖收集

  * `effect(fn)` 负责在执行过程中记录所有访问到的响应式属性
  * `track(target, key)` 将当前 `activeEffect` 放入 `targetMap[target][key]` 的 `Set`
  * `trigger(target, key, type)` 找到依赖集合并逐个执行或交由调度器处理
  * 通过 `effectStack` 支持嵌套 `effect` 与正确的 `activeEffect` 恢复
  * 通过清理旧依赖避免“脏依赖”导致的错误触发



复制
    
    
    function cleanup(effect: EffectFn) {
      if (!effect.deps) return;
      for (const dep of effect.deps) dep.delete(effect);
      effect.deps.clear();
    }
    
    export function effect(fn: () => any, options: { scheduler?: (job: () => void) => void; lazy?: boolean } = {}): EffectFn {
      const e: EffectFn = function wrappedEffect() {
        cleanup(e);
        activeEffect = e;
        effectStack.push(e);
        try {
          return fn();
        } finally {
          effectStack.pop();
          activeEffect = effectStack[effectStack.length - 1] || null;
        }
      } as EffectFn;
      e.deps = new Set();
      e.scheduler = options.scheduler;
      e.lazy = !!options.lazy;
      if (!e.lazy) e();
      return e;
    }
    
    function track(target: object, key: any) {
      if (!activeEffect) return;
      let depsMap = targetMap.get(target);
      if (!depsMap) {
        depsMap = new Map();
        targetMap.set(target, depsMap);
      }
      let dep = depsMap.get(key);
      if (!dep) {
        dep = new Set();
        depsMap.set(key, dep);
      }
      if (!dep.has(activeEffect)) {
        dep.add(activeEffect);
        activeEffect.deps!.add(dep);
      }
    }
    
    function trigger(target: object, key: any, type: 'set' | 'add' | 'delete') {
      const depsMap = targetMap.get(target);
      if (!depsMap) return;
      const effects = new Set<EffectFn>();
      const addEffects = (dep?: Set<EffectFn>) => {
        if (!dep) return;
        for (const e of dep) effects.add(e);
      };
      addEffects(depsMap.get(key));
      if (type === 'add' || type === 'delete') addEffects(depsMap.get(ITERATE_KEY));
      const run = (e: EffectFn) => {
        if (e.scheduler) e.scheduler(() => e());
        else e();
      };
      for (const e of effects) run(e);
    }

#### Proxy 拦截与 handler 设计

  * `get` 中进行 `track`，并返回属性值；对对象值递归包装以保持深度响应
  * `set` 区分新增与修改，从而决定是否触发迭代依赖
  * `has`、`ownKeys` 读操作也需要 `track`，迭代依赖采用 `ITERATE_KEY`
  * 对数组与 Map/Set 等容器在迭代与变更时进行特殊处理



复制
    
    
    const reactiveMap = new WeakMap<object, any>();
    
    export function reactive<T extends object>(obj: T): T {
      const existing = reactiveMap.get(obj);
      if (existing) return existing;
      const proxy = new Proxy(obj, {
        get(target, key, receiver) {
          const res = Reflect.get(target, key, receiver);
          track(target, key);
          if (typeof res === 'object' && res !== null) return reactive(res as object) as any;
          return res;
        },
        set(target, key, value, receiver) {
          const hadKey = Object.prototype.hasOwnProperty.call(target, key);
          const oldVal = (target as any)[key];
          const result = Reflect.set(target, key, value, receiver);
          if (!hadKey) trigger(target, key, 'add');
          else if (oldVal !== value) trigger(target, key, 'set');
          return result;
        },
        has(target, key) {
          const res = Reflect.has(target, key);
          track(target, key);
          return res;
        },
        ownKeys(target) {
          track(target, ITERATE_KEY);
          return Reflect.ownKeys(target);
        },
        deleteProperty(target, key) {
          const hadKey = Object.prototype.hasOwnProperty.call(target, key);
          const result = Reflect.deleteProperty(target, key);
          if (hadKey && result) trigger(target, key, 'delete');
          return result;
        }
      });
      reactiveMap.set(obj, proxy);
      return proxy as T;
    }

#### ref 与 computed 的实现

  * `ref` 将原始值包成对象，在 `value` 的 `get/set` 上 `track/trigger`
  * `computed` 用懒执行的 `effect`，首次访问求值，后续由依赖变更时标记为 `dirty`



复制
    
    
    export function ref<T>(raw: T) {
      const r = {
        get value() {
          track(r, 'value');
          return raw;
        },
        set value(v: T) {
          raw = v;
          trigger(r, 'value', 'set');
        }
      };
      return r;
    }
    
    export function computed<T>(getter: () => T) {
      let cached: T;
      let dirty = true;
      const runner = effect(() => {
        cached = getter();
      }, { lazy: true, scheduler: job => job() });
      return {
        get value() {
          if (dirty) {
            runner();
            dirty = false;
          }
          track(this, 'value');
          return cached!;
        }
      };
    }

#### 可运行的最小完整示例

复制
    
    
    // 基本使用
    const state = reactive({ count: 0, nested: { a: 1 } });
    const doubled = computed(() => state.count * 2);
    
    effect(() => {
      document.querySelector('#app')!.textContent = `count=${state.count}, doubled=${doubled.value}`;
    });
    
    setInterval(() => {
      state.count++;
    }, 1000);

#### 迭代依赖与数组/容器细节

  * 数组：`length` 变化会影响索引依赖；迭代依赖通过 `ITERATE_KEY`
  * Map/Set：键迭代与值迭代分别跟踪，可用 `MAP_KEY_ITERATE_KEY` 与 `ITERATE_KEY`
  * 容器方法需要“仪器化”，例如 `set.add`、`map.set` 在内部调用 `trigger`
  * 迭代读取（如 `for...in`、`for...of`、`Object.keys`、`ownKeys`）都需要 `track(ITERATE_KEY)`



#### 调度器与批处理

  * `effect` 可选 `scheduler`，用于将同步触发改为异步或批处理
  * 常见实现是微任务队列，将多次触发合并后统一执行



复制
    
    
    const queue = new Set<Function>();
    let flushing = false;
    function queueJob(job: Function) {
      queue.add(job);
      if (!flushing) {
        flushing = true;
        Promise.resolve().then(() => {
          for (const j of queue) j();
          queue.clear();
          flushing = false;
        });
      }
    }
    
    const state2 = reactive({ x: 0 });
    const e2 = effect(() => {
      console.log(state2.x);
    }, { scheduler: queueJob });
    state2.x = 1;
    state2.x = 2;

#### 性能与内存管理

  * `WeakMap` 避免持有对已释放对象的强引用，降低泄漏风险
  * 精准依赖收集减少无效更新；避免在未访问的属性上建立依赖
  * 清理旧依赖确保触发集合不膨胀；对高频更新用调度器批处理



#### 常见坑与排查

  * 未在 `effect` 中访问响应式数据，导致未收集依赖
  * 忽略迭代依赖，增删属性或容器项不触发更新
  * 忽略数组 `length` 与索引的耦合，更新行为不一致
  * 循环触发与递归更新，需借助调度器或状态分离
  * 深浅响应不当：`shallowReactive` 只包装一层；`readonly` 禁止写入



#### 与 Vue3 源码的差异与拓展

  * 示例为教学版，省略了 `readonly`、`shallow`、`toRaw`、`markRaw` 等
  * 未覆盖 Map/Set 的完整仪器化、`TrackOpTypes`/`TriggerOpTypes` 的枚举细分
  * 源码对数组、TypedArray、内建集合均做了更细粒度优化与边界处理



#### 总结

Vue3 响应式的核心在于“读时收集、写时触发”这条主线。以 `Proxy` 为载体、以 `WeakMap → Map → Set` 为依赖索引，辅以 `effect` 栈与调度器策略，既保证正确性与性能，又为容器类型与高级特性预留扩展空间。理解这些细节后，能够在业务中更精准地使用 `ref`、`reactive` 与 `computed`，在复杂场景中定位与优化更新行为。

本文参与 [腾讯云自媒体同步曝光计划](https://cloud.tencent.com/developer/support-plan)，分享自作者个人站点/博客。

原始发表：2025-12-11，如有侵权请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除

[vue3](https://cloud.tencent.com/developer/tag/16865)

[数组](https://cloud.tencent.com/developer/tag/17457)

[响应式](https://cloud.tencent.com/developer/tag/17512)

[原理](https://cloud.tencent.com/developer/tag/17566)

[proxy](https://cloud.tencent.com/developer/tag/15422)

目录

  *     *     *     *     *     *     *     *     *     *     *     *     *     * 


[问题归档](https://cloud.tencent.com/developer/ask/archives.html)[专栏文章](https://cloud.tencent.com/developer/column/archives.html)[快讯文章归档](https://cloud.tencent.com/developer/news/archives.html)[关键词归档](https://cloud.tencent.com/developer/information/all.html)[开发者手册归档](https://cloud.tencent.com/developer/devdocs/archives.html)[开发者手册 Section 归档](https://cloud.tencent.com/developer/devdocs/sections_p1.html)
