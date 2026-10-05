---
source: "http://www.cnblogs.com/quyanhui/p/6278587.html"
title: "Jenkins2.32.1+svn+maven安装配置与构建部署(一) - High阔天空 - 博客园"
fetched_at: "2026-10-05 15:29:58"
---

这两天学习了一下持久化集成工具Jenkins，在自己的本地搭建一个简单的Jenkins环境。

使用环境：Windows64系统，JDK1.8，eclipse，svn（Windows版本VisualSVN-Server-3.5.7-x64.msi），tomcat7，apache-maven-3.2.5，Jenkins_2.32.1等。

注：Jenkins2.32需要JDK7及以上版本；

**一、持续集成**

先了解一下持续集成的概念：持续集成是一种软件开发实践，即团队开发成员经常集成它们的工作，通过每个成员每天至少集成一次，也就意味着每天可能会发生多次集成。每次集成都通过自动化的构建（包括编译，发布，自动化测试）来验证，从而尽早地发现集成错误。而Jenkins就是基于Java开发的一种持续集成工具，用于监控持续重复的工作。

持续集成的核心价值：  
1）持续集成中的任何一个环节都是自动完成的，无需太多的人工干预，有利于减少重复过程以节省时间、费用和工作量；  
2）持续集成保障了每个时间点上团队成员提交的代码是能成功集成的。换言之，任何时间点都能第一时间发现软件的集成问题，使任意时间发布可部署的软件成为了可能；  
3）持续集成还能利于软件本身的发展趋势，这点在需求不明确或是频繁性变更的情景中尤其重要，持续集成的质量能帮助团队进行有效决策，同时建立团队对开发产品的信心。   
持续集成的原则：   
1）需要版本控制软件保障团队成员提交的代码不会导致集成失败。常用的版本控制软件有IBM Rational ClearCase、CVS、Subversion等；   
2）开发人员必须及时向版本控制库中提交代码，也必须经常性地从版本控制库中更新代码到本地；   
3）需要有专门的集成服务器来执行集成构建。根据项目的具体实际，集成构建可以被软件的修改来直接触发，也可以定时启动，如每半个小时构建一次；   
4）必须保证构建的成功。如果构建失败，修复构建过程中的错误是优先级最高的工作。一旦修复，需要手动启动一次构建。  
持续集成系统的组成 ：  
由此可见，一个完整的构建系统必须包括：  
1）一个自动构建过程，包括自动编译、分发、部署和测试等。  
2）一个代码存储库，即需要版本控制软件来保障代码的可维护性，同时作为构建过程的素材库。  
3）一个持续集成服务器。本文中介绍的Jenkins就是一个配置简单和使用方便的持续集成服务器。

**二、Jenkins是什么？**

Jenkins是一个开源软件项目，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。

功能: 1、持续的软件版本发布/测试项目。 

2、监控外部调用执行的工作。

特性：

1.开源  
2.安装、配置简单--只要把jenkins.war部署到servlet容器，不需要数据库支持，所有配置都是通过其提供的web界面实现。  
3.集成RSS/E-mail通过RSS发布构建结果或当构建完成时通过e-mail通知。  
4.生成JUnit/TestNG测试报告。  
5\. Jenkins支持分布式构建  
6.插件支持:支持扩展插件，目前有几百个现成的插件可以使用，这些插件涵盖从版本控制、构建工具、代码质量、构建通知、集成外部系统、 UI定制、游戏等等各个方面。

**三、安装配置**

jenkins官网：https://jenkins.io/index.html，选择适合自己的版本下载即可。我的版本  for Windows。

**1.安装：** 解压zip文件得到，双击安装即可，根据自己的需求选择要安装的目录。我的安装目录如下：

安装完成后如何验证一下是否成功呢？Jenkins.war！

验证方式:执行命令行或直接将Jenkins.war放到tomcat webapps下启动服务即可

（1）打开cmd命令行，进入到Jenkins安装目录，直接运行j[ava](http://lib.csdn.net/base/javase "Java SE知识库") -jar jenkins.war 默认的端口是8080（在jenkins.xml中配置），也可执行j[ava](http://lib.csdn.net/base/javase "Java SE知识库") -jar jenkins.war --httpPort=7080，自定义其他端口验证

启动成功如下：

（2）直接将Jenkins.war放到tomcat webapps下启动服务即可。

上述两种方式启动成功后，访问http://localhost:7080，根据提示设置用户登录信息，我的已设置直接进入登录页面

输入用户名密码登录：成功！！！

**2.配置：** 进入 系统管理--[Global Tool Configuration](http://localhost:7080/jenkins/configureTools)

配置JDK,MAVEN

配置完成后保存。接下来就可以新建job了。

**3.返回首页，新建任务** ，点击 新建 按钮，

输入任务名称，选择构建一个自由风格的软件项目并保存。

在general里面更具自己想需要勾选，包括工作空间，默认C:\Users\admin\\.jenkins\workspace;

注意：如果有多个项目，（1）建议工作空间+项目名称，例：C:\Users\admin\\.jenkins\workspace\demo,demo为项目名称，也可取其它名称，这样会在工作空间下新建不同目录，以便区分不同项目；（2）如果选择默认空间，可在“源码管理” 模块 Local module directory文本框中输入自己的项目名称，以区分不同项目

原码管理，在此我使用svn；填写Repository URL及Credentials，及svn的地址及用户信息，其中Credentials在首页Credentials选项新建;

注意：如果是Maven项目，且有多个模块，则Repository URL路径指向所有项目的根地址

在首页Credentials选项新建，输入svn的账号和密码

构建触发器：

Poll SCM：定时检查源码变更（根据SCM软件的版本号），如果有更新就checkout最新code下来，然后执行构建动作。我的配置如下：  
*/5 * * * * （每5分钟检查一次源码变化）  
Build periodically：周期进行项目构建（它不care源码是否发生变化），我的配置如下：  
0 2 * * * （每天2:00 必须build一次源码）

**4.项目构建：**

maven version : 选之前录入的maven;  
Goals选项输入打包编译时要执行的命令，如：clean package/clean install;  
POM选项选择pom文件所在的相对位置，如果有多个Maven模块，选择父级的pom.xml;

保存，首页左侧 点击 立即构建 选项即可构建项目了。

查看构建日志：

日志信息：

构建成功！！！如报一下错误：

解决方案：

(a)_修改pom.xml文件_

<build>  
<finalName>demo</finalName>  
</build>

添加<defaultGoal>install</defaultGoal>

即：

<build>  
<defaultGoal>install</defaultGoal>  
<finalName>demo</finalName>  
</build>

(b)指定默认Goals

重新构建。

**5.部署项目：**

构建后操作：

配置后保存，重新构建，其中demo是我web项目的名称，此处的http://localhost:8081，是部署demo项目的服务器和端口

WAR/EAR files:target\demo.war,是构建后生成的war包，正常情况下打包成功后就会部署到tomcat下webapps目录下，如

果构建成功，但没有自动部署，修改WAR/EAR files:**/*.war试试。

构建成功后，即可登录项目验证：

到此Jenkins部署就完成了！！！！！！！！！！！！！！

最后还有一个自动部署的问题：上面我们已经配置了构建触发器，那怎么用呢？

看管理插件：

已安装插件，如果在已安装插件未找到，即未安装，可在可选插件中搜素安装即可。

。。。。。。。。。
