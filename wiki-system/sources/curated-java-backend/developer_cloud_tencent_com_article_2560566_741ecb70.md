---
source: "https://developer.cloud.tencent.com/article/2560566"
title: "深入解析Spring框架底层原理：循环依赖三级缓存与AOP代理冲突-腾讯云开发者社区-腾讯云"
fetched_at: "2026-10-06 12:33"
---

[社区首页](https://developer.cloud.tencent.com) >[专栏](https://developer.cloud.tencent.com/column) >深入解析Spring框架底层原理：循环依赖三级缓存与AOP代理冲突

#### Spring框架循环依赖问题概述

在软件开发中，循环依赖是指两个或多个组件相互引用形成的闭环关系。以Spring框架为例，当Bean A依赖Bean B，而Bean B又反过来依赖Bean A时，就构成了典型的循环依赖场景。这种相互依赖关系如果处理不当，会导致应用程序启动时出现无限递归调用，最终引发栈溢出错误（StackOverflowError）。

Spring框架作为Java生态中最主流的IoC容器，其核心功能之一就是管理Bean的创建和依赖注入。在传统的对象创建流程中，循环依赖会导致严重的初始化问题：假设Bean A需要先初始化完成才能注入到Bean B，而Bean B又需要先初始化完成才能注入到Bean A，这种"先有鸡还是先有蛋"的悖论使得常规的创建流程无法继续执行。

##### 循环依赖的典型表现

在Spring应用中可以观察到三种循环依赖模式：

  1. **构造器循环依赖** ：通过构造方法参数形成的循环引用，这是Spring明确声明无法解决的场景，会在启动时直接抛出BeanCurrentlyInCreationException异常。因为构造器注入必须在实例化阶段完成，此时对象尚未创建，无法提前暴露引用。 
  2. **属性循环依赖** ：通过setter方法或字段注入形成的循环引用，这是Spring能够自动处理的主要场景。例如： 



复制
    
    
    @Component
    public class ServiceA {
        @Autowired
        private ServiceB serviceB;
    }
    
    @Component 
    public class ServiceB {
        @Autowired
        private ServiceA serviceA;
    }

  1. **代理对象循环依赖** ：当循环依赖的Bean需要被AOP代理时产生的特殊情况，这种场景下原始对象和代理对象的交替出现会形成更复杂的依赖关系，需要特殊处理机制。



##### Spring的解决方案演进

早期版本的Spring采用简单的"早期引用暴露"机制，即在对象实例化后立即将尚未初始化的原始引用暴露给其他Bean。但这种简单方案存在明显缺陷：当暴露的原始对象后续被AOP代理替换时，已经注入的引用仍然是原始对象，导致代理失效。

为解决这个问题，Spring发展出了成熟的三级缓存架构：

  * **一级缓存（singletonObjects）** ：存储完全初始化好的单例Bean，是最终可用的成品对象
  * **二级缓存（earlySingletonObjects）** ：存储提前暴露的Bean实例（已实例化但未初始化）
  * **三级缓存（singletonFactories）** ：存储Bean工厂（ObjectFactory），用于生成早期引用



这种分层缓存设计的关键创新在于：不是直接暴露对象实例，而是通过ObjectFactory延迟获取引用。当需要解决循环依赖时，Spring会调用ObjectFactory的getObject()方法，这个方法会执行SmartInstantiationAwareBeanPostProcessor的getEarlyBeanReference()处理，确保在AOP代理场景下返回的是代理对象而非原始对象。

##### 典型循环依赖处理流程

以一个简单的A→B→A循环依赖为例，Spring的处理过程可分为以下阶段：

  1. **开始创建Bean A**
     * 标记A为创建中状态
     * 通过反射调用构造器实例化A对象
     * 将包含A原始对象的ObjectFactory注册到三级缓存
     * 开始填充A的属性，发现需要注入B
  2. **开始创建Bean B**
     * 同样经历实例化过程
     * 将B的ObjectFactory放入三级缓存
     * 填充B属性时发现需要A
  3. **解决循环依赖**
     * 从三级缓存获取A的ObjectFactory
     * 执行getEarlyBeanReference()获取A的早期引用（可能是代理对象）
     * 将早期引用放入二级缓存
     * 将引用返回给B完成注入
  4. **完成B的初始化**
     * B继续执行后续初始化回调
     * 将完全初始化的B放入一级缓存
     * 返回B给A完成属性注入
  5. **完成A的初始化**
     * A执行初始化回调
     * 将最终版A放入一级缓存
     * 清理二级缓存中的临时引用



这种机制成功打破了循环依赖的死锁状态，通过将对象的创建过程分为多个阶段（实例化→属性填充→初始化），并在适当时机暴露中间状态的对象引用来实现依赖闭环。值得注意的是，三级缓存中存储的ObjectFactory不仅解决了基本的循环依赖问题，更重要的是为AOP代理等扩展功能提供了处理空间，这是二级缓存无法实现的复杂场景。

#### 三级缓存的工作原理

在Spring框架中，三级缓存机制是解决循环依赖问题的核心设计。这一机制通过三个不同层级的缓存协同工作，确保在对象尚未完全初始化时就能被其他对象引用，同时保证最终注入的Bean是完整且符合预期的。理解三级缓存的工作原理，需要从它的结构定义、运作流程以及与AOP代理的交互三个维度展开。

Spring三级缓存结构及其在解决循环依赖中的流程

##### 三级缓存的结构定义

Spring容器内部维护着三个关键缓存数据结构：

  1. **一级缓存（singletonObjects）** ：存储完全初始化完成的单例Bean，是Spring容器最终对外提供的成品。这个缓存采用ConcurrentHashMap实现，保证线程安全。
  2. **二级缓存（earlySingletonObjects）** ：存放已实例化但尚未完成属性注入和初始化的早期Bean对象。这个缓存的作用是避免重复创建早期引用，提升性能。
  3. **三级缓存（singletonFactories）** ：存储ObjectFactory对象工厂，这是解决循环依赖最关键的环节。每个ObjectFactory持有创建原始对象或代理对象的能力，在需要时通过getObject()方法动态生成Bean的早期引用。



值得注意的是，三级缓存的设计并非简单的层级递进关系，而是各司其职的协作体系。一级缓存是终点站，二级缓存是临时中转站，而三级缓存则是生产车间。

##### 循环依赖解决流程

以一个典型的A→B→A循环依赖场景为例，三级缓存的工作流程可分为以下关键步骤：

  1. **创建Bean A的实例** ： 
     * 首先调用构造函数实例化A对象（此时属性b为null）
     * 立即将A对应的ObjectFactory注册到三级缓存中，这个工厂能够返回A的原始对象或代理对象
     * 开始进行属性注入，发现需要注入Bean B
  2. **创建Bean B的实例** ： 
     * 同样先实例化B对象
     * 将B的ObjectFactory放入三级缓存
     * 在属性注入阶段发现需要Bean A的引用
  3. **解决循环引用** ： 
     * 容器从三级缓存中获取A的ObjectFactory
     * 调用getObject()方法： 
       * 如果A不需要AOP代理，直接返回原始对象
       * 如果需要代理，则通过AbstractAutoProxyCreator创建代理对象
     * 将得到的早期引用（可能是原始对象或代理对象）放入二级缓存
     * 从三级缓存移除A的ObjectFactory
  4. **完成依赖注入** ： 
     * B获得A的早期引用后完成属性注入和初始化
     * B被放入一级缓存
     * A继续完成对B的属性注入和初始化
     * 最终A也进入一级缓存，二级缓存中的临时对象被清除



这个过程中，三级缓存的核心价值在于：通过ObjectFactory的延迟执行能力，在需要时才决定返回原始对象还是代理对象，解决了AOP代理与循环依赖的时序矛盾。

##### 关键设计细节

  1. **ObjectFactory的动态性** ： 三级缓存存储的不是Bean本身，而是能够生产Bean的工厂。这种间接层设计使得Spring可以在运行时动态决定返回对象的形态。例如，当检测到Bean需要AOP代理时，ObjectFactory会通过AbstractAutoProxyCreator创建代理对象而非直接返回原始对象。 
  2. **二级缓存的优化作用** ： 当多个Bean同时依赖同一个早期Bean时，二级缓存避免了重复执行ObjectFactory.getObject()操作。一旦某个Bean的早期引用被创建并放入二级缓存，后续依赖都直接从二级缓存获取，这对性能敏感的场景尤为重要。 
  3. **缓存清理机制** ： 在Bean完成完整生命周期后，Spring会执行严格的缓存清理： 
     * 将成品Bean放入一级缓存
     * 从二级缓存移除对应的早期引用
     * 确保三级缓存中不再保留该Bean的ObjectFactory 这种清理机制防止了内存泄漏，也保证了缓存状态的一致性。



##### 与AOP代理的协同

当循环依赖遇上AOP代理时，三级缓存展现出不可替代的价值。考虑以下关键点：

  1. **代理时机问题** ： 常规情况下，AOP代理是在Bean初始化完成后通过BeanPostProcessor创建的。但在循环依赖场景中，其他Bean可能在目标Bean初始化完成前就需要它的引用。三级缓存的ObjectFactory通过判断当前Bean是否需要代理，动态返回适当形式的对象，完美解决了这个时序矛盾。 
  2. **代理一致性保证** ： 通过三级缓存获取的早期代理对象与最终放入一级缓存的代理对象是同一个实例。这是通过缓存机制和代理工厂的协作实现的，确保在整个依赖链中使用的都是同一个代理对象，避免出现多个代理实例的情况。 
  3. **AnnotationAwareAspectJAutoProxyCreator的作用** ： 这个关键的BeanPostProcessor会介入ObjectFactory.getObject()的执行过程。当发现当前Bean匹配切面规则时，它会通过JDK动态代理或CGLib生成代理对象，而不是直接返回原始对象。 



三级缓存机制展现了Spring框架在解决复杂问题时的精巧设计。它不仅解决了对象创建阶段的循环依赖问题，还通过ObjectFactory的抽象层，实现了与AOP等扩展功能的无缝集成。这种设计既保证了功能正确性，又维持了框架的扩展能力，是Spring IoC容器最核心的架构智慧之一。

#### 早期对象曝光（ObjectFactory）的作用

在Spring框架处理循环依赖的核心机制中，ObjectFactory扮演着"延迟暴露"的关键角色。当两个Bean相互依赖时（例如ServiceA依赖ServiceB，同时ServiceB又依赖ServiceA），传统的实例化流程会陷入死锁状态。三级缓存中的第二级缓存——singletonFactories通过存储ObjectFactory对象，创造性地解决了这个经典难题。

##### ObjectFactory的核心设计思想

ObjectFactory本质上是一个函数式接口，其核心方法是`getObject()`，它并非直接存储Bean实例，而是保存了一个能够生成Bean引用的逻辑。这种设计实现了两个重要特性：

  1. **延迟加载** ：只有在真正发生循环依赖时才会触发对象创建
  2. **动态代理兼容** ：允许在最终获取对象时插入AOP代理生成逻辑



当Spring容器完成Bean的实例化（分配内存空间）但尚未进行属性注入时，会执行以下关键操作：

复制
    
    
    // 伪代码展示Spring核心逻辑
    addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, bean));

