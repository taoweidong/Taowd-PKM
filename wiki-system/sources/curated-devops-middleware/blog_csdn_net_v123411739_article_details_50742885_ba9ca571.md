---
source: "http://blog.csdn.net/v123411739/article/details/50742885"
title: "SSM框架详细整合教程（Spring+SpringMVC+MyBatis）_ssm框架教程-CSDN博客"
fetched_at: "2026-10-05 15:30:19"
---

> 微信搜索【程序员囧辉】，关注这个坚持分享技术干货的程序员。

## **动机**

使用maven已经有一段时间了，但项目是别人搭建好的，因此一直想着自己要学习搭建一下。网上找了些资料后，结合自己实验，花了点时间就搞好，老样子，写在博客上，免得日后忘记。

**本文链接：<http://blog.csdn.net/v123411739/article/details/50742885>**

**博文中的MyEclipse链接：https://pan.baidu.com/s/1pMhiygz 密码：mqmc**

**博文中的完整项目代码：** https://pan.baidu.com/s/1mjsJNz6 密码：saqe

如果地址失效了，可以在文章下留言或者公众号给我发消息，我看到后会及时更新。

**注：文末有直接导入项目的方法。**

## 1.安装maven和配置（此步骤并非必须，可以根据情况选择）

  1. 进入官网下载中心<http://maven.apache.org/download.cgi>，下载[apache-maven-3.5.2-bin.zip](http://mirrors.hust.edu.cn/apache/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.zip)，**-src.zip为Maven的源码
  2. 配置环境变量，打开系统环境变量新建一个M2_HOME将解压后的Maven存放路径放在此，然后在path路径加入%M2_HOME%\bin路径
  3. 检测是否配置成功，打开命令行输入echo %M2_HOME%查看M2_HOME指向的Maven存放安装目录是否正确，输入mvn -v查看是否能找到正确的mvn执行脚本
  4. 以后升级的话将M2_HOME的路径换为最新的安装目录就行
  5. Maven实践：初次安装完后输入mvn help:system的命令，此时会打印出所有的Java系统属性和环境变量，然后Maven会执行一个真正的任务将相应的所需的构件下载到本地仓库中包括pom和jar文件，然后用户在C:\Users\Administrator\\.m2下就能看到本地仓库了
  6. 用户需要复制M2_HOME/conf/setting.xml文件到C:/Users/Administrator/.m2/setting.xml，这样用户每次升级后就不要在次修改setting.xml文件了



