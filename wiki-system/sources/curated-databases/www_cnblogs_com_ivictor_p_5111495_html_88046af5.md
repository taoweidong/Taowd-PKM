---
source: "https://www.cnblogs.com/ivictor/p/5111495.html"
title: "MyCAT简易入门 - iVictor - 博客园"
fetched_at: "2026-10-05 15:29:42"
---

MyCAT是mysql中间件，前身是阿里大名鼎鼎的Cobar，Cobar在开源了一段时间后，不了了之。于是MyCAT扛起了这面大旗，在大数据时代，其重要性愈发彰显。这篇文章主要是MyCAT的入门部署。

**一、安装java**

因Mycat是用java开发的，所以需要在实验环境下安装java，官方建议jdk1.7及以上版本

Java Oracle官方下载地址为：

<http://www.oracle.com/technetwork/java/javase/archive-139210.html>

解压jdk-7u79-linux-x64.tar.gz文件，并配置java的环境变量

# tar xvf jdk-7u79-linux-x64.tar.gz

# mv jdk1.7.0_79/ /usr/local/

编辑/etc/profile文件

# vim /etc/profile 添加如下内容
    
    
    export JAVA_HOME=/usr/local/jdk1.7.0_79
    export PATH=$JAVA_HOME/bin:$PATH
    export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

# source /etc/profile --使/etc/profile文件生效

# java -version
    
    
    java version "1.7.0_79"
    Java(TM) SE Runtime Environment (build 1.7.0_79-b15)
    Java HotSpot(TM) 64-Bit Server VM (build 24.79-b02, mixed mode)

**二、安装MySQL**

MySQL官方下载地址如下：

<http://dev.mysql.com/downloads/mysql/>

