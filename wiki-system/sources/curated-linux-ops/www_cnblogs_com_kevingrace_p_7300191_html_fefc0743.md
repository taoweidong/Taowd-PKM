---
source: "https://www.cnblogs.com/kevingrace/p/7300191.html"
title: "Netdata---Linux系统性能实时监控平台部署记录 - 散尽浮华 - 博客园"
fetched_at: "2026-10-05 15:34:51"
---

通常来说，作为一个Linux的SA，很有必要掌握一个专门的系统监控工具，以便能随时了解系统资源的占用情况。下面就介绍下一款Linux性能实时监测工具-Netdata，它是Linux系统实时性能监测工具，以web的可视化方式展示系统及应用程序的实时运行状态（包括cpu、内存、硬盘输入/输出、网络等linux性能的数据）。Netdata的web前端响应很快，而且不需要Flash插件。 UI很整洁，保持着 Netdata 应有的特性。第一眼看上去，你能够看到很多图表，幸运的是绝大多数常用的图表数据（像 CPU，RAM，网络和硬盘）都在顶部。如果你想深入了解图形化数据，你只需要下滑滚动条，或者点击在右边菜单的项目。通过每个图表的右下方的按钮，Netdata还能控制图表的显示，重置，缩放。Netdata文档地址：<https://github.com/firehol/netdata/wiki>

Netdata用可视化的手段，将被监测者最细微的细节，展现了出来。这样便可以清晰地了解linux系统和应用程序此时的状况。Netdata主要功能:


    优美的界面：bootstrap框架下的控制界面, 酷炫（主要是dark主题，light主题就没这感觉了）
    自定义的控制界面：你可以使用简单的HTML代码去自定义控制界面(不需要使用javascript)
    极其的快速而高效：程序使用C进行编写(默认安装下，预计只有2%的单核CPU使用率和少许的内存使用率)
    零配置：你只需要去安装它，接着它就会自动地监测一切数据
    零依赖：它的静态网络文件和网络接口拥有自己的网络服务器. netdata有自己的web server， 提供静态web文件和web API
    可扩展：用它自身的插件API(可以使用许多方式来制作它的插件，从bash到node.js),你可以检测任何可以衡量的数据。
    可嵌入：它可以在任何Linux内核可以运行的地方运行
    零维护：只管跑上！
    匪夷所思的快。。。所有请求每个metreic都在0.5ms内响应，即便是一台烂机器
    非常高效，每秒采集数千个指标，但仅占cpu单核1%，少量MB的内存以及完全没有磁盘IO
    提供复杂的、各种类型的告警，支持动态阈值、告警模板、多种通知方式等
    支撑多种时间序列后端服务，比如graphite, opentsdb, prometheus, json document DBs

**监测内容** ：下面是Netdata目前检测的内容（大多数都不需要进行配置，安装后即可开始监测）


    1.CPU的使用率,中断，软中断和频率(总量和每个单核)
    2.RAM，互换和内核内存的使用率（包括KSM和内核内存deduper）
    3.硬盘输入/输出(每个硬盘的带宽，操作，整理，利用等)
    4.IPv4网络（数据包，错误，分片）：
    TCP：连接，数据包，错误，握手
    UDP:数据包，错误
    广播：带宽，数据包
    组播：带宽，数据包
    5.Netfilter/iptables Linux防火墙(连接，连接跟踪事件，错误等)
    6.进程(运行，受阻，分叉，活动等)
    7.NFS文件服务器，v2,v3,v4(输入/输出，缓存，预读，RPC调用)
    8.网络服务质量（唯一一个可实时可视化网络状况的工具）
    9.应用程序，通过对进程树进行分组（CPU,内存，硬盘读取，硬盘写入，交换，线程，管道，套接字等）
    10.Apache Web服务器状态(v2.2, v2.4)
    11.Nginx Web服务器状态
    12.Mysql数据库（多台服务器，单个显示：带宽，查询/s, 处理者，锁，问题，临时操作，连接，二进制日志，线程，innodb引擎等）
    13.ISC Bind域名服务器（多个服务器，单个显示：客户，请求，查询，更新，失败等）
    14.Postfix邮件服务器的消息队列（条目，大小）
    15.Squid代理服务器（客户带宽和请求，服务带宽和请求）
    16.硬件传感器（温度，电压，风扇，电源，湿度等）
    17.NUT UPSes（负载，充电，电池电压，温度，使用指标，输出指标）
    可以监测任意数量的SNMP服务，不过你需要进行配置，还可以对此软件进行扩展，可以使用任何语言编写插件，以此来从任何来源收集数据


