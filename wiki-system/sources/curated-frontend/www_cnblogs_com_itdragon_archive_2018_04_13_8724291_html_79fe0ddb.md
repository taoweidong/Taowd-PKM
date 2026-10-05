---
source: "https://www.cnblogs.com/itdragon/archive/2018/04/13/8724291.html"
title: "Thymeleaf3语法详解和实战 - ITDragon龙 - 博客园"
fetched_at: "2026-10-05 15:32:15"
---

# Thymeleaf3语法详解

Thymeleaf是Spring boot推荐使用的模版引擎，除此之外常见的还有Freemarker和Jsp。Jsp应该是我们最早接触的模版引擎。而Freemarker工作中也很常见（[Freemarker教程](http://www.cnblogs.com/itdragon/p/7750903.html)）。今天我们从三个方面学习Thymeleaf的语法：有常见的TH属性，四种标准表达式用法，在SpringBoot中的应用。还在等什么，一起来学吧！

技术：Thymeleaf，SpringBoot

说明：为突出Thymeleaf3的语法知识，文章只提出与Thymeleaf有关的代码，完整代码请异步github，喜欢的朋友可以点个star，蟹蟹！

源码：<https://github.com/ITDragonBlog/daydayup/tree/master/Thymeleaf/spring-boot-thymeleaf>

好文推荐： <http://www.cnblogs.com/itdragon/p/8709948.html>

文章目录结构：
![文章目录结构](https://images2018.cnblogs.com/blog/806956/201804/806956-20180412175920781-874860611.png)

## 一、th属性

### 常用th属性解读

html有的属性，Thymeleaf基本都有，而常用的属性大概有七八个。其中th属性执行的优先级从1~8，数字越低优先级越高。

一、**th:text** ：设置当前元素的文本内容，相同功能的还有**th:utext** ，两者的区别在于前者不会转义html标签，后者会。优先级不高：order=7

二、**th:value** ：设置当前元素的value值，类似修改指定属性的还有**th:src** ，**th:href** 。优先级不高：order=6

三、**th:each** ：遍历循环元素，和th:text或th:value一起使用。注意该属性修饰的标签位置，详细往后看。优先级很高：order=2

四、**th:if** ：条件判断，类似的还有**th:unless** ，**th:switch** ，**th:case** 。优先级较高：order=3

五、**th:insert** ：代码块引入，类似的还有**th:replace** ，**th:include** ，三者的区别较大，若使用不恰当会破坏html结构，常用于公共代码块提取的场景。优先级最高：order=1

六、**th:fragment** ：定义代码块，方便被th:insert引用。优先级最低：order=8

七、**th:object** ：声明变量，一般和*{}一起配合使用，达到偷懒的效果。优先级一般：order=4

八、**th:attr** ：修改任意属性，实际开发中用的较少，因为有丰富的其他th属性帮忙，类似的还有th:attrappend，th:attrprepend。优先级一般：order=5

### 常用th属性使用

使用Thymeleaf属性需要注意点以下五点：

一、若要使用Thymeleaf语法，首先要声明名称空间： `xmlns:th="http://www.thymeleaf.org"`

二、设置文本内容 th:text，设置input的值 th:value，循环输出 th:each，条件判断 th:if，插入代码块 th:insert，定义代码块 th:fragment，声明变量 th:object

三、th:each 的用法需要格外注意，打个比方：如果你要循环一个div中的p标签，则th:each属性必须放在p标签上。若你将th:each属性放在div上，则循环的是将整个div。

四、变量表达式中提供了很多的内置方法，该内置方法是用#开头，请不要与#{}消息表达式弄混。

五、th:insert，th:replace，th:include 三种插入代码块的效果相似，但区别很大。


    <!DOCTYPE html>
    <!--名称空间-->
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8">
        <title>Thymeleaf 语法</title>
    </head>
    <body>
        <h2>ITDragon Thymeleaf 语法</h2>
        <!--th:text 设置当前元素的文本内容，常用，优先级不高-->



        <!--th:value 设置当前元素的value值，常用，优先级仅比th:text高-->
        <input type="text" th:value="${thValue}" />

        <!--th:each 遍历列表，常用，优先级很高，仅此于代码块的插入-->
        <!--th:each 修饰在div上，则div层重复出现，若只想p标签遍历，则修饰在p标签上-->
          <!-- 遍历整个div-p，不推荐-->


          <!--只遍历p，推荐使用-->



        <!--th:if 条件判断，类似的有th:switch，th:case，优先级仅次于th:each, 其中#strings是变量表达式的内置方法-->


        <!--th:insert 把代码块插入当前div中，优先级最高，类似的有th:replace，th:include，~{} ：代码块表达式 -->


        <!--th:object 声明变量，和*{} 一起使用-->

             ID:   <!--th:text="${thObject.id}"-->
             TH:   <!--${thObject.thName}-->
             DE:   <!--${thObject.desc}-->


    </body>
    </html>


后台给负责给变量赋值，和跳转页面。


    import com.itdragon.entities.ThObject;
    import org.springframework.stereotype.Controller;
    import org.springframework.ui.ModelMap;
    import org.springframework.web.bind.annotation.RequestMapping;
    import java.util.ArrayList;
    import java.util.Arrays;
    import java.util.List;

    @Controller
    public class ThymeleafController {

        @RequestMapping("thymeleaf")
        public String thymeleaf(ModelMap map) {
            map.put("thText", "th:text 设置文本内容 <b>加粗</b>");
            map.put("thUText", "th:utext 设置文本内容 <b>加粗</b>");
            map.put("thValue", "thValue 设置当前元素的value值");
            map.put("thEach", Arrays.asList("th:each", "遍历列表"));
            map.put("thIf", "msg is not null");
            map.put("thObject", new ThObject(1L, "th:object", "用来偷懒的th属性"));
            return "grammar/thymeleaf";
        }
    }


## 二、标准表达式语法

`${...}` 变量表达式，Variable Expressions

`@{...}` 链接表达式，Link URL Expressions

`#{...}` 消息表达式，Message Expressions

`~{...}` 代码块表达式，Fragment Expressions

`*{...}` 选择变量表达式，Selection Variable Expressions

变量表达式使用频率最高，其功能也是非常的丰富。所以我们先从简单的代码块表达式开始，然后是消息表达式，再是链接表达式，最后是变量表达式，随带介绍选择变量表达式。

### ~{...} 代码块表达式

#### 支持两种语法结构

推荐：`~{templatename::fragmentname}`

支持：`~{templatename::#id}`

templatename：模版名，Thymeleaf会根据模版名解析完整路径：/resources/templates/templatename.html，要注意文件的路径。

fragmentname：片段名，Thymeleaf通过th:fragment声明定义代码块，即：`th:fragment="fragmentname"`

id：HTML的id选择器，使用时要在前面加上#号，不支持class选择器。

#### 代码块表达式的使用

代码块表达式需要配合th属性（th:insert，th:replace，th:include）一起使用。

**th:insert** ：将代码块片段整个插入到使用了th:insert的HTML标签中，

**th:replace** ：将代码块片段整个替换使用了th:replace的HTML标签中，

**th:include** ：将代码块片段包含的内容插入到使用了th:include的HTML标签中，

用一个官方例子来区分三者的不同，第三部分会通过实战再次用到该知识。


    <!--th:fragment定义代码块标识-->
    <footer th:fragment="copy">
    © 2011 The Good Thymes Virtual Grocery
    </footer>

    <!--三种不同的引入方式-->




    <!--th:insert是在div中插入代码块，即多了一层div-->

        <footer>
        © 2011 The Good Thymes Virtual Grocery
        </footer>

    <!--th:replace是将代码块代替当前div，其html结构和之前一致-->
    <footer>
    © 2011 The Good Thymes Virtual Grocery
    </footer>
    <!--th:include是将代码块footer的内容插入到div中，即少了一层footer-->

    © 2011 The Good Thymes Virtual Grocery



### #{...} 消息表达式

消息表达式一般用于国际化的场景。结构：`th:text="#{msg}"` 。会在第三部分的实战详细介绍。

### @{...} 链接表达式

#### 链接表达式好处

不管是静态资源的引用，form表单的请求，凡是链接都可以用`@{...}` 。这样可以动态获取项目路径，即便项目名变了，依然可以正常访问


    #修改项目名，链接表达式会自动修改路径，避免资源文件找不到
    server.context-path=/itdragon


#### 链接表达式结构

无参：`@{/xxx}`

有参：`@{/xxx(k1=v1,k2=v2)}` 对应url结构：`xxx?k1=v1&k2=v2`

引入本地资源：`@{/项目本地的资源路径}`

引入外部资源：`@{/webjars/资源在jar包中的路径}`

列举：第三部分的实战引用会详细使用该表达式


    <link th:href="@{/webjars/bootstrap/4.0.0/css/bootstrap.css}" rel="stylesheet">
    <link th:href="@{/main/css/itdragon.css}" rel="stylesheet">
    <form class="form-login" th:action="@{/user/login}" th:method="post" >
    <a class="btn btn-sm" th:href="@{/login.html(l='zh_CN')}">中文</a>
    <a class="btn btn-sm" th:href="@{/login.html(l='en_US')}">English</a>


### ${...}变量表达式

变量表达式有丰富的内置方法，使其更强大，更方便。

#### 变量表达式功能

一、可以获取对象的属性和方法

二、可以使用ctx，vars，locale，request，response，session，servletContext内置对象

三、可以使用dates，numbers，strings，objects，arrays，lists，sets，maps等内置方法（重点介绍）

#### 常用的内置对象

一、**ctx** ：上下文对象。

二、**vars** ：上下文变量。

三、**locale** ：上下文的语言环境。

四、**request** ：（仅在web上下文）的 HttpServletRequest 对象。

五、**response** ：（仅在web上下文）的 HttpServletResponse 对象。

六、**session** ：（仅在web上下文）的 HttpSession 对象。

七、**servletContext** ：（仅在web上下文）的 ServletContext 对象

这里以常用的Session举例，用户刊登成功后，会把用户信息放在Session中，Thymeleaf通过内置对象将值从session中获取。


    // java 代码将用户名放在session中
    session.setAttribute("userinfo",username);
    // Thymeleaf通过内置对象直接获取
    th:text="${session.userinfo}"


#### 常用的内置方法

一、**strings** ：字符串格式化方法，常用的Java方法它都有。比如：equals，equalsIgnoreCase，length，trim，toUpperCase，toLowerCase，indexOf，substring，replace，startsWith，endsWith，contains，containsIgnoreCase等

二、**numbers** ：数值格式化方法，常用的方法有：formatDecimal等

三、**bools** ：布尔方法，常用的方法有：isTrue，isFalse等

四、**arrays** ：数组方法，常用的方法有：toArray，length，isEmpty，contains，containsAll等

五、**lists** ，**sets** ：集合方法，常用的方法有：toList，size，isEmpty，contains，containsAll，sort等

六、**maps** ：对象方法，常用的方法有：size，isEmpty，containsKey，containsValue等

七、**dates** ：日期方法，常用的方法有：format，year，month，hour，createNow等

文章底部提供了对应的官网链接


    <!DOCTYPE html>
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8">
        <title>ITDragon Thymeleaf 内置方法</title>
    </head>
    <body>
        <h2>ITDragon Thymeleaf 内置方法</h2>
        <h3>#strings </h3>

             Old Str :
             toUpperCase :
             toLowerCase :
             equals :
             equalsIgnoreCase :
             indexOf :
             substring :
             replace :
             startsWith :
             contains :


        <h3>#numbers </h3>

             formatDecimal 整数部分随意，小数点后保留两位，四舍五入:
             formatDecimal 整数部分保留五位数，小数点后保留两位，四舍五入:


        <h3>#bools </h3>




        <h3>#arrays </h3>

             length :
             contains :
             containsAll :

        <h3>#lists </h3>

             size :
             contains :
             sort :

        <h3>#maps </h3>

             size :
             containsKey :
             containsValue :

        <h3>#dates </h3>

             format :
             custom format :
             day :
             month :
             monthName :
             year :
             dayOfWeekName :
             hour :
             minute :
             second :
             createNow :

    </body>
    </html>


后台给负责给变量赋值，和跳转页面。


    @RequestMapping("varexpressions")
    public String varexpressions(ModelMap map) {
      map.put("itdragonStr", "itdragonBlog");
      map.put("itdragonBool", true);
      map.put("itdragonArray", new Integer[]{1,2,3,4});
      map.put("itdragonList", Arrays.asList(1,3,2,4,0));
      Map itdragonMap = new HashMap();
      itdragonMap.put("thName", "${#...}");
      itdragonMap.put("desc", "变量表达式内置方法");
      map.put("itdragonMap", itdragonMap);
      map.put("itdragonDate", new Date());
      map.put("itdragonNum", 888.888D);
      return "grammar/varexpressions";
    }


## 三、Thymeleaf在SpringBoot应用

Thymeleaf是Spring Boot 官方推荐使用的模版引擎，这也意味着用Thymeleaf比其他模版引擎更简单。

开发步骤：

第一步：引入Thymeleaf依赖。

第二步： 提取公共页面，提高代码的重用性，统一页面风格。

第三步：页面显示和国际化功能

### 引入Thymeleaf

pom.xml 引入Thymeleaf的依赖，并确定其版本



       UTF-8
       UTF-8
      <java.version>1.8</java.version>
      <thymeleaf.version>3.0.9.RELEASE</thymeleaf.version>
      <thymeleaf-layout-dialect.version>2.2.2</thymeleaf-layout-dialect.version>

    <dependencies>
      <dependency> <!--引入模版引擎thymeleaf-->
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
      </dependency>
    </dependencies>


### 提取公共页面

为了统一页面风格，提高页面的复用率，我们一般都会提取公共页面。之前在文章中介绍了SiteMesh的使用，今天用Thymeleaf来实现。

统一规范引入的资源文件


    <!DOCTYPE html>
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    	<head th:fragment="common-head">
    		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    		<meta name="viewport" content="initial-scale=1.0, width=device-width, user-scalable=no" />
    		<title>ITDragon系统</title>
    		<link type="image/x-icon" href="images/favicon.ico" rel="shortcut icon">
    		<link th:href="@{/sb-admin-1.0.4/css/bootstrap.min.css}" rel="stylesheet">
    	    <link th:href="@{/sb-admin-1.0.4/css/sb-admin.css}" rel="stylesheet">
    	    <link th:href="@{/sb-admin-1.0.4/css/plugins/morris.css}" rel="stylesheet">
    	    <link th:href="@{/sb-admin-1.0.4/font-awesome/css/font-awesome.min.css}" rel="stylesheet">





    	</head>
    </html>


统一左侧菜单栏


    <!DOCTYPE html>
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
    <header id="header" th:fragment="common-header">
        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">

                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                     Toggle navigation



                </button>
                <a class="navbar-brand" href="/dashboard">ITDragon sb-admin-1.0.4</a>

            <!--和知识点没关系的代码，这里就补贴出来了，完整代码请异步github-->
            <!-- Sidebar Menu Items - These collapse to the responsive navigation menu on small screens -->

                <ul class="nav navbar-nav side-nav itdragon-nav">
                    <li th:class="${activeUrl=='dashboard'?'nav-link active':'nav-link'}">
                        <a th:href="@{/dashboard}"><i class="fa fa-fw fa-dashboard"></i> Dashboard</a>
                    </li>
                    <li th:class="${activeUrl=='employees'?'nav-link active':'nav-link'}">
                        <a th:href="@{/employees}"><i class="fa fa-fw fa-bar-chart-o"></i> Employees</a>
                    </li>
                </ul>

            <!-- /.navbar-collapse -->
        </nav>
    </header>
    </body>
    </html>


以上代码用到了三个知识点：

一、使用链接表达式引入本地的资源文件，若引入第三方外部资源文件，可以通过webjars（将资源文件打成jar包放在项目中）方式引入。

二、使用th:fragment标识需要被引用的代码块，也可以用id选择器但不推荐。

三、activeUrl变量是通过代码块表达式在其他页面传入的变量，这也是代码块表达式强大的一个功能。

### 页面显示和国际化

Spring Boot 实现国际化步骤：

第一步：准备好国际化文件，至少三分（系统默认，中文，英文）

第二步：在Spring Boot全局配置文件中，指定国际化文件路径，

第三步：自定义Locale Resolver

第四步：在页面上使用消息表达式输出国际化内容

这里只贴出第四步的代码，前三步以及完整代码请异步github


    <!DOCTYPE html>
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    <head th:replace="~{commons/default::common-head}">
    	<meta name="viewport" content="initial-scale=1.0, width=device-width, user-scalable=no" />
    	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    	<meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1" />
    	<meta http-equiv="X-UA-Compatible" content="IE=8" />
    	<title>员工列表</title>
    </head>
    <body>

    	<header th:replace="~{commons/header::common-header(activeUrl='employees')}"></header>


    			<!-- Page Heading -->


    					<h1 class="page-header" th:text="#{employees}"></h1>
    					<ol class="breadcrumb">
    						<li><i class="fa fa-dashboard"></i> <a th:href="@{/dashboard}" th:text="#{dashboard}"></a>
    						</li>
    						<li class="active"><i class="fa fa-table"></i>   </li>
    					</ol>





    						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
    						<i class="fa fa-info-circle"></i> <strong th:text="${message}"></strong>



    			<!-- /.row -->


    					<h2 th:text="#{employees}"></h2>

    						<a class="pull-right btn" th:href="@{/employee}" th:text="#{add.employees}"></a>
    						<table class="table table-striped table-sm">
    							<thead>
    							<tr>
    								<th th:text="#{id}"></th>
    								<th th:text="#{last.name}"></th>
    								<th th:text="#{email}"></th>
    								<th th:text="#{gender}"></th>
    								<th th:text="#{department}"></th>
    								<th th:text="#{position}"></th>
    								<th th:text="#{birth}"></th>
    								<th th:text="#{operation}"></th>
    							</tr>
    							</thead>
    							<tbody>
    							<tr th:each="emp:${employees}">
    								<td th:text="${emp.id}"></td>
    								<td>[[${emp.lastName}]]</td>
    								<td th:text="${emp.email}"></td>
    								<td th:text="${emp.gender}==0?#{female}:#{male}"></td>
    								<td th:text="${emp.department.departmentName}"></td>
    								<td th:text="${emp.department.position}"></td>
    								<td th:text="${#dates.format(emp.birth, 'yyyy-MM-dd HH:mm')}"></td>
    								<td>
    									<a class="btn btn-sm btn-success" th:href="@{/employee/}+${emp.id}" th:text="#{edit}"></a>
    									<a class="btn btn-sm btn-danger deleteBtn" th:href="@{/employee/}+${emp.id}" th:text="#{delete}"></a>
    								</td>
    							</tr>
    							</tbody>
    						</table>



    			<!-- /.row -->



    </body>
    </html>


以上代码用到了知识点：

一、页面通过代码块表达式引入公共代码块，并传入参数给公共代码块文件。

二、页面使用消息表达式输出国际化内容。

三、使用th:if属性条件判断，使用内置方法#strings.isEmpty 判断参数是否为空，使用内置方法#dates.format 格式化参数

四、使用th:each属性循环遍历，注意该属性修改在tr标签上。并使用th:text属性给td标签赋值

## 四、总结

**一、Thymeleaf 是Spring Boot 官方推荐的Java模版引擎框架，其文件扩展名为.html**

**二、Thymeleaf 几乎支持所有的html属性，用于赋值的th:text和th:value，用于循环遍历的th:each，用于条件判断的th:if**

**三、Thymeleaf 提供四种标准的表达式，有丰富内置方法的${}，用于国际化的#{}，用于代码插入的~{}，用于处理链接的@{}**

**四、一定要注意循环遍历的th:each和代码插入的th:insert用法，尽量避免破坏html结构的细节问题**

参考文献：

### [Sort 坑爹的字符串排序](https://mp.weixin.qq.com/s?__biz=MzIzMzU2MzM1Mw==&mid=2247484915&idx=1&sn=a8ee3428db9e5d6119fd83d7e94f133e&chksm=e882f045dff5795346c28b20fc6ae0c332b41ced1d6e0f84d4983cd48dfba9015de615d398b2&token=592501673&lang=zh_CN#rd)

<https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#appendix-a-expression-basic-objects>

<https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#appendix-b-expression-utility-objects>

文章到这里就结束了。如果文章对你有帮助，可以点个"推荐"，也可以"关注"我，获得更多丰富的知识。

这里是博客文章目录一栏表中的部分内容，如果有感兴趣的内容可以点击右边的链接： <http://www.cnblogs.com/itdragon/p/8709948.html>

![文章目录](https://images2018.cnblogs.com/blog/806956/201804/806956-20180404120547967-1298773028.png)
