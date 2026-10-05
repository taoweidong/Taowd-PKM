---
source: "http://www.jb51.net/article/59352.htm"
title: "在与 SQL Server 建立连接时出现与网络相关的或特定于实例的错误。未找到或无法访问服务器_mssql2008_脚本之家"
fetched_at: "2026-10-05 15:29:14"
---

[脚本之家](/) [服务器常用软件](http://s.jb51.net)

  * __[手机版](https://m.jb51.net/)
  * __[关注微信](javascript:void\(0\))

![扫一扫](https://img.jbzj.com/skin/2018/images/erwm.jpg)

[快捷导航 __](javascript:void\(0\);)

[![脚本之家](/images/logo.gif)](/)

  * [网站首页](/)
  * [网页制作](/web/)
  * [网络编程](/list/index_1.htm)
  * [脚本专栏](/list/index_96.htm)
  * [脚本下载](/jiaoben/)
  * [数据库](/list/index_104.htm)
  * [服务器](/list/list_82_1.htm)
  * [电子书籍](/books/)
  * [操作系统](/os/)
  * [网站运营](/yunying/)
  * [平面设计](/pingmian/)
  * _其它_ [媒体动画](/media/) [电脑基础](/diannaojichu/) [硬件教程](/hardware/) [网络安全](/hack/)

__您的位置：[首页](/) → [数据库](/list/index_104.htm "数据库") → [mssql2008](/list/list_236_1.htm "mssql2008") → sql server 2005 找不到服务器名称

# 在与 SQL Server 建立连接时出现与网络相关的或特定于实例的错误。未找到或无法访问服务器

更新时间：2015年01月03日 12:40:43 投稿：mdxy-dxy

在与 SQL Server 建立连接时出现与网络相关的或特定于实例的错误。未找到或无法访问服务器。请验证实例名称是否正确并且 SQL Server 已配置为允许远程连接。 (provider: 命名管道提供程序, error: 40 - 无法打开到 SQL Server 的连接)

今早开机发现，打开SQL Server 2008 的 SQL Server Management Studio，输入sa的密码发现，无法登陆数据库？提示以下错误：

“在与 SQL Server 建立连接时出现与网络相关的或特定于实例的错误。未找到或无法访问服务器。请验证实例名称是否正确并且 SQL Server 已配置为允许远程连接。 (provider: 命名管道提供程序, error: 40 - 无法打开到 SQL Server 的连接)“

在网上看到他人说使用将服务器(local)替换成本机的localhost，但是还是不行，后来自己重置了IP就可以了。具体如下：

下面的步骤需要一些前提：

你的sqlserver服务已经安装了，就是找不到服务器名称。

**1、打开Sql server 管理配置器**

![](https://img.jbzj.com/file_images/article/201501/201501031230122.jpg)

或者在命令行输入：SQLServerManager10.msc

2、点击MSSQLSERVER的协议，在右侧的页面中选择TCP/IP协议

![](https://img.jbzj.com/file_images/article/201501/201501031230123.jpg)

3、右键点击TCP/IP协议，选择“属性”，需要修改连接数据库的端口地址

![](https://img.jbzj.com/file_images/article/201501/201501031230124.jpg)

4、跳出来的对话框，里面有好多TCP/IP的端口，找到“IP3”，更改IP地址 为自己电脑的IP地址（或者是127.0.0.1） 在TCP端口添加1433，然后选择启动

![](https://img.jbzj.com/file_images/article/201501/201501031230125.jpg)

5、“IPALL”的所有端口改成“1433”

![](https://img.jbzj.com/file_images/article/201501/201501031230126.jpg)

6、重新启动服务

![](https://img.jbzj.com/file_images/article/201501/201501031230127.jpg)

![](https://img.jbzj.com/file_images/article/201501/201501031230128.jpg)

7、通过以上1-6步骤设置好端口，重新打开SQL Server Management Studio，在服务器名称输入：(local)或者127.0.0.1，即可登录数据库了。

注：脚本之家小编最近安装了sql2005也是碰到这个问题，就是参考这个修改ip的方法解决的。记得要安装[sql 2005 sp3补丁](https://www.jb51.net/softs/36935.html)

VS报错：

在与 SQL Server 建立连接时出现与网络相关的或特定于实例的错误。未找到或无法访问服务器。请验证实例名称是否正确并且 SQL Server 已配置为允许远程连接。 (provider: SQL 网络接口, error: 26 - 定位指定的服务器/实例时出错)

解决方法:开始->>SQLServer2005->>配置工具->>SQLServer外围应用配置器->>

服务和外围连接的应用配置器->>点击"远程连接"->>本地连接和远程连接->>同时使用TCP/IP和named Pipes->>点"确定"->>重启SQLserver服务可是我的电脑改不了，SQLServer外围应用配置器报错误信息：更改失败。(Microsoft.SqlServer.Smo) 其它信息： SetEnable对于ServerProtocol“Tcp”失败。(Microsoft.SqlServer.Smo)我找到了一个解决的办法。我的操作系统也是win7：点击SQL Server Configuration Manager中Sql Server 2005网络配置“MSSQLSERVER”协议，启动协议“TCP/IP”以及"Name Pipes"。并且停止，重新启动SQL Server服务。便可以了。。

**您可能感兴趣的文章:**

  * [SQL Server附加数据库报错无法打开物理文件,操作系统错误5的图文解决教程](/article/99452.htm "SQL Server附加数据库报错无法打开物理文件,操作系统错误5的图文解决教程")
  * [SQL Server附加数据库出错，错误代码5123](/article/84843.htm "SQL Server附加数据库出错，错误代码5123")
  * [SQL Server 2005附加数据库时Read-Only错误的解决方案](/article/71259.htm "SQL Server 2005附加数据库时Read-Only错误的解决方案")
  * [Sqlserver 2005附加数据库时出错提示操作系统错误5(拒绝访问)错误5120的解决办法](/article/43671.htm "Sqlserver 2005附加数据库时出错提示操作系统错误5\(拒绝访问\)错误5120的解决办法")
  * [MSSQL2005在networkservice权限运行附加数据库报(Microsoft SQL Server，错误: 5120)](/article/31839.htm "MSSQL2005在networkservice权限运行附加数据库报\(Microsoft SQL Server，错误: 5120\)")
  * [SQL Server 2008登录错误:无法连接到(local)解决方法](/article/32345.htm "SQL Server 2008登录错误:无法连接到\(local\)解决方法")
  * [安装sql server 2008时的4个常见错误和解决方法](/article/54952.htm "安装sql server 2008时的4个常见错误和解决方法")
  * [MySQL错误ERROR 2002 (HY000): Can''t connect to local MySQL server through socket](/article/56952.htm "MySQL错误ERROR 2002 \(HY000\): Can''t connect to local MySQL server through socket")
  * [SQL Server错误代码大全及解释（留着备用）](/article/30653.htm "SQL Server错误代码大全及解释（留着备用）")
  * [SQL Server数据库附加失败的解决办法](/article/136939.htm "SQL Server数据库附加失败的解决办法")

__

  * [SQL](https://www.jb51.net/tag/SQL/1.htm "搜索关于SQL的文章")
  * [Server未找到或无法访问服务器](https://www.jb51.net/tag/Server%E6%9C%AA%E6%89%BE%E5%88%B0%E6%88%96%E6%97%A0%E6%B3%95%E8%AE%BF%E9%97%AE%E6%9C%8D%E5%8A%A1%E5%99%A8/1.htm "搜索关于Server未找到或无法访问服务器的文章")

## 相关文章

  *   * [ ![还原sqlserver2008 媒体的簇的结构不正确的解决方法](https://img.jbzj.com/images/xgimg/bcimg0.png) ](/article/24318.htm "还原sqlserver2008 媒体的簇的结构不正确的解决方法")

[还原sqlserver2008 媒体的簇的结构不正确的解决方法](/article/24318.htm "还原sqlserver2008 媒体的簇的结构不正确的解决方法")

还原sqlserver2008时，遇到的“媒体的簇的结构不正确的解决方法”

2010-07-07

  * [ ![sqlserver2008锁表语句详解\(锁定数据库一个表\)](https://img.jbzj.com/images/xgimg/bcimg1.png) ](/article/44960.htm "sqlserver2008锁表语句详解\(锁定数据库一个表\)")

[sqlserver2008锁表语句详解(锁定数据库一个表)](/article/44960.htm "sqlserver2008锁表语句详解\(锁定数据库一个表\)")

锁一个SQL表的语句是SQL数据库使用者都需要知道的，下面就将为您介绍锁SQL表的语句，希望对您学习锁SQL表方面能有所帮助

2013-12-12

  * [ ![sql2008 还原数据库解决方案](https://img.jbzj.com/images/xgimg/bcimg2.png) ](/article/32082.htm "sql2008 还原数据库解决方案")

[sql2008 还原数据库解决方案](/article/32082.htm "sql2008 还原数据库解决方案")

本文将介绍如何利用bak恢复数据库，以sql2008 还原数据库为例进行介绍，需要的朋友可以参考下

2012-11-11

  * [ ![SQL Server 2012降级至2008R2的方法](https://img.jbzj.com/images/xgimg/bcimg3.png) ](/article/109270.htm "SQL Server 2012降级至2008R2的方法")

[SQL Server 2012降级至2008R2的方法](/article/109270.htm "SQL Server 2012降级至2008R2的方法")

这篇文章主要为大家详细介绍了SQL Server 2012降级至SQL Server 2008R2的方法，具有一定的参考价值，感兴趣的小伙伴们可以参考一下

2017-03-03

  * [ ![SQLserver 2008将数据导出到Sql脚本文件的方法](https://img.jbzj.com/images/xgimg/bcimg4.png) ](/article/23007.htm "SQLserver 2008将数据导出到Sql脚本文件的方法")

[SQLserver 2008将数据导出到Sql脚本文件的方法](/article/23007.htm "SQLserver 2008将数据导出到Sql脚本文件的方法")

大家都知道使用SQL的企业管理器可以导出SQL脚本，但导不出SQL的数据到脚本中，目前SQL2008有这个功能了。

2010-04-04

  * [ ![SQLServer 2008 :error 40出现连接错误的解决方法](https://img.jbzj.com/images/xgimg/bcimg5.png) ](/article/41473.htm "SQLServer 2008 :error 40出现连接错误的解决方法")

[SQLServer 2008 :error 40出现连接错误的解决方法](/article/41473.htm "SQLServer 2008 :error 40出现连接错误的解决方法")

在与SQLServer建立连接时出现与网络相关的或特定与实例的错误.未找到或无法访问服务器.请验证实例名称是否正确并且SQL SERVER已配置允许远程链接

2013-09-09

  * [ ![SQL Server 2008 R2 超详细安装图文教程](https://img.jbzj.com/images/xgimg/bcimg6.png) ](/article/72561.htm "SQL Server 2008 R2 超详细安装图文教程")

[SQL Server 2008 R2 超详细安装图文教程](/article/72561.htm "SQL Server 2008 R2 超详细安装图文教程")

这篇文章主要介绍了SQL Server 2008 R2 超详细安装图文教程,需要的朋友可以参考下

2015-09-09

  * [ ![sql server 2008数据库连接字符串大全](https://img.jbzj.com/images/xgimg/bcimg7.png) ](/article/47789.htm "sql server 2008数据库连接字符串大全")

[sql server 2008数据库连接字符串大全](/article/47789.htm "sql server 2008数据库连接字符串大全")

这篇文章主要介绍了sql server 2008数据库的连接字符串大全,需要的朋友可以参考下

2014-03-03

  * [ ![SQL Server 2008中的代码安全（二） DDL触发器与登录触发器](https://img.jbzj.com/images/xgimg/bcimg8.png) ](/article/27382.htm "SQL Server 2008中的代码安全（二） DDL触发器与登录触发器")

[SQL Server 2008中的代码安全（二） DDL触发器与登录触发器](/article/27382.htm "SQL Server 2008中的代码安全（二） DDL触发器与登录触发器")

MicrosoftSQL Server 提供两种主要机制来强制使用业务规则和数据完整性：约束和触发器。触发器为特殊类型的存储过程，可在执行语言事件时自动生效。SQL Server 包括三种常规类型的触发器：DML 触发器、DDL 触发器和登录触发器。

2011-06-06

  * [ ![SQL Server2008 Order by在union子句不可直接使用的原因详解](https://img.jbzj.com/images/xgimg/bcimg9.png) ](/article/191929.htm "SQL Server2008 Order by在union子句不可直接使用的原因详解")

[SQL Server2008 Order by在union子句不可直接使用的原因详解](/article/191929.htm "SQL Server2008 Order by在union子句不可直接使用的原因详解")

这篇文章主要介绍了SQL Server2008 Order by在union子句不可直接使用的原因详解，文中通过示例代码介绍的非常详细，对大家的学习或者工作具有一定的参考学习价值，需要的朋友们下面随着小编来一起学习学习吧

2020-07-07

#### 大家感兴趣的内容

  * _1_[Sql Server 2008完全卸载方法(其他版本类似)](/article/37301.htm "Sql Server 2008完全卸载方法\(其他版本类似\)")
  * _2_[SQL Server 2008 安装和配置图解教程(附官方下](/article/30243.htm "SQL Server 2008 安装和配置图解教程\(附官方下载地址\)")
  *  _3_[SQL Server 2008 R2 超详细安装图文教程](/article/72561.htm "SQL Server 2008 R2 超详细安装图文教程")
  *  _4_[在与 SQL Server 建立连接时出现与网络相关的或特定](/article/59352.htm "在与 SQL Server 建立连接时出现与网络相关的或特定于实例的错误。未找到或无法访问服务器")
  *  _5_[安装sql server 2008时的4个常见错误和解决方法](/article/54952.htm "安装sql server 2008时的4个常见错误和解决方法")
  *  _6_[SQL Server 2008登录错误:无法连接到(loca](/article/32345.htm "SQL Server 2008登录错误:无法连接到\(local\)解决方法")
  *  _7_[SQL Server 2008 阻止保存要求重新创建表的更改](/article/30416.htm "SQL Server 2008 阻止保存要求重新创建表的更改问题的设置方法")
  *  _8_[SQLserver 2008将数据导出到Sql脚本文件的方法](/article/23007.htm "SQLserver 2008将数据导出到Sql脚本文件的方法")
  *  _9_[SQL Server 2008 清空删除日志文件(瞬间日志变](/article/37305.htm "SQL Server 2008 清空删除日志文件\(瞬间日志变几M\)")
  *  _10_[图文详解SQL Server 2008R2使用教程](/article/91230.htm "图文详解SQL Server 2008R2使用教程")

#### 最近更新的内容

  * [SQL Server 2008中的代码安全（二） DDL触发器与登录触发器](/article/27382.htm "SQL Server 2008中的代码安全（二） DDL触发器与登录触发器")
  * [SQL Server 2008安装图解(详细)](/article/83556.htm "SQL Server 2008安装图解\(详细\)")
  * [SQLServer 2008 :error 40出现连接错误的解决方法](/article/41473.htm "SQLServer 2008 :error 40出现连接错误的解决方法")
  * [windows系统下SQL Server 2008超详细安装教程](/article/269972.htm "windows系统下SQL Server 2008超详细安装教程")
  * [sql 实现将空白值替换为其他值](/article/204906.htm "sql 实现将空白值替换为其他值")
  * [SQL Server 2008 R2 超详细安装图文教程](/article/72561.htm "SQL Server 2008 R2 超详细安装图文教程")
  * [SQL2008定时任务作业创建教程](/article/32065.htm "SQL2008定时任务作业创建教程")
  * [sql server 2008 用户 NT AUTHORITY\IUSR 登](/article/70809.htm "sql server 2008 用户 NT AUTHORITY\\IUSR 登录失败的解决方法")
  * [SQL Server 2008 R2占用cpu、内存越来越大的两种解决方法](/article/126888.htm "SQL Server 2008 R2占用cpu、内存越来越大的两种解决方法")
  * [如何利用SQL进行推理](/article/69737.htm "如何利用SQL进行推理")

#### 常用在线小工具
