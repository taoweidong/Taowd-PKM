---
source: "https://springdoc.cn/spring-bean-circular-dependencies/"
title: "Spring Bean 循环依赖 - spring 中文网"
fetched_at: "2026-10-06 12:33"
---

## 1、背景

有好几次线上发布老应用时，遭遇代码启动报错，具体错误如下：
    
    
    Caused by: org.springframework.beans.factory.BeanCurrentlyInCreationException:
     Error creating bean with name 'xxxManageFacadeImpl': Bean with name 'xxxManageFacadeImpl'  has been injected into other beans [xxxProductMaintenceFacadeImpl]
     in its raw version as part of a circular reference, but has eventually been wrap means thff, for expped. This means that said other beans do not use the final version of the bean. 
    This is often the result of over-eager type matching - consider using 'getBeanNamesallowEageOfType' with the 'allowEagerInit' flag turned off, for example
    

咋眼一看，这不就是 Spring Bean 循环依赖报错吗？脑海立马闪过那些年为了进阿里面试时被死亡 N 连问的场景，那时我们都知道 Spring 已经支持 Bean 循环依赖，为啥我们的 Spring Boot 应用启动时还报这个错误？于是，带着这个问题重新温习下 Spring 如何解决 Bean 循环依赖。

## 2、相关知识点简介

### 2.1、什么是 Bean 循环依赖？

循环依赖是指 Bean 对象循环引用，是两个或多个 Bean 之间相互持有对方的引用。循环依赖有 2 种表现形式：

第一种是相互依赖，也就是 A 依赖 B，B 又依赖 A。

第二种是自我依赖，也就是 A 依赖自己形成自我依赖。

对象引用循环依赖在某些业务场景上可能是合理存在的，但是由于 Spring 容器设计了依赖注入机制，即 Spring 容器在创建 Bean 实例化以后就要给 Bean 中的属性自动赋值，要全部自动赋值之后，才能交给用户使用。

如果出现循环依赖的情况，以两个 Bean 互相依赖的情况作为举例，假设有 AService 已经实例化（但未完成初始化），但是 AService 中需要自动赋值的 BService 并没有初始化，如果 Spring 立刻初始化 BService，发现 BService 中需要自动赋值 AService 也没有初始化完成，这样就会出现相互等待，形成死循环，可能导致 Spring 容器都无法启动了。

由此可见，对 Bean 的填充属性是循环依赖源头的开始。

### 2.2、Spring 创建 Bean 主要流程

为了容易理解 Spring 解决循环依赖过程，我们先简单温习下 Spring 容器创建 Bean 的主要流程。

