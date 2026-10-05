---
source: "http://blog.csdn.net/snowfox326043/article/details/7463271"
title: "AIX 6.1安装 Oracle11g_aix部署oracle 11g-CSDN博客"
fetched_at: "2026-10-05 15:26:59"
---

## 

##   


##   


## 作者 阿九【转载时请务必以超链接形式标明文章原始出处和作者信息】 

  


##   


## 目录

目 录... 1

一、系统准备... 3

1.1、操作系统版本需求... 3

1.2、内存需求... 3

1.3、SWAP空间需求... 3

1.4、确认操作系统位数... 4

1.5、软件包需求... 4

1.6、系统补丁需求... 6

1.7、创建用户组和用户... 7

1.8、增加grid和oracle用户shell能力... 7

1.9、系统参数配置... 8

1.9.1、配置进程数... 8

1.9.2、配置grid用户和oracle用户Shell权限... 8

1.9.3、查看异步aio数... 9

1.9.4、配置网络参数... 9

1.9.5、配置主机虚拟内存... 10

1.9.6、增加操作系统块分配大小... 10

1.9.7、增加操作系统最大进程数... 10

1.10、配置Oracle和grid用户环境变量... 10

1.11、创建Oracle目录结构... 11

1.12、为ASM配置存储... 11

二、安装GridInfrastructure. 12

2.1、启动安装界面... 12

2.2、选择语言包... 13

2.3、为ASM存储指定磁盘... 15

2.4、为ASM磁盘设置密码... 15

2.5、指定操作系统用户组... 17

2.6、指定grid用户的ORACLE_BASE目录... 19

2.7、效验操作系统... 20

2.8、安装情况概况... 22

2.9、开始安装... 23

2.10、执行root脚本... 24

2.11、完成安装... 27

三、数据库软件安装... 28

3.1、启动安装界面... 28

3.2、更新方式询问... 30

3.3、选择安装的类型... 31

3.4、选择安装的类型... 32

3.5、选择安装的语言... 33

3.6、选择数据库要安装的版本... 34

3.7、指定软件安装的目录... 36

3.8、指定软件产品清单目录（保持默认）... 37

3.9、指定操作系统用户组（保持默认）... 38

3.10、产品预安装检查... 39

3.11、安装信息概况，点击Finish. 41

3.12、开始安装... 42

3.13、执行完成脚本... 42

四、配置监听程序... 44

4.1、启动配置界面... 44

4.2、选择操作类型... 45

4.3、指定监听名称... 45

4.4、选择网络协议（保持默认）... 46

4.5、选择监听端口号... 46

4.6、完成配置... 47

五、安装数据库... 48

5.1、启动安装界面... 48

5.2、选择操作类型... 49

5.3、选择数据库类型... 50

5.4、指定数据库名... 50

5.5、是否配置Enterprise Manager. 51

5.6、指定数据库SYS用户密码... 51

5.7、选择数据库文件的存储类型... 53

5.8、指定存储地址... 54

5.9、指定闪回区及归档模式... 55

5.10、指定数据库安装组件... 55

5.11、指定数据库内存分配... 56

5.12、指定数据库Processes大小... 56

5.13、指定数据库字符集... 57

5.14、指定数据库连接模式... 58

5.15、指定最大数据文件个数... 59

5.16、配置概况... 60

5.17、开始安装... 61

5.18、完成安装... 62

## 一、系统准备

### 1.1、操作系统版本需求

执行命令**oslevel –s** 来查看

# oslevel –s

6.1.0.0

### 1.2、内存需求

执行命令lsattr -E -l sys0 -a realmem 显示内存大小

# lsattr -E -l sys0 -a realmem

realmem 65273856 Amount of usable physical memory in Kbytes False

### 1.3、SWAP空间需求

执行命令**lsps –a** 查看SWAP空间大小

#lsps -a

PageSpace Physical Volume Volume Group Size %Used Active Auto Type Chksum

hd6 hdisk0 rootvg 16384MB 2 yes yes lv 0

### 1.4、确认操作系统位数

执行**getconfHARDWARE_BITMODE** 命令查看

# getconf HARDWARE_BITMODE

64

### 1.5、软件包需求

AIX 61系统需要如下软件包

bos.adt.base  
bos.adt.lib  
bos.adt.libm  
bos.perf.libperfstat 6.1.2.1 or later  
bos.perf.perfstat  
bos.perf.proctools  
xlC.aix61.rte:10.1.0.0 or later