这个Lambda表达式就是ObjectFactory的具体实现，它将被存入singletonFactories缓存，为后续可能的循环依赖提供解决方案。

##### 与三级缓存的协同工作流程

在典型的AB循环依赖场景中，ObjectFactory与三级缓存配合完成以下关键步骤：

**初始曝光阶段** ：

实例化ServiceA后，将其ObjectFactory存入singletonFactories

此时缓存状态：

复制
    
    
    singletonFactories：{"serviceA": ObjectFactory<ServiceA>}
    earlySingletonObjects：{}
    singletonObjects：{}

**依赖解析阶段** ：

当ServiceA需要注入ServiceB时，容器开始创建ServiceB

ServiceB实例化后，其ObjectFactory同样存入singletonFactories

缓存状态变为：

复制
    
    
    singletonFactories：{"serviceA": ObjectFactory<ServiceA>, "serviceB": ObjectFactory<ServiceB>}
    earlySingletonObjects：{}
    singletonObjects：{}

**循环触发阶段** ：

  * 当ServiceB需要注入ServiceA时，容器按顺序检查缓存： 
    * 一级缓存singletonObjects：无ServiceA
    * 二级缓存earlySingletonObjects：无ServiceA
    * 三级缓存singletonFactories：找到ServiceA的ObjectFactory
  * 调用`getObject()`方法获取ServiceA的早期引用



