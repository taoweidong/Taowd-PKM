---
source: "http://www.cnblogs.com/IT-1994/p/c3p0-jndi.html"
title: "C3p0连接池配置 - 书升 - 博客园"
fetched_at: "2026-10-05 15:32:58"
---

在Java开发中，使用JDBC操作数据库的四个步骤如下：

①加载数据库驱动程序(Class.forName("数据库驱动类");)
②连接数据库(Connection con = DriverManager.getConnection();)
③操作数据库(PreparedStatement stat = con.prepareStatement(sql);stat.executeQuery();)
④关闭数据库，释放连接(con.close();)
也就是说，所有的用户都需要经过此四步进行操作，但是这四步之中有三步(①加载数据库驱动程序、②连接数据库、④关闭数据库，释放连接)对所有人都是一样的，而所有人只有在操作数据库上是不一样，那么这就造成了性能的损耗。
那么最好的做法是，准备出一个空间，此空间里专门保存着全部的数据库连接，以后用户用数据库操作的时候不用再重新加载驱动、连接数据库之类的，而直接从此空间中取走连接，关闭的时候直接把连接放回到此空间之中。

那么此空间就可以称为连接池（保存所有的数据库连接）

C3P0相关认识

C3P0是一个开源的JDBC[连接池](http://baike.baidu.com/view/1528732.htm)，它实现了数据源和JNDI绑定，支持JDBC3规范和JDBC2的标准扩展。目前使用它的[开源项目](http://baike.baidu.com/view/188327.htm)有 _Hibernate，Spring_ 等。

什么是连接池：

连接池是创建和管理一个连接的缓冲池的技术，这些连接准备好被任何需要它们的线程使用；简单理解为，当一辆汽车搬运东西，如果使用jdbc连接，(jdbc连接:与数据库建立连接、发送操作数据库的语句并处理结果)那么每一次都要去打开数据库，获得连接，关闭数据库。假设汽车搬运的东西是连接，那么我可不可以每一次将连接搬运多个呢？而不是jdbc那样，一次只搬运一个连接，然后就把汽车扔掉？这时候，使用连接池。

原理：

连接池基本的思想是在[系统初始化](http://baike.baidu.com/view/811790.htm)的时候，将数据库连接作为对象存储在内存中，当用户需要访问数据库时，并非建立一个新的连接，而是从连接池中取出一个已建立的空闲连接对象。使用完毕后，用户也并非将连接关闭，而是将连接放回连接池中，以供下一个请求访问使用。而连接的建立、断开都由连接池自身来管理。同时，还可以通过设置连接池的参数来控制连接池中的初始连接数、连接的上下限数以及每个连接的最大使用次数、最大空闲时间等等。也可以通过其自身的管理机制来监视数据库连接的数量、使用情况等。

为什么要用到连接池

数据库连接池的基本思想就是为数据库连接建立一个“缓冲池”。预先在缓冲池中放入一定数量的连接，当需要建立数据库连接时，只需从“缓冲池”中取出一个，使用完毕之后再放回去。我们可以通过设定连接池最大连接数来防止系统无尽的与数据库连接。连接池主要由三部分组成：连接池的建立、连接池中连接的使用管理、连接池的关闭。

数据库连接池的最小连接数和最大连接数的设置要考虑到以下几个因素:

  1. 最小连接数:是连接池一直保持的数据库连接,所以如果应用程序对数据库连接的使用量不大,将会有大量的数据库连接资源被浪费.
  2. 最大连接数:是连接池能申请的最大连接数,如果数据库连接请求超过次数,后面的数据库连接请求将被加入到等待队列中,这会影响以后的数据库操作
  3. 如果最小连接数与最大连接数相差很大:那么最先连接请求将会获利,之后超过最小连接数量的连接请求等价于建立一个新的数据库连接.不过,这些大于最小连接数的数据库连接在使用完不会马上被释放,他将被放到连接池中等待重复使用或是空间超时后被释放

使用c3p0需要导包:

c3p0-0.9.5.2-sources.jar

mchange-commons-java-0.2.11-sources.jar

c3p0-oracle-thin-extras-0.9.5.2.jar

hsqldb.jar

commons-pool-1.4.jar

commons-dbcp-1.2.2.jar

将包导入到lib中

测试代码：

连接oracle数据库

使用c3p0-config.xml配置：


    package com.c3p0;

    import java.sql.Connection;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;
    import java.sql.Statement;

    import com.mchange.v2.c3p0.ComboPooledDataSource;

    public class TestC3P0 {
          static ComboPooledDataSource cpds=null;
            static{
                //这里有个优点，写好配置文件，想换数据库，简单
                //cpds = new ComboPooledDataSource("oracle");//这是oracle数据库
                cpds = new ComboPooledDataSource("oracle");//这是mysql数据库
            }
            /**
             * 获得数据库连接
             * @return   Connection
             */
            public static Connection getConnection(){
                try {
                    return cpds.getConnection();
                } catch (SQLException e) {
                    e.printStackTrace();
                    return null;
                }
            }

            /**
             * 数据库关闭操作
             * @param conn
             * @param st
             * @param pst
             * @param rs
             */
            public static void close(Connection conn,PreparedStatement pst,ResultSet rs){
                if(rs!=null){
                    try {
                        rs.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
                if(pst!=null){
                    try {
                        pst.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }

                if(conn!=null){
                    try {
                        conn.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
            }
            /**
             * 测试DBUtil类
             * @param args
             */
            public static void main(String[] args) {
                Connection conn=getConnection();
                System.out.println(conn.getClass().getName());
                Statement stmt;
                ResultSet rs=null;
                try {
                    stmt = conn.createStatement();
                    rs=stmt.executeQuery("select empno from emp");
                    while(rs.next()){
                        System.out.println(rs.getInt(1));
                    }
                } catch (SQLException e) {
                    e.printStackTrace();
                } finally {
                    try {
                        conn.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
                close(conn,null,null);
            }
    }


配置文件：c3p0-config.xml(路径放在src下)


    <?xml version="1.0" encoding="UTF-8"?>
    <c3p0-config>
    <named-config name="oracle">
             oracle.jdbc.driver.OracleDriver
             jdbc:oracle:thin:@192.168.85.2:1521:orcl
             scott
             tiger
             10
             30
             100
             10
             200
        </named-config>
    </c3p0-config>

java配置连接hsqldb数据库

以下测试代码需要开启hsqldb，否则会有异常信息(具体方法请看[proxool+hsqldb](http://www.cnblogs.com/IT-1994/p/5886584.html))

hsqldb.jar --> org.hsqldb.server --> Server 右击选择run -->java Application ，开启hsqldb

新建监听类，继承 ServletContextListenpackage com.c3p0.Listener;


    import java.beans.PropertyVetoException;
    import java.sql.Connection;
    import java.sql.SQLException;

    import javax.annotation.Resource;
    import javax.naming.InitialContext;
    import javax.naming.NamingException;
    import javax.servlet.ServletContextEvent;
    import javax.servlet.ServletContextListener;
    import javax.servlet.annotation.WebListener;
    import javax.sql.DataSource;

    import com.mchange.v2.c3p0.ComboPooledDataSource;


    @WebListener
    public class cplistener implements ServletContextListener {
        @Override
        public void contextDestroyed(ServletContextEvent arg0) {
            com.close();
        }

        @Override
        public void contextInitialized(ServletContextEvent arg0) {
          //封装数据库连接
    　　　　private ComboPooledDataSource com = new ComboPooledDataSource();

            System.out.println("初始化参数");

            try {
                 //加载hsqldb数据库的驱动
                com.setDriverClass("org.hsqldb.jdbc.JDBCDriver");
                //使用客户端连接
                com.setJdbcUrl("jdbc:hsqldb:hsql://localhost/");
                com.setUser("sa");           //账号
                com.setPassword("");         //密码
                com.setMaxPoolSize(15);      //最大连接数
                com.setMaxIdleTime(10);      //设置连接时间
                Connection conn = com.getConnection();
                arg0.getServletContext().setAttribute("conn", conn);
                } catch (PropertyVetoException e) {
                e.printStackTrace();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

使用properties配置文件连接hsqldb

新建c3p0.properties(注意名字必须为这个，放在src文件夹下面)


    c3p0.driverClass=org.hsqldb.jdbc.JDBCDriver
    c3p0.jdbcUrl=jdbc:hsqldb:hsql://localhost/
    c3p0.user=sa
    c3p0.password=

测试代码


    package com.c3p0.Listener;

    import java.beans.PropertyVetoException;
    import java.sql.Connection;
    import java.sql.SQLException;

    import javax.annotation.Resource;
    import javax.naming.InitialContext;
    import javax.naming.NamingException;
    import javax.servlet.ServletContextEvent;
    import javax.servlet.ServletContextListener;
    import javax.servlet.annotation.WebListener;
    import javax.sql.DataSource;

    import com.mchange.v2.c3p0.ComboPooledDataSource;

    @WebListener
    public class cplistener implements ServletContextListener {
        //封装数据库连接
        private ComboPooledDataSource com = new ComboPooledDataSource();
        @Override
        public void contextDestroyed(ServletContextEvent arg0) {
            com.close();
        }

        @Override
        public void contextInitialized(ServletContextEvent arg0) {
            // TODO Auto-generated method stub
            System.out.println("监听数据库连接");
            //使用java代码配置hsqldb
            try {
                Connection conn = com.getConnection();
                //将连接赋值给上下文的属性中，后期可通过请求获取
                arg0.getServletContext().setAttribute("conn", conn);
            } catch (SQLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            System.out.println("监听初始化方法结束");
        }
    }

使用jndi连接mysql数据库

导包：mysql-connector-java-5.1.39-bin.jar，可将包导入到Tomcat服务器lib中。

注意:mysql数据库必须启动

使用JNDI数据源
在项目Servers中，该项目是Tomcat导入eclipse中的自动生成的，里面是配置文件信息，找到context.xml，将以下代码添加进去

代码：


    <Resource
            name="jdbc/mysql"
            auth="Container"
            type="javax.sql.DataSource"
            maxActive="100"
            maxIdle="30"
            maxWait="10000"
            username="root"
            password="root"
            driverClassName="com.mysql.jdbc.Driver"
            url="jdbc:mysql://localhost:3306/mysql?useUnicode=true&characterEncoding=utf-8"/>

注意：

1、name的名字必须和等下在Web.xml中一样，还有在java代码中连接数据库语句的一处一样。

2、这里使用的是mysql数据库连接，外部mysql服务器必须开着。

3、jdbc:mysql://localhost:3306/mysql中的mysql是你mysql中的数据库，必须存在，否则会包null错误

4、如果异常报空，要么就是配置文件错误，要么就是mysql中没有当前的数据库错误。

5、context.xml配置信息，当eclipse项目删除Tomcat服务器的时候，该配置需要重新配置

在Web.xml配置中添加以下代码


    <resource-ref>
     <res-ref-name>jdbc/mysql</res-ref-name>
     <res-type>javax.sql.DataSource</res-type>
     <res-auth>Container</res-auth>
    </resource-ref>

java代码，新建监听类继承 ServletContextListener


    package com.c3p0.Listener;

    import java.beans.PropertyVetoException;
    import java.sql.Connection;
    import java.sql.SQLException;

    import javax.annotation.Resource;
    import javax.naming.InitialContext;
    import javax.naming.NamingException;
    import javax.servlet.ServletContextEvent;
    import javax.servlet.ServletContextListener;
    import javax.servlet.annotation.WebListener;
    import javax.sql.DataSource;

    import com.mchange.v2.c3p0.ComboPooledDataSource;

    @WebListener
    public class cplistener implements ServletContextListener {
        //封装数据库连接
        private ComboPooledDataSource com = new ComboPooledDataSource();
        @Override
        public void contextDestroyed(ServletContextEvent arg0) {
            com.close();
        }

        @Override
        public void contextInitialized(ServletContextEvent arg0) {
            // TODO Auto-generated method stub
            System.out.println("初始化参数");

            Connection connMySQL = null;
            try {
                //1、初始化名称查找上下文
                InitialContext ctx = new InitialContext();
                //2、通过JNDI名称找到DataSource,对名称进行定位java:comp/env是必须加的,后面跟的是DataSource名
                /*
                DataSource名在web.xml文件中的<res-ref-name>jdbc/mysql</res-ref-name>进行了配置
                  <!--MySQL数据库JNDI数据源引用 -->
                  <resource-ref>
                      <res-ref-name>jdbc/mysql</res-ref-name>
                      <res-type>javax.sql.DataSource</res-type>
                      <res-auth>Container</res-auth>
                  </resource-ref>
                */
                DataSource ds = (DataSource)ctx.lookup("java:comp/env/jdbc/mysql");
                //3、通过DataSource取得一个连接
                connMySQL = ds.getConnection();
                System.out.println("连接正常！");
                //4、操作数据库
            } catch (NamingException e) {
                System.out.println(e.getMessage());
            } catch (SQLException e) {
                e.printStackTrace();
            } finally {
                //5、关闭数据库，关闭的时候是将连接放回到连接池之中
                try {
                    connMySQL.close();
                } catch (SQLException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
    }




    Java连接池编辑
    在Java中开源的数据库连接池有以下几种 ：
    1、C3P0：是一个开放源代码的JDBC连接池，它在lib目录中与Hibernate[2]  一起发布，包括了实现jdbc3和jdbc2扩展规范说明的Connection 和Statement 池的DataSources 对象。
    2、Proxool：是一个Java SQL Driver驱动程序，提供了对选择的其它类型的驱动程序的连接池封装。可以非常简单的移植到现存的代码中，完全可配置，快速、成熟、健壮。可以透明地为现存的JDBC驱动程序增加连接池功能。
    3、Jakarta DBCP：DBCP是一个依赖Jakartacommons-pool对象池机制的数据库连接池。DBCP可以直接的在应用程序中使用。
    4、DDConnectionBroker：是一个简单、轻量级的数据库连接池。
    5、DBPool：是一个高效、易配置的数据库连接池。它除了支持连接池应有的功能之外，还包括了一个对象池，使用户能够开发一个满足自己需求的数据库连接池。
    6、XAPool：是一个XA数据库连接池。它实现了javax.sql.XADataSource并提供了连接池工具。
    7、Primrose：是一个Java开发的数据库连接池。当前支持的容器包括Tomcat4&5、Resin3与JBoss3。它同样也有一个独立的版本，可以在应用程序中使用而不必运行在容器中。Primrose通过一个WEB接口来控制SQL处理的追踪、配置，以及动态池管理。在重负荷的情况下可进行连接请求队列处理。
    8、SmartPool：是一个连接池组件，它模仿应用服务器对象池的特性。SmartPool能够解决一些临界问题如连接泄漏（connection leaks）、连接阻塞、打开的JDBC对象（如Statements、PreparedStatements）等。SmartPool的特性包括：
    支持多个pool
    自动关闭相关联的JDBC对象
    在所设定time-outs之后察觉连接泄漏
    追踪连接使用情况
    强制启用最近最少用到的连接
    把SmartPool“包装”成现存的一个pool
    9、MiniConnectionPoolManager：是一个轻量级JDBC数据库连接池。它只需要Java1.5（或更高）并且没有依赖第三方包。
    10、BoneCP：是一个快速、开源的数据库连接池。帮用户管理数据连接，让应用程序能更快速地访问数据库。比C3P0/DBCP连接池速度快25倍。
    11、Druid：Druid不仅是一个数据库连接池，还包含一个ProxyDriver、一系列内置的JDBC组件库、一个SQL Parser。
    支持所有JDBC兼容的数据库，包括Oracle、MySql、Derby、Postgresql、SQL Server、H2等。
    Druid针对Oracle和MySql做了特别优化，比如：
    Oracle的PS Cache内存占用优化
    MySql的ping检测优化
    Druid提供了MySql、Oracle、Postgresql、SQL-92的SQL的完整支持，这是一个手写的高性能SQL Parser，支持Visitor模式，使得分析SQL的抽象语法树很方便。
    简单SQL语句用时10微秒以内，复杂SQL用时30微秒。
    通过Druid提供的SQL Parser可以在JDBC层拦截SQL做相应处理，比如说分库分表、审计等。Druid防御SQL注入攻击的WallFilter，就是通过Druid的SQL Parser分析语义实现的

Java连接池常识点
