---
source: "http://jingyan.baidu.com/article/380abd0a77ae041d90192cf4.html"
title: "Linux平台下快速搭建FTP服务器-百度经验"
fetched_at: "2026-10-05 15:35:51"
---

# Linux平台下快速搭建FTP服务器

  * 原创
  * |
  * 浏览：86863
  * |
  * 更新：2018-02-23 03:00
  * |
  * 标签：[linux](/tag?tagName=linux)

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=1)1

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=2)2

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=3)3

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=4)4

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=5)5

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=6)6

  * [](/album/380abd0a77ae041d90192cf4.html?picindex=7)7

[分步阅读](/album/380abd0a77ae041d90192cf4.html)

FTP 是File Transfer Protocol（文件传输协议）的英文简称，而中文简称为“文传协议”。用于Internet上的控制文件的双向传输。同时，它也是一个应用程序（Application）。基于不同的操作系统有不同的FTP应用程序，而所有这些应用程序都遵守同一种协议以传输文件。在FTP的使用当中，用户经常遇到两个概念："下载"（Download）和"上传"（Upload）。

一般在各种linux的发行版中，默认带有的ftp软件是vsftp，从各个linux发行版对vsftp的认可可以看出，vsftp应该是一款不错的ftp软件。

## [](javascript:;)方法/步骤

  * 1、检查安装vsftpd软件

使用如下命令#rpm -qa |grep vsftpd可以检测出是否安装了vsftpd软件，

如果没有安装，使用YUM命令进行安装。

  * 2、启动服务

使用vsftpd软件，主要包括如下几个命令：

启动ftp命令#service vsftpd start

停止ftp命令#service vsftpd stop

重启ftp命令#service vsftpd restart

  * 3、vsftpd的配置

ftp的配置文件主要有三个，位于/etc/vsftpd/目录下，分别是：

ftpusers 该文件用来指定那些用户不能访问ftp服务器。

user_list 该文件用来指示的默认账户在默认情况下也不能访问ftp

vsftpd.conf vsftpd的主配置文件

  * 4、以匿名用户为例，我们去掉配置文件vsftpd.conf 里面以下

anon_upload_enable=YES

anon_mkdir_write_enable=YES

两项前面的#号，就可以完成匿名用户的配置，此时匿名用户既可以登录上传、下载文件。记得修改配置文件后需要重启服务。

  * 5、非匿名账户的创建与使用

vsftpd服务与系统用户是相互关联的，例如我们创建一个名为test 的系统用户，那么此用户在默认配置的情况下就可以实现登录，如图

  * 登录后在页面创建名为“aa”的文件夹，同样我们在服务器test用户 的home目录里也可以看到相同的文件。

END

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
