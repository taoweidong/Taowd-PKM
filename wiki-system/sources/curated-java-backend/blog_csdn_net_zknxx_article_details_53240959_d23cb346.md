---
source: "https://blog.csdn.net/zknxx/article/details/53240959"
title: "SpringBoot之集成Spring AOP_springboot aop execution 匹配controller包下某几个方法-CSDN博客"
fetched_at: "2026-10-05 15:32:24"
---

在开始之前，我们先把需要的jar包添加到工程里。新增Maven依赖如下：


            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-aop</artifactId>
            </dependency>

接下来，我们进入正题。这里的涉及的通知类型有：前置通知、后置最终通知、后置返回通知、后置异常通知、环绕通知，下面我们就具体的来看一下怎么在SpringBoot中添加这些通知。

首先我们先创建一个Aspect切面类：


    @Component
    @Aspect
    public class WebControllerAop {

    }

指定切点：


        //匹配com.zkn.learnspringboot.web.controller包及其子包下的所有类的所有方法
        @Pointcut("execution(* com.zkn.learnspringboot.web.controller..*.*(..))")
        public void executeService(){

        }

接着我们再创建一个Controller请求处理类：


    package com.zkn.learnspringboot.web.controller;

    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;

    /**
     * Created by zkn on 2016/11/19.
     */
    @RestController
    @RequestMapping("/aop")
    public class AopTestController {

    }

### 前置通知

配置前置通知：


        /**
         * 前置通知，方法调用前被调用
         * @param joinPoint
         */
        @Before("executeService()")
        public void doBeforeAdvice(JoinPoint joinPoint){
            System.out.println("我是前置通知!!!");
            //获取目标方法的参数信息
            Object[] obj = joinPoint.getArgs();
            //AOP代理类的信息
            joinPoint.getThis();
            //代理的目标对象
            joinPoint.getTarget();
            //用的最多 通知的签名
            Signature signature = joinPoint.getSignature();
            //代理的是哪一个方法
            System.out.println(signature.getName());
            //AOP代理类的名字
            System.out.println(signature.getDeclaringTypeName());
            //AOP代理类的类（class）信息
            signature.getDeclaringType();
            //获取RequestAttributes
            RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
            //从获取RequestAttributes中获取HttpServletRequest的信息
            HttpServletRequest request = (HttpServletRequest) requestAttributes.resolveReference(RequestAttributes.REFERENCE_REQUEST);
            //如果要获取Session信息的话，可以这样写：
            //HttpSession session = (HttpSession) requestAttributes.resolveReference(RequestAttributes.REFERENCE_SESSION);
            Enumeration<String> enumeration = request.getParameterNames();
            Map<String,String> parameterMap = Maps.newHashMap();
            while (enumeration.hasMoreElements()){
                String parameter = enumeration.nextElement();
                parameterMap.put(parameter,request.getParameter(parameter));
            }
            String str = JSON.toJSONString(parameterMap);
            if(obj.length > 0) {
                System.out.println("请求的参数信息为："+str);
            }
        }

注意：这里用到了JoinPoint和RequestContextHolder。通过JoinPoint可以获得通知的签名信息，如目标方法名、目标方法参数信息等。通过RequestContextHolder来获取请求信息，Session信息。

接下来我们在Controller类里添加一个请求处理方法来测试一下前置通知：


        @RequestMapping("/testBeforeService.do")
        public String testBeforeService(String key,String value){

            return "key="+key+"  value="+value;
        }

前置通知拦截结果如下所示：

