---
source: "http://jingyan.baidu.com/article/1612d50079cfe5e20f1eee71.html"
title: "linux下安装tomcat，并设置自动启动-百度经验"
fetched_at: "2026-10-05 15:35:04"
---

# linux下安装tomcat，并设置自动启动。

  * 浏览：12515
  * |
  * 更新：2014-01-15 16:17
  * |
  * 标签：[linux](/tag?tagName=linux) [tomcat](/tag?tagName=tomcat)

在linux服务器下，肯定是需要系统启动时自动启动tomcat服务的。

## [](javascript:;)工具/原料

  *  centos6.x

  *  tomcat rpm包

## [](javascript:;)方法/步骤

  1. 1

安装tomcat不管是在windows下还是在linux下都很简单的。一般都是下载免安装版本的。

我们可以在：http://archive.apache.org/dist/tomcat/ 网站下载我们需要的tomcat版本的tar.gz包。

  2. 2

然后我们用：tar -zxvf apache-tomcat-7.0.10.tar.gz,解压tomcat的包。解压后，我们可以用cd命令进入bin文件夹下，执行./startup.sh,启动tomcat。

  3. 3

下面我来介绍怎么在linux系统下设置tomcat自启动。我们都知道，在linux系统下，设置某个服务自启动的话，需要在/etc/rcX.d下挂载，还要在/etc/init.d/下写启动脚本的。

第一补：我们在/etc/init.d/下新建一个文件tomcat（需要在root权限下操作）

vi /etc/init.d/tomcat

写入如下代码：

# tomcat自启动脚本

#!/bin/sh

# chkconfig: 345 99 10

# description: Auto-starts tomcat

# /etc/init.d/tomcatd

# Tomcat auto-start

# Source function library.

#. /etc/init.d/functions

# source networking configuration.

#. /etc/sysconfig/network

RETVAL=0

export JDK_HOME=/usr/java/jdk1.7.0_45 （请填写真实的JDK目录）

export CATALINA_HOME=/home/ldatum/usr/apache-tomcat-7.0.10（请填写真实的tomcat目录）

export CATALINA_BASE=/home/ldatum/usr/apache-tomcat-7.0.10（请填写真实的tomcat目录）

start()

{

if [ -f $CATALINA_HOME/bin/startup.sh ];

then

echo $"Starting Tomcat"

$CATALINA_HOME/bin/startup.sh

RETVAL=$?

echo " OK"

return $RETVAL

fi

}

stop()

{

if [ -f $CATALINA_HOME/bin/shutdown.sh ];

then

echo $"Stopping Tomcat"

$CATALINA_HOME/bin/shutdown.sh

RETVAL=$?

sleep 1

ps -fwwu tomcat | grep apache-tomcat|grep -v grep | grep -v PID | awk '{print $2}'|xargs kill -9

echo " OK"

# [ $RETVAL -eq 0 ] && rm -f /var/lock/...

return $RETVAL

fi

}

case "$1" in

start)

start

;;

stop)

stop

;;

restart)

echo $"Restaring Tomcat"

$0 stop

sleep 1

$0 start

;;

*)

echo $"Usage: $0 {start|stop|restart}"

exit 1

;;

esac

exit $RETVAL

  4. 4

添加完毕之后，给其增加可执行权限： _chmod +x /etc/init.d/tomcat._

  5. 5

之后就是将这个shell文件的link连到/etc/rc2.d/目录下。linux的/etc/rcX.d/目录中的数字代表开机启动时不同的run level，也就是启动的顺序，Ubuntu9.10下有0-5六个level，不能随便连到其他目录下，可能在那个目录中的程序启动时Tomcat所需要的一些库尚未被加载，用ln命令将tomcat的链接链过去： _ln -s /etc/init.d/tomcat_ _/etc/rc2.d/S16Tomcat_ 。rcX.d目录下的命名规则是很有讲究的，更具不同需要可能是S开头，也可能是K开头，之后的数字代表他们的启动顺序，详细看各自目录下的Readme文件。

  6. 6

接下来就是把这个脚本设置成系统启动时自动执行，系统关闭时自动停止，使用如下命令： _chkconfig ——add tomcat_ 。如果 _chkconfig_ 没有安装，则使用 _apt-get_ 或者 _yum_ 之类的程序进行安装，一般服务器版本的Linux都已经自带了。

  7. 7

最后，就是 _reboot_ 重启系统了。重启之后就会发现，你的Tomcat已经成功运行了。

END

## [](javascript:;)注意事项

  * 在root权限下执行以上所有命令

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

展开阅读全部 __
