---
source: "http://www.cnblogs.com/csonezp/p/3642817.html"
title: "Eclipse中Maven+Spring3.2.8+SpringMVC HelloWorld项目 - csonezp - 博客园"
fetched_at: "2026-10-05 15:30:14"
---

本文适合有一定spring和springmvc基础，并想使用Maven管理项目的人。

源码打包：<http://pan.baidu.com/s/1hqurUcs>

转载请声明出处（<http://www.cnblogs.com/csonezp/>）

## 准备工作

确保你的eclipse已经整合M2E插件，即新建项目有Maven选项。不要用Eclipse自带的Maven，在设置中将本地Maven添加进去。

> [![image](https://images0.cnblogs.com/blog/424424/201404/031329157505870.png)](https://images0.cnblogs.com/blog/424424/201404/031329146258313.png)

我的Maven本地库备份：<http://pan.baidu.com/s/1o6yj0Gq>

里面基本包含所有Spring，Hibernate，Struts需要用到的依赖。下载后解压到自己的.m2文件夹中即可。

## 建立项目

在Eclipse中新建一个Maven项目，Select Archetype时选择maven-archetype-webapp。

修改pom.xml，最终结果如下：



        <modelVersion>4.0.0</modelVersion>
        <groupId>zp.maven</groupId>
        <artifactId>test</artifactId>
         war
        <version>0.0.1-SNAPSHOT</version>
        <name>test Maven Webapp</name>
        <url>http://maven.apache.org</url>
        <dependencies>
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>4.7</version>
                <scope>test</scope>
            </dependency>
            <dependency>
                <groupId>jstl</groupId>
                <artifactId>jstl</artifactId>
                <version>1.2</version>
            </dependency>

            <dependency>
                <groupId>taglibs</groupId>
                <artifactId>standard</artifactId>
                <version>1.1.2</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-web</artifactId>
                <version>3.2.8.RELEASE</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-webmvc</artifactId>
                <version>3.2.8.RELEASE</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-aspects</artifactId>
                <version>3.2.8.RELEASE</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-orm</artifactId>
                <version>3.2.8.RELEASE</version>
            </dependency>
            <dependency>
                <groupId>org.aspectj</groupId>
                <artifactId>aspectjrt</artifactId>
                <version>1.6.12</version>
            </dependency>

            <dependency>
                <groupId>org.hibernate</groupId>
                <artifactId>hibernate-core</artifactId>
                <version>4.3.4.Final</version>
            </dependency>

            <dependency>
                <groupId>commons-pool</groupId>
                <artifactId>commons-pool</artifactId>
                <version>1.6</version>
            </dependency>

            <dependency>
                <groupId>c3p0</groupId>
                <artifactId>c3p0</artifactId>
                <version>0.9.1</version>
            </dependency>

            <dependency>
                <groupId>commons-pool</groupId>
                <artifactId>commons-pool</artifactId>
                <version>1.6</version>
            </dependency>
            <dependency>
                <groupId>cglib</groupId>
                <artifactId>cglib</artifactId>
                <version>2.2.2</version>
            </dependency>

            <dependency>
                <groupId>commons-dbcp</groupId>
                <artifactId>commons-dbcp</artifactId>
                <version>1.4</version>
            </dependency>
            <dependency>
                <groupId>commons-dbcp</groupId>
                <artifactId>commons-dbcp</artifactId>
                <version>1.4</version>
            </dependency>
            <dependency>
                <groupId>javaee</groupId>
                <artifactId>javaee-api</artifactId>
                <version>5</version>
            </dependency>
        </dependencies>
        <build>


                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <configuration>
                        <source>1.6</source>
                        <target>1.6</target>
                    </configuration>


            <finalName>test</finalName>
        </build>


dependences标签中是spring和hibernate需要用的的所有依赖，其中javaee-api可以换成 javax:javaee-web-api:6.0。build标签中是将项目设为java1.6编译。

然后，用资源管理器打开项目的根目录中的.setting文件夹，修改其中的org.eclipse.wst.common.project.facet.core.xml文件，改为：


    <?xml version="1.0" encoding="UTF-8"?>
    <faceted-project>
      <fixed facet="wst.jsdt.web"/>
      <installed facet="java" version="1.6"/>
      <installed facet="jst.web" version="3.0"/>
      <installed facet="wst.jsdt.web" version="1.0"/>
    </faceted-project>

此时项目即设置为servlet3.0的web项目。

重启eclipse，更新项目（右键点项目-maven-update project）。

下面的部分是从网上复制的，不想打了。其中add source folder可以换成在build path的source选项卡中修改。

\--------------------------------------------分割线-----------------------------------------------------

#### 2、配置Maven项目

接下来就需要更改好多配置了。

##### 2.1 添加Source文件夹

接下来需要添加src/main/java，src/test/java ，src/test/resources三个文件夹。右键项目根目录点击New -> Source Folder，

建出这三个文件夹。注意不是建普通的Folder，而是Source Folder。

![](http://dl.iteye.com/upload/attachment/357980/3a50a05a-d6c2-3570-a7b7-6c4351d1c84b.png)

![](http://dl.iteye.com/upload/attachment/357982/f6031745-c5b6-3eaa-bed5-7d00bce91caa.png)

##### 2.2 更改class路径

右键项目，Java Build Path -> Source

下面应该有4个文件夹。src/main/java，src/main/resources，src/test/java ，src/test/resources。

双击每个文件夹的Output folder，选择路径。

src/main/java，src/main/resources，选择target/classes;

src/test/java ，src/test/resources, 选择target/test-classes;

选上Allow output folders for source folders.

\--------------------------------------------分割线-----------------------------------------------------

此时Maven Web项目基本骨架已经完成，下面要进行的就是开发部分了。

首先，要修改Web.xml文件（位于webapp/WEB-INF下），最终结果如下：


    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" id="WebApp_ID" version="3.0">



      <display-name>Archetype Created Web Application</display-name>
      <context-param>
             contextConfigLocation

                classpath:spring-config.xml

        </context-param>

        <listener>
            <listener-class>
                org.springframework.web.context.ContextLoaderListener
            </listener-class>
        </listener>
        <!-- Spring配置文件结束 -->


        <filter>
            <filter-name>Encoding</filter-name>
            <filter-class>
                org.springframework.web.filter.CharacterEncodingFilter
            </filter-class>
            <init-param>
                 encoding
                 utf8
            </init-param>
        </filter>
        <filter-mapping>
            <filter-name>Encoding</filter-name>
            <url-pattern>/*</url-pattern>
        </filter-mapping>


        <!-- Spring MVC配置开始 -->
        <servlet>
            <servlet-name>spring</servlet-name>
            <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
            <init-param>
                 contextConfigLocation
                 classpath:spring-servlet.xml
            </init-param>
            <load-on-startup>1</load-on-startup>
        </servlet>

        <servlet-mapping>
            <servlet-name>spring</servlet-name>
            <url-pattern>*.html</url-pattern>
        </servlet-mapping>
        <!-- Spring MVC配置结束-->
    </web-app>

其中涉及的Spring和SpringMVC设置均为个人喜好，你可以根据自己的习惯更改。其中classpath:spring-config.xml 和classpath:spring-servlet.xml分表指向Spring配置文件和SrpingMVC配置文件的位置，本文中即为两者都在ClassPath下。如果想要跨模块引用，则需将classpath：xxx改为classpath*:XXX。

在src/main/resources下建立classpath:spring-config.xml 文件


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context"
        xmlns:aop="http://www.springframework.org/schema/aop" xmlns:p="http://www.springframework.org/schema/p"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
               http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
               http://www.springframework.org/schema/context
               http://www.springframework.org/schema/context/spring-context-3.0.xsd
                http://www.springframework.org/schema/aop
               http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">
        <context:annotation-config />
        <context:component-scan base-package="com.zp.test" >
            <!-- <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/> -->
        </context:component-scan>
    </beans>

代码就不多解释了，不懂的再看看spring的基础配置。

在src/main/resources下建立classpath:spring-servlet.xml 文件


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:p="http://www.springframework.org/schema/p"
        xmlns:context="http://www.springframework.org/schema/context"
        xmlns:util="http://www.springframework.org/schema/util"
        xmlns:mvc="http://www.springframework.org/schema/mvc"
        xsi:schemaLocation="
            http://www.springframework.org/schema/util
            http://www.springframework.org/schema/util/spring-util-3.0.xsd
            http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context-3.0.xsd
            http://www.springframework.org/schema/mvc
           http://www.springframework.org/schema/mvc/spring-mvc-3.0.xsd" >

             <context:annotation-config />
        <context:component-scan base-package="com.zp.test.controller">
            <context:include-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        </context:component-scan>

            <bean id="defaultViewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver" p:order="3">




        </bean>

    </beans>

此时Spring和SpringMVC配置已经完成。

然后在src/main/java/YouPackage下建立controller，service，service.impl三个包。

在service包中添加HelloWorldService接口


    package com.zp.test.service;
    public interface HelloWorldService {
         public String getNewName(String userName);
    }

service.impl中添加HelloWorldServiceImpl类


    package com.zp.test.service.impl;

    import org.springframework.stereotype.Service;

    import com.zp.test.service.HelloWorldService;

    @Service
    public class HelloWorldServiceImpl implements HelloWorldService {

        @Override
        public String getNewName(String userName) {
            return "hello spring!"+userName;
        }

    }

此服务的功能就是将传过来的参数前面加上Hello spring。

controller中添加HelloWorldController类


    package com.zp.test.controller;

    import javax.servlet.http.HttpServletRequest;

    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Controller;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RequestParam;

    import com.zp.test.service.HelloWorldService;

    @Controller
    public class HelloWorldController {
         @Autowired
         private HelloWorldService helloWorldService;


         @RequestMapping("helloworld")
         public String getNewName(@RequestParam("userName") String userName, HttpServletRequest request){

                String newUserName = helloWorldService.getNewName(userName);

                request.setAttribute("newUserName", newUserName);

                return "helloworld";

         }

    }

控制器作用是将httprequest传过来的参数通过HelloWorldService加上hello spring后返回给helloworld.jsp，由其显示出来。

后台部分完成。

前台：

index.jsp:


    <%@ page language="java" contentType="text/html; charset=UTF-8"
        pageEncoding="UTF-8"%>
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Insert title here</title>
    </head>
    <body>
    <form action="helloworld.html" method="post">

    请输入姓名：<input type="text" name="userName" />

    <input type="submit" value="提交" />



    </form>
    </body>
    </html>

helloworld.jsp:


    <%@ page language="java" contentType="text/html; charset=UTF-8"
        pageEncoding="UTF-8"%>
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Insert title here</title>
    </head>
    <body>
    <h1><%=request.getAttribute("newUserName")%></h1>
    </body>
    </html>

两者都在webapp根目录下建立。

项目完成，run on service或者打包发布到本地tomcat即可运行。
