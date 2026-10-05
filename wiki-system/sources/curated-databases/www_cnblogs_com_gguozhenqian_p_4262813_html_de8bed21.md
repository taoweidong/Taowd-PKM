---
source: "http://www.cnblogs.com/gguozhenqian/p/4262813.html"
title: "C#连接Oracle数据库(直接引用dll使用) - 振乾 - 博客园"
fetched_at: "2026-10-05 15:27:44"
---

项目中有个功能需要从一台Oracle数据库获取数据，本以为是很简单的事情，直接将原来的SqlClient换成OracleClient调用，

结果远没自己想的简单。有很多需要安装Oracle客户端，正好项目非常急，公司也没有Oracle环境，可把我急坏了。网上这方面搜索后，

太多的文章，还要不停的去测试，选择，都快烦透了。最后找了我一个哥们，他直接帮我写了一个Demo，我改了一下连接字符串，

就成功连接了，太感谢他了。这个DLL其实是Oracle为C#专门提供的，在它的官方也可以下载到（不过找起来很麻烦）。

这里我就把这个方案和dll分享给大家。

操作步骤：

  1. DLL下载后并引用
下载地址：[Oracle.ManagedDataAccess.zip](https://files.cnblogs.com/files/gguozhenqian/Oracle.ManagedDataAccess.zip)
下载后，将Oracle.ManagedDataAccess.dll放到自己的项目中，然后引用


  2. 直接调用（connString 改为自己的连接字符串）


         using Oracle.ManagedDataAccess.Client;

         public static string ConnectOracle()
                 {
                     try
                     {
                         string connString = "Data Source=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=130.147.246.144)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ECMS)));Persist Security Info=True;User ID=system;Password=Service01;";
                         OracleConnection con = new OracleConnection(connString);

                         con.Open();
                         return string.Empty;
                     }
                     catch (Exception ex)
                     {
                         return ex.ToString();
                     }
                 }



就是这么简单！！！

其他帮助文档：

<http://www.cnblogs.com/yjmyzz/archive/2013/11/01/3400999.html>
<http://www.cnblogs.com/ly303550688/archive/2013/01/31/2887104.html>
