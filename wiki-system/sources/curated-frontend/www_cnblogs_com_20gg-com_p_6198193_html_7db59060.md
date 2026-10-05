---
source: "https://www.cnblogs.com/20gg-com/p/6198193.html"
title: "EasyUI、Struts2、Hibernate、spring 框架整合 - 丶疏影横斜 - 博客园"
fetched_at: "2026-10-05 15:31:24"
---

经历了四个月的学习，中间过程曲折离奇，好在坚持下来了，也到了最后框架的整合中间过程也只有自己能体会了。

接下来开始说一下整合中的问题和技巧：

1, jar包导入

c3p0(2个)、jdbc（1个）、spring（15个）、Hibernate（10个）、Struts2（13个）、json（3个）

及EasyUI的jquery包

2， 在src目录下新建一个实体类的包，并新建一个实体类


    package com.han.entity;

    import java.util.Date;

    public class Student {

        private String sno ;
        private String sname ;
        private String ssex ;
        private Date sbirthday ;
        private String sclass ;

        /*省略set、get方法*/
    }

3， 生成hibernate.cfg.xml的文件，并生成实体类的 Student.hbm.xml

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219180537244-1480285246.png)

值得提的是cfg.xml中并不需要连接数据库的驱动、用户名、用户密码及文件的映射，因为在spring中我们会添加这些配置

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219170247916-74963197.png)

4， 这里我们用的是连接池连接数据库

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219170546150-673682182.png)

db.properties的配置（放在src下面）：

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219170707760-570333817.png)

5， 接下来我们在app.xml配置中声明事务及事务的切点

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219181645478-1795313001.png)

6， 我们建如下包，并分别在对应包中建新的接口和实现类

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219182406510-1736185672.png)

7， 接下来我们开始Struts2的配置

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219194230525-1765329137.png)

这里要注意的是Action的name这里要与网页中发送地址对应，class对应的则是aap.xml中的id名，这里整合spring的话class不能写类的限定名，不然会有空指针异常，method就是Action这个类中的方法名

8， 这里整合spring所以我们都定义了接口及其实现类

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219195633697-1898184463.png)

9， 在service层中我们定义了一个dao接口的实例化作为属性，并设置了set方法

