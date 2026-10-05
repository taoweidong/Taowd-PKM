---
source: "http://blog.csdn.net/baiyinqiqi/article/details/46468113"
title: "Redhat6.4静默安装Oracle11g_redhat6.4 oracle11g 依赖包 下载-CSDN博客"
fetched_at: "2026-10-05 15:27:55"
---

Linux 版本：Red Hat Enterprise Linux Server release 6.4 (Santiago)

Oracle版本：Oracle Database 11g Release 2 (11.2.0.1.0) for Linux x86-64

在Linux上安装oracle可以使用窗口模式，如果有x-window的话直接在安装服务器上操作很方便，但是如果需要从远程登录就很麻烦了。你可能需要设置display环境变量到本地，或者你可以使用vnc之类的工具远程到linux服务器，无形中增加了复杂度与工作量。关于这种方式，可以参考网上的帖子，很多。

这里我们介绍oracle的静默安装方式。相比而言，我更喜欢这种方式，操作简便，不需要x-window或者vnc等额外工具，效率更高。

oracle11g for Linux x86_64 官方下载地址：

http://download.oracle.com/otn/linux/oracle11g/R2/linux.x64_11gR2_database_1of2.zip

http://download.oracle.com/otn/linux/oracle11g/R2/linux.x64_11gR2_database_2of2.zip  


下载完成后在服务器直接解压，会解压到统一个目录database

1、安装环境检查

内存1G以上：more /proc/meminfo | grep MemTotal  


虚拟内存要求：more /proc/meminfo | grep SwapTotal  
物理内存4-8G，要求虚拟内存为2倍物理内存；  
物理内存8-32G，要求虚拟内存为1.5倍物理内存；  
物理内存32G，要求虚拟内存为32G；  


/tmp目录下需至少1G空间：df -h /tmp   
如果不足1G需设置oracle用户的TMP和TMPDIR环境变量。   
对数据库安装目录，需至少4.35G空间，对数据文件目录，需至少1.68G空间。  


  


内核版本最低2.6.18：uname -r

  


依赖的包:

binutils-2.20.51.0.2-5.36.el6.x86_64  
compat-libstdc++-296-2.96-144.el6.i686  
compat-libstdc++-33-3.2.3-69.el6.x86_64  
elfutils-libelf-devel-0.152-1.el6.x86_64  
elfutils-libelf-0.152-1.el6.x86_64  
gcc-4.4.7-3.el6.x86_64  
glibc-headers-2.12-1.107.el6.x86_64  
compat-glibc-headers-2.5-46.2.x86_64  
glibc-common-2.12-1.107.el6.x86_64  
glibc-2.12-1.107.el6.i686  
compat-glibc-2.5-46.2.x86_64  
glibc-2.12-1.107.el6.x86_64  
glibc-devel-2.12-1.107.el6.x86_64  
ksh-20060214  
libaio-0.3.107-10.el6.x86_64  
libgcc-4.4.7-3.el6.x86_64  
libgcc-4.4.7-3.el6.i686  
libstdc++-4.4.7-3.el6.x86_64  
make-3.81-20.el6.x86_64  
numactl-2.0.7-6.el6.x86_64  
sysstat-9.0.4-20.el6.x86_64  
unixODBC-devel-2.2.14-12.el6_3.x86_64  
unixODBC-2.2.14-12.el6_3.x86_64  
elfutils-libelf-0.152-1.el6.x86_64  
kernel-headers-2.6.32-358.el6.x86_64  
libgomp-4.4.7-3.el6.x86_64  


检查命令:rpm -qa | grep name

若没有安装的话，在Linux镜像文件中会有Packages文件夹，在这里基本都能找到，尽量不要在网上下载，版本不同会导致依赖包的版本也必须变更。

2、系统内核参数修改

vi /etc/sysctl.conf

kernel.shmall = 268435456  
kernel.shmmni = 4096  
kernel.sem = 250 32000 100 128  
net.ipv4.ip_local_port_range = 1024 65000  
net.core.rmem_default = 4194304  
net.core.rmem_max = 4194304  
net.core.wmem_default = 262144  
net.core.wmem_max = 262144  
fs.aio-max-nr = 1048576  
fs.file-max = 6815744   


修改后使用命令sysctl -p应用设置

3、创建组与用户并修改用户权限

groupadd oinstall

groupadd dba

useradd oracle -g oinstall -G dba -b /oracle -p 密码

修改用户权限:

vi /etc/security/limits.conf

oracle soft nofile 65536  
oracle hard nofile 65536  
oracle soft nproc 16384  
oracle hard nproc 16384  


  


vi /etc/pam.d/login  
session required /lib/security/pam_limits.so  
session required pam_limits.so  


  


vi /etc/profile

if [ $USER = "oracle" ]; then  
if [ $SHELL = "/bin/ksh" ]; then  
ulimit -p 16384  
ulimit -n 65536  
else  
ulimit -u 16384 -n 65536  
fi  
fi  


4、创建安装目录

mkdir -p /home/oracle/oraInventory  
chown -R oracle:oinstall /home/  
chmod -R 775 /home/  


5、设置oracle用户环境变量

vi /oracle/.bash_profile

export ORACLE_BASE=/home/oracle

export ORACLE_SID=orabi

除了ORACLE_BASE与ORACLE_SID外，在/oracle/.bash_profile与/etc/profile中不设置任何其它的环境变量

6、创建oraInst.loc并修改所有者

vi /etc/oraInst.loc  


