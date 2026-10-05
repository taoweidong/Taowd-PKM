---
source: "http://www.cnblogs.com/pinbo/archive/2010/10/22/1858246.html"
title: "Oracle 数据库导入导出 dmp文件 - anny0320 - 博客园"
fetched_at: "2026-10-05 15:27:49"
---

首先询问对方数据库的表空间名称和大小，然后在你的oracle中建立相应表空间，最后使用命令导入、导出数据。
补充：
1.要新建一个数据库；

Oracle数据导入导出imp/exp就相当于oracle数据还原与备份。exp命令可

以把数据从远程数据库服务器导出到本地的dmp文件，imp命令可以把dmp文件从本

地导入到远处的数据库服务器中。 利用这个功能可以构建两个相同的数据库，一

个用来测试，一个用来正式使用。
例如：imp命令导入数据：
imp username/password@SID file=XXX.dmp fromuser=XXX touser=XXX tables=(XXX,XXX)
其中，fromuser指对方数据库用户名，touser指你的数据库的用户名；

fromuser若为多个表空间的话，使用()将其括起来：fromuser=(a,b)；
touser参数仿fromuser参数；
若只导入一部分表，使用tables参数，用()括起要导入的表；如果想全部导入，不需要指定tables参数

下面介绍的是导入导出的实例。
数据导出：
1 将数据库TEST完全导出,用户名system 密码manager 导出到D:\daochu.dmp中
exp system/manager@TEST file=d:\daochu.dmp full=y

2 将数据库中system用户与sys用户的表导出
exp system/manager@TEST file=d:\daochu.dmp owner=(system,sys)

3 将数据库中的表inner_notify、notify_staff_relat导出
exp aichannel/aichannel@TESTDB2 file= d:\data\newsmgnt.dmp tables=

(inner_notify,notify_staff_relat)


上面是常用的导出，对于压缩，既用winzip把dmp文件可以很好的压缩。
也可以在上面命令后面 加上 compress=y 来实现。
数据的导入
1 将D:\daochu.dmp 中的数据导入 TEST数据库中。
imp system/manager@TEST file=d:\daochu.dmp
imp aichannel/aichannel@HUST full=y file=file= d:\data\newsmgnt.dmp

ignore=y
上面可能有点问题，因为有的表已经存在，然后它就报错，对该表就不进行导

入。
在后面加上 ignore=y 就可以了。

2 将d:\daochu.dmp中的表table1 导入
imp system/manager@TEST file=d:\daochu.dmp tables=(table1)

基本上上面的导入导出够用了。不少情况要先是将表彻底删除，然后导入。

注意：
操作者要有足够的权限，权限不够它会提示。
数据库时可以连上的。可以用tnsping TEST 来获得数据库TEST能否连上。

附录一：
给用户增加导入数据权限的操作
第一,启动sql*puls
第二，以system/manager登陆
第三，create user 用户名 IDENTIFIED BY 密码 （如果已经创建过用户，这步

可以省略）
第四，GRANT CREATE USER,DROP USER,ALTER USER ,CREATE ANY VIEW ,
DROP ANY VIEW,EXP_FULL_DATABASE,IMP_FULL_DATABASE,
DBA,CONNECT,RESOURCE,CREATE SESSION TO 用户名字
第五, 运行-cmd-进入dmp文件所在的目录,
imp userid=system/manager full=y file=*.dmp
或者 imp userid=system/manager full=y file=filename.dmp

执行示例:
F:\Work\Oracle_Data\backup>imp userid=test/test full=y

file=inner_notify.dmp

屏幕显示
Import: Release 8.1.7.0.0 - Production on 星期四 2月 16 16:50:05 2006
(c) Copyright 2000 Oracle Corporation. All rights reserved.

连接到: Oracle8i Enterprise Edition Release 8.1.7.0.0 - Production
With the Partitioning option
JServer Release 8.1.7.0.0 - Production

经由常规路径导出由EXPORT:V08.01.07创建的文件
已经完成ZHS16GBK字符集和ZHS16GBK NCHAR 字符集中的导入
导出服务器使用UTF8 NCHAR 字符集 (可能的ncharset转换)
. 正在将AICHANNEL的对象导入到 AICHANNEL
. . 正在导入表 "INNER_NOTIFY" 4行被导入
准备启用约束条件...
成功终止导入，但出现警告。


来自: <http://hi.baidu.com/ooofcu/blog/item/ec5d1f9580d41f007af48077.html>
