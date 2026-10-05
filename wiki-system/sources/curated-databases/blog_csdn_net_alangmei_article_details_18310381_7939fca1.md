---
source: "http://blog.csdn.net/alangmei/article/details/18310381"
title: "Oracle RAC （11.2.0.4版本） For AIX 6.1安装手册_rsct.basic.rte下载-CSDN博客"
fetched_at: "2026-10-05 15:27:13"
---

【部分引用别人的文档修改而成，实际经过安装验证的文档】

Oracle Rac 11GR2（11.2.0.4）

For AIX6.1+ASM安装手册

##

部分截图采用了网上别人的图片以及部分章节

## 2 安装环境说明

**节点**
---
**节点名称** |  **实例名称** |  **数据库名称** |  **处理器** |  **RAM** |  **操作系统**
Rac1 |  rac1 |  Rac |  4颗cpu*8核*4228Mhz |  32GB |  AIX6.1
Rac2 |  rac2 |  4颗cpu*8核*4228Mhz |  32GB |  AIX6.1
**网络配置**
**节点名称** |  **公共 IP 地址** |  **专用 IP 地址** |  **虚拟 IP 地址** |  **SCAN 名称** |  **SCAN IP 地址**
Rac1 |  172.1.1.204 |  192.168.0.204 |  172.1.1.206 |  Scan-ip |  172.1.1.208
Rac2 |  172.1.1.205 |  192.168.0.205 |  172.1.1.207
**Oracle 软件组件**
**软件组件** |  **操作系统用户** |  **主组** |  **辅助组** |  **主目录** |  **Oracle 基目录/Oracle 主目录**
Grid Infra |  grid |  oinstall |  asmadmin、asmdba、asmoper、oinstall |  /home/grid |  /u01/app/grid
/u01/app/11.2/grid
Oracle RAC |  oracle |  oinstall |  dba、oper、asmdba、oinstall |  /home/oracle |  /u01/app /oracle
/u01/app/oracle/product/11.2.0/db_1
**存储组件**
**存储组件** |  **文件系统** |  **卷大小** |  **ASM 卷组名** |  **ASM 冗余** |  **设备名**
OCR/VOTING |  ASM |  50G |  CRSDG |  normal |  /dev/rhdisk4-6
数据 |  ASM |  600G |  DATA |  normal |  /dev/rhdisk7-9
恢复区 |  ASM |  100G |  FRA_ARCHIVE |  Normal |  /dev/rhdisk10-12

###

###

###

###

###

###

###

###

###

###

###

###

###

###

###

###

###

























在Oracle RAC架构中共有四种IP，分别是Public IP，Private IP，VIP，SCAN IP。它们的作用如下：

Private IP：私有IP用于节点间同步心跳，这个对于用户层面，可以直接忽略，简单理解，这个IP是用来保证两台服务器同步数据用的。

Public IP：公有IP一般用于管理员使用，用来确保可以操作到正确的机器，也叫真实IP。

VIP：虚拟IP用于客户端应用，一般情况下VIP是飘在配置Public IP地址的网卡上的。VIP支持失效转移，通俗说就是配置该VIP的节点宕机了，另一个主机节点会自动接管该VIP，而客户端没有任何感觉。这也是为什么要使用RAC的原因之一，另一个原因，我认为是负载均衡。客户端在配置tnsnames.ora时，有些场合是要使用的vip，而有些场合又必须使用Public IP。例如，当你在定位一个数据库的死锁时，使用Public IP，可以确保连到你想处理的机器。相反此时使用VIP时，会出现不确定性，因为服务器默认是开启负载均衡的，也就是有可能你想连A机，系统却给你分配了B机。



SCAN IP：在Oracle 11gR2以前，如果数据库采用了RAC架构，在客户端的tnsnames中，需要配置多个节点的连接信息，从而实现诸如负载均衡，failover等等RAC的特性。因此，当数据库RAC集群需要添加或删除节点时，需要及时对客户端机器的tns进行更新，以免出现安全隐患。在11gR2中，为了简化该项配置工作，引入了SCAN（Single ClientAccess Name）的特性，该特性的好处在于，在数据库与客户端之间，添加了一层虚拟的服务层，就是所谓的SCAN IP以及SCAN IP Listener，在客户端仅需要配置SCAN IP的TNS信息，通过SCAN IPListener，连接后台集群数据库。这样，不论集群数据库是否有添加或者删除节点的操作，均不会对client产生影响。



两个RAC节点主机的规划：

网关：10.1.0.254

主机名称 |  主机别名 |  类型 |  IP地址 |  解析方式
---|---|---|---|---
rac1 |  rac1 |  Public |  172.1.1.204/255.255.255.0 |  host
rac1-vip |  rac1-vip |  Virtual |  172.1.1.206/255.255.255.0 |  host
rac1-priv |  rac1-priv |  Private |  192.168.0.204/255.255.255.0 |  host
rac2 |  rac2 |  Public |  172.1.1.205/255.255.255.0 |  host
rac2-vip |  rac2-vip |  Virtual |  172.1.1.207/255.255.255.0 |  host
rac2-priv |  rac2-priv |  Private |  192.168.0.205/255.255.255.0 |  host
Scan-ip |  Scan-ip |  Virtual |  172.1.1.208/255.255.255.0 |  host

### 2.4 存储盘规划

存储盘名称 |  大小 |  用途
---|---|---
hdisk 4 |  50GB |  CRSDG
hdisk 5 |  51GB
hdisk 6 |  52GB
hdisk 7 |  600GB |  DATA
hdisk 8 |  601GB
hdisk 9 |  602GB
hdisk10 |  100GB |  FRA_ARCHIVE
hdisk11 |  101GB
hdisk12 |  102GB

### 2.5 数据库安全信息

项目名称 |  用户名 |  口令或实例
---|---|---
操作系统用户 |  root |
数据库网格安装用户 |  Grid |
数据库安装用户 |  oracle |
集群实例名 |  rac |
ASM管理 |  Sys |
数据库管理 |  sys/system |
审计用户 |  rac_vault |

### 2.6 安装目录规划

**安装目录规划原则：** 建立/u01文件系统用来安装grid、datbase程序。程序都安装在/u01/app下面，对于grid与database分别建立不同的目录，分配不同的权限。其中grid的ORACLE_BASE和ORACLE_HOME建议安装在不同的目录下，具体规划如下：

**新建70G lv：** oralv

**新建文件系统，挂载点：** /u01

**grid base目录：** /u01/app/grid #grid用户的ORACLE_BASE

**grid asm安装目录：** /u01/app/11.2/grid #grid用户的ORACLE_HOME，也即是安装时的software location

Oracle base目录：/u01/app/oracle #oracle用户的ORACLE_BASE

注：此规划为后来总结，本次安装中与此略有出入。Grid用户的ORACLE_BASE、ORACLE_HOME都需要手工创建。Oracle用户只创建ORACLE_BASE目录即可。

## 3 预安装任务列表的检查配置

**说明：** 下面所列检查配置任务，默认需要在所有RAC节点执行，有很少的操作步骤只需在一个节点执行即可，这些步骤会一一说明，在检查配置时应该注意。

### 3.1 检查主机硬件配置

主机硬件检查包括：可用内存，页面交换空间、可用硬盘空间、/tmp目录可用空间。

1\. 使用如下命令查看主机的内存和交换空间，内存至少2.5G，交换空间应为物理可用内存的2倍。

# /usr/sbin/lsattr -HE -l sys0 -a realmem

attribute value description user_settable

realmem 32243712 Amount of usable physical memory in Kbytes False

#/usr/sbin/lsps -a

2\. 检查硬件架构：#/usr/bin/getconf HARDWARE_BITMODE，要求64位硬件架构。

3\. 检查集群软件和数据库软件安装目录至少有6.5GB可用空间，/tmp目录至少有1GB可用空间：#df -h。

4．查看主机信息

#prtconf

System Model: IBM,8231-E1D

Machine SerialNumber:

Processor Type:PowerPC_POWER7

ProcessorImplementation Mode: POWER 7

Processor Version:PV_7_Compat

Number OfProcessors: 8

Processor ClockSpeed: 4228 MHz

CPU Type: 64-bit

Kernel Type: 64-bit

LPAR Info: 106-E80AT

Memory Size: 31488MB

Good Memory Size:31488 MB

Platform Firmwarelevel: AL770_052

Firmware Version:IBM,AL770_052

Console Login:enable

Auto Restart: true

Full Core: false

Network Information

Host Name: rac1

IP Address: 172.1.1.204

Sub Netmask: 255.255.255.0

Gateway: 10.1.0.254

Name Server:

Domain Name:

Paging SpaceInformation

Total Paging Space: 9216MB

Percent Used: 1%

Volume GroupsInformation

==============================================================================

Active VGs

==============================================================================

rootvg:

PV_NAME PV STATE TOTAL PPs FREE PPs FREE DISTRIBUTION

hdisk0 active 558 304 111..80..00..01..112

hdisk1 active 558 450 111..86..30..111..112

INSTALLED RESOURCELIST

The followingresources are installed on the machine.

+/- = Added ordeleted from Resource List.

* = Diagnostic support not available.

Model Architecture: chrp

Model Implementation: Multiple Processor, PCIbus

\+ sys0 System Object

\+ sysplanar0 SystemPlanar

* vio0 Virtual I/O Bus

* vsa1 U78AB.001.WZSKA2R-P1-T2 LPARVirtual Serial Adapter

* vty1 U78AB.001.WZSKA2R-P1-T2-L0 AsynchronousTerminal

* vsa0 U78AB.001.WZSKA2R-P1-T1 LPARVirtual Serial Adapter

* vty0 U78AB.001.WZSKA2R-P1-T1-L0 AsynchronousTerminal

* pci8 U78AB.001.WZSKA2R-P1 PCIExpress Bus

\+ sissas2 U78AB.001.WZSKA2R-P1-C6-T1 PCI Expressx8 Ext Dual-x4 3Gb SAS Adapter

* sas2 U78AB.001.WZSKA2R-P1-C6-T1 ControllerSAS Protocol

* sfwcomm6 SAS Storage Framework Comm

* sata2 U78AB.001.WZSKA2R-P1-C6-T1 ControllerSATA Protocol

* pci7 U78AB.001.WZSKA2R-P1 PCIExpress Bus

\+ ent6 U78AB.001.WZSKA2R-P1-C5-T1 2-Port Gigabit Ethernet-SX PCI-ExpressAdapter (14103f03)

\+ ent7 U78AB.001.WZSKA2R-P1-C5-T2 2-PortGigabit Ethernet-SX PCI-Express Adapter (14103f03)

* pci6 U78AB.001.WZSKA2R-P1 PCI Express Bus

\+ ent4 U78AB.001.WZSKA2R-P1-C4-T1 2-PortGigabit Ethernet-SX PCI-Express Adapter (14103f03)

\+ ent5 U78AB.001.WZSKA2R-P1-C4-T2 2-Port Gigabit Ethernet-SX PCI-ExpressAdapter (14103f03)

* pci5 U78AB.001.WZSKA2R-P1 PCIExpress Bus

\+ fcs2 U78AB.001.WZSKA2R-P1-C3-T1 8Gb PCIExpress Dual Port FC Adapter (df1000f114108a03)

* fcnet2 U78AB.001.WZSKA2R-P1-C3-T1 FibreChannel Network Protocol Device

\+ fscsi2 U78AB.001.WZSKA2R-P1-C3-T1 FC SCSI I/OController Protocol Device

* sfwcomm2 U78AB.001.WZSKA2R-P1-C3-T1-W0-L0 Fibre ChannelStorage Framework Comm

\+ fcs3 U78AB.001.WZSKA2R-P1-C3-T2 8Gb PCIExpress Dual Port FC Adapter (df1000f114108a03)

* fcnet3 U78AB.001.WZSKA2R-P1-C3-T2 FibreChannel Network Protocol Device

\+ fscsi3 U78AB.001.WZSKA2R-P1-C3-T2 FC SCSI I/OController Protocol Device

* sfwcomm3 U78AB.001.WZSKA2R-P1-C3-T2-W0-L0 Fibre ChannelStorage Framework Comm

* pci4 U78AB.001.WZSKA2R-P1 PCIExpress Bus

\+ fcs0 U78AB.001.WZSKA2R-P1-C2-T1 8Gb PCI ExpressDual Port FC Adapter (df1000f114108a03)

* fcnet0 U78AB.001.WZSKA2R-P1-C2-T1 FibreChannel Network Protocol Device

\+ fscsi0 U78AB.001.WZSKA2R-P1-C2-T1 FC SCSI I/OController Protocol Device

* hdisk8 U78AB.001.WZSKA2R-P1-C2-T1-W5000D3100070E30C-L5000000000000 Compellent FC SCSI Disk Drive

* hdisk9 U78AB.001.WZSKA2R-P1-C2-T1-W5000D3100070E30C-L6000000000000 Compellent FC SCSI Disk Drive

* sfwcomm0 U78AB.001.WZSKA2R-P1-C2-T1-W0-L0 Fibre ChannelStorage Framework Comm

\+ fcs1 U78AB.001.WZSKA2R-P1-C2-T2 8Gb PCIExpress Dual Port FC Adapter (df1000f114108a03)

* fcnet1 U78AB.001.WZSKA2R-P1-C2-T2 FibreChannel Network Protocol Device

\+ fscsi1 U78AB.001.WZSKA2R-P1-C2-T2 FC SCSI I/OController Protocol Device

* hdisk4 U78AB.001.WZSKA2R-P1-C2-T2-W5000D3100070E30A-L1000000000000 Compellent FC SCSI Disk Drive

*hdisk5 U78AB.001.WZSKA2R-P1-C2-T2-W5000D3100070E30A-L2000000000000 Compellent FC SCSI Disk Drive

*hdisk6 U78AB.001.WZSKA2R-P1-C2-T2-W5000D3100070E30A-L3000000000000 Compellent FC SCSI Disk Drive

*hdisk7 U78AB.001.WZSKA2R-P1-C2-T2-W5000D3100070E30A-L4000000000000 Compellent FC SCSI Disk Drive