![](https://img-blog.csdn.net/20161120152308004?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

### 后置返回通知

配置后置返回通知的代码如下：


        /**
         * 后置返回通知
         * 这里需要注意的是:
         *      如果参数中的第一个参数为JoinPoint，则第二个参数为返回值的信息
         *      如果参数中的第一个参数不为JoinPoint，则第一个参数为returning中对应的参数
         * returning 限定了只有目标方法返回值与通知方法相应参数类型时才能执行后置返回通知，否则不执行，对于returning对应的通知方法参数为Object类型将匹配任何目标返回值
         * @param joinPoint
         * @param keys
         */
        @AfterReturning(value = "execution(* com.zkn.learnspringboot.web.controller..*.*(..))",returning = "keys")
        public void doAfterReturningAdvice1(JoinPoint joinPoint,Object keys){

            System.out.println("第一个后置返回通知的返回值："+keys);
        }

        @AfterReturning(value = "execution(* com.zkn.learnspringboot.web.controller..*.*(..))",returning = "keys",argNames = "keys")
        public void doAfterReturningAdvice2(String keys){

            System.out.println("第二个后置返回通知的返回值："+keys);
        }

Controller里添加响应的请求处理信息来测试后置返回通知：


        @RequestMapping("/testAfterReturning.do")
        public String testAfterReturning(String key){

            return "key=: "+key;
        }
        @RequestMapping("/testAfterReturning01.do")
        public Integer testAfterReturning01(Integer key){

            return key;
        }

当发送请求为：http://localhost:8001/aop/testAfterReturning.do?key=testsss&value=855sss时，处理结果如图所示：

![](https://img-blog.csdn.net/20161120152735134?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

当发送请求为：http://localhost:8001/aop/testAfterReturning01.do?key=55553&value=855sss时，处理结果如图所示：

![](https://img-blog.csdn.net/20161120152832559?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

### 后置异常通知

后置异常通知的配置方式如下：


        /**
         * 后置异常通知
         *  定义一个名字，该名字用于匹配通知实现方法的一个参数名，当目标方法抛出异常返回后，将把目标方法抛出的异常传给通知方法；
         *  throwing 限定了只有目标方法抛出的异常与通知方法相应参数异常类型时才能执行后置异常通知，否则不执行，
         *      对于throwing对应的通知方法参数为Throwable类型将匹配任何异常。
         * @param joinPoint
         * @param exception
         */
        @AfterThrowing(value = "executeService()",throwing = "exception")
        public void doAfterThrowingAdvice(JoinPoint joinPoint,Throwable exception){
            //目标方法名：
            System.out.println(joinPoint.getSignature().getName());
            if(exception instanceof NullPointerException){
                System.out.println("发生了空指针异常!!!!!");
            }
        }

Controller里配置响应的请求处理类：


        @RequestMapping("/testAfterThrowing.do")
        public String testAfterThrowing(String key){

            throw new NullPointerException();
        }

后置异常通知方法的处理结果如下所示：

![](https://img-blog.csdn.net/20161120153237814?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

### 后置最终通知

后置最终通知的配置方式如下：


        /**
         * 后置最终通知（目标方法只要执行完了就会执行后置通知方法）
         * @param joinPoint
         */
        @After("executeService()")
        public void doAfterAdvice(JoinPoint joinPoint){

            System.out.println("后置通知执行了!!!!");
        }

Controller类配置相应的请求处理类：


        @RequestMapping("/testAfter.do")
        public String testAfter(String key){

            throw new NullPointerException();
        }
        @RequestMapping("/testAfter02.do")
        public String testAfter02(String key){

            return key;
        }

当发送请求为：http://localhost:8001/aop/testAfter.do?key=55553&value=855sss

![](https://img-blog.csdn.net/20161120153553412?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
当发送请求为：http://localhost:8001/aop/testAfter02.do?key=55553&value=855sss

![](https://img-blog.csdn.net/20161120153553412?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)


### 环绕通知

环绕通知的配置方式如下：


        /**
         * 环绕通知：
         *   环绕通知非常强大，可以决定目标方法是否执行，什么时候执行，执行时是否需要替换方法参数，执行完毕是否需要替换返回值。
         *   环绕通知第一个参数必须是org.aspectj.lang.ProceedingJoinPoint类型
         */
        @Around("execution(* com.zkn.learnspringboot.web.controller..*.testAround*(..))")
        public Object doAroundAdvice(ProceedingJoinPoint proceedingJoinPoint){
            System.out.println("环绕通知的目标方法名："+proceedingJoinPoint.getSignature().getName());
            try {
                Object obj = proceedingJoinPoint.proceed();
                return obj;
            } catch (Throwable throwable) {
                throwable.printStackTrace();
            }
            return null;
        }

Controller对应的请求处理类如下：


        @RequestMapping("/testAroundService.do")
        public String testAroundService(String key){

            return "环绕通知："+key;
        }

当发送请求为：http://localhost:8001/aop/testAroundService.do?key=55553

![](https://img-blog.csdn.net/20161120154320017?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

当发送请求为:http://localhost:8001/aop/testAfter02.do?key=55553&value=855sss时，不符合环绕通知的切入规则，所以环绕通知不会 执行。

完整的AOP配置代码如下：


    package com.zkn.learnspringboot.aop;

    import com.alibaba.fastjson.JSON;
    import com.google.common.collect.Maps;
    import org.aspectj.lang.JoinPoint;
    import org.aspectj.lang.ProceedingJoinPoint;
    import org.aspectj.lang.Signature;
    import org.aspectj.lang.annotation.*;
    import org.springframework.stereotype.Component;
    import org.springframework.web.context.request.RequestAttributes;
    import org.springframework.web.context.request.RequestContextHolder;

    import javax.servlet.http.HttpServletRequest;
    import javax.servlet.http.HttpSession;
    import java.util.Enumeration;
    import java.util.Map;

    /**
     * Created by zkn on 2016/11/18.
     */
    @Component
    @Aspect
    public class WebControllerAop {

        //匹配com.zkn.learnspringboot.web.controller包及其子包下的所有类的所有方法
        @Pointcut("execution(* com.zkn.learnspringboot.web.controller..*.*(..))")
        public void executeService(){

        }

        /**
         * 前置通知，方法调用前被调用
         * @param joinPoint
         */
        @Before("executeService()")
        public void doBeforeAdvice(JoinPoint joinPoint){
            System.out.println("我是前置通知!!!");
            //获取目标方法的参数信息
            Object[] obj = joinPoint.getArgs();
            //AOP代理类的信息
            joinPoint.getThis();
            //代理的目标对象
            joinPoint.getTarget();
            //用的最多 通知的签名
            Signature signature = joinPoint.getSignature();
            //代理的是哪一个方法
            System.out.println(signature.getName());
            //AOP代理类的名字
            System.out.println(signature.getDeclaringTypeName());
            //AOP代理类的类（class）信息
            signature.getDeclaringType();
            //获取RequestAttributes
            RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
            //从获取RequestAttributes中获取HttpServletRequest的信息
            HttpServletRequest request = (HttpServletRequest) requestAttributes.resolveReference(RequestAttributes.REFERENCE_REQUEST);
            //如果要获取Session信息的话，可以这样写：
            //HttpSession session = (HttpSession) requestAttributes.resolveReference(RequestAttributes.REFERENCE_SESSION);
            Enumeration<String> enumeration = request.getParameterNames();
            Map<String,String> parameterMap = Maps.newHashMap();
            while (enumeration.hasMoreElements()){
                String parameter = enumeration.nextElement();
                parameterMap.put(parameter,request.getParameter(parameter));
            }
            String str = JSON.toJSONString(parameterMap);
            if(obj.length > 0) {
                System.out.println("请求的参数信息为："+str);
            }
        }

        /**
         * 后置返回通知
         * 这里需要注意的是:
         *      如果参数中的第一个参数为JoinPoint，则第二个参数为返回值的信息
         *      如果参数中的第一个参数不为JoinPoint，则第一个参数为returning中对应的参数
         * returning 限定了只有目标方法返回值与通知方法相应参数类型时才能执行后置返回通知，否则不执行，对于returning对应的通知方法参数为Object类型将匹配任何目标返回值
         * @param joinPoint
         * @param keys
         */
        @AfterReturning(value = "execution(* com.zkn.learnspringboot.web.controller..*.*(..))",returning = "keys")
        public void doAfterReturningAdvice1(JoinPoint joinPoint,Object keys){

            System.out.println("第一个后置返回通知的返回值："+keys);
        }

        @AfterReturning(value = "execution(* com.zkn.learnspringboot.web.controller..*.*(..))",returning = "keys",argNames = "keys")
        public void doAfterReturningAdvice2(String keys){

            System.out.println("第二个后置返回通知的返回值："+keys);
        }

        /**
         * 后置异常通知
         *  定义一个名字，该名字用于匹配通知实现方法的一个参数名，当目标方法抛出异常返回后，将把目标方法抛出的异常传给通知方法；
         *  throwing 限定了只有目标方法抛出的异常与通知方法相应参数异常类型时才能执行后置异常通知，否则不执行，
         *      对于throwing对应的通知方法参数为Throwable类型将匹配任何异常。
         * @param joinPoint
         * @param exception
         */
        @AfterThrowing(value = "executeService()",throwing = "exception")
        public void doAfterThrowingAdvice(JoinPoint joinPoint,Throwable exception){
            //目标方法名：
            System.out.println(joinPoint.getSignature().getName());
            if(exception instanceof NullPointerException){
                System.out.println("发生了空指针异常!!!!!");
            }
        }

        /**
         * 后置最终通知（目标方法只要执行完了就会执行后置通知方法）
         * @param joinPoint
         */
        @After("executeService()")
        public void doAfterAdvice(JoinPoint joinPoint){

            System.out.println("后置通知执行了!!!!");
        }

        /**
         * 环绕通知：
         *   环绕通知非常强大，可以决定目标方法是否执行，什么时候执行，执行时是否需要替换方法参数，执行完毕是否需要替换返回值。
         *   环绕通知第一个参数必须是org.aspectj.lang.ProceedingJoinPoint类型
         */
        @Around("execution(* com.zkn.learnspringboot.web.controller..*.testAround*(..))")
        public Object doAroundAdvice(ProceedingJoinPoint proceedingJoinPoint){
            System.out.println("环绕通知的目标方法名："+proceedingJoinPoint.getSignature().getName());
            try {//obj之前可以写目标方法执行前的逻辑
                Object obj = proceedingJoinPoint.proceed();//调用执行目标方法
                return obj;
            } catch (Throwable throwable) {
                throwable.printStackTrace();
            }
            return null;
        }
    }


完整的Controller类代码如下:


    package com.zkn.learnspringboot.web.controller;

    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;

    /**
     * Created by zkn on 2016/11/19.
     */
    @RestController
    @RequestMapping("/aop")
    public class AopTestController {

        @RequestMapping("/testBeforeService.do")
        public String testBeforeService(String key,String value){

            return "key="+key+"  value="+value;
        }
        @RequestMapping("/testAfterReturning.do")
        public String testAfterReturning(String key){

            return "key=: "+key;
        }
        @RequestMapping("/testAfterReturning01.do")
        public Integer testAfterReturning01(Integer key){

            return key;
        }
        @RequestMapping("/testAfterThrowing.do")
        public String testAfterThrowing(String key){

            throw new NullPointerException();
        }
        @RequestMapping("/testAfter.do")
        public String testAfter(String key){

            throw new NullPointerException();
        }
        @RequestMapping("/testAfter02.do")
        public String testAfter02(String key){

            return key;
        }
        @RequestMapping("/testAroundService.do")
        public String testAroundService(String key){

            return "环绕通知："+key;
        }
    }
