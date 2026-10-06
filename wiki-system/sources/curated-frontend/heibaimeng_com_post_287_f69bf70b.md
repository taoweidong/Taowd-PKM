---
source: "https://heibaimeng.com/post/287"
title: "Vue 3 的响应式系统基础原理分析，模拟实现 reactive、ref、computed 方法 - 黑白梦"
fetched_at: "2026-10-06 12:33"
---

[全部文章](/posts/1)

# Vue 3 的响应式系统基础原理分析，模拟实现 reactive、ref、computed 方法

发布于 2026-01-10更新于 2026-01-11约 17 分钟

Vue 3 的响应式系统基于 ES6 Proxy，通过拦截对象的访问和修改，实现依赖收集与更新机制，其核心源码位于 packages/reactivity 目录。

学习响应式原理、阅读源码，可以使得在用响应式数据时心中有数，也可在 Vue 版本更新里识别版本差异的影响。

## 基础语法

### Proxy 概念

Proxy 用于创建一个代理对象，可以拦截并重新定义对目标对象的基本操作。传参：

  * target : 要被代理的目标对象
  * handler : 一个对象，定义了代理的行为，包含拦截操作的方法



handler 用于拦截对象的基本操作：

  * get ：读取属性时收集依赖
  * set ：设置属性时触发更新
  * deleteProperty ：删除属性时触发更新
  * has ：检查属性存在时收集依赖
  * ownKeys ：获取所有键时收集依赖



get 拦截器 - 拦截属性读取：
    
    
    const obj = { name: 'Vue', version: 3.5 }
    const proxy = new Proxy(obj, {
      get(target, key, receiver) {
        console.log(`访问属性: ${key}`)
        return Reflect.get(target, key, receiver)
      }
    })
    
    console.log(proxy.name) 
    console.log(proxy.version) 

set 拦截器 - 拦截属性设置：
    
    
    const obj = { count: 0 }
    const proxy = new Proxy(obj, {
      set(target, key, value, receiver) {
        console.log(`设置属性: ${key} = ${value}`)
        return Reflect.set(target, key, value, receiver)
      }
    })
    
    proxy.count = 5 
    proxy.name = 'Vue' 

对比 Vue 2 使用的 defineProperty ，Proxy 有许多好处，如整个对象维度监听而不是具体属性，新属性不需要 Vue.set 这样的语法；可以监听“新增 / 删除属性”；可直接拦截数组索引、length、支持 Map / Set 等。

### Reflect 概念

Reflect 是一个内置对象，提供拦截 JavaScript 操作的方法。这些方法与 proxy handler 的方法相同。

get 方法，等同于 obj.name，但更安全：
    
    
    const obj = { name: 'Vue', version: 3.5 }
    console.log(Reflect.get(obj, 'name')) 
    console.log(Reflect.get(obj, 'version')) 

set 方法：
    
    
    const obj = { count: 0 }
    Reflect.set(obj, 'count', 5)
    console.log(obj.count) 
    
    Reflect.set(obj, 'name', 'Vue')
    console.log(obj.name) 

### receiver 参数（了解）

receiver 参数用于保证正确上下文：

  * 在 Proxy 的 get(target, key, receiver) 拦截器中，receiver 是最初被调用的对象，通常是 Proxy 实例本身或继承自 Proxy 的对象。
  * 在 Reflect 的 get(target, key, receiver) 拦截器中，receiver 的作用是：如果 target 对象中指定了 getter， receiver 则为 getter 调用时的this值。



Vue 源码中有这一句：`isRef(target) ? target : receiver` ，当被访问的对象本身是 ref 时，不使用 proxy 作为 receiver，而是使用 ref 自身，避免 this 绑定到代理对象从而破坏 ref 的语义，确保 ref 在方法调用中的行为保持一致。

### WeakMap 概念

WeakMap 是一种键值对的集合，优势 ：

  * 弱引用 ：当原始对象被垃圾回收时，对应的映射也会自动被清理，防止内存泄漏
  * 键值对存储 ：以对象作为键，存储对应的代理对象或依赖映射



在 Vue 3 中，WeakMap 被广泛用于存储各种映射关系。

## 结合 Proxy 和 Reflect 实现 reactive 方法

reactive 方法和 ref 方法都可以创建响应式对象，对于非简单类型数据， ref 内部也是调用了 reactive 来创建。

这里实现一版最基础的 reactive 方法：
    
    
    function reactive(target) {
      return new Proxy(target, {
        get(target, key, receiver) {
          
          track(target, key)
          
          return Reflect.get(target, key, receiver)
        },
        
        set(target, key, value, receiver) {
          const oldValue = target[key]
          const result = Reflect.set(target, key, value, receiver)
          
          
          if (oldValue !== value) {
            trigger(target, key)
          }
          
          return result
        }
      })
    }

