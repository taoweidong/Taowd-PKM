---
source: "http://blog.csdn.net/xiaoyu411502/article/details/47864969"
title: "Spring Boot 快速入门_springboot jar couldn't find template-CSDN博客"
fetched_at: "2026-10-05 15:32:22"
---

今天给大家介绍一下Spring Boot MVC，让我们学习一下如何利用Spring Boot快速的搭建一个简单的web应用。

###  环境准备

  * 一个称手的文本编辑器（例如Vim、Emacs、Sublime Text）或者IDE（Eclipse、Idea Intellij）
  * Java环境（JDK 1.7或以上版本）
  * Maven 3.0+（Eclipse和Idea IntelliJ内置，如果使用IDE并且不使用命令行工具可以不安装）

###  一个最简单的Web应用

使用Spring Boot框架可以大大加速Web应用的开发过程，首先在Maven项目依赖中引入`spring-boot-starter-web`：

`pom.xml`


    <?xml version="1.0" encoding="UTF-8"?>

      <modelVersion>4.0.0</modelVersion>

      <groupId>com.tianmaying</groupId>
      <artifactId>spring-web-demo</artifactId>
      <version>0.0.1-SNAPSHOT</version>
       jar

      <name>spring-web-demo</name>
      <description>Demo project for Spring WebMvc</description>


        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.2.5.RELEASE</version>
        <relativePath/>



         UTF-8
        <java.version>1.8</java.version>


      <dependencies>
        <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
      </dependencies>

      <build>


            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>


      </build>




接下来创建`src/main/java/Application.java`:


    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;

    @SpringBootApplication
    @RestController
    public class Application {

        @RequestMapping("/")
        public String greeting() {
            return "Hello World!";
        }

        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    }

运行应用：`mvn spring-boot:run`或在IDE中运行`main()`方法，在浏览器中访问[http://localhost:8080](http://localhost:8080/)，`Hello World!`就出现在了页面中。只用了区区十几行Java代码，一个Hello World应用就可以正确运行了，那么这段代码究竟做了什么呢？我们从程序的入口`SpringApplication.run(Application.class, args);`开始分析：

  1. `SpringApplication`是Spring Boot框架中描述Spring应用的类，它的`run()`方法会创建一个Spring应用上下文（Application Context）。另一方面它会扫描当前应用类路径上的依赖，例如本例中发现`spring-webmvc`（由 `spring-boot-starter-web`传递引入）在类路径中，那么Spring Boot会判断这是一个Web应用，并启动一个内嵌的Servlet容器（默认是Tomcat）用于处理HTTP请求。

  2. Spring WebMvc框架会将Servlet容器里收到的HTTP请求根据路径分发给对应的`@Controller`类进行处理，`@RestController`是一类特殊的`@Controller`，它的返回值直接作为HTTP Response的Body部分返回给浏览器。

  3. `@RequestMapping`注解表明该方法处理那些URL对应的HTTP请求，也就是我们常说的URL路由（routing)，请求的分发工作是有Spring完成的。例如上面的代码中`http://localhost:8080/`根路径就被路由至`greeting()`方法进行处理。如果访问`http://localhost:8080/hello`，则会出现`404 Not Found`错误，因为我们并没有编写任何方法来处理`/hello`请求。

###  使用`@Controller`实现URL路由

现代Web应用往往包括很多页面，不同的页面也对应着不同的URL。对于不同的URL，通常需要不同的方法进行处理并返回不同的内容。

####  匹配多个URL


    @RestController
    public class Application {

        @RequestMapping("/")
        public String index() {
            return "Index Page";
        }

        @RequestMapping("/hello")
        public String hello() {
            return "Hello World!";
        }
    }

`@RequestMapping`可以注解`@Controller`类：


    @RestController
    @RequestMapping("/classPath")
    public class Application {
        @RequestMapping("/methodPath")
        public String method() {
            return "mapping url is /classPath/methodPath";
        }
    }

