---
source: "https://www.cnblogs.com/wgwyanfs/p/20159999"
title: "Spring三级缓存：循环依赖的优雅解决之道 - wgwyanfs - 博客园"
fetched_at: "2026-10-06 12:33"
---

#  [ Spring三级缓存：循环依赖的优雅解决之道 ](https://www.cnblogs.com/wgwyanfs/p/20159999 "发布于 2026-05-25 20:12")

在大型Java项目中，循环依赖是一个常见但棘手的问题。Spring通过一套精巧的三级缓存机制，在Bean的生命周期中动态化解这种依赖闭环，保证了容器的高效与稳定。本文将从实战角度，深度剖析这一机制的设计思想与实现原理。

## 一、什么是循环依赖？

循环依赖指的是两个或多个Bean之间相互引用，形成闭环。最经典的场景如：
    
    
    @Component
    class A {
        @Autowired
        private B b;
    }
    @Component
    class B {
        @Autowired
        private A a;
    }

如果没有特殊机制，Spring在创建A时会发现需要B，于是去创建B；创建B时又发现需要A，从而陷入无限递归，最终抛出异常。这就像在Python或JavaScript中两个模块相互导入一样，会导致死锁或栈溢出。

> ❌ Bean 创建会直接死循环

## 二、Spring创建Bean的关键流程

要理解三级缓存，必须先掌握Spring创建Bean的核心步骤。整个过程大致分为：
    
    
    doCreateBean()
       ↓
    createBeanInstance()   // 实例化（调用构造函数）
       ↓
    populateBean()         // 依赖注入
       ↓
    initializeBean()       // 初始化（AOP 也在这里）

**关键概念：** 实例化（Instance）不等于初始化（Initialize）。实例化只是通过反射创建了一个“空壳对象”，此时属性尚未填充，AOP代理也未生成。这就像在C++中声明一个对象但不调用构造函数一样，内存已分配但内容未就绪。

### 2.1 核心入口：doCreateBean()

Spring创建Bean的核心方法位于：
    
    
    AbstractAutowireCapableBeanFactory#doCreateBean

其主要流程为：
    
    
    protected Object doCreateBean(...) {
        // 1️⃣ 实例化 Bean（调用构造函数）
        Object beanInstance = createBeanInstance(beanName, mbd, args);
        // 2️⃣ 提前暴露（解决循环依赖关键）
        if (earlySingletonExposure) {
            addSingletonFactory(beanName,
                () -> getEarlyBeanReference(beanName, mbd, beanInstance));
        }
        // 3️⃣ 依赖注入（填充属性）
        populateBean(beanName, mbd, instanceWrapper);
        // 4️⃣ 初始化（AOP 在这里发生）
        Object exposedObject = initializeBean(beanName, beanInstance, mbd);
        // 5️⃣ 放入一级缓存
        addSingleton(beanName, exposedObject);
        return exposedObject;
    }

### 2.2 实例化（createBeanInstance）
    
    
    createBeanInstance()

这一步主要完成：通过反射调用构造函数，创建一个空壳对象。此时Bean的状态如下：

状态| 是否完成  
---|---  
对象创建| ✅  
属性注入| ❌  
AOP代理| ❌  
  
### 2.3 提前暴露
    
    
    addSingletonFactory(beanName,
        () -> getEarlyBeanReference(...))

⚠️ 这一步是解决循环依赖的**核心** 。作用是把Bean包装成一个 `ObjectFactory` ，放入三级缓存。这意味着Bean在尚未完成初始化时，就已经可以“被引用”了。

### 2.4 依赖注入
    
    
    populateBean()

执行 `@Autowired` 给字段赋值。注意：此时如果发现依赖的Bean尚未创建，就会触发递归创建过程，循环依赖正是在这个阶段被检测到的。

> ❗这里只是“赋引用”，不会调用方法

## 三、Spring三级缓存机制详解

三级缓存的核心实现位于 `DefaultSingletonBeanRegistry` 类中，本质上是三个Map，用来存储不同阶段的Bean。源码如下：
    
    
    // 一级缓存：存放最终完成初始化的 Bean
    private final Map singletonObjects = new ConcurrentHashMap<>(256);
    // 二级缓存：存放提前暴露的 Bean（未完成初始化）
    private final Map earlySingletonObjects = new HashMap<>(16);
    // 三级缓存：存放 ObjectFactory，用于生成早期 Bean
    private final Map> singletonFactories = new HashMap<>(16);