从代码看 Spring 对于 Bean 的生成过程，步骤还是很多的，我把一些扩展业务代码省略掉，先上点开胃菜：
    
    
    protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)
            throws BeanCreationException {
        if (mbd.isSingleton()) {
            instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
        }
        // Bean初始化第一步：默认调用无参构造实例化Bean
        // 如果是只有带参数的构造方法，构造方法里的参数依赖注入，就是发生在这一步
        if (instanceWrapper == null) {
            instanceWrapper = createBeanInstance(beanName, mbd, args);
        }
        // Initialize the bean instance.
        Object exposedObject = bean;
        try {
            // bean创建第二步：填充属性（DI依赖注入发生在此步骤）
            populateBean(beanName, mbd, instanceWrapper);
            // bean创建第三步：调用初始化方法，完成bean的初始化操作（AOP的第三个入口）
            // AOP是通过自动代理创建器AbstractAutoProxyCreator的postProcessAfterInitialization()
    //方法的执行进行代理对象的创建的,AbstractAutoProxyCreator是BeanPostProcessor接口的实现
            exposedObject = initializeBean(beanName, exposedObject, mbd);
        }
        catch (Throwable ex) {
            // ...
        }
        // ...
    

从上述代码看出，整体脉络可以归纳成 3 个核心步骤：

  1. 实例化 Bean

主要是通过反射调用默认构造函数创建 Bean 实例，此时 Bean 的属性都还是默认值 `null`。被注解 `@Bean` 标记的方法就是此阶段被调用的。

  2. 填充 Bean 属性

这一步主要是对 Bean 的依赖属性进行填充，对 `@Value`、`@Autowired`、`@Resource` 注解标注的属性注入对象引用。

  3. 调用 Bean 初始化方法

调用配置指定中的 `init` 方法，如 xml 文件指定 Bean 的 `init-method` 方法或注解 `@Bean(initMethod = "initMethod")` 指定的方法。




### 2.3、BeanPostProcessor 接口拓展点

在 Bean 创建的流程中 Spring 提供了多个 `BeanPostProcessor` 接口（下称 BPP）方便开发者对 Bean 进行自定义调整和加工。有以下几种 BPP 接口比较常用：

  * `postProcessMergedBeanDefinition`：可对 `BeanDefinition` 添加额外的自定义配置；
  * `getEarlyBeanReference`：返回早期暴露的 Bean 引用，一个典型的例子是循环依赖时如果有动态代理，需要在此先返回代理实例；
  * `postProcessAfterInstantiation`：在 `populateBean` 前用户可以手动注入一些属性；
  * `postProcessProperties`：对属性进行注入，例如配置文件加密信息在此解密后注入；
  * `postProcessBeforeInitialization`：属性注入后的一些额外操作；
  * `postProcessAfterInitialization`：实例完成创建的最后一步，这里也是一些 BPP 进行 AOP 代理的时机。



最后，对 Bean 的生命流程进行一个流程图的总结：

此处敲黑板划重点：Spring 的动态代理（AOP）是通过 BPP 实现的（在图三中的 3.4 步实现），其中 `AbstractAutoProxyCreator` 是十分典型的自动代理类，它实现了 `SmartInstantiationAwareBeanPostProcessor` 接口，并重写了 `getEarlyBeanReference` 和 `postProcessAfterInitialization` 两个方法实现代理的逻辑，这样完成对原始 Bean 进行增强，生成新 Bean 对象，将增强后的新 Bean 对象注入到属性依赖中。

## 3、Spring 如何解决循环依赖？

先说结论，Spring 是通过三级缓存和提前曝光的机制来解决循环依赖的问题。

### 3.1、三级缓存作用

三级缓存其实就是用三个 `Map` 来存储不同阶段 Bean 对象。

  * 一级缓存 `singletonObjects`：主要存放的是已经完成实例化、属性填充和初始化所有步骤的单例 Bean 实例，这样的 Bean 能够直接提供给用户使用，我们称之为终态 Bean 或叫成熟 Bean。
  * 二级缓存 `earlySingletonObjects`：主要存放的已经完成初始化但属性还没自动赋值的 Bean，这些 Bean 还不能提供用户使用，只是用于提前暴露的 Bean 实例，我们把这样的 Bean 称之为临时 Bean 或早期的 Bean（半成品 Bean）
  * 三级缓存 `singletonFactories`：存放的是 `ObjectFactory` 的匿名内部类实例，调用 `ObjectFactory.getObject()` 最终会调用 `getEarlyBeanReference` 方法，该方法可以获取提前暴露的单例 Bean 引用。



### 3.2、三级缓存解决循环依赖过程

现在通过源码分析，深入理解下 Spring 如何运用三级缓存解决循环依赖。Spring 创建 Bean 的核心代码 `doGetBean` 中，在实例化 Bean 之前，会先尝试从三级缓存获取 Bean，这也是 Spring 解决循环依赖的开始。

我们假设现在有这样的场景：`AService` 依赖 `BService`，`BService` 依赖 `AService`。

一开始加载 `AService` Bean 首先依次从一、二、三级缓存中查找是否存在 `beanName=AService` 的对象。
    
    
    // AbstractBeanFactory.java
        protected <T> T doGetBean(final String name, @Nullable final Class<T> requiredType,
                                  @Nullable final Object[] args, boolean typeCheckOnly) throws BeansException {
            final String beanName = transformedBeanName(name);
            // 1.尝试从缓存中获取bean，AService还没创建三级缓存都没命中
            Object sharedInstance = getSingleton(beanName);
            if (mbd.isSingleton()) {
    
                sharedInstance = getSingleton(beanName,    () -> {  //注意此处参数是一个lambda表达式即参数传入的是ObjectFactory类型一个匿名内部类对象
                                                            try {
                                                                return createBean(beanName, mbd, args);  // 
                                                            }
                                                            catch (BeansException ex) {}
                                                        });
                beanInstance = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
            }
        }
    

因为 `AService` 还没创建，三级缓存都没命中于是走到创建 Bean 代码逻辑。调用方法 `getSingleton(String beanName，ObjectFactory objectFactory)` 方法，第二个参数传入一个 `ObjectFactory` 接口的匿名内部类实例。
    
    
    public Object getSingleton(String beanName, ObjectFactory singletonFactory) {
    //将当前beanName放到singletonsCurrentlyInCreation 集合中，标识该bean正在创建
        beforeSingletonCreation(beanName);
        //通过回调getObject()方法触发AbstractAutowireCapableBeanFactory#createBean(String beanName, RootBeanDefinition mbd, Object[] args)的执行
        singletonObject = singletonFactory.getObject();
        afterSingletonCreation(beanName);
        addSingleton(beanName, singletonObject);
    }
    

该方法主要做四件事情：

  * 将当前 `beanName` 放到 `singletonsCurrentlyInCreation` 集合中标识该 Bean 正在创建；
  * 调用匿名内部类实例对象的 `getObject()` 方法触发 `AbstractAutowireCapableBeanFactory#createBean` 方法的执行；
  * 将当前 `beanName` 从 `singletonsCurrentlyInCreation` 集合中移除；



`singletonFactory.getObject()` 方法触发回调 `AbstractAutowireCapableBeanFactory#createBean(String beanName, RootBeanDefinition mbd, Object[] args)` 的执行，进入真正创建 AService Bean 流程。
    
    
    //真正创建Bean的地方 AbstractAutowireCapableBeanFactory#doCreateBean
        protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)  throws BeanCreationException {
    
            // Instantiate the bean.
            BeanWrapper instanceWrapper = null;
            if (mbd.isSingleton()) {
                instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
            }
            // bean初始化第一步：默认调用无参构造实例化Bean
            // 构造参数依赖注入，就是发生在这一步
            if (instanceWrapper == null) {
                instanceWrapper = createBeanInstance(beanName, mbd, args);
            }
            // 实例化后的Bean对象
            final Object bean = instanceWrapper.getWrappedInstance();
            // 将刚创建的bean放入三级缓存中singleFactories(key是beanName，value是ObjectFactory)
            //注意此处参数又是一个lambda表达式即参数传入的是ObjectFactory类型一个匿名内部类对象，在后续再缓存中查找Bean时会触发匿名内部类getEarlyBeanReference()方法回调
            addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
            // Initialize the bean instance.
            Object exposedObject = bean;
            try {
                // bean创建第二步：填充属性（DI依赖注入发生在此步骤）
                populateBean(beanName, mbd, instanceWrapper);
                // bean创建第三步：调用初始化方法，完成bean的初始化操作（AOP的第三个入口）
                // AOP是通过自动代理创建器AbstractAutoProxyCreator的postProcessAfterInitialization()
    //方法的执行进行代理对象的创建的,AbstractAutoProxyCreator是BeanPostProcessor接口的实现
                exposedObject = initializeBean(beanName, exposedObject, mbd);
            }
            catch (Throwable ex) {
                // ...
            }
    
        }
    