执行命令 lslpp -l bos.adt.base bos.adt.lib bos.adt.libm bos.perf.libperfstatbos.perf.perfstat bos.perf.proctools xlC.aix61.rte 查看软件包安装情况

# lslpp -l bos.adt.base bos.adt.lib bos.adt.libm bos.perf.libperfstatbos.perf.perfstat bos.perf.proctools xlC.aix61.rte

Fileset Level State Description 

\----------------------------------------------------------------------------

Path: /usr/lib/objrepos

bos.adt.base 6.1.6.1 COMMITTED Base Application Development

Toolkit 

bos.adt.lib 6.1.2.0 COMMITTED Base Application Development

Libraries 

bos.adt.libm 6.1.6.0 COMMITTED Base Application Development

Math Library 

bos.perf.libperfstat 6.1.6.1 COMMITTED Performance StatisticsLibrary

Interface 

bos.perf.perfstat 6.1.6.0 COMMITTED Performance Statistics

Interface 

bos.perf.proctools 6.1.6.0 COMMITTED Proc Filesystem Tools 

xlC.aix61.rte 11.1.0.1 COMMITTED XL C/C++ Runtime forAIX 6.1 

Path: /etc/objrepos

bos.adt.base 6.1.6.1 COMMITTED Base Application Development

Toolkit 

bos.perf.libperfstat 6.1.6.1 COMMITTED Performance StatisticsLibrary

Interface 

bos.perf.perfstat 6.1.6.0 COMMITTED Performance Statistics

Interface

### 1.6、系统补丁需求

11gR2需要以下补丁，执行命令 instfix -i查询

instfix -i | grep IZ41855

instfix -i | grep IZ51456

instfix -i | grep IZ52319

### 1.7、创建用户组和用户

使用如下命令创建：

mkgroup -'A' id='401' adms='root' oinstall

mkgroup -'A' id='402' adms='root' dba 

useradd -d /home/oracle -m -u 401 -g oinstall -G dba oracle

useradd -d /home/grid -m -u 402 -g oinstall -G dba grid

# passwd oracle

Changing password for "oracle"

oracle's New password: 

Enter the new password again:

# passwd grid

Changing password for "grid"

grid's New password: 

Enter the new password again:

### 1.8、增加grid和oracle用户shell能力

查看grid和oracle用户shell能力

/usr/bin/lsuser -a capabilitiesgrid

/usr/bin/lsuser -a capabilities oracle

增加grid用户shell能力

/usr/bin/chusercapabilities=CAP_NUMA_ATTACH,CAP_BYPASS_RAC_VMM,CAP_PROPAGATE grid

增加oracle用户shell能力

/usr/bin/chusercapabilities=CAP_NUMA_ATTACH,CAP_BYPASS_RAC_VMM,CAP_PROPAGATE oracle

### 1.9、系统参数配置

#### 1.9.1、配置进程数

执行命令**smitty chgsys** 修改，将PROCESSES修改为16384

#### 1.9.2、配置grid用户和oracle用户Shell权限

修改**/etc/security/limits** 文件****

default:

fsize = -1

core = 2097151

cpu = -1

data = -1

rss = -1

stack = -1

nofiles = -1

#### 1.9.3、查看异步aio数

执行命令**ioo -oaio_maxreqs**

#### 1.9.4、配置网络参数

查看参数 

# /usr/sbin/no -a | fgrepephemeral

tcp_ephemeral_high = 65535

tcp_ephemeral_low = 32768

udp_ephemeral_high = 65535

udp_ephemeral_low = 32768

配置参数

**# /usr/sbin/no -p -otcp_ephemeral_low=9000 -o tcp_ephemeral_high=65500**

Settingtcp_ephemeral_low to 9000

Settingtcp_ephemeral_low to 9000 in nextboot file

Settingtcp_ephemeral_high to 65500

Settingtcp_ephemeral_high to 65500 in nextboot file

**# /usr/sbin/no -p -oudp_ephemeral_low=9000 -o udp_ephemeral_high=65500**

Settingudp_ephemeral_low to 9000

Settingudp_ephemeral_low to 9000 in nextboot file

Settingudp_ephemeral_high to 65500

Settingudp_ephemeral_high to 65500 in nextboot file

#### 1.9.5、配置主机虚拟内存

