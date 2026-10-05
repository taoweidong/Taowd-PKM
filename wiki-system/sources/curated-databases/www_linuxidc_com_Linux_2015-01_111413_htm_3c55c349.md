---
source: "http://www.linuxidc.com/Linux/2015-01/111413.htm"
title: "CentOS 6.5下安装MySQL 5.6.21_数据库技术_Linux公社-Linux系统门户网站"
fetched_at: "2026-10-05 15:28:28"
---

你好，游客 登录 [注册](../../memberreg.aspx) [搜索](../../search.aspx)

[![Linux公社](../../pic/logo.jpg)](http://www.linuxidc.com/) |
---|---

[首页](../../index.htm)[Linux新闻](../../it/)[Linux教程](../../Linuxit/)[数据库技术](../../MySql/)[Linux编程](../../RedLinux/)[服务器应用](../../Apache/)[Linux安全](../../Unix/)[Linux下载](../../download/)[Linux认证](../../Linuxrz/)[Linux主题](../../theme/)[Linux壁纸](../../Linuxwallpaper/)[Linux软件](../../linuxsoft/)[数码](../../digi/)[手机](../../mobile/)[电脑](../../diannao/)

[首页](../../index.htm) → [数据库技术](../../MySql/)

背景：  阅读新闻

# CentOS 6.5下安装MySQL 5.6.21

| [日期：2015-01-07] | 来源：Linux社区 作者：ysztcn | [字体：[大](javascript:ContentSize\(16\)) [中](javascript:ContentSize\(0\)) [小](javascript:ContentSize\(12\))]
---|---|---

## MySQL安装

Linux中使用最广泛的数据库就是MySQL，使用在线yum的方式安装的版本落后MySQL网站好几个小版本，本节亲自测试安装新版的MySQL。

* * *

### 测试机器环境：

VMware Workstation 10 虚拟机

内存：1G

Linux版本：[CentOS](http://www.linuxidc.com/topicnews.aspx?tid=14 "CentOS") MinimalCD 6.5

JAVA：JAVA_HOME=/opt/jdk

* * *

安装mysql前需要查询系统中含有的有关mysql的软件。


    rpm -qa | grep -i mysql  //grep -i是不分大小写字符查询，只要含有mysql就显示

屏幕显示：


    mysql-libs-5.1.71-1.el6.i686  //它是好几个软件的依赖，其中在mini版本中postfix软件依赖mysql-libs，网络上很多建议都是直接删除，

    yum remove mysql-libs 或者 rpm -e --nodeps mysql-libs-5.1.71-1.el6.i686，总觉得这样做不好。


    查找mysql官方资料，得到安装方法是用MySQL-shared-compat将mysql-libs-5.1.71-1.el6.i686替换为同版本后在安装mysql。

下载mysql地址：<http://dev.mysql.com/downloads/mysql/>

[![ba9ed174-94cc-49ca-94e8-ca8770febaa9](../../upload/2015_01/150107130977752.jpg)](../../upload/2015_01/150107130977751.jpg)

CentOS是[RedHat](http://www.linuxidc.com/topicnews.aspx?tid=10 "RedHat")Linux系列的，因此选择RedHatLinux(见红线地方)，网页会自动变成RedHatLinux有关的mysql下载:

[![d6a270d5-5738-4e37-9f7f-f7466c168503](../../upload/2015_01/150107130977754.png)](../../upload/2015_01/150107130977753.png)

需要下载2个内容，一个是MySQL-5.6.21-1.el6.i686.rpm-bundle.tar，这个是几个程序的合集包，另一个是MySQL-shared-compat-5.6.21-1.el6.i686.rpm，这个是软件包包括MySQL 3.23和MySQL 4.0的共享库。如果你安装了应用程序动态连接MySQL 3.23，但是你想要升级到ySQL 4.0而不想打破库的从属关系，则安装该软件包而不要安装MySQL-shared。从MySQL 4.0.13起包含该安装软件包。

将2个文件上传到CentOS中，解压MySQL-5.6.21-1.el6.i686.rpm-bundle.tar。


    #tar xvf MySQL-5.6.21-1.el6.i686.rpm-bundle.tar

    MySQL-client-5.6.21-1.el6.i686.rpm

    MySQL-devel-5.6.21-1.el6.i686.rpm

    MySQL-shared-5.6.21-1.el6.i686.rpm

    MySQL-test-5.6.21-1.el6.i686.rpm

    MySQL-server-5.6.21-1.el6.i686.rpm

    MySQL-embedded-5.6.21-1.el6.i686.rpm

    #ls -l

    total 415068

    -rw-r--r--. 1 root root  210442240 Nov 11 11:12 MySQL-5.6.21-1.el6.i686.rpm-bundle.tar

    -rw-r--r--. 1 7155 wheel  17813608 Sep 12 16:25 MySQL-client-5.6.21-1.el6.i686.rpm

    -rw-r--r--. 1 7155 wheel   3131328 Sep 12 16:25 MySQL-devel-5.6.21-1.el6.i686.rpm

    -rw-r--r--. 1 7155 wheel  83106000 Sep 12 16:25 MySQL-embedded-5.6.21-1.el6.i686.rpm

    -rw-r--r--. 1 7155 wheel  54611632 Sep 12 16:26 MySQL-server-5.6.21-1.el6.i686.rpm

    -rw-r--r--. 1 7155 wheel   1878756 Sep 12 16:27 MySQL-shared-5.6.21-1.el6.i686.rpm

    -rw-r--r--. 1 root root    4141488 Nov 18 14:42 MySQL-shared-compat-5.6.21-1.el6.i686.rpm

    -rw-r--r--. 1 7155 wheel  49887932 Sep 12 16:27 MySQL-test-5.6.21-1.el6.i686.rpm

安装MySQL-shared-compat替换mysql-libs，如果不替换，在删除mysql-libs，会提示postfix依赖于mysql-libs：


    # rpm -i MySQL-shared-compat-5.6.21-1.el6.i686.rpm

    # rpm -qa | grep -i mysql

    mysql-libs-5.1.71-1.el6.i686

    MySQL-shared-compat-5.6.21-1.el6.i686

    # yum remove mysql-libs

测试MySQL-server安装，提示需要安装perl：


    # rpm -ivh --test MySQL-server-5.6.21-1.el6.i686.rpm

    # yum install perl

安装MySQL-server，MySQL-client：


    # rpm -ivh  MySQL-server-5.6.21-1.el6.i686.rpm

    Preparing...                ########################################### [100%]

       1:MySQL-server           ########################################### [100%]

    ………………

    ………………

    A RANDOM PASSWORD HAS BEEN SET FOR THE MySQL root USER !

    You will find that password in '/root/.mysql_secret'.

    You must change that password on your first connect,

    no other statement but 'SET PASSWORD' will be accepted.

    See the manual for the semantics of the 'password expired' flag.

    Also, the account for the anonymous user has been removed.

    In addition, you can run:

      /usr/bin/mysql_secure_installation

    ………………

    ………………

    # rpm -ivh  MySQL-client-5.6.21-1.el6.i686.rpm

    Preparing...                ########################################### [100%]

       1:MySQL-client           ########################################### [100%]

在安装MySQL-server，见上面的一段话，大意是全新安装设置的root密码在/root/.mysql_secret中，这是一个随机密码，你需要运行/usr/bin/mysql_secure_installation，删除anonymous用户。当然不建议用root用户来运行，rpm包已经建了一个mysql用户，可以使用这个用户：


    #more .mysql_secret

    # The random password set for the root user at Tue Nov 18 22:57:46 2014 (local t

    ime): NljqL63OYlGo5cqy    <– 得到root访问mysql的密码：NljqL63OYlGo5cqy

    # service mysql start

    Starting MySQL... SUCCESS!

    # /usr/bin/mysql_secure_installation --user=mysql

    NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MySQL

          SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!



    In order to log into MySQL to secure it, we'll need the current

    password for the root user.  If you've just installed MySQL, and

    you haven't set the root password yet, the password will be blank,

    so you should just press enter here.



    Enter current password for root (enter for none):    <–使用刚才得到的root的密码 NljqL63OYlGo5cqy

    OK, successfully used password, moving on...



    Setting the root password ensures that nobody can log into the MySQL

    root user without the proper authorisation.



    You already have a root password set, so you can safely answer 'n'.



    Change the root password? [Y/n] y   <– 是否更换root用户密码，输入y并回车，强烈建议更换

    New password:      <– 设置root用户的密码

    Re-enter new password:    <– 再输入一次你设置的密码

    Password updated successfully!

    Reloading privilege tables..

     ... Success!





    By default, a MySQL installation has an anonymous user, allowing anyone

    to log into MySQL without having to have a user account created for

    them.  This is intended only for testing, and to make the installation

    go a bit smoother.  You should remove them before moving into a

    production environment.



    Remove anonymous users? [Y/n] y   <– 是否删除匿名用户,生产环境建议删除，所以输入y并回车

     ... Success!



    Normally, root should only be allowed to connect from 'localhost'.  This

    ensures that someone cannot guess at the root password from the network.



    Disallow root login remotely? [Y/n] y    <–是否禁止root远程登录,根据自己的需求选择Y/n并回车,建议禁止

     ... Success!



    By default, MySQL comes with a database named 'test' that anyone can

    access.  This is also intended only for testing, and should be removed

    before moving into a production environment.



    Remove test database and access to it? [Y/n] y    <– 是否删除test数据库,输入y并回车

     - Dropping test database...

     ... Success!

     - Removing privileges on test database...

     ... Success!



    Reloading the privilege tables will ensure that all changes made so far

    will take effect immediately.



    Reload privilege tables now? [Y/n] y   是否重新加载权限表，输入y并回车

     ... Success!









    All done!  If you've completed all of the above steps, your MySQL

    installation should now be secure.



    Thanks for using MySQL!





    Cleaning up...

至此，MySQL已经安装完成，最后看一下是否已将MySQL加到开机服务里：


    #  chkconfig

    auditd          0:off   1:off   2:on    3:on    4:on    5:on    6:off

    blk-availability        0:off   1:on    2:on    3:on    4:on    5:on    6:off

    crond           0:off   1:off   2:on    3:on    4:on    5:on    6:off

    ip6tables       0:off   1:off   2:on    3:on    4:on    5:on    6:off

    iptables        0:off   1:off   2:on    3:on    4:on    5:on    6:off

    iscsi           0:off   1:off   2:off   3:on    4:on    5:on    6:off

    iscsid          0:off   1:off   2:off   3:on    4:on    5:on    6:off

    lvm2-monitor    0:off   1:on    2:on    3:on    4:on    5:on    6:off

    mdmonitor       0:off   1:off   2:on    3:on    4:on    5:on    6:off

    multipathd      0:off   1:off   2:off   3:off   4:off   5:off   6:off

    mysql           0:off   1:off   2:on    3:on    4:on    5:on    6:off   <-看到这个OK了

    netconsole      0:off   1:off   2:off   3:off   4:off   5:off   6:off

    netfs           0:off   1:off   2:off   3:on    4:on    5:on    6:off

    network         0:off   1:off   2:on    3:on    4:on    5:on    6:off

    postfix         0:off   1:off   2:on    3:on    4:on    5:on    6:off

    rdisc           0:off   1:off   2:off   3:off   4:off   5:off   6:off

    restorecond     0:off   1:off   2:off   3:off   4:off   5:off   6:off

    rsyslog         0:off   1:off   2:on    3:on    4:on    5:on    6:off

    saslauthd       0:off   1:off   2:off   3:off   4:off   5:off   6:off

    sshd            0:off   1:off   2:on    3:on    4:on    5:on    6:off

    udev-post       0:off   1:on    2:on    3:on    4:on    5:on    6:off

MySQL安装后涉及的目录如下：

目录 | 目录中的内容
---|---
/usr/bin | 客户端程序和脚本
/usr/sbin | **Mysqld** 服务器
/var/lib/mysql | 数据库的日志文件
/usr/share/info | 信息格式手册
/usr/share/man | Unix 手册页
/usr/include/mysql | 包括 （标题） 的文件
/usr/lib/mysql | mysql的lib包
/usr/share/mysql | 杂项的支持文件，包括错误消息） 字符设置的文件，示例配置文件，SQL 数据库安装
/usr/share/sql-bench | 基准

现在好了，可以测试你的MySQL了。

\--------------------------------------分割线 --------------------------------------

[Ubuntu](http://www.linuxidc.com/topicnews.aspx?tid=2 "Ubuntu") 14.04下安装MySQL [http://www.linuxidc.com/Linux/2014-05/102366.htm](../../Linux/2014-05/102366.htm)

《MySQL权威指南(原书第2版)》清晰中文扫描版 PDF [http://www.linuxidc.com/Linux/2014-03/98821.htm](../../Linux/2014-03/98821.htm)

Ubuntu 14.04 LTS 安装 LNMP Nginx\PHP5 (PHP-FPM)\MySQL [http://www.linuxidc.com/Linux/2014-05/102351.htm](../../Linux/2014-05/102351.htm)

Ubuntu 14.04下搭建MySQL主从服务器 [http://www.linuxidc.com/Linux/2014-05/101599.htm](../../Linux/2014-05/101599.htm)

Ubuntu 12.04 LTS 构建高可用分布式 MySQL 集群 [http://www.linuxidc.com/Linux/2013-11/93019.htm](../../Linux/2013-11/93019.htm)

Ubuntu 12.04下源代码安装MySQL5.6以及Python-MySQLdb [http://www.linuxidc.com/Linux/2013-08/89270.htm](../../Linux/2013-08/89270.htm)

MySQL-5.5.38通用二进制安装 [http://www.linuxidc.com/Linux/2014-07/104509.htm](../../Linux/2014-07/104509.htm)

\--------------------------------------分割线 --------------------------------------

**本文永久更新链接地址** ：[http://www.linuxidc.com/Linux/2015-01/111413.htm](../../Linux/2015-01/111413.htm)

[![linux](/linuxfile/logo.gif)](http://www.linuxidc.com)

[通过Gearman实现MySQL到Redis的数据同步](../../Linux/2015-01/111380.htm)

[10款最好用的MySQL数据库客户端图形界面管理工具](../../Linux/2015-01/111421.htm)

相关资讯 [CentOS下安装MySQL](../../search.aspx?where=nkey&keyword=19398) [MySQL 5.6.21安装](../../search.aspx?where=nkey&keyword=33302)

  * [CentOS下MySQL安装与主从同步配置](../../Linux/2017-11/148524.htm "CentOS下MySQL安装与主从同步配置详解") (今 19:55)
  * [CentOS下MySQL数据库的安装](../../Linux/2014-12/111019.htm) (12/30/2014 14:23:49)

|

  * [CentOS下MySQL安装配置](../../Linux/2015-07/120234.htm) (07/21/2015 10:59:38)
  * [CentOS 6.2上使用YUM安装MySQL](../../Linux/2013-03/80326.htm) (03/04/2013 09:53:44)


---|---

本文评论 [查看全部评论](../../remark.aspx?id=111413) (0)

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

  * [CentOS下MySQL安装与主从同步配置详解](../../Linux/2017-11/148524.htm)
  * [CentOS 7.3.1611下 rpm方式安装MySQL 5.7.](../../Linux/2017-11/148523.htm "CentOS 7.3.1611下 rpm方式安装MySQL 5.7.18 教程")
  * [CentOS 7.3 安装MySQL 5.7并修改初始密码](../../Linux/2017-11/148522.htm)
  * [Windows安装MySQL 5.7并修改初始密码](../../Linux/2017-11/148521.htm)
  * [MySQL 5.7.18 数据库主从（Master/Slave）](../../Linux/2017-11/148520.htm "MySQL 5.7.18 数据库主从（Master/Slave）同步安装与配置详解")
  * [CentOS 通过 Nginx 和 vsftpd 构建图片服务](../../Linux/2017-11/148519.htm "CentOS 通过 Nginx 和 vsftpd 构建图片服务器")
  * [基于 CentOS 搭建 FTP 文件服务](../../Linux/2017-11/148518.htm)
  * [CentS 7.3 搭建 Redis-4.0.1 Cluster 集群](../../Linux/2017-11/148517.htm "CentS 7.3 搭建 Redis-4.0.1 Cluster 集群服务")
  * [CentOS 7.3 搭建 Redis-4.0.1 单机服务](../../Linux/2017-11/148516.htm)
  * [MySQL导入数据提示ERROR 1418 (HY000)](../../Linux/2017-11/148515.htm)



[Linux公社简介](http://www.linuxidc.com/aboutus.htm) \- [广告服务](http://www.linuxidc.com/adsense.htm) \- [网站地图](http://www.linuxidc.com/sitemap.aspx) \- [帮助信息](http://www.linuxidc.com/help.htm) \- [联系我们](http://www.linuxidc.com/contactus.htm)
本站（LinuxIDC）所刊载文章不代表同意其说法或描述，仅为提供更多信息，也不构成任何建议。


Copyright © 2006-2017 [Linux公社](http://www.linuxidc.com/) All rights reserved 沪ICP备15008072号-1号
