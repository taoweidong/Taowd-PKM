---
source: "http://www.cnblogs.com/WuXuanKun/p/5483414.html"
title: "用SqlParameter 给SQL传递参数 - 吴玄坤 - 博客园"
fetched_at: "2026-10-05 15:29:36"
---

1.数据访问层

using的用法:

01.可以using System;导命名控空间

02.using 的语法结构

using(变量类型 变量名 =new 变量类型())

{

}

案例:

03.using的原理

为什么出了using所在的{}，会自动回收对象。

原因是当我们将要出{}，系统自动调用了Dispose()方法。

而在DISpose方法中是这么实现的

2.哪些对象才可以使用Using回收！如:SqlConnection Font 和File 也都可以使用using 因为他们实现了IDisposable接口

必须实现了[IDisposable](http://www.aisto.com/roeder/dotnet/Default.aspx?Target=code://mscorlib:4.0.0.0:b77a5c561934e089/System.IDisposable "System.IDisposable

CTRL+Click to open in new tab.") 接口的类型才可以使用using回收！

3.using回收的是托管还是非托管资源？

解析：什么是托管：所有的C#代码都是被CLR监管，

结论是using回收的是 非托管资源！

2.会实现参数化SQL

解析：username: ' or 1=1 -- pwd:sb

## 1.使用using释放资源

Using释放的是托管资源还是非托管资源？

解析：非托管，C#应用托管到.NET Framework.但是他可以释放非托管资源。

1.using用法：

01.有人问，什么样的的语句可以使用using管理？？

官方人士解析：稀缺的资源，才需要using管理。接着有人问：what is less resource ?例如：Connection对象，IO流。

02.Dispose方法会自动调用Close()

要想让一个类型可以通过using管理，该类型或者父类必须实现了IDisposable接口。

using(SqlConnection con=new SqlConnection)

{

//本质上自动调用了Dispose方法

}

2.close()和dispose()区别？

解析：close()只是关闭连接，但是通道没有销毁，dispose()不仅把连接给关闭了，而且把通道也给销毁了。

## 2.会使用SqlParameter给SQL传递参数

1.又有人问，菜鸟写的程序，被SQL注入怎么办？？

官方人士解析：

01.要想避免，就通过参数的方式，来书写SQL语句

02.通过存储过程，存储过程中使用参数

2.哪些年，童鞋们用过的@

解析：01.数据库中@@error：全局变量

@num:局部变量，程序员自己定义的变量

02.路径转义：@"D:\"

03.在SQL语句中进行参数化查询时，可以避免SQL注入

SqlParameter对象

在C#中获取存储过程的返回值

SqlParameter para=new SqlParameter("@myresult",SqlDBType.Int);

para.Dirction=ParameterDirction.Output;

para.Value;

## 3.会使用ADO.NET调用存储过程，包括SqlHelper类的使用

无参的存储过程

带输入参数的存储过程

带输入和输出参数的存储过程

## 4.con.CrateCommand()的用法

## 5.SQL语句中参数化模糊查询写法

解析：like '%'+@name+'%'


    private void btnOK_Click(object sender, EventArgs e)
            {
                string str = "Data Source=.;initial catalog=MySchool;uid=sa;pwd=6375196";

                SqlConnection con = new SqlConnection(str);
                string sql = "select * from student where studentname like '%'+@name+'%'";
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandText = sql;
                cmd.Parameters.Add(new SqlParameter("@name", txtName.Text));
                SqlDataAdapter da=new SqlDataAdapter(cmd);
                DataSet ds=new DataSet();
                da.Fill(ds, "Info");
                dataGridView1.DataSource = ds.Tables[0];

            }

SQL注入


                //登录按钮 用户名和密码不对也可以成功登录
                //1.1获取到用户名和密码
                string uname = txtName.Text;
                string pwd = txtPwd.Text;
                //1.2发送SQL指令，拼接SQL方式
                string str = "Data Source=.;Initial Catalog=MySchool;uid=sa;";
                string sql = "select count(1) from student where studentName='" + uname + "' and Loginpwd='" + pwd + "'";
                SqlConnection con = new SqlConnection(str);
                SqlCommand cmd = new SqlCommand(sql, con);
                con.Open();
                int count = Convert.ToInt32(cmd.ExecuteScalar());
                if (count > 0)
                {
                    MessageBox.Show("成功登录!");
                }
                else
                {
                    MessageBox.Show("失败!");
                }


                //用户名输入 ' or 1=1 --  密码输入 :随便输
                //SQL Server 查询的语句是  select count(1) from student where studentName='' or 1=1 --' and Loginpwd='sb


为防止SQL注入


                //1.1获取到用户名和密码
                string uname = txtName.Text;
                string pwd = txtPwd.Text;
                //1.2发送SQL指令，拼接SQL方式
                string str = "Data Source=.;Initial Catalog=MySchool;uid=sa;";
                string sql = "select count(1) from student where studentName=@name and loginpwd=@pwd";
                SqlConnection con = new SqlConnection(str);
                SqlCommand cmd = new SqlCommand(sql, con);

                con.Open();
                SqlParameter p1 = new SqlParameter("@name", uname);
                SqlParameter p2 = new SqlParameter("@pwd", pwd);
                cmd.Parameters.Add(p1);
                cmd.Parameters.Add(p2);
                try
                {
                    int count = Convert.ToInt32(cmd.ExecuteScalar());
                    if (count > 0)
                    {
                        MessageBox.Show("成功登录!");
                    }
                    else
                    {
                        MessageBox.Show("失败!");
                    }

                }
                catch (Exception)
                {

                    // throw;
                }

C#调用带输入参数的存储过程

数据库--->可编程性--->存储过程--->


    //开始把Alter改成如下的create
    create procedure usp_selectInfoOutput
    @sex nvarchar(32),
    @count int output
    as
    select * from Student where gender=@sex
    select @count=count(1) from student
    where gender=@sex
    return 100

按性别加载数据

在Main窗体中写


    //1.1  连接字符串
                string str = "data source=.;initial catalog=MySchool;uid=sa;";
                //1.2 创建连接对象    呵呵
                SqlConnection con = new SqlConnection(str);
                //创建SqlCommand 对象的第二种方式
                //从Con出发
                //1.3  从连接对象构建命令对象
                SqlCommand cmd = con.CreateCommand();
                //1.4  给命令对象需要执行的SQL语句赋值
                cmd.CommandText = "usp_selectInfo";
                //告诉SQL引擎我传递过来的是        存储过程的名称
                //1.5  我们告诉SQL引擎   我通过网线送过去的字符串是  一个存储过程的名字啊
                cmd.CommandType = CommandType.StoredProcedure;
                //1.6   构建存储过程的输入参数，并且给参数赋值，
                //参数的名称必须和定义存储过程的输入参数名称完成相同
                SqlParameter para = new SqlParameter("@sex", "1");
                //1.7   将参数和命令对象的参数集合绑定
                cmd.Parameters.Add(para);
                //1.8  打开数据库连接通道真正建立
                con.Open();
                //1.9   构建一个适配器 ）卡车（ 对象
                SqlDataAdapter da = new SqlDataAdapter();
                //1.10  将已经初始化好的cmd对象和da绑定
                da.SelectCommand = cmd;
                //1.11   构建内存中的数据集对象
                DataSet ds = new DataSet();
                //1.12   从DB   拎    数据到DataSet 中的一张表
                da.Fill(ds, "StuInfo");
                //1.13    将dgv的数据源指向表
                dgvList.DataSource = ds.Tables["StuInfo"];
                //1.14    连接关闭
                con.Close();

同上


                string str = "Data Source=.;Initial Catalog=MySchool;uid=sa;";
                SqlConnection con = new SqlConnection(str);
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandText = "usp_selectInfo";
                cmd.CommandType = CommandType.StoredProcedure;
                SqlParameter pare = new SqlParameter("@sex", "1");
                cmd.Parameters.Add(pare);
                con.Open();
                SqlDataAdapter da = new SqlDataAdapter();
                da.SelectCommand = cmd;
                DataSet ds = new DataSet();
                da.Fill(ds, "Info");
                dgvList.DataSource = ds.Tables["Info"];
                con.Close();

三: C#调用带输出和返回值的存储过程

在boy's number 的输出:5 在返回值:100 在 学生框中支持模糊查询 在dgvList控件输出查询的结果

数据库--->可编程性--->存储过程--->


    create procedure usp_selectInfoOutput
    @sex nvarchar(32),
    @count int output
    as
    select * from Student where gender=@sex
    select @count=count(1) from student
    where gender=@sex
    return 100

在<调用带输出和返回值的存储过程>窗体里写


     //1.1  连接字符串
                string str = "data source=.;initial catalog=MySchool;uid=sa;";
                //1.2 创建连接对象    呵呵
                SqlConnection con = new SqlConnection(str);
                SqlCommand cmd = con.CreateCommand();

                cmd.CommandText = "usp_selectInfoOutput";
                cmd.CommandType = CommandType.StoredProcedure;

                SqlParameter[] paras =
                {
                    new SqlParameter("@sex","1"),
                    //凭什么    C#  @count  输出参数
                    new SqlParameter("@count",SqlDbType.Int),
                    new SqlParameter("@myreturn",SqlDbType.Int)
                    //返回值
                };

                //为参数指定方向
                paras[1].Direction = ParameterDirection.Output;
                paras[2].Direction = ParameterDirection.ReturnValue;
                cmd.Parameters.AddRange(paras);
                SqlDataAdapter da = new SqlDataAdapter();
                da.SelectCommand = cmd;
                DataSet ds = new DataSet();
                da.Fill(ds, "StuInfo");

                dataGridView1.DataSource = ds.Tables["StuInfo"];
                //填充总人数
                txtNum.Text = paras[1].Value.ToString();
                txtReturn.Text = paras[2].Value.ToString();

四:模糊查询 在Select控件中写


    string name = '%' + "hhe" + '%';
                //1.1  连接字符串
                string str = "data source=.;initial catalog=MySchool;uid=sa;";
                //1.2 创建连接对象    呵呵
                SqlConnection con = new SqlConnection(str);
                SqlCommand cmd = con.CreateCommand();
                //1.3  SQL脚本       like后直接跟@name
                //cmd.CommandText = "select * from student where studentname like @name";
                //cmd.CommandType = CommandType.Text;
                //SqlParameter para = new SqlParameter("@name", '%' + txtName.Text + '%');
                //同下三行代码效果一样
                cmd.CommandText = "select * from student where studentname like '%'+@name+'%'";
                cmd.CommandType = CommandType.Text;
                SqlParameter para = new SqlParameter("@name",  txtName.Text);

                cmd.Parameters.Add(para);

                SqlDataAdapter da = new SqlDataAdapter();
                da.SelectCommand = cmd;
                DataSet ds = new DataSet();
                da.Fill(ds, "StuInfo");
                dataGridView1.DataSource = ds.Tables["StuInfo"];