inst_group=oinstall  
inventory_loc=/home/oracle/oraInventory

chown -R oracle:oinstall /etc/oraInst.loc

7、配置响应文件

首先修改安装文件目录的所有者：

chown -R oracle:oinstall /database

切换到oracle用户:

su -l oracle

cp /install/database/response/* /home/oracle/

仅安装oracle软件的响应文件：

vi /home/oracle/db_install.rsp

oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v11_2_0  
oracle.install.option=INSTALL_DB_SWONLY  
ORACLE_HOSTNAME=localhost.iareport  
UNIX_GROUP_NAME=oinstall  
INVENTORY_LOCATION=/home/oracle/oraInventory  
SELECTED_LANGUAGES=en,zh_CN,zh_TW  
ORACLE_HOME=/home/oracle/product/11.2.0/db_1  
ORACLE_BASE=/home/oracle  
oracle.install.db.InstallEdition=EE  
oracle.install.db.isCustomInstall=false  
oracle.install.db.DBA_GROUP=dba  
oracle.install.db.OPER_GROUP=dba  
DECLINE_SECURITY_UPDATES=true  


创建数据库的响应文件：

vi /home/oracle/dbca.rsp

[GENERAL]  
RESPONSEFILE_VERSION = "11.2.0"  
OPERATION_TYPE = "createDatabase"  
[CREATEDATABASE]  
GDBNAME = "orabi"  
SID = "orabi"  
TEMPLATENAME = "General_Purpose.dbc"  
DATAFILEDESTINATION = "/home/oracle/oradata"  
RECOVERYAREADESTINATION= "/home/oracle/flash_recovery_area"  
CHARACTERSET = "AL32UTF8"  
NATIONALCHARACTERSET= "UTF8"  


net响应文件使用系统默认即可：netca.rsp

8、安装数据库

安装数据库软件：

oracle用户，进入database目录执行以下命令

./runInstaller -silent -debug -force -responseFile /home/oracle/db_install.rsp  


出现以下提示表示安装成功，当然有可能是英文的：

以下配置脚本需要以 "root" 用户的身份执行。  
#!/bin/sh   
#要运行的 Root 脚本

/home/oracle/product/11.2.0/db_1/root.sh  
要执行配置脚本, 请执行以下操作:  
1\. 打开一个终端窗口  
2\. 以 "root" 身份登录  
3\. 运行脚本  
4\. 返回此窗口并按 "Enter" 键继续

Successfully Setup Software.  


  


root执行$ORACLE_HOME下的root.sh来建立oratab,dbhome,oraenv,coraenv文件, 如果提示则一直回车:  
su - root  
/home/oracle/product/11.2.0/db_1/root.sh  
more /etc/oratab  


  


设置oracle用户环境变量：

export ORACLE_BASE=/home/oracle  
export ORACLE_SID=orabi

  
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1  
export TNS_ADMIN=$ORACLE_HOME/network/admin  
export PATH=.:${PATH}:$HOME/bin:$ORACLE_HOME/bin  
export PATH=${PATH}:/usr/bin:/bin:/usr/bin/X11:/usr/local/bin  
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$ORACLE_HOME/lib  
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$ORACLE_HOME/oracm/lib  
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/lib:/usr/lib:/usr/local/lib  
export CLASSPATH=${CLASSPATH}:$ORACLE_HOME/JRE  
export CLASSPATH=${CLASSPATH}:$ORACLE_HOME/JRE/lib  
export CLASSPATH=${CLASSPATH}:$ORACLE_HOME/jlib  
export CLASSPATH=${CLASSPATH}:$ORACLE_HOME/rdbms/jlib  
export CLASSPATH=${CLASSPATH}:$ORACLE_HOME/network/jlib  
export LIBPATH=${CLASSPATH}:$ORACLE_HOME/lib:$ORACLE_HOME/ctx/lib  
export ORACLE_OWNER=oracle  
export SPFILE_PATH=$ORACLE_HOME/dbs  
export ORA_NLS10=$ORACLE_HOME/nls/data  


  


source /oracle/.bash_profile

  


sqlplus /nolog 测试登录

9、安装网络配置

su -l oracle  


$ORACLE_HOME/bin/netca /silent /responseFile /home/oracle/netca.rsp  


10、静默创建数据库

$ORACLE_HOME/bin/dbca -silent -responseFile /home/oracle/dbca.rsp  


安装期间查看日志信息了解进度:  
$ tail -100f $ORACLE_BASE/cfgtoollogs/dbca/$ORACLE_SID/$ORACLE_SID.log  
  
建库后实例检查  
$ ps -ef | grep ora_ | grep -v grep | wc -l  
$ ps -ef | grep ora_ | grep -v grep  
  
建库后监听检查  
$ lsnrctl status  
  
如果使用归档日志  
$ sqlplus / as sysdba  
SQL> shutdown immediate;  
SQL> startup mount;  
SQL> alter database archivelog;  
SQL> alter database flashback on; (如果要启用数据库闪回功能则执行)  
SQL> alter database open;  
SQL> execute utl_recomp.recomp_serial(); (重新编译所有可能失效对象)  
SQL> alter system archive log current; (手工归档测试)  
  
默认安装的数据库用户检查  
SQL> set lines 256 pages 500  
SQL> select USER_ID,USERNAME,ACCOUNT_STATUS,DEFAULT_TABLESPACE from dba_users order by 1;  


  


参考：http://blog.sina.com.cn/s/blog_6b7ae4270101ns2v.html

  


  


  
  
  
  
  
  
  


  

