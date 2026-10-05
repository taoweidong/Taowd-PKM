---
source: "http://www.cnblogs.com/xiaopang2010/p/3382383.html"
title: ".NET Oracle Developer的福音——ODP.NET Managed正式推出 - 小胖2010 - 博客园"
fetched_at: "2026-10-05 15:27:34"
---

在.NET平台下开发Oracle应用的小伙伴们肯定都知道一方面做Oracle开发和实施相比SqlServer要安装Oracle客户端（XCopy、自己提取相关文件也有一定复杂性），另一方面相比JAVA平台不如JDBC方便快捷，特别是一些刚接触Oracle的小伙伴，面临配置tns.ora、OraHome等等多少有些畏难情绪。

# 初始庐山

现在，这一切都即将成为过去啦。继早些时候Oracle官方推出的ODP.NET Managed的Beta版之后，最近的版本已经跟随12c一起发布了，可以[在此](http://www.oracle.com/technetwork/topics/dotnet/downloads/index.html)下载。对应的[12c文档](http://docs.oracle.com/cd/E48297_01/doc/win.121/e41125.pdf)粗看一下，下载了64bit的版本，下载完成后文件不多。

[![image](https://images0.cnblogs.com/blog/78254/201310/22143809-8a1defc86490499ba44e221c01c5c016.png)](https://images0.cnblogs.com/blog/78254/201310/22143808-ff48ac7b7d9a4989ada62cafca0e07b8.png)

一个readme.htm中只寥寥数语，熟悉的network文件夹相当于与一个tnsnames和sqlnet的模板，managed里也提供里一个文档，里面描述也很少，主要介绍一些配置和BUG情况，核心就在common里面的Oracle.ManagedDataAccess.dll这个文件了，Oracle.ManagedDataAccess.Client.Configuration.Section.xsd这个文件一看就知道是提供给vs的xml编辑器提供智能提示的，接着里面还区分了X64和X86的文件夹，一方便主要是分布式事务的Oracle.ManagedDataAccessDTC.dll不同，另一个就是bat文件里相关命令不同了。

[![image](https://images0.cnblogs.com/blog/78254/201310/22143810-066c493732884274bc0dd8e9d93fa06b.png)](https://images0.cnblogs.com/blog/78254/201310/22143809-c5c9bd3b51524ce48b58cb519c8ddd63.png)

如果你对之前的ODP.NET的OraProvCfg已经比较熟悉的话，那么configure.bat里面的内容就很好理解了，这个批处理一共干了这么几件事情，其中2、4、5其实并不是必须的：

1、将驱动对应db factory注册以及添加configuration处理器，其实就是在machine.config里增加<section name="oracle.manageddataaccess.client" type="OracleInternal.Common.ODPMSectionHandler, Oracle.ManagedDataAccess, Version=4.121.1.0, Culture=neutral, PublicKeyToken=89b483f429c47342" />和<add name="ODP.NET, Managed Driver" invariant="Oracle.ManagedDataAccess.Client" description="Oracle Data Provider for .NET, Managed Driver" type="Oracle.ManagedDataAccess.Client.OracleClientFactory, Oracle.ManagedDataAccess, Version=4.121.1.0, Culture=neutral, PublicKeyToken=89b483f429c47342" />，这样在接下来的开发和部署中才能识别Oracle.ManagedDataAccess.Client的驱动以及oracle.manageddataaccess.client的配置节点（其实如果在单独的程序配置也是可以的，需要注意的是是否使用gac）

2、添加ODP.NET Managed的性能计数器(Performance Counter)

3、将Oracle.ManagedDataAccess.dll添加到GAC中

4、提供在VS开发环境下配置节点的智能提示，其实就是将之前提到的Oracle.ManagedDataAccess.Client.Configuration.Section.xsd拷贝到VS对应目录下

5、添加日志记录

6、添加VS开发环境对Oracle.ManagedDataAccess.dll引用的支持

[![image](https://images0.cnblogs.com/blog/78254/201310/22143811-192b7ec2e8dd487d8a0450ddf0e9ef2b.png)](https://images0.cnblogs.com/blog/78254/201310/22143810-b8c9fa74e04b436aaa262c703a2878d6.png)

# 牛刀小试

VS新建一个项目，引用Oracle.ManagedDataAccess.dll，开始随意码几行烂熟的入门级代码…，可以看到，正如Orale自己描述的，跟以前的API差别很小，所不同的就是命名空间换成了using Oracle.ManagedDataAccess.Client;


       1:              OracleConnection con = new OracleConnection();


       2:              con.ConnectionString = "user id=his3;password=his3;data source=192.168.1.237/ORCL";


       3:              con.Open();


       4:


       5:              OracleCommand cmd = new OracleCommand();


       6:              cmd.CommandType = System.Data.CommandType.Text;


       7:              cmd.CommandText = "select * from gy_yonghuxx";


       8:              cmd.Connection = con;


       9:


      10:              OracleDataAdapter da = new OracleDataAdapter();


      11:              da.SelectCommand = cmd;


      12:              DataSet ds = new DataSet();


      13:              da.Fill(ds);


      14:


      15:              con.Close();


      16:              da.Dispose();


      17:              cmd.Dispose();


      18:              con.Dispose();

眼力好的伙伴肯定能马上发现ConnectionString的特殊之处，字符连接串有三种方式 ：

a、tns alias："user id=scott;password=tiger;data source=sales";在此具体的对应tns文件是可以在config文件中指定，比如我的machine.config给我默认了一个<setting name="tns_admin" value="d:\installsoft\oracle\odp.net_managed121010\odp.net\managed\x64\\..\\..\\..\network\admin" />

b、Connect Descriptor:该种方式就是将tns配置的一段拿出来写进去，相比c的有点在于可配置项全面


      "user id=scott;password=tiger;data source=" +
         "(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)" +
         "(HOST=sales-server)(PORT=1521))(CONNECT_DATA="+
         "(SERVICE_NAME=sales.us.acme.com)))"


     c、Easy Connect Naming Method：PROTOCOL等一些选项好像就没地方配置了


      "user id=scott;password=tiger;data source=//sales-server:1521/sales.us.acme.com"




# Entity Framework重构


       对于已经开始或准备使用Entity Framework的项目（目前版本还不支持Code First），如果熟悉ADO.NET替换起来其实也很简单，共有三点需要注意


     1、配置文件里的连接字符串中provider=Oracle.DataAccess.Client;替换为provider=Oracle.ManagedDataAccess.Client;provider


     2、对应实体文件edmx中的Provider="Oracle.DataAccess.Client"也替换为Provider="Oracle.ManagedDataAccess.Client"


     3、如果对数据类型映射做过配置（Oracle默认的类型映射有点坑爹），需要将下图红线下面的加上去


    [![image](https://images0.cnblogs.com/blog/78254/201310/22143811-cac097d9cdc3478dbf86e10d8a8ec759.png)](https://images0.cnblogs.com/blog/78254/201310/22143811-dfb05c94b98440408995ac805861a5b5.png)

# 一探究竟

性能测试我想正式版发布前Oracle官方肯定做过的，自己做测试对比毕竟不够专业，但粗略看下内部实现多少能看出端倪的，如果看过以前Oracle驱动的dll（Mircrosoft、Oracle、Devert提供的dll）肯定知道以前都是依赖于oci.dll这个接口，调用的最终实现是通过P\Invoke。下图是顺着OracleConnect.Open最后跟踪到的OracleCommunication的类，在此已经出现了soket、socketStream等对象，可见这次的托管版本托管的还是比较彻底的，个人觉得在性能上应该会比P\Invoke来的高效。

[![image](https://images0.cnblogs.com/blog/78254/201310/22143812-5f5e0f9c50ae47ee98e08a1d44d5afad.png)](https://images0.cnblogs.com/blog/78254/201310/22143812-ed6b8a7edda44b1dbcfb421c9508cdbe.png)