在上面创建 `AService` Bean 代码流程可以看出，`AService` 实例化后调用 `addSingletonFactory(String beanName, ObjectFactory singletonFactory)` 方法将以 Key 为`AService`，Value 是 `ObjectFactory` 类型一个匿名内部类对象放入三级缓存中，在后续使用 `AService` 时会依次在一、二、三级缓存中查找，最终三级缓存中查到这个匿名内部类对象，从而触发匿名内部类中 `getEarlyBeanReference`() 方法回调。

**此处为什么不是`AService` 实例直接放入三级缓存呢？因为我们上面说了 AOP 增强逻辑是在创建 Bean 第三步：调用初始化方法之后进行的，AOP 增强后生成的新代理类 `AServiceProxy` 实例对象，假如此时直接把 `AService` 实例直接放入三级缓存，那么在对 `BService` Bean 依赖的 `aService` 属性赋值的就是 `AService` 实例，而不是增强后的 `AServiceProxy` 实例对象。**

在以 Key 为 `AService`，Value 为 `ObjectFactory` 类型一个匿名内部类对象放入三级缓存后，继续对 `AService` 进行属性填充（依赖注入），这时发现 `AService` 依赖 `BService`。

于是又依次从一、二、三级缓存中查询 `BService` Bean，没找到，于是又按照上述的流程实例化 `BService`，将以 Key 为 `BService`，Value 是 `ObjectFactory` 类型一个匿名内部类对象放入三级缓存中，继续对 `BService` 进行属性填充（依赖注入），这时发现 `BService` 又依赖 `AService`。于是依次在一、二、三级缓存中查找 `AService`。
    
    
    //DefaultSingletonBeanRegistry.java
    public Object getSingleton(String beanName) {
        return getSingleton(beanName, true);
    }
    protected Object getSingleton(String beanName, boolean allowEarlyReference) {
            // 从一级缓存获取，key=AService
            Object singletonObject = this.singletonObjects.get(beanName);
            if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
                synchronized (this.singletonObjects) {
                    // 从二级缓存获取，key=AService 
                    singletonObject = this.earlySingletonObjects.get(beanName);
                    // 是否允许循环引用
                    if (singletonObject == null && allowEarlyReference) {
                       // 前面已经将以Key为AService，value是ObjectFactory类型一个匿名内部类对象放入三级缓存了
                        ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                        if (singletonFactory != null) {
                             //singletonFactory是一个匿名内部类对象，此处触发匿名内部类中getEarlyBeanReference()方法回调。
                            singletonObject = singletonFactory.getObject();
                            // 将三级缓存生产的bean放入二级缓存中
                            this.earlySingletonObjects.put(beanName, singletonObject);
                            // 删除三级缓存
                            this.singletonFactories.remove(beanName);
                        }
                    }
                }
            }
            return singletonObject;
        }
    