后续实现**依赖收集和触发更新** 函数，先打印：
    
    
    function track(target, key) {
      console.log(`收集依赖: ${target.constructor.name}[${key}]`)
    }
    
    function trigger(target, key) {
      console.log(`触发更新: ${target.constructor.name}[${key}]`)
    }

使用示例：
    
    
    const obj = reactive({ count: 0 })
    console.log(obj.count) 
    obj.count = 5 

## 依赖收集和触发更新

在 Vue 源码里，track 方法和 trigger 方法做在了 dep.ts 文件中，用于记录和执行 effect 副作用方法。

### 记录依赖关系

依赖收集，需要记录当前活动的副作用函数（effect）与被访问的响应式数据之间的依赖关系。

  * targetMap 属性储存映射关系，key 为 target ，值为对象的字段依赖映射 depsMap
  * depsMap 存一个普通 Map 结构，键为对象被操作的字段，值为该属性的 effect 集合
  * depsMap 的 value 是 Dep 对象，是一个双向链表结构，用于记录依赖，这里使用 Set 做简化效果



targetMap 的结构如下：
    
    
    targetMap = {
      [原始对象1]: {
        '属性名1': Set { effect1, effect2, ... },
        '属性名2': Set { effect3, effect4, ... },
      },
      [原始对象2]: {
        '属性名1': Set { effect5, ... },
      }
    }

### track 依赖收集

如上文所述， track 在 proxy 对象的 get 中触发。模拟一个简化的 track 依赖收集：
    
    
    const targetMap = new WeakMap()
    
    function track(target, key) {
      
      if (!activeEffect) return
    
      
      let depsMap = targetMap.get(target)
      if (!depsMap) {
        targetMap.set(target, (depsMap = new Map()))
      }
      
      let dep = depsMap.get(key)
      if (!dep) {
        depsMap.set(key, (dep = new Set()))
      }
      
      dep.add(activeEffect)
    }

### trigger 触发更新

trigger 触发更新，当 proxy 的 set 调用，当响应式数据发生变化时，通知所有依赖该数据的副作用函数重新执行。
    
    
    function trigger(target, key) {
      
      const depsMap = targetMap.get(target)
      if (!depsMap) {
        return
      }
      
      
      const effects = depsMap.get(key)
      if (effects) {
        
        effects.forEach(effect => {
          effect() 
        })
      }
    }

### effect 副作用函数

模拟 effect 副作用函数：

  * 创建一个 activeEffect 变量，用于 track 时确保当前有活动的副作用函数，避免重复监听和无意义的监听
  * 当在 effect 副作用函数执行时会记录为 activeEffect ，然后执行 回调函数
  * 在回调函数中访问了 proxy 某个属性时，调用它的 get ，会触发 track，把 activeEffect 记录为该属性的依赖
  * 访问多个属性时，activeEffect存在，直到回调函数执行完毕，销毁 activeEffect
  * 实际源码中的 activeEffect 是 activeSub ，还有另一个检查条件 shouldTrack 是否允许跟踪


    
    
    let activeEffect = null
    function effect(fn) {
      const effectFn = () => {
        activeEffect = effectFn  
        fn()  
        activeEffect = null  
      }
      effectFn()  
    }

使用 effect 函数：
    
    
    const obj = obj({ a: 1, b: 2 })
    let sum
    effect(() =>  {
      sum = obj.a + obj.b
    })
    let product
    effect(() =>  {
      product = obj.a * obj.b
    })

响应式更新使用效果：
    
    
    console.log(sum, product) 
    
    reactiveObj.a = 5
    console.log(sum, product) 
    
    reactiveObj.b = 10
    console.log(sum, product) 

## 模拟 ref 实现

ref 实现位于 ref.ts 文件，实际创建 ref 时会创建一个 RefImpl 类对象：

  * `_value` 属性判断如果不是简单类型，会创建为 reactive ，普通值直接记录
  * 而 reactive 内部会做一个 key 为原始值，value 为 Proxy 值的 WeekMap 缓存，会发现 ref(arr) 的 value 和 reactive(arr) 是全等的
  * 所以复杂类型时，通过两种方式创建响应式数据，本质上无区别，不存在好坏对错之分
  * ref 的 dep 属性也是 Dep 对象，跟 track 方法里创建到 depsMap 里的一样
  * 使用 get 和 set 来对外暴露 value 属性，在 get 里就能执行 dep.track ，set 里执行 dep.trigger
  * Vue 3.5 源码中 reactive 调用的 track 方法创建的 depsMap 里的属性值，和 ref 里的 dep 属性都是 Dep 对象，二者其实是独立的，dep 不会调 reactive 调那个外部的 track 方法，只是把收集依赖（即 demo 中的把函数加到set），和执行的逻辑（即demo里调用set里的所有方法），封装起来在 Dep 对象的 track 和 trigger 方法里。



