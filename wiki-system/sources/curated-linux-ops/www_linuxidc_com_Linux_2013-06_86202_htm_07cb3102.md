---
source: "http://www.linuxidc.com/Linux/2013-06/86202.htm"
title: "RedHat设置Yum源_Linux教程_Linux公社-Linux系统门户网站"
fetched_at: "2026-10-05 15:34:53"
---

[手机版](http://m.linuxidc.com)

你好，游客 登录 [注册](../../memberreg.aspx)

[![Linux公社](../../pic/logo.jpg)](https://www.linuxidc.com/) |
---|---

[首页](../../index.htm)[Linux新闻](../../it/)[Linux教程](../../Linuxit/)[数据库技术](../../MySql/)[Linux编程](../../RedLinux/)[服务器应用](../../Apache/)[Linux安全](../../Unix/)[Linux下载](../../download/)[Linux主题](../../theme/)[Linux壁纸](../../Linuxwallpaper/)[Linux软件](../../linuxsoft/)[数码](../../digi/)[手机](../../mobile/)[电脑](../../diannao/)

[首页](../../index.htm) → [Linux教程](../../Linuxit/)

背景：  阅读新闻

# RedHat设置Yum源

| [日期：2013-06-18] | 来源：Linux社区 作者：wangdongsong  | [字体：[大](javascript:ContentSize\(16\)) [中](javascript:ContentSize\(0\)) [小](javascript:ContentSize\(12\))]
---|---|---

Linux:[RedHat](https://www.linuxidc.com/topicnews.aspx?tid=10 "RedHat") AS 6.2的版本

1、删除原有的yum:

rpm -aq | grep yum | xargs rpm -e –nodeps

2、安装新的yum

《1》rpm –ivh http://mirrors.163.com/[CentOS](https://www.linuxidc.com/topicnews.aspx?tid=14 "CentOS")/6/os/x86_64/Packages/[Python](https://www.linuxidc.com/topicnews.aspx?tid=17 "Python")-iniparse-0.3.1-2.1.el6.noarch.rpm

注：python-iniparse-0.3.1-2.1.el6.noarch.rpm这个版本可能随着包的更新导致在这个地址上不一定存在，可输入http://mirrors.163.com/centos/6/os/x86_64/Packages（CentOS6），这个页上面有具体包列表，查找python-iniparse的包，修改为正确的地址即可。下面几步和这一步相似。

《2》rpm -ivh http://mirrors.163.com/centos/6/os/x86_64/Packages/yum-metadata-parser-1.1.2-16.el6.x86_64.rpm

《3》rpm -ivhhttp://mirrors.163.com/centos/6/os/x86_64/Packages/yum-3.2.29-40.el6.centos.noarch.rpm http://mirrors.163.com/centos/6/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.30-14.el6.noarch.rpm

注：这是两个rpm包

《4》cd /etc/yum.repos.d/

《5》wget http://mirrors.163.com/.help/CentOS6-Base-163.repo

《6》sed -i "s/\$releasever/6/"CentOS6-Base-163.repo

《7》yum makecache

更多RedHat相关信息见[RedHat](../../topicnews.aspx?tid=10 "RedHat") 专题页面 [http://www.linuxidc.com/topicnews.aspx?tid=10](../../topicnews.aspx?tid=10 "RedHat")

[![linux](/linuxfile/logo.gif)](http://www.linuxidc.com)

[利用VMware虚拟机的NAT形式组建Linux虚拟局域网](../../Linux/2013-06/86201.htm)

[解决 UNetbootin 引导故障](../../Linux/2013-06/86224.htm)

相关资讯 [YUM源](../../search.aspx?where=nkey&keyword=13300) [RedHat YUM](../../search.aspx?where=nkey&keyword=17174) [设置Yum源](../../search.aspx?where=nkey&keyword=22442)

  * [CentOS 7的yum更换为国内的阿里云](../../Linux/2019-08/160310.htm "CentOS 7的yum更换为国内的阿里云yum源") (今 06:13)
  * [Linux里如何配置本地yum源和外网源](../../Linux/2019-06/158907.htm) (06月01日)
  * [Red Hat Enterprise Linux 7.3更换](../../Linux/2018-12/155855.htm "Red Hat Enterprise Linux 7.3更换CentOS 7 yum源") (12/14/2018 21:17:04)

|

  * [按需制作最小的本地yum源](../../Linux/2019-08/159982.htm) (08月12日)
  * [yum更换国内源及yum下载rpm包](../../Linux/2019-06/158905.htm) (06月01日)
  * [Linux基础入门教程-RHEL7.4之YUM更](../../Linux/2018-09/154064.htm "Linux基础入门教程-RHEL7.4之YUM更换CentOS源") (09/13/2018 09:06:34)


---|---

本文评论 [查看全部评论](../../remark.aspx?id=86202) (0)

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
  * [如何在Linux或Unix上使用grep计算单词出现](../../Linux/2019-08/160309.htm "如何在Linux或Unix上使用grep计算单词出现次数")
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