最终三级缓存中查到之前放入的以 Key 为 `AService`，Value为 `ObjectFactory` 类型一个匿名内部类对象，从而触发匿名内部类 `getEarlyBeanReference()` 方法回调。`getEarlyBeanReference()` 方法决定返回的 `AService` 实例到底是 `AService` 实例本身还是被 AOP 增强后的 `AServiceProxy` 实例对象。

如果没 AOP 切面对 `AService` 进行拦截，这时返回的将是 `AService` 实例本身。接着将半成品 `AService` Bean 放入二级缓存并将 `AService` Key 从三级缓存中删除，这样实现了提前将 `AService` Bean 曝光给 `BService` 完成属性依赖注入。继续进行 `BService` 后续初始化逻辑，最后生产了成熟的 `BService` Bean 实例。

接着原路返回，`AService` 也成功获取到依赖 `BService` 实例，完成后续的初始化工作，然后完美的解决了循环依赖的问题。

最后，来一张解决 `AService` 依赖 `BService`，`BService` 又依赖 `AService` 这样循环依赖的流程图对上述 Spring 代码逻辑进行总结。

### 3.3、当 AOP 遇到循环依赖

从 **2.3、BeanPostProcessor 接口拓展点** 小节，我们知道 Bean 的 AOP 动态代理创建时在初始化之后通过回调 `postProcessAfterInitialization` 后置处理器进行的，但是出现循环依赖的 Bean 如果使用了 AOP， 那就需要在 `getEarlyBeanReference()` 方法创建动态代理，将生成的代理 Bean 放在二级缓存提前曝光出来， 这样 `BService` 的属性 `aService` 注入的就是被代理后的 `AServiceProxy` 实例对象。

