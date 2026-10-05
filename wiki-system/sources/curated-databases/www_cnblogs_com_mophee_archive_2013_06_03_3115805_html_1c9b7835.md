---
source: "http://www.cnblogs.com/mophee/archive/2013/06/03/3115805.html"
title: "Linux下建立Oracle服务及其开机自启动 - PanpChing - 博客园"
fetched_at: "2026-10-05 15:28:00"
---

说明：以下操作环境在CentOS 6.4 + Oracle 11gR2（Oracle安装在ORACLE_BASE=/opt/oracle中，其ORACLE_HOME=/opt/oracle/11g）

用OUI安装并配置Oracle数据库后，Oracle就开启了(包括：数据库实例、监听器、EM)。在重启操作系统之后，Oracle默认是没有启动的。使用如下命令查看Oracle相关服务是否已启动：


    ps aux | grep ora_ #若无ora_**_**相关的进程，则oracle数据库实例未启动
    netstat -tlnup | grep 1521 #若无任何显示，则监听器未启动
    lsnrctl status #查看监听器状态
    netstat -tlnup | grep 1158 #若无任何显示，则EM未启动
    emctl status dbconsole #查看EM状态

手工启动Oracle实例，可用sqlplus建立一个idle instance，然后再用startup启动，如下：

![](https://images0.cnblogs.com/blog/51034/201306/03164637-2667e391dfac4b148ecf3c27c269c38d.jpg)

数据库实例启动之后，需启动监听器，才能让远程用户建立连接。可使用如下命令启动监听器：


    lsnrctl start

Oracle还提供网页版的管理器，要使用该管理器需启动相关服务，使用如下命令启动：


    emctl start dbconsole

至此，可在web浏览器中输入：https://｛主机IP 或 主机名 或 本地localhost｝:1158/em，打开管理器，使用相关帐号登录进行数据库查看和管理。

如果每次重启操作系统都要进行以上操作好麻烦，那么如何让Oracle作为系统服务在开机的时候自动启动呢？

Oracle在$ORACLE_HOME/bin下提供许多对数据库进行操作的脚本，其中dbstart和dbshut可分别用来启动和关闭数据库。注意，这两个脚本已包含监听器的启动或关闭，但并未对EM进行相关的操作。使用如下命令：


    /opt/oracle/11g/bin/dbstart /opt/oracle/11g #启动数据库实例(包含监听器)
    /opt/oracle/11g/bin/dbshut /opt/oracle/11g #关闭数据库实例(包括监听器)

以上命令要成功启动数据库实例还得打开Oracle设置的一个关卡：vi /etc/oratab，修改行：


    orcl:/opt/oracle/11g:Y #默认为orcl:/opt/oracle/11g:N

以root身份建立开机启动oracle服务的脚本：vi /etc/init.d/oracle，添加如下脚本：


    #!/bin/sh
    #chkconfig: 2345 20 80
    #description: Oracle dbstart / dbshut
    #以上两行为chkconfig所需
    ORA_HOME=/opt/oracle/11g
    ORA_OWNER=oracle
    LOGFILE=/var/log/oracle.log
    echo "#################################" >> ${LOGFILE}
    date +"### %T %a %D: Run Oracle" >> ${LOGFILE}
    if [ ! -f ${ORA_HOME}/bin/dbstart ] || [ ! -f ${ORA_HOME}/bin/dbshut ]; then
        echo "Error: Missing the script file ${ORA_HOME}/bin/dbstart or ${ORA_HOME}/bin/dbshut!" >> ${LOGFILE}
        echo "#################################" >> ${LOGFILE}
        exit
    fi
    start(){
        echo "###Startup Database..."
        su - ${ORA_OWNER} -c "${ORA_HOME}/bin/dbstart ${ORA_HOME}"
        echo "###Done."
        echo "###Run database control..."
        su - ${ORA_OWNER} -c "${ORA_HOME}/bin/emctl start dbconsole"
        echo "###Done."
    }
    stop(){
        echo "###Stop database control..."
        su - ${ORA_OWNER} -c "${ORA_HOME}/bin/emctl stop dbconsole"
        echo "###Done."
        echo "###Shutdown Database..."
        su - ${ORA_OWNER} -c "${ORA_HOME}/bin/dbshut ${ORA_HOME}"
        echo "###Done."
    }
    case "$1" in
        'start')
            start >> ${LOGFILE}
        ;;
        'stop')
            stop >> ${LOGFILE}
        ;;
        'restart')
            stop >> ${LOGFILE}
            start >> ${LOGFILE}
        ;;
    esac
    date +"### %T %a %D: Finished." >> ${LOGFILE}
    echo "#################################" >> ${LOGFILE}
    echo ""

使用如下命令将 /etc/init.d/oracle 置为可执行文件：


    chmod a+x /etc/init.d/oracle

至此，可使用如下命令对oracle进行启动和关闭


    /etc/init.d/oracle start #启动oracle(包括数据库实例、监听器、EM)
    /etc/init.d/oracle stop #关闭oracle
    /etc/init.d/oracle restart #重启oracle

将 oracle 添加到 chkconfig中：


    chkconfig --add oracle

可使用如下命令查看和设置oracle服务的开机启动级别：


    chkconfig | grep oracle #查看oracle服务的开机启动级别
    chkconfig --level 24 oracle off #修改oracle服务的开机启动级别
    chkconfig --level 35 oracle on

至此可使用如下命令对oracle的启动或关闭进行管理


    service oracle start #启动
    service oracle stop #关闭
    service oracle restart #重启

建立连接：


    ln -s /etc/init.d/oracle /etc/rc0.d/K01oracle   #关机执行
    ln -s /etc/init.d/oracle /etc/rc6.d/K01oracle   #重启执行