![](https://images2015.cnblogs.com/blog/1009603/201612/1009603-20161219195915307-1695963589.png)

10， 到这里基本的环境搭建就完成了

下面是每个层的具体方法：

dao层接口


    package com.hanqi.dao;

    import java.util.List;
    import java.util.Map;

    import com.han.entity.Student;

    public interface StudentDAO {

        //获取分页数据集合
        List<Student> find(int page, int rows, String sort, Map<String, String> map) ;

        //获取数据条数
        int findTotal(Map<String, String> map) ;

        //添加数据
        void add(Student stu) ;
    }

dao层接口的实现类impl


    package com.hanqi.dao.impl;

    import java.util.ArrayList;
    import java.util.List;
    import java.util.Map;

    import org.hibernate.Query;
    import org.hibernate.SessionFactory;

    import com.han.entity.Student;
    import com.hanqi.dao.StudentDAO;

    public class StudentDAOImpl implements StudentDAO {

        private SessionFactory sessionFactory ;

        public void setSessionFactory(SessionFactory sessionFactory) {
            this.sessionFactory = sessionFactory;
        }

        @Override
        public List<Student> find(int page, int rows, String sort, Map<String, String> map) {

            List<Student> list = new ArrayList<>() ;//定义list变量并实例化

            String sql = "from Student where 1=1 " ; //创建基础HQL语句

            String snames = map.get("snames") ;//接收参数

            if(snames != null && !snames.equals(""))//判断参数
            {
                sql += "and sname =:snames " ;//
            }

            String sclasss = map.get("sclasss") ;

            if(sclasss != null && !sclasss.equals(""))
            {
                sql += "and sclass =:sclasss " ;
            }

            if(sort != null && !sort.equals(""))
            {
                sql += "order by " + sort ;
            }

            Query qu = sessionFactory.getCurrentSession().createQuery(sql) ;

            if(snames != null && !snames.equals(""))
            {
                qu.setString("snames", snames) ;
            }

            if(sclasss != null && !sclasss.equals(""))
            {
                 qu.setString("sclasss", sclasss) ;
            }


            //System.out.println(sql);
            list = qu.setMaxResults(rows)//每页行数
                         .setFirstResult((page-1)*rows)//起始页码
                         .list() ;

            return list ;

        }

        @Override
        public int findTotal(Map<String, String> map) {
            int rtn = 0 ;//定义变量并赋值

            String sql = "select count(1) from Student where 1=1 " ;

            String snames = map.get("snames") ;//接收参数

            if(snames != null && !snames.equals(""))//判断参数
            {
                sql += "and sname =:snames " ;//
            }

            String sclasss = map.get("sclasss") ;

            if(sclasss != null && !sclasss.equals(""))
            {
                sql += "and sclass =:sclasss " ;
            }

            Query qu = sessionFactory.getCurrentSession().createQuery(sql) ;    //获取Query对象

            if(snames != null && !snames.equals(""))
            {
                qu.setString("snames", snames) ;
            }

            if(sclasss != null && !sclasss.equals(""))
            {
                 qu.setString("sclasss", sclasss) ;
            }

            List<Object> list = qu.list() ;//定义list变量并实例化

            if(list != null && list.size() > 0 )//判断获取的集合非空及长度
            {
                rtn = Integer.parseInt(list.get(0).toString()) ;//给变量rtn赋值
            }

            return rtn ;//返回变量值
        }

        @Override
        public void add(Student stu) {

            sessionFactory.getCurrentSession().save(stu) ;

        }

    }

service层接口


    package com.hanqi.service;

    import java.util.List;
    import java.util.Map;

    import com.han.entity.Student;

    public interface StudentService {

        //获取分页数据集合
        public List<Student> getList(int page, int rows, String sort, Map<String, String> map) ;

        //获取数据条数
        int getTotal(Map<String, String> map) ;

        //查询分页数据，并返回JSON
        String getPageJSON(int page, int rows, String sort, Map<String, String> map) ;

        //添加数据
        void insert(Student stu) ;
    }

service层接口的实现类impl


    package com.hanqi.service.impl;

    import java.util.List;
    import java.util.Map;

    import com.alibaba.fastjson.JSONArray;
    import com.alibaba.fastjson.JSONObject;
    import com.hanqi.service.PageJSON;
    import com.han.entity.Student;
    import com.hanqi.dao.StudentDAO;
    import com.hanqi.service.StudentService;

    public class StudentServiceImpl implements StudentService {

        private StudentDAO studentDAO ;

        public void setStudentDAO(StudentDAO studentDAO) {
            this.studentDAO = studentDAO;
        }

        @Override
        public List<Student> getList(int page, int rows, String sort, Map<String, String> map) {

            return studentDAO.find(page, rows, sort, map) ;

        }

        @Override
        public int getTotal(Map<String, String> map) {

            return studentDAO.findTotal(map) ;
        }

        @Override
        public String getPageJSON(int page, int rows, String sort, Map<String, String> map) {

            PageJSON<Student> pj = new PageJSON<Student>() ;

            String rtn = "{\"total\":0,\"rows\":[ ]}" ;//转义字符

            int total = studentDAO.findTotal(map) ;

            if(total > 0)
            {
                List<Student> list = studentDAO.find(page, rows, sort, map) ;

                //将List集合转为JSON集合
                String json_list = JSONArray.toJSONString(list) ;

                pj.setRows(list);
                pj.setTotal(total);

                rtn = JSONObject.toJSONString(pj) ;

                //转义字符返回复合类型的JSON字符串
                //rtn =  "{\"total\":"+total+",\"rows\":"+json_list+"}" ;
            }

            return rtn ;

        }

        @Override
        public void insert(Student stu) {

            studentDAO.add(stu);

        }

    }

action类（这里用的域模型来接受从页面传递过来的参数，即直接定义名字相同的属性值，并生成set、get方法）


    package com.hanqi.action;

    import java.io.IOException;
    import java.text.SimpleDateFormat;
    import java.util.HashMap;
    import java.util.Map;

    import javax.servlet.http.HttpServletResponse;

    import org.apache.struts2.ServletActionContext;

    import com.han.entity.Student;
    import com.hanqi.service.StudentService;

    public class StudentAction {

        private StudentService studentService ;

        public void setStudentService(StudentService studentService) {
            this.studentService = studentService;
        }

        public StudentService getStudentService() {
            return studentService;
        }

        private int page ;
        private int rows ;
        private String sort ;
        private String order ;

        private String snames ;
        private String sclasss ;

        @Override
        public String toString() {
            return "StudentAction [page=" + page + ", rows=" + rows + ", sort=" + sort + ", order=" + order + ", snames="
                    + snames + ", sclasss=" + sclasss + "]";
        }

        public int getPage() {
            return page;
        }

        public void setPage(int page) {
            this.page = page;
        }

        public int getRows() {
            return rows;
        }

        public void setRows(int rows) {
            this.rows = rows;
        }

        public String getSort() {
            return sort;
        }

        public void setSort(String sort) {
            this.sort = sort;
        }

        public String getOrder() {
            return order;
        }

        public void setOrder(String order) {
            this.order = order;
        }

        public String getSnames() {
            return snames;
        }

        public void setSnames(String snames) {
            this.snames = snames;
        }

        public String getSclasss() {
            return sclasss;
        }

        public void setSclasss(String sclasss) {
            this.sclasss = sclasss;
        }

        public void getStudentList()
        {
            System.out.println(this);

            try{
                //查询参数
                if(snames != null)
                {
                    snames =new String(snames.getBytes("ISO-8859-1"),"UTF-8") ;//转码
                }

                if(sclasss != null)
                {
                    sclasss =new String(sclasss.getBytes("ISO-8859-1"),"UTF-8") ;//转码
                }
                System.out.println("snames = "+ snames );

                System.out.println("sclasss = " + sclasss );

                Map<String, String> map = new HashMap<String, String>() ;

                map.put("snames", snames) ;
                map.put("sclasss", sclasss) ;

    //            map.put("snames","刘四") ;
    //            map.put("sclasss", "11111") ;
                String ls = "" ;

                System.out.println(order +"=" +sort);

                if(sort != null && order != null)
                {
                    ls = sort + " " + order ;
                }

                String json_list = studentService.getPageJSON(page, rows, ls, map) ;
                //返回数据
                //System.out.println("json = "+json_list);

                HttpServletResponse response = ServletActionContext.getResponse();

                response.setCharacterEncoding("UTF-8");

                response.getWriter().write(json_list) ;

            }catch(Exception e)
            {
                e.printStackTrace();
            }

        }

        //接收参数
        private String sno  ;
        private String sname ;
        private String ssex ;
        private String sclass ;
        private String sbirthday ;


        public String getSno() {
            return sno;
        }

        public void setSno(String sno) {
            this.sno = sno;
        }

        public String getSname() {
            return sname;
        }

        public void setSname(String sname) {
            this.sname = sname;
        }

        public String getSsex() {
            return ssex;
        }

        public void setSsex(String ssex) {
            this.ssex = ssex;
        }

        public String getSclass() {
            return sclass;
        }

        public void setSclass(String sclass) {
            this.sclass = sclass;
        }

        public String getSbirthday() {
            return sbirthday;
        }

        public void setSbirthday(String sbirthday) {
            this.sbirthday = sbirthday;
        }

        public void insert() throws IOException
        {
            if(sno != null  )
            {
                String msg ;

                try
                {
                    Student stu = new Student();

                    stu.setSclass(sclass);
                    stu.setSname(sname);
                    stu.setSno(sno);
                    stu.setSsex(ssex);

                    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");


                    stu.setSbirthday(sdf.parse(sbirthday));

                    studentService.insert(stu);

                    msg = "{'success':true,'message':'保存成功'}" ;

                }
                catch(Exception e)
                {
                    msg = "{'success':false,'message':'保存失败'}";
                    System.out.println("yichanghaha");

                }

                HttpServletResponse response = ServletActionContext.getResponse();

                response.setCharacterEncoding("UTF-8");

                response.getWriter().write(msg);
            }
            else
            {
                String msg = "{'success':false,'message':'访问异常'}" ;

                HttpServletResponse response = ServletActionContext.getResponse();

                response.setCharacterEncoding("UTF-8");

                response.getWriter().write(msg);
            }
        }

    }

同时在上面的action数据往前台html传送时我们为了返回json格式的字符串更加的方便灵活，我们定义了一个获取json

字符串格式的泛型辅助类，代码如下：


    package com.hanqi.service;

    import java.util.ArrayList;
    import java.util.List;

    public class PageJSON<T> {

        private int total = 0 ;

        private List<T> rows = new ArrayList<T>() ;

        public int getTotal() {
            return total;
        }

        public void setTotal(int total) {
            this.total = total;
        }

        public List<T> getRows() {
            return rows;
        }

        public void setRows(List<T> rows) {
            this.rows = rows;
        }


    }

Struts.xml


    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE struts PUBLIC
        "-//Apache Software Foundation//DTD Struts Configuration 2.3//EN"
        "http://struts.apache.org/dtds/struts-2.3.dtd">

    <struts>
        <!-- 允许调用静态方法和静态属性 -->
        <constant name="struts.ognl.allowStaticMethodAccess" value="true"></constant>
        <constant name="struts.action.extension" value="do,action,,"></constant>



                <action name="studentAction"
                        class="studentAction" method="getStudentList">
                        <!-- name 对应的是网页中的post/get请求 -->
                        <!-- 这里的class来源是spring配置中的id名 -->
                        <!-- method 方法是Action这个类中的方法 -->
                </action>

                <action name="addstudentAction"
                        class="studentAction" method="insert">
                        <!-- name 对应的是网页中的post/get请求 -->
                        <!-- 这里的class来源是spring配置中的id名 -->
                        <!-- method 方法是Action这个类中的方法 -->
                </action>


    </struts>

app.xml


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:context="http://www.springframework.org/schema/context"
        xmlns:aop="http://www.springframework.org/schema/aop"
        xmlns:p="http://www.springframework.org/schema/p"
        xmlns:tx="http://www.springframework.org/schema/tx"
        xmlns:jdbc="http://www.springframework.org/schema/jdbc"
        xsi:schemaLocation="http://www.springframework.org/schema/jdbc http://www.springframework.org/schema/jdbc/spring-jdbc-4.2.xsd
            http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.2.xsd
            http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.2.xsd
            http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.2.xsd">

    <!-- 基于c3p0连接池的数据源 -->
    <!-- 加载外部配置文件 -->
    <context:property-placeholder location="classpath:db.properties"/>

    <!-- 连接池 -->
    <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">






    </bean>


    <!-- Hibernate 的 SessionFactory -->
    <bean id="sessionFactory" class="org.springframework.orm.hibernate4.LocalSessionFactoryBean">




        <!-- 加载Hibernate的配置文件 -->


        <!-- 映射文件， 可以使用*作为通配符-->


    </bean>


    <!-- bean -->
    <!-- DAO -->
    <bean id="studentDAOImpl"  class="com.hanqi.dao.impl.StudentDAOImpl"
                p:sessionFactory-ref="sessionFactory"></bean>

    <!-- Service -->
    <bean id="studentServiceImpl" class="com.hanqi.service.impl.StudentServiceImpl"
                p:studentDAO-ref="studentDAOImpl"></bean>

    <!-- 配置Action -->
    <!-- Action 的实例不能是单例的 -->
    <bean id="studentAction" class="com.hanqi.action.StudentAction" scope="prototype"
    p:studentService-ref="studentServiceImpl"></bean>

    <!-- 声明式事务 -->
    <!-- 1.事务管理器 和sessionFactory关联 -->
    <bean id="transactionManager"
                class="org.springframework.orm.hibernate4.HibernateTransactionManager">

    </bean>

    <!-- 事务通知 -->
    <tx:advice id="adv" transaction-manager="transactionManager">
            <tx:attributes>
                    <tx:method name="*"/><!-- 使用事务的方法 -->
                    <tx:method name="get" read-only="true"/> <!-- get开头的只读方法，不使用事务 -->
                    <tx:method name="find" read-only="true"/> <!-- find开头的只读方法，不使用事务 -->
            </tx:attributes>
    </tx:advice>

    <!-- 事务切点 -->
    <aop:config>
            <aop:advisor advice-ref="adv" pointcut="execution(* com.hanqi.service.*.*(..))"/>  <!-- 接口 -->
    </aop:config>

    </beans>

Hibernate.cfg.xml


    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE hibernate-configuration PUBLIC "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
                                             "http://hibernate.sourceforge.net/hibernate-configuration-3.0.dtd">
    <hibernate-configuration>
     <session-factory >

      <!--  数据库方案-->
       TEST0816

      <!--  数据库方言-->
       org.hibernate.dialect.Oracle10gDialect

      <!--  调试-->
       true
       true

      <!-- 自动建表方式-->
       update

     </session-factory>
    </hibernate-configuration>

web.xml(这里同时还配置了过滤器要放在Struts配置之前)


    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" id="WebApp_ID" version="2.5">
      <display-name>Test41</display-name>
      <welcome-file-list>
        <welcome-file>index.html</welcome-file>
        <welcome-file>index.htm</welcome-file>
        <welcome-file>index.jsp</welcome-file>
        <welcome-file>default.html</welcome-file>
        <welcome-file>default.htm</welcome-file>
        <welcome-file>default.jsp</welcome-file>
      </welcome-file-list>

      <!-- 过虑器 -->
       <filter>
          <filter-name>encodingFilter</filter-name>
          <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
              <init-param>
                    encoding
                    UTF-8
              </init-param>
              <init-param>
                    forceEncoding
                    true
              </init-param>
         </filter>
      <filter-mapping>
              <filter-name>encodingFilter</filter-name>
              <url-pattern>/*</url-pattern>
         </filter-mapping>

      <!-- 加载 Struts2 过滤器配置 -->
      <filter>
            <filter-name>struts2</filter-name>
            <filter-class>org.apache.struts2.dispatcher.ng.filter.StrutsPrepareAndExecuteFilter</filter-class>
        </filter>

        <filter-mapping>
            <filter-name>struts2</filter-name>
            <url-pattern>/*</url-pattern>
        </filter-mapping>


      <!-- 加载 spring 配置 -->
      <!-- needed for ContextLoaderListener -->
        <context-param>
             contextConfigLocation
             classpath:app.xml
        </context-param>

        <!-- Bootstraps the root web application context before servlet initialization -->
        <listener>
            <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
        </listener>




    </web-app>

html（在页面的部分并没有多大改动，只是提交的servlert变成了Struts2的action）


    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>77</title>
    <!-- 1    jQuery的js包 -->


    <!-- 2    css资源 -->
    <link rel="stylesheet" type="text/css" href="jquery-easyui-1.4.4/themes/default/easyui.css">

    <!-- 3    图标资源 -->
    <link rel="stylesheet" type="text/css" href="jquery-easyui-1.4.4/themes/icon.css">

    <!-- 4    EasyUI的js包 -->


    <!-- 5    本地语言 -->


    </head>
    <body>


    //把long型日期转为想要类型
    function getDate(date)
    {
        //得到日期对象
        var d = new Date(date) ;

        //得到年月日
        var year = d.getFullYear() ;
        var month = (d.getMonth()+ 1) ;
        var day = d.getDate() ;

        //封装
        var tt = year+"-"+(month<10?"0"+month: month)+"-"+(day<10?"0"+day:day) ;

        return tt ;
        }

    //定义一个type变量，判断修改添加操作
    var type = "add" ;

    $(function(){
    $('#dg').datagrid({
        url:'studentAction.action',
        idField:'sno',
        frozenColumns:[ [ {field:'id',checkbox:true},//复选框
                          {field:'sno',title:'学号',width:100,align:'center'} ] ],
        columns:[[
            {field:'sname',title:'姓名',width:100,align:'center'},
            {field:'ssex',title:'性别',width:100,align:'center'},
            {field:'sbirthday',title:'生日',width:100,align:'center',
                formatter:function(value, row, index){
                    if(value && value != "")
                        {
                        //var valuee = new Date(value).toLocaleDateString();
                        //return valuee;

                        //调用function方法
                        return getDate(value) ;
                        }
                else
                    {
                        return  "" ;
                    }
                }},
            {field:'sclass',title:'班级',width:100,align:'center'}

        ]],
        pagination:true,//分页
        fitColumns:true,//列自适应宽度
        rownumbers:true,//显示行号
        striped:true,//斑马线
        singleSelect:false,//是否单选
        sortName:'sno',//排序字段
        sortOrder:'desc',//排序方式
        remoteSort:true,//服务器端排序
        toolbar:[
                 {iconCls:'icon-reload',text:'刷新',
                     handler:function(){
                        $("#dg").datagrid('reload');}},
                 {iconCls:'icon-search',text:'查询',
                             handler:function(){
                                 //序列化查询表单

                                var f =  $("#form2").serialize() ;

                                 //alert(f) ;
                                $("#dg").datagrid({url:"studentAction.action?"+f});
                                $("#form2").form("reset");
                                $("#dg").datagrid('reload');
                                }},
                 {iconCls:'icon-add',text:'添加',
                            handler:function(){
                                $("#sno").textbox({readonly:false});
                                type = "add" ;
                                //清除表单旧数据
                                $("#form1").form("reset");
                                $("#savestu").dialog('open').dialog('setTitle','New User');

                                }},

                 {iconCls:'icon-edit',text:'修改',handler:function(){
                     //alert("修改");
                     //设置主键字段为只读模式
                     $("#sno").textbox({readonly:true});

                     type = "edit" ;
                     $("#form1").form("reset");
                     var rt = $("#dg").datagrid('getSelected');
                     //document.write(rt);
                     if(rt)
                    {
                         $("#form1").form('load',{
                             sno:rt.sno,
                             sname:rt.sname,
                             sclass:rt.sclass,
                             ssex:rt.ssex,
                             sbirthday:getDate(rt.sbirthday)
                         } ) ;
                         $("#savestu").dialog('open').dialog('setTitle','Edit User');
                     }
                     else
                     {
                        $.messager.show({title:"提示",msg:"请选中一条记录"});
                    }
                    // $("#editstu").dialog('open') ;
                     }},
                 {iconCls:'icon-delete1',text:'单条删除',handler:function(){
                     var rt = $("#dg").datagrid('getSelected');
                     if(rt)
                         {
                         $.messager.confirm('Confirm','Are you sure you want to destroy this user?',
                                 function(r){
                                         if(r)
                                         {
                                            // alert(rt.sno);
                                            $.post('deleteServlet?sno='+rt.sno,function(result){var msg = eval('('  + result + ')') ;
                                                    if(msg.success){$("#dg").datagrid('reload');alert(msg.message)}});
                                         }

                         })}
                     else
                         {
                         $.messager.show({title:"提示",msg:"请选中一条记录"});
                         }
                 }},
                 {iconCls:'icon-delete1',text:'多条删除',handler:function(){
                     var rt = $("#dg").datagrid('getSelections');
                //保存选中记录的主键
                     var arr = [] ;
                     for(i in rt){
                         arr.push(rt[i].sno);
                    }
                    // alert(arr);
                     if(rt.length>0)
                         {
                         $.messager.confirm('Confirm','Are you sure you want to destroy these users?',
                                 function(r){
                                         if(r)
                                         {
                                            // alert(rt.sno);
                                            $.post('duoDeleteServlet?arr='+arr,function(result){var msg = eval('('  + result + ')') ;
                                                    if(msg.success){$("#dg").datagrid('reload');$.messager.show({title:'消息',msg:msg.message})}});
                                         }

                         })}
                     else
                         {
                         $.messager.show({title:"提示",msg:"请选中至少一条记录"});
                         }
                 }}]
    });
    })


            <form action=""  id="form2">
            姓名<input class="easyui-textbox" id="snames" name="snames">
            班级<input class="easyui-textbox" id="sclasss" name="sclasss">
            </form>

    <table id="dg"></table>


    <form action="" id="form1" method="post">
    <table border="0" width="100%">

        <tr>
                <td align="right" width="30%" >学号</td>
                <td><input class="easyui-textbox" id="sno" name="sno"
                                      data-options="required:true,validType:'length[3,3]'"></td>
        </tr>
        <tr>
                <td align="right" width="30%">姓名</td>
                <td><input class="easyui-textbox" id="sname" name="sname"
                                      data-options="required:true,validType:'length[2,4]'"></td>
        </tr>
        <tr>
                <td align="right" width="30%">性别</td>
                <td><input type="radio" name="ssex" value="男" checked>男
                        <input type="radio" name="ssex" value="女">女</td>
        </tr>
        <tr>
                <td align="right" width="30%">班级</td>
                <td><input class="easyui-textbox" id="sclass" name="sclass"
                                      data-options="required:true,validType:'length[5,5]'"></td>
        </tr>
        <tr>
                <td align="right" width="30%">生日</td>
                <td><input class="easyui-datebox" id="sbirthday" name="sbirthday"
                                      data-options="required:false,showSeconds:true"></td>
        </tr>
    </table>
    </form>




    </body>
    </html>