* sfwcomm1 U78AB.001.WZSKA2R-P1-C2-T2-W0-L0 Fibre Channel StorageFramework Comm

* pci3 U78AB.001.WZSKA2R-P1 PCIExpress Bus

\+ ent0 U78AB.001.WZSKA2R-P1-C7-T1 4-PortGigabit Ethernet PCI-Express Adapter (e414571614102004)

\+ ent1 U78AB.001.WZSKA2R-P1-C7-T2 4-PortGigabit Ethernet PCI-Express Adapter (e414571614102004)

\+ ent2 U78AB.001.WZSKA2R-P1-C7-T3 4-Port Gigabit Ethernet PCI-ExpressAdapter (e414571614102004)

\+ ent3 U78AB.001.WZSKA2R-P1-C7-T4 4-PortGigabit Ethernet PCI-Express Adapter (e414571614102004)

* pci2 U78AB.001.WZSKA2R-P1 PCI ExpressBus

\+ sissas1 U78AB.001.WZSKA2R-P1-C18-T1 PCIe x4Internal 3Gb SAS RAID Adapter

* sas1 U78AB.001.WZSKA2R-P1-C18-T1 ControllerSAS Protocol

* sfwcomm5 SAS Storage Framework Comm

\+ ses0 U78AB.001.WZSKA2R-P2-Y2 SASEnclosure Services Device

\+ ses1 U78AB.001.WZSKA2R-P2-Y1 SASEnclosure Services Device

* tmscsi1 U78AB.001.WZSKA2R-P1-C18-T1-LFE0000-L0 SAS I/O ControllerInitiator Device

* sata1 U78AB.001.WZSKA2R-P1-C18-T1 Controller SATAProtocol

* pci1 U78AB.001.WZSKA2R-P1 PCIExpress Bus

* pci9 U78AB.001.WZSKA2R-P1 PCIBus

\+ usbhc0 U78AB.001.WZSKA2R-P1 USBHost Controller (33103500)

\+ usbhc1 U78AB.001.WZSKA2R-P1 USBHost Controller (33103500)

\+ usbhc2 U78AB.001.WZSKA2R-P1 USB Enhanced HostController (3310e000)

* pci0 U78AB.001.WZSKA2R-P1 PCIExpress Bus

\+ sissas0 U78AB.001.WZSKA2R-P1-T9 PCIe x4Planar 3Gb SAS RAID Adapter

* sas0 U78AB.001.WZSKA2R-P1-T9 Controller SAS Protocol

* sfwcomm4 SAS StorageFramework Comm

\+ hdisk0 U78AB.001.WZSKA2R-P3-D1 SAS DiskDrive (300000 MB)

\+ hdisk1 U78AB.001.WZSKA2R-P3-D2 SAS DiskDrive (300000 MB)

\+ hdisk2 U78AB.001.WZSKA2R-P3-D3 SAS Disk Drive (300000 MB)

\+ hdisk3 U78AB.001.WZSKA2R-P3-D4 SAS DiskDrive (300000 MB)

\+ ses2 U78AB.001.WZSKA2R-P2-Y1 SASEnclosure Services Device

* tmscsi0 U78AB.001.WZSKA2R-P1-T9-LFE0000-L0 SAS I/O ControllerInitiator Device

* sata0 U78AB.001.WZSKA2R-P1-T9 Controller SATA Protocol

\+ cd0 U78AB.001.WZSKA2R-P3-D7 SATADVD-RAM Drive

\+ L2cache0 L2 Cache

\+ mem0 Memory

\+ proc0 Processor

\+ proc4 Processor

\+ proc8 Processor

\+ proc12 Processor

\+ proc16 Processor

\+ proc20 Processor

\+ proc24 Processor

\+ proc28 Processor

### 3.2 主机网络配置

主机网络设置检查：hosts文件系修改、网卡IP配置。

1\. 编辑hosts文件，将如下内容添加到hosts文件中，指定Public IP、VIP、Private IP。

#public

172.1.1.204 rac1

172.1.1.205 rac2

# private

192.168.0.204 rac1-priv

192.168.0.205 rac2-priv

# virtual

172.1.1.206 rac1-vip

172.1.1.207 rac2-vip

#scan

172.1.1.208 scan-ip

2\. 网卡的IP地址已经在系统安装过程中配置完成，可以使用如下命令检查IP配置情况：#ifconfig–a。

### 3.3 检查主机软件配置

主机软件配置检查包括：操作系统版本、系统内核版本、必须软件包安装。

1\. 检查操作系统版本：#oslevel -s，最低要求6100-02-01。

2\. 检查操作系统内核：#bootinfo -K，要求64位内核。

3\. 检出主机SSH配置：#lssrc -ssshd。

4\. 系统必须安装如下（或更高版本）软件包：

bos.adt.base

bos.adt.lib

bos.adt.libm

bos.perf.libperfstat 6.1.2.1 or later

bos.perf.perfstat

bos.perf.proctools

xlC.aix61.rte. 10.1.0.0 or later

xlC.rte. 10.1.0.0or later

gpfs.base 3.2.1.8or later(当使用GPFS共享文件系统时安装)

可以使用如下命令：

# lslpp -l bos.adt.*

# lslpp -l bos.perf.*

# lslpp -l xlC.*

# lslpp -l gpfs.*

来查看系统是否已经安装相应的软件包。如果系统中缺少上述软件包或者版本较低，请使用系统安装光盘安装相关软件包。

**AIX 6.1需要安装如下软件包：**

bos.adt.base

bos.adt.lib

bos.adt.libm

bos.perf.libperfstat 6.1.2.1 or later

bos.perf.perfstat

bos.perf.proctools

rsct.basic.rte

rsct.compat.clients.rte

xlC.aix61.rte 10.1.0.0 (or later)

**AIX 5.3需要安装如下软件包：**

bos.adt.base

bos.adt.lib

bos.adt.libm

bos.perf.libperfstat 5.3.9.0 or later

bos.perf.perfstat

bos.perf.proctools

rsct.basic.rte

rsct.compat.clients.rte

xlC.aix50.rte 10.1.0.0 (or later)

以上filesets安装与否可以用命令lslpp －l进行检查确认。默认安装是不全的，需要手工进行添加。同时系统盘的版本与上述也有差异，安装尝试。

其它单个补丁的要求如下：

AIX 6L installations All AIX 6L 6.1 installations Authorized Problem Analysis

Reports (APARs) for AIX 5L v. 5.3 ML06, and the following AIX

fixes:

IZ41855

IZ51456

IZ52319

AIX 5L installations All AIX 5L 5.3 installations Authorized Problem Analysis

Reports (APARs) for AIX 5L v. 5.3 ML06, and the following AIX

fixes:

IZ42940

IZ49516

IZ52331

验证：#**/usr/sbin/instfix -i -k IZ41855**

**安装补丁：**

**由于6100-04不需要任何补丁，所以我们将系统升级到6100-04（但是安装grid的时候还是出现3个包未安装提示）**

1、 从IBM官网上下载6100-04-00-0943

2、 将补丁文件上传至/tmp/tools下

**3、 smit update_all**

选择不提交，保存被覆盖的文件，可以回滚操作，接受许可协议

COMMIT software updates? No

SAVE replaced files? yes

ACCEPT new license agreements? Yes

**升级完后查看：**

# **oslevel -s**

6100-04-01-0944

5\. 检查java版本：#java-version，要求1.6版本64位。

### 3.4 创建操作系统组和用户

建立用户组，用户和目录（简易版，如果是11.2.0.4以上，rootpre.sh会要求更为细致的组，比如asmadmin等等，具体可参考文档）

创建相应的操作系统组和用户，先创建组，然后创建用户：

Ø 以root用户使用如下命令为网格及Oracle用户创建OS组：

#mkgroup-'A' id='501' adms='root' oinstall

#mkgroup-'A' id='502' adms='root' asmadmin

#mkgroup-'A' id='503' adms='root' asmdba

#mkgroup-'A' id='504' adms='root' asmoper

#mkgroup-'A' id='505' adms='root' dba

#mkgroup-'A' id='506' adms='root' oper

Ø 创建Oracle软件所有者：

#mkuser id='501' pgrp='oinstall'groups='dba,asmadmin,asmdba,asmoper' home='/home/grid' fsize=-1 cpu=-1 data=-1rss=-1 stack=-1 stack_hard=-1capabilities=CAP_NUMA_ATTACH,CAP_BYPASS_RAC_VMM,CAP_PROPAGATE grid

#mkuser id='502' pgrp='oinstall'groups='dba,asmdba,oper' home='/home/oracle' fsize=-1 cpu=-1 data=-1 rss=-1stack=-1 stack_hard=-1capabilities=CAP_NUMA_ATTACH,CAP_BYPASS_RAC_VMM,CAP_PROPAGATE oracle

Ø 检查上面创建的两个用户：

#id grid

#id oracle

Ø 使用passwd命令为grid（密码：grid）和oracle（密码：oracle）账户设置密码。

#passwdgrid

#passwdoracle

### 3.5 创建软件安装目录结构并更改权限

修改磁盘数组为grid oinstall（如果是11.2.0.4以上，根据设置的需求，可能会要求更改为 grid dba，是具体设置而定）：

创建Oracle软件相应的目录结构，包括：GRID目录，RDBMS目录。

注意grid用户的BASE目录和HOME目录不能有父子关系。

Ø 以root用户创建“Oracle inventory 目录”，并更改权限：

#mkdir-p /u01/app/oraInventory

#chown-R grid:oinstall /u01/app/oraInventory

#chmod-R 775 /u01/app/oraInventory

Ø 以root用户创建“Grid Infrastructure BASE 目录”

#mkdir-p /u01/app/grid

#chowngrid:oinstall /u01/app/grid

#chmod-R 775 /u01/app/grid

Ø 以root用户创建“Grid Infrastructure Home 目录”

#mkdir-p /u01/app/11.2.0/grid

#chown-R grid:oinstall /u01/app/11.2.0/grid

#chmod-R 775 /u01/app/11.2.0/grid

Ø 以root用户创建“Oracle Base 目录”

#mkdir-p /u01/app/oracle

#mkdir/u01/app/oracle/cfgtoollogs

#chown-R oracle:oinstall /u01/app/oracle

#chmod-R 775 /u01/app/oracle

Ø 以root用户创建“Oracle RDBMS Home 目录”

#mkdir-p /u01/app/oracle/product/11.2.0/db_1

#chown-R oracle:oinstall /u01/app/oracle/product/11.2.0/db_1

#chmod-R 775 /u01/app/oracle/product/11.2.0/db_1

### 3.6 修改用户环境参数文件

如果分别以oracle用户和grid用户修改环境参数文件，修改之后可以使用如下命令使其生效：$.profile。如果使用root用户修改则不需要重新加载环境配置文件。

1\. 在rac1节点上设置grid用户和oracle的环境变量参数。

Ø grid用户：编辑家目下的.profile文件，添加如下内容：

umask 022

export ORACLE_BASE=/u01/app/grid

export ORACLE_HOME=/u01/app/11.2.0/grid

export ORACLE_SID=+ASM1

export ORACLE_HOSTNAME=rac1

export NLS_LANG=AMERICAN_AMERICA.AL32UTF8

export NLS_DATE_FORMAT="yyyy-mm-ddhh24:mi:ss"

export PATH=$PATH:$ORACLE_HOME/bin:$ORACLE_HOME/OPatch

Ø oracle用户：编辑家目下的.profile文件，添加如下内容：

umask 022

export ORACLE_BASE=/u01/app/oracle

exportORACLE_HOME=/u01/app/oracle/product/11.2.0/db_1

export ORACLE_SID=rac1

export ORACLE_HOSTNAME=rac1

export ORACLE_UNQNAME=rac

export NLS_LANG=AMERICAN_AMERICA.AL32UTF8

export NLS_DATE_FORMAT="yyyy-mm-ddhh24:mi:ss"

export PATH=$PATH:$ORACLE_HOME/bin:$ORACLE_HOME/OPatch

2\. 在rac2节点上设置grid用户和oracle的环境变量参数。

Ø grid用户：编辑家目下的.profile文件，添加如下内容：

umask 022

export ORACLE_BASE=/u01/app/grid

export ORACLE_HOME=/u01/app/11.2.0/grid

export ORACLE_SID=+ASM2

export ORACLE_HOSTNAME=rac2

export NLS_LANG=AMERICAN_AMERICA.AL32UTF8

export NLS_DATE_FORMAT="yyyy-mm-ddhh24:mi:ss"

export PATH=$PATH:$ORACLE_HOME/bin:$ORACLE_HOME/OPatch

Ø oracle用户：编辑家目下的.profile文件，添加如下内容：

umask 022

exportORACLE_BASE=/u01/app/oracle

exportORACLE_HOME=/u01/app/oracle/product/11.2.0/db_1

export ORACLE_SID=rac2

export ORACLE_HOSTNAME=rac2

export ORACLE_UNQNAME=rac

export NLS_LANG=AMERICAN_AMERICA.AL32UTF8

export NLS_DATE_FORMAT="yyyy-mm-ddhh24:mi:ss"

export PATH=$PATH:$ORACLE_HOME/bin:$ORACLE_HOME/OPatch

注意：环境变量要注意是否含有空格，虽然安装可以正常进行，但是安装完后命令都不能正常执行，比如你在grid用户执行asmcmd，进入的是一个空实例，你无法管理ASM实例，那么出了问题就回天无力了，所以还是注意检查下，就算安装完了，也需要重新请重装。

### 3.7 系统部分参数修改

系统参数的修改包括：虚拟内存管理参数、网络参数、系统内核参数、异步IO。

从AIX 6.1以后，下属值貌似是缺省值了，跟Oracle installguide一致，因此无需修改:
vmo -p -o minperm%=3
vmo -p -o maxperm%=90
vmo -p -o maxclient%=90
vmo -p -o lru_file_repage=0
vmo -p -o strict_maxclient=1
vmo -p -o strict_maxperm=0

1\. 分别使用如下命令查看虚拟内存管理参数，

vmo -L minperm%

vmo -L maxperm%

vmo -L maxclient%

vmo -L lru_file_repage

vmo -L strict_maxclient

