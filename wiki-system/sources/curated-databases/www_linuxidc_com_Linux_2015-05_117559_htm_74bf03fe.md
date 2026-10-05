---
source: "http://www.linuxidc.com/Linux/2015-05/117559.htm"
title: "Linux平台Oracle 11g单实例 安装部署配置 快速参考_数据库技术_Linux公社-Linux系统门户网站"
fetched_at: "2026-10-05 15:27:44"
---

你好，游客 登录 [注册](../../memberreg.aspx) [搜索](../../search.aspx)

[![Linux公社](../../pic/logo.jpg)](http://www.linuxidc.com/) |   
---|---  
  
[首页](../../index.htm)[Linux新闻](../../it/)[Linux教程](../../Linuxit/)[数据库技术](../../MySql/)[Linux编程](../../RedLinux/)[服务器应用](../../Apache/)[Linux安全](../../Unix/)[Linux下载](../../download/)[Linux认证](../../Linuxrz/)[Linux主题](../../theme/)[Linux壁纸](../../Linuxwallpaper/)[Linux软件](../../linuxsoft/)[数码](../../digi/)[手机](../../mobile/)[电脑](../../diannao/)

[首页](../../index.htm) → [数据库技术](../../MySql/)

背景：  阅读新闻

# Linux平台Oracle 11g单实例 安装部署配置 快速参考

| [日期：2015-05-15] | 来源：Linux社区 作者：AlfredZhao | [字体：[大](javascript:ContentSize\(16\)) [中](javascript:ContentSize\(0\)) [小](javascript:ContentSize\(12\))]   
---|---|---  
  
1.重建主机的[Oracle](http://www.linuxidc.com/topicnews.aspx?tid=12 "Oracle")用户 组 统一规范 uid gid 以保证共享存储挂接或其他需求的权限规范

userdel -r oracle  
groupadd -g 500 oinstall  
groupadd -g 501 dba  
useradd -g oinstall -G dba -u 500 oracle

#id oracle  
uid=500(oracle) gid=500(oinstall) 组=500(oinstall),501(dba)

2.安装好Oracle 需要的rpm包。安装rpm依赖包

rpm -q binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc- gcc-c++ libaio-devel libaio libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel pdksh ksh

yum install binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc- gcc-c++ libaio-devel libaio libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel pdksh ksh

注：pdksh没有安装，可以忽略。安装了ksh。

yum本地源配置参考：

**更多 YUM相关教程见以下内容**：

[RedHat](http://www.linuxidc.com/topicnews.aspx?tid=10 "RedHat") 6.2 Linux修改yum源免费使用[CentOS](http://www.linuxidc.com/topicnews.aspx?tid=14 "CentOS")源 [http://www.linuxidc.com/Linux/2013-07/87383.htm](../../Linux/2013-07/87383.htm)

配置EPEL YUM源 [http://www.linuxidc.com/Linux/2012-10/71850.htm](../../Linux/2012-10/71850.htm)

Redhat 本地yum源配置 [http://www.linuxidc.com/Linux/2012-11/75127.htm](../../Linux/2012-11/75127.htm)

yum的配置文件说明 [http://www.linuxidc.com/Linux/2013-04/83298.htm](../../Linux/2013-04/83298.htm)

RedHat 6.1下安装yum(图文) [http://www.linuxidc.com/Linux/2013-06/86535.htm](../../Linux/2013-06/86535.htm)

YUM 安装及清理 [http://www.linuxidc.com/Linux/2013-07/87163.htm](../../Linux/2013-07/87163.htm)

CentOS 6.4上搭建yum本地源 [http://www.linuxidc.com/Linux/2014-07/104533.htm](../../Linux/2014-07/104533.htm)

3.修改配置文件 /etc/security/limits.conf

oracle soft nproc 2047  
oracle hard nproc 16384  
oracle soft nofile 1024  
oracle hard nofile 65536  
oracle soft stack 10240

4.修改配置文件 /etc/sysctl.conf

fs.aio-max-nr = 1048576  
fs.file-max = 6815744  
kernel.shmall = 2097152  
kernel.shmmax = XXXXXXXXXX //共享内存字节数(一般75%物理内存)  
kernel.shmmni = 4096  
kernel.sem = 250 32000 100 128  
net.ipv4.ip_local_port_range = 9000 65500  
net.core.rmem_default = 262144  
net.core.rmem_max = 4194304  
net.core.wmem_default = 262144  
net.core.wmem_max = 1048586

注：重启主机或者输入命令 sysctl -p 生效当前配置

5.Oracle用户环境变量配置

export ORACLE_BASE=/u01/app/oracle  
export ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1  
export ORACLE_SID=jingyu  
export NLS_LANG="american_america.ZHS16GBK"  
export NLS_DATE_FORMAT="YYYY-MM-DD HH24:Mi:SS"  
export LD_LIBRARY_PATH=$ORACLE_HOME/lib  
export PATH=$ORACLE_HOME/bin:$PATH

6.解压oracle软件安装包

# unzip p10404530_112030_Linux-x86-64_1of7.zip; unzip p10404530_112030_Linux-x86-64_2of7.zip  
# chown -R oracle:oinstall database

7.xmanager 安装数据库软件，dbca建库，netca创建监听

如果没有图形可采用静默模式安装~ 配置response配置文件即可。

8.根据实际需要调整数据库内存

9.调整数据库参数

打开数据库归档，规划归档路径，确定db_recovery_file_dest_size大小

\--调整processes和open_cursors  
alter system set processes = 1500 scope=spfile;  
alter system set open_cursors = 1000;

system/sysaux表空间大小；

undo表空间大小 ；

temp表空间大小；

10.迁移win平台src用户的数据

创建表空间，用户，赋权

创建dblink

SQL> create public database link jingyu connect to src identified by src using 'src_db';

$impdp src/src network_link=jingyu schemas=src remap_tablespace=USERS:DBS_D_JINGYU parallel=2 logfile=src_jingyu.log

LONG 类型的 dblink 迁移报错信息：

ORA-31679: Table data object "SRC"."SRC_WF_FLOW" has long columns, and longs can not be loaded/unloaded using a network link

这种情况采用exp导出， imp导入 这些数据行即可。

11.rman备份策略制定

rman备份策略：手工做一个数据库的全备份，定时每周日凌晨3点 0级备份 每周三凌晨3点 1级备份 每天凌晨4点备份归档 备份窗口为7天。

为提高1级备份效率，打开block_change_tracking

SQL> alter database enable block change tracking using file '/u01/app/oracle/oradata/jingyu/block_change_tracking.dbf';  
SQL> select status from v$block_change_tracking;  
\--确定STATUS状态为ENABLED

更多Oracle相关信息见[Oracle](../../topicnews.aspx?tid=12) 专题页面 [http://www.linuxidc.com/topicnews.aspx?tid=12](../../topicnews.aspx?tid=12 "Oracle")

**本文永久更新链接地址** ：[http://www.linuxidc.com/Linux/2015-05/117559.htm](../../Linux/2015-05/117559.htm)

[![linux](/linuxfile/logo.gif)](http://www.linuxidc.com)

[Linux同平台Oracle数据库整体物理迁移](../../Linux/2015-05/117558.htm)

[DG环境数据库RMAN备份策略制定](../../Linux/2015-05/117561.htm)

相关资讯 [Oracle 11g单实例](../../search.aspx?where=nkey&keyword=27039)

  * [Linux上Oracle 11g单实例安装详解](../../Linux/2017-06/144630.htm) (今 05:14)
  * [Oracle 11g单实例GI and DB升级](../../Linux/2014-02/96512.htm) (02/12/2014 14:31:38)

| 

  * [Linux平台Oracle 11g单实例 + ASM](../../Linux/2015-04/115721.htm "Linux平台Oracle 11g单实例 + ASM存储 安装部署 快速参考") (04/03/2015 08:07:20)

  
---|---  
  
本文评论 [查看全部评论](../../remark.aspx?id=117559) (0)

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

  * [Linux上Oracle 11g单实例安装详解](../../Linux/2017-06/144630.htm)
  * [你为什么使用 Linux 和开源软件？](../../Linux/2017-06/144629.htm)
  * [Adwaita Tweaks 一款简洁细腻的 GNOME ](../../Linux/2017-06/144628.htm "Adwaita Tweaks 一款简洁细腻的 GNOME Adwaita 主题")
  * [iOS 11 将允许用户限制应用的位置跟踪](../../Linux/2017-06/144627.htm)
  * [Canonical Kernel Livepatch服务支持扩展到](../../Linux/2017-06/144626.htm "Canonical Kernel Livepatch服务支持扩展到Ubuntu 14.04 LTS")
  * [Google 列出停止支持各款 Pixel 和 Nexus ](../../Linux/2017-06/144625.htm "Google 列出停止支持各款 Pixel 和 Nexus 设备的具体时间表")
  * [苹果：打赏算内购，要抽成 30%](../../Linux/2017-06/144624.htm)
  * [FreeFileSync：在 Ubuntu 中对比及同步文件](../../Linux/2017-06/144623.htm)
  * [Linux 系统中修复 SambaCry 漏洞（CVE-2017](../../Linux/2017-06/144622.htm "Linux 系统中修复 SambaCry 漏洞（CVE-2017-7494）")
  * [更快的机器学习即将来到 Linux 内核](../../Linux/2017-06/144621.htm)

  
  
[Linux公社简介](http://www.linuxidc.com/aboutus.htm) \- [广告服务](http://www.linuxidc.com/adsense.htm) \- [网站地图](http://www.linuxidc.com/sitemap.aspx) \- [帮助信息](http://www.linuxidc.com/help.htm) \- [联系我们](http://www.linuxidc.com/contactus.htm)  
本站（LinuxIDC）所刊载文章不代表同意其说法或描述，仅为提供更多信息，也不构成任何建议。  
  
  
Copyright © 2006-2016 [Linux公社](http://www.linuxidc.com/) All rights reserved 沪ICP备15008072号-1号 
