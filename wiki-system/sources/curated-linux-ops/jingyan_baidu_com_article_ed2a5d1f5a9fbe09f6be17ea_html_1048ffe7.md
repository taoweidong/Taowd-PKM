---
source: "http://jingyan.baidu.com/article/ed2a5d1f5a9fbe09f6be17ea.html"
title: "linux下yum安装及配置-百度经验"
fetched_at: "2026-10-05 15:35:07"
---

# linux下yum安装及配置

  * 原创
  * |
  * 浏览：60851
  * |
  * 更新：2014-12-08 16:09
  * |
  * 标签：[linux](/tag?tagName=linux)

  * [](/album/ed2a5d1f5a9fbe09f6be17ea.html?picindex=1)1

  * [](/album/ed2a5d1f5a9fbe09f6be17ea.html?picindex=2)2

  * [](/album/ed2a5d1f5a9fbe09f6be17ea.html?picindex=3)3

  * [](/album/ed2a5d1f5a9fbe09f6be17ea.html?picindex=4)4

[分步阅读](/album/ed2a5d1f5a9fbe09f6be17ea.html)

公司使用的是linux搭建服务器，linux安装软件能够使用yum安装依赖包是一件非常简单而幸福的事情，所以这里简单介绍一下linux安装yum源流程和操作。

## [](javascript:;)工具/原料

  * 电脑

  * linux基础操作知识

## [](javascript:;)方法/步骤

  1. 1

查看、卸载已安装的yum包

查看已安装的yum包

#rpm –qa|grep yum

卸载软件包

#rpm –e –nodeps yum

  2. 2

下载安装依赖包python python-iniparse

下载地址http://centos.ustc.edu.cn/centos/6.5/os/x86_64/Packages/

http://mirrors.163.com/centos/6/os/x86_64/Packages/

找到对应包如：python-2.6.6-51.el6.x86_64.rpm python-iniparse-0.3.1-2.1.el6.noarch.rpm

源地址可以从网上找一些速度比较快的，自身测试这两个地址速度还不错。包的名字可能跟上面不同，主要是版本和操作系统位数的不同，建议不要在页面搜索全部，如第一个包只搜索python，第二个包搜索python-iniparse。

  3. 3

安装

#rpm –ivh python-2.6.6-51.el6.x86_64.rpm python-iniparse-0.3.1-2.1.el6.noarch.rpm

下载安装yum包

下载地址http://centos.ustc.edu.cn/centos/6.5/os/x86_64/Packages/

http://mirrors.163.com/centos/6/os/x86_64/Packages/

找到对应包如：http://centos.ustc.edu.cn/centos/6.5/os/x86_64/Packages/ yum-plugin-fastestmirror-1.1.30-14.el6.noarch.rpm yum-metadata-parser-1.1.2-16.el6.x86_64.rpm

yum-3.2.29-40.el6.centos.noarch.rpm

#rpm-ivh yum-*

若安装失败可重新输入此命令并加参数--nodeps –force

查找包的方法与步骤二相同，在此不做赘述。

  4. 4

更改yum源

下载配置文件

http://mirrors.163.com/.help/CentOS6-Base-163.repo

将此配置文件替换/etc/yum.repos.d同名文件

编辑配置文件

#cd /etc/yum.repos.d

#vi CentOS-Base.repo

  5. 5

将文件中$releasever改成对应版本（6/6.5）

将源mirrorlist.centos.org改为使用的yum源

centos.ustc.edu.cn

mirrors.163.com

保存配置文件即可

  6. 6

清理yum缓存

#yum clean all

将服务器软件包信息缓存至本地，提高搜索安装效率

#yum makecache

若上面两条命令有报错，一般为配置文件更改不完全，可根据错误信息查找配置文件中更改错误

测试

#yum install vim

完成

END

## [](javascript:;)注意事项

  * 我这里做的是redhat系统yum源配置，不同版本linux可能稍有不同，如配置过程中出现问题，请大家见谅。

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