vmo -L strict_maxperm

如果设置不合适，使用如下命令修改：

#vmo -p -o minperm%=3

#vmo -p -o maxperm%=90

#vmo -p -o maxclient%=90

#vmo -p -o lru_file_repage=0

#vmo -p -o strict_maxclient=1

#vmo -p -o strict_maxperm=0

2\. 检查网络参数设置

Ø ephemeral参数：

使用命令no -a |fgrep ephemeral可以查看当前系统ephemeral参数设置，建议的参数设置如下

tcp_ephemeral_high = 65500

tcp_ephemeral_low = 9000

udp_ephemeral_high= 65500

udp_ephemeral_low = 9000

如果系统中参数设置和上述值不一样，使用命令修改：

#no -p -o tcp_ephemeral_low=9000 -o tcp_ephemeral_high=65500

#no -p -o udp_ephemeral_low=9000 -o udp_ephemeral_high=65500

Ø 使用如下命令修改网络可调整参数：

#no -r -o rfc1323=1

#no -r -o ipqmaxlen=512

#no -p -o sb_max=4194304

#no -p -o tcp_recvspace=65536

#no -p -o tcp_sendspace=65536

#no -p -o udp_recvspace=1351680 该值是udp_sendspace的10倍，但须小于sb_max

#no -p -o udp_sendspace=135168

备注：-r表示reboot后生效，-p表示即刻生效.

3\. 检查内核参数maxuproc（建议16384）和ncargs（至少128）

#lsattr -E -l sys0 -a ncargs

#lsattr -E -l sys0 -a maxuproc

如果设置不合适使用如下命令修改：

#chdev -l sys0 -a ncargs=256

#chdev -l sys0 -a maxuproc=16384

4\. 检查异步IO是否开启，AIX6.1默认系统已经开启，使用如下命令查询：

#ioo -a | more 或 #ioo -o aio_maxreqs

注意：AIX5.3使用如下命令查看lsattr -El aio0 -a maxreqs

### 3.8 配置共享存储

下面的几步操作均需要在**所有节点** 执行。

1\. 修改物理卷的属主和权限：

#chown grid:asmadmin /dev/rhdisk4

#chown grid:asmadmin /dev/rhdisk5

#chown grid:asmadmin /dev/rhdisk6

#chown grid:asmadmin /dev/rhdisk7

#chown grid:asmadmin /dev/rhdisk8

#chown grid:asmadmin /dev/rhdisk9

#chown grid:asmadmin /dev/rhdisk10

#chown grid:asmadmin /dev/rhdisk11

#chown grid:asmadmin /dev/rhdisk12

#chmod 660 /dev/rhdisk4

#chmod 660 /dev/rhdisk5

#chmod 660 /dev/rhdisk6

#chmod 660 /dev/rhdisk7

#chmod 660 /dev/rhdisk8

#chmod 660 /dev/rhdisk9

#chmod 660 /dev/rhdisk10

#chmod 660 /dev/rhdisk11

#chmod 660 /dev/rhdisk12

2\. 修改物理卷属性，共享存储磁盘的reserve_policy属性需要是no，使用如下命令查看：

#lsattr -E -l hdisk4 | grep reserve_policy

#lsattr -E -l hdisk5 | grep reserve_policy

#lsattr -E -l hdisk6 | grep reserve_policy

#lsattr -E -l hdisk7 | grep reserve_policy

#lsattr -E -l hdisk8 | grep reserve_policy

#lsattr -E -l hdisk9 | grep reserve_policy

#lsattr -E -l hdisk10 | grepreserve_policy

#lsattr -E -l hdisk11 | grepreserve_policy

#lsattr -E -l hdisk12 | grepreserve_policy

如果需要修改reserve_policy属性，使用如下命令：

#chdev -l hdisk4 -areserve_policy=no_reserve

#chdev -l hdisk5 -areserve_policy=no_reserve

#chdev -l hdisk6 -areserve_policy=no_reserve

#chdev -l hdisk7 -areserve_policy=no_reserve

#chdev -l hdisk8 -areserve_policy=no_reserve

#chdev -l hdisk9 -areserve_policy=no_reserve

#chdev -l hdisk10 -areserve_policy=no_reserve

#chdev -l hdisk11 -areserve_policy=no_reserve

#chdev -l hdisk12 -areserve_policy=no_reserve

3、每台主机的硬盘信息

hdisk0 00f8e8092df611fa rootvg active

hdisk1 00f8e8082e4a46d5 rootvg active

hdisk2 00f8e80857a08edf appvg active

hdisk3 none None

#本地磁盘，其中hdisk0和hdisk1做成系统镜像，hdisk2和hdisk3做成镜像用于应用安装

hdisk4 none None

hdisk5 none None

hdisk6 none None

#oracle 的OCR和Voting盘，设置为正常冗余

hdisk7 none None

hdisk8 none None

hdisk9 none None

#oracle的数据盘，正常冗余。

hdisk10 none None

hdisk11 none None

hdisk12 none None

#oracle的闪回以及归档盘，正常冗余。

#### 3.8.1 清除PVID

查看LUN，如果已经有了PVID的话，需要进行清除。

**chdev -l hdisk2 -a pv=clear**

重复同样的操作，清除2-6所有LUN的PVID

### 3.9 配置NTP服务（可选）

Oracle 11g R2提供Cluster Time SynchronizationService（CTSS）集群时间同步服务，在没有NTP服务时，该功能可以保证所有RAC节点的时间保持一致。ASM可以作为统一的存储把Oracle Cluster Registry（OCR）和Voting disks统一安装在ASM磁盘上，不再需要单独安装集群文件系统了，11g第二版也不再支持裸设备了（之前可以把集群件安装到裸设备上）。还有一个功能SCAN（Single Client Access Name）即单客户端访问名称而且该功能包括了Failover故障自动切换功能，在访问集群是只写一个SCAN名称就可以了，不需要象以前要把所有节点的VIP写在应用程序的配置文件里面了，这样就大大方便了客户端程序对RAC系统的访问，但该功能需要DNS服务器的支持。SCAN配置也可以采用hosts文件作解析。

如果系统配置了NTP服务，CTSS服务会处于观察者模式，配置NTP具体步骤可参考AIX服务配置。

### 3.10 配置SSH

11.2,中，配置SSH需要作如下设置：
By default, OUI searches for SSH public keys in the directory /usr/local/etc/,and
ssh-keygen binaries in /usr/local/bin. However, on AIX, SSH public keys
typically are located in the path /etc/ssh, and ssh-keygen binaries are locatedin
the path /usr/bin. To ensure that OUI can set up SSH, use the following commandto
create soft links:
# ln -s /etc/ssh /usr/local/etc
# ln -s /usr/bin /usr/local/bin

配置root环境变量:
====================================================================
export ORACLE_BASE=/u01/app/grid
export ORACLE_HOME=/u01/app/11.2.0/grid
export PATH=$ORACLE_HOME/OPatch:$ORACLE_HOME/bin:$PATH

if [ -t 0 ]; then
stty intr ^C
fi

export AIXTHREAD_SCOPE=S

set -o vi
alias ll=”ls -lrt”

#### 3.10.1 SSH信任关系设置（可选）

SSH信任关系也可在grid安装时选择自动配置。

**注意：Oracle11g R2 grid在AIX上自动配置ssh时会报错，因为Oracle调用的命令路径和AIX系统上命令实际路径不符，可以修改oracle安装程序的sshsetup.sh脚本，或按照oracle调用路径添加程序软连接，具体路径安装过程中Oracle会提示。**

##### 3.10.1.1 首先在两台机器上安装好OpenSSH软件；

具体安装方法本处不详述，需要下载openssh、openssl，安装时需先安装openssl，然后再安装openssh。

也可以通过AIX系统光盘，执行smitty install，选择所有ssh包安装。

安装完毕后可以检查：

# lslpp -l | grep ssh

##### 3.10.1.2 然后在grid安装中选择自动配置SSH双机信任关系

###### 3.10.1.2.1 方法1

l **修改/etc/ssh/sshd_config**

将：

RSAAuthentication yes

PubkeyAuthentication yes

AuthorizedKeysFile .ssh/authorized_keys

前面的注释去掉。

l **利用命令:ssh-keygen生成key**

全部选择默认的就可以 , 生成的private key和publicKey会保存在 ~/.ssh目录下 .

**注:** 为了后面的访问方便, passphrase一行密码一般设置为空.

l **将2台机器的public key互相传给对方**

可以有好几种方法: ftp , rcp , scp都可以 .这里我们通过FTP将两个节点的~/.ssh下的id_rsa、id_rsa.pub两个文件分别拷下来传至对方。由于同名，分别将其更改为id_rsa239、id_rsa239.pub、id_rsa237、id_rsa237.pub，为了区分，后面加上其IP标识。

l 建立authorized_keys文件

由于上面修改了sshd_config文件 , 其中一行为

AuthorizedKeysFile .ssh/authorized_keys

为认证读取文件的位置 .

我们采取默认的方式 , 在~/.ssh下touch一个authorized_keys文件.

**touch authorized_keys**

将传输过来的对方主机的pub key内容 ,追加到authorized_keys文件上,

**Node1(192.168.0.204):**

bash-3.00#**cat id_rsa204.pub > authorized_keys**

**node2(192.168.0.205):**

#**cat id_rsa205.pub > authorized_keys**

**测试：**

ssh 192.168.0.204

ssh 192.168.0.205

第一次登录会出现提示，输入yes后以后就不会了

###### 3.10.1.2.2 方法2

**以下两个节点都执行：**

#su – grid

$mkdir ~/.ssh

$chmod 700 ~/.ssh

$/usr/bin/ssh-keygen -t rsa

rac1:/home/grid$/usr/bin/ssh-keygen -t rsa

Generating public/private rsa key pair.

Enter file in which to save the key (/home/grid/.ssh/id_rsa):

Enter passphrase (empty for no passphrase):

Enter same passphrase again:

提示输入密码时，保持为空，直接回车即可。

**以下只在节点1上执行：**

$ touch ~/.ssh/authorized_keys

$ ssh rac1 cat ~/.ssh/id_rsa.pub>>~/.ssh/authorized_keys

$ ssh rac2 cat ~/.ssh/id_rsa.pub>>~/.ssh/authorized_keys

$ scp ~/.ssh/authorized_keys rac2:.ssh/authorized_keys

修改如下：

$ touch ~/.ssh/authorized_keys

$ ssh rac1 cat ~/.ssh/id_rsa.pub>>~/.ssh/authorized_keys

$ ssh rac2 cat ~/.ssh/id_rsa.pub>>~/.ssh/authorized_keys

$ scp ~/.ssh/authorized_keys rac2:.ssh/authorized_keys

**以下只在节点2上执行：**

$ chmod 600 ~/.ssh/authorized_keys

配置完成后按方法1中测试方法进行测试。

### 3.11 DNS配置（避免grid最后验证报错，可忽略）

#[/]mv/usr/bin/nslookup /usr/bin/nslookup.org

#[/]cat/usr/bin/nslookup

#!/usr/bin/sh

HOSTNAME=${1}

if[[ $HOSTNAME = "rx-cluster-scan" ]]; then

echo "Server: 24.154.1.34"

echo "Address: 24.154.1.34#53"

echo "Non-authoritative answer:"

echo "Name: rx-cluster-scan"

echo "Address: 1.1.1.11" #假设1.1.1.1为SCAN地址

else

/usr/bin/nslookup.org $HOSTNAME

fi

注意：if you need to modify your SQLNET.ORA, ensure thatEZCONNECT is in the list if you specify the order of the naming methods usedfor client name resolution lookups (11gRelease 2 default is NAMES.DIRECTORY_PATH=(tnsnames, ldap, ezconnect)).

### 3.12 事先需要注意的事项

A、安装11gR2 RAC要求必须配置ssh用户对等性，以前配置rsh的方式现在已经无法通过安装检查。OUI中提供了自动配置ssh用户对等性的按钮，因此无需再事先手动配置。

需要注意的是：该功能完全针对Linux环境进行的开发，因此在AIX环境中，需要事先作如下操作：

ln -s /usr/bin/ksh/bin/bash

mkdir -p /usr/local/bin

ln -s /usr/bin/ssh-keygen/usr/local/bin/ssh-keygen

在配置对等性时，OUI会使用/bin/bash，而AIX默认是没有bash的，因此需要将ksh软链接到bash（当然你也可以安装bash包）。

同样，OUI会使用/usr/local/bin/ssh-keygen产生对等性密钥，而AIX中在安装了OpenSSH以后，ssh-keygen命令默认是存储在/usr/bin中，因此也需要做link。

B、在成功安装完Grid Infrastructure之后，运行cluvf命令可能会报错。

# cluvfy comp nodeapp -verbose

ERROR:

CRS is not installed on any of the nodes

Verification cannot proceed

并且，在碰到这样的错误之后，也无法安装RAC，会碰到如下错误：

[INS-35354] The system on which you areattempting to install Oracle RAC is not part of a valid cluster.

也就是无论是cluvf命令还是OUI，都认为这个机器上没有安装CRS，并不是在一个集群环境中。但是实际上运行crsctl check crs命令是完全正常的。

这个错误的解决方法可以参看MetalinkNote [ID 798203.1]，大体上来说就是在安装Grid Infrastructure的时候，inventory.xml文件中丢掉了CRS=”true”字样，这无疑是安装程序的bug。需要手工detachHome再attachHome。

## 4 安装Oracle GridInfrastructure 11g R2

### 4.1 准备Grid Infrastructure安装软件

1\. 将下载的p13390677_112040_AIX64-5L_3of7.zip压缩包上传到grid用户的主目录中。

2\. 将p13390677_112040_AIX64-5L_3of7.zip解压到当前文件夹：

#cd /home/grid

#unzip p13390677_112040_AIX64-5L_3of7.zip

如果没有安装unzip包也可以用jar解压。

#jar -xvfp13390677_112040_AIX64-5L_1of7.zip

3\. 修改解压后的文件夹grid的权限：

#chown -R grid:oinstall/home/grid/grid

### 4.2 使用CVU脚本校验系统是否满足安装需求