下面以 `AService` 依赖 `BService`，`BService` 依赖 `AService`，`AService` 被 AOP 切面拦截的场景进行代码分析循环依赖的 Bean 使用了 AOP 如何在 `getEarlyBeanReference()` 方法如何提前创建动态代理 Bean。
    
    
    // 将Aservice添加三级缓存
    addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
    // 添加Bservice的aService属性时从三级中找Aservice的ObjectFactory类型一个匿名内部类对象，从而触发匿名内部类getEarlyBeanReference()方法回调，进入创建AService切面代理对象逻辑
    protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
        Object exposedObject = bean;
        if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
            //判断后置处理器是否实现了SmartInstantiationAwareBeanPostProcessor接口
            //调用SmartInstantiationAwareBeanPostProcessor的getEarlyBeanReference
            for (SmartInstantiationAwareBeanPostProcessor bp : getBeanPostProcessorCache().smartInstantiationAware) {
                exposedObject = bp.getEarlyBeanReference(exposedObject, beanName);
            }
        }
        return exposedObject;
    }
    

可以看出 `getEarlyBeanReference()` 方法判断后置处理器是否实现了 `SmartInstantiationAwareBeanPostProcessor` 后置处理器接口。

而我们演示代码通过 `@EnableAspectJAutoProxy` 注解导入的 AOP 核心业务处理 `AnnotationAwareAspectJAutoProxyCreator` 类，它继承了 `AbstractAutoProxyCreator`，在 `AbstractAutoProxyCreator` 类中实现了 `getEarlyBeanReference()` 方法。
    
    
    //真正实现了该方法的类就是AbstractAutoProxyCreator
    public abstract class AbstractAutoProxyCreator extends ProxyProcessorSupport
          implements SmartInstantiationAwareBeanPostProcessor, BeanFactoryAware { 
        @Override
        public Object getEarlyBeanReference(Object bean, String beanName) throws BeansException {
            // 先获取beanName,主要是为FactoryBean类型添加&前缀
            Object cacheKey = getCacheKey(bean.getClass(), beanName);
            // 判断是否已经在earlyProxyReferences集合中，不在则添加进去
            if (!this.earlyProxyReferences.contains(cacheKey)) {
                this.earlyProxyReferences.add(cacheKey);
            }
            // 创建代理对象，如果必要的话
            return wrapIfNecessary(bean, beanName, cacheKey);
        }  
        /**
         * Wrap the given bean if necessary, i.e. if it is eligible for being proxied.
         * @param bean the raw bean instance
         * @param beanName the name of the bean
         * @param cacheKey the cache key for metadata access
         * @return a proxy wrapping the bean, or the raw bean instance as-is
         */
        protected Object wrapIfNecessary(Object bean, String beanName, Object cacheKey) {
            // 前面先做一些基本的判断
            if (StringUtils.hasLength(beanName) && this.targetSourcedBeans.contains(beanName)) {
                return bean;
            }
            if (Boolean.FALSE.equals(this.advisedBeans.get(cacheKey))) {
                return bean;
            }
            // Advice/Pointcut/Advisor/AopInfrastructureBean接口的beanClass不进行代理以及对beanName为aop内的切面名也不进行代理
            // 此处可查看子类复写的shouldSkip()方法
            if (isInfrastructureClass(bean.getClass()) || shouldSkip(bean.getClass(), beanName)) {
                this.advisedBeans.put(cacheKey, Boolean.FALSE);
                return bean;
            }
            // Create proxy if we have advice.
            // 查找对代理类相关的advisor对象集合，此处就与point-cut表达式有关了
            Object[] specificInterceptors = getAdvicesAndAdvisorsForBean(bean.getClass(), beanName, null);
            // 对相应的advisor不为空才采取代理
            if (specificInterceptors != DO_NOT_PROXY) {
                this.advisedBeans.put(cacheKey, Boolean.TRUE);
                // 通过jdk动态代理或者cglib动态代理，产生代理对象,这里传入的是SingletonTargetSource对象喔，对原始bean对象进行了包装
                Object proxy = createProxy(
                        bean.getClass(), beanName, specificInterceptors, new SingletonTargetSource(bean));
                // 放入代理类型缓存
                this.proxyTypes.put(cacheKey, proxy.getClass());
                return proxy;
            }
            // 放入通知缓存
            this.advisedBeans.put(cacheKey, Boolean.FALSE);
            return bean;
        }
    }
    

