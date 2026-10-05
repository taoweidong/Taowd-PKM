---
source: "http://hadoop.apache.org/docs/r1.0.4/cn/quickstart.html"
title: "Hadoop快速入门"
fetched_at: "2026-10-05 15:43:41"
---

[Apache](https://www.apache.org/) > [Hadoop](https://hadoop.apache.org/) > [Core](https://hadoop.apache.org/core/)

[![Hadoop](images/hadoop-logo.jpg)](https://hadoop.apache.org/)

[![Hadoop](images/core-logo.gif)](https://hadoop.apache.org/core/)

  * [项目](https://hadoop.apache.org/core/)
  * [维基](https://wiki.apache.org/hadoop)
  * [Hadoop 0.18文档](index.html)

文档

[概述](index.html)

快速入门

[集群搭建](cluster_setup.html)

[HDFS构架设计](hdfs_design.html)

[HDFS使用指南](hdfs_user_guide.html)

[HDFS权限指南](hdfs_permissions_guide.html)

[HDFS配额管理指南](hdfs_quota_admin_guide.html)

[命令手册](commands_manual.html)

[FS Shell使用指南](hdfs_shell.html)

[DistCp使用指南](distcp.html)

[Map-Reduce教程](mapred_tutorial.html)

[Hadoop本地库](native_libraries.html)

[Streaming](streaming.html)

[Hadoop Archives](hadoop_archives.html)

[Hadoop On Demand](hod.html)

[API参考](https://hadoop.apache.org/core/docs/r0.18.2/api/index.html)

[API Changes](https://hadoop.apache.org/core/docs/r0.18.2/jdiff/changes.html)

[维基](https://wiki.apache.org/hadoop/)

[常见问题](https://wiki.apache.org/hadoop/FAQ)

[邮件列表](https://hadoop.apache.org/core/mailing_lists.html)

[发行说明](https://hadoop.apache.org/core/docs/r0.18.2/releasenotes.html)

[变更日志](https://hadoop.apache.org/core/docs/r0.18.2/changes.html)

![](skin/images/rc-b-l-15-1body-2menu-3menu.png)

[![PDF -icon](skin/images/pdfdoc.gif)
PDF](quickstart.pdf)

# Hadoop快速入门

  * 目的
  * 先决条件
    * 支持平台
    * 所需软件
    * 安装软件
  * 下载
  * 运行Hadoop集群的准备工作
  * 单机模式的操作方法
  * 伪分布式模式的操作方法
    * 配置
    * 免密码ssh设置
    * 执行
  * 完全分布式模式的操作方法

## 目的

这篇文档的目的是帮助你快速完成单机上的Hadoop安装与使用以便你对[Hadoop分布式文件系统(HDFS)](hdfs_design.html)和Map-Reduce框架有所体会，比如在HDFS上运行示例程序或简单作业等。

## 先决条件

### 支持平台

  * GNU/Linux是产品开发和运行的平台。 Hadoop已在有2000个节点的GNU/Linux主机组成的集群系统上得到验证。
  * Win32平台是作为 _开发平台_ 支持的。由于分布式操作尚未在Win32平台上充分测试，所以还不作为一个 _生产平台_ 被支持。

### 所需软件

Linux和Windows所需软件包括:

  1. JavaTM1.5.x，必须安装，建议选择Sun公司发行的Java版本。
  2. **ssh** 必须安装并且保证 **sshd** 一直运行，以便用Hadoop 脚本管理远端Hadoop守护进程。

Windows下的附加软件需求

  1. [Cygwin](http://www.cygwin.com/) \- 提供上述软件之外的shell支持。

### 安装软件

如果你的集群尚未安装所需软件，你得首先安装它们。

以Ubuntu Linux为例:

$ sudo apt-get install ssh
$ sudo apt-get install rsync

在Windows平台上，如果安装cygwin时未安装全部所需软件，则需启动cyqwin安装管理器安装如下软件包：

  * openssh - _Net_ 类

## 下载

为了获取Hadoop的发行版，从Apache的某个镜像服务器上下载最近的 [稳定发行版](https://hadoop.apache.org/core/releases.html)。

## 运行Hadoop集群的准备工作

解压所下载的Hadoop发行版。编辑 conf/hadoop-env.sh文件，至少需要将JAVA_HOME设置为Java安装根路径。

尝试如下命令：
$ bin/hadoop
将会显示**hadoop** 脚本的使用文档。

现在你可以用以下三种支持的模式中的一种启动Hadoop集群：

  * 单机模式
  * 伪分布式模式
  * 完全分布式模式

## 单机模式的操作方法

默认情况下，Hadoop被配置成以非分布式模式运行的一个独立Java进程。这对调试非常有帮助。

下面的实例将已解压的 conf 目录拷贝作为输入，查找并显示匹配给定正则表达式的条目。输出写入到指定的output目录。
$ mkdir input
$ cp conf/*.xml input
$ bin/hadoop jar hadoop-*-examples.jar grep input output 'dfs[a-z.]+'
$ cat output/*

## 伪分布式模式的操作方法

Hadoop可以在单节点上以所谓的伪分布式模式运行，此时每一个Hadoop守护进程都作为一个独立的Java进程运行。

### 配置

使用如下的 conf/hadoop-site.xml:

<configuration>
---

<name>fs.default.name</name>
<value>localhost:9000</value>


<name>mapred.job.tracker</name>
<value>localhost:9001</value>


<name>dfs.replication</name>
<value>1</value>

</configuration>

### 免密码ssh设置

现在确认能否不输入口令就用ssh登录localhost:
$ ssh localhost

如果不输入口令就无法用ssh登陆localhost，执行下面的命令：
$ ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
$ cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys

### 执行

格式化一个新的分布式文件系统：
$ bin/hadoop namenode -format

启动Hadoop守护进程：
$ bin/start-all.sh

Hadoop守护进程的日志写入到 ${HADOOP_LOG_DIR} 目录 (默认是 ${HADOOP_HOME}/logs).

浏览NameNode和JobTracker的网络接口，它们的地址默认为：

  * NameNode \- <http://localhost:50070/>
  * JobTracker \- <http://localhost:50030/>

将输入文件拷贝到分布式文件系统：
$ bin/hadoop fs -put conf input

运行发行版提供的示例程序：
$ bin/hadoop jar hadoop-*-examples.jar grep input output 'dfs[a-z.]+'

查看输出文件：

将输出文件从分布式文件系统拷贝到本地文件系统查看：
$ bin/hadoop fs -get output output
$ cat output/*

或者

在分布式文件系统上查看输出文件：
$ bin/hadoop fs -cat output/*

完成全部操作后，停止守护进程：
$ bin/stop-all.sh

## 完全分布式模式的操作方法

关于搭建完全分布式模式的，有实际意义的集群的资料可以在[这里](cluster_setup.html)找到。

_Java与JNI是Sun Microsystems, Inc.在美国以及其他国家地区的商标或注册商标。_

Copyright © 2007 [The Apache Software Foundation.](https://www.apache.org/licenses/)