![](https://images2015.cnblogs.com/blog/576154/201601/576154-20160107221239684-1402862656.png)

里面有各种版本，包括RPM，二进制，源码包。

为了方便起见，我这里选择是RPM包

# yum install -y mysql-community-server-5.6.26-2.el5.x86_64.rpm

启动MySQL

# /etc/init.d/mysqld start
    
    
    Starting mysqld (via systemctl):                           [  OK  ]

为root账户创建密码

# mysqladmin -u root password "123456"

建议为123456，后面MyCAT配置文件schema.xml中会用到

**三、安装MyCAT**

创建MyCAT用户并设置密码

# useradd mycat

# passwd mycat

解压MyCAT文件

# tar xvf Mycat-server-1.5-alpha-20151221110028-linux.tar.gz

# mv mycat/ /usr/local/

设置mycat目录的属主和属组

# chown -R mycat.mycat /usr/local/mycat/

**四、测试MyCAT**

首先在MySQL上创建三个数据库：db1，db2，db3。
    
    
    mysql> create database db1;
    Query OK, 1 row affected (0.00 sec)
    
    mysql> create database db2;
    Query OK, 1 row affected (0.00 sec)
    
    mysql> create database db3;
    Query OK, 1 row affected (0.00 sec)

启动mycat服务

# cd /usr/local/mycat/bin/

# ./mycat start
    
    
    Starting Mycat-server...

查看mycat服务是否启动

# ps -ef |grep mycat
    
    
    root       9640   7257  0 22:47 pts/3    00:00:00 grep --color=auto mycat

并没有启动

查看日志

# cd /usr/local/mycat/logs/

# cat wrapper.log
    
    
    STATUS | wrapper  | 2016/01/07 22:44:23 | --> Wrapper Started as Daemon
    STATUS | wrapper  | 2016/01/07 22:44:23 | Launching a JVM...
    ERROR  | wrapper  | 2016/01/07 22:44:25 | JVM exited while loading the application.
    INFO   | jvm 1    | 2016/01/07 22:44:25 | Error: Exception thrown by the agent : java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException: MySQL-Server1: MySQL-Server1: Name or service not known
    STATUS | wrapper  | 2016/01/07 22:44:29 | Launching a JVM...
    ERROR  | wrapper  | 2016/01/07 22:44:29 | JVM exited while loading the application.
    INFO   | jvm 2    | 2016/01/07 22:44:29 | Error: Exception thrown by the agent : java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException: MySQL-Server1: MySQL-Server1: Name or service not known
    STATUS | wrapper  | 2016/01/07 22:44:34 | Launching a JVM...
    ERROR  | wrapper  | 2016/01/07 22:44:34 | JVM exited while loading the application.
    INFO   | jvm 3    | 2016/01/07 22:44:34 | Error: Exception thrown by the agent : java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException: MySQL-Server1: MySQL-Server1: Name or service not known
    STATUS | wrapper  | 2016/01/07 22:44:38 | Launching a JVM...
    ERROR  | wrapper  | 2016/01/07 22:44:38 | JVM exited while loading the application.
    INFO   | jvm 4    | 2016/01/07 22:44:38 | Error: Exception thrown by the agent : java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException: MySQL-Server1: MySQL-Server1: Name or service not known
    STATUS | wrapper  | 2016/01/07 22:44:42 | Launching a JVM...
    ERROR  | wrapper  | 2016/01/07 22:44:43 | JVM exited while loading the application.
    INFO   | jvm 5    | 2016/01/07 22:44:43 | Error: Exception thrown by the agent : java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException: MySQL-Server1: MySQL-Server1: Name or service not known
    FATAL  | wrapper  | 2016/01/07 22:44:43 | There were 5 failed launches in a row, each lasting less than 300 seconds.  Giving up.
    FATAL  | wrapper  | 2016/01/07 22:44:43 |   There may be a configuration problem: please check the logs.
    STATUS | wrapper  | 2016/01/07 22:44:43 | <-- Wrapper Stopped

根据报错信息，怀疑主机名没有绑定

修改hosts文件，绑定主机名

# vim /etc/hosts
    
    
    127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
    ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
    192.168.244.144 MySQL-Server1

重新启动mycat服务

# cd /usr/local/mycat/bin/

# ./mycat start

这次mycat正常启动

# ps -ef |grep mycat
    
    
    root      10725      1  0 22:54 ?        00:00:00 /usr/local/mycat/bin/./wrapper-linux-x86-64 /usr/local/mycat/conf/wrapper.conf wrapper.syslog.ident=mycat wrapper.pidfile=/usr/local/mycat/logs/mycat.pid wrapper.daemonize=TRUE wrapper.lockfile=/var/lock/subsys/mycat
    root      10881   7257  0 22:55 pts/3    00:00:00 grep --color=auto mycat

下面以Travelrecord为例，来进行插入，查询，路由分析等基本操作。

首先利用mycat连接mysql数据库

# mysql -utest -ptest -h127.0.0.1 -P8066 -DTESTDB

其中8066是mycat的监听端口，类似于mysql的3306端口，其中-u，-p，-h分别是用户名，密码和主机，-D是连接的逻辑库。

至于为什么是这些，这个跟配置文件有关。

![](https://images2015.cnblogs.com/blog/576154/201601/576154-20160107230440762-1826952583.png)

红色部分表明连接的是mycat。

创建Travelrecord表
    
    
    create table travelrecord (id bigint not null primary key,user_id varchar(100),traveldate DATE, fee decimal,days int);

插入数据
    
    
    mysql> insert into travelrecord(id,user_id,traveldate,fee,days)  values(1,'Victor',20160101,100,10);
    Query OK, 1 row affected (0.00 sec)
    
    mysql> insert into travelrecord(id,user_id,traveldate,fee,days)  values(5000001,'Job',20160102,100,10);
    Query OK, 1 row affected (0.00 sec)
    
    mysql> insert into travelrecord(id,user_id,traveldate,fee,days)  values(10000001,'Slow',20160103,100,10);
    Query OK, 1 row affected (0.00 sec)

至于ID为什么取三个值，这个与conf目录下autopartition-long.txt的定义有关，这个文件主要定义auto-sharding-long的规则。
    
    
    # range start-end ,data node index
    # K=1000,M=10000.
    0-500M=0
    500M-1000M=1
    1000M-1500M=2

我主要是测试在id取不同区间的值时，分片的效果。

下面来看看分片的效果
    
    
    mysql> select * from db1.travelrecord;
    +----+---------+------------+------+------+
    | id | user_id | traveldate | fee  | days |
    +----+---------+------------+------+------+
    |  1 | Victor  | 2016-01-01 |  100 |   10 |
    +----+---------+------------+------+------+
    1 row in set (0.00 sec)
    
    mysql> select * from db2.travelrecord;
    +---------+---------+------------+------+------+
    | id      | user_id | traveldate | fee  | days |
    +---------+---------+------------+------+------+
    | 5000001 | Job     | 2016-01-02 |  100 |   10 |
    +---------+---------+------------+------+------+
    1 row in set (0.00 sec)
    
    mysql> select * from db3.travelrecord;
    +----------+---------+------------+------+------+
    | id       | user_id | traveldate | fee  | days |
    +----------+---------+------------+------+------+
    | 10000001 | Slow    | 2016-01-03 |  100 |   10 |
    +----------+---------+------------+------+------+
    1 row in set (0.00 sec)

果然是分配到三个不同的节点上了。

如果想看MyCAT具体会将数据分配到哪个节点上，可通过路由分析。

语法其实蛮简单，就是SQL语句前加上explain语句。

下面根据explain命令查看create语句和insert语句具体会分配到哪些Datanode上。
    
    
    mysql> explain create table travelrecord (id bigint not null primary key,user_id varchar(100),traveldate DATE, fee decimal,days int);
    +-----------+-----------------------------------------------------------------------------------------------------------------------+
    | DATA_NODE | SQL                                                                                                                   |
    +-----------+-----------------------------------------------------------------------------------------------------------------------+
    | dn1       | create table travelrecord (id bigint not null primary key,user_id varchar(100),traveldate DATE, fee decimal,days int) |
    | dn2       | create table travelrecord (id bigint not null primary key,user_id varchar(100),traveldate DATE, fee decimal,days int) |
    | dn3       | create table travelrecord (id bigint not null primary key,user_id varchar(100),traveldate DATE, fee decimal,days int) |
    +-----------+-----------------------------------------------------------------------------------------------------------------------+
    3 rows in set (0.00 sec)
    
    mysql>  explain insert into travelrecord(id,user_id,traveldate,fee,days)  values(1,'Victor',20160101,100,10);
    +-----------+----------------------------------------------------------------------------------------------+
    | DATA_NODE | SQL                                                                                          |
    +-----------+----------------------------------------------------------------------------------------------+
    | dn1       | insert into travelrecord(id,user_id,traveldate,fee,days)  values(1,'Victor',20160101,100,10) |
    +-----------+----------------------------------------------------------------------------------------------+
    1 row in set (0.01 sec)
    
    mysql> explain insert into travelrecord(id,user_id,traveldate,fee,days)  values(5000001,'Job',20160102,100,10);
    +-----------+-------------------------------------------------------------------------------------------------+
    | DATA_NODE | SQL                                                                                             |
    +-----------+-------------------------------------------------------------------------------------------------+
    | dn2       | insert into travelrecord(id,user_id,traveldate,fee,days)  values(5000001,'Job',20160102,100,10) |
    +-----------+-------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    
    mysql> explain insert into travelrecord(id,user_id,traveldate,fee,days)  values(10000001,'Slow',20160103,100,10);
    +-----------+---------------------------------------------------------------------------------------------------+
    | DATA_NODE | SQL                                                                                               |
    +-----------+---------------------------------------------------------------------------------------------------+
    | dn3       | insert into travelrecord(id,user_id,traveldate,fee,days)  values(10000001,'Slow',20160103,100,10) |
    +-----------+---------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

**总结：**

关于MyCAT的配置其实是蛮简单的，最主要的是熟悉各配置文件的规则。以上用户名，密码，如何分库，都是在配置文件中定义的，后续，有时间再一一详表。

关于配置文件，conf目录下主要以下三个需要熟悉。

server.xml是Mycat服务器参数调整和用户授权的配置文件

schema.xml是逻辑库定义和表以及分片定义的配置文件

rule.xml是分片规则的配置文件
