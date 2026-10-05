---
source: "http://blog.csdn.net/xiaokui_wingfly/article/details/8265208"
title: "Java zTree 的异步加载demo示例_ztree 异步加载的 demo-CSDN博客"
fetched_at: "2026-10-05 15:31:09"
---

查看原文：<http://www.ibloger.net/article/419.html>

最近需要使用树形展示权限，所以研究了一下Java Tree，其实java中有不少Tree展示，具体有如下几种：![吐舌头](http://static.blog.csdn.net/xheditor/xheditor_emot/default/tongue.gif)

Tree的几种开源组件：
1.**dtree**

**2.ztree(国内的，api全中文，我用这个)**

****3.**JTree**

4.**dhtmlxTree**(国外的，种类齐全)，网址为:_http://dhtmlx.com/docs/products/dhtmlxTree/index.shtml_

##以后是我找的还不错的Tree组件，还有很多！

具体使用方式请参考**zTreeAPI或zTree Demo**

**（1）编写数据库脚本添加数据**

![](https://img-my.csdn.net/uploads/201211/29/1354176987_6431.png)

**（2）定义一个基本权限类：Competence.java**


    public class Competence {
    	private int id; // 编号
    	private int pId;	// 父节点
    	private int isParent;	// 是否父节点
    	private String name;	// 节点名称
    	private int open;	// 是否打开



    	// 此处省略 get,set方法


    ｝


**（3）创建BaseDao.java联接数据库**


    package com.demo.test;

    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;
    import java.sql.Statement;

    /**
     * 连接数据源
     * @author 小奎
     */
    public class BaseDao {
    	 static Connection conn; // 创建联接
    	 PreparedStatement st; // 　预执行类
    	 ResultSet rs; // 结果集

    	/**
    	 *  得到连接
    	 *  @return connnection
    	 */
    	public static Connection getConnection() {
    		try {
    			// 加载驱动
    			Class.forName("oracle.jdbc.driver.OracleDriver");
    			try {
    				// 创建联接
    				conn = DriverManager.getConnection("jdbc:oracle:thin:@127.0.0.1:1521:orcl", "scott", "scott");
    				System.out.println("---------------- 打开连接 -----------------");
    			} catch (SQLException e) {
    				System.out.println("---------------- 连接失败 -----------------");
    				e.printStackTrace();
    			}
    		} catch (ClassNotFoundException e) {
    			System.out.println("---------------- 驱动加载失败 -----------------");
    			e.printStackTrace();
    		}
    		return conn;
    	}

    	/**
    	 * 关闭连接对象
    	 * @param rs
    	 * @param st
    	 * @param conn
    	 */
    	public static void closeConnection(ResultSet rs, Statement st, Connection conn) {
    		try {
    			if (rs != null) {
    				rs.close();
    			}
    			if (st != null) {
    				st.close();
    			}
    			if (conn != null && !conn.isClosed()) {
    				conn.close();
    			}
    			System.out.println("---------------- 关闭连接 -----------------");
    		} catch (SQLException e) {
    			System.out.println("---------------- 关闭连接失败 -----------------");
    			e.printStackTrace();
    		}
    	}
    }



       <strong>（4） 创建测试的类 Test.java </strong>   package com.demo.test;

    import java.sql.Connection;
    import java.sql.SQLException;
    import java.util.ArrayList;
    import java.util.List;

    public class Test extends BaseDao {

    	public List<Competence> getAllAuthorize() {
    		List<Competence> authorizes = new ArrayList<Competence>();
    		Connection conn = getConnection(); // 得到联接
    		try {
    			st = conn.prepareStatement("select * from authorize2 ");
    			rs = st.executeQuery(); // 得到结果集
    			while (rs.next()) {
    				Competence authorize = new Competence();
    				authorize.setId(rs.getInt("id"));
    				authorize.setpId(rs.getInt("pid"));
    				authorize.setOpen(rs.getInt("open"));
    				authorize.setIsParent(rs.getInt("isParent"));
    				authorize.setName(rs.getString("name"));
    				// 添加到集合
    				authorizes.add(authorize);
    			}
    		} catch (SQLException e) {
    			System.out.println("---------------- 查询authorize失败 -----------------");
    			e.printStackTrace();
    		} finally {
    			closeConnection(rs, st, conn);
    		}
    		return authorizes;
    	}

    	/**
    	 * 拼接成json类型
    	 * @return
    	 */
    	public String getJSONData(){
    		Test d = new Test();
    		List<Competence> list=d.getAllAuthorize();
    		StringBuffer json=new StringBuffer("[");
    		String data="";
    		for (int i = 0; i < list.size(); i++) {
    			json.append("{id:"+list.get(i).getId()+",");
    			json.append("pId:"+list.get(i).getpId()+",");
    			json.append("name:\""+list.get(i).getName()+"\",");
    			if (list.get(i).getIsParent() !=0) {
    				json.append("isParent:"+list.get(i).getIsParent()+",");
    			}
    			if (list.get(i).getOpen() !=0) {
    				json.append("open:"+list.get(i).getOpen()+",");
    			}
    			data=json.substring(0,json.lastIndexOf(","))+"},";
    			json=new StringBuffer(data);
    		}
    		data=json.substring(0, json.length()-1)+"]";
    		System.out.println(data);
    		return data;
    	}
    	public static void main(String[] args) {
    		Test demoTest=new Test();
    		demoTest.getJSONData();
    	}
    }



**（4） 创建加载zTree 树的html或jsp页面 asyncLoad.html**


    <!DOCTYPE html>
    <HTML>
    <HEAD>
    <TITLE>zTree Demo</TITLE>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="../css/demo.css" type="text/css">
    <!-- 必须文件 zTreeStyle.css、jquery.ztree.core-x.js、jquery-x.min.js -->
    <link rel="stylesheet" href="../css/zTreeStyle/zTreeStyle.css" type="text/css">



    	var setting = {
    		async : {
    			enable : true, // 设置 zTree是否开启异步加载模式
    			url : "asyncData/loadData2.jsp", // Ajax 获取数据的 URL 地址
    			autoParam : [ "id" ]	// 异步加载时自动提交父节点属性的参数,假设父节点 node = {id:1, name:"test"}，异步加载时，提交参数 zId=1
    		},
    		data:{ // 必须使用data
     			simpleData : {
    				enable : true,
    				idKey : "id", // id编号命名 默认
    				pIdKey : "pId", // 父id编号命名 默认
    				rootPId : 0	// 用于修正根节点父节点数据，即 pIdKey 指定的属性值
    			}
    		},
    		// 回调函数
    		callback : {
    			onClick : function(event, treeId, treeNode, clickFlag) {
    				// 判断是否父节点
    				if(!treeNode.isParent){
    					alert("treeId自动编号：" + treeNode.tId + ", 节点id是：" + treeNode.id + ", 节点文本是：" + treeNode.name);
    				}
    			},
    			//捕获异步加载出现异常错误的事件回调函数 和 成功的回调函数
    			onAsyncError : zTreeOnAsyncError,
    			onAsyncSuccess : function(event, treeId, treeNode, msg){

    			}
    		}
    	};

    	// 加载错误提示
    	function zTreeOnAsyncError(event, treeId, treeNode, XMLHttpRequest, textStatus, errorThrown) {
    		alert("加载错误：" + XMLHttpRequest);
    	};

    	// 过滤函数
    	function filter(treeId, parentNode, childNodes) {
    		if (!childNodes)
    			return null;
    		for ( var i = 0, l = childNodes.length; i < l; i++) {
    			childNodes[i].name = childNodes[i].name.replace(/\.n/g, '.');
    		}
    		return childNodes;
    	}

    	// 渲染
    	$(document).ready(function() {
    		$.fn.zTree.init($("#treeDemo"), setting);
    	});

    </HEAD>
    <BODY>

    		<ul id="treeDemo" class="ztree"></ul>

    </BODY>
    </HTML>


**（5） 创建一个接收的Servlet，本测试使用jsp代替 loadData.jsp**


    <%@ page language="java" import="java.util.*" pageEncoding="utf-8"%>
    <%@ page import="com.demo.test.*" %>

    <%
    		String id = request.getParameter("id");	// 父节点编号
    		System.out.print("得到的节点id："+id);
    		Test demo=new Test();
    		String json=demo.getJSONData();
    		out.print(json);
    %>


**注：json数据最终会被拼接成array的形式，如下结果：雷同即可显示**


    [{id:100,pId:0,name:"父节点",isParent:1,open:1},{id:101,pId:100,name:"叶子节点—1",isParent:1},{id:102,pId:100,name:"叶子节点—2",isParent:1},{id:103,pId:100,name:"叶子节点—3",isParent:1},{id:104,pId:0,name:"NB的父节点",isParent:1,open:1},{id:105,pId:104,name:"叶子节点2—1",isParent:1},{id:106,pId:104,name:"叶子节点2—2",isParent:1},{id:107,pId:104,name:"叶子节点2—3"},{id:108,pId:0,name:"郁闷的父节点",isParent:1},{id:109,pId:108,name:"叶子节点3—1"},{id:110,pId:108,name:"叶子节点3—2"},{id:111,pId:108,name:"叶子节点3—3"},{id:112,pId:101,name:"秘书"},{id:113,pId:101,name:"行政"},{id:114,pId:102,name:"助理"},{id:115,pId:102,name:"保安"},{id:116,pId:103,name:"销售"},{id:117,pId:103,name:"前台"},{id:118,pId:103,name:"主管"},{id:119,pId:105,name:"卫生"},{id:120,pId:106,name:"人事"}]

**效果如图**

![](https://img-my.csdn.net/uploads/201211/29/1354178695_6895.png)


这里的小测试使用了子父节点同时加载完毕效果，加载完毕后，单击父节点不会再次访问数据库，会从缓存中加载。所以这里使用的**open** 属性有效果，如果是单击父节点，加载子节点再次访问数据库的方式，open可能无效。

json的数据中如**isParent:1** ，这样的数据1代表**true**
