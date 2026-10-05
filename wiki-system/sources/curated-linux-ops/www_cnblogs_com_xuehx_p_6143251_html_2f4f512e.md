---
source: "http://www.cnblogs.com/xuehx/p/6143251.html"
title: "linux yum安装jdk - 黄皮书生 - 博客园"
fetched_at: "2026-10-05 15:35:03"
---

>>>>>>>>>>

实例: yum安装jdk

1.查看当前的jdk版本，并卸载

（注1：rpm -qa ###解释：查询所有安装的rpm包

grep jdk ###解释：显示名字中包含字符串"jdk"的包）

yum提供了查找、安装、删除某一个、一组甚至全部软件包的命令.



options：可选，选项包括-h（帮助），-y（当安装过程提示选择全部为"yes"），-q（不显示安装的过程）

command：要进行的操作。

package操作的对象。

yum常用命令

1.列出所有可更新的软件清单命令：yum check-update

2.更新所有软件命令：yum update

3.仅安装指定的软件命令：yum install

4.仅更新指定的软件命令：yum update

5.列出所有可安裝的软件清单命令：yum list

6.删除软件包命令：yum remove

7.查找软件包 命令：yum search <keyword>

8.清除缓存命令:

yum clean packages: 清除缓存目录下的软件包

yum clean headers: 清除缓存目录下的 headers

yum clean oldheaders: 清除缓存目录下旧的 headers

yum clean, yum clean all (= yum clean packages; yum clean oldheaders) :清除缓存目录下的软件包及旧的headers

实例: yum安装jdk

1.查看当前的jdk版本，并卸载

（注1：rpm -qa ###解释：查询所有安装的rpm包

grep jdk ###解释：显示名字中包含字符串"jdk"的包）

2.查找java相关得列表

(yum -y list java)

(注1： yum install java-1.8.0-openjdk.x86_64)

（注2：yum -y install java-1.8.0-openjdk*）

（注： java -version）

通过yum默认安装的路径为

（注：cd /usr/lib/jvm）

将jdk的安装路径加入到JAVA_HOME

（注：vi /etc/profile

. /etc/profile）

以上内容均摘自ppt，侵删致歉。