这个过程中，ObjectFactory的智能之处在于它并非简单地返回原始对象。通过`getEarlyBeanReference()`方法，Spring会检查该Bean是否需要AOP代理，如果需要则提前生成代理对象，确保后续注入的都是一致的代理引用。

##### 动态代理的兼容处理

ObjectFactory对AOP代理的特殊处理体现在`getEarlyBeanReference()`方法的实现中。该方法会遍历所有BeanPostProcessor，特别是`AbstractAutoProxyCreator`，在以下两种情况下生成代理对象：

  1. 当Bean被标记为需要自动代理时
  2. 当存在匹配的切面表达式时



这种设计解决了"代理不一致"的经典问题。如果没有ObjectFactory的这层包装，可能会出现：

  * 属性注入的是原始对象
  * 但最终容器中的是代理对象 导致方法调用时切面逻辑不一致的严重问题



##### 性能与安全权衡

ObjectFactory的设计体现了Spring在性能与安全性之间的精巧平衡：

  1. **内存优化** ：仅存储轻量的ObjectFactory而非完整Bean实例
  2. **线程安全** ：通过三级缓存的层级检查避免并发问题
  3. **懒加载** ：只有真正发生循环依赖时才执行代理生成等耗时操作



一个值得注意的实现细节是，当ObjectFactory完成使命后，Spring会立即执行清理操作：

