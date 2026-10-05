---
source: "http://www.cnblogs.com/donghua2014/p/4274268.html"
title: "Oracle 11G for redhat 自启动脚本 - 奋斗吧~少年 - 博客园"
fetched_at: "2026-10-05 15:28:02"
---

##### 在$ORACLE_HOME/bin中，有dbstart和dbshut这两个脚本，可以使用这两个oracle自带的脚本实现oracle的开机自启动。这个脚本中包含oraclelistener、instance、asm instances的启动，同样dbshut也是起到关闭服务的作用。

方法一：使用/etc/rc.local系统开机启动脚本，启动oracle

配置系统使dbstart和dbshut脚本起作用：

1）、以root编辑/etc/oratab，

orcl:/home/oracle/app/oracle/product/11.2.0/dbhome_1:N 这种格式，

orcl是你的ORACLE_SID，

/home/oracle/app/oracle/product/11.2.0/dbhome_1是ORACLE_HOME，

这里需要把N改为Y，即orcl:/home/oracle/app/oracle/product/11.2.0/dbhome_1:Y。

2）、以oracle编辑$ORACLE_HOME/bin/dbstart，找到其中第78行:ORACLE_HOME_LISTNER=改为你自己的路径，或者可以改成ORACLE_HOME_LISTNER=$ORACLE_HOME

保存脚本，以oracle用户运行dbshut和dbstart看是否能关闭、启动数据库。如果不能，一般是参数设置，根据报错找到对应位置更改。

经过上一步的配置，可以直接用dbstart命令启动数据listener、instance、asm instances，但是还没有启动oracle10g的EM，ORACLE利用web页面管理数据库相当方便，也是10g的一个特色，所以应该一并启动起该服务来。

$ORACLE_HOME/bin/emctl start dbconsole

因此我们可以用rc.local或者redhat服务都可以实现要求的开机启动。下面分别说一下：

1）、利用rc.local。直接把dbstart加到rc.local中，实现开机自动启动。这里需要注意的是必须以oracle启动该脚本。

用root编辑/etc/rc.local，添加下面三行：

su oracle –lc "/home/oracle/app/oracle/product/11.2.0/dbhome_1/bin/lsnrctl start"

su - oracle -c "/home/oracle/app/oracle/product/11.2.0/dbhome_1/bin/dbstart"

su - oracle -c "/u01/product/10.2.0/db_1/bin/emctl start dbconsole"

这里"/home/oracle/app/oracle/product/11.2.0/dbhome_1需要替换成实际的ORACLE_HOME

保存并退出后，reboot服务器测试一下，可以看到，当系统启动以后oracle监听、实例和em都已经起来了

方法二：使用/etc/rc.d/init.d/oracle 自创脚本启动关闭数据库

如果我们不用rc.local，也可以加到redhat服务中。在/etc/rc.d/init.d中添加如下脚本文件，命名为oracle：

#!/bin/sh

#chkconfig: 2345 99 01

#description: ORACLE 10g Server

ORACLE_HOME=/u01/product/10.2.0/db_1

if [ ! -f $ORACLE_HOME/bin/dbstart ]

then

echo "ORACLE cannot start"

exit

fi

case "$1" in

'start')

echo "Starting Oracle Database..."

su - oracle -c "$ORACLE_HOME/bin/dbstart"

su - oracle -c "$ORACLE_HOME/bin/emctl start dbconsole"

;;

'stop')

echo "Stoping Oracle Database"

su - oracle -c "$ORACLE_HOME/bin/emctl stop dbconsole"

su - oracle -c "$ORACLE_HOME/bin/dbshut"

;;

esac

注意其中两行注释，网上很多脚本因为少了这两行不能使服务自启动：

#chkconfig: 2345 99 01

#description: ORACLE 10g Server

其中chkconfig：2345 99 01 是指脚本将为运行级2、3、4、5启动oracle 10g服务，启动优先级为99，关闭优先级为01。

然后以root权限:

# mv oracle /etc/init.d

# chkconfig --add oracle

# chkconfig --list oracle 查看，这样的话就把ORACLE就可以开机启动和关机前shutdown immediate

重启系统，就可以在启动的过程中看到 Starting oracle ，因为我们设置的优先级为99，一般是最后启动。[OK]以后就可以了。因为要启动emctl，可能有点慢，等待的时间要稍微长一点。

启动以后可以以root执行oracle start或者oracle stop来启动或停止服务

总结：我是采用方式一进行实现的，方法二没有经过测试

转载请注明：<http://blog.163.com/nocturnal_ken/blog/static/17802332720111945726777/>
