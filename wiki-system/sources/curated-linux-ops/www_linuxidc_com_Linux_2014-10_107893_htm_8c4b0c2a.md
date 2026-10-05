---
source: "http://www.linuxidc.com/Linux/2014-10/107893.htm"
title: "VMware虚拟机网络模式的区别_Linux教程_Linux公社-Linux系统门户网站"
fetched_at: "2026-10-05 15:35:52"
---

你好，游客 登录 [注册](../../memberreg.aspx) [搜索](../../search.aspx)

[![Linux公社](../../pic/logo.jpg)](http://www.linuxidc.com/) |
---|---

[首页](../../index.htm)[Linux新闻](../../it/)[Linux教程](../../Linuxit/)[数据库技术](../../MySql/)[Linux编程](../../RedLinux/)[服务器应用](../../Apache/)[Linux安全](../../Unix/)[Linux下载](../../download/)[Linux认证](../../Linuxrz/)[Linux主题](../../theme/)[Linux壁纸](../../Linuxwallpaper/)[Linux软件](../../linuxsoft/)[数码](../../digi/)[手机](../../mobile/)[电脑](../../diannao/)

[首页](../../index.htm) → [Linux教程](../../Linuxit/)

背景：  阅读新闻

# VMware虚拟机网络模式的区别

| [日期：2014-10-11] | 来源：Linux社区 作者：yinuoqianjin | [字体：[大](javascript:ContentSize\(16\)) [中](javascript:ContentSize\(0\)) [小](javascript:ContentSize\(12\))]
---|---|---

一、虚拟机网卡模式分类
二、环境
三、网卡简介
四、模式简介
五、使用“仅主机模式”让虚拟机和物理机进行相互通信（重点）

**一、虚拟机网卡模式分类**

虚拟机网卡模式，共5种。如下，在此主要讲解前三种，即桥接模式，NAT模式，仅主机模式。

![](../../upload/2014_10/141011195445023.jpg)

**二、环境**

物理机系统：win7旗舰版

虚拟机系统：[RedHat](http://www.linuxidc.com/topicnews.aspx?tid=10 "RedHat")6.5

虚拟机软件：VMware Workstation 10（[http://www.linuxidc.com/Linux/2012-11/73743.htm](../../Linux/2012-11/73743.htm)）

**三、网卡简介**

我们首先说一下VMware的几个虚拟设备

VMnet0：用于虚拟桥接网络下的虚拟交换机

VMnet1：用于虚拟Host-Only网络下的虚拟交换机

VMnet8：用于虚拟NAT网络下的虚拟交换机

VMware Network Adepter VMnet1：Host用于与Host-Only虚拟网络进行通信的虚拟网卡

VMware Network Adepter VMnet8：Host用于与NAT虚拟网络进行通信的虚拟网卡

其中VMnet0、VMnet1和VMnet8是虚拟机自身的虚拟交换机。

![](../../upload/2014_10/141011195445022.jpg)

VMware Network Adepter VMnet1和VMware Network Adepter VMnet8是物理机安装完虚拟机后生成的虚拟网卡。

![](../../upload/2014_10/141011195445021.jpg)

**四、模式简介**

1.桥接模式：

桥接网络是指本地物理网卡和虚拟网卡通过VMnet0虚拟交换机进行桥接，物理网卡和虚拟网卡在拓扑图上处于同等地位（虚拟网卡既不是VMware Network Adepter VMnet1也不是VMware Network Adepter VMnet8）。桥接模式必须要使用交换机或路由器才能和外界通信，此时，虚拟机自身和物理机是相互独立的，处于同等地位，如果虚拟机和物理机的网卡在同一网段，是相互能通信的。

2.NAT模式：

在NAT网络中，会用到VMware Network Adepter VMnet8虚拟网卡，主机上的VMware Network Adepter VMnet8虚拟网卡被直接连接到VMnet8虚拟交换机上与虚拟网卡进行通信。VMware Network Adepter VMnet8虚拟网卡的作用仅限于和VMnet8网段进行通信，它不给VMnet8网段提供路由功能，所以虚拟机虚拟一个NAT服务器，使虚拟网卡可以连接到Internet。VMware Network Adepter VMnet8虚拟网卡的IP地址是在安装VMware时由系统DHCP指定生成的，我们不要修改这个数值，否则会使主机和虚拟机无法通信。

3.仅主机模式：

在Host-Only模式下，虚拟网络是一个全封闭的网络，它唯一能够访问的就是主机。其实Host-Only网络和NAT网络很相似，不同的地方就是Host-Only网络没有NAT服务，所以虚拟网络不能连接到Internet。主机和虚拟机之间的通信是通过VMware Network Adepter VMnet1虚拟网卡来实现的。

**五、使用“仅主机模式”让虚拟机和物理机进行相互通信**

注意：校园锐捷用户请注意，因为你们使用的校园网锐捷客户端是限制多网卡的使用的，所以如果把VMware Network Adepter VMnet1网卡打开，这样你们就无法正常上网了，但是锐捷的客户端可以破解多网卡模式的，破解后，多网卡可以同时使用，所以请校园锐捷用户首先破解自己的锐捷客户端为多网卡模式，具体破解办法请自行解决。

1.首先编辑物理机的VMware Network Adepter VMnet1网卡信息。

![](../../upload/2014_10/141011195445025.jpg)

2.假设我们目前使用192.168.2.0/24网段内的地址。

![](../../upload/2014_10/141011195445024.jpg)

**更多详情见请继续阅读下一页的精彩内容** ： [http://www.linuxidc.com/Linux/2014-10/107893p2.htm](../../Linux/2014-10/107893p2.htm)

[![linux](/linuxfile/logo.gif)](http://www.linuxidc.com)

  * 1
  * [2](../../Linux/2014-10/107893p2.htm)
  * [下一页](../../Linux/2014-10/107893p2.htm "下一页")
  *

---

[解决KVM中宿主机通过console无法连接客户机](../../Linux/2014-10/107891.htm)

[如何使用XManager下的Xshell远程连接Linux](../../Linux/2014-10/107894.htm)

相关资讯 [VMware虚拟机](../../search.aspx?where=nkey&keyword=1134)

  * [VMware Workstation 虚拟机使用方](../../Linux/2017-03/141972.htm "VMware Workstation 虚拟机使用方法图文详解") (今 15:11)
  * [使用VMware虚拟机安装virt-manager](../../Linux/2016-01/126959.htm "使用VMware虚拟机安装virt-manager unable to connect to libvirt的处理办法") (01/01/2016 19:46:47)
  * [VMware Workstation虚拟机Ubuntu中](../../Linux/2015-03/114991.htm "VMware Workstation虚拟机Ubuntu中实现与主机共享（复制和粘贴）") (03/14/2015 19:25:21)

|

  * [从外网访问VMware虚拟机的Web服务](../../Linux/2017-01/139529.htm) (01月13日)
  * [VMware虚拟机无法上网 无法启动](../../Linux/2015-05/117704.htm "VMware虚拟机无法上网 无法启动VMnet0等问题") (05/19/2015 10:19:19)
  * [VMware 虚拟机使用RedHat，出现 ](../../Linux/2015-02/113119.htm "VMware 虚拟机使用RedHat，出现 connect: Network is unreachable解決方法") (02/08/2015 20:41:14)


---|---

本文评论 [查看全部评论](../../remark.aspx?id=107893) (0)

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

  * [VMware Workstation 虚拟机使用方法图文详](../../Linux/2017-03/141972.htm "VMware Workstation 虚拟机使用方法图文详解")
  * [GRUB应用详解](../../Linux/2017-03/141971.htm)
  * [Linux Kernel 本地拒绝服务漏洞(CVE-2017-](../../Linux/2017-03/141970.htm "Linux Kernel 本地拒绝服务漏洞\(CVE-2017-6951\)")
  * [QEMU 'virtio-gpu-3d.c'本地拒绝服务漏洞(](../../Linux/2017-03/141969.htm "QEMU 'virtio-gpu-3d.c'本地拒绝服务漏洞\(CVE-2017-5857\)")
  * [Google Android Audioserver多个权限提升漏](../../Linux/2017-03/141968.htm "Google Android Audioserver多个权限提升漏洞")
  * [Google Android Kernel ION Subsystem多个](../../Linux/2017-03/141967.htm "Google Android Kernel ION Subsystem多个权限提升漏洞")
  * [CentOS系统启动流程图文详解](../../Linux/2017-03/141966.htm)
  * [Oracle开启并行的几种方法](../../Linux/2017-03/141965.htm)
  * [Oracle中常见的Hint(一)](../../Linux/2017-03/141964.htm)
  * [Windows 10 仍然会通过以量计费的网络推送](../../Linux/2017-03/141963.htm "Windows 10 仍然会通过以量计费的网络推送部份更新")



[Linux公社简介](http://www.linuxidc.com/aboutus.htm) \- [广告服务](http://www.linuxidc.com/adsense.htm) \- [网站地图](http://www.linuxidc.com/sitemap.aspx) \- [帮助信息](http://www.linuxidc.com/help.htm) \- [联系我们](http://www.linuxidc.com/contactus.htm)
本站（LinuxIDC）所刊载文章不代表同意其说法或描述，仅为提供更多信息，也不构成任何建议。


Copyright © 2006-2016 [Linux公社](http://www.linuxidc.com/) All rights reserved 沪ICP备15008072号-1号
