---
source: "http://blog.sina.com.cn/s/blog_545b2fb20100mkmr.html"
title: "MySQL批量执行sql语句_有为3060_新浪博客"
fetched_at: "2026-10-05 15:28:31"
---

[![新浪博客](//simg.sinajs.cn/blog7style/images/common/topbar/topbar_logo.gif)](//blog.sina.com.cn)

![](//simg.sinajs.cn/blog7style/images/common/loading.gif)加载中…

<http://blog.sina.com.cn/u/1415262130>

个人资料

![有为3060](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)

![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif) **有为3060**

[![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)微博](//weibo.com/u/1415262130?source=blog)

[加好友](javascript:void\(0\);) [发纸条](javascript:void\(0\);)

[写留言](//blog.sina.com.cn/s/profile_1415262130.html#write) 加关注

  * 博客等级：
  * 博客积分：**0**


  * 博客访问：**0**
  * 关注人气：**0**
  * 获赠金笔：**0支**
  * 赠出金笔：**0支**
  * 荣誉徽章：



正文 字体大小：[大](javascript:;) **中** [小](javascript:;)

## MySQL批量执行sql语句

(2010-11-08 22:01:50)

标签：

### mysql

### 批量

### it

|  分类： [数据库](//blog.sina.com.cn/s/articlelist_1415262130_5_1.html)  
---|---  
  
首先建立一个bat文件，然后用记事本打开bat文件并编辑如下：  
  
rem MySQL_HOME 本地MySQL的安装路径  
rem host mysql 服务器的ip地址，可以是本地，也可以是远程  
rem port mysql 服务器的端口，缺省为3306  
rem user password 具有操作数据库权限的用户名和密码，如root  
rem default-character-set 数据库所用的字符集  
rem database 要连接的数据名，这里用的qc1  
rem test.sql 要执行的脚本文件，这里为mysql.sql  
rem mysql 后面的应该放在一行。  
set MySQL_HOME=D:\database\MySQL\MySQL Server 5.1  
set PATH=%MySQL_HOME%\bin;%PATH%  
mysql --host=localhost --port=3306 --user=root --password=sa \--default-character-set=utf8 qc1 < mysql.sql  
pause  
  
保存后，双击bat文件运行即可 

分享：

![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)喜欢

0

![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)赠金笔

阅读 _┊_ [收藏](javascript:;) _┊_ [喜欢](javascript:;)[**▼**](javascript:;) _┊_[打印](//blog.sina.com.cn/main_v5/ria/print.html?blog_id=blog_545b2fb20100mkmr) _┊_举报/Report  
  
加载中，请稍候......

前一篇：[荐一款AWT/Swing第三方皮肤插件](//blog.sina.com.cn/s/blog_545b2fb20100lfqg.html)

后一篇：[制作bat:清理系统垃圾文件](//blog.sina.com.cn/s/blog_545b2fb20100n0bi.html)
