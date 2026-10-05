---
source: "http://blog.csdn.net/a214919447/article/details/54892235"
title: "Maven设置本地仓库及依赖包下载不全的解决方法_eclipse maven local repository 不全-CSDN博客"
fetched_at: "2026-10-05 15:30:18"
---

[原文链接](http://www.imooc.com/article/11323)

1、maven设置本地仓库的方法：在apache-maven-3.3.9-bin/conf/setting.xml中加入<localRepository>E:\m2\repository</localRepository>

2、当你在pom.xml中加入坐标后，maven自动下载相应jar包，完成之后发现pom.xml内容没有报错但是就是有个红叉，应该就是有各别jar包缺失，可以在Maven Denpendencies右键build path 选择configure 里面就可以查看到miss的jar包  
接下来可以到你本地仓库的文件夹中根据miss jar包的路径打开文件夹，删除里面.lastUpdated（我连同pom 、sha1后缀一起也都删除了。。）然后 右键项目maven 中的disable maven nature 然后再右击项目中configure中的 convert maven 接下来项目又会重新下载 如果这样重复几次还是jar包始终下不下来，就到相应的网络仓库中去下 比如http://repo.maven.apache.org/  
去这个网站找需要的包 将其手动下载添加 然后再重复一下convert to maven

  