**下面简单记录下Netdata的部署过程（Cetnos下）：**


    netdata下载地址：http://firehol.org/download/netdata/releases/v1.0.0/
    autogen下载地址：http://ftp.gnu.org/gnu/autogen/5.11.8/

    [root@monit ~]# yum install zlib-devel gcc make git autoconf autogen guile-devel automake pkgconfig
    [root@monit ~]# rpm -ivh autogen-5.11.8-5.x86_64.rpm --force                    //yum安装autogen可能会报错说没有此包，那么就单独下载autogen的rpm包进行安装
    [root@monit ~]# tar -jvxf netdata-1.0.0.tar.bz2
    [root@monit ~]# cd netdata-1.0.0
    [root@monit netdata-1.0.0]# ./netdata-installer.sh --install /data

    按照上面命令执行后的提示进行安装，安装后，netdata会自动重启。端口为19999
    [root@monit ~]# ps -ef|grep netdata
    netdata  10976     1  0 17:01 ?        00:00:03 /data/netdata/usr/sbin/netdata
    netdata  10982 10976  0 17:01 ?        00:00:00 /bin/bash /data/netdata/usr/libexec/netdata/plugins.d/tc-qos-helper.sh 1
    netdata  10984 10976  0 17:01 ?        00:00:07 /bin/bash /data/netdata/usr/libexec/netdata/plugins.d/charts.d.plugin 1
    root     10986 10976  0 17:01 ?        00:00:04 /data/netdata/usr/libexec/netdata/plugins.d/apps.plugin 1
    netdata  29395 10982  0 17:22 ?        00:00:00 sleep 0.998
    netdata  29401 10984  0 17:22 ?        00:00:00 sleep 0.2
    root     29403 25980  0 17:22 pts/0    00:00:00 grep netdata
    [root@monit ~]# lsof -i:19999
    COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    netdata 10976 netdata    3u  IPv6 499147      0t0  TCP *:dnp-sec (LISTEN)

    启动与关闭
    启动：/data/netdata/usr/sbin/netdata
    关闭：killall netdata


**或者 通过下面方式进行安装:**


    1) 安装准备
    Netdata提供了一个非常简便的安装方法，只需要执行下面的命令即可完成安装netdata所依赖的各种东西：
    # curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata

    注意，上面的命令是安装基本的部分，不包括mysql / mariadb, postgres, named, hardware sensors and SNMP. 如果要完整安装，则需要执行下面的命令：
    # curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata-all

    2) 安装Netdata
    安装Netdata也很简单，按照wiki的说明即可：
    # git clone https://github.com/firehol/netdata.git --depth=1
    # cd netdata
    # ./netdata-installer.sh

    注意上面要使用root权限，执行命令后的提示信息也很丰富有趣

    安装完后，还可以根据wiki所说的配置开机启动，照做之后执行service netdata start启动服务，可以访问http://localhost:19999/ 看到监控界面。

Netdata的访问，http://localhost:19999 运行动态效果图如下：

**Netdata backend**
Netdata也可以后台服务收集监控指标，多服务器的监控指标汇总到前台展示，或者归档汇总后提供给其他工具如grafana， 如下图：

Netdata支持如下几个backends:
\- graphite;
\- opentsdb;
\- json document DBs.

Netdata还提供了3种计算模式：
\- as collected；
\- average;
\- sum or volume。

具体的可以到[netdata wiki](https://docs.netdata.cloud/backends/)查看。利用这种方式，应该也较容易能够折腾出来一个集群监控的解决方案，并且netdata和grafana的界面看起来都非常的酷炫!
