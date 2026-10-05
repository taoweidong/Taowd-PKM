---
source: "http://jingyan.baidu.com/article/c33e3f48a3365dea15cbb5c9.html"
title: "JDK环境变量配置－－ubuntu版-百度经验"
fetched_at: "2026-10-05 15:34:43"
---

# JDK环境变量配置－－ubuntu版

  * 原创
  * |
  * 浏览：37192
  * |
  * 更新：2014-04-19 01:03
  * |
  * 标签：[ubuntu](/tag?tagName=ubuntu)

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=1)1

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=2)2

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=3)3

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=4)4

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=5)5

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=6)6

  * [](/album/c33e3f48a3365dea15cbb5c9.html?picindex=7)7

[分步阅读](/album/c33e3f48a3365dea15cbb5c9.html)

ubuntu14.04长期支持已经出来，今天迫不及等地安装上去了。对于学习Java的我，又要重新安装JDK了，今天带着大家一起安装Oracle JDK；

## [](javascript:;)工具/原料

  *  jdk-7u55-linux-x64.tar.gz

  *  ubuntu12.04以上版本

## [](javascript:;)方法/步骤

  1. 1

首先，百度搜索jdk,选择第一个,网站是Oracle Jdk。点击进去

  2. 2

点击Download,到官网下载linux版本的jdk。选择自己对应的操作系统及32或64位版本,这里我下载的是64位版本的jdk-7u55-linux-x64.tar.gz

  3. 3

创建Java的目标路径文件夹，这里我们放在usr/lib/jvm下面。在终端下操作：

$ sudo mkdir /usr/lib/jvm

之后输入你的密码完成创建

  4. 4

解压你下载的jdk压缩文件至你创建的目录，用以下命令。

$ sudo tar -C /usr/lib/jvm -xzf jdk-7u55-linux-x64.tar.gz

注意把你的jdk文件放到你的主页home下，这里我放到"**下载** "的上一个目录

  5. 5

查看jdk文件是否正确安装到你所创建你的文件夹下，并查看文件

  6. 6

查看本机上是否还有java可选。这里用到以下命令

$ sudo update-alternatives --list java

如果出现显示图中错误，系统中没有java可选，我们可以进行以下步骤

  7. 7

配置环境变量命令：

$sudo gedit ~/.bashrc

添加以下代码：

export JAVA_HOME=/usr/lib/jvm/jdk1.7.0_55

export JRE_HOME=${JAVA_HOME}/jre

export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib

export PATH=${JAVA_HOME}/bin:$PATH

  8. 8

查看是否配置成功：java -version

有如图下信息配置成功！

END

## [](javascript:;)注意事项

  * jdk配置还有其他方法，不只此一种

  * 如果你觉得不错，点个赞吧

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