复制
    
    
    // 从三级缓存移除
    this.singletonFactories.remove(beanName);
    // 将早期引用存入二级缓存
    this.earlySingletonObjects.put(beanName, bean);

这种缓存升级机制既保证了后续依赖注入能直接获取对象，又避免了重复创建代理对象的开销。

##### 典型异常场景分析

在实际开发中，ObjectFactory相关的问题往往表现为以下形式：

  1. **代理对象不一致** ：当自定义BeanPostProcessor处理顺序不当，可能导致ObjectFactory生成的代理与实际最终代理不同
  2. **循环依赖链断裂** ：在复杂的多层级循环依赖中，如果某个中间Bean不支持早期暴露，会导致整个依赖链失败
  3. **作用域冲突** ：prototype作用域的Bean无法使用三级缓存机制，因为ObjectFactory每次需要生成新实例



通过理解ObjectFactory的工作原理，开发者可以更准确地诊断这类复杂问题。例如，当遇到"AOP增强方法不生效"的情况时，首先应该检查循环依赖中的Bean是否通过ObjectFactory正确生成了代理对象，而不是盲目地排查切面配置。

#### AOP代理与循环依赖的冲突

在Spring框架中，AOP代理与循环依赖的冲突是一个典型的"时序悖论"问题。当两个需要被AOP增强的Bean相互依赖时，常规的代理创建流程会被循环依赖打破，导致注入的可能是未经增强的原始对象。这种冲突的核心在于：**AOP代理的标准创建时机（初始化完成后）与循环依赖要求的提前暴露时机（初始化完成前）存在根本性矛盾** 。

AOP代理在循环依赖中的冲突场景及其解决方案

##### 冲突产生的根本原因

通过分析Spring的Bean生命周期可以发现，AbstractAutoProxyCreator作为AOP代理的核心处理器，其wrapIfNecessary方法通常只在postProcessAfterInitialization阶段执行。但在循环依赖场景下，当Bean A依赖Bean B，而Bean B又反过来依赖Bean A时，Spring会通过三级缓存提前暴露正在创建中的Bean A。此时若Bean A需要AOP增强，就会出现两种可能的问题场景：

  1. **过早暴露原始对象** ：如果直接暴露半成品Bean，后续AOP增强将无法作用于已被引用的对象
  2. **重复代理问题** ：如果在提前暴露时就创建代理，后续初始化阶段可能再次生成不同实例的代理对象



参考CSDN博客中的案例，当ServiceA和ServiceB相互依赖且都需要事务增强时，可能出现ServiceA中注入的ServiceB未被事务增强的情况。这是因为ServiceB在注入到ServiceA时，可能还处于原始对象状态，而事务代理尚未生成。

##### 三级缓存的精妙设计