从结构上看：

  * **一级缓存（singletonObjects）** ：存储完全初始化好的Bean，是最终态对象。
  * **二级缓存（earlySingletonObjects）** ：存储已实例化但尚未初始化的早期对象。
  * **三级缓存（singletonFactories）** ：存储的不是Bean本身，而是可以生成Bean的工厂（`ObjectFactory`）。



这种设计不是简单的多级缓存，而是围绕Bean生命周期进行分层控制，为后续解决循环依赖打下基础。

### 3.2 三级缓存的工作机制

当Spring创建一个Bean时，会在“实例化之后、依赖注入之前”做一次关键操作：将当前Bean以工厂的形式放入三级缓存。
    
    
    addSingletonFactory(beanName,
        () -> getEarlyBeanReference(beanName, mbd, bean));

Spring并没有直接把Bean放入缓存，而是包装成了一个 `ObjectFactory` 。真正的Bean是“延迟获取”的，只有在发生循环依赖时，才会通过这个工厂去生成对象。

在依赖注入过程中，当出现A依赖B、B又依赖A的情况时，Spring会递归创建Bean。容器开始创建A时，先完成实例化，然后将A以 `ObjectFactory` 的形式放入三级缓存 `singletonFactories` 中。接着在执行 `populateBean("A")` 时发现A依赖B，于是调用 `getBean("B")` 开始创建B；B在实例化完成后也会被放入三级缓存。在B的依赖注入过程中，发现其依赖A，此时再次调用 `getBean("A")` ，进入 `getSingleton("A")` 的查找逻辑：首先从一级缓存 `singletonObjects.get("A")` 获取失败，接着检查A正处于创建过程中（`isSingletonCurrentlyInCreation("A")` 为true），于是从二级缓存查找，如果仍未命中，则从三级缓存中获取对应的 `ObjectFactory` ，执行其 `getObject()` 方法，返回A的一个“早期引用”（可能已是代理对象）。随后这个早期对象被放入二级缓存 `earlySingletonObjects` ，并从三级缓存中移除，最终返回给B使用。这样，B完成依赖注入并初始化，接着回到A的创建流程，A也顺利完成后续初始化，最终放入一级缓存。

> 一个小的注意点：当 Bean 完整创建后放入一级缓存时，会同时清理二级和三级缓存中的对应数据

其中，`getSingleton(beanName)` 方法的核心逻辑如下：
    
    
    protected Object getSingleton(String beanName, boolean allowEarlyReference) {
        // 1️⃣ 先从一级缓存获取
        Object singletonObject = singletonObjects.get(beanName);
        // isSingletonCurrentlyInCreation 用来判断 这个 Bean 现在是不是“正在创建中”
        if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
            // 2️⃣ 再从二级缓存获取
            singletonObject = earlySingletonObjects.get(beanName);
            // 3️⃣ 如果还没有，从三级缓存获取
            if (singletonObject == null && allowEarlyReference) {
                ObjectFactory singletonFactory = singletonFactories.get(beanName);
                if (singletonFactory != null) {
                    // ⭐ 执行工厂，获取早期引用
                    singletonObject = singletonFactory.getObject();
                    // 放入二级缓存
                    earlySingletonObjects.put(beanName, singletonObject);
                    // 删除三级缓存
                    singletonFactories.remove(beanName);
                }
            }
        }
        return singletonObject;
    }

整个查找过程遵循“一级 → 二级 → 三级”的顺序。当从三级缓存获取到对象后，会立即放入二级缓存，并删除三级缓存中的对应项。这个过程本质上完成了“从工厂到对象”的转换，实现了Bean的提前暴露。
    
    
    三级缓存（ObjectFactory） → 二级缓存（早期对象） → 一级缓存（最终对象）

### 3.3 ObjectFactory与AOP的关系（为什么必须三级缓存）

很多人会问：为什么不能直接用二级缓存？答案就在 `ObjectFactory` 上。

> ❓ 为什么不能直接用二级缓存？为什么一定要三级缓存？

在三级缓存中，Spring存放的是一个函数式接口：
    
    
    ObjectFactory singletonFactory