安装Oracle RAC环境需要多个步骤。硬件、OS、集群软件、数据库软件应按照顺序来安装。每一个步骤所包含的重要组件都是成功安装不可缺少的。Oracle提供了一个工具CVU（Cluster Verification Utility）用于在Oracle RAC的安装过程中验证系统是否满足安装需求。

1\. 以grid用户登录系统，确认当前目录为grid用户家目，即使用pwd命令输出的结果为：

#pwd //命令执行结果为“/home/grid/”

#cd grid //进入到安装程序根目录

2\. 执行CVU脚本校验系统，并将检查结果输出到report.txt文本文件中。

#./runcluvfy.sh stage -precrsinst -n rac1,rac2 -fixup -verbose >report.txt

3\. 可以使用如下命令查看分析 report.txt文件：

#cat report.txt|grep failed

4\. 将安装介质grid目录下rootpre.sh拷贝到所有节点grid用户的家目录下，root用户执行rootpre.sh在**所有节点 ：**

#scp -r /home/grid/grid/rootpre/root@192.168.0.205:/home/grid/rootpre/

#**./** rootpre.sh

### 4.3 开始安装Grid Infrastructure

1\. 首先在宿主机上安装Xmanager软件，并在宿主机上打开一个"Xmanager - Passive"会话进程。

2\. 在宿主机上以grid用户SSH远程连接到Linux主机，输入如下命令：xclock，验证图形界面是否可以正常在本地显示。如果可以正常显示一个“钟表”图形（如下图），请继续后续的步骤，如果不能正常显示，请检查排错。

3\. 在SSH会话中，切换到grid安装目录下，执行安装脚本开启grid安装程序。

./runInstaller

#su - grid

rac1:/home/grid$exportDISPLAY=172.1.165.172:0.0

rac1:/home/grid$/u01/soft/grid/runInstaller

********************************************************************************

Yourplatform requires the root user to perform certain pre-installation

OSpreparation. The root user should runthe shell script 'rootpre.sh' before

youproceed with Oracle installation. rootpre.sh can be found at the top level

ofthe CD or the stage area.

Answer'y' if root has run 'rootpre.sh' so you can proceed with Oracle

installation.

Answer'n' to abort installation and then ask root to run 'rootpre.sh'.

********************************************************************************

Has'rootpre.sh' been run by root on all nodes? [y/n] (n)

y

StartingOracle Universal Installer...

CheckingTemp space: must be greater than 190 MB. Actual 9516 MB Passed

Checkingswap space: must be greater than 150 MB. Actual 9216 MB Passed

Checkingmonitor: must be configured to display at least 256 colors. Actual 16

777216 Passed

Preparingto launch Oracle Universal Installer from /tmp/OraInstall2014-01-03_11-

05-23PM.Please wait ...rac1:/home/grid$

4\. 弹出OUI主界面，选择“Skipsoftware updates”，点击“Next”。

5\. 选择“Install and Configure Oracle Grid Infrastructure for a Cluster”，点击“Next”。

6\. 选择“Advanced Installation”，点击“Next”。

7\. 选择添加“Simplified Chinese”到“Selected Langusges”，点击“Next”。

8\. 输入相关配置信息，如下图所示，点击“Next”。

9\. 点击“Add”，增加一个网格节点rac2，具体配置信息如下图，点击“OK”，之后点击“Next”。如果前面没有配置“SSH互信”，可以在此步配置。

10\. OUI安装程序会自动区分Public和Private网络，点击“Next”。

11\. 选择“Oracle ASM”存储，点击“Next”。

12\. 将/dev/rhdisk2、/dev/rhdisk3、/dev/rhdisk4加到磁盘组“OCR_VOTE”中，选择“Normal”冗余，AU大小为1M，点击“Next”。

13\. 选择“Use same passwords for these accounts”，输入密码“Abc560647”，点击“Next”。

14\. 指定ASM管理相关组信息，点击“Next”。

15\. 指定Oracle基目录和软件安装位置，点击“Next”。

16\. 指定Oracle软件安装清单目录位置，点击“Next”。

17\. 执行安装条件检查。

18\. 安装条件检查合格后，弹出配置信息汇总情况，点击“Install”。

19\. OUI开始安装grid infrastructure 软件。

20\. 安装过程中会弹出如下执行脚本提示框，以root用户分别在每个节点执行提示框中的脚本，执行完成后点击“OK”。**注意：节点 rac1执行之后，才可在rac2节点执行。**

第一个节点的执行信息如下：

#/u01/app/oraInventory/orainstRoot.sh

Changing permissionsof /u01/app/oraInventory.

Adding read,writepermissions for group.

Removingread,write,execute permissions for world.

Changing groupnameof /u01/app/oraInventory to dba.

The execution of thescript is complete.

#/u01/app/11.2/grid/root.sh

Performing root useroperation for Oracle 11g

The followingenvironment variables are set as:

ORACLE_OWNER= grid

ORACLE_HOME= /u01/app/11.2/grid

Enter the fullpathname of the local bin directory: [/usr/local/bin]:

The contents of"dbhome" have not changed. No need to overwrite.

The contents of"oraenv" have not changed. No need to overwrite.

The contents of"coraenv" have not changed. No need to overwrite.

Creating /etc/oratabfile...

Entries will beadded to the /etc/oratab file as needed by

DatabaseConfiguration Assistant when a database is created

Finished runninggeneric part of root script.

Now product-specificroot actions will be performed.

Using configurationparameter file: /u01/app/11.2/grid/crs/install/crsconfig_params

Creating trace directory

User ignoredPrerequisites during installation

Installing TraceFile Analyzer

User grid has therequired capabilities to run CSSD in realtime mode

OLR initialization -successful

root wallet

root wallet cert

root cert export

peer wallet

profile reader wallet

pa wallet

peer wallet keys

pa wallet keys

peer cert request

pa cert request

peer cert

pa cert

peer root cert TP

profile reader root cert TP

pa root cert TP

peer pa cert TP

pa peer cert TP

profile reader pa cert TP

profile reader peer cert TP

peer user cert

pa user cert

Adding Clusterwareentries to inittab

CRS-2672: Attemptingto start 'ora.mdnsd' on 'rac1'

CRS-2676: Start of'ora.mdnsd' on 'rac1' succeeded

CRS-2672: Attemptingto start 'ora.gpnpd' on 'rac1'

CRS-2676: Start of'ora.gpnpd' on 'rac1' succeeded

CRS-2672: Attemptingto start 'ora.cssdmonitor' on 'rac1'

CRS-2672: Attemptingto start 'ora.gipcd' on 'rac1'

CRS-2676: Start of'ora.cssdmonitor' on 'rac1' succeeded

CRS-2676: Start of'ora.gipcd' on 'rac1' succeeded

CRS-2672: Attemptingto start 'ora.cssd' on 'rac1'

CRS-2672: Attemptingto start 'ora.diskmon' on 'rac1'

CRS-2676: Start of'ora.diskmon' on 'rac1' succeeded

CRS-2676: Start of'ora.cssd' on 'rac1' succeeded

ASM created andstarted successfully.

Disk Group CRSDGcreated successfully.

clscfg: -installmode specified

Successfullyaccumulated necessary OCR keys.

Creating OCR keysfor user 'root', privgrp 'system'..

Operationsuccessful.

CRS-4256: Updatingthe profile

Successful additionof voting disk a58239b181b14f03bff383940a72cbe9.

Successful additionof voting disk 12931f422fe74fd6bf2721d63a02f639.

Successful additionof voting disk 6f7ee1cbbe6a4ff1bf3a1b097a00deb7.

Successfullyreplaced voting disk group with +CRSDG.

CRS-4256: Updating theprofile

CRS-4266: Votingfile(s) successfully replaced

## STATE File Universal Id File Name Disk group

\-- ----- ----------------- --------- ---------

1\. ONLINE a58239b181b14f03bff383940a72cbe9 (/dev/rhdisk4) [CRSDG]

2\. ONLINE 12931f422fe74fd6bf2721d63a02f639 (/dev/rhdisk5) [CRSDG]

3\. ONLINE 6f7ee1cbbe6a4ff1bf3a1b097a00deb7 (/dev/rhdisk6) [CRSDG]

Located 3 votingdisk(s).

CRS-2672: Attemptingto start 'ora.asm' on 'rac1'

CRS-2676: Start of'ora.asm' on 'rac1' succeeded

CRS-2672: Attemptingto start 'ora.CRSDG.dg' on 'rac1'

CRS-2676: Start of'ora.CRSDG.dg' on 'rac1' succeeded

Configure OracleGrid Infrastructure for a Cluster ... succeeded

第二个节点的执行信息如下：

#/u01/app/oraInventory/orainstRoot.sh

Changing permissionsof /u01/app/oraInventory.

Adding read,writepermissions for group.

Removingread,write,execute permissions for world.

Changing groupnameof /u01/app/oraInventory to dba.

The execution of thescript is complete.

#/u01/app/11.2/grid/root.sh

Performing root useroperation for Oracle 11g

The followingenvironment variables are set as:

ORACLE_OWNER= grid

ORACLE_HOME= /u01/app/11.2/grid

Enter the fullpathname of the local bin directory: [/usr/local/bin]:

The contents of"dbhome" have not changed. No need to overwrite.

The contents of"oraenv" have not changed. No need to overwrite.

The contents of"coraenv" have not changed. No need to overwrite.

Creating /etc/oratabfile...

Entries will beadded to the /etc/oratab file as needed by

DatabaseConfiguration Assistant when a database is created

Finished runninggeneric part of root script.

Now product-specificroot actions will be performed.

Using configurationparameter file: /u01/app/11.2/grid/crs/install/crsconfig_params

Creating tracedirectory

User ignoredPrerequisites during installation

Installing TraceFile Analyzer

User grid has therequired capabilities to run CSSD in realtime mode

OLR initialization -successful

Adding Clusterwareentries to inittab

CRS-4402: The CSSdaemon was started in exclusive mode but found an active CSS daemon on node rac1,number 1, and is terminating

An active clusterwas found during exclusive startup, restarting to join the cluster

Configure OracleGrid Infrastructure for a Cluster ... succeeded

21\. 安装过程继续执行，完成安装任务后点击“Close”。

22\. 安装完成之后以grid用户执行如下命令校验gridinfrastructure安装：

cluvfy stage -post crsinst -n rac1,rac2

分析输出结果，看看grid infrastructure是否安装成功。

23\. 以grid用户执行如下命令查看gridinfrastructure安当前工作状态：

[grid@rac1 ~]$ crsctl check crs //检查CRS整体状态

[grid@rac1 ~]$ crsctl check cluster -all //检查CRS在各个节点的状态

[grid@rac1 ~]$ crsctl stat res -t(或者crs_stat -t -v【10g命令】) //检查CRS资源状态

[grid@rac1 ~]$ olsnodes -n //检查集群节点数

## 5 安装OracleDatabase 11g R2

### 5.1 准备DataBase安装软件

1\. 将p13390677_112040_AIX64-5L_1of7.zip、p13390677_112040_AIX64-5L_2of7.zip上传到oracle用户的家目录中。

2\. 将p13390677_112040_AIX64-5L_1of7.zip、p13390677_112040_AIX64-5L_2of7.zip解压到当前文件夹（root用户执行）：

#cd /home/oracle

#unzip p13390677_112040_AIX64-5L_1of7.zip

#unzip p13390677_112040_AIX64-5L_2of7.zip

3\. 修改解压后的文件夹database的权限：

#chown -R oracle:oinstall/home/oracle/database

### 5.2 使用cluvfy脚本校验系统是否满足安装需求

在安装oracle数据库之前，cluvfy脚本工具还没有安装，所以oracle用户需要调用grid用户目录下的cluvfy工具进行校验，具体步骤如下：

1\. 以oracle用户登录系统，切换当前目录为/u01/11.2.0/grid/bin。

#cd /u01/app/11.2.0/grid/bin

2\. 执行cluvfy脚本校验系统，并将检查结果输出到oracle用户家目录下的report.txt文本文件中。

#./cluvfy stage -pre dbinst -n rac1,rac2>/home/oracle/report.txt

3\. 切换回oracle家目录并使用如下命令查看分析report.txt文件：

#cd //切换回oracle用户家目录

#cat report.txt|grep failed //分析校验脚本输出的内容

### 5.3 开始安装DataBase

1\. 以oracle用户SSH登录rac1节点系统，打开一个命令行终端，切换当前目录为/home/oracle/database。

2\. 在命令行终端中输入如下命令，开启oracle database安装程序。

./runInstaller

3\. 弹出OUI安装程序，取消“安全更新通知配置”，点击“Next”。

4\. 接着弹出一个错误提示框，提示你没有指定账户和邮件地址，点击“Yes”忽略。

5\. 选择“Skip software updates”，点击“Next”。

6\. 选择“Install database software only”，点击“Next”。

7\. 选择如下配置，点击“Next”。

8\. 添加“中文”支持，点击“Next”。

9\. 选择安装“企业版”，点击“Next”。

10\. 选择Oraac了基目录和软件安装位置，点击“Next”。

11\. 选择操作系统组，点击“Next”。

12\. 执行安装条件检查。

13\. 执行安装条件检查时可能出现以下如图的错误：

【ERROR】An internal error occurred withincluster verification framework

Unable to obtain network interface list fromOracle ClusterwarePRCT-1011 : Failed to run "oifcfg". Detailed error:null

可以采用以下方法解决：

一、可能是OCR中记录的网络设置不正确，那可以参考以下处理。

su - root

/u01/app/11.2.0/grid/bin/ocrdump/tmp/dump.ocr1

grep 'css.interfaces' /tmp/dump.ocr1 | awk-F \\] '{print $1}' | awk -F \\. '{print $5}' | sort -u

/u01/app/11.2/grid/bin/oifcfg delif -globalen6 -force

/u01/app/11.2/grid/bin/oifcfg delif -globalen7 -force

su - grid

/u01/app/11.2/grid/bin/oifcfg iflist -p-n

$ /u01/app/11.2/grid/bin/oifcfg iflist -p-n

en8 10.1.0.0 PUBLIC 255.255.255.128

