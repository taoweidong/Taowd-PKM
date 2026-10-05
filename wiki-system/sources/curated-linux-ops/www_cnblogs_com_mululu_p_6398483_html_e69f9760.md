---
source: "http://www.cnblogs.com/mululu/p/6398483.html"
title: "Nmon的安装及使用 - 西瓜汁拌面 - 博客园"
fetched_at: "2026-10-05 15:34:51"
---

一、下载Nmon

根据CPU的类型选择下载相应的版本：

<http://nmon.sourceforge.net/pmwiki.php?n=Site.Download>
wget [http://sourceforge.net/projects/nmon/files/download/nmon_x86_12a.zip](http://sourceforge.net/projects/nmon/files/download/nmon_x86_12a.zip/download)

二、初始化工具


    [root@mululu ~]# cd /opt
    [root@mululu opt]# mkdir nmon
    [root@mululu opt]# cd nmon
    [root@mululu nmon]#wget [http://sourceforge.net/projects/nmon/files/download/nmon_x86_12a.zip](http://sourceforge.net/projects/nmon/files/download/nmon_x86_12a.zip/download)


    [root@mululu nmon]# unzip nmon_x86_12a.zip
    Archive:  nmon_x86_12a.zip
      inflating: nmon_x86_rhel45
      inflating: nmon_x86_rhel52
      inflating: nmon_x86_sles9
      inflating: nmon_x86_sles10
      inflating: nmon_x86_ubuntu810
      inflating: nmon_x86_fedora10
      inflating: nmon_x86_opensuse10
    [root@mululu nmon]# ls
    nmon1             nmon_x86_fedora10    nmon_x86_rhel45  nmon_x86_sles10  nmon_x86_ubuntu810
    nmon_x86_12a.zip  nmon_x86_opensuse10  nmon_x86_rhel52  nmon_x86_sles9
    [root@mululu nmon]# mv nmon_x86_ubuntu810 nmon
    [root@mululu nmon]# chmod +x nmon
    [root@mululu nmon]#ls
    _nmon nmon1 nmon_x86_12a.zip nmon_x86_fedora10 nmon_x86_opensuse10 nmon_x86_rhel45 nmon_x86_rhel52 nmon_x86_sles10 nmon_x86_sles9_

然后直接运行 nmon 即可，直接运行nmon可以实时监控系统资源的使用情况，执行下面的步骤可以展现一段时间系统资源消耗的报告。

下面是直接执行nmon命令实时监控系统资源消耗情况的截图：


    [root@mululu nmon]#./nmon

CPU、内存、磁盘和网络的消耗情况都被很直观的展现出来。

按键“C”可以查看CPU相 关信息；

按键“D”可以查看磁盘信息；

按键“T”可以查看系统的进程信息；

“M”对应内存、“N”对应网络等等；

完整的快捷键对应内容可以通过帮助（按键 “H”）查看。

可以显示Linux系统CPU、内存、进程信息，包括了CPU的用户、系统、等待和空闲状态值，可用内存、缓存大小以及进程的CPU消耗等详细指标。该种方式显示信息实时性强，能够及时掌握系统承受压力下的运行情况，每颗CPU利用率是多少、内存使用多少、网络流量多少、磁盘读写……这些数据均是实时刷新，一目了然。

**三.生成nmon报告。**

**1).采集数据：**
#./nmon -s10 -c60 -f -m /home/

参数解释：
-s10 每 10 秒采集一次数据。
-c60 采集 60 次，即为采集十分钟的数据。
-f 生成的数据文件名中包含文件创建的时间。
-m 生成的数据文件的存放目录。

这样就会生成一个 nmon 文件，并每十秒更新一次，直到十分钟后。
生成的文件名如： _090824_1306.nmon ，"" 是这台主机的主机名。

nmon -h查看更多帮助信息。

解决方式：


    先看看这个命令属于哪个软件包：
    [root@mululu ~]#  yum provides */lsb_release
    Loaded plugins: fastestmirror
    Loading mirror speeds from cached hostfile
    * base: mirrors.psychz.net
    * epel: mirrors.solfo.com
    * extras: mirror.san.fastserv.com
    * updates: mirror.lax.hugeserver.com
    base/filelists_db                                                       | 5.1 MB     00:00
    epel/filelists_db                                                       | 7.8 MB     00:00
    extras/filelists_db                                                     |  31 kB     00:00
    updates/filelists_db                                                    | 614 kB     00:00
    vz-base/filelists                                                       |  825 B     00:00
    vz-updates/filelists                                                    | 3.0 kB     00:00
    redhat-lsb-core-4.0-7.el6.centos.i686 : LSB base libraries support for CentOS
    Repo        : base
    Matched from:
    Filename    : /usr/bin/lsb_release
    dkms-2.2.0.3-28.git.7c3e7c5.el6.noarch : Dynamic Kernel Module Support Framework
    Repo        : epel
    Matched from:
    Filename    : /usr/lib/dkms/lsb_release
    dkms-2.2.0.3-26.el6.noarch : Dynamic Kernel Module Support Framework
    Repo        : installed
    Matched from:
    Filename    : /usr/lib/dkms/lsb_release
    redhat-lsb-core-4.0-7.el6.centos.i686 : LSB base libraries support for CentOS
    Repo        : installed
    Matched from:
    Filename    : /usr/bin/lsb_release

    可以看出，属于redhat-lsb这个包，那么接着使用yum安装这个包：
    [root@mululu ~]# yum install  -y  redhat-lsb
    [root@mululu ~]#lsb_release -r

2).**生成报表：**
下载 nmon analyser (生成性能报告的免费工具)：
<https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Power%20Systems/page/nmon_analyser>


将之前生成的 nmon 数据文件传到 Windows 机器上，用 Excel 打开分析工具 nmon analyser v33C.xls 。点击 Excel 文件中的 "Analyze nmon data" 按钮，选择 nmon 数据文件，这样就会生成一个分析后的结果文件： hostname_090824_1306.nmon.xls ，用 Excel 打开生成的文件就可以看到结果了。

如果宏不能运行，需要做以下操作：
工具 -> 宏 -> 安全性 -> 中，然后再打开文件并允许运行宏。


下面是在测试环境中生成的NMON报告截图：

红色区域为不同指标的分析报告。

**3).**

### 定时任务

除配合性能测试的短期监控，我们也可以实现对系统的定期监控，作为运营维护阶段的参考。定期监控实现如下：

1) 执行命令：#crontab –e

2) 在最后一行添加如下命令：
0 8 * * 1,2,3,4,5 /nmon/nmon_x86_rhel5 -f -N -m /nmon/log -s 30 -c 1200
**表示：**
周一到周五，从早上08点开始，监控10个小时（到18:00整为止），输出到/nmon/log

**自动按天采集数据：**
在 crontab 中增加一条记录：
0 0 * * * root nmon -s300 -c288 -f -m /home/ > /dev/null 2>&1

300*288=86400 秒，正好是一天的数据。
