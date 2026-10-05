---
source: "http://hotstrong.iteye.com/blog/1160153"
title: "使用Spring Security实现权限管理 - Java软件工程师之路 - ITeye博客"
fetched_at: "2026-10-05 15:32:31"
---

[首页](https://www.iteye.com/) [资讯](https://www.iteye.com/news) [精华](https://www.iteye.com/magazines) [论坛](https://www.iteye.com/forums) [问答](https://www.iteye.com/ask) [博客](https://www.iteye.com/blogs) [专栏](https://www.iteye.com/blogs/subjects) [群组](https://www.iteye.com/groups) [下载](https://www.iteye.com/resources)

* __搜索

[您还未登录!](/login "登录") [登录](/login)

`

[![HotStrong的博客](https://www.iteye.com/upload/logo/user/459088/186169f8-08f3-381b-a3c2-e1f7b49ecf24.jpg?1717537742)](https://www.iteye.com/blog/user/hotstrong)

HotStrong

  * 浏览: 522047 次
  * 性别: ![Icon_minigender_1](https://www.iteye.com/images/icon_minigender_1.gif?1652290086)
  * 来自: 成都
  * ![](/images/status/offline.gif)

##### 最近访客  [更多访客>>](/blog/user_visits)

[![一往无前bhz的博客](https://www.iteye.com/upload/logo/user/1035580/ba61d431-5db6-3261-86b7-1324d61639d9-thumb.jpg?1717537491)](https://www.iteye.com/blog/user/849622692)

[一往无前bhz](https://www.iteye.com/blog/user/849622692 "一往无前bhz")

[![草料场的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/pre)

[草料场](https://www.iteye.com/blog/user/pre "草料场")

[![dahai533418的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/dahai533418)

[dahai533418](https://www.iteye.com/blog/user/dahai533418 "dahai533418")

[![dongguangming88的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/dongguangming88)

[dongguangming88](https://www.iteye.com/blog/user/dongguangming88 "dongguangming88")

##### 博主相关

* [博客](https://www.iteye.com/blog/user/hotstrong)
* [微博](/weibo)
* [相册](/album)
* [收藏](/link)
* [留言](/blog/guest_book)
* [关于我](/blog/profile)

##### 文章分类

  * [全部博客 (34)](/blog/user/hotstrong)
  * [0、关于本站 (1)](/category/152942)
  * [1、关于参考资料 (1)](/category/153079)
  * [2、Java基础 (2)](/category/153078)
  * [3、数据库基础 (9)](/category/153080)
  * [4、C/S系统开发 (0)](/category/153081)
  * [5、HTML/JavaScript (11)](/category/152939)
  * [6、JSP/Servlet (0)](/category/153082)
  * [7、B/S系统开发 (0)](/category/153083)
  * [8、Java框架技术 (8)](/category/153084)
  * [9、综合项目设计 (1)](/category/152941)
  * [10、其他 (1)](/category/301021)

##### 社区版块

  * [我的资讯](/blog/news) ( 0)
  * [我的论坛](/blog/post) ( 0)
  * [我的问答](/blog/answered_problems) ( 0)

##### 存档分类

  * [2013-12](/blog/monthblog/2013-12) ( 2)
  * [2012-02](/blog/monthblog/2012-02) ( 1)
  * [2011-12](/blog/monthblog/2011-12) ( 2)
  * [更多存档...](/blog/monthblog_more)

##### 最新评论

  * [hsluoyz](https://www.iteye.com/blog/user/hsluoyz "hsluoyz")： 现在新推出了一个权限框架，叫jCasbin（https://g ...
[使用Spring Security实现权限管理](/blog/1160153#bc2403130)
  * [woohuu](https://www.iteye.com/blog/user/woohuu "woohuu")： 过来学习，结合楼主的分享，自己试一试，谢谢分享
[使用Spring Security实现权限管理](/blog/1160153#bc2402190)
  * [nlilewy](https://www.iteye.com/blog/user/nlilewy "nlilewy")： 布置好了项目和数据库弄好了，但是登录就报这个错org.spri ...
[Spring AOP 完成日志记录](/blog/1330046#bc2395162)
  * [zyaaa117203](https://www.iteye.com/blog/user/zyaaa117203 "zyaaa117203")： 请问使用ajax之后那个spring security的权限管 ...
[使用ajax gson增强用户体验](/blog/1164379#bc2395150)
  * [it1990eye0920](https://www.iteye.com/blog/user/it1990eye0920 "it1990eye0920")：
[Spring AOP 完成日志记录](/blog/1330046#bc2394589)

[HotStrong](https://www.iteye.com/blog/user/hotstrong)

###  使用Spring Security实现权限管理 __

**博客分类：**
  * [8、Java框架技术](/category/153084)

阅读更多

**使用Spring Security实现权限管理**

**1、技术目标**

  * 了解并创建Security框架所需数据表
  * 为项目添加Spring Security框架
  * 掌握Security框架配置
  * 应用Security框架为项目的CRUD操作绑定权限

**注意：本文所用项目为"影片管理"，参看**

**[http://hotstrong.iteye.com/blog/1156785](/blog/1156785)**

**2、权限管理需求描述**

  * 为系统中的每个操作定义权限，如定义4个权限：
1）超级权限，可以使用所有操作
2）添加影片权限
3）修改影片权限
4）删除影片权限
  * 为系统设置管理员帐号、密码
  * 为系统创建权限组，每个权限组可以配置多个操作权限，如创建2个权限组：
1）"Administrator"权限组，具有超级权限
2）"影片维护"权限组，具有添加影片、修改影片权限
  * 可将管理员加入权限组，管理员登录后具备权限组所对应操作权限
  * 管理员可不属于某权限组，可为管理员直接分配权限

**3、使用准备**

**3.1）在数据库中创建6张表**

t_admin 管理员帐号表

t_role权限表

t_group 权限组表

t_group_role权限组对应权限表

t_group_user管理员所属权限组表

t_user_role管理员对应权限表

**建表SQL语句如下：**


    SET FOREIGN_KEY_CHECKS=0;

    	------------------------------

    	-- 创建管理员帐号表t_admin

    	-- ----------------------------

    	CREATE TABLE `t_admin` (

    	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,

    	  `passwd` varchar(12) NOT NULL DEFAULT '' COMMENT '用户密码',

    	  `nickname` varchar(20) NOT NULL DEFAULT '' COMMENT '用户名字',

    	  `phoneno` varchar(32) NOT NULL DEFAULT '' COMMENT '电话号码',

    	  PRIMARY KEY (`id`)

    	) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;



    	-- ----------------------------

    	-- 添加3个管理帐号

    	-- ----------------------------

    	INSERT INTO `t_admin` VALUES ('1', 'admin', 'admin', '');

    	INSERT INTO `t_admin` VALUES ('4', '123456', 'test', '');

    	INSERT INTO `t_admin` VALUES ('5', '111111', '111111', '');



    	-- ----------------------------

    	-- 创建权限表t_role

    	-- ----------------------------

    	CREATE TABLE `t_role` (

    	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,

    	  `role` varchar(40) NOT NULL DEFAULT '',

    	  `descpt` varchar(40) NOT NULL DEFAULT '' COMMENT '角色描述',

    	  `category` varchar(40) NOT NULL DEFAULT '' COMMENT '分类',

    	  PRIMARY KEY (`id`)

    	) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;



    	-- ----------------------------

    	-- 加入4个操作权限

    	-- ----------------------------

    	INSERT INTO `t_role` VALUES ('1', 'ROLE_ADMIN', '系统管理员', '系统管理员');

    	INSERT INTO `t_role` VALUES ('2', 'ROLE_UPDATE_FILM', '修改', '影片管理');

    	INSERT INTO `t_role` VALUES ('3', 'ROLE_DELETE_FILM', '删除', '影片管理');

    	INSERT INTO `t_role` VALUES ('4', 'ROLE_ADD_FILM', '添加', '影片管理');



    	-- ----------------------------

    	-- 创建权限组表

    	-- ----------------------------

    	CREATE TABLE `t_group` (

    	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,

    	  `groupname` varchar(50) NOT NULL DEFAULT '',

    	  PRIMARY KEY (`id`)

    	) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;



    	-- ----------------------------

    	-- 添加2个权限组

    	-- ----------------------------

    	INSERT INTO `t_group` VALUES ('1', 'Administrator');

    	INSERT INTO `t_group` VALUES ('2', '影片维护');



    	-- ----------------------------

    	-- 创建权限组对应权限表t_group_role

    	-- ----------------------------

    	CREATE TABLE `t_group_role` (

    	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,

    	  `groupid` bigint(20) unsigned NOT NULL,

    	  `roleid` bigint(20) unsigned NOT NULL,

    	  PRIMARY KEY (`id`),

    	  UNIQUE KEY `groupid2` (`groupid`,`roleid`),

    	  KEY `roleid` (`roleid`),

    	  CONSTRAINT `t_group_role_ibfk_1` FOREIGN KEY (`groupid`) REFERENCES `t_group` (`id`),

    	  CONSTRAINT `t_group_role_ibfk_2` FOREIGN KEY (`roleid`) REFERENCES `t_role` (`id`)

    	) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;



    	-- ----------------------------

    	-- 加入权限组与权限的对应关系

    	-- ----------------------------

    	INSERT INTO `t_group_role` VALUES ('1', '1', '1');

    	INSERT INTO `t_group_role` VALUES ('2', '2', '2');

    	INSERT INTO `t_group_role` VALUES ('4', '2', '4');



    	-- ----------------------------

    	-- 创建管理员所属权限组表t_group_user

    	-- ----------------------------

    	CREATE TABLE `t_group_user` (

    	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,

    	  `userid` bigint(20) unsigned NOT NULL,

    	  `groupid` bigint(20) unsigned NOT NULL,

    	  PRIMARY KEY (`id`),

    	  KEY `userid` (`userid`),

    	  KEY `groupid` (`groupid`),

    	  CONSTRAINT `t_group_user_ibfk_2` FOREIGN KEY (`groupid`) REFERENCES `t_group` (`id`),

    	  CONSTRAINT `t_group_user_ibfk_3` FOREIGN KEY (`userid`) REFERENCES `t_admin` (`id`)

    	) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;



    	-- ----------------------------

    	-- 将管理员加入权限组

    	-- ----------------------------

    	INSERT INTO `t_group_user` VALUES ('1', '1', '1');

    	INSERT INTO `t_group_user` VALUES ('2', '4', '2');



    	-- ----------------------------

    	-- 创建管理员对应权限表t_user_role

    	-- 设置该表可跳过权限组，为管理员直接分配权限

    	-- ----------------------------

    	CREATE TABLE `t_user_role` (

    	  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,

    	  `userid` bigint(20) unsigned NOT NULL,

    	  `roleid` bigint(20) unsigned NOT NULL,

    	  PRIMARY KEY (`id`),

    	  KEY `userid` (`userid`),

    	  KEY `roleid` (`roleid`),

    	  CONSTRAINT `t_user_role_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `t_admin` (`id`),

    	  CONSTRAINT `t_user_role_ibfk_2` FOREIGN KEY (`roleid`) REFERENCES `t_role` (`id`)

    	) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;