## 2.MyEclipse配置Maven

  1. 在本地创建一个文件夹MavenRepository，并在MavenRepository文件夹下创建文件夹repository。
  2. 进入Maven解压后的文件夹，进入conf文件夹，将settings.xml文件复制到上一步创建的MavenRepository文件夹下
  3. 打开MavenRepository文件夹下的settings.xml文件，找到localRepository标签，此时是被注释掉的，我们解除注释，然后配置步骤1中的repository路径，如<localRepository>F:\m2\repository</localRepository>![](https://i-blog.csdnimg.cn/blog_migrate/01efe1949369b05937d7909d1eab7c03.png)
  4. 在MyEclipse中的Perferences进行如下配置，添加自己的Maven![](https://i-blog.csdnimg.cn/blog_migrate/a5ee4572cb5cc7b3af22ad985794390a.png)
  5. User Settings设置为之前修改过的setting.xml![](https://i-blog.csdnimg.cn/blog_migrate/a5648267c2ca7ae111dd318395cf9029.png)
  6. File->New->others，搜索maven，如果看到有Maven Project则代表配置成功。



![](https://i-blog.csdnimg.cn/blog_migrate/5b0431ab0ccb635c62095edcdc35be15.jpeg)

## 3.MyEclipse使用maven创建web项目

**1、创建一个maven项目**

![](https://i-blog.csdnimg.cn/blog_migrate/6a385d4bb7c9bb22b3202f762b6aeb02.jpeg)

![](https://i-blog.csdnimg.cn/blog_migrate/6a385d4bb7c9bb22b3202f762b6aeb02.jpeg)![](https://i-blog.csdnimg.cn/blog_migrate/6a7b3679df76995e1d5bc98e7cb377f0.jpeg)![](https://i-blog.csdnimg.cn/blog_migrate/2d84af24c72cb553ce02d5a0880f211b.jpeg)

![](https://i-blog.csdnimg.cn/blog_migrate/7f7101e472628e336dcdf1f0becbf994.jpeg)

**2、按照上面教程，即可创建出一个Maven项目，项目结构如下图**![](https://i-blog.csdnimg.cn/blog_migrate/650116b4f7c1b57695e27ae3e8cf44c1.png)

**3、将JRE版本设置为1.7，可使用默认的或者自己导入**

![](https://i-blog.csdnimg.cn/blog_migrate/3d1ca6a53bba5211d23daab8a8296709.jpeg)

**4、此时index.jsp会报以下错误**

![](https://i-blog.csdnimg.cn/blog_migrate/396990c9392148946acb67cf5cfc4ec8.png)

**在pom.xml文件的dependencies节点下添加如下代码即可，添加完后，会下载对应的jar包**

![](https://i-blog.csdnimg.cn/blog_migrate/e3c019dd0c8312b3307baf87a0a97d08.png)

**5、右键项目，选择Properties，进行如下配置**

![](https://i-blog.csdnimg.cn/blog_migrate/fc23b0b210da39fea3782fa95f461597.png)

## 4.搭建Spring+SpringMVC+Mybatis框架

### 1、Maven引入项目用到的jar包，修改pom.xml后保存会自动下载，存放在之前配置的本地仓库中，即：F:\m2\repository文件夹

**pom.xml**
    
    
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    	<modelVersion>4.0.0</modelVersion>
    	<groupId>com.chillax</groupId>
    	<artifactId>Maven_Project</artifactId>
    	<packaging>war</packaging>
    	<version>0.0.1-SNAPSHOT</version>
    	<name>Maven_Project Maven Webapp</name>
    	<url>http://maven.apache.org</url>
    
    	<!-- 用来设置版本号 -->
    	<properties>
    		<spring.version>4.0.2.RELEASE</spring.version>
    		<mybatis.version>3.2.8</mybatis.version>
    		<slf4j.version>1.7.12</slf4j.version>
    		<log4j.version>1.2.17</log4j.version>
    	</properties>
    	<!-- 用到的jar包 -->
    	<dependencies>
    		<!-- 单元测试 -->
    		<dependency>
    			<groupId>junit</groupId>
    			<artifactId>junit</artifactId>
    			<version>4.11</version>
    			<!-- 表示开发的时候引入，发布的时候不会加载此包 -->
    			<scope>test</scope>
    		</dependency>
    		<!-- java ee包 -->
    		<dependency>
    			<groupId>javax</groupId>
    			<artifactId>javaee-api</artifactId>
    			<version>7.0</version>
    		</dependency>
    		<!-- spring框架包 start -->
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-test</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-core</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-oxm</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-tx</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-jdbc</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-aop</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-context</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-context-support</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-expression</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-orm</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-web</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-webmvc</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.springframework</groupId>
    			<artifactId>spring-aspects</artifactId>
    			<version>${spring.version}</version>
    		</dependency>
    		<!-- spring框架包 end -->
    		<!-- mybatis框架包 start -->
    		<dependency>
    			<groupId>org.mybatis</groupId>
    			<artifactId>mybatis</artifactId>
    			<version>${mybatis.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.mybatis</groupId>
    			<artifactId>mybatis-spring</artifactId>
    			<version>1.2.2</version>
    		</dependency>
    		<!-- mybatis框架包 end -->
    		<!-- 数据库驱动 -->
    		<dependency>
    			<groupId>mysql</groupId>
    			<artifactId>mysql-connector-java</artifactId>
    			<version>5.1.35</version>
    		</dependency>
    		<!-- 导入dbcp的jar包，用来在applicationContext.xml中配置数据库 -->
    		<dependency>
    			<groupId>commons-dbcp</groupId>
    			<artifactId>commons-dbcp</artifactId>
    			<version>1.4</version>
    		</dependency>
    		<!-- jstl标签类 -->
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
    		<!-- log start -->
    		<dependency>
    			<groupId>log4j</groupId>
    			<artifactId>log4j</artifactId>
    			<version>${log4j.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.slf4j</groupId>
    			<artifactId>slf4j-api</artifactId>
    			<version>${slf4j.version}</version>
    		</dependency>
    		<dependency>
    			<groupId>org.slf4j</groupId>
    			<artifactId>slf4j-log4j12</artifactId>
    			<version>${slf4j.version}</version>
    		</dependency>
    		<!-- log END -->
    		<!-- Json -->
    		<!-- 格式化对象，方便输出日志 -->
    		<dependency>
    			<groupId>com.alibaba</groupId>
    			<artifactId>fastjson</artifactId>
    			<version>1.2.6</version>
    		</dependency>
    		<dependency>
    			<groupId>org.codehaus.jackson</groupId>
    			<artifactId>jackson-mapper-asl</artifactId>
    			<version>1.9.13</version>
    		</dependency>
    		<!-- 上传组件包 start -->
    		<dependency>
    			<groupId>commons-fileupload</groupId>
    			<artifactId>commons-fileupload</artifactId>
    			<version>1.3.1</version>
    		</dependency>
    		<dependency>
    			<groupId>commons-io</groupId>
    			<artifactId>commons-io</artifactId>
    			<version>2.4</version>
    		</dependency>
    		<dependency>
    			<groupId>commons-codec</groupId>
    			<artifactId>commons-codec</artifactId>
    			<version>1.10</version>
    		</dependency>
    		<!-- 上传组件包 end -->
    
    		<!-- AL相关添加 -->
    		<dependency>
    			<groupId>net.sourceforge.jexcelapi</groupId>
    			<artifactId>jxl</artifactId>
    			<version>2.6</version>
    		</dependency>
    		<dependency>
    			<groupId>org.apache.poi</groupId>
    			<artifactId>poi</artifactId>
    			<version>3.8</version>
    		</dependency>
    		<dependency>
    			<groupId>org.apache.poi</groupId>
    			<artifactId>poi-ooxml</artifactId>
    			<version>3.9</version>
    		</dependency>
    		<!-- AL相关添加 -->
    	</dependencies>
    
    	<build>
    		<finalName>Maven_Project</finalName>
    		<plugins>
    			<plugin>
    				<groupId>org.apache.maven.plugins</groupId>
    				<artifactId>maven-compiler-plugin</artifactId>
    				<version>2.3.2</version>
    				<configuration>
    					<source>1.7</source>
    					<target>1.7</target>
    				</configuration>
    			</plugin>
    		</plugins>
    	</build>
    </project>

### 2、在src/main/resources下添加如下配置文件

**applicationContext.xml**
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:mvc="http://www.springframework.org/schema/mvc"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans  
                            http://www.springframework.org/schema/beans/spring-beans-3.1.xsd  
                            http://www.springframework.org/schema/context  
                            http://www.springframework.org/schema/context/spring-context-3.1.xsd  
                            http://www.springframework.org/schema/mvc  
                            http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd">
                            
        <!-- 使用注解式注入 -->
    	<context:annotation-config />
    	
        <!-- 自动扫描 -->
    	<context:component-scan base-package="com.chillax" />
    	
        <!-- 导入DAO配置 -->
    	<import resource="spring-dao.xml"/>
    	
    	<!-- 导入数据库配置 -->
    	<import resource="spring-db.xml"/>
    	
    	<!-- 导入数据库配置 -->
    	<import resource="spring-tx.xml"/>
    	
    </beans>

**jdbc.properties，** 有多人反映直接复制时，第一行的driver最后面多了个空格，请注意
    
    
    driver=com.mysql.jdbc.Driver
    url=jdbc:mysql://127.0.0.1:3306/maventest
    username=root
    password=root
    #定义初始连接数
    initialSize=0
    #定义最大连接数
    maxActive=20
    #定义最大空闲
    maxIdle=20
    #定义最小空闲
    minIdle=1
    #定义最长等待时间
    maxWait=60000

**log4j.properties**
    
    
    #定义LOG输出级别
    log4j.rootLogger=INFO,Console,File
    #定义日志输出目的地为控制台
    log4j.appender.Console=org.apache.log4j.ConsoleAppender
    log4j.appender.Console.Target=System.out
    #可以灵活地指定日志输出格式，下面一行是指定具体的格式
    log4j.appender.Console.layout = org.apache.log4j.PatternLayout
    log4j.appender.Console.layout.ConversionPattern=[%c] - %m%n
    
    #文件大小到达指定尺寸的时候产生一个新的文件
    log4j.appender.File = org.apache.log4j.RollingFileAppender
    #指定输出目录
    log4j.appender.File.File = logs/ssm.log
    #定义文件最大大小
    log4j.appender.File.MaxFileSize = 10MB
    # 输出所以日志，如果换成DEBUG表示输出DEBUG以上级别日志
    log4j.appender.File.Threshold = ALL
    log4j.appender.File.layout = org.apache.log4j.PatternLayout
    log4j.appender.File.layout.ConversionPattern =[%p] [%d{yyyy-MM-dd HH\:mm\:ss}][%c]%m%n

**spring-dao.xml**
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:mvc="http://www.springframework.org/schema/mvc"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans  
                            http://www.springframework.org/schema/beans/spring-beans-3.1.xsd  
                            http://www.springframework.org/schema/context  
                            http://www.springframework.org/schema/context/spring-context-3.1.xsd  
                            http://www.springframework.org/schema/mvc  
                            http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd">
                            
                            
    	<!-- DAO接口所在包名，Spring会自动查找其下的类 -->
    	<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
    	 	<!--basePackage指定要扫描的包，在此包之下的映射器都会被搜索到。
    		 可指定多个包，包与包之间用逗号或分号分隔-->
    		<property name="basePackage" value="com.chillax.dao" />
    		<property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"></property>
    	</bean>                       
                            
    </beans>

**spring-db.xml**
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:mvc="http://www.springframework.org/schema/mvc"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans  
                            http://www.springframework.org/schema/beans/spring-beans-3.1.xsd  
                            http://www.springframework.org/schema/context  
                            http://www.springframework.org/schema/context/spring-context-3.1.xsd  
                            http://www.springframework.org/schema/mvc  
                            http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd">
    
    	<!-- 引入配置文件 -->
    	<bean id="propertyConfigurer" class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
    		<property name="location" value="classpath:jdbc.properties" />
    	</bean>
    	
    	<bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    		<property name="driverClassName" value="${driver}" />
    		<property name="url" value="${url}" />
    		<property name="username" value="${username}" />
    		<property name="password" value="${password}" />
    		<!-- 初始化连接大小 -->
    		<property name="initialSize" value="${initialSize}"></property>
    		<!-- 连接池最大数量 -->
    		<property name="maxActive" value="${maxActive}"></property>
    		<!-- 连接池最大空闲 -->
    		<property name="maxIdle" value="${maxIdle}"></property>
    		<!-- 连接池最小空闲 -->
    		<property name="minIdle" value="${minIdle}"></property>
    		<!-- 获取连接最大等待时间 -->
    		<property name="maxWait" value="${maxWait}"></property>
    	</bean>
    
    	<!-- spring和MyBatis完美整合，不需要mybatis的配置映射文件 -->
    	<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    		<property name="dataSource" ref="dataSource" />
    		<!-- 自动扫描mapping.xml文件 -->
    		<property name="mapperLocations" value="classpath:com/chillax/mapper/*.xml"></property>
    	</bean>
    	
    </beans>

**spring-tx.xml**
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:aop="http://www.springframework.org/schema/aop"
    	xmlns:tx="http://www.springframework.org/schema/tx"
    	xmlns:mvc="http://www.springframework.org/schema/mvc"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans  
                            http://www.springframework.org/schema/beans/spring-beans-3.1.xsd  
                            http://www.springframework.org/schema/context  
                            http://www.springframework.org/schema/context/spring-context-3.1.xsd  
                            http://www.springframework.org/schema/aop 
               				http://www.springframework.org/schema/aop/spring-aop-3.1.xsd
               				http://www.springframework.org/schema/tx
         	  				http://www.springframework.org/schema/tx/spring-tx-3.1.xsd">
    
    	<!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->
    	<bean id="transactionManager"
    		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    		<property name="dataSource" ref="dataSource" />
    	</bean>
    	
    	 <!--  配置参与事务的类 -->
    	 <aop:config>
    		 <aop:pointcut id="allServiceMethod" expression="execution(* com.chillax.service.*.*(..))"/>
    		 <aop:advisor pointcut-ref="allServiceMethod" advice-ref="TxAdvice" />
    	 </aop:config>
    	
    	<!-- 使用声明方式配置事务 -->
    	<tx:advice id="TxAdvice" transaction-manager="transactionManager">
    	     <tx:attributes>
    		       <tx:method name="*" propagation="REQUIRED" rollback-for="java.lang.Exception"/>
    	     </tx:attributes>
     	</tx:advice>
     	
    </beans>

### 3、在WEB-INF文件夹下添加/修改以下配置文件

**spring-mvc.xml**
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
    	xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:mvc="http://www.springframework.org/schema/mvc"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans  
                            http://www.springframework.org/schema/beans/spring-beans-3.1.xsd  
                            http://www.springframework.org/schema/context  
                            http://www.springframework.org/schema/context/spring-context-3.1.xsd  
                            http://www.springframework.org/schema/mvc  
                            http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd">
    
    	 <!-- 添加注解驱动 -->  
        <mvc:annotation-driven />
        <mvc:default-servlet-handler/>
        
        <!-- 设置使用注解的类所在的包 -->
    	<context:component-scan base-package="com.chillax.controller" />
    	
    	<!-- 定义跳转的文件的前后缀 ，视图模式配置-->
    	<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    		<!-- 这里的配置我的理解是自动给后面action的方法return的字符串加上前缀和后缀，变成一个 可用的url地址 -->
    		<property name="prefix" value="/WEB-INF/jsp/" />
    		<property name="suffix" value=".jsp" />
    	</bean>
    	
    	<!-- SpringMVC上传文件时，需要配置MultipartResolver处理器-->
    	<bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver">  
            <!-- 默认编码 -->
            <property name="defaultEncoding" value="utf-8" />  
            <!-- 文件大小最大值 -->
            <property name="maxUploadSize" value="10485760000" />  
            <!-- 内存中的最大值 -->
            <property name="maxInMemorySize" value="40960" />  
        </bean> 
    
    </beans>

**web.xml**
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xmlns="http://java.sun.com/xml/ns/javaee"
    	xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
    	version="3.0">
    	<display-name>Archetype Created Web Application</display-name>
    	
    	<welcome-file-list>
    		<welcome-file>/index.jsp</welcome-file>
    	</welcome-file-list>
    	
    	<!-- 加载spring bean -->
        <context-param>
             <param-name>contextConfigLocation</param-name>
            <param-value>classpath:applicationContext.xml</param-value>
        </context-param>
        <listener>
            <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
        </listener>
        
    	<!-- 编码过滤器 -->
    	<filter>
    		<filter-name>encodingFilter</filter-name>
    		<filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    		<async-supported>true</async-supported>
    		<init-param>
    			<param-name>encoding</param-name>
    			<param-value>UTF-8</param-value>
    		</init-param>
    	</filter>
    	<filter-mapping>
    		<filter-name>encodingFilter</filter-name>
    		<url-pattern>/*</url-pattern>
    	</filter-mapping>
    	
    	<!-- Spring MVC servlet -->
    	<servlet>
    		<servlet-name>SpringMVC</servlet-name>
    		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    		<init-param>
    			<param-name>contextConfigLocation</param-name>
    			<param-value>/WEB-INF/spring-mvc.xml</param-value>
    		</init-param>
    		<load-on-startup>1</load-on-startup>
    		<async-supported>true</async-supported>
    	</servlet>
    	<servlet-mapping>
    		<servlet-name>SpringMVC</servlet-name>
    		<url-pattern>/</url-pattern>
    	</servlet-mapping>
    	
    </web-app>
    

### 4、在src/main/java下添加如下包和类

**UserController.java**
    
    
    package com.chillax.controller;
    
    import java.util.List;
    
    import javax.annotation.Resource;
    import javax.servlet.http.HttpServletRequest;
    
    import org.springframework.stereotype.Controller;
    import org.springframework.ui.Model;
    import org.springframework.web.bind.annotation.RequestMapping;
    
    import com.chillax.dto.User;
    import com.chillax.service.IUserService;
    
    @Controller
    @RequestMapping("/user")
    public class UserController {
    	@Resource
    	private IUserService userService;
    	
    	@RequestMapping("/userList")
    	public String userList(HttpServletRequest request,Model model){
    		List<User> uList = userService.getAllUser();
    		model.addAttribute("uList", uList);
    		return "userList";
    	}
    	
    	@RequestMapping("/showUser")
    	public String showUser(HttpServletRequest request,Model model){
    		int userId = Integer.parseInt(request.getParameter("id"));
    		User user = userService.getUserById(userId);
    		model.addAttribute("user", user);
    		return "showUser";
    	}
    	
    	@RequestMapping("/addUserUI")
    	public String addUserUI(){
    		return "addUser";
    	}
    	
    	@RequestMapping("/addUser")
    	public String addUser(HttpServletRequest request,Model model){
    		User user = new User();
    		user.setName(String.valueOf(request.getParameter("name")));
    		user.setPassword(String.valueOf(request.getParameter("password")));
    		user.setAge(Integer.parseInt(String.valueOf(request.getParameter("age"))));
    		userService.addUser(user);
    		return "redirect:/user/userList";
    	}
    }

**IUserDao.java**
    
    
    package com.chillax.dao;
    
    import java.util.List;
    import java.util.Map;
    
    import com.chillax.dto.User;
    
    public interface IUserDao {
    	
    	public User queryByPrimaryKey(Integer id);
    	
    	public List<User> getAllUser();
    		
    	public void insertUser(User user);
    	
    	public void insertUserByBatch(List<User> list);
    	
    	public void deleteByPrimaryKey(Integer id);
    	
    	public void delteUserByBatch(Map<String,Object> params);
    	
    	public void updateByPrimaryKey(User user);
    	
    }

**User.java**
    
    
    package com.chillax.dto;
    
    public class User {
        private Integer id;
    
        private String name;
    
        private String password;
    
        private Integer age;
    
        public Integer getId() {
            return id;
        }
    
        public void setId(Integer id) {
            this.id = id;
        }
    
        public String getName() {
    		return name;
    	}
    
    	public void setName(String name) {
    		this.name = name;
    	}
    
    	public String getPassword() {
            return password;
        }
    
        public void setPassword(String password) {
            this.password = password == null ? null : password.trim();
        }
    
        public Integer getAge() {
            return age;
        }
    
        public void setAge(Integer age) {
            this.age = age;
        }
    }

**UserMapper.xml**
    
    
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
    <mapper namespace="com.chillax.dao.IUserDao" >  
        <resultMap id="BaseResultMap" type="com.chillax.dto.User">
    		<result column="id" property="id" jdbcType="INTEGER" />
    		<result column="name" property="name" jdbcType="VARCHAR" />
    		<result column="password" property="password" jdbcType="VARCHAR" />
    		<result column="age" property="age" jdbcType="INTEGER" />
    	</resultMap>
    
    	<sql id="Base_Column_List">
    		id, name, password, age
    	</sql>
    
    	<!-- 查询用户-->
    	<select id="queryByPrimaryKey" resultMap="BaseResultMap"
    		parameterType="java.lang.Integer">
    		select
    		<include refid="Base_Column_List" />
    		from user
    		where id = #{id,jdbcType=INTEGER}
    	</select>
    	
    	<!-- 查询用户-->
    	<select id="getAllUser" resultMap="BaseResultMap">
    		select
    		<include refid="Base_Column_List" />
    		from user
    	</select>
    	
    	<!-- 插入用户 -->
    	<insert id="insertUser" parameterType="com.chillax.dto.User">
    		insert into user  
    		<trim prefix="(" suffix=")" suffixOverrides="," >  
    		  <if test="id != null" >  
    		    id,  
    		  </if>  
    		  <if test="name != null" >  
    		    name,  
    		  </if>  
    		  <if test="password != null" >  
    		    password,  
    		  </if>  
    		  <if test="age != null" >  
    		    age,  
    		  </if>  
    		</trim>  
    		<trim prefix="values (" suffix=")" suffixOverrides="," >  
    		  <if test="id != null" >  
    		    #{id,jdbcType=INTEGER},  
    		  </if>  
    		  <if test="name != null" >  
    		    #{name,jdbcType=VARCHAR},  
    		  </if>  
    		  <if test="password != null" >  
    		    #{password,jdbcType=VARCHAR},  
    		  </if>  
    		  <if test="age != null" >  
    		    #{age,jdbcType=INTEGER},  
    		  </if>  
    		</trim>   
    	</insert>
    	
    	<!-- 批量插入用户 -->
    	<insert id="insertUserByBatch" parameterType="java.util.List" >
        insert into USER
           (ID,
            NAME,
            PASSWORD,
            AGE)
        select A.* from
             (
             <foreach collection="list" item="user" index="index" separator="union">
                 select 
                 #{user.id,jdbcType=INTEGER},
                 #{user.name,jdbcType=VARCHAR},
                 #{user.password,jdbcType=VARCHAR},
                 #{user.age,jdbcType=INTEGER}
                  from dual
             </foreach>
             ) A
      	</insert>
    
    	<!-- 删除用户 -->
    	<delete id="deleteByPrimaryKey" parameterType="java.lang.Integer">
    		delete from user
    		where id = #{id,jdbcType=INTEGER}  
      	</delete>
      	
      	<!-- 批量删除用户 -->
    	<delete id="deleteUserByBatch" parameterType="java.util.Map" >
    	 delete from user
    	 where id IN 
    	     <foreach item="ids" collection="iList" open="(" separator="," close=")">
    	         #{ids,jdbcType=DECIMAL}
    	     </foreach>
    	</delete>
    
    	<!-- 更新用户 -->
    	<update id="updateByPrimaryKey" parameterType="com.chillax.dto.User" >  
    	    update user  
    		<set >  
    		  <if test="name != null" >  
    		    name = #{name,jdbcType=VARCHAR},  
    		  </if>  
    		  <if test="password != null" >  
    		    password = #{password,jdbcType=VARCHAR},  
    		  </if>  
    		  <if test="age != null" >  
    		    age = #{age,jdbcType=INTEGER},  
    		  </if>  
    		</set>  
    		where id = #{id,jdbcType=INTEGER} 
      	</update>
      
    </mapper>

**IUserService.java**
    
    
    package com.chillax.service;
    
    import java.util.List;
    
    import com.chillax.dto.User;
    
    public interface IUserService {
    	
    	public User getUserById(int userId);
    
    	public void insertUser(User user);
    
    	public void addUser(User user);
    
    	public List<User> getAllUser();
    }

**UserServiceImpl.java**
    
    
    package com.chillax.service.Impl;
    
    import java.util.List;
    
    import javax.annotation.Resource;
    
    import org.springframework.stereotype.Service;
    
    import com.chillax.dao.IUserDao;
    import com.chillax.dto.User;
    import com.chillax.service.IUserService;
    
    @Service("userService")
    public class UserServiceImpl implements IUserService {
    	@Resource
    	private IUserDao userDao;
    	
    	public User getUserById(int userId) {
    		return userDao.queryByPrimaryKey(userId);
    	}
    
    	public void insertUser(User user) {
    		userDao.insertUser(user);
    	}
    
    	public void addUser(User user) {
    		userDao.insertUser(user);
    	}
    
    	@Override
    	public List<User> getAllUser() {
    		return userDao.getAllUser();
    	}
    
    }

### 5、在WEB-INF文件夹下创建jsp文件夹，并添加userList.jsp，showUser.jsp、addUser.jsp

**userList.jsp**
    
    
    <%@ page language="java" import="java.util.*" pageEncoding="utf-8"%>
    <%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
    <%
    String path = request.getContextPath();
    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
    %>
    
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
      <head>
        <base href="<%=basePath%>">
        
        <title>My JSP 'showUser.jsp' starting page</title>
        
    	<meta http-equiv="pragma" content="no-cache">
    	<meta http-equiv="cache-control" content="no-cache">
    	<meta http-equiv="expires" content="0">    
    	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
    	<meta http-equiv="description" content="This is my page">
    	<!--
    	<link rel="stylesheet" type="text/css" href="styles.css">
    	-->
    
      </head>
      
      <body>
        <c:forEach items="${uList }" var="u">
        	用户名称：${u.name}
        	用户年龄：${u.age }
        	<br/>
        </c:forEach>
      </body>
    </html>

**addUser.jsp**
    
    
    <%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
    <%
    String path = request.getContextPath();
    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
    %>
    
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
      <head>
        <base href="<%=basePath%>">
        
        <title>My JSP 'addUser.jsp' starting page</title>
        
    	<meta http-equiv="pragma" content="no-cache">
    	<meta http-equiv="cache-control" content="no-cache">
    	<meta http-equiv="expires" content="0">    
    	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
    	<meta http-equiv="description" content="This is my page">
    	<!--
    	<link rel="stylesheet" type="text/css" href="styles.css">
    	-->
    
      </head>
      
      <body>
        <form id="addUser" action="user/addUser" method="post"> 
    	    userName: <input id="name" name="name" /><br/> 
    	    password: <input id="password" name="password" /><br/> 
    	    age: <input id="age" name="age"/><br/> 
    	    <input type="submit" value="添加新用户"/> 
    	</form>
      </body>
    </html>

**showUser.jsp**
    
    
    <%@ page language="java" import="java.util.*" pageEncoding="utf-8"%>
    <%
    String path = request.getContextPath();
    String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
    %>
    
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
      <head>
        <base href="<%=basePath%>">
        
        <title>My JSP 'showUser.jsp' starting page</title>
        
    	<meta http-equiv="pragma" content="no-cache">
    	<meta http-equiv="cache-control" content="no-cache">
    	<meta http-equiv="expires" content="0">    
    	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
    	<meta http-equiv="description" content="This is my page">
    	<!--
    	<link rel="stylesheet" type="text/css" href="styles.css">
    	-->
    
      </head>
      
      <body>
        ${user.name }<br>
      </body>
    </html>

### 6、创建数据库，并创建表
    
    
    create database maventest;
    use maventest;
    
    CREATE TABLE `user` (
      `id` int(12) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `password` varchar(50) NOT NULL,
      `age` int(9) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
    
    insert  into `user`(`id`,`name`,`password`,`age`) values (1,'admin','admin',22);

### 7、整个项目文件结构图

![](https://i-blog.csdnimg.cn/blog_migrate/b6a85522b7dfd855163a503aebcc89f0.png)![](https://i-blog.csdnimg.cn/blog_migrate/f4ecc9148cf5e3518335d5dfeb760a8d.png)

### 8、部署发布项目，进行测试

![](https://i-blog.csdnimg.cn/blog_migrate/030ca2ceab9649588bae896b2d0a62e5.png)![](https://i-blog.csdnimg.cn/blog_migrate/84da0d17dc1d8786cd837ab5cf227a34.png)![](https://i-blog.csdnimg.cn/blog_migrate/1689d8f85af2c018f7e01a3d55144fd5.png)

**至此，框架搭建完成。**

## 5.常见问题

### 问题1：pom.xml文件里的代码到哪里找？

解答：http://www.mvnrepository.com/

### 问题2：新建MAVEN项目过程中，出现下图错误？

![](https://i-blog.csdnimg.cn/blog_migrate/41e525a3e0133cb26266f9a6708f86db.jpeg)

**解决：** 在MyEclipse的安装目录找到myeclipse.ini，将分配的堆内存加大

![](https://i-blog.csdnimg.cn/blog_migrate/7b2e1b6dc13b61c606670b311b82e3e5.jpeg)

### 问题3：新建完工程后出现以下错误？

![](https://i-blog.csdnimg.cn/blog_migrate/1ca1cb1be7a07d1b655e9d98f669e7ba.png)

**解答：** 在pom.xml添加以下代码即可，添加完代码就会自动下载好jar包

![](https://i-blog.csdnimg.cn/blog_migrate/ea1c93d0d1477574fbd946098b7254c3.png)

### 问题4：修改pom.xml时出现以下错误？

**![](https://i-blog.csdnimg.cn/blog_migrate/0dbb34655bb2436155839cbe226df634.png)**

**解答：** 这是由于jar包没有正确下载导致的，找到错误的jar包位置，将文件夹里的文件删掉，将pom.xml里该jar包的配置代码删除后再重新写上，让MAVEN重新下载jar包即可。

![](https://i-blog.csdnimg.cn/blog_migrate/c40575e98c38bf01f95d10702934f274.png)

### 问题5：出现以下错误？

**![](https://i-blog.csdnimg.cn/blog_migrate/8c016f1a06da63661dd46274e9527e49.jpeg)**

**解答：**

**![](https://i-blog.csdnimg.cn/blog_migrate/fe76d89c29c1017ca8b214541f481d77.jpeg)**

### 问题6：出现以下错误？

**![](https://i-blog.csdnimg.cn/blog_migrate/24aa04e86abe156781270b0d47df6c6b.jpeg)**

**解答：** 将项目的jre版本换成1.7或者以上的版本即可

### 问题7：出现以下错误，并且已经确定jre是1.7版本或者以上版本。

![](https://i-blog.csdnimg.cn/blog_migrate/2c28f292d6d3bef52ac64a305af6c153.png)

**解答：** 在pom.xml文件的<build></build>的标签中加入以下代码，然后Update Project（参照问题5）
    
    
    <build>
    	<finalName>Maven_Project</finalName>
    	<plugins>
    		<plugin>
    			<groupId>org.apache.maven.plugins</groupId>
    			<artifactId>maven-compiler-plugin</artifactId>
    			<version>2.3.2</version>
    			<configuration>
    				<source>1.7</source>
    				<target>1.7</target>
    			</configuration>
    		</plugin>
    	</plugins>
    </build>

### 问题8：访问报错

![](https://i-blog.csdnimg.cn/blog_migrate/11dccc72da1c8c1058efa0557e71bf03.png)

**解答：** 请确认地址中的项目，跟项目中的Web Context-root地址一致。

![](https://i-blog.csdnimg.cn/blog_migrate/ee3cb1651e5d069df18c19908e466106.png)

### 问题9：直接导入代码报错

**解答：** 如果想直接导入代码需要先做文章开头的1和2两步，即用一个自己的新的仓库来存储jar包，不然容易跟已有的仓库配置冲突，导致jar包无法下载或下载不全。下图是我导入的过程，下载jar的过程比较慢，并且下载完了还报错，但是报错并不影响项目的正确运行。

![](https://i-blog.csdnimg.cn/blog_migrate/fd0911267743ddfbff55c15704b9d275.png)

## 推荐阅读

_[如何写一份让 HR 眼前一亮的简历（附模板）](https://joonwhee.blog.csdn.net/article/details/109709619)_

_[字节、美团、快手核心部门面试总结（真题解析）](https://joonwhee.blog.csdn.net/article/details/109588711)_

_[面试阿里，HashMap 这一篇就够了](https://joonwhee.blog.csdn.net/article/details/106324537)_

_[面试必问的 MySQL，你懂了吗？](https://joonwhee.blog.csdn.net/article/details/106893197)_

_[面试必问的线程池，你懂了吗？](https://joonwhee.blog.csdn.net/article/details/106609583)_

_[4 年 Java 经验，阿里网易拼多多面试总结、心得体会](https://joonwhee.blog.csdn.net/article/details/99708892)_

_[跳槽，如何选择一家公司](https://joonwhee.blog.csdn.net/article/details/109171171)_

_[如何准备好一场大厂面试](https://joonwhee.blog.csdn.net/article/details/108702592)_

_[MySQL 8.0 MVCC 核心原理解析（核心源码）](https://joonwhee.blog.csdn.net/article/details/108379583)_

_[921天，咸鱼到阿里的修仙之路](https://joonwhee.blog.csdn.net/article/details/106182747)_

_[复习2个月拿下美团offer，我都做了些啥](https://joonwhee.blog.csdn.net/article/details/106463578)_

![](https://i-blog.csdnimg.cn/blog_migrate/870c07e73831ded5f315ddfe8d9d9dde.png)