Spring通过引入三级缓存中的ObjectFactory机制，创造性地解决了这一难题。具体流程表现为：

  1. **工厂封装** ：当Bean实例化后，Spring不会直接暴露对象本身，而是将其包装为ObjectFactory存入三级缓存（singletonFactories）
  2. **按需代理** ：在getEarlyBeanReference调用时，通过AbstractAutoProxyCreator的早期代理引用机制动态决定是否创建代理
  3. **一致性保证** ：earlyProxyReferences集合记录已生成代理的Bean，避免后续初始化阶段重复创建



这种设计的关键优势在于将代理决策时机延迟到最后可能的时刻。如博客园某技术文章所述：“Spring并非在暴露时就创建代理，而是在其他Bean真正需要注入时才通过ObjectFactory.getObject()动态决定是否生成代理”。

##### 典型问题场景分析

在实际开发中，这种冲突常表现为以下现象：

  1. **切面未生效** ：@Transactional等基于AOP的注解在循环依赖场景下失效
  2. **代理类型不一致** ：JDK动态代理与CGLIB代理混合使用导致类型转换异常
  3. **NPE风险** ：过早暴露的对象可能因未完成依赖注入而引发空指针



以事务失效为例，当存在如下循环依赖时：

复制
    
    
    @Service
    public class OrderService {
        @Autowired
        private UserService userService;
        
        @Transactional
        public void createOrder() {...}
    }
    
    @Service 
    public class UserService {
        @Autowired
        private OrderService orderService;
    }

若处理不当，UserService中注入的OrderService可能是未被事务增强的原始对象，导致createOrder()方法的事务特性丢失。

##### Spring的解决方案剖析

Spring通过三级缓存与AbstractAutoProxyCreator的协作，建立了完整的解决方案：

  1. **早期代理标记** ：在getEarlyBeanReference方法中，将待代理Bean记录到earlyProxyReferences集合
  2. **代理一致性检查** ：在postProcessAfterInitialization阶段，通过earlyProxyReferences判断是否已处理过该Bean
  3. **智能代理选择** ：根据Bean是否需要代理以及代理类型（JDK/CGLIB）动态生成合适的代理对象



源码层面，AbstractAutoProxyCreator的关键处理逻辑如下：

复制
    
    
    public Object getEarlyBeanReference(Object bean, String beanName) {
        Object cacheKey = getCacheKey(bean.getClass(), beanName);
        this.earlyProxyReferences.put(cacheKey, bean);
        return wrapIfNecessary(bean, beanName, cacheKey); // 可能返回代理或原始对象
    }
    
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean != null) {
            Object cacheKey = getCacheKey(bean.getClass(), beanName);
            if (this.earlyProxyReferences.remove(cacheKey) != bean) {
                return wrapIfNecessary(bean, beanName, cacheKey);
            }
        }
        return bean;
    }

这种双重检查机制确保了无论Bean是通过常规初始化还是循环依赖提前暴露，最终获得的都是正确且唯一的代理实例。

##### 开发实践中的注意事项

为避免AOP代理与循环依赖的冲突问题，建议采用以下最佳实践：

  1. **避免必要循环** ：通过架构设计消除非必要的循环依赖
  2. **使用setter注入** ：相比字段注入，setter注入能提供更灵活的代理处理时机
  3. **明确代理模式** ：通过spring.aop.proxy-target-class统一指定CGLIB代理，避免JDK动态代理的接口限制
  4. **延迟注入** ：对于必须的循环依赖，可以考虑使用@Lazy延迟初始化



特别值得注意的是，在Spring Boot 2.6+版本中，默认禁止了循环依赖。如需使用，必须显式配置spring.main.allow-circular-references=true。这一改变正是由于循环依赖与AOP等高级特性的兼容性问题难以完美解决。

#### 源码层面的流程分析

在Spring框架的核心容器实现中，循环依赖的解决机制主要围绕`DefaultSingletonBeanRegistry`类的三级缓存体系展开。通过跟踪`AbstractAutowireCapableBeanFactory`的`doCreateBean`方法调用链，我们可以完整还原Spring处理循环依赖的底层逻辑。

Spring框架中循环依赖解决的源码流程

##### 三级缓存的底层数据结构

在`DefaultSingletonBeanRegistry`类中定义了三个关键Map结构：

复制
    
    
    // 一级缓存：存储完全初始化后的单例Bean
    private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);
    
    // 二级缓存：存储早期曝光的原始Bean对象
    private final Map<String, Object> earlySingletonObjects = new ConcurrentHashMap<>(16);
    
    // 三级缓存：存储ObjectFactory包装对象
    private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);

