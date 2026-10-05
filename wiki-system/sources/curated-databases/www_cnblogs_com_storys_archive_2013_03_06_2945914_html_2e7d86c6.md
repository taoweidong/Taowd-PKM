---
source: "http://www.cnblogs.com/storys/archive/2013/03/06/2945914.html"
title: "C# 连接 Oracle 的几种方式 - storys - 博客园"
fetched_at: "2026-10-05 15:27:43"
---

**一：通过System.Data.OracleClient(需要安装Oracle客户端并配置tnsnames.ora)**
1\. 添加命名空间System.Data.OracleClient引用
2\. using System.Data.OracleClient;
3\.
string connString = "User ID=IFSAPP;Password=IFSAPP;Data Source=RACE;";
OracleConnection conn = new OracleConnection(connString);
try
{
conn.Open();
MessageBox.Show(conn.State.ToString());
}
catch (Exception ex)
{
ShowErrorMessage(ex.Message.ToString());
}
finally
{
conn.Close();
}

**二：通过System.Data.OracleClient(需要安装Oracle客户端不需配置tnsnames.ora)**
1\. 添加命名空间System.Data.OracleClient引用
2\. using System.Data.OracleClient;
3.
string connString = "User ID=IFSAPP;Password=IFSAPP;Data Source=(DESCRIPTION = (ADDRESS_LIST= (ADDRESS = (PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME = RACE)))";
OracleConnection conn = new OracleConnection(connString);
try
{
conn.Open();
MessageBox.Show(conn.State.ToString());
}
catch (Exception ex)
{
ShowErrorMessage(ex.Message.ToString());
}
finally
{
conn.Close();
}

**三：通过System.Data.OleDb和Oracle公司的驱动**
1\. 添加命名空间System.Data.OracleClient引用
2\. using System.Data.OleDb;
3.
string connString = "Provider=OraOLEDB.Oracle.1;User ID=IFSAPP;Password=IFSAPP;Data Source=(DESCRIPTION = (ADDRESS_LIST= (ADDRESS = (PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME = RACE)))";
OleDbConnection conn = new OleDbConnection(connString);
try
{
conn.Open();
MessageBox.Show(conn.State.ToString());
}
catch (Exception ex)
{
ShowErrorMessage(ex.Message.ToString());
}
finally
{
conn.Close();
}

**四：通过System.Data.OleDb和微软公司的Oracle驱动**
1\. 添加命名空间System.Data.OracleClient引用
2\. using System.Data.OleDb;
3.
string connString = "Provider=MSDAORA.1;User ID=IFSAPP;Password=IFSAPP;Data Source=(DESCRIPTION = (ADDRESS_LIST= (ADDRESS = (PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME = RACE)))";
OleDbConnection cnn = new OleDbConnection(connString);
try
{
conn.Open();
MessageBox.Show(conn.State.ToString());
}
catch (Exception ex)
{
ShowErrorMessage(ex.Message.ToString());
}
finally
{
conn.Close();
}

备注：
a.XP操作系统已经安装了微软公司的Oracle驱动C:\Program Files\Common Files\System\Ole DB\msdaora.dll
b.该驱动需要Oracle客户端的三个文件(oraocixe10.dll、oci.dll、ociw32.dll)放在System32下即可

**五：使用ODP连接**
1\. 下载安装ODP.NET(<http://www.oracle.com/technetwork/developer-tools/visual-studio/downloads/index.html>)
2\. 安装完全成后会产生一序列文件。
3\. 找到这个安装目录，打开文件夹%ORACLE_HOME%\Network\Admin在这个下面建立一个tnsnames.ora的文件，其内容可以参考其下的Sample目录下面的配置
Oracle.RACE =
(DESCRIPTION=
(ADDRESS_LIST=
(ADDRESS=
(PROTOCOL=TCP)
(HOST=127.0.0.1)
(PORT=1521)
)
)
(CONNECT_DATA=
(SID=RACE)
(SERVER=DEDICATED)
)
)
Oracle.RACE为连接字符串名称，可以随便取。等号后面的字符串可以在Enterprise Manager Console工具中连接数据库后的TNS描述符中拷过来
4\. 引用Oracle.DataAccess命名空间
5\. using Oracle.DataAccess.Client;
6\. 示例代码：
string connString = "DATA SOURCE=Oracle.RACE;PERSIST SECURITY INFO=True;USER ID=IFSAPP;password=IFSAPP";
OracleConnection conn = new OracleConnection(connString);
try
{
conn.Open();
OracleCommand cmd = new OracleCommand(cmdText,conn);
OracleDataReader reader = cmd.ExecuteReader();
this.DataGridView1.DataSource = reader;
this.DataGridView1.DataBind();
}
catch (Exception ex)
{
ShowErrorMessage(ex.Message.ToString());
}
finally
{
conn.Close();
}

**六：使用第三方驱动**
第三方驱动有 Devart，下载驱动 <http://www.devart.com/dotconnect/oracle/>，但是是商业版，需要购买许可或破解
连接格式 User ID=myUsername;Password=myPassword;Host=ora;Pooling=true;Min Pool Size=0;Max Pool Size=100;Connection Lifetime=0;
1\. 引用Devart.Data.Oracle命名空间
2\. using Devart.Data.Oracle;
3.
OracleConnection conn = new OracleConnection();
conn.ConnectionString = "";
conn.Unicode = true;
conn.UserId = "IFSAPP";
conn.Password = "IFSAPP";
conn.Port = 1521;
conn.Server = "127.0.0.1";
conn.Sid = "RACE";
try
{
conn.Open();
//execute queries, etc
}
catch (Exception ex)
{
ShowErrorMessage(ex.Message.ToString());
}
finally
{
conn.Close();
}
