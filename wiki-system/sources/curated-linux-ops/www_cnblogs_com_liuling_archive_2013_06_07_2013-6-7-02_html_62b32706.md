---
source: "http://www.cnblogs.com/liuling/archive/2013/06/07/2013-6-7-02.html"
title: "linux中搭建java开发环境 - 残剑_ - 博客园"
fetched_at: "2026-10-05 15:36:32"
---

今天试着在Linux下面搭建java开发环境，现总结一下具体步骤。

1、JDK的安装
执行下面命令安装JDK（首先创建/opt/java目录）
tar -xvf jdk-7u9-linux-i586.tar.gz -C /opt/java

ln -s /opt/java/jdk1.7.0_09 /opt/java/jdk 创建一个链接

vi /etc/frofile 设置环境变量

export JAVA_HOME=/opt/java/jdk
exprot PATH=$JAVA_HOME/bin:$PATH
相当于重新设置PATH=JAVA_HOME/bin+PATH

配置好之后要用命令source /etc/profile
执行java -version 命令测试一下jdk是否安装成功


2、tomcat的安装
解压安装
tar -xvf apache-tomcat-6.0.10.tar.gz -C /opt/tomcat/
ln -s /opt/tomcat/apache-tomcat-6.0.10 /opt/tomcat/tomcat6.0 创建一个链接
然后 cd /opt/tomcat/tomcat6.0/bin
执行./startup.sh
再打开浏览器测试一下,输入http:localhost:8080，看有没有那个猫的页面出来，有的话就说明安装成功了。

3、eclipse的安装
解压，gunzip eclipse-java-juno-SR2-linux-gtk.tar.gz
安装 tar -xvf eclipse-java-juno-SR2-linux-gtk.tar -C /opt
然后去图形界面进入/opt/eclipse目录，运行eclipse，就可以打开eclipse界面了。