它最终会调用：
    
    
    getEarlyBeanReference(beanName, mbd, bean);

该方法源码如下：
    
    
    protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
        Object exposedObject = bean;
        for (BeanPostProcessor bp : beanPostProcessors) {
            if (bp instanceof SmartInstantiationAwareBeanPostProcessor) {
                exposedObject = bp.getEarlyBeanReference(exposedObject);
            }
        }
        return exposedObject;
    }

关键在于 `getEarlyBeanReference()` 方法内部会执行一系列 `BeanPostProcessor` ，而AOP的代理创建逻辑正是在这里触发的。也就是说：从三级缓存中拿到的对象，很可能已经是一个代理对象，而不是原始Bean。

> ⭐ **延迟决定返回的是原始对象，还是代理对象**

如果只有二级缓存，那么在Bean刚实例化后就必须立即放入缓存，此时还无法判断该Bean是否需要被AOP增强，从而导致：注入的是原始对象，最终使用的却是代理对象，造成引用不一致问题。而通过三级缓存中的 `ObjectFactory` ，Spring可以在“真正需要的时候”再去决定返回哪种对象，从而保证：循环依赖可以被解决，AOP代理不会失效，所有引用保持一致。

[AFFILIATE_SLOT_1] 

### 3.4 因为循环依赖提前生成了代理对象，后续是否会再生成一次？

在循环依赖场景下，如果某个Bean在 `getEarlyBeanReference()` 阶段已经被AOP代理，那么后续在初始化阶段（`initializeBean()`）中**不会再次生成代理对象** ，但相关的后置处理流程仍然会执行。Spring通过内部机制避免了“重复代理”。

具体来说，在提前暴露阶段，Spring会调用 `SmartInstantiationAwareBeanPostProcessor#getEarlyBeanReference()` ，此时AOP的核心实现（如 `AbstractAutoProxyCreator` ）会判断当前Bean是否需要代理，如果需要，则直接创建代理对象并返回。同时，该处理器将当前Bean记录到一个缓存集合中（通常是 `earlyProxyReferences` ）。当后续执行到初始化阶段的 `postProcessAfterInitialization()` 时，会再次进入AOP的处理逻辑，但此时会先检查当前Bean是否已经存在于 `earlyProxyReferences` 中，如果存在，则直接返回，不再创建新的代理对象。

因此，从执行流程上看是：
    
    
    提前暴露阶段：可能创建代理（第一次，也是唯一一次）
    初始化阶段：仍然会走 AOP 流程，但不会重复创建代理

这样设计的核心目的在于：

  * ✅ 保证代理对象只创建一次（避免性能损耗）
  * ✅ 保证循环依赖中注入的是“最终形态对象”（而不是原始对象）
  * ✅ 保证整个生命周期中引用一致，不会出现前后对象不一致的问题



> 注意：在循环依赖场景下，Spring 仅在提前暴露阶段执行 AOP 代理创建逻辑，而不会执行完整的初始化流程，真正的初始化（如 Aware 回调和 init 方法）仍然在后续 中完成。
> 
> **再额外说明一点，Spring AOP 默认只能增强：方法级别（Method Level）**

### 3.5 Spring容器创建Bean的过程中如何判断产生了循环依赖

#### 3.5.1 循环依赖的判定本质

Spring并不存在一个“预先分析依赖关系图”的过程。循环依赖是在Bean创建过程中**动态发现** 的。其核心判定标准是：

> **当一个 Bean 在创建过程中，再次被请求获取时，即可认为发生了循环依赖。**

这一机制依赖于Spring内部对“正在创建的Bean”的状态记录。

#### 3.5.2 正在创建集合（核心判断依据）

Spring使用一个集合来标识当前正在创建的Bean：
    
    
    private final Set singletonsCurrentlyInCreation = new HashSet<>();

当一个Bean开始创建时，会被加入该集合：
    
    
    protected void beforeSingletonCreation(String beanName) {
        singletonsCurrentlyInCreation.add(beanName);
    }

当Bean创建完成后，会被移出：
    
    
    protected void afterSingletonCreation(String beanName) {
        singletonsCurrentlyInCreation.remove(beanName);
    }

因此，这个集合本质上表示：

> **哪些 Bean 还没有初始化完成**