实现一个 ref 方法，暂不考虑复杂类型，且为了简化，利用当前对象和value属性调用前面的 track 和 trigger 方：
    
    
    function ref(raw) {
      let _value = raw
      const res = {
        get value() {
          track(res, 'value')
          return _value
        },
        set value(x) {
         if (_value !== x) {
          _value = x
          trigger(res, 'value')
         }
        }
      }
      return res
    }

将前面 demo 的 b 属性改为通过 ref 创建：
    
    
    const reactiveObj = reactive({ a: 1 })
    const b = ref(2)
    let sum
    effect(() => {
      sum = reactiveObj.a + b.value
    })
    let product
    effect(() => {
      product = reactiveObj.a * b.value
    })
    
    console.log(sum, product) 
    
    reactiveObj.a = 5
    console.log(sum, product) 
    
    b.value = 10
    console.log(sum, product) 

## 模拟 computed 实现

computed 实现位于 computed.ts 文件，实际创建 ComputedRefImpl 对象：

  * 只传入函数时，作为 getter 处理，也可以传入 setter
  * 内部把相当于前面调用 effect 并记录值的方法封装了起来
  * 内部也有 `_value` 和 dep 属性，跟 ref 类似，也需要进行依赖收集



模拟一个简单的实现，只考虑 getter：
    
    
    function computed(getter) {
      let _value
    
      const res = {
        get value() {
          track(res, 'value')
          return _value
        }
      }
      effect(() => {
        const v = getter()
        if (v !== _value) {
          _value = v
          trigger(res, 'value')
        }
      })
      return res
    }

使用为：
    
    
    const reactiveObj = reactive({ a: 1 })
    const b = ref(2)
    let sum = computed(() => reactiveObj.a + b.value)
    let product = computed(() => reactiveObj.a * b.value)
    
    console.log(sum.value, product.value) 
    
    reactiveObj.a = 5
    console.log(sum.value, product.value) 
    
    b.value = 10
    console.log(sum.value, product.value) 

## 完整代码

这个 demo 实现了 Vue 响应式的观察者/发布订阅的最小模型，被观察者是数据的“属性级别状态”，观察者是 effect 副作用方法。观察关系在 effect 执行期间，通过读取数据自动建立（如 Proxy 对象 get 方法、ref 返回对象中的 get value 方法），当状态变化时，被观察者通知所有观察者重新执行，从而完成响应式更新。

在实际的 Vue 源码中，还需要处理各种复杂类型；需要处理 effect 嵌套场景，非单一 activeEffect；依赖需要进行清理；computed 需要懒执行；effect需调度执行等等。可参照 Vue 源码进行阅读，从而加深对 Vue 响应式实现的理解。

以上所有实现，整体代码如下：
    
    
    function reactive(target) {
      return new Proxy(target, {
        get(target, key, receiver) {
          
          track(target, key)
          
          return Reflect.get(target, key, receiver)
        },
        
        set(target, key, value, receiver) {
          const oldValue = target[key]
          const result = Reflect.set(target, key, value, receiver)
          
          
          if (oldValue !== value) {
            trigger(target, key)
          }
          
          return result
        }
      })
    }
    
    
    
    const targetMap = new WeakMap()
    
    let activeEffect = null
    function track(target, key) {
      
      if (!activeEffect) return
    
      
      let depsMap = targetMap.get(target)
      if (!depsMap) {
        targetMap.set(target, (depsMap = new Map()))
      }
      
      let dep = depsMap.get(key)
      if (!dep) {
        depsMap.set(key, (dep = new Set()))
      }
      
      dep.add(activeEffect)
    }
    function trigger(target, key) {
      
      const depsMap = targetMap.get(target)
      if (!depsMap) {
        return
      }
      
      
      const effects = depsMap.get(key)
      if (effects) {
        
        effects.forEach(effect => {
          effect() 
        })
      }
    }
    
    function effect(fn) {
      const effectFn = () => {
        activeEffect = effectFn  
        fn()  
        activeEffect = null  
      }
      effectFn()  
    }
    
    
    function ref(raw) {
      let _value = raw
      const res = {
        get value() {
          track(res, 'value')
          return _value
        },
        set value(x) {
         if (_value !== x) {
          _value = x
          trigger(res, 'value')
         }
        }
      }
      return res
    }
    
    function computed(getter) {
      let _value
    
      const res = {
        get value() {
          track(res, 'value')
          return _value
        }
      }
      effect(() => {
        const v = getter()
        if (v !== _value) {
          _value = v
          trigger(res, 'value')
        }
      })
      return res
    }
    
    const reactiveObj = reactive({ a: 1 })
    const b = ref(2)
    let sum = computed(() => reactiveObj.a + b.value)
    let product = computed(() => reactiveObj.a * b.value)
    let view = computed(() => `sum: ${sum.value}, product: ${product.value}`)
    
    console.log(view.value)  
    
    reactiveObj.a = 5
    console.log(view.value) 
    
    b.value = 10
    console.log(view.value)  
