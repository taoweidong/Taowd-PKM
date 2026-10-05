---
source: "http://www.linuxidc.com/Linux/2017-05/143308.htm"
title: "Eclipse使用Maven搭建Java Web项目并直接部署Tomcat_服务器应用_Linux公社-Linux系统门户网站"
fetched_at: "2026-10-05 15:30:14"
---

[手机版](http://m.linuxidc.com)

你好，游客 登录 [注册](../../memberreg.aspx)

[![Linux公社](../../pic/logo.jpg)](https://www.linuxidc.com/) |   
---|---  
  
[首页](../../index.htm)[Linux新闻](../../it/)[Linux教程](../../Linuxit/)[数据库技术](../../MySql/)[Linux编程](../../RedLinux/)[服务器应用](../../Apache/)[Linux安全](../../Unix/)[Linux下载](../../download/)[Linux主题](../../theme/)[Linux壁纸](../../Linuxwallpaper/)[Linux软件](../../linuxsoft/)[数码](../../digi/)[手机](../../mobile/)[电脑](../../diannao/)

[首页](../../index.htm) → [服务器应用](../../Apache/)

背景：  阅读新闻

# Eclipse使用Maven搭建Java Web项目并直接部署Tomcat

| [日期：2017-05-02] | 来源：Linux社区 作者：hackyo | [字体：[大](javascript:ContentSize\(16\)) [中](javascript:ContentSize\(0\)) [小](javascript:ContentSize\(12\))]   
---|---|---  
  
1.环境：

Windows 10

[Java](../../Java "https://www.linuxidc.com/topicnews.aspx?tid=19") 1.8

Maven 3.3.9

Eclipse IDE for Java EE Developers

2.准备：

eclipse环境什么的不赘述，Maven环境还是要的

先下载Maven，地址：<http://maven.apache.org/download.cgi>

直接点apache-maven-3.3.9-bin.zip下载，然后解压到随便什么目录

![](../../upload/2017_05/170502073386232.png)

下好之后配置环境变量，在系统变量里新建：
    
    
    变量名：M2_HOME
    变量值：C:\Program Files\Maven   （你的Maven目录）

然后在Path变量最后插入：
    
    
    %M2_HOME%\bin

注意：和前面应该是有;分号间隔的

完成后在命令行里测试：mvn -v

![](../../upload/2017_05/170502073386233.png)

3.整合Eclipse、Maven：

现在打开eclipse--Window--preferences--Maven--Installations

点Add...-->>Directory...选择你的Maven目录后Finish

![](../../upload/2017_05/170502073386234.png)

然后继续左边选择Maven--User Settings，将两个配置文件目录都设置成Maven目录\conf\settings.xml

再点击Update Settings更新配置，点击OK后Maven和Eclipse的整合就完成了

![](../../upload/2017_05/1705020733862318.png)

4.建立并配置Maven项目：

File--New--Other...

选择Maven下的Maven Project，Next

![](../../upload/2017_05/170502073386235.png)

保持默认，Next

![](../../upload/2017_05/170502073386236.png)

这里选择webapp，Next

![](../../upload/2017_05/170502073386237.png)

输入包名，工程名，Package可以不填，Finish

![](../../upload/2017_05/170502073386238.png)

建好之后右击工程--Properties--Project Facets

![](../../upload/2017_05/170502073386239.png)

在这里先将Dynamic Web Services的勾去掉，将Java版本改为1.8，点击Apply

![](../../upload/2017_05/1705020733862310.png)

现在再将Dynamic Web Services勾上，版本改为3.1，同时下面会出现一行字，单击他！

![](../../upload/2017_05/1705020733862311.png)

修改里面Content directory为src/main/webapp，并将Generate...勾选，单击OK

![](../../upload/2017_05/1705020733862312.png)

可以看的右边有Runtimes选项，单击，选中其中你的Tomcat后单击OK结束设置

![](../../upload/2017_05/1705020733862313.png)

接下来先修改web.xml文件

![](../../upload/2017_05/1705020733862316.png)

将里面的代码全部改为下面的，保存退出
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://xmlns.jcp.org/xml/ns/javaee" xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd" id="WebApp_ID" version="3.1">
      <display-name>Demo</display-name>
    </web-app>

接下来再编辑pom.xml文件

先将junit的版本改为4.12，然后在<dependencies></dependencies>中加入以下代码，用以支持Servlet
    
    
        <dependency>
          <groupId>javax.servlet</groupId>
          <artifactId>javax.servlet-api</artifactId>
          <version>3.1.0</version>
        </dependency>

![](../../upload/2017_05/1705020733862314.png)

然后在<build></build>里面加入以下代码，用以Maven直接部署tomcat，并配置jdk版本

![复制代码](../../upload/2017_05/170502073386231.gif)
    
    
      <plugins>
          <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.6.1</version>
            <configuration>
              <source>1.8</source>
              <target>1.8</target>
            </configuration>
          </plugin>
          <plugin>
            <groupId>org.apache.tomcat.maven</groupId>
            <artifactId>tomcat7-maven-plugin</artifactId>
            <version>2.2</version>
            <configuration>
              <url>http://localhost:8080/manager/text</url>
              <username>tomcat</username>
              <password>tomcat</password>
            </configuration>
          </plugin>
        </plugins>

![复制代码](../../upload/2017_05/170502073386231.gif)

![](../../upload/2017_05/1705020733862315.png)

其中<username>tomcat</username>和<password>tomcat</password>是tomcat中配置的密码，稍后会继续说明

保存并退出，右击项目--Maven--Update Poject...更新配置，弹出框点击OK

5.配置Tomcat：

这个配置只需配置一次即可，并不是每个工程都需要配置

编辑Tomcat目录下/conf/tomcat-users.xml

在<tomcat-users></tomcat-users>标签中加入以下代码后，保存退出
    
    
    <role rolename="manager-gui"/>
    <role rolename="manager-script"/>
    <user username="tomcat" password="tomcat" roles="manager-gui,manager-script"/>

这里的用户名和密码是和上面Maven中配置相对应的

6.部署运行项目：

先运行Tomcat目录下/bin/startup.bat clean install tomcat7:redeploy

然后右击项目Run As--Maven build，在Goals中输入：clean install tomcat7:redeploy

![](../../upload/2017_05/1705020733862317.png)

单击Run即可运行项目，之后只需单击Maven build即可自动运行。

这时候在http://localhost:8080/项目名 即可看到

### Hello World!

如果工程有报错，可以将Eclipse中jre改一下

window--Preferences--java--Installed JREs，选择jdk目录下的jre后点OK即可

![](../../upload/2017_05/1705020733862319.png)

**本文永久更新链接地址** ：[http://www.linuxidc.com/Linux/2017-05/143308.htm](../../Linux/2017-05/143308.htm)

[![linux](/linuxfile/logo.gif)](http://www.linuxidc.com)

[Tomcat性能优化简述](../../Linux/2017-05/143306.htm)

[CentOS 使用 MUTT发送邮件](../../Linux/2017-05/143310.htm)

相关资讯 [TomCat部署](../../search.aspx?where=nkey&keyword=11710) [Java Web项目](../../search.aspx?where=nkey&keyword=51443)

  * [企业级Tomcat部署实践及安全调优](../../Linux/2017-11/148926.htm) (11/27/2017 22:17:11)
  * [Linux下Tomcat的简单部署](../../Linux/2017-02/140856.htm) (02/20/2017 19:28:16)
  * [Solr4.0的Tomcat部署及Solrj的简单](../../Linux/2014-05/102135.htm "Solr4.0的Tomcat部署及Solrj的简单使用教程") (05/23/2014 12:39:55)

| 

  * [Maven实现Tomcat热部署](../../Linux/2017-03/141397.htm) (03/05/2017 10:50:06)
  * [快速部署Tomcat项目的Shell脚本](../../Linux/2016-01/127258.htm) (01/10/2016 13:19:59)
  * [Tomcat Ubuntu 部署问题](../../Linux/2014-03/97958.htm) (03/10/2014 10:09:15)

  
---|---  
  
本文评论 [查看全部评论](../../remark.aspx?id=143308) (0)

表情： ![表情](../../pic/b.gif) 姓名：  匿名 字数    
  
同意评论声明 发表   
评论声明 

  * 尊重网上道德，遵守中华人民共和国的各项有关法律法规
  * 承担一切因您的行为而直接或间接导致的民事或刑事法律责任
  * 本站管理人员有权保留或删除其管辖留言中的任意内容
  * 本站有权在网站内转载或引用您的评论
  * 参与本评论即表明您已经阅读并接受上述条款

|   
---|---  
  
最新资讯

  * [如何在Java中获取当前日期和时间](../../Linux/2019-05/158797.htm)
  * [DVDStyler 3.1 发布，高清视频支持（如何安](../../Linux/2019-05/158796.htm "DVDStyler 3.1 发布，高清视频支持（如何安装）")
  * [Elastic Stack的核心安全功能现在免费提供](../../Linux/2019-05/158795.htm)
  * [Microsoft正式为macOS用户发布Microsoft ](../../Linux/2019-05/158794.htm "Microsoft正式为macOS用户发布Microsoft Edge Canary版本")
  * [Linux下递归更改文件夹和子文件夹的权限](../../Linux/2019-05/158793.htm)
  * [如何在Laravel 5中正确设置文件权限](../../Linux/2019-05/158792.htm)
  * [react新更新的context传递数据](../../Linux/2019-05/158791.htm)
  * [使用TypeScript开发React Native应用示例教](../../Linux/2019-05/158790.htm "使用TypeScript开发React Native应用示例教程")
  * [如何在Ubuntu 18.04上为MySQL配置SSL/TLS](../../Linux/2019-05/158789.htm)
  * [DragonFlyBSD 5.4.3 发布，各种修复](../../Linux/2019-05/158788.htm)

  
  
[Linux公社简介](https://www.linuxidc.com/aboutus.htm) \- [广告服务](https://www.linuxidc.com/adsense.htm) \- [网站地图](https://www.linuxidc.com/sitemap.aspx) \- [帮助信息](https://www.linuxidc.com/help.htm) \- [联系我们](https://www.linuxidc.com/contactus.htm)  
本站（LinuxIDC）所刊载文章不代表同意其说法或描述，仅为提供更多信息，也不构成任何建议。  
  
  
Copyright © 2006-2019 [Linux公社](https://www.linuxidc.com/) All rights reserved 浙ICP备07014134号-8 
