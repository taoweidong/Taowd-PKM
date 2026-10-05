---
source: "http://blog.sina.com.cn/s/blog_6a7cdcd40101b1j6.html"
title: "linux CentOS 6.5 中安装与配置JDK-7_梦幻飞雪_新浪博客"
fetched_at: "2026-10-05 15:35:02"
---

[![新浪博客](https://simg.sinajs.cn/blog7style/images/common/topbar/topbar_logo.gif)](https://blog.sina.com.cn)

![](https://simg.sinajs.cn/blog7style/images/common/loading.gif)加载中…

<http://blog.sina.com.cn/u/1786567892>

个人资料

![梦幻飞雪](https://simg.sinajs.cn/blog7style/images/common/sg_trans.gif)

![](https://simg.sinajs.cn/blog7style/images/common/sg_trans.gif) **梦幻飞雪**

[![](https://simg.sinajs.cn/blog7style/images/common/sg_trans.gif)微博](https://weibo.com/u/1786567892?source=blog)

[加好友](javascript:void\(0\);) [发纸条](javascript:void\(0\);)

[写留言](https://blog.sina.com.cn/s/profile_1786567892.html#write) 加关注

  * 博客等级：
  * 博客积分：**0**

  * 博客访问：**0**
  * 关注人气：**0**
  * 获赠金笔：**0支**
  * 赠出金笔：**0支**
  * 荣誉徽章：

正文 字体大小：[大](javascript:;) **中** [小](javascript:;)

## linux CentOS 6.5 中安装与配置JDK-7

(2013-10-22 09:29:37)

标签：

### 中安

### 不用

### 还是

### 软件

### 内容

|  分类： [linuxssh](https://blog.sina.com.cn/s/articlelist_1786567892_10_1.html)
---|---

系统环境：centos-6.5

安装方式：rpm安装

软件：jdk-7-linux-i586.rpm

下载地址：<http://www.oracle.com/technetwork/java/javase/downloads/index.html>

检验系统原版本

[root@localhost ~]# java -version

java version "1.7.0_24"

OpenJDK Runtime Environment (build 1.7.0_24-b18)

OpenJDK HotSpot(TM) Client VM (build 24.45-b08, mixed mode, sharing)

进一步查看JDK信息：

[root@localhost ~]# rpm -qa | grep java

tzdata-java-2012c-1.el6.noarch

java-1.7.0-openjdk-1.7.0.45-1.45.1.11.1.el6.x86_64

卸载OpenJDK，执行以下操作：

[root@localhost ~]# rpm -e \--nodeps tzdata-java-2012c-1.el6.noarch

[root@localhost ~]# rpm -e \--nodeps java-1.7.0-openjdk-1.7.0.45-1.45.1.11.1.el6.x86_64

安装JDK

上传新的jdk-7-linux-i586.rpm软件到/usr/local/执行以下操作：

[root@localhost ckb]# rpm -ivh jdk-7-linux-i586.rpm

JDK默认安装在/usr/java中。

验证安装

执行以下操作，查看信息是否正常：

[root@localhost bin]# java

[root@localhost bin]# javac

[root@localhost bin]# java -version

java version "1.7.0_45"

Java(TM) SE Runtime Environment (build 1.7.0_45-b18)

Java HotSpot(TM) Client VM (build 24.45-b08, mixed mode, sharing)

配置环境变量

我的机器安装完jdk-7-linux-i586.rpm后不用配置环境变量也可以正常执行javac、java –version操作，因此我没有进行JDK环境变量的配置。但是为了以后的不适之需，这里还是记录一下怎么进行配置，操作如下：

修改系统环境变量文件

vi + /etc/profile

向文件里面追加以下内容：

JAVA_HOME=/usr/java/jdk1.7.0_45

JRE_HOME=/usr/java/jdk1.7.0_45/jre

PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

CLASSPATH=:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib

export JAVA_HOME JRE_HOME PATH CLASSPATH

使修改生效

[root@localhost ~]# source /etc/profile  //使修改立即生效

[root@localhost ~]# echo $PATH  //查看PATH值

查看系统环境状态

[root@localhost ~]# echo $PATH

/usr/lib/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/java/jdk1.7.0_45/bin:

/usr/java/jdk1.7.0_45/jre/bin:/home/ckb/bin

分享：

![](https://simg.sinajs.cn/blog7style/images/common/sg_trans.gif)喜欢

0

![](https://simg.sinajs.cn/blog7style/images/common/sg_trans.gif)赠金笔

阅读 _┊_ [收藏](javascript:;) _┊_ [喜欢](javascript:;)[**▼**](javascript:;) _┊_[打印](https://blog.sina.com.cn/main_v5/ria/print.html?blog_id=blog_6a7cdcd40101b1j6) _┊_举报/Report

加载中，请稍候......

前一篇：[公钥与秘钥的理解](https://blog.sina.com.cn/s/blog_6a7cdcd40101ay40.html)

后一篇：[Linux CentOS 6.5中安装与配置Tomcat-8方法](https://blog.sina.com.cn/s/blog_6a7cdcd40101b1km.html)