**3.2）在项目中新增如下jar包(security框架所需jar包)：**

**注意：以下jar包本文已提供下载**

spring-security-config-3.1.0.RC2.jar

spring-security-core-3.1.0.RC2.jar

spring-security-taglibs-3.1.0.RC2.jar

spring-security-web-3.1.0.RC2.jar

**3.3）创建如下包，放置登录验证过滤器代码：**

com.xxx.security

**3.4）在src下创建Spring配置文件 applicationContext-security.xml，内容如下：**


    <?xml version="1.0" encoding="UTF-8"?>



    	<beans:beans xmlns="http://www.springframework.org/schema/security"

    		xmlns:b="http://www.springframework.org/schema/beans" xmlns:beans="http://www.springframework.org/schema/beans"

    		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

    		xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd

    	                        http://www.springframework.org/schema/security http://www.springframework.org/schema/security/spring-security-3.1.xsd">



    	<!-- 这里进行配置 -->



    </beans:beans>

**3.5）在 web.xml中加入security配置，如下：**


    <?xml version="1.0" encoding="UTF-8"?>

    	<web-app version="2.5"

    		xmlns="http://java.sun.com/xml/ns/javaee"

    		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

    		xsi:schemaLocation="http://java.sun.com/xml/ns/javaee

    		http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd">

    	  <welcome-file-list>

    	    <welcome-file>index.jsp</welcome-file>

    	  </welcome-file-list>



    	  	<context-param>

    			 contextConfigLocation

    			 /WEB-INF/applicationContext-*.xml,classpath*:applicationContext-*.xml

    		</context-param>



    		<!-- 配置Spring Security -->

    		<filter>

    			<filter-name>springSecurityFilterChain</filter-name>

    			<filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>

    		</filter>

    		<filter-mapping>

    			<filter-name>springSecurityFilterChain</filter-name>

    			<url-pattern>/*</url-pattern>

    		</filter-mapping>



    		<filter>

    			<filter-name>struts2</filter-name>

    			<filter-class>org.apache.struts2.dispatcher.ng.filter.StrutsPrepareAndExecuteFilter</filter-class>

    		</filter>

    		<filter-mapping>

    			<filter-name>struts2</filter-name>

    			<url-pattern>/*</url-pattern>

    		</filter-mapping>

    		<listener>

    			<listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>

    		</listener>

    	</web-app>

**4、站点根路径下创建登录页面 login.jsp，代码如下：**


    <%@ page language="java" contentType="text/html; charset=UTF-8"

    	pageEncoding="UTF-8"%>

    <%@ taglib prefix="s" uri="/struts-tags"%>

    <%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>

    <%

    String path = request.getContextPath();

    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path;

    %>

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>后台登录</title>

    </head>

    <body onload="document.loginForm.j_username.focus();">

    	<!-- 登录表单 -->

    	<form name="loginForm" action="<c:url value='/j_spring_security_check'/>" method="post">

    		<!-- 登录失败后，显示之前的登录名 -->

    		用户名：<input type='text' name='j_username' class="txtinput"

    		value='<c:if test="${not empty param.login_error}" >

    		<c:out value="${SPRING_SECURITY_LAST_USERNAME}"/></c:if>' />



    		密码：<input type='password' name='j_password' class="txtinput" />





    		<input type="checkbox" name="_spring_security_remember_me" />

    		 保存登录信息

    		<input name="submit" type="submit" value="提交" />

    		<input name="reset" type="reset" value="重置" />



    	</form>



    	<!-- 显示登录失败原因 -->

    	<c:if test="${not empty param.error}">

    		  登录失败



    		原因: <c:out value="${SPRING_SECURITY_LAST_EXCEPTION.message}" />.

    	</c:if>

    </body>

    </html>

**5、站点根路径下创建注销页面 loggedout.jsp，代码如下：**


    <%@page session="false" %>

    <%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

    <%@ page pageEncoding="UTF-8"%>

    <%

    String path = request.getContextPath();

    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path;

    %>

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml">

      <head>

          <meta http-equiv="content-type" content="text/html; charset=UTF-8" />

          <title>登出</title>

      </head>

    <body>

    你已经退出。

    <a href="<c:url value='/login.jsp'/>">点击这里登录</a>

    </body>

    </html>

**6、站点根路径下创建HttpSession超时提示页面 timeout.jsp，代码如下：**


    <%@page session="false" %>

    <%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

    <%@ page pageEncoding="UTF-8" contentType="text/html; charset=UTF-8"%>

    <%

    String path = request.getContextPath();

    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path;

    %>

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml">

      <head>

          <title>用户失效</title>

      </head>

    <body>

    你的登录已经失效，请重新登录。



    <a href="<c:url value='/login.jsp'/>" >

    点击这里登录</a>

    </body>

    </html>



**7、在com.xxx.security包下创建登录验证过滤器，该过滤器可用于在管理员登录时进行 日志记录等相关操作，包括两个类：**

  * LoginUsernamePasswordAuthenticationFilter
  * LoginSuccessHandler

**7.1）LoginUsernamePasswordAuthenticationFilter代码如下：**


    package com.xxx.security;

    import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;



    public class LoginUsernamePasswordAuthenticationFilter extends

    		UsernamePasswordAuthenticationFilter {



    }

**7.2）LoginSuccessHandler代码如下：**


    package com.xxx.security;



    import java.io.IOException;

    import javax.servlet.ServletException;

    import javax.servlet.http.HttpServletRequest;

    import javax.servlet.http.HttpServletResponse;

    import org.springframework.security.core.Authentication;

    import org.springframework.security.core.userdetails.UserDetails;

    import org.springframework.security.web.authentication.SavedRequestAwareAuthenticationSuccessHandler;



    /**

     * 处理管理员登录日志

     *

     */

    public class LoginSuccessHandler extends SavedRequestAwareAuthenticationSuccessHandler{



    	@Override

    	public void onAuthenticationSuccess(HttpServletRequest request,

    			HttpServletResponse response, Authentication authentication) throws IOException,

    			ServletException {



    		UserDetails userDetails = (UserDetails)authentication.getPrincipal();



    		//输出登录提示信息

    		System.out.println("管理员 " + userDetails.getUsername() + " 登录");



    		super.onAuthenticationSuccess(request, response, authentication);

    	}



    }

