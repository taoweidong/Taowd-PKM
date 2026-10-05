---
source: "http://www.linuxidc.com/Linux/2013-07/87383.htm"
title: "RedHat 6.2 Linux修改yum源免费使用CentOS源_Linux教程_Linux公社-Linux系统门户网站"
fetched_at: "2026-10-05 15:34:53"
---

[手机版](http://m.linuxidc.com)

你好，游客 登录 [注册](../../memberreg.aspx)

[![Linux公社](../../pic/logo.jpg)](https://www.linuxidc.com/) |
---|---

[首页](../../index.htm)[Linux新闻](../../it/)[Linux教程](../../Linuxit/)[数据库技术](../../MySql/)[Linux编程](../../RedLinux/)[服务器应用](../../Apache/)[Linux安全](../../Unix/)[Linux下载](../../download/)[Linux主题](../../theme/)[Linux壁纸](../../Linuxwallpaper/)[Linux软件](../../linuxsoft/)[数码](../../digi/)[手机](../../mobile/)[电脑](../../diannao/)

[首页](../../index.htm) → [Linux教程](../../Linuxit/)

背景：  阅读新闻

# RedHat 6.2 Linux修改yum源免费使用CentOS源

| [日期：2013-07-15] | 来源：Linux社区 作者：Linux | [字体：[大](javascript:ContentSize\(16\)) [中](javascript:ContentSize\(0\)) [小](javascript:ContentSize\(12\))]
---|---|---

在没有光盘的情况，需要安装软件包，就要用到共网的yum源来安装了。

[RedHat](https://www.linuxidc.com/topicnews.aspx?tid=10 "RedHat") linux 默认是安装了yum软件的，但是由于激活认证的原因让redhat无法直接进行yum安装一些软件，如果我们需要在redhat下直接yum安装软件，我们只用把yum的源修改成[CentOS](https://www.linuxidc.com/topicnews.aspx?tid=14 "CentOS")的就好了，然后把源里面的变量全部修改成实际的值，这样就能使用yum直接安装我们需要的软件了。

使用说明

1、到http://mirrors.163.com的 centos帮助文档 中下载CentOS6-Base-163.repo文件，存放到/etc/yum.repo.d中

Centos 5 wget http://mirrors.163.com/.help/CentOS5-Base-163.repo

Centos 6 wget http://mirrors.163.com/.help/CentOS6-Base-163.repo

操作如下：

![](../../upload/2013_07/130715112197511.png)

2、首先备份/etc/yum.repos.d/CentOS-Base.repo

3、编辑CentOS6-Base-163.repo文件，将其中的$releasever更改为centos的版本号，如果是RedHat 6.2 X86_64为例“baseurl=http://mirrors.163.com/centos/6.2/os/x86_64/”，本文档是以RedHat 6.2 32位为例所写！

[base]

name=CentOS-6.2 - Base - 163.com

baseurl=http://mirrors.163.com/centos/6.2/os/$basearch/

#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os

gpgcheck=1

gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6.2

#released updates

[updates]

name=CentOS-6.2 - Updates - 163.com

baseurl=http://mirrors.163.com/centos/6.2/updates/$basearch/

#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates

gpgcheck=1

gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6.2

#additional packages that may be useful

[extras]

name=CentOS-6.2 - Extras - 163.com

baseurl=http://mirrors.163.com/centos/6.2/extras/$basearch/

#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras

gpgcheck=1

gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6.2

#additional packages that extend functionality of existing packages

[centosplus]

name=CentOS-6 .2- Plus - 163.com

baseurl=http://mirrors.163.com/centos/6.2/centosplus/$basearch/

#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus

gpgcheck=1

enabled=0

gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6.2

#contrib - packages by Centos Users

[contrib]

name=CentOS-6.2 - Contrib - 163.com

baseurl=http://mirrors.163.com/centos/6.2/contrib/$basearch/

#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=contrib

gpgcheck=1

enabled=0

gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6.2

编辑完后保存，运行：

yum clean all 清除原有缓存

yum makecache 获取yum列表

**相关阅读：**

RedHat设置Yum源 [http://www.linuxidc.com/Linux/2013-06/86202.htm](../../Linux/2013-06/86202.htm)

搭建内网yum服务器 [http://www.linuxidc.com/Linux/2013-07/86847.htm](../../Linux/2013-07/86847.htm)

搭建局域网CentOS Yum服务器 [http://www.linuxidc.com/Linux/2012-05/60167.htm](../../Linux/2012-05/60167.htm)

更多CentOS相关信息见[CentOS](../../topicnews.aspx?tid=14) 专题页面 [http://www.linuxidc.com/topicnews.aspx?tid=14](../../topicnews.aspx?tid=14 "CentOS")

更多RedHat相关信息见[RedHat](../../topicnews.aspx?tid=10 "RedHat") 专题页面 [http://www.linuxidc.com/topicnews.aspx?tid=10](../../topicnews.aspx?tid=10 "RedHat")

[![linux](/linuxfile/logo.gif)](http://www.linuxidc.com)

[Linux使用入门教程2-Linux基础](../../Linux/2013-07/87382.htm)

[浅谈Linux 的grep命令与正则表达式](../../Linux/2013-07/87384.htm)

相关资讯 [yum](../../search.aspx?where=nkey&keyword=836) [YUM源](../../search.aspx?where=nkey&keyword=13300)

  * [CentOS 7的yum更换为国内的阿里云](../../Linux/2019-08/160310.htm "CentOS 7的yum更换为国内的阿里云yum源") (今 06:13)
  * [按需制作最小的本地yum源](../../Linux/2019-08/159982.htm) (08月12日)
  * [yum更换国内源及yum下载rpm包](../../Linux/2019-06/158905.htm) (06月01日)

|

  * [YUM仓库配置及命令详解](../../Linux/2019-08/160112.htm) (08月16日)
  * [Linux里如何配置本地yum源和外网源](../../Linux/2019-06/158907.htm) (06月01日)
  * [你希望在Fedora中将DNF重命名为Yum](../../Linux/2019-03/157505.htm "你希望在Fedora中将DNF重命名为Yum吗？") (03月15日)


---|---

本文评论 [查看全部评论](../../remark.aspx?id=87383) (0)

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

  * [CentOS 7的yum更换为国内的阿里云yum源](../../Linux/2019-08/160310.htm)
  * [CentOS 7.6下编译安装Python 3.8.0](../../Linux/2019-08/160311.htm)
  * [如何在Linux或Unix上使用grep计算单词出现](../../Linux/2019-08/160309.htm "如何在Linux或Unix上使用grep���算单词出现次数")
  * [GitHub现在支持安全密钥和生物识别进行身份](../../Linux/2019-08/160308.htm "GitHub现在支持安全密钥和生物识别进行身份验证")
  * [F-Secure在Xilinx Zynq UltraScale+ SoCs上](../../Linux/2019-08/160307.htm "F-Secure在Xilinx Zynq UltraScale+ SoCs上发现两个漏洞")
  * [研究人员发现Neutrino僵尸网络可以窃取其他](../../Linux/2019-08/160306.htm "研究人员发现Neutrino僵尸网络可以窃取其他黑客的WebShell")
  * [MongoDB实现评论榜](../../Linux/2019-08/160305.htm)
  * [微软，谷歌和其他巨头创建了机密计算联盟，](../../Linux/2019-08/160304.htm "微软，谷歌和其他巨头创建了机密计算联盟，共同保护数据安全")
  * [Qt 推出 Qt for MCUs，用于在微控制器上创](../../Linux/2019-08/160303.htm "Qt 推出 Qt for MCUs，用于在微控制器上创建图形工具")
  * [Red Hat Enterprise Linux 6 和 CentOS 6 ](../../Linux/2019-08/160302.htm "Red Hat Enterprise Linux 6 和 CentOS 6 收到重要的内核安全更新")



[Linux公社简介](https://www.linuxidc.com/aboutus.htm) \- [广告服务](https://www.linuxidc.com/adsense.htm) \- [网站地图](https://www.linuxidc.com/sitemap.aspx) \- [帮助信息](https://www.linuxidc.com/help.htm) \- [联系我们](https://www.linuxidc.com/contactus.htm)
本站（LinuxIDC）所刊载文章不代表同意其说法或描述，仅为提供更多信息，也不构成任何建议。


Copyright © 2006-2019 [Linux公社](https://www.linuxidc.com/) All rights reserved 浙ICP备07014134号-8