##### Bean实例化的关键流程

  1. **创建原始对象阶段** 在`createBeanInstance()`方法执行后，会通过`addSingletonFactory()`将原始对象包装为ObjectFactory存入三级缓存：



复制
    
    
    protected void addSingletonFactory(String beanName, ObjectFactory<?> singletonFactory) {
        synchronized (this.singletonObjects) {
            if (!this.singletonObjects.containsKey(beanName)) {
                this.singletonFactories.put(beanName, singletonFactory);
                this.earlySingletonObjects.remove(beanName);
            }
        }
    }

  1. **属性注入触发循环依赖** 当执行到`populateBean()`进行属性注入时，如果发现依赖对象尚未创建，会触发`getSingleton()`的递归调用。此时关键判断逻辑如下：



复制
    
    
    protected Object getSingleton(String beanName, boolean allowEarlyReference) {
        Object singletonObject = this.singletonObjects.get(beanName);
        if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
            synchronized (this.singletonObjects) {
                singletonObject = this.earlySingletonObjects.get(beanName);
                if (singletonObject == null && allowEarlyReference) {
                    ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                    if (singletonFactory != null) {
                        singletonObject = singletonFactory.getObject();
                        this.earlySingletonObjects.put(beanName, singletonObject);
                        this.singletonFactories.remove(beanName);
                    }
                }
            }
        }
        return singletonObject;
    }

##### AOP代理的特殊处理

当存在AOP代理需求时，`AbstractAutoProxyCreator`会介入处理流程。关键代码体现在`getEarlyBeanReference()`方法：

复制
    
    
    protected Object getEarlyBeanReference(String beanName, Object bean) {
        Object cacheKey = getCacheKey(bean.getClass(), beanName);
        this.earlyProxyReferences.put(cacheKey, bean);
        return wrapIfNecessary(bean, beanName, cacheKey);
    }

此时代理对象的生成时机被提前到三级缓存阶段，通过`SmartInstantiationAwareBeanPostProcessor`接口的扩展点实现。在后续`initializeBean()`阶段，会通过`earlyProxyReferences`判断是否已生成代理对象，避免重复代理。

##### 典型场景的代码执行路径

以A依赖B，B依赖A的循环场景为例：

  1. 创建A实例，原始对象A存入三级缓存
  2. A进行属性注入时触发B的创建
  3. 创建B实例时发现需要注入A，从三级缓存获取A的ObjectFactory
  4. ObjectFactory执行`getEarlyBeanReference()`生成A的代理对象
  5. B完成初始化后，A继续完成属性注入
  6. A初始化时检查`earlyProxyReferences`发现已处理过代理，直接返回现有对象



##### 关键设计决策点

  1. **三级缓存的必要性** 通过源码可见，如果只有二级缓存，在存在AOP代理时会导致以下问题： 
     * 无法区分原始对象和代理对象
     * 多次调用`getEarlyBeanReference()`可能产生不同的代理对象
  2. **同步锁的作用范围** 所有缓存操作都在`synchronized (this.singletonObjects)`代码块内完成，既保证线程安全又避免过度锁竞争。 
  3. **对象状态标记体系** `singletonsCurrentlyInCreation`等集合配合`isSingletonCurrentlyInCreation()`方法，精确控制Bean的创建阶段状态。 



#### 结语：Spring框架设计的智慧

在Spring框架的设计哲学中，循环依赖问题的解决方案堪称经典。通过三级缓存机制与早期对象曝光的巧妙结合，Spring不仅解决了对象创建过程中的死锁问题，更展现了框架设计者对复杂系统问题的深刻洞察。这种设计智慧体现在三个关键维度：分层治理、动态适配和风险隔离。

##### 分层治理的艺术

三级缓存（singletonObjects、earlySingletonObjects、singletonFactories）的层级结构体现了分而治之的思想。当检测到循环依赖时，Spring并不试图一次性解决所有问题，而是通过ObjectFactory将半成品对象暂存于三级缓存，允许其他对象先行引用。这种"先搭骨架再填血肉"的做法，打破了传统对象构造必须一步到位的思维定式。正如腾讯云开发者社区案例所示，即使AService和BService相互注入，Spring也能通过阶段性完成对象构建来避免死锁。