**8、在 applicationContext-security.xml中加入权限管理配置，如下：**


    <?xml version="1.0" encoding="UTF-8"?>



    <beans:beans xmlns="http://www.springframework.org/schema/security"

    	xmlns:b="http://www.springframework.org/schema/beans" xmlns:beans="http://www.springframework.org/schema/beans"

    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

    	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd

                            http://www.springframework.org/schema/security http://www.springframework.org/schema/security/spring-security-3.1.xsd">



    	<http >

    		<!-- 不拦截login.jsp -->

    		<intercept-url pattern="/login.jsp*" access="IS_AUTHENTICATED_ANONYMOUSLY" />

    		<!--仅拦截到manager下面的内容，具备access对应权限的-->

    		<intercept-url pattern="/manager/**" access="ROLE_ADMIN,ROLE_UPDATE_FILM,ROLE_DELETE_FILM,ROLE_ADD_FILM" />

    		<!-- 设置登录过滤器 -->

    		<custom-filter before="FORM_LOGIN_FILTER" ref="authenticationProcessingFilter" />

    		<!-- 登录表单设置 -->

    		<form-login login-page="/login.jsp"

    			default-target-url="/manager/films.jsp"

    			authentication-failure-url="/login.jsp?error=true" />



    		<!-- 登出操作后跳转到该页面 -->

    		<logout logout-success-url="/loggedout.jsp"

    			delete-cookies="JSESSIONID" />

    		<remember-me />



    		<!-- SESSION超时后跳转到该页面 -->

    		<session-management invalid-session-url="/timeout.jsp">

    		</session-management>

    	</http>



    	<authentication-manager alias="authenticationManager">

    		<authentication-provider>

    			<!--

    				直接使用SQL语句查询登录帐号对应权限，

    				users-by-username-query：查询登录用户是否存在

    				authorities-by-username-query：查询登录用户权限(登录用户可以不属于任何组，从t_user_role表中获取权限)

    				group-authorities-by-username-query：查询登录用户所在组的权限

    			-->

    			<jdbc-user-service data-source-ref="dataSource"

    			group-authorities-by-username-query="SELECT g.id,g.groupname,role.role

    							 FROM t_group AS g

    							 LEFT OUTER JOIN t_group_role AS grouprole ON (g.id = grouprole.groupid)

    							 LEFT OUTER JOIN t_role AS role ON (role.id = grouprole.roleid)

    							 LEFT OUTER JOIN t_group_user AS groupuser on (g.id = groupuser.groupid)

    							 LEFT OUTER JOIN t_admin ON (t_admin.id = groupuser.userid)

    							 WHERE t_admin.nickname = ?"

    				users-by-username-query="SELECT t_admin.nickname AS username,t_admin.passwd as password,'true' AS enabled

    							 FROM t_admin

    							 WHERE t_admin.nickname = ?"

    				authorities-by-username-query="SELECT t_admin.nickname AS username,role.role as authorities

    							   FROM t_admin

    							   LEFT OUTER JOIN t_user_role AS userrole ON(t_admin.id = userrole.userid)

    							   LEFT OUTER JOIN t_role AS role ON (userrole.roleid = role.id)

    							   WHERE t_admin.nickname = ?" />

    		</authentication-provider>

    	</authentication-manager>



    	<!-- 自定义消息 -->

    	<b:bean id="messageSource"

    		class="org.springframework.context.support.ReloadableResourceBundleMessageSource">

    		<b:property name="basename"

    			value="classpath:org/springframework/security/messages" />

    	</b:bean>



    	<!-- 定制登录过滤器 -->

    	<beans:bean id="loginSuccessHandler" class="com.xxx.security.LoginSuccessHandler">

    		<b:property name="defaultTargetUrl">

    			<!-- 登录成功后转发到该页面 -->

    			<b:value>/manager/films.jsp</b:value>

    		</b:property>

    	</beans:bean>

    	<beans:bean id="authenticationProcessingFilter" class="com.xxx.security.LoginUsernamePasswordAuthenticationFilter">

    	<beans:property name="authenticationSuccessHandler" ref="loginSuccessHandler"></beans:property>

    	<beans:property name="authenticationFailureHandler" ref="authenticationFailureHandler"></beans:property>

    	<beans:property name="authenticationManager" ref="authenticationManager"></beans:property>

    	</beans:bean>

    	<beans:bean id="authenticationFailureHandler" class="org.springframework.security.web.authentication.SimpleUrlAuthenticationFailureHandler">

    	<beans:property name="defaultFailureUrl">

    		<!-- 登录失败后转发到该页面 -->

    		<beans:value>/login.jsp?error=true</beans:value>

    	</beans:property>

    	</beans:bean>



    </beans:beans>