`wrapIfNecessary` 方法查找 `AService` 是否查找存在的 `advisor` 对象集合，此处就与 `point-cut` 表达式有关了，显然我们的切点 `@Around("execution(* com.example.service.AService.helloA(..))")` 拦截了 `AService`，因此需要创建 `AService` 的代理 Bean。

通过 jdk 动态代理或者 cglib 动态代理，产生代理对象，对原始 `AService` 对象进行了包装最后返回的是 `AService` 的代理对象 `aServiceProxy`，然后把 `aServiceProxy` 放入二级缓存里面，并删除三级缓存中的 `AService` 的 `ObjectFactory`。这样实现了提前为 `AService` 生成动态对象 `aServiceProxy` 并赋值给 `BService` 的 `aService` 属性依赖注入。这样 `BService` 完成了属性依赖注入，继续进行 `BService` 后续初始化逻辑，最后生产了成熟的 `BService` Bean 实例。

当 `BService` 创建完了之后，`AService` 在缓存 `BService` Bean 对象完成 `bService` 属性注入后，接着进行到 Bean 创建流程的第三步：初始化 `AService`，有了上面的知识，我们知道初始化 `AService` 会回调 `postProcessAfterInitialization` 后置处理器又开始 `AOP` 逻辑。

而此时判断 `AService` 已经存在 `getEarlyBeanReference()` 方法中放入 `earlyProxyReferences` 了，说明 原始对象已经经历过了 AOP，因此就不用重复进行 AOP 逻辑。

这样 `AService` 也完成初始化工作，然后完美地解决了 `Aservice` 依赖 `BService`、`BService` 依赖 `Aservice` 这个循环依赖的问题。

最后，也来一张解决 `AService`、`BService` 相互依赖，且 `AService` 使用了 AOP 的循环依赖的流程图对上述 Spring 代码逻辑进行总结。

红色部分主要显示了与 “没有 AOP 情况下 `AService`、`BService` 相互依赖流程” 中的区别。

## 4、为啥我们应用还会报错？

前面章节已经详细讲了 Spring 通过三级缓存和提前曝光机制解决循环依赖问题。那我们的应用怎么还报此类错误呢？首先回顾下报错详情：

从错误描述看 `xxxProductMaintenanceFacadeImpl` 注入的 `xxxManageFacadeImpl` 对象与最终的 `xxxManageFacadeImpl` 对象不一致。

从上面代码分析，我们知道 Spring 能改变单例 Bean 的对象只有在 AOP 情况下出现，而出现循环依赖且使用 AOP 的 Bean 有 `getEarlyBeanReference()` 方法和 Bean 初始化步骤里后置处理器 `postProcessAfterInitialization` 两处时机进行AOP，如图五中第 18 步和第 22 步。

如果是同一个 AOP 的织入类，那么在 Bean 初始化步骤里后置处理器 `postProcessAfterInitialization` 处会判断 Bean 已经被代理过，不会再做 AOP 代理。但现在报错 `xxxManageFacadeImpl` 对象最终版本不一致，说明 `XxxManageFacadeImpl` 存在另一个 AOP 的织入类且是在后置处理器 `postProcessAfterInitialization` 处进行 AOP 的。

以下模拟我们的项目代码：

从示例代码看出 `AServiceImpl` 类被 `@Aspect` 和 `@Async` 两个切面注解拦截。