en9 192.168.0.0 PUBLIC 255.255.255.0

#su - grid

/u01/app/11.2/grid/bin/oifcfg setif -globalen9/192.168.0.0:cluster_interconnect

/u01/app/11.2/grid/bin/oifcfg setif -globalen8/10.1.0.0:public

#su - grid

/u01/app/11.2/grid/bin/oifcfg getif

$ /u01/app/11.2/grid/bin/oifcfg getif

en8 192.168.0.0 global cluster_interconnect

en9 10.1.0.0 global public

二、是因为环境变量的问题：

#su - oracle

$unset ORA_NLS10

或者修改ORA_NLS10变量正确，指向export ORA_NLS10=$GRID_HOME/nls/data

这个时候重新的运行./runInstaller

# 关于这个报错,可以参考MOS文章:

11gR2 OUI On AIX Pre-Requisite Check GivesError "Patch IZ97457, IZ89165 Are Missing" [ID 1439940.1]

大意是说在不同的TL级别,补丁号会变.该文章给出了IZ97457和IZ89165在各个TL中所对应的补丁号,所以,你只要打了相应的补丁,那就完全可以无视报错了.

Below are the equivalent APAR's for eachspecific TL:

** Patch IZ89165 **

6100-03 - use AIX APAR IZ89304

6100-04 - use AIX APAR IZ89302

6100-05 - use AIX APAR IZ89300

6100-06 - use AIX APAR IZ89514

7100-00 - use AIX APAR IZ89165

** Patch IZ97457 **

5300-11 - use AIX APAR IZ98424

5300-12 - use AIX APAR IZ98126

6100-04 - use AIX APAR IZ97605

6100-05 - use AIX APAR IZ97457

6100-06 - use AIX APAR IZ96155

7100-00 - use AIX APAR IZ97035

查看当前操作系统版本:

# oslevel -s

6100-06-08-1216

#

查看补丁应用:

# instfix -i -k IZ89514

All filesets for IZ89514 were found.

#

# instfix -i -k IZ96155

All filesets for IZ96155 were found.

#

****

14\. 安装条件检查通过，则显示安装配置汇总信息，点击“Install”。

15\. OUI开始安装DataBase，如图。

16\. 安装过程中会弹出如下执行脚本提示框，以root用户分别在每个节点执行提示框中的脚本，执行完成后点击“OK”。注意：节点RAC1执行之后，才可在RAC2节点执行。

17\. 点击“Close”，结束OracleDataBase软件安装。

## 6 创建Oracle RAC集群数据库

在本次安装配置中使用ASM存储数据库文件，由于在安装grid infrastructure时，已经创建了一个ASM磁盘组OCR_VOTE，在这里我们新建DATA磁盘组来存储我们的数据库文件。Oracle官方建议将Oracle集群文件（OCR和voting_disk）和数据库文件放在一个磁盘组上。在这个生产环境中需要使用快速恢复区和归档配置，所以还需要创建一个用于存放快速恢复区文件和归档文件的磁盘组FRA_ARCHIVE。

### 6.1 创建ASM磁盘组

1\. 以grid用户在SSH登录rac1节点，打开一个命令行终端，输入asmca命令。

2\. 弹出如下ASM管理界面，点击“Create”按钮。

3\. 弹出新建ASM磁盘组对话框，输入如下图所示信息，点击“OK”。

4\. 过一会就会弹出如下创建成功提示框，点击“OK”。

5\. DATA磁盘组创建成功之后的显示界面如下图，接下来创建用于闪回恢复区的FRA_ARCHIVE磁盘组，点击“Create”。

6\. 弹出新建ASM磁盘组对话框，输入如下图所示信息，点击“OK”。

7\. 过一会就会弹出如下创建成功提示框，点击“OK”。

8\. FRA_ARCHIVE磁盘组创建成功之后的显示界面如下图，点击“Exit”，弹出提示框，点击“Yes”。

### 6.2 使用DBCA创建RAC数据库

1\. 以oracle用户Xmanager的Xbrower登录rac1节点，打开一个命令行终端，输入dbca命令。

2\. 弹出如下创建数据库向导，选择Oracle RAC数据库，点击“Next”。

3\. 选择创建数据库，点击“Next”。

4\. 选择“自定义数据库”，点击“Next”。

5\. 输入集群数据库的SID和全局名称，并选择在所有节点上创建集群数据库，点击“Next”。

6\. 这一步选择创建DataBase Control，并启用自动管理任务，点击“Next”。

7\. 为所有账户使用相同密码：changanjie，点击“Next”。

8\. 选择存储类型为ASM，数据区为DATA磁盘组，点击“Next”。

在这一步如果没有找到ASM磁盘需要检查，oracle用户两个节点的组别是否一致。

9\. 此时会弹出ASMSNMP管理账户密码，密码为4.3节中第12步中指定的密码：**dragonsoft** ，点击“OK”。

10\. 指定快速恢复区的数据存放区域为FRA_ARCHIVE磁盘组，并启用归档，点击“Next”。

11\. 数据库组件选择默认，没有自定义脚本，点击“Next”。

12\. 在这一步中需修改字符编码，process数为500，别的标签页上的参数均默认，点击“Next”。

13\. 弹出创建数据数据文件的详细信息，这里可以修改在线日志组个数，表空间大小等参数，点击“Next”。

14\. 选择生成数据库脚本，点击“Finish”。

15\. 弹出一个DBCA汇总信息，点击“OK”。

16\. DBCA首先会生成创建数据库的脚本并保存到指定目录，成功生成脚本后，会弹出一个提示框，点击“OK”，即可开始创建数据库。

17\. 创建数据库过程如图所示。

18\. 数据库创建进程完成之后，会弹出如下密码管理界面，点击“Exit”退出。

19\. 至此Oracle RAC 集群数据库创建完成。

## 7 Oracle RAC集群数据库的简单管理

grid用户查看集群节点个数：

#olsnodes-n

grid用户查看集群状态：

#crsctlstat res -t(或者crs_stat -t-v)

oracle用户关闭数据库:

#sqlplus/ as sysdba

SQL>shutdownimmediate

SQL>exit

Srvctl stop database –d dbid

root用户关闭集群：

#/u01/app/11.2.0/grid/bin/crsctlstop crs

crsctl stop cluster -all

root用户关闭操作系统：

shutdown-F

root用户启动集群：

#/u01/app/11.2.0/grid/bin/crsctlstart crs

oracle用户启动数据库:

#sqlplus/ as sysdba

SQL>startup

SQL>exit

## 8 附录

### 8.1Uninstall/Remove 11.2.0.2 Grid Infrastructure & Database inLinux

出于研究或者测试的目的我们可能已经在平台上安装了11gR2的GridInfrastructure和RACDatabase，因为GI部署的特殊性我们不能直接删除CRS_HOME和一些列脚本的方法来卸载GI和RAC Database软件，所幸在11gR2中Oracle提供了卸载软件的新特性:Deinstall，通过执行Deinstall脚本可以方便地删除Oracle软件产品在系统上的各类配置文件。

具体的卸载步骤如下：

1\. 将平台上现有的数据库迁移走或者物理、逻辑地备份，如果该数据库已经没有任何价值的话使用DBCA删除该数据库及相关服务。

以oracle用户登录系统启动DBCA界面，并选择RACdatabase:

[oracle@rac2~]$ dbca

