---
source: "http://www.cnblogs.com/yangang2013/p/5651906.html"
title: "Maven基础学习(一)—Maven入门 - ✈✈✈ - 博客园"
fetched_at: "2026-10-05 15:30:17"
---

# 一、概述

Maven是一个项目管理工具，它包含了一个项目对象模型(Project Object Model)，一组标准集合，一个项目生命周期(Project Lifecycle)，一个依赖管理系统(Dependency Management System)，和用来运行定义在生命周期阶段(phase)中插件(plugin)目标(goal)的逻辑。当你使用Maven的时候，你用一个明确定义的项目对象模型来描述你的项目，然后Maven可以应用横切的逻辑，这些逻辑来自一组共享的（或者自定义的）插件。   
Maven有一个生命周期，当你运行mvn install的时候被调用。这条命令告诉Maven执行一系列的有序的步骤，直到到达你指定的生命周期。遍历生命周期旅途中的一个影响就是，Maven 运行了许多默认的插件目标，这些目标完成了像编译和创建一个JAR文件这样的工作。   
此外，Maven能够很方便的帮你管理项目报告，生成站点，管理JAR文件，等等。

## 1.项目的构建流程

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231142749-1268611930.png)

## 2.Maven模型

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231145061-1431615939.png)

## 3.Maven的约定

src/main/java: 存放项目的java文件。

src/main/resources: 存放项目的资源文件，如spring，hibernate的配置文件。

src/test/java: 存放所有的测试的java文件。

src/test/resources: 存放测试用的资源文件。

target: 项目输出位置。

pom.xml 文件

# 二、基础入门

## 1.下载jar包并解压

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231147921-282061464.png)

**bin:** 含有mvn运行的脚本。 

**boot:** 含有plexus-classworlds类加载器框架 。

**conf:** 含有settings.xml配置文件。 

**lib:** 含有Maven运行时所需要的java类库。 

LICENSE.txt, NOTICE.txt, README.txt针对Maven版本，第三方软件等简要介绍。

## 2.配置环境变量

**(1)在path路径添加Maven的bin目录路径**

D:\maven-3.3.9\bin

**(2)添加环境变量 M2_HOME**

M2_HOME = D:\maven-3.3.9

## 3.建库

**(1)打开路径**

**C:\Users\Administrator\\.m2**

**(2)复制settings.xml到上述路径**

D:\maven-3.3.9\conf目录下有settings.xml文件，复制到上面的路径下。

**(3)修改settings.xml文件**

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231149467-1474235630.png)

**(4)配置Eclipse**

****

**第一步**

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231150905-479852215.png)

**第二步**

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231200155-1508864588.png)

**第三步**

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231202264-193750955.png)

-Dmaven.multiModuleProjectDirectory=$M2_HOME

## 4.Hello

**(1)新建一个MavenProject**

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231204483-321691051.png)

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231206171-947840631.png)

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231208061-537348369.png)

**(2)创建Java文件**

稍等片刻，这个工程左上角会出现M字样。

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231209436-542665887.png)

****

**One.java**
    
    
    public class One{
    
    	public String say(String name){
    	
    		return "Hello Maven " + name;
    	}
    }

**OneTest.java**
    
    
    public class OneTest{
    	
    	@Test
    	public void testOne(){
    		One one = new One();
    		String result = one.say("AAA");
    		Assert.assertEquals("Hello Maven AAA",result);
    	}
    }

**(3)运行项目**

单击右键项目"run as"--->maven build，在Navigator视图下可以看到target目录下有文件了。

[](http://images2015.cnblogs.com/blog/496517/201607/496517-20160707231211077-458667928.png)

**(4)POM文件的解释**
    
    
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
      
      <!-- 模型版本号 -->
      <modelVersion>4.0.0</modelVersion> 
      <!-- 群组ID: 公司域名反写 -->
      <groupId>com.kiwi</groupId>
      <!-- 项目ID: 一个公司只有一个域名，但是可以有多个项目 -->
      <artifactId>One</artifactId>
      <!-- 版本号: 用于描述开发过程的阶段性标识-->
      <version>0.0.1-SNAPSHOT</version>
    
      <!-- 默认字符集 -->
      <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
      </properties>
    
     <!-- 依赖管理 -->
      <dependencies>
    	  	<!-- 具体的依赖 -->
    	    <dependency>
    		      <groupId>junit</groupId>
    		      <artifactId>junit</artifactId>
    		      <version>4.9</version>
    		      <scope>test</scope>
    	    </dependency>
      </dependencies>
    </project>
