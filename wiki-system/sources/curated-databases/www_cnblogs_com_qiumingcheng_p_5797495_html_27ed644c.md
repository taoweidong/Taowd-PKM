---
source: "http://www.cnblogs.com/qiumingcheng/p/5797495.html"
title: "解决在Linux下安装Oracle时的中文乱码问题 - 邱明成 - 博客园"
fetched_at: "2026-10-05 15:28:27"
---

本帖最后由 TsengYia 于 2012-2-22 17:06 编辑  
  
解决在Linux下安装Oracle时的中文乱码问题  
  
操作系统：Red Hat Enterprise Linux 6.1  
数据库：Oracle Database 11g R2  
  
方法一：逃避法，改用英文界面安装  
  
[root@dbserver ~]# su - oracle  
[oracle@dbserver ~]$ export LANG=en_US.UTF-8  
[oracle@dbserver ~]$ cd /var/ftp/pub/database/  
[oracle@dbserver ~]$ ./runInstaller  
...   
  
方法二：偷梁换柱，改用系统的中文JDK环境  
[root@localhost ~]# yum -y install java-1.6.0  
[root@localhost ~]# cd /usr/lib/jvm/jre-1.6.0/lib/  
[root@localhost lib]# mv fontconfig.bfc fontconfig.bfc.origin  
[root@localhost lib]# cp fontconfig.RedHat.6.0.bfc fontconfig.bfc  
  
[root@dbserver ~]# su - oracle  
[oracle@dbserver ~]$ export LANG=zh_CN.UTF-8  
[oracle@dbserver ~]$ cd /var/ftp/pub/database/  
[oracle@dbserver ~]$ ./runInstaller -jreLoc /usr/lib/jvm/jre-1.6.0  
---
