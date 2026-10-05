---
source: "http://jingyan.baidu.com/article/08b6a591f0fafc14a9092275.html"
title: "Linux系统下如何配置SSH？如何开启SSH-百度经验"
fetched_at: "2026-10-05 15:34:47"
---

# Linux系统下如何配置SSH？如何开启SSH？

  * 原创
  * |
  * 浏览：178245
  * |
  * 更新：2020-05-20 14:41

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=1)1

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=2)2

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=3)3

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=4)4

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=5)5

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=6)6

  * [](/album/08b6a591f0fafc14a9092275.html?picindex=7)7

[分步阅读](/album/08b6a591f0fafc14a9092275.html)

SSH作为Linux远程连接重要的方式，如何配置安装linux系统的SSH服务，如何开启SSH？下面来看看吧（本例为centos系统演示如何开启SSH服务）

## [](javascript:;)工具/原料

  * linux  centos

## [](javascript:;)查询\安装SSH服务

  1. 1

1.登陆linux系统，打开终端命令。输入 rpm -qa |grep ssh 查找当前系统是否已经安装

  2. 2

2.如果没有安装SSH软件包，可以通过yum 或rpm安装包进行安装（具体就不截图了)

END

## [](javascript:;)启动SSH服务2

  1. 1

安装好了之后，就开启ssh服务。Ssh服务一般叫做 SSHD

命令行输入 service sshd start 可以启动

  2. 2

或者使用 /etc/init.d/sshd start

END

## [](javascript:;)配置\查看SSHD端口3

  1. 1

查看或编辑SSH服务配置文件，如 vi /etc/ssh/sshd.config

如果要修改端口，把 port 后面默认的22端口改成别的端口即可（注意前面的#号要去掉）

END

## [](javascript:;)远程连接SSH4

  1. 1

如果需要远程连接SSH，需要把22端口在防火墙上开放。

.关闭防火墙，或者设置22端口例外

END

## [](javascript:;)注意事项

  * 如果还不清楚SSH端口如何修改，可以参考小编的经验如何修改SSH端口号？http://jingyan.baidu.com/article/414eccf61b23ca6b431f0ad8.html

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