vmo -p -o minperm%=3

vmo -p -o maxperm%=90

vmo -p -o maxclient%=90

vmo -p -o lru_file_repage=0

vmo -p -o strict_maxclient=1

vmo -p -o strict_maxperm=0

#### 1.9.6、增加操作系统块分配大小

/usr/sbin/chdev -l sys0 -a ncargs='128'

如果报错

Method error(/usr/lib/methods/chggen):

0514-018 The values specified for thefollowing attributes

are not valid:

ncargs ARG/ENV list size in 4Kbyte blocks

则使用命令 smit chgsys 查看ARG/ENV列的数值。

#### 1.9.7、增加操作系统最大进程数

使用命令 smit chgsys，将“Maximum number of PROCESSES allowed per user”列修改为16384

### 1.10、配置Oracle和grid用户环境变量

Oracle用户

umask 022

export ORACLE_BASE=/oracle/db

export ORACLE_HOME=$ORACLE_BASE/ora11g

export ORACLE_SID=hlky

PATH=$ORACLE_HOME/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:$HOME/bin:/usr/bin/X11:/sbin:.

grid用户

umask 022

export ORACLE_BASE=/oracle/grid

export ORACLE_HOME=$ORACLE_BASE/asm

export ORACLE_SID=+ASM

PATH=$ORACLE_HOME/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:$HOME/bin:/usr/bin/X11:/sbin:.

export PATH

### 1.11、创建Oracle目录结构

Root用户登录执行：

# mkdir /oracle

# mkdir /oracle/db

# mkdir /oracle/grid

# mkdir /oraInventory

# chown -R grid:dba /oracle

# chown -R oracle:dba /oraInventory

# chown -R oracle:dba /oracle/db

# chown -R grid:dba /oracle/grid

# chmod -R 775 /oracle/

### 1.12、为ASM配置存储

# lspv

hdisk0 00f69cfd61b1206e rootvg active

hdisk1 00f69cfd62b72e86 testvg active

hdisk2 00f69cfd62b81c04 testvg active

hdisk3 00f69cfd62b90c28 testvg active

hdisk4 00f69cfd62b9fa83 testvg active

hdisk5 none None 

hdisk6 none None 

hdisk7 none None 

hdisk8 none None 

#

#chown grid:dba /dev/rhdisk1

#chown grid:dba /dev/rhdisk2

#chown grid:dba /dev/rhdisk3

#chown grid:dba /dev/rhdisk4

#chdev -l hdisk1 -a pv=yes

#chdev -l hdisk2 -a pv=yes

#chdev -l hdisk3 -a pv=yes

#chdev -l hdisk4 -a pv=yes

# chmod 660 /dev/rhdisk1

# chmod 660 /dev/rhdisk2

# chmod 660 /dev/rhdisk3

# chmod 660 /dev/rhdisk4

## 二、安装Grid Infrastructure

注：先以root用户登录执行rootpre.sh脚本

### 2.1、启动安装界面

以Grid用户登录系统，执行命令 /cdrom0/runInstaller

### 2.2、选择语言包

添加简体中文语言包

### 2.3、为ASM存储指定磁盘

### 2.4、为ASM磁盘设置密码

密码为：oracle

这里会提示因设置的密码（oracle）不安全，点击YES跳过

### 2.5、指定操作系统用户组

这里需要确认几个操作系统用户组为同一用户组

### 2.6、指定grid用户的ORACLE_BASE目录

### 2.7、效验操作系统

这里提示缺少操作系统补丁包，选择忽略

### 2.8、安装情况概况

### 2.9、开始安装

### 2.10、执行root脚本

以root用户登录系统，执行命令

（注意：root执行命令的当前目录不能在CDROM的挂着目录）

#/grid/product/11.2.0/grid/root.sh

RunningOracle 11g root.sh script...

Thefollowing environment variables are set as:

ORACLE_OWNER= grid

ORACLE_HOME= /grid/product/11.2.0/grid

Enterthe full pathname of the local bin directory: [/usr/local/bin]: 

Thefile "dbhome" already exists in /usr/local/bin. Overwrite it? (y/n) [n]: 

Thefile "oraenv" already exists in /usr/local/bin. Overwrite it? (y/n) [n]: 

Thefile "coraenv" already exists in /usr/local/bin. Overwrite it? (y/n) [n]: 

Entrieswill be added to the /etc/oratab file as needed by

