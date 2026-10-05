---
source: "http://www.jb51.net/LINUXjishu/159472.html"
title: "linux查看当前shell的方法_LINUX_操作系统_脚本之家"
fetched_at: "2026-10-05 15:35:41"
---

[脚本之家](/) [服务器常用软件](http://s.jb51.net)

  * __[手机版](https://m.jb51.net/)
  * __[投稿中心](http://tougao.jb51.net)
  * __[关注微信](javascript:void\(0\))

![扫一扫](https://img.jbzj.com/skin/2018/images/erwm.jpg)

[快捷导航 __](javascript:void\(0\);)

[![脚本之家](/images/logo.gif)](/)

  * [网站首页](/)
  * [网页制作](/web/)
  * [网络编程](/list/index_1.htm)
  * [脚本专栏](/list/index_96.htm)
  * [脚本下载](/jiaoben/)
  * [数据库](/list/index_104.htm)
  * [服务器](/list/list_82_1.htm)
  * [电子书籍](/books/)
  * [操作系统](/os/)
  * [网站运营](/yunying/)
  * [平面设计](/pingmian/)
  * _其它_ [媒体动画](/media/) [电脑基础](/diannaojichu/) [硬件教程](/hardware/) [网络安全](/hack/)

__您的位置：[主页](https://www.jb51.net/) > [操作系统](/os/) > [LINUX](/LINUXjishu/) >

# linux查看当前shell的方法

发布时间：2014-04-28 16:41:16 作者：佚名  ![](/skin/2018/images/text-message.png) 我要评论

这篇文章主要介绍了linux查看当前shell的方法,需要的朋友可以参考下

1、实时查看当前进程中使用的shell种类：推荐


 _复制代码_

代码如下:


ps | grep $$ | awk '{print $4}'


（注：$$表示shell的进程号）

2、最常用的查看shell的命令，但不能实时反映当前shell


 _复制代码_

代码如下:


$ echo $SHELL

3、更简洁，但并不是所有shell都支持


 _复制代码_

代码如下:


$ echo $0

4、环境变量中shell的匹配查找


 _复制代码_

代码如下:


env | grep SHELL

5、口令文件中shell的匹配查找


 _复制代码_

代码如下:


cat /etc/passwd | grep muye

6、用ps -ef时候


 _复制代码_

代码如下:


$ ps -ef | grep $$ | grep -v grep | grep -v ps

注：grep -v 表示取反，如下：


 _复制代码_

代码如下:


<a href="mailto:muye@bupt:~$">muye@bupt:~$</a> ps -ef | grep $$
muye 4750 4745 0 15:47 pts/1 00:00:00 bash
muye 5331 4750 0 16:51 pts/1 00:00:00 ps -ef
muye 5332 4750 0 16:51 pts/1 00:00:00 grep --color=auto 4750

去掉后两个

__

  * Tag：[Linux](/do/tag/Linux/) [Shell](/do/tag/Shell/)

## 相关文章

  *   * ![](https://img.jbzj.com/do/uploads/litimg/260413/1551243G458.jpg)

[集成系统级Claw模式! Deepin 官宣发布 25.1 版本](/LINUXjishu/1023027.html "集成系统级Claw模式! Deepin 官宣发布 25.1 版本")

deepin操作系统发布了最新的 25.1 版本更新，该版本基于 deepin 25 正式版积累的多轮内测成果，在 AI 能力、内核版本、桌面环境、文件管理器以及系统安全等方面进行了更新

2026-04-13

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[又一代老硬件退场! Linux 内核正式放弃Intel 486 CPU](/LINUXjishu/1022509.html "又一代老硬件退场! Linux 内核正式放弃Intel 486 CPU")

在过去的几十年间，CPU 的架构已经经历了飞速发展，x86 系列就是其中之一，而 i486 则属于该系列中的一个，当前，i486 的CPU处理器已经够老，从 Linux 7.1 开始将不再有对

2026-04-09

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[赶紧收藏! 全网最全 Linux 命令总结](/LINUXjishu/1022286.html "赶紧收藏! 全网最全 Linux 命令总结")

我把 Linux 中最常用、最实用、最常被问到的命令按照实际使用场景分类整理，方便你快速查阅和记忆，内容覆盖日常运维、开发调试、性能分析、文件处理、网络、安全、系统管

2026-04-08

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[一分钟内检查Linux服务器性能? 9个性能检测常用的基本命令](/LINUXjishu/1019998.html "一分钟内检查Linux服务器性能? 9个性能检测常用的基本命令")

今天我们来看看Linux系统中用于性能监控的一系列命令，这些命令可以快速查看机器的负载情况，详细请看下文介绍

2026-03-18

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[从零基础到精通! 适合高级用户的15款Linux发行版推荐](/LINUXjishu/1019052.html "从零基础到精通! 适合高级用户的15款Linux发行版推荐")

Linux作为操作系统领域灵活性和可定制性的基石，提供了大量满足不同用户需求的发行版，今天分享适合高级用户的15款Linux发行版

2026-03-10

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[开箱即用? 这4个高手级Linux发行版远没你想象的那么安全易用](/LINUXjishu/1019043.html "开箱即用? 这4个高手级Linux发行版远没你想象的那么安全易用")

如果你正在纠结用哪个发行版？零基础新手别被“高端”“极客”“声明式”这些词冲昏头脑，先用好用的，再慢慢进阶

2026-03-10

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[这几款SSH工具真的够用了! Linux好用的ssh工具推荐](/LINUXjishu/1018856.html "这几款SSH工具真的够用了! Linux好用的ssh工具推荐")

在Linux上使用SSH，您需要安装一个SSH客户端，今天整理找到的8 款 SSH / 终端工具，从免费开源到企业级商用，从轻量化命令行到一站式工具箱，每款都做了介绍与对比，希望能

2026-03-09

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[Linux怎么在终端和GNOME中切换用户?](/LINUXjishu/1017575.html "Linux怎么在终端和GNOME中切换用户?")

在Linux系统下有两种用户，即高级用户root，普通用户，高级用户root可以在系统中做任何事情，普通用户仅可在Linux系统中做有限的事情，下面我们就来看看切换方法

2026-02-28

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[揭秘当前登录用户的身份! Linux中使用logname命令的技巧](/LINUXjishu/1017280.html "揭秘当前登录用户的身份! Linux中使用logname命令的技巧")

logname命令就是这样一个简单但强大的工具，它能帮助我们轻松获取当前登录用户的用户名,今天，我们就来深入探索一下这个命令的工作原理、使用方法和最佳实践

2026-02-26

  * ![](https://img.jbzj.com/do/uploads/litimg/241021/1523313N405.jpg)

[Linux怎么刷DNS? linux刷新dns缓存命令](/LINUXjishu/1017265.html "Linux怎么刷DNS? linux刷新dns缓存命令")

在 Linux 系统中，DNS 缓存是一种将域名和 IP 地址映射关系缓存在本地的机制，可以加快域名解析速度，并减轻 DNS 服务器的负载

2026-02-26

#### 文章分类

  * [bios](/os/list682_1.html "bios")
  * [系统安装](/os/list490_1.html "系统安装")
  * [系统进程](/os/list685_1.html "系统进程")
  * [Windows系列](/os/windows/ "Windows系列")
  * [苹果MAC](/os/MAC/ "苹果MAC")
  * [LINUX](/LINUXjishu/ "LINUX")
  * [RedHat/Centos](/os/RedHat/ "RedHat/Centos")
  * [Ubuntu/Debian](/os/Ubuntu/ "Ubuntu/Debian")
  * [Fedora](/os/Fedora/ "Fedora")
  * [Solaris](/os/Solaris/ "Solaris")
  * [麒麟系统](/os/qilin/ "麒麟系统")
  * [红旗Linux](/os/hongqi/ "红旗Linux")
  * [Unix/BSD](/os/Unix/ "Unix/BSD")
  * [注册表](/os/list381_1.html "注册表")
  * [鸿蒙系统](/os/harmonyos/ "鸿蒙系统")
  * [其它系统](/os/other/ "其它系统")

#### 大家感兴趣的内容

  * _1_[linux下tar.gz、tar、bz2、zip等解压缩、压缩命令小结](/LINUXjishu/43356.html "linux下tar.gz、tar、bz2、zip等解压缩、压缩命令小结")
  *  _2_[Linux crontab定时执行任务 命令格式与详细例子](/LINUXjishu/19905.html "Linux crontab定时执行任务 命令格式与详细例子")
  *  _3_[Linux Top 命令解析 比较详细](/LINUXjishu/34604.html "Linux Top 命令解析 比较详细")
  *  _4_[linux下提示bash:command not found ](/LINUXjishu/32192.html "linux下提示bash:command not found ")
  * _5_[Linux中zip压缩和unzip解压缩命令详解](/LINUXjishu/105916.html "Linux中zip压缩和unzip解压缩命令详解")
  *  _6_[linux下配置ip地址四种方法(图文方法)](/LINUXjishu/64000.html "linux下配置ip地址四种方法\(图文方法\)")
  * _7_[史上最全的Linux系统 ISO下载](/LINUXjishu/239493.html "史上最全的Linux系统 ISO下载")
  *  _8_[linux ln 命令使用参数详解(ln -s 软链接)](/LINUXjishu/150570.html "linux ln 命令使用参数详解\(ln -s 软链接\)")
  * _9_[linux su和sudo命令的区别](/LINUXjishu/12713.html "linux su和sudo命令的区别")
  *  _10_[linux下磁盘分区详解 图文](/LINUXjishu/57192.html "linux下磁盘分区详解 图文")

#### 最近更新的内容

  * [集成系统级Claw模式! Deepin 官宣发布 25.1 版本](/LINUXjishu/1023027.html "集成系统级Claw模式! Deepin 官宣发布 25.1 版本")
  * [又一代老硬件退场! Linux 内核正式放弃Intel 486 CPU](/LINUXjishu/1022509.html "又一代老硬件退场! Linux 内核正式放弃Intel 486 CPU")
  * [赶紧收藏! 全网最全 Linux 命令总结](/LINUXjishu/1022286.html "赶紧收藏! 全网最全 Linux 命令总结")
  * [Linux如何安装运行.AppImage文件?.AppImage文件两种运](/LINUXjishu/675717.html "Linux如何安装运行.AppImage文件?.AppImage文件两种运")
  * [一分钟内检查Linux服务器性能? 9个性能检测常用的基本](/LINUXjishu/1019998.html "一分钟内检查Linux服务器性能? 9个性能检测常用的基本")
  * [从零基础到精通! 适合高级用户的15款Linux发行版推荐](/LINUXjishu/1019052.html "从零基础到精通! 适合高级用户的15款Linux发行版推荐")
  * [开箱即用? 这4个高手级Linux发行版远没你想象的那么安](/LINUXjishu/1019043.html "开箱即用? 这4个高手级Linux发行版远没你想象的那么安")
  * [这几款SSH工具真的够用了! Linux好用的ssh工具推荐](/LINUXjishu/1018856.html "这几款SSH工具真的够用了! Linux好用的ssh工具推荐")
  * [Linux怎么在终端和GNOME中切换用户?](/LINUXjishu/1017575.html "Linux怎么在终端和GNOME中切换用户?")
  * [揭秘当前登录用户的身份! Linux中使用logname命令的技](/LINUXjishu/1017280.html "揭秘当前登录用户的身份! Linux中使用logname命令的技")

微信 [投稿](http://tougao.jb51.net/ "投稿") [脚本任务](https://task.jb51.net/ "脚本任务") [在线工具](http://tools.jb51.net/ "在线工具")

关注微信公众号

![扫一扫](https://img.jbzj.com/skin/2018/images/erwm.jpg)