#### 3.5.3 循环依赖的触发点（getBean调用）

在依赖注入过程中，Spring会递归调用 `getBean()` 来获取依赖对象：
    
    
    protected Object doGetBean(String name) {
        if (isSingletonCurrentlyInCreation(name)) {
            // 关键判断点
        }
    }

判断逻辑如下：
    
    
    public boolean isSingletonCurrentlyInCreation(String beanName) {
        return this.singletonsCurrentlyInCreation.contains(beanName);
    }

含义是：

> 如果当前要获取的 Bean，已经在“正在创建集合”中，就说明发生了循环依赖

#### 3.5.4 检测到循环依赖后的处理机制

当检测到循环依赖后，Spring并不会立即报错，而是尝试通过三级缓存解决：
    
    
    Object singleton = getSingleton(beanName, true);

核心逻辑为：
    
    
    // 位于DefaultSingletonBeanRegistry#getSingleton(String beanName,
     boolean allowEarlyReference)
    if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
        singletonObject = earlySingletonObjects.get(beanName);
        if (singletonObject == null) {
            ObjectFactory factory = singletonFactories.get(beanName);
            if (factory != null) {
                singletonObject = factory.getObject(); //  提前引用
                earlySingletonObjects.put(beanName, singletonObject);
                singletonFactories.remove(beanName);
            }
        }
    }

关键点：从三级缓存获取ObjectFactory，调用 `getObject()` 生成“早期对象（可能是代理）”。该方法的调用链为：
    
    
    getBean()
      ↓
    doGetBean()
      ↓
    getSingleton(beanName)   ⭐ 第一次尝试从一级缓存拿
      ↓（如果没有）
    createBean()
      ↓
    doCreateBean()
      ↓
    populateBean（属性填充）
      ↓
    getBean(依赖Bean)  ⭐ 这里会再次调用
      ↓
    getSingleton(beanName, true) ⭐  触发你这段代码

> 小结：Spring 对循环依赖的判断并非基于静态分析，而是通过运行时状态检测实现的。具体而言，当一个 Bean 在创建过程中再次被请求，且该 Bean 已存在于“正在创建集合”中时，即可判定为循环依赖。此时，Spring 会优先尝试通过三级缓存机制获取早期引用来解决问题，若无法解决（如构造器循环依赖），则抛出异常终止创建过程。

[AFFILIATE_SLOT_2] 

## 四、三级缓存总结

在Spring中，循环依赖（如A依赖B、B又依赖A）并不是在一开始就被检测出来的，而是在Bean依赖注入的递归创建过程中逐步触发的。为了解决这一问题，Spring在Bean实例化之后，通过**三级缓存机制提前暴露Bean引用** ，从而打破依赖闭环。同时，为了保证AOP代理的一致性，Spring通过 `ObjectFactory + getEarlyBeanReference()` 实现了代理对象的提前创建与复用，确保整个生命周期中引用始终一致。

缓存级别| 存储内容| 进入时机| 移除时机| 核心作用| 是否可能是代理  
---|---|---|---|---|---  
一级缓存| 完整初始化后的 Bean| Bean 初始化完成后（initializeBean 之后）| 容器销毁| 对外提供最终可用对象| ✅（如果有 AOP）  
二级缓存| 提前暴露的 Bean（早期对象）| 从三级缓存获取早期引用后| Bean 完成初始化后| 解决循环依赖（直接提供对象）| ✅（可能是代理）  
三级缓存| Bean 工厂（延迟生成对象）| Bean 实例化之后（依赖注入前）| 被调用后立即移除| 提供“提前生成代理对象”的能力| ✅（通过工厂生成）  
  
理解这一机制，不仅有助于诊断Spring容器启动中的异常，还能让你在Go、Python或JavaScript等语言中设计依赖注入框架时，借鉴这种优雅的延迟暴露思想。

`initializeBean()`

posted on 2026-05-25 20:12 [wgwyanfs](https://www.cnblogs.com/wgwyanfs) 阅读(80) 评论(0) [收藏](javascript:void\(0\)) [举报](https://report.cnblogs.com?targetLink=https%3A%2F%2Fwww.cnblogs.com%2Fwgwyanfs%2Fp%2F20159999&targetId=20159999&targetType=0)
