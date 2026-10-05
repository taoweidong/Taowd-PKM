---
source: "http://www.cnblogs.com/zzj-suxiao/articles/3934805.html"
title: "C# sqlcommand 使用方法  （转） - 邹邹 - 博客园"
fetched_at: "2026-10-05 15:29:33"
---

**使用sqlcommand对象来返回数据集合的方法、**
    
    
    string strconn="data source=billgates;initial catalog=test;integrated security=SSPI;";
    SqlConnection conn=new SqlConnection(strconn);
    conn.Open();
    SqlCommand sqlcmd=new SqlCommand();
    sqlcmd.CommandText ="select * from student";
    sqlcmd.Connection=conn;
    SqlDataAdapter adp=new SqlDataAdapter(sqlcmd);
    DataTable dt=new DataTable();
    adp.Fill(dt);
    dataGrid1.DataSource=dt;
    
    使用sqlcommand对象来返回SQL执行正确与否
    string strconn="data source=billgates;initial catalog=test;integrated security=SSPI;";
    SqlConnection conn=new SqlConnection(strconn);
    conn.Open();
    SqlCommand sqlcmd=new SqlCommand();
    sqlcmd.CommandText ="select * from student";
    sqlcmd.Connection=conn;
    try
    {
      sqlcmd.ExecuteNonQuery();
      MessageBox.Show("success");
    }
    catch
    {
      MessageBox.Show("false");
    }

**使用sqlcommand对象来操作存储过程**
    
    
    string strconn="data source=billgates;initial catalog=test;integrated security=SSPI;";
    SqlConnection conn=new SqlConnection(strconn);
    conn.Open();
    SqlCommand sqlcmd=new SqlCommand();
    sqlcmd.CommandText ="a";
    sqlcmd.CommandType=CommandType.StoredProcedure ;
    sqlcmd.Connection=conn;
    sqlcmd.Parameters.Add("@param1",textBox1.Text.Trim());
    sqlcmd.Parameters.Add("@param2",textBox2.Text.Trim());
    sqlcmd.Parameters.Add("@param3",textBox3.Text.Trim());
    
    SqlDataAdapter adp=new SqlDataAdapter(sqlcmd);
    DataTable dt=new DataTable();
    adp.Fill(dt);
    dataGrid1.DataSource=dt;

**ExecuteReader方法**
    
    
    using System;
    using System.Data.SqlClient;
    public class Lvcha
    {
      public static void Main(string[] args)
      {
        string source="Server =192.168.1.100; User ID=ac_sy_guest; Password=guest1314; Initial CataLog=Account";
        string select="select * from dbUser";
        SqlConnection conn=new SqlConnection(source);
        conn.Open();
        SqlCommand cmd=new SqlCommand(select,conn);
        SqlDataReader reader=cmd.ExecuteReader();//返回只能读取,不能写入的SqlDataReader对象
        while(reader.Read())
        {
          Console.WriteLine("{0}",reader["user_name"]);
        }
        Console.ReadLine();
      }
    }

**ExecuteNonQuery方法**
    
    
    一般修改删除都插入都用它
    返回受影响的行数。
    
    using System;
    using System.Data.SqlClient;
    public class Lvcha
    {
      public static void Main(string[] args)
      {
        string source="Server =192.168.1.100; User ID=ac_sy_guest; Password=guest1314; Initial CataLog=Account";
        string select="updata .....";
        SqlConnection conn=new SqlConnection(source);
        conn.Open();
        SqlCommand cmd=new SqlCommand(select,conn);
        object o=cmd.ExecuteNonQuery();
       
        while(reader.Read())
        {
          Console.WriteLine("{0}",reader["user_name"]);
        }
        Console.ReadLine();
      }
    }

**ExecuteScalar方法**

**执行查询，并返回查询所返回的结果集中第一行的第一列。所有其他的列和行将被忽略。**
    
    
    using System;
    using System.Data.SqlClient;
    public class Lvcha
    {
      public static void Main(string[] args)
      {
        string source="Server =192.168.1.100; User ID=ac_sy_guest; Password=guest1314; Initial CataLog=Account";
        string select="select count(*) from dbUser";
        SqlConnection conn=new SqlConnection(source);
        conn.Open();
        SqlCommand cmd=new SqlCommand(select,conn);
        object o=cmd.ExecuteScalar();
        Console.WriteLine(o);
        Console.ReadLine();
      }
    }

ExecuteNonQuery用于执行不返回任何记录的SQL语句或存储过程。在数据库执行如更新、插入、删除操作时，应使用这个方法。ExecuteNonQuery返回一个整数值，用来说明受查询语句影响的行数。  
connection.Open();  
command.ExecuteNonQuery();  
command.Close(); 

ExecuteScalar与ExecuteNonQuery一样，其返回的也是单值，但该返回值是从数据库中读出来的，而不是受影响的行数。它通常用于选择一个值的SQL语句。如果SELECT返回多行或多列，则使用该方法仅返回第一行第一列的数据。

ExecuteReader被用于返回多条记录的SELECT语句（包含任意个字段）。ExecuteReader将返回一个包含查询结果的SqlDataReader对象。一个SqlDataReader对象是以顺序向前且只读的形式逐个读取并返回结果的。SqlDataReader是数据库中读取数据最快的对象，但必须打开连接。通过SqlDataReader取回所有的记录，并把它们存入DataTable对象中（它可以存储离线数据而不需要一个打开的连接），这样就可以马上关闭数据库连接了。DataTable类可以存放本地的结果集而不需要一个打开的SQL Server连接，和其它的ADO.NET对象一样，它也不是特定于某种数据提供程序的。

conn.Open();  
SqlDataReader reader = comm.ExecuteReader();  
DataTable table = new DataTable();  
table.Load(reader);  
reader.Close();  
conn.Close();

出处：<http://bluelightning.blog.163.com/blog/static/581653201002010511090/>
