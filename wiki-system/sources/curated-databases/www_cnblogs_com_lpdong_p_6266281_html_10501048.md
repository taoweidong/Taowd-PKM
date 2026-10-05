---
source: "http://www.cnblogs.com/lpdong/p/6266281.html"
title: "linux下的oracle11gR2静默安装，经验分享 - 沛东 - 博客园"
fetched_at: "2026-10-05 15:28:03"
---

说明：

1、我的linux是64位的redhat6.5，安装的oracle版本是11.2.0的。

2、我这是自己安装的linux虚拟机，主机名为ora11g，ip为192.168.100.122

3、这台机器以前没有安装过oracle数据库，这是第一次安装；系统安装好了之后，仅仅只配了ip地址；所以新手完全可以按照我的步骤装一次oracle。

准备工作：

1、确认主机名一致：


    [root@ora11g ~]# vi /etc/hosts

在末尾添加 (#其中192.168.100.123为本机ip地址，ora11g为本机主机名，请根据服务器不同自行更改)


    192.168.100.123    ora11g

2、上传数据库安装压缩包，比如/home/下，并解压，会得到一个database的文件夹。

打系统补丁包

1、建立光盘源

1）查看光盘位置，可以看出/dev/sr0即为系统光盘文件



    [root@ora11g ~]# df -h

提示内容为

Filesystem Size Used Avail Use% Mounted on
/dev/sda3 26G 2.8G 22G 12% /
tmpfs 936M 224K 936M 1% /dev/shm
/dev/sda1 194M 34M 151M 19% /boot
/dev/sr0 3.6G 3.6G 0 100% /media/RHEL_6.5 x86_64 Disc 1

2）、挂载光盘 （挂载点为mnt目录）


    [root@ora11g ~]# mount /dev/sr0 /mnt/

3）、创建本地yum源并编辑


    [root@ora11g ~]# touch /etc/yum.repos.d/redhat.repo

    [root@ora11g ~]# vi /etc/yum.repos.d/redhat.repo

在redhat.repo中添加内容（#后面文字为说明，复制的时候请自行删除）


    [Sever]
    name=redhat6.5           #自定义名称
    baseurl=file:///mnt/     #本地光盘挂载路径
    enabled=1                #启用yum源，0为不启用，1为启用
    gpgcheck=0               #检查GPG-key，0为不启用

4）、把 yum.conf中的gpgcheck改为0


    vi /etc/yum.conf

2、打补丁

rqm -qa | grep compat(补丁包名) 为查看系统是否有这个补丁包

yum install compat(补丁包名) 为安装这个补丁包

1）、redhat6.5版本64位系统所需系统补丁截图

2）、打补丁（根据我系统安装的版本检查完后发现只需要安装以下补丁，这里不在赘述）


      [root@ora11g ~]#yum install compat-libcap*

      [root@ora11g ~]#yum install compat-libstdc++-33*

      [root@ora11g ~]#yum install compat-libstdc++-33*.i686

      [root@ora11g ~]#yum install gcc*

      [root@ora11g ~]#yum install glibc-devel-*.i686

      [root@ora11g ~]#yum install libstdc++-devel*.i686

      [root@ora11g ~]#yum install libaio*.i686

      [root@ora11g ~]#yum install libaio-devel*

      [root@ora11g ~]#yum install unixODBC*

      [root@ora11g ~]#yum install unixODBC*.i686

      [root@ora11g ~]#yum install ksh

(ps:上述的包为我这个系统中没有的补丁包，在安装的时候针对不同系统有不同的情况，请注意。请对照图片中所列的补丁包一一确认，其中(*86_64)与(.i686)为不同的补丁包，i686的需要的后面加上.i686，可以参照上面的写法。)

可以使用下面命令检验补丁包是否打完


    [root@ora11g ~]#rpm -q binutils compat-libcap1 compat-libstdc++-33 gcc gcc-c++ glibc glibc-devel ksh

    [root@ora11g ~]#rpm -q libgcc libstdc++ libstdc++-devel libaio libaio-devel make sysstat unixODBC unixODBC-devel

修改系统文件参数

1、配置linux内核参数


    [root@ora11g ~]# vi /etc/sysctl.conf

注释掉kernel.shmmax与kernel.shmall，并追加以下内容


    kernel.shmmax = 68719476736
    kernel.shmall = 4294967296
    fs.file-max = 6815744
    kernel.shmmni = 4096
    kernel.sem = 250 32000 100 128
    net.ipv4.ip_local_port_range = 9000 65500
    net.core.rmem_default = 262144
    net.core.rmem_max = 4194304
    net.core.wmem_default = 262144
    net.core.wmem_max = 1048586
    fs.aio-max-nr = 1048576

2、配置资源使用情况


    [root@ora11g ~]# vi /etc/security/limits.conf

追加以下内容


    oracle soft nproc 2047
    oracle hard nproc 16384
    oracle soft nofile 1024
    oracle hard nofile 65536
    oracle hard stack 10240

3、登陆设置


    [root@ora11g ~]# vi /etc/pam.d/login

追加以下内容


    session required /lib64/security/pam_limits.so
    session required pam_limits.so


    [root@ora11g ~]# vi /etc/profile

追加以下内容


    if [ $USER = "oracle" ]; then
    if [ $SHELL = "/bin/ksh" ]; then
    ulimit -p 16384
    ulimit -n 65536
    else
    ulimit -u 16384 -n 65536
    fi
    fi

4、关闭selinux ，确保SELINUX=disabled


    [root@ora11g ~]# vi /etc/selinux/config

创建用户、用户组和安装目录

1、创建oinstall和dba组和oracle用户


    [root@ora11g ~]# groupadd oinstall

    [root@ora11g ~]# groupadd dba

    [root@ora11g ~]# useradd -g oinstall -G dba oracle

    [root@ora11g ~]# passwd oracle

    ##之后会输入两次oracle密码

2、创建安装目录并修改所属用户和组


    [root@ora11g ~]# mkdir -p /u01/app/oracle

    [root@ora11g ~]# chown -R oracle:oinstall /u01/app/

修改环境变量

1、切换到oracle用户。


    [root@ora11g ~]# su - oracle

2、修改环境变量


    [oracle@ora11g ~]$ vi .bash_profile

追加以下内容


    export ORACLE_BASE=/u01/app/oracle
    export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1
    export ORACLE_SID=ora11g
    export PATH=$PATH:$HOME/bin:$ORACLE_HOME/bin
    export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib

移动database文件

移动文件并修改权限等


    [root@ora11g ~]# mv /home/database/ /u01/

    [root@ora11g ~]# chown -R oracle:oinstall database/

    [root@ora11g ~]# chmod -R 777 database/

下面才是正菜（静默安装oracle）

1、静默安装oracle软件

1）、编辑响应文件db_install.rsp


    [root@ora11g ~]# vi /u01/database/response/db_install.rsp

需要修改的配置有以下内容（参考大神说明 http://blog.csdn.net/jameshadoop/article/details/48086933）


    oracle.install.option=INSTALL_DB_SWONLY          #选择安装类型：1.只装数据库软件 2.安装数据库软件并建库 3.升级数据库

    ORACLE_HOSTNAME=ora11g                           #指定操作系统主机名，通过hostname命令获得

    UNIX_GROUP_NAME=oinstall                         #指定oracle inventory目录的所有者，通常会是oinstall或者dba

    INVENTORY_LOCATION=/u01/app/oraInventory         #指定产品清单oracle inventory目录的路径

    SELECTED_LANGUAGES=en,zh_CN,zh_TW                #指定数据库语言，可以选择多个，用逗号隔开

    ORACLE_HOME=/u01/app/oracle/product/11.2.0/db_1  #设置ORALCE_HOME的路径

    ORACLE_BASE=/u01/app/oracle                      # 设置ORALCE_BASE的路径

    oracle.install.db.InstallEdition=EE              #选择Oracle安装数据库软件的版本

    oracle.install.db.isCustomInstall=false

    oracle.install.db.DBA_GROUP=dba                  #指定拥有OSDBA、OSOPER权限的用户组，通常会是dba组

    oracle.install.db.OPER_GROUP=oinstall

    oracle.install.db.config.starterdb.type=GENERAL_PURPOSE      #选择数据库的用途，一般用途/事物处理，数据仓库

    oracle.install.db.config.starterdb.globalDBName=ora11g       #指定GlobalName

    oracle.install.db.config.starterdb.SID=ora11g                #指定SID

    oracle.install.db.config.starterdb.characterSet=ZHS16GBK     #选择字符集。不正确的字符集会给数据显示和存储带来麻烦无数。
                                                                 #通常中文选择的有ZHS16GBK简体中文库，根据公司规定自行选择
    oracle.install.db.config.starterdb.password.ALL=123456       #设定所有数据库用户使用同一个密码，其它数据库用户就不用单独设置了。

    DECLINE_SECURITY_UPDATES=true                   # False表示不需要设置安全更新，注意，在11.2的静默安装中疑似有一个BUG
                                                    # Response File中必须指定为true，否则会提示错误,不管是否正确填写了邮件地址

2）、切换到oracle用户进入到/u01/database目录下执行安装命令


    [oracle@ora11g ~]$ cd /u01/database/

    [oracle@ora11g database]$ ./runInstaller -silent -ignorePrereq responseFile /u01/database/response/db_install.rsp

使用root用户使用tail -f 查看实时日志，不赘述。

3）、等到窗口出现以下命令时


    出现类似如下提示表示安装完成：
    #-------------------------------------------------------------------
    ...
    /u01/app/oraInventory/orainstRoot.sh
    /u01/app/oracle/product/11.2.0/db_1/root.sh
    To execute the configuration scripts:
    1. Open a terminal window
    2. Log in as "root"
    3. Run the scripts
    4. Return to this window and hit "Enter" key to continue

    Successfully Setup Software.
    #-------------------------------------------------------------------

新开窗口使用root用户登陆并执行以下命令


    [root@ora11g ~]#  /u01/app/oraInventory/orainstRoot.sh
    [root@ora11g ~]#  /u01/app/oracle/product/11.2.0/db_1/root.sh

oracle软件安装完成。

2、静默安装监听，（ $ORACLE_HOME/bin/netca /silent /responsefile u01/database/response/netca.rsp）


    [oracle@ora11g ~]$ /u01/app/oracle/product/11.2.0/db_1/bin/netca /silent /responseFile /u01/database/response/netca.rsp

3、静默建库

1）、编辑dbca.rsp


    [root@ora11g ~]# vi /u01/database/response/dbca.rsp

修改配置如下


    #以下内容不要修改
    RESPONSEFILE_VERSION = "11.2.0"

    OPERATION_TYPE = "createDatabase"

    #以下内容必须设置

    GDBNAME = "ora11g"

    SID = "ora11g"

    TEMPLATENAME = "General_Purpose.dbc"

    #以下内容根据需要修改

    CHARACTERSET = "ZHS16GBK"

2）、使用oracle用户执行建库命令（注意执行监听的时候是 /silent /responseFile 而执行建库则是 -silent -responseFile）


    [oracle@ora11g ~]$ /u01/app/oracle/product/11.2.0/db_1/bin/dbca -silent -responseFile /u01/database/response/dbca.rsp

之后会提示输入sys和system的密码，我的都是123456，所有输入2次都是一样的。（我这里命令行会先删除界面的内容才可以输入，不知道是不是系统的原因还是别的导致的）

界面会提示安装进度


    Copying database files

    ...

    37% complete

    Creating and starting Oracle instance

    ...

    62% complete

    Completing Database Creation

    ...

    100% complete

    Look at the log file "/u01/app/oracle/cfgtoollogs/dbca/ORCL/ORCL.log" for further details.

之后就完成了数据库的安装。
