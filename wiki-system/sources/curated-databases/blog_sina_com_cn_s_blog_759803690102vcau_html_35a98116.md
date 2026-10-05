---
source: "http://blog.sina.com.cn/s/blog_759803690102vcau.html"
title: "MYSQL批量插入数据库实现语句性能分析_kidswoods_新浪博客"
fetched_at: "2026-10-05 15:28:28"
---

[![新浪博客](//simg.sinajs.cn/blog7style/images/common/topbar/topbar_logo.gif)](//blog.sina.com.cn)

![](//simg.sinajs.cn/blog7style/images/common/loading.gif)加载中…

<http://blog.sina.com.cn/u/1972896617>

个人资料

![kidswoods](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)

![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif) **kidswoods**

[![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)微博](//weibo.com/u/1972896617?source=blog)

[加好友](javascript:void\(0\);) [发纸条](javascript:void\(0\);)

[写留言](//blog.sina.com.cn/s/profile_1972896617.html#write) 加关注

  * 博客等级：
  * 博客积分：**0**


  * 博客访问：**0**
  * 关注人气：**0**
  * 获赠金笔：**0支**
  * 赠出金笔：**0支**
  * 荣誉徽章：



正文 字体大小：[大](javascript:;) **中** [小](javascript:;)

## MYSQL批量插入数据库实现语句性能分析

(2014-12-09 01:30:15)

标签：

### 股票

|  分类： [数据库/网络/java/php学习](//blog.sina.com.cn/s/articlelist_1972896617_4_1.html)  
---|---  
  
假定我们的表结构如下

代码如下 |   
---|---  
CREATE TABLE example (  
example_id INT NOT NULL,  
name VARCHAR( 50 ) NOT NULL,  
value VARCHAR( 50 ) NOT NULL,  
other_value VARCHAR( 50 ) NOT NULL  
)  
  
通常情况下单条插入的sql语句我们会这么写：

代码如下 |   
---|---  
INSERT INTO example  
(example_id, name, value, other_value)  
VALUES  
(100, 'Name 1', 'Value 1', 'Other 1');  
  
[mysql](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=mysql&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=2&seller_id=1&di=8)允许我们在一条sql语句中批量插入数据，如下sql语句：

代码如下 |   
---|---  
INSERT INTO example  
(example_id, name, value, other_value)  
VALUES  
(100, 'Name 1', 'Value 1', 'Other 1'),  
(101, 'Name 2', 'Value 2', 'Other 2'),  
(102, 'Name 3', 'Value 3', 'Other 3'),  
(103, 'Name 4', 'Value 4', 'Other 4');  
  
如果我们插入列的顺序和表中列的顺序一致的话，还可以省去列名的定义，如下sql

代码如下 |   
---|---  
INSERT INTO example  
VALUES  
(100, 'Name 1', 'Value 1', 'Other 1'),  
(101, 'Name 2', 'Value 2', 'Other 2'),  
(102, 'Name 3', 'Value 3', 'Other 3'),  
(103, 'Name 4', 'Value 4', 'Other 4');  
  
上面看上去没什么问题，下面我来使用[sql](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=sql&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=1&seller_id=1&di=8)语句优化的小技巧，下面会分别进行测试，目标是插入一个空的[数据](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=%EF%BF%BD%EF%BF%BD%EF%BF%BD&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=5&seller_id=1&di=8)表200W条数据

第一种方法：使用insert into 插入，代码如下：

代码如下 |   
---|---  
  
$params = array('value'=>'50');  
set_time_limit(0);  
echo date("H:i:s");  
for($i=0;$i<2000000;$i++){  
$connect_mysql->insert($params);  
};  
echo date("H:i:s");  
  
最后显示为：23:25:05 01:32:05 也就是花了2个小时多!

第二种方法：使用事务提交，批量插入[数据库](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=3&seller_id=1&di=8)(每隔10W条提交下)最后显示消耗的时间为：22:56:13 23:04:00 ，一共8分13秒 ，代码如下：

代码如下 |   
---|---  
echo date("H:i:s");  
  
$connect_mysql->query('BEGIN');  
$params = array('value'=>'50');  
for($i=0;$i<2000000;$i++){   
$connect_[mysql](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=mysql&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=2&seller_id=1&di=8)->insert($params);  
if($i0000==0){  
$connect_mysql->query('COMMIT');  
$connect_mysql->query('BEGIN');  
}  
}  
$connect_mysql->query('COMMIT');  
echo date("H:i:s");  
  
第三种方法：使用优化SQL语句：将SQL语句进行[拼接](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=%C6%B4%EF%BF%BD%EF%BF%BD&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=4&seller_id=1&di=8)，使用 insert into table () values (),(),(),()然后再一次性插入，如果字符串太长，

则需要配置下MYSQL，在[mysql](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=mysql&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=2&seller_id=1&di=8) 命令行中运行 ：set global max_allowed_packet = 2*1024*1024*10;消耗时间为：11:24:06 11:25:06;

插入200W条测试数据仅仅用了1分钟!代码如下：

代码如下 |   
---|---  
$sql= "insert into twenty_million (value) values";  
for($i=0;$i<2000000;$i++){  
$sql.="('50'),";  
};  
$sql = substr($sql,0,strlen($sql)-1);  
$connect_[mysql](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=mysql&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=2&seller_id=1&di=8)->query($[sql](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=sql&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=1&seller_id=1&di=8));  
  
最后总结下，在插入大批量[数据](http://cpro.baidu.com/cpro/ui/uijs.php?rs=1&u=http://www.3lian.com/edu/2013/07-15/80916.html&p=baidu&c=news&n=10&t=tpclicked3_hc&q=3liancpr&k=%EF%BF%BD%EF%BF%BD%EF%BF%BD&k0=sql&kdi0=4&k1=mysql&kdi1=8&k2=%EF%BF%BD%EF%BF%BD%DD%BF%EF%BF%BD&kdi2=8&k3=%C6%B4%EF%BF%BD%EF%BF%BD&kdi3=1&k4=%EF%BF%BD%EF%BF%BD%EF%BF%BD&kdi4=8&sid=410c50feb03e1236&ch=0&tu=u1833515&jk=d121c74465a45616&cf=29&fv=15&stid=9&urlid=0&luki=5&seller_id=1&di=8)时，第一种方法无疑是最差劲的，而第二种方法在实际应用中就比较广泛，第三种方法在插入测试数据或者其他低要求时比较合适，速度确实快。

分享：

![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)喜欢

0

![](//simg.sinajs.cn/blog7style/images/common/sg_trans.gif)赠金笔

阅读 _┊_ [收藏](javascript:;) _┊_ [喜欢](javascript:;)[**▼**](javascript:;) _┊_[打印](//blog.sina.com.cn/main_v5/ria/print.html?blog_id=blog_759803690102vcau) _┊_举报/Report  
  
加载中，请稍候......

前一篇：[java连接mysql批量写入数据](//blog.sina.com.cn/s/blog_759803690102vcat.html)

后一篇：[Everything You Need to Know About the HyperTransport Bus](//blog.sina.com.cn/s/blog_759803690102vfya.html)
