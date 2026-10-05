---
source: "http://jingyan.baidu.com/article/9c69d48fb9fd7b13c8024e6b.html"
title: "Ubuntu 14.04远程登录服务器--ssh的安装和配置-百度经验"
fetched_at: "2026-10-05 15:34:55"
---

# Ubuntu 14.04远程登录服务器--ssh的安装和配置

  * 原创
  * |
  * 浏览：112158
  * |
  * 更新：2017-12-22 17:53
  * |
  * 标签：[ubuntu](/tag?tagName=ubuntu)

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=1)1

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=2)2

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=3)3

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=4)4

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=5)5

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=6)6

  * [](/album/9c69d48fb9fd7b13c8024e6b.html?picindex=7)7

[分步阅读](/album/9c69d48fb9fd7b13c8024e6b.html)

ssh是一种安全协议，主要用于给远程登录会话数据进行加密，保证数据传输的安全，现在介绍一下如何在Ubuntu 14.04上安装和配置ssh

## [](javascript:;)工具/原料

  * Ubuntu 14.04

  * putty v0.63

## [](javascript:;)方法/步骤

  1. 1

**更新源列表**

打开"终端窗口"，输入"sudo apt-get update"-->回车-->"输入当前登录用户的管理员密码"-->回车,就可以了。

  2. 2

**安装ssh**

打开"终端窗口"，输入"sudo apt-get install openssh-server"-->回车-->输入"y"-->回车-->安装完成。

  3. 3

**查看ssh服务是否启动**

打开"终端窗口"，输入"sudo ps -e |grep ssh"-->回车-->有sshd,说明ssh服务已经启动，如果没有启动，输入"sudo service ssh start"-->回车-->ssh服务就会启动。

  4. 4

**使用gedit修改配置文件"/etc/ssh/sshd_config"**

打开"终端窗口"，输入"sudo gedit /etc/ssh/sshd_config"-->回车-->把配置文件中的"PermitRootLogin without-password"加一个"#"号,把它注释掉-->再增加一句"PermitRootLogin yes"-->保存，修改成功。

  5. 5

**查看Ubuntu 14.04的IP地址**

打开"终端窗口"，输入"sudo ifconfig"-->回车-->就可以查看到IP地址。

  6. 6

**下载putty v0.63**

在百度中输入"putty"-->回车-->单击第一个查询结果中的"立即下载"-->下载完成后，运行putty-->输入主机的ip地址、会话名称-->保存-->双击"会话名称"打开连接-->输入用户名和密码-->登录成功。

END

## [](javascript:;)注意事项

  * 本操作是在Ubuntu 14.04上完成，其它版本应该差不多，我没有去试

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
