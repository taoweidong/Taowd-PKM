---
source: "http://jingyan.baidu.com/article/e4d08ffd89cc130fd2f60d15.html"
title: "xshell连接虚拟机下创建的linux-百度经验"
fetched_at: "2026-10-05 15:35:47"
---

# xshell连接虚拟机下创建的linux

  * 浏览：10746
  * |
  * 更新：2015-12-01 13:38
  * |
  * 标签：[linux](/tag?tagName=linux) [虚拟机](/tag?tagName=%E8%99%9A%E6%8B%9F%E6%9C%BA) [连接](/tag?tagName=%E8%BF%9E%E6%8E%A5)

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=1)1

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=2)2

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=3)3

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=4)4

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=5)5

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=6)6

  * [](/album/e4d08ffd89cc130fd2f60d15.html?picindex=7)7

[分步阅读](/album/e4d08ffd89cc130fd2f60d15.html)

Xshell 是一个强大的安全终端模拟软件，它支持SSH1, SSH2, 以及Microsoft Windows 平台的TELNET 协议。Xshell 通过互联网到远程主机的安全连接以及它创新性的设计和特色帮助用户在复杂的网络环境中享受他们的工作。

Xshell可以在Windows界面下用来访问远端不同系统下的服务器，从而比较好的达到远程控制终端的目的。

## [](javascript:;)工具/原料

  * linux虚拟机

  * xshell

## [](javascript:;)方法/步骤

  1. 1

1 打开虚拟机，设置linux虚拟机为 仅主机 模式。

2 编辑linux的网卡配置文件 /etc/sysconfig/network-scripts/ifcfg-eth0（redhat6和7版本配置文件不一样，以6为例）

3 为虚拟机配置一个ip（ip不做固定要求）（注意重启网卡服务：service network restart）

  2. 2

1 打开真实机的网络配置

2 找到vmnet1的连接，右键-属性

3 双击 版本协议4 （tcp/ipv4）

4 设置静态ip地址 ，地址要和虚拟机的ip地址为同一网段

  3. 3

1 打开xshell客户端

2 右上角 文件-新建

3 主机栏里填入linux虚拟机的ip地址，其他按需求填写

4 右上角 文件-打开-选择我们创建的会话。点击 连接 。

  4. 4

1 等待弹出对话框，用户名中填入linux虚拟机中创建的用户（可以选保存用户名，方便下次使用） 点击 确定

2 在密码栏里输入你选择用户的密码（同样可以选择保存）

3 点击确定，等待连接。

  5. 5

也可以通过命令连接：ssh （要连接的虚拟机ip地址）

END

## [](javascript:;)注意事项

  * linux服务器配置完ip地址后记着重启服务

  * 连接时，保证虚拟机的开启

  * 保证vmnet1的开启状态

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

展开阅读全部 __
