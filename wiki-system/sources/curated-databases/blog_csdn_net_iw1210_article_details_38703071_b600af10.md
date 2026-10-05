---
source: "http://blog.csdn.net/iw1210/article/details/38703071"
title: "Oracle静默安装文件 db_install.rsp 详解_oracle21 db.rsp-CSDN博客"
fetched_at: "2026-10-05 15:27:53"
---

Oracle静默安装文件 db_install.rsp 详解

（ 转自：<http://blog.chinaunix.net/uid-23886490-id-3565908.html> ）



相关阅读：《 [ 静默安装Oracle](http://blog.csdn.net/iw1210/article/details/10277145) 》



附录A：db_install.rsp 文件详解

####################################################################

## Copyright(c) Oracle Corporation1998,2008. Allrightsreserved. ##

## Specify values for the variables listedbelow tocustomize your installation. ##

## Each variable is associated with acomment. Thecomment ##

## can help to populate the variables withtheappropriate values. ##

## IMPORTANT NOTE: This file contains plaintextpasswords and ##

## should be secured to have readpermission onlyby oracle user ##

## or db administrator who ownsthisinstallation. ##

##**对整个文件的说明，该文件包含参数说明，静默文件中密码信息的保密 ##**

####################################################################

#------------------------------------------------------------------------------

# Do not change the following systemgeneratedvalue. **标注响应文件版本，这个版本必须和要 安装的数据库版本相同，安装检验无法通过,不能更改**

#------------------------------------------------------------------------------

oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v11_2_0

#------------------------------------------------------------------------------

# Specify the installation option.

# It can be one of the following:

# 1. INSTALL_DB_SWONLY

# 2. INSTALL_DB_AND_CONFIG

# 3. UPGRADE_DB

#**选择安装类型： 1. 只装数据库软件 2. 安装数据库软件并建库 3. 升级数据库**

#-------------------------------------------------------------------------------

oracle.install.option=INSTALL_DB_SWONLY

#-------------------------------------------------------------------------------

# Specify the hostname of the system as setduringthe install. It can be used

# to force the installation to use analternativehostname rather than using the

# first hostname found on the system.(e.g., forsystems with multiple hostnames

# and network interfaces)**指定操作系统主机名，通过 hostname命令获得**

#-------------------------------------------------------------------------------

ORACLE_HOSTNAME=ora11gr2

#-------------------------------------------------------------------------------

# Specify the Unix group to be set fortheinventory directory.

#**指定 oracleinventory目录的所有者，通常会是oinstall或者dba**

#-------------------------------------------------------------------------------

UNIX_GROUP_NAME=oinstall

#-------------------------------------------------------------------------------

# Specify the location which holds theinventoryfiles.

#**指定产品清单 oracleinventory目录的路径,如果是Win平台下可以省略**

#-------------------------------------------------------------------------------

INVENTORY_LOCATION=/u01/app/oracle/oraInventory

#-------------------------------------------------------------------------------

# Specify the languages in which thecomponentswill be installed.

# en :English ja :Japanese

# fr :French ko :Korean

# ar :Arabic es : Latin AmericanSpanish

# bn :Bengali lv :Latvian

# pt_BR: BrazilianPortuguese lt :Lithuanian

# bg :Bulgarian ms :Malay

# fr_CA: CanadianFrench es_MX: MexicanSpanish

# ca :Catalan no :Norwegian

# hr :Croatian pl :Polish

# cs :Czech pt :Portuguese

# da :Danish ro :Romanian

# nl :Dutch ru :Russian

# ar_EG:Egyptian zh_CN: SimplifiedChinese

# en_GB: English (Great Britain) sk :Slovak

# et :Estonian sl :Slovenian

# fi :Finnish es_ES:Spanish

# de :German sv :Swedish

# el :Greek th :Thai

# iw :Hebrew zh_TW:TraditionalChinese

# hu :Hungarian tr :Turkish

# is :Icelandic uk :Ukrainian

# in :Indonesian vi :Vietnamese

# it :Italian

# Example : SELECTED_LANGUAGES=en,fr,ja

#**指定数据库语言，可以选择多个，用逗号隔开。选择 en,zh_CN(英文和简体中文)**

#------------------------------------------------------------------------------

SELECTED_LANGUAGES=en,zh_CN

#------------------------------------------------------------------------------

# Specify the complete path of theOracleHome.**设置 ORALCE_HOME的路径**

#------------------------------------------------------------------------------

ORACLE_HOME=/u01/app/oracle/product/11.2.0/db_1

#------------------------------------------------------------------------------

# Specify the complete path of theOracleBase. **设置 ORALCE_BASE的路径**

#------------------------------------------------------------------------------

ORACLE_BASE=/u01/app/oracle

#------------------------------------------------------------------------------

# Specify the installation edition ofthecomponent.

# The value should contain only one ofthesechoices.

#EE :EnterpriseEdition

#SE :StandardEdition

# SEONE Standard EditionOne

#PE :Personal Edition (WINDOWS ONLY)

#**选择 Oracle安装数据库软件的版本（企业版，标准版，标准版1），不同的版本功能不同**

#**详细的版本区别参考附录 D**

#------------------------------------------------------------------------------

oracle.install.db.InstallEdition=EE

#------------------------------------------------------------------------------

# This variable is used to enable ordisable custominstall.

# true : Components mentioned aspart of 'customComponents' property

#are considered for install.

# false : Value for 'customComponents' isnotconsidered.

#**是否自定义 Oracle的组件，如果选择false，则会使用默认的组件**

#**如果选择 true需要自己在下面一条参数将要安装的组件一一列出。**

#**安装相应版权后会安装所有的组件，后期如果缺乏某个组件，再次安装会非常的麻烦。**

#------------------------------------------------------------------------------

oracle.install.db.isCustomInstall=true

#------------------------------------------------------------------------------

# This variable is considered onlyif'IsCustomInstall' is set to true.

# Description: List of Enterprise EditionOptionsyou would like to install.

# The following choices areavailable. You may specify any

# combination of thesechoices. The components youchooseshould

# be specified in theform"internal-component-name:version"

# Below is a list of components youmay specify to install.

# oracle.rdbms.partitioning:11.2.0.1.0- OraclePartitioning

# oracle.rdbms.dm:11.2.0.1.0- Oracle Data Mining

# oracle.rdbms.dv:11.2.0.1.0- Oracle Database Vault

# oracle.rdbms.lbac:11.2.0.1.0- Oracle Label Security

# oracle.rdbms.rat:11.2.0.1.0- Oracle Real ApplicationTesting

# oracle.oraolap:11.2.0.1.0- Oracle OLAP

# **oracle.install.db.isCustomInstall=true 的话必须手工选择需要安装组件的话**

#------------------------------------------------------------------------------

oracle.install.db.customComponents=oracle.server:11.2.0.1.0,oracle.sysman.ccr:10.2.7.0.0,oracle.xdk:11.2.0.1.0,oracle.rdbms.oci:11.2.0.1.0,oracle.network:11.2.0.1.0,oracle.network.listener:11.2.0.1.0,oracle.rdbms:11.2.0.1.0,oracle.options:11.2.0.1.0,oracle.rdbms.partitioning:11.2.0.1.0,oracle.oraolap:11.2.0.1.0,oracle.rdbms.dm:11.2.0.1.0,oracle.rdbms.dv:11.2.0.1.0,orcle.rdbms.lbac:11.2.0.1.0,oracle.rdbms.rat:11.2.0.1.0

###############################################################################

# PRIVILEGED OPERATING SYSTEMGROUPS

# Provide values for the OS groups to whichOSDBAand OSOPERprivileges #

# needs to be granted. If the install isbeingperformed as a member ofthe #

# group "dba", then that will beused unlessspecified otherwisebelow. #

#**指定拥有 OSDBA、OSOPER权限的用户组，通常会是 dba 组**

###############################################################################

#------------------------------------------------------------------------------

# The DBA_GROUP is the OS group which is tobegranted OSDBA privileges.

#------------------------------------------------------------------------------

oracle.install.db.DBA_GROUP=dba

#------------------------------------------------------------------------------

# The OPER_GROUP is the OS group which isto begranted OSOPER privileges.

#------------------------------------------------------------------------------

oracle.install.db.OPER_GROUP=oinstall

#------------------------------------------------------------------------------

# Specify the cluster node names selectedduringthe installation.

#**如果是 RAC 的安装，在这里指定所有的节点**

#------------------------------------------------------------------------------

oracle.install.db.CLUSTER_NODES=

#------------------------------------------------------------------------------

# Specify the type of database tocreate.

# It can be one of the following:

# -GENERAL_PURPOSE/TRANSACTION_PROCESSING

# -DATA_WAREHOUSE

#**选择数据库的用途，一般用途 /事物处理，数据仓库**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.type=GENERAL_PURPOSE

#------------------------------------------------------------------------------

# Specify the Starter Database GlobalDatabaseName. **指定 GlobalName**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.globalDBName=ora11g

#------------------------------------------------------------------------------

# Specify the Starter DatabaseSID.**指定 SID**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.SID=ora11g

#------------------------------------------------------------------------------

# Specify the Starter Databasecharacterset.

# It can be one of the following:

# AL32UTF8, WE8ISO8859P15,WE8MSWIN1252,EE8ISO8859P2,

# EE8MSWIN1250, NE8ISO8859P10,NEE8ISO8859P4,BLT8MSWIN1257,

# BLT8ISO8859P13, CL8ISO8859P5,CL8MSWIN1251,AR8ISO8859P6,

# AR8MSWIN1256, EL8ISO8859P7,EL8MSWIN1253,IW8ISO8859P8,

# IW8MSWIN1255, JA16EUC, JA16EUCTILDE,JA16SJIS,JA16SJISTILDE,

# KO16MSWIN949, ZHS16GBK, TH8TISASCII,ZHT32EUC,ZHT16MSWIN950,

# ZHT16HKSCS, WE8ISO8859P9,TR8MSWIN1254,VN8MSWIN1258

#**选择字符集。不正确的字符集会给数据显示和存储带来麻烦无数。**

#**通常中文选择的有 ZHS16GBK 简体中文库，建议选择unicode 的 AL32UTF8 国际字符集**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.characterSet=AL32UTF8

#------------------------------------------------------------------------------

# This variable should be set to true ifAutomaticMemory Management

# in Database is desired.

# If Automatic Memory Management is notdesired,and memory allocation

# is to be done manually, then set ittofalse.

#**11g 的新特性自动内存管理，也就是 SGA_TARGET 和 PAG_AGGREGATE_TARGET 都****不用设置了， Oracle 会自动调配两部分大小。**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.memoryOption=true

#------------------------------------------------------------------------------

# Specify the total memory allocation forthedatabase. Value(in MB) should be

# at least 256 MB, and should not exceedthe totalphysical memory available on the system.

#Example:oracle.install.db.config.starterdb.memoryLimit=512

#**指定 Oracle 自动管理内存的大小，最小是256MB**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.memoryLimit=

#------------------------------------------------------------------------------

# This variable controls whether to loadExampleSchemas onto the starter

# database or not.**是否载入模板示例**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.installExampleSchemas=false

#------------------------------------------------------------------------------

# This variable includes enabling auditsettings,configuring password profiles

# and revoking some grants to public.Thesesettings are provided by default.

# These settings may also bedisabled. **是否启用安全设置**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.enableSecuritySettings=true

###############################################################################

# Passwords can be supplied for thefollowing fourschemas in the #

# starterdatabase: #

# SYS #

# SYSTEM #

# SYSMAN (usedby EnterpriseManager) #

# DBSNMP (usedby EnterpriseManager) #

# Same password can be used for allaccounts (notrecommended) #

# or different passwords for each accountcan beprovided (recommended) #

#**设置数据库用户密码**

###############################################################################

#------------------------------------------------------------------------------

# This variable holds the password that isto beused for all schemas in the

# starter database.

#**设定所有数据库用户使用同一个密码，其它数据库用户就不用单独设置了。**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.ALL=oracle

#-------------------------------------------------------------------------------

# Specify the SYS password for thestarterdatabase.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.SYS=

#-------------------------------------------------------------------------------

# Specify the SYSTEM password for thestarterdatabase.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.SYSTEM=

#-------------------------------------------------------------------------------

# Specify the SYSMAN password for thestarterdatabase.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.SYSMAN=

#-------------------------------------------------------------------------------

# Specify the DBSNMP password for thestarterdatabase.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.DBSNMP=

#-------------------------------------------------------------------------------

# Specify the management option to beselected forthe starter database.

# It can be one of the following:

# 1. GRID_CONTROL

# 2. DB_CONTROL

#**数据库本地管理工具 DB_CONTROL，远程集中管理工具 GRID_CONTROL**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.control=DB_CONTROL

#-------------------------------------------------------------------------------

# Specify the Management Service to use ifGridControl is selected to manage

# the database. **GRID_CONTROL 需要设定 gridcontrol 的远程路径 URL**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.gridcontrol.gridControlServiceURL=

#-------------------------------------------------------------------------------

# This variable indicates whether toreceive emailnotification for critical

# alerts when using DBcontrol.**是否启用 Email 通知, 启用后会将告警等信息发送到指定邮箱**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.dbcontrol.enableEmailNotification=false

#-------------------------------------------------------------------------------

# Specify the email address to whichthenotifications are to be sent.**设置通知 EMAIL 地址**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.dbcontrol.emailAddress=

#-------------------------------------------------------------------------------

# Specify the SMTP server used foremailnotifications.**设置 EMAIL 邮件服务器**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.dbcontrol.SMTPServer=

###############################################################################

# SPECIFY BACKUP AND RECOVERYOPTIONS #

# Out-of-box backup and recovery optionsfor thedatabase can bementioned #

# using the entriesbelow. #

#**安全及恢复设置（默认值即可） out-of-box（out-of-boxexperience）缩写为 OOBE**

#**产品给用产品给用户良好第一印象和使用感受**

###############################################################################

#------------------------------------------------------------------------------

# This variable is to be set to false ifautomatedbackup is not required. Else

# this can be set to true.**设置自动备份，和 OUI里的自动备份一样。**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.automatedBackup.enable=false

#------------------------------------------------------------------------------

# Regardless of the type of storage that ischosenfor backup and recovery, if

# automated backups are enabled, a job willbescheduled to run daily at

# 2:00 AM to backup the database. This jobwill runas the operating system

# user that is specified in thisvariable.**自动备份会启动一个 job，指定启动 JOB 的系统用户ID**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.automatedBackup.osuid=

#-------------------------------------------------------------------------------

# Regardless of the type of storage that ischosenfor backup and recovery, if

# automated backups are enabled, a job willbescheduled to run daily at

# 2:00 AM to backup the database. This jobwill runas the operating system user

# specified by the above entry. Thefollowing entrystores the password for the

# above operating systemuser.**自动备份会开启一个 job，需要指定 OSUser的密码**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.automatedBackup.ospwd=

#-------------------------------------------------------------------------------

# Specify the type of storage to use forthedatabase.

# It can be one of the following:

# - FILE_SYSTEM_STORAGE

# - ASM_STORAGE

#**自动备份，要求指定使用的文件系统存放数据库文件还是 ASM**

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.storageType=

#-------------------------------------------------------------------------------

# Specify the database file location whichis adirectory for datafiles, control

# files, redologs.

# Applicable only whenoracle.install.db.config.starterdb.storage=FILE_SYSTEM

#**使用文件系统存放数据库文件才需要指定数据文件、控制文件、 Redolog 的存放目录**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.fileSystemStorage.dataLocation=

#-------------------------------------------------------------------------------

# Specify the backup and recoverylocation.

# Applicable onlywhenoracle.install.db.config.starterdb.storage=FILE_SYSTEM

#**使用文件系统存放数据库文件才需要指定备份恢复目录**

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.fileSystemStorage.recoveryLocation=

#-------------------------------------------------------------------------------

# Specify the existing ASM disk groups tobe usedfor storage.

# Applicable onlywhenoracle.install.db.config.starterdb.storage=ASM

#**使用 ASM存放数据库文件才需要指定存放的磁盘组**

#-------------------------------------------------------------------------------

oracle.install.db.config.asm.diskGroup=

#-------------------------------------------------------------------------------

# Specify the password for ASMSNMP user ofthe ASMinstance.

# Applicable onlywhenoracle.install.db.config.starterdb.storage=ASM_SYSTEM

#**使用 ASM 存放数据库文件才需要指定ASM实例密码**

#-------------------------------------------------------------------------------

oracle.install.db.config.asm.ASMSNMPPassword=

#------------------------------------------------------------------------------

# Specify the My Oracle SupportAccountUsername.

# Example :MYORACLESUPPORT_USERNAME=metalink

#**指定 metalink账户用户名**

#------------------------------------------------------------------------------

MYORACLESUPPORT_USERNAME=

#------------------------------------------------------------------------------

# Specify the My Oracle Support AccountUsernamepassword.

#Example :MYORACLESUPPORT_PASSWORD=password

# **指定 metalink 账户密码**

#------------------------------------------------------------------------------

MYORACLESUPPORT_PASSWORD=

#------------------------------------------------------------------------------

# Specify whether to enable the user to setthepassword for

# My Oracle Support credentials. The valuecan beeither true or false.

# If left blank it will be assumed tobefalse.

#Example :SECURITY_UPDATES_VIA_MYORACLESUPPORT=true

# **用户是否可以设置 metalink 密码**

#------------------------------------------------------------------------------

SECURITY_UPDATES_VIA_MYORACLESUPPORT=

#------------------------------------------------------------------------------

# Specify whether user wants to give anyproxydetails for connection.

# The value can be either true or false. Ifleftblank it will be assumed to be false.

#Example :DECLINE_SECURITY_UPDATES=false

# **False 表示不需要设置安全更新，注意，在11.2的静默安装中疑似有一个BUG**

# **ResponseFile 中必须指定为true，否则会提示错误,不管是否正确填写了邮件地址**

#------------------------------------------------------------------------------

DECLINE_SECURITY_UPDATES=true

#------------------------------------------------------------------------------

# Specify the Proxy server name. Lengthshould begreater than zero.

#**代理服务器名**

#Example :PROXY_HOST=proxy.domain.com

#------------------------------------------------------------------------------

PROXY_HOST=

#------------------------------------------------------------------------------

# Specify the proxy port number. Should beNumericand atleast 2 chars.

#**代理服务器端口**

#Example :PROXY_PORT=25

#------------------------------------------------------------------------------

PROXY_PORT=

#------------------------------------------------------------------------------

# Specify the proxy user name. LeavePROXY_USER andPROXY_PWD

# blank if your proxy server requiresnoauthentication.

#**代理服务器用户名**

#Example :PROXY_USER=username

#------------------------------------------------------------------------------

PROXY_USER=

#------------------------------------------------------------------------------

# Specify the proxy password. LeavePROXY_USER andPROXY_PWD

# blank if your proxy server requiresnoauthentication.

#**代理服务器密码**

#Example :PROXY_PWD=password

#------------------------------------------------------------------------------

PROXY_PWD=