`method`方法匹配的URL是`/classPath/methodPath"`。

提示

可以定义多个`@Controller`将不同URL的处理方法分散在不同的类中

####  URL中的变量——PathVariable

在Web应用中URL通常不是一成不变的，例如微博两个不同用户的个人主页对应两个不同的URL:`http://weibo.com/user1`，`http://weibo.com/user2`。我们不可能对于每一个用户都编写一个被`@RequestMapping`注解的方法来处理其请求，Spring MVC提供了一套机制来处理这种情况：


    @RequestMapping("/users/{username}")
    public String userProfile(@PathVariable("username") String username) {
        return String.format("user %s", username);
    }

    @RequestMapping("/posts/{id}")
    public String post(@PathVariable("id") int id) {
        return String.format("post %d", id);
    }

在上述例子中，URL中的变量可以用`{variableName}`来表示，同时在方法的参数中加上`@PathVariable("variableName")`，那么当请求被转发给该方法处理时，对应的URL中的变量会被自动赋值给被`@PathVariable`注解的参数（能够自动根据参数类型赋值，例如上例中的`int`）。

####  支持HTTP方法

对于HTTP请求除了其URL，还需要注意它的方法（Method）。例如我们在浏览器中访问一个页面通常是GET方法，而表单的提交一般是POST方法。`@Controller`中的方法同样需要对其进行区分：


    @RequestMapping(value = "/login", method = RequestMethod.GET)
    public String loginGet() {
        return "Login Page";
    }

    @RequestMapping(value = "/login", method = RequestMethod.POST)
    public String loginPost() {
        return "Login Post Request";
    }

###  模板渲染

在之前所有的`@RequestMapping`注解的方法中，返回值字符串都被直接传送到浏览器端并显示给用户。但是为了能够呈现更加丰富、美观的页面，我们需要将HTML代码返回给浏览器，浏览器再进行页面的渲染、显示。

一种很直观的方法是在处理请求的方法中，直接返回HTML代码，但是这样做的问题在于——一个复杂的页面HTML代码往往也非常复杂，并且嵌入在Java代码中十分不利于维护。更好的做法是将页面的HTML代码写在模板文件中，渲染后再返回给用户。为了能够进行模板渲染，需要将`@RestController`改成`@Controller`：


    import org.springframework.ui.Model;

    @Controller
    public class HelloController {

        @RequestMapping("/hello/{name}")
        public String hello(@PathVariable("name") String name, Model model) {
            model.addAttribute("name", name);
            return "hello"
        }
    }

在上述例子中，返回值`"hello"`并非直接将字符串返回给浏览器，而是寻找名字为`hello`的模板进行渲染，我们使用[Thymeleaf](http://www.thymeleaf.org/)模板引擎进行模板渲染，需要引入依赖：


    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>

接下来需要在默认的模板文件夹`src/main/resources/templates/`目录下添加一个模板文件`hello.html`：


    <!DOCTYPE HTML>
    <html xmlns:th="http://www.thymeleaf.org">
    <head>
        <title>Getting Started: Serving Web Content</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>

    </body>
    </html>

`th:text="'Hello, ' + ${name} + '!'"`也就是将我们之前在`@Controller`方法里添加至`Model`的属性`name`进行渲染，并放入` `标签中（因为`th:text`是` `标签的属性）。模板渲染还有更多的用法，请参考[Thymeleaf官方文档](http://www.thymeleaf.org/doc/tutorials/2.1/usingthymeleaf.html)。

###  处理静态文件

浏览器页面使用HTML作为描述语言，那么必然也脱离不了CSS以及JavaScript。为了能够浏览器能够正确加载类似`/css/style.css`, `/js/main.js`等资源，默认情况下我们只需要在`src/main/resources/static`目录下添加`css/style.css`和`js/main.js`文件后，Spring MVC能够自动将他们发布，通过访问`/css/style.css`, `/js/main.js`也就可以正确加载这些资源。