**9、为影片页面films.jsp定制操作权限，定制后，不同的帐号登录会看到不同的操作，**

**比如，帐号"admin"属于权限组"Administrator"，具备权限"ROLE_ADMIN"，登录后**

**可以看到所有操作，帐号"test"属于权限组"影片维护"，具备权限"ROLE_UPDATE_FILM"**

**和"ROLE_ADD_FILM"，登录后只能看到"添加影片信息"和"修改"操作**

films.jsp页面权限分布图：

![](/upload/picture/pic/97730/1f20a420-30d1-3415-9159-84dfe99a82b6.jpg)

films.jsp代码如下：


    <%@ page language="java" contentType="text/html; charset=utf-8"

    pageEncoding="utf-8" %>

    <%@taglib uri="/struts-tags" prefix="s" %>

    <%@ taglib prefix="security"

    	uri="http://www.springframework.org/security/tags"%>

    <%

    String path = request.getContextPath();

    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";

    %>

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

    <html>

      <head>

        <title>信息操作</title>

      </head>

      <body>

        <s:form action="/film/findFilm" method="post">

        	<s:submit value=" 获取所有影片信息 "></s:submit>

        </s:form>

        <!-- 添加影片操作，登录帐号具备ROLE_ADMIN权限或者ROLE_ADD_FILM权限可以执行 -->

        <security:authorize ifAnyGranted="ROLE_ADMIN,ROLE_ADD_FILM">

    	<a href="<%=basePath %>manager/insertFilm.jsp">添加影片信息</a>

        </security:authorize>



        <s:if test="filmList != null">

        	<table border="1" width="40%">

    	<tr>

    		<th>序号</th><th>影片名</th><th>操作</th>

    	</tr>

        	<%-- 遍历影片信息 --%>

        	<s:iterator var="film" value="filmList" status="st">

    	    	<tr>

    	    		<td><s:property value="#st.index+1" /></td>

    	    		<td><s:property value="fname" /></td>

    	    		<td>



    	    			<!-- 修改影片操作，登录帐号具备ROLE_ADMIN权限或者ROLE_UPDATE_FILM权限可以执行 -->

    	    			<security:authorize ifAnyGranted="ROLE_ADMIN,ROLE_UPDATE_FILM">

    		    			<s:url id="detailUrl" value="/film/detailFilm">

    		                      		<s:param name="id" value="%{id}"/>

    		                      		</s:url>

    		    			<s:a href="%{detailUrl}">[修改]</s:a>

    	    			</security:authorize>

    			    	<!-- 删除影片操作，登录帐号具备ROLE_ADMIN权限或者ROLE_DELETE_FILM权限可以执行 -->

    			    	<security:authorize ifAnyGranted="ROLE_ADMIN,ROLE_DELETE_FILM">

    				    	<s:url id="deleteUrl" value="/film/deleteFilm">

    		                      		<s:param name="id" value="%{id}"/>

    		                      		</s:url>

    				    	<s:a href="%{deleteUrl}">[删除]</s:a>

    			    	</security:authorize>

    			</td>

    	    	</tr>

    		</s:iterator>

    	</table>

        </s:if>

      </body>

    </html>

  * [Spring_security3.1框架所需jar包.rar](http://dl.iteye.com/topics/download/dfdf3168-3f9f-3d96-a95e-372eb0e4c834) (670.9 KB)
  * 下载次数: 1645

**31**
顶

**5**
踩

分享到： [![](/images/sina.jpg)](javascript:; "分享到新浪微博") [![](/images/tec.jpg)](javascript:; "分享到腾讯微博")

  * 2011-08-29 10:49
  * 浏览 237674
  * 评论(13)
  * 分类:[企业架构](https://www.iteye.com/blogs/category/architecture)
  * [查看更多](https://www.iteye.com/wiki/blog/1160153)

Global site tag (gtag.js) - Google Analytics