##### 动态适配的智慧

ObjectFactory的延迟加载特性展现了Spring的动态适配能力。在AOP代理场景下，三级缓存存储的不是原始对象而是ObjectFactory，这使得框架能够在最终实例化时动态决定返回原始对象还是代理对象。CSDN技术博客中提到的案例证明，这种设计完美解决了代理对象与原始对象在循环依赖中的身份冲突问题——当Bean需要被代理时，ObjectFactory.getObject()会返回增强后的实例，而普通Bean则直接返回原始引用。

##### 风险隔离的机制

早期曝光与完整初始化的分离体现了防御性编程思想。Spring将对象曝光分为两个阶段：三级缓存存储工厂对象（可生成早期引用），二级缓存存储已处理代理的半成品，一级缓存存储完全初始化的成品。这种隔离机制确保在并发环境下，其他线程要么获得统一代理对象，要么等待对象完全初始化。某技术社区分析的源码显示，DefaultSingletonBeanRegistry中的getSingleton方法通过同步块与三级缓存检查的组合，实现了线程安全与性能的平衡。

值得注意的是，这种设计并非完美无缺。构造器注入的循环依赖仍无法解决，这反而成为Spring推崇设值注入的最佳实践佐证。框架设计者有意为之的约束，引导开发者遵循更合理的对象关联方式，体现了"约定优于配置"的深层设计哲学。

在AOP代理与循环依赖的冲突处理中，Spring通过AbstractAutoProxyCreator的postProcessAfterInitialization与三级缓存的协同，展示了横切逻辑与核心容器的无缝集成能力。当检测到当前Bean正在被循环依赖时，SmartInstantiationAwareBeanPostProcessor会提前触发代理生成，这种条件判断与流程跳转的精密配合，使得本应相互排斥的两种机制产生了化学反应般的协同效应。

* * *

#### 引用资料

[1] : https://blog.csdn.net/qq_43290318/article/details/114679612

[2] : https://www.cnblogs.com/oneokrock-373/p/18965981

[3] : https://juejin.cn/post/7477883001449005091

[4] : https://developer.aliyun.com/article/1436029

本文参与 [腾讯云自媒体同步曝光计划](https://developer.cloud.tencent.com/support-plan)，分享自作者个人站点/博客。

原始发表：2025-08-04，如有侵权请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除

[框架](https://developer.cloud.tencent.com/tag/17353)

[原理](https://developer.cloud.tencent.com/tag/17566)

[缓存](https://developer.cloud.tencent.com/tag/10670)

[aop](https://developer.cloud.tencent.com/tag/10746)

[代理](https://developer.cloud.tencent.com/tag/17225)

目录

  *     *     *     * 

  *     *     *     *     * 

  *     *     *     *     *     * 

  *     *     *     *     *     * 

  *     *     *     *     *     * 

  *     *     *     * 

  * 


相关产品与服务

云开发 CloudBase

AI-Native 的全栈应用开发平台，为 AI 驱动的开发流程和终端应用而设计。提供应用开发所需的完整后端资源，包括数据库、服务托管、函数计算、文件存储、Web 应用托管等能力；支持小程序/小游戏、AI Agent 应用、Web 应用等场景；提供 Skills/MCP 工具适配主流 AI 编程工具，避免了开发过程中繁琐的服务端搭建及运维，开发者可以专注于业务逻辑的实现，开发效率更高。

[ __产品介绍](https://cloud.tencent.com/product/tcb?from=21341&from_column=21341)[ __产品文档](https://cloud.tencent.com/document/product/876?from=21342&from_column=21342)

[ __2026上云采购 | AI焕新·智启新局](https://cloud.tencent.com/act/pro/featured-202607?from=21344&from_column=21344)

[问题归档](https://developer.cloud.tencent.com/ask/archives.html)[专栏文章](https://developer.cloud.tencent.com/column/archives.html)[快讯文章归档](https://developer.cloud.tencent.com/news/archives.html)[关键词归档](https://developer.cloud.tencent.com/information/all.html)[开发者手册归档](https://developer.cloud.tencent.com/devdocs/archives.html)[开发者手册 Section 归档](https://developer.cloud.tencent.com/devdocs/sections_p1.html)
