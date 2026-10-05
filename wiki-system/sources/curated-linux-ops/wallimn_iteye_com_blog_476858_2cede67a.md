---
source: "http://wallimn.iteye.com/blog/476858"
title: "Log4J输出日志到WEB工程目录的实现方法 - 隔壁老王 - ITeye博客"
fetched_at: "2026-10-05 15:36:11"
---

[首页](https://www.iteye.com/) [资讯](https://www.iteye.com/news) [精华](https://www.iteye.com/magazines) [论坛](https://www.iteye.com/forums) [问答](https://www.iteye.com/ask) [博客](https://www.iteye.com/blogs) [专栏](https://www.iteye.com/blogs/subjects) [群组](https://www.iteye.com/groups) [下载](https://www.iteye.com/resources)

* __搜索

[您还未登录!](/login "登录") [登录](/login)

`

[![wallimn的博客](https://www.iteye.com/upload/logo/user/1215014/0f9c49b3-bb43-34d6-873c-064beef228c9.jpg?1717536505)](https://www.iteye.com/blog/user/wallimn)

wallimn

  * 浏览: 5485556 次
  * 性别: ![Icon_minigender_1](https://www.iteye.com/images/icon_minigender_1.gif?1652290086)
  * 来自: 北京
  * ![](/images/status/offline.gif)

##### 最近访客  [更多访客>>](/blog/user_visits)

[![yhf8866的博客](https://www.iteye.com/upload/logo/user/1171244/2d1e4595-73e4-354d-b212-8e12dbfc8338-thumb.jpg?1717537145)](https://www.iteye.com/blog/user/yhf8866)

[yhf8866](https://www.iteye.com/blog/user/yhf8866 "yhf8866")

[![ZZ_lll的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/zz-lll)

[ZZ_lll](https://www.iteye.com/blog/user/zz-lll "ZZ_lll")

[![java-007的博客](https://www.iteye.com/upload/logo/user/1325623/aaa75b48-befa-323a-96c9-209997ef4f19-thumb.jpg?1767504295)](https://www.iteye.com/blog/user/java-007)

[java-007](https://www.iteye.com/blog/user/java-007 "java-007")

[![xckouy的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/xckouy)

[xckouy](https://www.iteye.com/blog/user/xckouy "xckouy")

##### 博主相关

* [博客](https://www.iteye.com/blog/user/wallimn)
* [微博](/weibo)
* [相册](/album)
* [收藏](/link)
* [留言](/blog/guest_book)
* [关于我](/blog/profile)

##### 文章分类

  * [全部博客 (1118)](/blog/user/wallimn)
  * [JAVA、WEB开发 (460)](/category/55614)
  * [数据库 (298)](/category/55615)
  * [桌面程序(VC、Dephi、.Net) (61)](/category/55616)
  * [android (7)](/category/349475)
  * [Linux (38)](/category/55746)
  * [存储知识 (11)](/category/193402)
  * [精彩美文 (1)](/category/70786)
  * [杂文 (74)](/category/55729)
  * [English (9)](/category/77259)
  * [GIS (4)](/category/64824)
  * [成长日志(1) (24)](/category/334211)
  * [成长日志(2) (12)](/category/334213)
  * [成长日志(3) (12)](/category/334214)
  * [成长日志(4) (12)](/category/334215)
  * [成长日志(5) (12)](/category/334216)
  * [成长日志(6) (12)](/category/55809)
  * [成长日志(7) (11)](/category/351752)
  * [成长日志(8) (7)](/category/368106)
  * [留影 (18)](/category/226081)
  * [游记 (8)](/category/334187)
  * [生活趣事 (6)](/category/226080)
  * [D90 (22)](/category/252365)

##### 社区版块

  * [我的资讯](/blog/news) ( 0)
  * [我的论坛](/blog/post) ( 22)
  * [我的问答](/blog/answered_problems) ( 0)

##### 存档分类

  * [2024-09](/blog/monthblog/2024-09) ( 1)
  * [2024-02](/blog/monthblog/2024-02) ( 2)
  * [2023-02](/blog/monthblog/2023-02) ( 2)
  * [更多存档...](/blog/monthblog_more)

##### 最新评论

  * [silence19841230](https://www.iteye.com/blog/user/silence19841230 "silence19841230")： 先拿走看看
[SpringBoot2.0开发WebSocket应用完整示例](/blog/2425666#bc2403797)
  * [wallimn](https://www.iteye.com/blog/user/wallimn "wallimn")： masuweng 写道发下源码下载地址吧!三个相关文件打了个包 ...
[SpringBoot2.0开发WebSocket应用完整示例](/blog/2425666#bc2403427)
  * [masuweng](https://www.iteye.com/blog/user/basobunn2688 "masuweng")： 发下源码下载地址吧!
[SpringBoot2.0开发WebSocket应用完整示例](/blog/2425666#bc2403423)
  * [masuweng](https://www.iteye.com/blog/user/basobunn2688 "masuweng")：
[SpringBoot2.0开发WebSocket应用完整示例](/blog/2425666#bc2403419)
  * [wallimn](https://www.iteye.com/blog/user/wallimn "wallimn")： 水淼火 写道你好,我使用以后,图标不显示,应该怎么引用呢,谢谢 ...
[前端框架iviewui使用示例之菜单+多Tab页布局](/blog/2403931#bc2403227)

[wallimn](https://www.iteye.com/blog/user/wallimn)

###  Log4J输出日志到WEB工程目录的实现方法 __

**博客分类：**
  * [JAVA、WEB开发](/category/55614)

[log4j](http://www.iteye.com/blogs/tag/log4j)[Web](http://www.iteye.com/blogs/tag/Web)[配置管理](http://www.iteye.com/blogs/tag/%E9%85%8D%E7%BD%AE%E7%AE%A1%E7%90%86)[Servlet](http://www.iteye.com/blogs/tag/Servlet)[网络应用](http://www.iteye.com/blogs/tag/%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8)

阅读更多

将Log4j的日志输出的web工程目录会方便系统移植、日志远程查看。那么如何来实现呢？可以通过一个自定义的Servlet设置系统属性的方法来实现，只需要几句代码，而且可配置、移植方便。
**一、Servlet代码**




    package com.wallimn.gyz.util;

    import javax.servlet.ServletException;

    import javax.servlet.http.HttpServlet;

    /**

     * 设置一些系统变量

     * 博客：http://wallimn.iteye.com

     * 编码：wallimn　时间：2009-9-25　下午12:16:27

     * 版本：V1.0

     */

    public class SystemServlet extends HttpServlet {



    	private static final long serialVersionUID = 8164865597169685698L;

    	/**

    	 * 读配置，设置系统变量

    	 */

    	public void init() throws ServletException {

    		String rootPath = this.getServletContext().getRealPath("/");

    		String log4jPath = this.getServletConfig().getInitParameter("wallimn.log4j.path");

    		//若没有指定wallimn.log4j.path初始参数，则使用WEB的工程目录

    		log4jPath = (log4jPath==null||"".equals(log4jPath))?rootPath:log4jPath;

    		System.setProperty("wallimn.log4j.path", log4jPath);

    		super.init();

    	}

    }




**二、web.xml文件配置**
<servlet>
<servlet-name>SystemServlet</servlet-name>
<servlet-class>com.wallimn.gyz.util.SystemServlet</servlet-class>
<init-param>
 wallimn.log4j.path
<!--引自若未指定，则使用工程目录，若指定，使用指定目录-->

</init-param>
<load-on-startup>0</load-on-startup>
</servlet>

**三、log4j.properties文件配置（输出到工程目录下的logs子目录中）**
log4j.appender.FILEOUT = org.apache.log4j.DailyRollingFileAppender
log4j.appender.FILEOUT.File = ${wallimn.log4j.path}logs/log.html
log4j.appender.FILEOUT.Append = true
log4j.appender.FILEOUT.Threshold = DEBUG
log4j.appender.FILEOUT.layout = org.apache.log4j.HTMLLayout

**网上流传的另一种方法：**[color=brown][/color]

具体实现：编写一个 servlet, 在系统加载的时候, 就把 properties 的文件读到一个 properties 文件中。那个 file 的属性值(我使用的是相对目录)改掉(前面加上系统的根目录)，然后把这个 properties 对象设置到 propertyConfig 中去，这样就初始化了 log 的设置。在后面的使用中就用不着再配置了。
一般在我们开发项目过程中，log4j 日志输出路径固定到某个文件夹，这样如果我换一个环境，日志路径又需要重新修改，比较不方便，目前我采用了动态改变日志路径的方法来实现相对路径保存日志文件
(1) 在项目启动时,装入初始化类:


public class Log4jInit extends HttpServlet {

static Logger logger = Logger.getLogger(Log4jInit.class);

public Log4jInit() {
}

public void init(ServletConfig config) throws ServletException {
String prefix = config.getServletContext().getRealPath("/");
String file = config.getInitParameter("log4j");
String filePath = prefix + file;
Properties props = new Properties();
try {
FileInputStream istream = new FileInputStream(filePath);
props.load(istream);
istream.close();
//toPrint(props.getProperty("log4j.appender.file.File"));
String logFile = prefix + props.getProperty("log4j.appender.file.File");//设置路径
props.setProperty("log4j.appender.file.File",logFile);
PropertyConfigurator.configure(props);//装入log4j配置信息
} catch (IOException e) {
toPrint("Could not read configuration file [" + filePath + "].");
toPrint("Ignoring configuration file [" + filePath + "].");
return;
}
}

public static void toPrint(String content) {
System.out.println(content);
}
}

实际上 log4j 的配置文件如果为默认名称: log4j.properties，则可放置在 JVM 能读到的 classpath 里的任意地方，一般是放在 WEB-INF/classes 目录下。当log4j 的配置文件不再是默认名称，则需要另外加载并给出参数，如上 "PropertyConfigurator.configure(props);//装入log4j配置信息"。

(2) web.xml 中的配置


<servlet>
<servlet-name>log4j-init</servlet-name>
<servlet-class>Log4jInit</servlet-class>
<init-param>
 log4j
 WEB-INF/classes/log4j.properties
</init-param>
<load-on-startup>1</load-on-startup> </servlet>

注意：上面的 load-on-startup 设为 0 ，以便在 Web 容器启动时即装入该 Servlet 。log4j.properties 文件放在根的properties子目录中，也可以把它放在其它目录中。应该把 .properties 文件集中存放，这样方便管理。

(3) log4j.properties 中即可配置 log4j.appender.file.File 为当前应用的相对路径
/***********本人原创，欢迎转载，转载请保留本人信息*************/
作者：wallimn 电邮：wallimn@sohu.com 时间：2009-09-24
博客：http://wallimn.iteye.com
网络硬盘：http://wallimn.ys168.com
/***********文章发表请与本人联系，作者保留所有权利*************/

分享到： [![](/images/sina.jpg)](javascript:; "分享到新浪微博") [![](/images/tec.jpg)](javascript:; "分享到腾讯微博")

  * 2009-09-24 22:47
  * 浏览 10485
  * 评论(4)
  * 分类:[编程语言](https://www.iteye.com/blogs/category/language)
  * [查看更多](https://www.iteye.com/wiki/blog/476858)

Global site tag (gtag.js) - Google Analytics