`@Aspect` 注解的 AOP 核心业务处理由 `AnnotationAwareAspectJAutoProxyCreator` 类，它继承了 `AbstractAutoProxyCreator` 了，在 `AbstractAutoProxyCreator` 类中实现了 `getEarlyBeanReference()` 方法。

`@Async` 注解的 AOP 核心业务处理由 `AsyncAnnotationBeanPostProcessor` 类，它只实现了 `postProcessAfterInitialization()` 方法，至于为什么 `@Async` 不实现提早暴露 `getEarlyBeanReference()`，我还没有想明白。这样 `@Async` 注解是在 `AService` 初始化步骤里后置处理器 `postProcessAfterInitialization` 进行 AOP，新生成了 `AServiceProxy2` 对象。

如下图所示 `@Aspect` 注解的 AOP 是在第 18 步实现的，这样二级缓存里的存放和 `BService` 对象的 `aService` 属性注入都是 `AServiceProxy` 实例对象；

而 `@Async` 注解的 AOP 是在第22步实现的，这是新生成 `AServiceProxy2` 实例对象；下图中蓝色部分就是进行两次 AOP 地方。

那么单例 Bean `AService` 存在两个 AOP 后的实例对象，这就违背单例的单一性原则，因此报错了。

或许到此你还会疑问，这个循环依赖问题为什么日常或预发没出现，而都是线上部署时才遇到报错此错误？

这就跟 Spring 的 Bean 加载顺序有关系了， Spring 容器载入 Bean 顺序是不确定的，Spring 框架没有约定特定顺序逻辑规范。在某些机器环境下是 `AService` 比 `BService` 先加载，但在某些环境下是 `BService` 比 `AService` 先加载。

还是拿上面示例分析，`AServiceImpl` 类被 `@Aspect` 和 `@Async` 两个切面注解拦截，但是先加载 `BService` 再加载 `AService`。

由图可以看出 `AService` 的 `@Aspect` 和 `@Async` 两个注解 AOP 在都是在后置处理器进行，因此只生成一个代理对象 `AServiceProxy` 实例，这种情况下应用启动就不会报错。

## 5、总结

总结下 Spring 解决循环依赖的思路：

在创建单例 Bean 时，会把该 Bean 的工厂函数的匿名类对象放入三级缓存中的 `singletonFactories` 中。

然后在填充属性时，如果出现循环依赖依赖本 Bean，必然执行之前放入的工厂函数的匿名实现，如果该 Bean 无需 AOP 的话，工厂函数返回的就是原 Bean 对象；如果该 Bean n有 AOP 的话，也有可能是被某些 BBP 处理 AOP 之后的代理对象，会放入二级缓存中的 `earlySingletonObjects` 中。

接着 Bean 开始初始化，如果该 Bean 无需 AOP 的话，结果返回的原来创建的 Bean 对象；如果该 Bean 有 AOP 的话，检查 AOP 织入逻辑是否已经在提前曝光时已经执行了，如果已经执行 AOP 则返回提前曝光的代理 Bean 对象；如果 AOP 织入逻辑未执行过，则进行后续的 `BeanPostProcessor` 后置处理器进行 AOP 织入，生成 AOP 代理 Bean 对象，并返回。

最后对于提前曝光的单例，就会去检查初始化后的 Bean 对象与二级缓存中提前曝光的 Bean 是不是同一个对象，只有不是的情况下才可能抛出异常。

深入阅读我们应用本身代码，发现项目中出现 Bean 的循环依赖，本质原因是代码架构设计不合理，某些 `facade` 类实现了本应在 `serivce` 层的业务逻辑，导致其他业务依赖地方反复应用 `facade` 层对象。SpringBoot 2.6.x 以上的版本官方已经不推荐使用循环依赖，说不定今后某个最新版本的 Spring 会强制不能出现 Bean 循环依赖，因此需要我们开发者在平时编码时要重视代码架构设计。

* * *

Ref：`https://mp.weixin.qq.com/s/DDgYHPChoo63-kL06PACog`
