---
source: "https://www.cnblogs.com/EasonJim/p/6394434.html"
title: "Jenkins内存溢出的处理方法 - EasonJim - 博客园"
fetched_at: "2026-10-05 15:30:03"
---

参考：<http://openwares.net/java/jenkens_deploy_to_tomcat_error_of_outofmemoryerror.html>上的说明，有如下解释：

**-Xms：** 初始堆内存大小

**-Xmx：** 最大堆内存大,一般设置-Xms与-Xmx一样大小,根据应用类型和物理内存大小来决定二者的大小

**-Xmn或者-XX:NewSize：** 堆内存中年轻代的大小

**-XX:PermSize：** 永久代内存的初始大小

**-XX:MaxPermSize：** 永久代内存的最大值

以上参数都是针对jvm的内存配置。更详细的参数说明，请参考：<http://blog.csdn.net/kongls08/article/details/8468713>

实际上，这个是tomcat的配置，一般部署jenkins时，采用war包的形式部署，那么直接修改tomcat的启动参数。

同样，如果直接使用java -jar以jetty的形式启动，也是修改启动参数即可。

具体实现方式：

1、在windows上采用msi安装包安装的，找到"C:\Program Files (x86)\Jenkins\jenkins.xml"的文件，然后找到arguments节点，参照以上参数修改成合适的值。如：-Xms64m -Xmx256m -XX:PermSize=128M -XX:MaxNewSize=256m -XX:MaxPermSize=256m

2、如果以war包部署到tomcat的，直接修改tomcat的启动命令：

①如果以zip包下载的tomcat，那么直接修改如下文件：

（windows）在catalina.bat的第一行增加：set JAVA_OPTS=-Xms64m -Xmx256m -XX:PermSize=128M -XX:MaxNewSize=256m -XX:MaxPermSize=256m

（linux/mac）在catalina.sh的第一行增加：JAVA_OPTS=-Xms64m -Xmx256m -XX:PermSize=128M -XX:MaxNewSize=256m -XX:MaxPermSize=256m

②如果是以windows服务安装的tomcat，那么直接在服务管理器上直接增加启动的参数，找到安装目录下bin文件夹的Tomcat7w.exe，打开，在java的选项卡上加上如上的配置参数，如下所示：

![](https://images2015.cnblogs.com/blog/417876/201702/417876-20170213163104019-1232810328.png)

总结：

其实要说jenkins的内存溢出，我觉得应该是jvm的调优才对，所以在找关键字解决这类问题时，应该转变思路，查找jvm方面的解决方案。

以下是参考第一个网址给出的16G内存服务器的配置解决方案，可以尝试一下。


    -Xmx5120m -Xms5120m -Xmn1024m -XX:PermSize=1024m -XX:MaxPermSize=1024m
