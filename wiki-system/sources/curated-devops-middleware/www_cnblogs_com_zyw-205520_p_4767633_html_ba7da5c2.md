---
source: "http://www.cnblogs.com/zyw-205520/p/4767633.html"
title: "Eclipse+Tomcat+MAVEN+SVN项目完整环境搭建 - 酷玩时刻 - 博客园"
fetched_at: "2026-10-05 15:30:14"
---

## 1.JDK的安装

首先下载JDK，这个从sun公司官网可以下载，根据自己的系统选择64位还是32位，安装过程就是next一路到底。安装完成之后当然要配置环境变量了。

———————————————————————————————————————————————————

1.1新建变量名：JAVA_HOME 变量值：E:\Java\jdk1.6.0_43（这是我的jdk安装路径）

1.2编辑变量名：Path 在后面加上：%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin

1.3 新建变量名：CLASSPATH 变量值： .;%JAVA_HOME%\lib;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar

（注意：在设置变量的末尾时不要加上“；”）

———————————————————————————————————————————————————

设置完成之后我们当然需要测试，打开“运行”-->输入“CMD"-->在命令行上面输入：java，然后回车；输入javac，回车，输入java -version，回车，如果出现下列三个画面，那么JDK配置成功，否则就需要检查环境变量的配置。

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828184836297-33049194.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828184815406-301835825.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828184850890-1079694292.png)

## 2.Eclipse的安装

下载地址：http://www.eclipse.org/downloads/ 版本自行选择 

完成之后我们启动Eclipse，设置好工作路径，也可以直接默认。我们打开window-->preference输入jre，安装下图

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828185304219-909517504.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828190251437-403272735.png)

此时我们可以随便建立一个JAVA项目，然后编写一个helloworld来测试一下是否正确。

## 3.Tomcat8的安装

Tomcat我使用的版本是8，大家可以到apache的官网上去下载，[http://tomcat.apache.org](http://tomcat.apache.org/download-80.cgi)，下载直接解压就行

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828190448875-2048839166.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828190629703-89662533.png)

## 5.Maven安装配置

### 5.1 maven配置环境变量 

下载maven，就是一个包：apache-maven-3.2.1，我用的版本是3.2.1，解压到一个路径，然后配置环境变量：

——————————————————————————————————————————————————

5.1 新建变量名：MAVEN_HOME 变量值：D:\server\apache-maven-3.2.1（这是我的MAVEN路径）

5.2 编辑变量名：Path 在最前面加上：%MAVEN_HOME%\bin;（注意，最后要有个";"作为分隔符）

——————————————————————————————————————————————————

完成之后，在命令行输入：mvn -version查看是否有以下内容，如果有表示配置成功。

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150828190819234-882295285.png)

### 5.2Maven数据仓库的配置 

MAVEN中还有一个重要的配置就是数据仓库的路径配置，我们找到MAVEN的安装路径，进入conf-->打开settings.xml，找到localRepository标签，此时是被注释掉的，我们解除注释，然后配置一个路径，例如：E:\Dev\Java\maven\repo，这样以后MAVEN管理下载的jar包都会在这个路径下。当然我们需要建这样一个目录结构，然后还要讲settings.xml复制一份到E:\Dev\Java\maven下，这个在与Eclipse集成时会用到。**修改默认保存路径**

**![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829203627344-2088280037.png)**

### 5.3Eclipse中集成Maven 

在preferences中进行配置，如图：

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829204010922-1975818603.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829204215719-809768030.png)

此时，点击File-->new-->other-->输入maven-->\-->Maven Project，如果可以看到这些，证明配置成功，已经可以建立Maven项目了。

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829204454765-1161572702.png)![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829204928656-1589383472.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829204944172-1087694389.png)![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829204953047-22835249.png)

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829205005375-1380967534.png)

如果indexjsp 提示有错误需要在pom.xml中导入 javaee-api.jar
    
    
    <dependency>
                <groupId>javax</groupId>
                <artifactId>javaee-api</artifactId>
                <version>7.0</version>
    </dependency>

## 6.SVN安装

参考之前写的博客地址：<http://www.cnblogs.com/zyw-205520/p/4598091.html>

![](https://images2015.cnblogs.com/blog/441423/201508/441423-20150829205515859-847674917.png)

**到此Eclipse+Tomcat+MAVEN+SVN项目完整环境搭建完成 如果疑问欢迎评论 如果此文件对你有用 请点击下面的 推荐 关注我**
