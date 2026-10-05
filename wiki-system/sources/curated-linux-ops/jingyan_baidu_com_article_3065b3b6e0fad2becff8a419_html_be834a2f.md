---
source: "http://jingyan.baidu.com/article/3065b3b6e0fad2becff8a419.html"
title: "Linux终端如何安装Tomcat 7-百度经验"
fetched_at: "2026-10-05 15:34:50"
---

# Linux终端如何安装Tomcat 7

  * 原创
  * |
  * 浏览：20433
  * |
  * 更新：2014-08-04 14:09
  * |
  * 标签：[tomcat](/tag?tagName=tomcat)

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=1)1

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=2)2

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=3)3

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=4)4

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=5)5

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=6)6

  * [](/album/3065b3b6e0fad2becff8a419.html?picindex=7)7

[分步阅读](/album/3065b3b6e0fad2becff8a419.html)

本次安装建立在Ubuntu 14.04上。采用putty连接终端。

## [](javascript:;)安装Jdk

  1. 1

由于Tomcat需要JDK的支持，所以在安装Tomcat之前需要先安装JDK。假如安装了JDK则跳过该步，直接看安装Tomcat7。

首先打开Java SE的官网，选择屏幕中下方的Java SE 7u65 JDK下载。

  2. 2

然后根据自己的linux系统选择相应的版本，比如我的ubuntu是x64的，所以我选择jdk-7u65-linux-x64.tar.gz下载。

  3. 3

如果用户操作的是linux图形化界面，直接打开浏览器下载即可。

假如是像我等这样，操作着终端，只能苦逼的使用wget命令进行下载了。

这里需要注意，官网上需要做一个选择。只有同意后才能够进行下载。这里将下载的命令写出来，大家直接复制即可。或者是通过获取Cookie来进行修改。

wget --no-cookie --header "Cookie: s_cc=true; oraclelicense=accept-securebackup-cookie; s_nr=1407131063040; gpw_e24=http%3A%2F%2Fwww.oracle.com%2Ftechnetwork%2Fjava%2Fjavase%2Fdownloads%2Fjdk7-downloads-1880260.html; s_sq=%5B%5BB%5D%5D" http://download.oracle.com/otn-pub/java/jdk/7u65-b17/jdk-7u65-linux-x64.tar.gz

  4. 4

下载下来以后，我们将其移到我们创建的一个目录中。

mv /alidata/download/jdk-7u65-linux-x64.tar.gz /alidata/server

然后进行解压

tar -zxvf /alidata/server/jdk-7u65-linux-x64.tar.gz

  5. 5

解压以后，我们需要编辑profile文件，相当于Windows中配置JDK那样设置环境变量。

输入vi /etc/profile进行编辑。

  6. 6

配置成功后，需要关闭终端，重新进入，输入java -version，如果出现如下内容，则证明JDK安装成功。

END

## [](javascript:;)安装Tomcat 7

  1. 1

首先同样我们需要将Tomcat 7下载下来。打开Tomcat的官网。

我们选择左边的Tomcat 7下载

  2. 2

选择tar.gz下载方式，复制下载地址，在linux终端中输入:

wget -c 下载地址

进行下载。

  3. 3

下载下来以后，同样，复制到/alidata/server目录中，该目录存放有jdk,tomcat等服务。

mv /alidata/download/apache-tomcat-7.0.54.tar.gz /alidata/server

然后进行解压

tar -zxvf /alidata/server/apache-tomcat-7.0.54.tar.gz

  4. 4

当解压成功以后，我们直接进入到tomcat bin目录中。

输入 ./startup.sh启动Tomcat，假如显示Tomcat started，则表明启动成功。

  5. 5

输入地址，假如能够成功的访问到Tomcat的默认界面表示成功.

Tomcat的默认端口为8080

END

## [](javascript:;)注意事项

  * Tomcat的默认端口为8080

  * 由于系统的不一样，可能其他系统配置环境变量不是/etc/profile

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
