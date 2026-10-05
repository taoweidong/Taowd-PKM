---
source: "http://blog.csdn.net/makenothing/article/details/17080069"
title: "ASP.NET(C#) VS2010连接Oracle数据库_vs2010 安装oracle.manageddataaccess.client-CSDN博客"
fetched_at: "2026-10-05 15:27:00"
---

数学基础是通信密码学原理关键，我建议大家找几个比较靠谱入门的机器学习或者人工智能学习平台，在此推荐一个我看过的小白人工智能入门教程，零基础教程，简单通俗易懂，[点击这里可以直达：人工智能入门基础教程](https://www.captainbed.net/makenothing)， 一定要系统全面的去学习才能有效果，不要半途而废，

首先介绍个人环境：win7 + VS2010 + Oracle 11g Client （注意：我这里只是安装的client，如果安装了整个数据库也是可以的） 。

正题：

一. 在VS2010中连接 Oracle数据库有两种方法：

第一种：微软提供的连接方法 : using System.Data.OracleClient;

第二种：Oracle自己提供的方法：using Oracle.DataAccess.Client;

连接字符串：


    connectionString="Password=czh;User ID=czh;Data Source=(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=XXX.XXX.XXX.XXX)(PORT=1521)))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=skydream)));"



1\. 微软提供的连接方法 : using System.Data.OracleClient;

测试例程：

··1.在VS2010新建控制台应用程序（C#）；

··2.右键、引用，在.NET中选择System.Data.OracleClient；（注明：找不到System.Data.OracleClient 请看此链接：<http://blog.csdn.net/makenothing/article/details/17187965>）

··3.在程序中 using System.Data.OracleClient;


    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Data.OracleClient;


    namespace ConsoleApplication2
    {
        class Program
        {
            static void Main(string[] args)
            {
                string connectionString;
                string queryString;

                connectionString = "Data Source=202.200.136.125/orcl;User ID=openlab;PassWord=open123";

                queryString = "SELECT * FROM T_USER";

                OracleConnection myConnection = new OracleConnection(connectionString);

                OracleCommand myORACCommand = myConnection.CreateCommand();

                myORACCommand.CommandText = queryString;

                myConnection.Open();

                OracleDataReader myDataReader = myORACCommand.ExecuteReader();

                myDataReader.Read();

                Console.WriteLine("email: " + myDataReader["EMAIL"]);

                myDataReader.Close();

                myConnection.Close();

            }
        }
    }




2.Oracle自己提供的方法：using Oracle.DataAccess.Client;

前提条件：安装oracle或者oracle client（说明：oracle client比较小，本人安装的是client）下载地址：[http://pan.baidu.com/share/link?shareid=462035167&uk=2098256597](http://pan.baidu.com/share/link?shareid=462035167&uk=2098256597)

以及安装 Oracle Client 教程链接：<http://www.cnblogs.com/jiguixin/archive/2011/09/09/2172672.html>

··1.在VS2010新建控制台应用程序（C#）；

··2.右键、引用，在.NET/组件中选择Oracle.DataAccess.Client；如果找不到则选择 浏览，进入到oracleclient的安装目录寻找 Oracle.Data.Access.dll （典型目录为：E:\app\Administrator\product\11.2.0\client_1\ODP.NET\bin\2.x\Oracle.Data>Access.dll）

··3.程序中添加引用：using Oracle.DataAccess.Client;


    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using Oracle.DataAccess.Client;

    namespace testConnectionOracle
    {
        class Program
        {
            static void Main(string[] args)
            {
                string connectionString;
                string queryString;

                connectionString = "Data Source=202.200.155.123/orcl;User ID=openlab;PassWord=open123";

                queryString = "SELECT * FROM T_USER";

                OracleConnection myConnection = new OracleConnection(connectionString);

                OracleCommand myORACCommand = myConnection.CreateCommand();

                myORACCommand.CommandText = queryString;

                myConnection.Open();

                OracleDataReader myDataReader = myORACCommand.ExecuteReader();

                myDataReader.Read();

                Console.WriteLine("email: " + myDataReader["EMAIL"]);

                myDataReader.Close();

                myConnection.Close();

            }
        }
    }




技术交流沟通请扫码或者关注公众: 木石说 （ mushiwords）, 直接回复 cpp 获取下载链接，其他问题，有空必回，欢迎交流沟通。

![](https://i-blog.csdnimg.cn/blog_migrate/04fb1c30a7671c91b16dd025e3f69217.png)