[](http://www.flickr.com/photos/59721537@N08/6100296874/ "deinstall_11gr2_rac_1 by Maclean Liu, on Flickr")

在step 1 of 2 :operations上选择删除数据库delete a Database

[](http://www.flickr.com/photos/59721537@N08/6099755145/ "deinstall_11gr2_rac_2 by Maclean Liu, on Flickr")

在 step 2 of 2 : List of clusterdatabases上选择所要删除的数据库

[](http://www.flickr.com/photos/59721537@N08/6100300428/ "deinstall_11gr2_rac_3 by Maclean Liu, on Flickr")

逐一删除Cluster环境中所有的Database

2.
使用oracle用户登录**任意节点** 并执行$ORACLE_HOME/deinstall目录下的deinstall脚本





    SQL> select * from v$version;





    BANNER


    --------------------------------------------------------------------------------


    Oracle Database 11g Enterprise Edition Release 11.2.0.2.0 - 64bit Production


    PL/SQL Release 11.2.0.2.0 - Production


    CORE    11.2.0.2.0      Production


    TNS for Linux: Version 11.2.0.2.0 - Production


    NLSRTL Version 11.2.0.2.0 - Production





    SQL> select * from global_name;





    GLOBAL_NAME


    --------------------------------------------------------------------------------


    www.oracledatabase12g.com








    [root@rac2 ~]# su - oracle





    [oracle@rac2 ~]$ cd $ORACLE_HOME/deinstall





    **[oracle@rac2 deinstall]$ ./deinstall**





    Checking for required files and bootstrapping ...


    Please wait ...


    Location of logs /g01/oraInventory/logs/





    ############ ORACLE DEINSTALL & DECONFIG TOOL START ############





    ######################### CHECK OPERATION START #########################


    Install check configuration START





    Checking for existence of the Oracle home location /s01/orabase/product/11.2.0/dbhome_1


    Oracle Home type selected for de-install is: RACDB


    Oracle Base selected for de-install is: /s01/orabase


    Checking for existence of central inventory location /g01/oraInventory


    Checking for existence of the Oracle Grid Infrastructure home /g01/11.2.0/grid


    The following nodes are part of this cluster: rac1,rac2





    Install check configuration END





    Skipping Windows and .NET products configuration check





    Checking Windows and .NET products configuration END





    Network Configuration check config START





    Network de-configuration trace file location:


    /g01/oraInventory/logs/netdc_check2011-08-31_11-19-25-PM.log





    Specify all RAC listeners (do not include SCAN listener) that are to be de-configured [CRS_LISTENER]:





    Network Configuration check config END





    Database Check Configuration START





    Database de-configuration trace file location: /g01/oraInventory/logs/databasedc_check2011-08-31_11-19-39-PM.log





    Use comma as separator when specifying list of values as input





    Specify the list of database names that are configured in this Oracle home []:


    Database Check Configuration END





    Enterprise Manager Configuration Assistant START





    EMCA de-configuration trace file location: /g01/oraInventory/logs/emcadc_check2011-08-31_11-19-46-PM.log





    Enterprise Manager Configuration Assistant END


    Oracle Configuration Manager check START


    OCM check log file location : /g01/oraInventory/logs//ocm_check131.log


    Oracle Configuration Manager check END





    ######################### CHECK OPERATION END #########################





    ####################### CHECK OPERATION SUMMARY #######################


    Oracle Grid Infrastructure Home is: /g01/11.2.0/grid


    The cluster node(s) on which the Oracle home de-installation will be performed are:rac1,rac2


    Oracle Home selected for de-install is: /s01/orabase/product/11.2.0/dbhome_1


    Inventory Location where the Oracle home registered is: /g01/oraInventory


    Skipping Windows and .NET products configuration check


    Following RAC listener(s) will be de-configured: CRS_LISTENER


    No Enterprise Manager configuration to be updated for any database(s)


    No Enterprise Manager ASM targets to update


    No Enterprise Manager listener targets to migrate


    Checking the config status for CCR


    rac1 : Oracle Home exists with CCR directory, but CCR is not configured


    rac2 : Oracle Home exists with CCR directory, but CCR is not configured


    CCR check is finished


    Do you want to continue (y - yes, n - no)? [n]: y


    A log of this session will be written to: '/g01/oraInventory/logs/deinstall_deconfig2011-08-31_11-19-23-PM.out'


    Any error messages from this session will be written to: '/g01/oraInventory/logs/deinstall_deconfig2011-08-31_11-19-23-PM.err'





    ######################## CLEAN OPERATION START ########################





    Enterprise Manager Configuration Assistant START





    EMCA de-configuration trace file location: /g01/oraInventory/logs/emcadc_clean2011-08-31_11-19-46-PM.log





    Updating Enterprise Manager ASM targets (if any)


    Updating Enterprise Manager listener targets (if any)


    Enterprise Manager Configuration Assistant END


    Database de-configuration trace file location: /g01/oraInventory/logs/databasedc_clean2011-08-31_11-20-00-PM.log





    Network Configuration clean config START





    Network de-configuration trace file location: /g01/oraInventory/logs/netdc_clean2011-08-31_11-20-00-PM.log





    De-configuring RAC listener(s): CRS_LISTENER





    De-configuring listener: CRS_LISTENER


        Stopping listener: CRS_LISTENER


        Listener stopped successfully.


        Unregistering listener: CRS_LISTENER


        Listener unregistered successfully.


    Listener de-configured successfully.





    De-configuring Listener configuration file on all nodes...


    Listener configuration file de-configured successfully.





    De-configuring Naming Methods configuration file on all nodes...


    Naming Methods configuration file de-configured successfully.





    De-configuring Local Net Service Names configuration file on all nodes...


    Local Net Service Names configuration file de-configured successfully.





    De-configuring Directory Usage configuration file on all nodes...


    Directory Usage configuration file de-configured successfully.





    De-configuring backup files on all nodes...


    Backup files de-configured successfully.





    The network configuration has been cleaned up successfully.





    Network Configuration clean config END





    Oracle Configuration Manager clean START


    OCM clean log file location : /g01/oraInventory/logs//ocm_clean131.log


    Oracle Configuration Manager clean END


    Removing Windows and .NET products configuration END


    Oracle Universal Installer clean START





    Detach Oracle home '/s01/orabase/product/11.2.0/dbhome_1' from the central inventory on the local node : Done





    Delete directory '/s01/orabase/product/11.2.0/dbhome_1' on the local node : Done





    Delete directory '/s01/orabase' on the local node : Done





    Detach Oracle home '/s01/orabase/product/11.2.0/dbhome_1' from the central inventory on the remote nodes 'rac1' : Done





    Delete directory '/s01/orabase/product/11.2.0/dbhome_1' on the remote nodes 'rac1' : Done





    Delete directory '/s01/orabase' on the remote nodes 'rac1' : Done





    Oracle Universal Installer cleanup was successful.





    Oracle Universal Installer clean END





    Oracle install clean START





    Clean install operation removing temporary directory '/tmp/deinstall2011-08-31_11-19-18PM' on node 'rac2'


    Clean install operation removing temporary directory '/tmp/deinstall2011-08-31_11-19-18PM' on node 'rac1'





    Oracle install clean END





    ######################### CLEAN OPERATION END #########################





    ####################### CLEAN OPERATION SUMMARY #######################


    Following RAC listener(s) were de-configured successfully: CRS_LISTENER


    Cleaning the config for CCR


    As CCR is not configured, so skipping the cleaning of CCR configuration


    CCR clean is finished


    Skipping Windows and .NET products configuration clean


    Successfully detached Oracle home '/s01/orabase/product/11.2.0/dbhome_1' from the central inventory on the local node.


    Successfully deleted directory '/s01/orabase/product/11.2.0/dbhome_1' on the local node.


    Successfully deleted directory '/s01/orabase' on the local node.


    Successfully detached Oracle home '/s01/orabase/product/11.2.0/dbhome_1' from the central inventory on the remote nodes 'rac1'.


    Successfully deleted directory '/s01/orabase/product/11.2.0/dbhome_1' on the remote nodes 'rac1'.


    Successfully deleted directory '/s01/orabase' on the remote nodes 'rac1'.


    Oracle Universal Installer cleanup was successful.





    Oracle deinstall tool successfully cleaned up temporary directories.


    #######################################################################





    ############# ORACLE DEINSTALL & DECONFIG TOOL END #############

以上deinstall脚本会删除所有节点上的$ORACLE_HOME下的RDBMS软件，并从centralinventory中将已经卸载的RDBMS软件注销，注意这种操作是不可逆的！

3.

使用root用户登录在所有节点上注意运行”$ORA_CRS_HOME/crs/install/rootcrs.pl-verbose -deconfig -force”的命令，注意在最后一个节点不要运行该命令。举例来说如果你有2个节点的话，就只要在一个节点上运行上述命令即可：


    [root@rac1 ~]# **$ORA_CRS_HOME/crs/install/rootcrs.pl -verbose -deconfig -force**





    Using configuration parameter file: /g01/11.2.0/grid/crs/install/crsconfig_params


    Network exists: 1/172.1.1.0/255.255.255.0/eth0, type static


    VIP exists: /rac1-vip/172.1.1.206/172.1.1.0/255.255.255.0/eth0, hosting node rac1


    VIP exists: /rac2-vip/172.1.1.207/172.1.1.0/255.255.255.0/eth0, hosting node rac2


    GSD exists


    ONS exists: Local port 6100, remote port 6200, EM port 2016


    ACFS-9200: Supported


    CRS-2673: Attempting to stop 'ora.registry.acfs' on 'rac1'


    CRS-2677: Stop of 'ora.registry.acfs' on 'rac1' succeeded


    CRS-2791: Starting shutdown of Oracle High Availability Services-managed resources on 'rac1'


    CRS-2673: Attempting to stop 'ora.crsd' on 'rac1'


    CRS-2790: Starting shutdown of Cluster Ready Services-managed resources on 'rac1'


    CRS-2673: Attempting to stop 'ora.oc4j' on 'rac1'


    CRS-2673: Attempting to stop 'ora.DATA.dg' on 'rac1'


    CRS-2673: Attempting to stop 'ora.FRA.dg' on 'rac1'


    CRS-2673: Attempting to stop 'ora.SYSTEMDG.dg' on 'rac1'


    CRS-2677: Stop of 'ora.oc4j' on 'rac1' succeeded


    CRS-2672: Attempting to start 'ora.oc4j' on 'rac2'


    CRS-2676: Start of 'ora.oc4j' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.DATA.dg' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.SYSTEMDG.dg' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.FRA.dg' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.asm' on 'rac1'


    CRS-2677: Stop of 'ora.asm' on 'rac1' succeeded


    CRS-2792: Shutdown of Cluster Ready Services-managed resources on 'rac1' has completed


    CRS-2677: Stop of 'ora.crsd' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.ctssd' on 'rac1'


    CRS-2673: Attempting to stop 'ora.evmd' on 'rac1'


    CRS-2673: Attempting to stop 'ora.asm' on 'rac1'


    CRS-2673: Attempting to stop 'ora.mdnsd' on 'rac1'


    CRS-2673: Attempting to stop 'ora.drivers.acfs' on 'rac1'


    CRS-2677: Stop of 'ora.asm' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.cluster_interconnect.haip' on 'rac1'


    CRS-2677: Stop of 'ora.drivers.acfs' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.evmd' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.cluster_interconnect.haip' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.mdnsd' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.ctssd' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.cssd' on 'rac1'


    CRS-2677: Stop of 'ora.cssd' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.crf' on 'rac1'


    CRS-2673: Attempting to stop 'ora.diskmon' on 'rac1'


    CRS-2677: Stop of 'ora.diskmon' on 'rac1' succeeded


    CRS-2677: Stop of 'ora.crf' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.gipcd' on 'rac1'


    CRS-2677: Stop of 'ora.gipcd' on 'rac1' succeeded


    CRS-2673: Attempting to stop 'ora.gpnpd' on 'rac1'


    CRS-2677: Stop of 'ora.gpnpd' on 'rac1' succeeded


    CRS-2793: Shutdown of Oracle High Availability Services-managed resources on 'rac1' has completed


    CRS-4133: Oracle High Availability Services has been stopped.


    Successfully deconfigured Oracle clusterware stack on this node

4.在最后的节点(lastnode)以root用户执行”$ORA_CRS_HOME/crs/install/rootcrs.pl-verbose -deconfig -force -lastnode”命令，该命令会清空OCR和Votedisk :


    [root@rac2 ~]# **$ORA_CRS_HOME/crs/install/rootcrs.pl -verbose -deconfig -force -lastnode**





    Using configuration parameter file: /g01/11.2.0/grid/crs/install/crsconfig_params


    CRS resources for listeners are still configured


    Network exists: 1/172.1.1.0/255.255.255.0/eth0, type static


    VIP exists: /rac1-vip/172.1.1.206/172.1.1.0/255.255.255.0/eth0, hosting node rac1


    VIP exists: /rac2-vip/172.1.1.207/172.1.1.0/255.255.255.0/eth0, hosting node rac2


    GSD exists


    ONS exists: Local port 6100, remote port 6200, EM port 2016


    ACFS-9200: Supported


    CRS-2673: Attempting to stop 'ora.registry.acfs' on 'rac2'


    CRS-2677: Stop of 'ora.registry.acfs' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.crsd' on 'rac2'


    CRS-2790: Starting shutdown of Cluster Ready Services-managed resources on 'rac2'


    CRS-2673: Attempting to stop 'ora.DATA.dg' on 'rac2'


    CRS-2673: Attempting to stop 'ora.FRA.dg' on 'rac2'


    CRS-2673: Attempting to stop 'ora.SYSTEMDG.dg' on 'rac2'


    CRS-2673: Attempting to stop 'ora.oc4j' on 'rac2'


    CRS-2677: Stop of 'ora.oc4j' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.DATA.dg' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.SYSTEMDG.dg' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.FRA.dg' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.asm' on 'rac2'


    CRS-2677: Stop of 'ora.asm' on 'rac2' succeeded


    CRS-2792: Shutdown of Cluster Ready Services-managed resources on 'rac2' has completed


    CRS-2677: Stop of 'ora.crsd' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.ctssd' on 'rac2'


    CRS-2673: Attempting to stop 'ora.evmd' on 'rac2'


    CRS-2673: Attempting to stop 'ora.asm' on 'rac2'


    CRS-2677: Stop of 'ora.asm' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.cluster_interconnect.haip' on 'rac2'


    CRS-2677: Stop of 'ora.evmd' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.cluster_interconnect.haip' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.ctssd' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.cssd' on 'rac2'


    CRS-2677: Stop of 'ora.cssd' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.diskmon' on 'rac2'


    CRS-2677: Stop of 'ora.diskmon' on 'rac2' succeeded


    CRS-2672: Attempting to start 'ora.cssdmonitor' on 'rac2'


    CRS-2676: Start of 'ora.cssdmonitor' on 'rac2' succeeded


    CRS-2672: Attempting to start 'ora.cssd' on 'rac2'


    CRS-2672: Attempting to start 'ora.diskmon' on 'rac2'


    CRS-2676: Start of 'ora.diskmon' on 'rac2' succeeded


    CRS-2676: Start of 'ora.cssd' on 'rac2' succeeded


    CRS-4611: Successful deletion of voting disk +SYSTEMDG.


    ASM de-configuration trace file location: /tmp/asmcadc_clean2011-08-31_11-55-52-PM.log


    ASM Clean Configuration START


    ASM Clean Configuration END





    ASM with SID +ASM1 deleted successfully. Check /tmp/asmcadc_clean2011-08-31_11-55-52-PM.log for details.





    CRS-2791: Starting shutdown of Oracle High Availability Services-managed resources on 'rac2'


    CRS-2673: Attempting to stop 'ora.mdnsd' on 'rac2'


    CRS-2673: Attempting to stop 'ora.ctssd' on 'rac2'


    CRS-2673: Attempting to stop 'ora.asm' on 'rac2'


    CRS-2677: Stop of 'ora.asm' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.mdnsd' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.ctssd' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.cssd' on 'rac2'


    CRS-2677: Stop of 'ora.cssd' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.gipcd' on 'rac2'


    CRS-2673: Attempting to stop 'ora.diskmon' on 'rac2'


    CRS-2677: Stop of 'ora.gipcd' on 'rac2' succeeded


    CRS-2673: Attempting to stop 'ora.gpnpd' on 'rac2'


    CRS-2677: Stop of 'ora.diskmon' on 'rac2' succeeded


    CRS-2677: Stop of 'ora.gpnpd' on 'rac2' succeeded


    CRS-2793: Shutdown of Oracle High Availability Services-managed resources on 'rac2' has completed


    CRS-4133: Oracle High Availability Services has been stopped.


    Successfully deconfigured Oracle clusterware stack on this node

5.在任意节点以GridInfrastructure拥有者用户执行”$ORA_CRS_HOME/deinstall/deinstall”脚本:


    [root@rac1 ~]# su - grid


    [grid@rac1 ~]$ cd $ORA_CRS_HOME


    [grid@rac1 grid]$ cd deinstall/





    [grid@rac1 deinstall]$ cat deinstall


    #!/bin/sh


    #


    # $Header: install/utl/scripts/db/deinstall /main/3 2010/05/28 20:12:57 ssampath Exp $


    #


    # Copyright (c) 2005, 2010, Oracle and/or its affiliates. All rights reserved.


    #


    #    NAME


    #      deinstall - wrapper script that calls deinstall tool.


    #


    #    DESCRIPTION


    #      This script will set all the necessary variables and call the tools


    #      entry point.


    #


    #    NOTES


    #


    #


    #    MODIFIED   (MM/DD/YY)


    #    mwidjaja    04/29/10 - XbranchMerge mwidjaja_bug-9579184 from


    #                           st_install_11.2.0.1.0


    #    mwidjaja    04/15/10 - Added SHLIB_PATH for HP-PARISC


    #    mwidjaja    01/14/10 - XbranchMerge mwidjaja_bug-9269768 from


    #                           st_install_11.2.0.1.0


    #    mwidjaja    01/14/10 - Fix help message for params


    #    ssampath    12/24/09 - Fix for bug 9227535. Remove legacy version_check


    #                           function


    #    ssampath    12/01/09 - XbranchMerge ssampath_bug-9167533 from


    #                           st_install_11.2.0.1.0


    #    ssampath    11/30/09 - Set umask to 022.


    #    prsubram    10/12/09 - XbranchMerge prsubram_bug-9005648 from main


    #    prsubram    10/08/09 - Compute ARCHITECTURE_FLAG in the script


    #    prsubram    09/15/09 - Setting LIBPATH for AIX


    #    prsubram    09/10/09 - Add AIX specific code check java version


    #    prsubram    09/10/09 - Change TOOL_DIR to BOOTSTRAP_DIR in java cmd


    #                           invocation of bug#8874160


    #    prsubram    09/08/09 - Change the default shell to /usr/xpg4/bin/sh on


    #                           SunOS


    #    prsubram    09/03/09 - Removing -d64 for client32 homes for the bug8859294


    #    prsubram    06/22/09 - Resolve port specific id cmd issue


    #    ssampath    06/02/09 - Fix for bug 8566942


    #    ssampath    05/19/09 - Move removal of /tmp/deinstall to java


    #                           code.


    #    prsubram    04/30/09 - Fix for the bug#8474891


    #    mwidjaja    04/29/09 - Added user check between the user running the


    #                           script and inventory owner


    #    ssampath    04/29/09 - Changes to make error message better when deinstall


    #                           tool is invoked from inside ORACLE_HOME and -home


    #                           is passed.


    #    ssampath    04/15/09 - Fix for bug 8414555


    #    prsubram    04/09/09 - LD_LIBRARY_PATH is ported for sol,hp-ux & aix


    #    mwidjaja    03/26/09 - Disallow -home for running from OH


    #    ssampath    03/24/09 - Fix for bug 8339519


    #    wyou        02/25/09 - restructure the ohome check


    #    wyou        02/25/09 - change the error msg for directory existance check


    #    wyou        02/12/09 - add directory existance check


    #    wyou        02/09/09 - add the check for the writablity for the oracle


    #                           home passed-in


    #    ssampath    01/21/09 - Add oui/lib to LD_LIBRARY_PATH


    #    poosrini    01/07/09 - LOG related changes


    #    ssampath    11/24/08 - Create /main/osds/unix branch


    #    dchriste    10/30/08 - eliminate non-generic tools like 'cut'


    #    ssampath    08/18/08 - Pickup srvm.jar from JLIB directory.


    #    ssampath    07/30/08 - Add http_client.jar and OraCheckpoint.jar to


    #                           CLASSPATH


    #    ssampath    07/08/08 - assistantsCommon.jar and netca.jar location has


    #                           changed.


    #    ssampath    04/11/08 - If invoking the tool from installed home, JRE_HOME


    #                           should be set to $OH/jdk/jre.


    #    ssampath    04/09/08 - Add logic to instantiate ORA_CRS_HOME, JAVA_HOME


    #                           etc.,


    #    ssampath    04/03/08 - Pick up ldapjclnt11.jar


    #    idai        04/03/08 - remove assistantsdc.jar and netcadc.jar


    #    bktripat    02/23/07 -


    #    khsingh     07/18/06 - add osdbagrp fix


    #    khsingh     07/07/06 - fix regression


    #    khsingh     06/20/06 - fix bug 5228203


    #    bktripat    06/12/06 - Fix for bug 5246802


    #    bktripat    05/08/06 -


    #    khsingh     05/08/06 - fix tool to run from any parent directory


    #    khsingh     05/08/06 - fix LD_LIBRARY_PATH to have abs. path


    #    ssampath    05/01/06 - Fix for bug 5198219


    #    bktripat    04/21/06 - Fix for bug 5074246


    #    khsingh     04/11/06 - fix bug 5151658


    #    khsingh     04/08/06 - Add WA for bugs 5006414 & 5093832


    #    bktripat    02/08/06 - Fix for bug 5024086 & 5024061


    #    bktripat    01/24/06 -


    #    mstalin     01/23/06 - Add lib to pick libOsUtils.so


    #    bktripat    01/19/06 - adding library changes


    #    rahgupta    01/19/06 -


    #    bktripat    01/19/06 -


    #    mstalin     01/17/06 - Modify the assistants deconfig jar file name


    #    rahgupta    01/17/06 - updating emcp classpath


    #    khsingh     01/17/06 - export ORACLE_HOME


    #    khsingh     01/17/06 - fix for CRS deconfig.


    #    hying       01/17/06 - netcadc.jar


    #    bktripat    01/16/06 -


    #    ssampath    01/16/06 -


    #    bktripat    01/11/06 -


    #    clo         01/10/06 - add EMCP entries


    #    hying       01/10/06 - netcaDeconfig.jar


    #    mstalin     01/09/06 - Add OraPrereqChecks.jar


    #    mstalin     01/09/06 -


    #    khsingh     01/09/06 -


    #    mstalin     01/09/06 - Add additional jars for assistants


    #    ssampath    01/09/06 - removing parseOracleHome temporarily


    #    ssampath    01/09/06 -


    #    khsingh     01/08/06 - fix for CRS deconfig


    #    ssampath    12/08/05 - added java version check


    #    ssampath    12/08/05 - initial run,minor bugs fixed


    #    ssampath    12/07/05 - Creation


    #





    #MACROS





    if [ -z "$UNAME" ]; then UNAME="/bin/uname"; fi


    if [ -z "$ECHO" ]; then ECHO="/bin/echo"; fi


    if [ -z "$AWK" ]; then AWK="/bin/awk"; fi


    if [ -z "$ID" ]; then ID="/usr/bin/id"; fi


    if [ -z "$DIRNAME" ]; then DIRNAME="/usr/bin/dirname"; fi


    if [ -z "$FILE" ]; then FILE="/usr/bin/file"; fi





    if [ "`$UNAME`" = "SunOS" ]


    then


        if [ -z "${_xpg4ShAvbl_deconfig}" ]


        then


            _xpg4ShAvbl_deconfig=1


            export _xpg4ShAvbl_deconfig


            /usr/xpg4/bin/sh $0 "$@"


            exit $?


        fi


            AWK="/usr/xpg4/bin/awk"


    fi





    # Set umask to 022 always.


    umask 022





    INSTALLED_VERSION_FLAG=true


    ARCHITECTURE_FLAG=64





    TOOL_ARGS=$* # initialize this always.





    # Since the OTN and the installed version of the tool is same, only way to


    # differentiate is through the instantated variable ORA_CRS_HOME.  If it is


    # NOT instantiated, then the tool is a downloaded version.


    # Set HOME_VER to true based on the value of $INSTALLED_VERSION_FLAG


    if [ x"$INSTALLED_VERSION_FLAG" = x"true" ]


    then


       ORACLE_HOME=/g01/11.2.0/grid


       HOME_VER=1     # HOME_VER


       TOOL_ARGS="$ORACLE_HOME $TOOL_ARGS"


    else


       HOME_VER=0


    fi





    # Save current working directory


    CURR_DIR=`pwd`





    # If CURR_DIR is different from TOOL_DIR get that location and cd into it.


    TOOL_REL_PATH=`$DIRNAME $0`


    cd $TOOL_REL_PATH





    DOT=`$ECHO $TOOL_REL_PATH | $AWK -F'/' '{ print $1}'`





    if [ "$DOT" = "." ];


    then


      TOOL_DIR=$CURR_DIR/$TOOL_REL_PATH


    elif [ `expr "$DOT" : '.*'` -gt 0 ];


    then


      TOOL_DIR=$CURR_DIR/$TOOL_REL_PATH


    else


      TOOL_DIR=$TOOL_REL_PATH


    fi





    # Check if this script is run as root.  If so, then error out.


    # This is fix for bug 5024086.





    RUID=`$ID|$AWK -F\( '{print $2}'|$AWK -F\) '{print $1}'`


    if [ ${RUID} = "root" ];then


     $ECHO "You must not be logged in as root to run $0."


     $ECHO "Log in as Oracle user and rerun $0."


     exit $ROOT_USER


    fi





    # DEFINE FUNCTIONS BELOW


    computeArchFlag() {


       TOOL_HOME=$1


       case `$UNAME` in


          HP-UX)


             if [ "`/usr/bin/file $TOOL_HOME/bin/kfod | $AWK -F\: '{print $2}' | $AWK -F\- '{print $2}' | $AWK '{print $1}'`" = "64" ];then


                ARCHITECTURE_FLAG="-d64"


             fi


          ;;


          AIX)


             if [ "`/usr/bin/file $TOOL_HOME/bin/kfod | $AWK -F\: '{print $2}' | $AWK '{print $1}' | $AWK -F\- '{print $1}'`" = "64" ];then


                ARCHITECTURE_FLAG="-d64"


             fi


          ;;


          *)


             if [ "`/usr/bin/file $TOOL_HOME/bin/kfod | $AWK -F\: '{print $2}' | $AWK '{print $2}' | $AWK -F\- '{print $1}'`" = "64" ];then


                ARCHITECTURE_FLAG="-d64"


             fi


          ;;


       esac


    }





    if [ $HOME_VER = 1 ];


    then


       $ECHO "Checking for required files and bootstrapping ..."


       $ECHO "Please wait ..."


       TEMP_LOC=`$ORACLE_HOME/perl/bin/perl $ORACLE_HOME/deinstall/bootstrap.pl $HOME_VER $TOOL_ARGS`


       TOOL_DIR=$TEMP_LOC


    else


       TEMP_LOC=`$TOOL_DIR/perl/bin/perl $TOOL_DIR/bootstrap.pl $HOME_VER $TOOL_ARGS`


    fi





    computeArchFlag $TOOL_DIR





    $TOOL_DIR/perl/bin/perl $TOOL_DIR/deinstall.pl $HOME_VER $TEMP_LOC $TOOL_DIR $ARCHITECTURE_FLAG $TOOL_ARGS





    **[grid@rac1 deinstall]$ ./deinstall**





    Checking for required files and bootstrapping ...


    Please wait ...


    Location of logs /tmp/deinstall2011-08-31_11-59-55PM/logs/





    ############ ORACLE DEINSTALL & DECONFIG TOOL START ############





    ######################### CHECK OPERATION START #########################


    Install check configuration START





    Checking for existence of the Oracle home location /g01/11.2.0/grid


    Oracle Home type selected for de-install is: CRS


    Oracle Base selected for de-install is: /g01/orabase


    Checking for existence of central inventory location /g01/oraInventory


    Checking for existence of the Oracle Grid Infrastructure home /g01/11.2.0/grid


    The following nodes are part of this cluster: rac1,rac2





    Install check configuration END





    Skipping Windows and .NET products configuration check





    Checking Windows and .NET products configuration END





    Traces log file: /tmp/deinstall2011-08-31_11-59-55PM/logs//crsdc.log


    Enter an address or the name of the virtual IP used on node "rac1"[rac1-vip]


     >





    The following information can be collected by running "/sbin/ifconfig -a" on node "rac1"


    Enter the IP netmask of Virtual IP "172.1.1.206" on node "rac1"[255.255.255.0]


     >





    Enter the network interface name on which the virtual IP address "172.1.1.206" is active


     >





    Enter an address or the name of the virtual IP used on node "rac2"[rac2-vip]


     >





    The following information can be collected by running "/sbin/ifconfig -a" on node "rac2"


    Enter the IP netmask of Virtual IP "172.1.1.207" on node "rac2"[255.255.255.0]


     >





    Enter the network interface name on which the virtual IP address "172.1.1.207" is active


     >





    Enter an address or the name of the virtual IP used on node "rac2"[rac2-vip]


     >





    The following information can be collected by running "/sbin/ifconfig -a" on node "rac1"


    Enter the IP netmask of Virtual IP "172.1.1.204" on node "rac3"[255.255.255.0]


     >





    Enter the network interface name on which the virtual IP address "172.1.1.166" is active


     >





    Enter an address or the name of the virtual IP[]


     >





    Network Configuration check config START





    Network de-configuration trace file location: /tmp/deinstall2011-08-31_11-59-55PM/logs/


    netdc_check2011-09-01_12-01-50-AM.log





    Specify all RAC listeners (do not include SCAN listener) that are to be de-configured [LISTENER,LISTENER_SCAN1]:





    Network Configuration check config END





    Asm Check Configuration START





    ASM de-configuration trace file location: /tmp/deinstall2011-08-31_11-59-55PM/logs/


    asmcadc_check2011-09-01_12-01-51-AM.log





    ASM configuration was not detected in this Oracle home. Was ASM configured in this Oracle home (y|n) [n]:


    ASM was not detected in the Oracle Home





    ######################### CHECK OPERATION END #########################





    ####################### CHECK OPERATION SUMMARY #######################


    Oracle Grid Infrastructure Home is: /g01/11.2.0/grid


    The cluster node(s) on which the Oracle home de-installation will be performed are:rac1,rac2,rac3


    Oracle Home selected for de-install is: /g01/11.2.0/grid


    Inventory Location where the Oracle home registered is: /g01/oraInventory


    Skipping Windows and .NET products configuration check


    Following RAC listener(s) will be de-configured: LISTENER,LISTENER_SCAN1


    ASM was not detected in the Oracle Home


    Do you want to continue (y - yes, n - no)? [n]: y


    A log of this session will be written to: '/tmp/deinstall2011-08-31_11-59-55PM/logs/deinstall_deconfig2011-09-01_12-01-15-AM.out'


    Any error messages from this session will be written to: '/tmp/deinstall2011-08-31_11-59-55PM/logs/deinstall_deconfig2011-09-01_12-01-15-AM.err'





    ######################## CLEAN OPERATION START ########################


    ASM de-configuration trace file location: /tmp/deinstall2011-08-31_11-59-55PM/logs/asmcadc_clean2011-09-01_12-02-00-AM.log


    ASM Clean Configuration END





    Network Configuration clean config START





    Network de-configuration trace file location: /tmp/deinstall2011-08-31_11-59-55PM/logs/netdc_clean2011-09-01_12-02-00-AM.log





    De-configuring RAC listener(s): LISTENER,LISTENER_SCAN1





    De-configuring listener: LISTENER


        Stopping listener: LISTENER


        Warning: Failed to stop listener. Listener may not be running.


    Listener de-configured successfully.





    De-configuring listener: LISTENER_SCAN1


        Stopping listener: LISTENER_SCAN1


        Warning: Failed to stop listener. Listener may not be running.


    Listener de-configured successfully.





    De-configuring Naming Methods configuration file on all nodes...


    Naming Methods configuration file de-configured successfully.





    De-configuring Local Net Service Names configuration file on all nodes...


    Local Net Service Names configuration file de-configured successfully.





    De-configuring Directory Usage configuration file on all nodes...


    Directory Usage configuration file de-configured successfully.





    De-configuring backup files on all nodes...


    Backup files de-configured successfully.





    The network configuration has been cleaned up successfully.





    Network Configuration clean config END





    ---------------------------------------->





    The deconfig command below can be executed in parallel on all the remote nodes.


    Execute the command on  the local node after the execution completes on all the remote nodes.





    Run the following command as the root user or the administrator on node "rac3".





    /tmp/deinstall2011-08-31_11-59-55PM/perl/bin/perl -I/tmp/deinstall2011-08-31_11-59-55PM/perl/lib


    -I/tmp/deinstall2011-08-31_11-59-55PM/crs/install /tmp/deinstall2011-08-31_11-59-55PM/crs/install/rootcrs.pl


    -force  -deconfig -paramfile "/tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp"





    Run the following command as the root user or the administrator on node "rac2".





    /tmp/deinstall2011-08-31_11-59-55PM/perl/bin/perl -I/tmp/deinstall2011-08-31_11-59-55PM/perl/lib


    -I/tmp/deinstall2011-08-31_11-59-55PM/crs/install /tmp/deinstall2011-08-31_11-59-55PM/crs/install/rootcrs.pl -force


    -deconfig -paramfile "/tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp"





    Run the following command as the root user or the administrator on node "rac1".





    /tmp/deinstall2011-08-31_11-59-55PM/perl/bin/perl -I/tmp/deinstall2011-08-31_11-59-55PM/perl/lib


    -I/tmp/deinstall2011-08-31_11-59-55PM/crs/install /tmp/deinstall2011-08-31_11-59-55PM/crs/install/rootcrs.pl


    -force  -deconfig -paramfile "/tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp"


    -lastnode





    Press Enter after you finish running the above commands





    **执行 deinstall过程中会要求以root用户在所有平台上执行相关命令**





    su - root





    [root@rac3 ~]# /tmp/deinstall2011-08-31_11-59-55PM/perl/bin/perl -I/tmp/deinstall2011-08-31_11-59-55PM/perl/lib


    -I/tmp/deinstall2011-08-31_11-59-55PM/crs/install /tmp/deinstall2011-08-31_11-59-55PM/crs/install/rootcrs.pl -force


    -deconfig -paramfile "/tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp"


    Using configuration parameter file: /tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp


    PRCR-1119 : Failed to look up CRS resources of ora.cluster_vip_net1.type type


    PRCR-1068 : Failed to query resources


    Cannot communicate with crsd


    PRCR-1070 : Failed to check if resource ora.gsd is registered


    Cannot communicate with crsd


    PRCR-1070 : Failed to check if resource ora.ons is registered


    Cannot communicate with crsd





    ACFS-9200: Supported


    CRS-4535: Cannot communicate with Cluster Ready Services


    CRS-4000: Command Stop failed, or completed with errors.


    CRS-4544: Unable to connect to OHAS


    CRS-4000: Command Stop failed, or completed with errors.


    Successfully deconfigured Oracle clusterware stack on this node





    [root@rac2 ~]# /tmp/deinstall2011-08-31_11-59-55PM/perl/bin/perl -I/tmp/deinstall2011-08-31_11-59-55PM/perl/lib -I/tmp/deinstall2011-08-31_11-59-55PM/crs/install /tmp/deinstall2011-08-31_11-59-55PM/crs/install/rootcrs.pl -force  -deconfig -paramfile


    "/tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp"


    Using configuration parameter file: /tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp


    Usage: srvctl [command] [object] []


        commands: enable|disable|start|stop|status|add|remove|modify|getenv|setenv|unsetenv|config


        objects: database|service|asm|diskgroup|listener|home|ons


    For detailed help on each command and object and its options use:


      srvctl [command] -h or


      srvctl [command] [object] -h


    PRKO-2012 : nodeapps object is not supported in Oracle Restart


    ACFS-9200: Supported


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Stop failed, or completed with errors.


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Stop failed, or completed with errors.


    You must kill crs processes or reboot the system to properly


    cleanup the processes started by Oracle clusterware


    ACFS-9313: No ADVM/ACFS installation detected.


    Either /etc/oracle/olr.loc does not exist or is not readable


    Make sure the file exists and it has read and execute access


    Failure in execution (rc=-1, 256, No such file or directory) for command 1 /etc/init.d/ohasd deinstall


    error: package cvuqdisk is not installed


    Successfully deconfigured Oracle clusterware stack on this node





    [root@rac1 ~]# /tmp/deinstall2011-08-31_11-59-55PM/perl/bin/perl -I/tmp/deinstall2011-08-31_11-59-55PM/perl/lib


    -I/tmp/deinstall2011-08-31_11-59-55PM/crs/install /tmp/deinstall2011-08-31_11-59-55PM/crs/install/rootcrs.pl -force


    -deconfig -paramfile "/tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp" -lastnode


    Using configuration parameter file: /tmp/deinstall2011-08-31_11-59-55PM/response/deinstall_Ora11g_gridinfrahome1.rsp


    Adding daemon to inittab


    crsexcl failed to start


    Failed to start the Clusterware. Last 20 lines of the alert log follow:


    2011-08-31 23:36:55.813


    [ctssd(4067)]CRS-2408:The clock on host rac1 has been updated by the Cluster Time Synchronization Service to be synchronous with the mean cluster time.


    2011-08-31 23:38:23.855


    [ctssd(4067)]CRS-2408:The clock on host rac1 has been updated by the Cluster Time Synchronization Service to be synchronous with the mean cluster time.


    2011-08-31 23:39:03.873


    [ctssd(4067)]CRS-2408:The clock on host rac1 has been updated by the Cluster Time Synchronization Service to be synchronous with the mean cluster time.


    2011-08-31 23:39:11.707


    [/g01/11.2.0/grid/bin/orarootagent.bin(4559)]CRS-5822:Agent '/g01/11.2.0/grid/bin/orarootagent_root'


    disconnected from server. Details at (:CRSAGF00117:) {0:2:27} in


    /g01/11.2.0/grid/log/rac1/agent/crsd/orarootagent_root/orarootagent_root.log.


    2011-08-31 23:39:12.725


    [ctssd(4067)]CRS-2405:The Cluster Time Synchronization Service on host rac1 is shutdown by user


    2011-08-31 23:39:12.764


    [mdnsd(3868)]CRS-5602:mDNS service stopping by request.


    2011-08-31 23:39:13.987


    [/g01/11.2.0/grid/bin/orarootagent.bin(3892)]CRS-5016:Process "/g01/11.2.0/grid/bin/acfsload"


    spawned by agent "/g01/11.2.0/grid/bin/orarootagent.bin" for action "check" failed:


    details at "(:CLSN00010:)" in "/g01/11.2.0/grid/log/rac1/agent/ohasd/orarootagent_root/orarootagent_root.log"


    2011-08-31 23:39:27.121


    [cssd(3968)]CRS-1603:CSSD on node rac1 shutdown by user.


    2011-08-31 23:39:27.130


    [ohasd(3639)]CRS-2767:Resource state recovery not attempted for 'ora.cssdmonitor' as its target state is OFFLINE


    2011-08-31 23:39:31.926


    [gpnpd(3880)]CRS-2329:GPNPD on node rac1 shutdown.





    Usage: srvctl [command] [object] []


        commands: enable|disable|start|stop|status|add|remove|modify|getenv|setenv|unsetenv|config


        objects: database|service|asm|diskgroup|listener|home|ons


    For detailed help on each command and object and its options use:


      srvctl [command] -h or


      srvctl [command] [object] -h


    PRKO-2012 : scan_listener object is not supported in Oracle Restart


    Usage: srvctl [command] [object] []


        commands: enable|disable|start|stop|status|add|remove|modify|getenv|setenv|unsetenv|config


        objects: database|service|asm|diskgroup|listener|home|ons


    For detailed help on each command and object and its options use:


      srvctl [command] -h or


      srvctl [command] [object] -h


    PRKO-2012 : scan_listener object is not supported in Oracle Restart


    Usage: srvctl [command] [object] []


        commands: enable|disable|start|stop|status|add|remove|modify|getenv|setenv|unsetenv|config


        objects: database|service|asm|diskgroup|listener|home|ons


    For detailed help on each command and object and its options use:


      srvctl [command] -h or


      srvctl [command] [object] -h


    PRKO-2012 : scan object is not supported in Oracle Restart


    Usage: srvctl [command] [object] []


        commands: enable|disable|start|stop|status|add|remove|modify|getenv|setenv|unsetenv|config


        objects: database|service|asm|diskgroup|listener|home|ons


    For detailed help on each command and object and its options use:


      srvctl [command] -h or


      srvctl [command] [object] -h


    PRKO-2012 : scan object is not supported in Oracle Restart


    Usage: srvctl [command] [object] []


        commands: enable|disable|start|stop|status|add|remove|modify|getenv|setenv|unsetenv|config


        objects: database|service|asm|diskgroup|listener|home|ons


    For detailed help on each command and object and its options use:


      srvctl [command] -h or


      srvctl [command] [object] -h


    PRKO-2012 : nodeapps object is not supported in Oracle Restart


    ACFS-9200: Supported


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Stop failed, or completed with errors.


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Delete failed, or completed with errors.


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Stop failed, or completed with errors.


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Modify failed, or completed with errors.


    Adding daemon to inittab


    crsexcl failed to start


    Failed to start the Clusterware. Last 20 lines of the alert log follow:


    [ctssd(4067)]CRS-2408:The clock on host rac1 has been updated by the Cluster Time


    Synchronization Service to be synchronous with the mean cluster time.


    2011-08-31 23:38:23.855


    [ctssd(4067)]CRS-2408:The clock on host rac1 has been updated by the Cluster Time


    Synchronization Service to be synchronous with the mean cluster time.


    2011-08-31 23:39:03.873


    [ctssd(4067)]CRS-2408:The clock on host rac1 has been updated by the Cluster Time


    Synchronization Service to be synchronous with the mean cluster time.


    2011-08-31 23:39:11.707


    [/g01/11.2.0/grid/bin/orarootagent.bin(4559)]CRS-5822:Agent '/g01/11.2.0/grid/bin/orarootagent_root'


    disconnected from server. Details at (:CRSAGF00117:) {0:2:27} in


    /g01/11.2.0/grid/log/rac1/agent/crsd/orarootagent_root/orarootagent_root.log.


    2011-08-31 23:39:12.725


    [ctssd(4067)]CRS-2405:The Cluster Time Synchronization Service on host rac1 is shutdown by user


    2011-08-31 23:39:12.764


    [mdnsd(3868)]CRS-5602:mDNS service stopping by request.


    2011-08-31 23:39:13.987


    [/g01/11.2.0/grid/bin/orarootagent.bin(3892)]CRS-5016:Process


    "/g01/11.2.0/grid/bin/acfsload" spawned by agent "/g01/11.2.0/grid/bin/orarootagent.bin" for action


    "check" failed: details at "(:CLSN00010:)" in


    "/g01/11.2.0/grid/log/rac1/agent/ohasd/orarootagent_root/orarootagent_root.log"


    2011-08-31 23:39:27.121


    [cssd(3968)]CRS-1603:CSSD on node rac1 shutdown by user.


    2011-08-31 23:39:27.130


    [ohasd(3639)]CRS-2767:Resource state recovery not attempted for 'ora.cssdmonitor' as its target state is OFFLINE


    2011-08-31 23:39:31.926


    [gpnpd(3880)]CRS-2329:GPNPD on node rac1 shutdown.


    [client(13099)]CRS-10001:01-Sep-11 00:11 ACFS-9200: Supported





    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Delete failed, or completed with errors.


    crsctl delete for vds in SYSTEMDG ... failed


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Delete failed, or completed with errors.


    CRS-4047: No Oracle Clusterware components configured.


    CRS-4000: Command Stop failed, or completed with errors.


    ACFS-9313: No ADVM/ACFS installation detected.


    Either /etc/oracle/olr.loc does not exist or is not readable


    Make sure the file exists and it has read and execute access


    Failure in execution (rc=-1, 256, No such file or directory) for command 1 /etc/init.d/ohasd deinstall


    error: package cvuqdisk is not installed


    Successfully deconfigured Oracle clusterware stack on this node





    回到最初运行deintall的终端摁下回车





    The deconfig command below can be executed in parallel on all the remote nodes.


    Execute the command on  the local node after the execution completes on all the remote nodes.





    Press Enter after you finish running the above commands





    <----------------------------------------





    Removing Windows and .NET products configuration END


    Oracle Universal Installer clean START





    Detach Oracle home '/g01/11.2.0/grid' from the central inventory on the local node : Done





    Delete directory '/g01/11.2.0/grid' on the local node : Done





    Delete directory '/g01/oraInventory' on the local node : Done





    Delete directory '/g01/orabase' on the local node : Done





    Detach Oracle home '/g01/11.2.0/grid' from the central inventory on the remote nodes 'rac1,rac2' : Done





    Delete directory '/g01/11.2.0/grid' on the remote nodes 'rac1,rac2' : Done





    Delete directory '/g01/oraInventory' on the remote nodes 'rac1' : Done





    Delete directory '/g01/oraInventory' on the remote nodes 'rac2' : Failed <<<<





    The directory '/g01/oraInventory' could not be deleted on the nodes 'rac2'.


    Delete directory '/g01/orabase' on the remote nodes 'rac2' : Done





    Delete directory '/g01/orabase' on the remote nodes 'rac1' : Done





    Oracle Universal Installer cleanup completed with errors.





    Oracle Universal Installer clean END





    Oracle install clean START





    Clean install operation removing temporary directory '/tmp/deinstall2011-08-31_11-59-55PM' on node 'rac1'


    Clean install operation removing temporary directory '/tmp/deinstall2011-08-31_11-59-55PM' on node 'rac2'





    Oracle install clean END





    ######################### CLEAN OPERATION END #########################





    ####################### CLEAN OPERATION SUMMARY #######################


    Following RAC listener(s) were de-configured successfully: LISTENER,LISTENER_SCAN1


    Oracle Clusterware is stopped and successfully de-configured on node "rac3"


    Oracle Clusterware is stopped and successfully de-configured on node "rac2"


    Oracle Clusterware is stopped and successfully de-configured on node "rac1"


    Oracle Clusterware is stopped and de-configured successfully.


    Skipping Windows and .NET products configuration clean


    Successfully detached Oracle home '/g01/11.2.0/grid' from the central inventory on the local node.


    Successfully deleted directory '/g01/11.2.0/grid' on the local node.


    Successfully deleted directory '/g01/oraInventory' on the local node.


    Successfully deleted directory '/g01/orabase' on the local node.


    Successfully detached Oracle home '/g01/11.2.0/grid' from the central inventory on the remote nodes 'rac1,rac2'.


    Successfully deleted directory '/g01/11.2.0/grid' on the remote nodes 'rac2,rac3'.


    Successfully deleted directory '/g01/oraInventory' on the remote nodes 'rac3'.


    Failed to delete directory '/g01/oraInventory' on the remote nodes 'rac2'.


    Successfully deleted directory '/g01/orabase' on the remote nodes 'rac2'.


    Successfully deleted directory '/g01/orabase' on the remote nodes 'rac3'.


    Oracle Universal Installer cleanup completed with errors.





    Run 'rm -rf /etc/oraInst.loc' as root on node(s) 'rac1,rac2' at the end of the session.





    Run 'rm -rf /opt/ORCLfmap' as root on node(s) 'rac1 rac2 ' at the end of the session.


    Oracle deinstall tool successfully cleaned up temporary directories.


    #######################################################################





    ############# ORACLE DEINSTALL & DECONFIG TOOL END #############

deintall运行完成后会提示让你在必要的节点上运行”rm-rf /etc/oraInst.loc”和”rm -rf /opt/ORCLfmap”，照做即可。
以上脚本运行完成后各节点上的GI已被删除，且/etc/inittab文件已还原为非GI版，/etc/init.d下的CRS相关脚本也已相应删除。

### 8.2 创建数据库时找不到磁盘组

DBCA创建数据库时找不到所需要的磁盘组，请检查oracle安装用户的主组和辅助组是否正确，两台机器是否一致。





[下载完整PDF文档](http://download.csdn.net/detail/alangmei/6851553)http://download.csdn.net/detail/alangmei/6851553