DatabaseConfiguration Assistant when a database is created

Finishedrunning generic part of root.sh script.

Nowproduct-specific root actions will be performed.

2011-09-2222:14:37: Checking for super user privileges

2011-09-2222:14:37: User has super user privileges

2011-09-2222:14:37: Parsing the host name

Usingconfiguration parameter file: /grid/product/11.2.0/grid/crs/install/crsconfig_params

Creatingtrace directory

.profile[2]:/grid: This is not an identifier.

LOCALADD MODE 

CreatingOCR keys for user 'grid', privgrp 'oinstall'..

Operationsuccessful.

CRS-4664:Node p750 successfully pinned.

Addingdaemon to inittab

CRS-4123:Oracle High Availability Services has been started.

ohasdis starting

p750 2011/09/22 22:15:05 /grid/product/11.2.0/grid/cdata/p750/backup_20110922_221505.olr

Successfullyconfigured Oracle Grid Infrastructure for a Standalone Server

Updatinginventory properties for clusterware

StartingOracle Universal Installer...

Checkingswap space: must be greater than 500 MB. Actual 16384 MB Passed

Theinventory pointer is located at /etc/oraInst.loc

Theinventory is located at /oraInventory

'UpdateNodeList'was successful.

### 2.11、完成安装

## 三、数据库软件安装

注：在安装之前，需重建/etc/oraInst.loc中的地址

### 3.1、启动安装界面

以Oracle用户登录系统，执行命令 /cdrom0/runInstaller

$ /cdrom0/runInstaller

********************************************************************************

Your platform requires the root user to perform certain pre-installation

OS preparation. The root user shouldrun the shell script 'rootpre.sh' before

you proceed with Oracle installation. rootpre.sh can be found at the top level

of the CD or the stage area.

Answer 'y' if root has run 'rootpre.sh' so you can proceed with Oracle 

installation.

Answer 'n' to abort installation and then ask root to run 'rootpre.sh'.

********************************************************************************

Has 'rootpre.sh' been run by root? [y/n] (n)

y

Starting Oracle Universal Installer...

Checking Temp space: must be greater than 190 MB. Actual 5072 MB Passed

Checking swap space: must be greater than 150 MB. Actual 16384 MB Passed

Checking monitor: must be configured to display at least 256 colors. Actual 16777216 Passed

Preparing to launch Oracle Universal Installer from/tmp/OraInstall2011-09-22_05-32-00PM. Please wait ...$

### 3.2、更新方式询问

询问是否不填写E-MAIL地址，点击YES

### 3.3、选择安装的类型

选择安装的同时是否安装数据库，选择第二项：仅安装数据库软件

### 3.4、选择安装的类型

选择第一项：单实例数据库安装

### 3.5、选择安装的语言

选择英语和简体中文

### 3.6、选择数据库要安装的版本

选择第一项企业版

### 3.7、指定软件安装的目录

### 3.8、指定软件产品清单目录（保持默认）

### 3.9、指定操作系统用户组（保持默认）

### 3.10、产品预安装检查

同样提示缺少操作系统补丁包，选择忽略

### 3.11、安装信息概况，点击Finish

### 3.12、开始安装

### 3.13、执行完成脚本

以root用户登录执行

## 四、配置监听程序

### 4.1、启动配置界面

以oracle用户登录，执行命令netca

### 4.2、选择操作类型

### 4.3、指定监听名称

### 4.4、选择网络协议（保持默认）

### 4.5、选择监听端口号

### 4.6、完成配置

单击Finish完成配置

## 五、安装数据库

### 5.1、启动安装界面

以oracle用户登录系统，执行dbca命令

### 5.2、选择操作类型

### 5.3、选择数据库类型

### 5.4、指定数据库名

### 5.5、是否配置EnterpriseManager

### 5.6、指定数据库SYS用户密码

密码为：oracle

这里提示密码不安全，选择YES忽略

### 5.7、选择数据库文件的存储类型

### 5.8、指定存储地址

### 5.9、指定闪回区及归档模式

### 5.10、指定数据库安装组件

### 5.11、指定数据库内存分配

### 5.12、指定数据库Processes大小

### 5.13、指定数据库字符集

### 5.14、指定数据库连接模式

### 5.15、指定最大数据文件个数

### 5.16、配置概况

### 5.17、开始安装

### 5.18、完成安装
