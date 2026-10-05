---
source: "http://yangzb.iteye.com/blog/1132591"
title: "oracle复制表数据，复制表结构  - 东写西读终见大海无量 - ITeye博客"
fetched_at: "2026-10-05 15:40:51"
---

[首页](https://www.iteye.com/) [资讯](https://www.iteye.com/news) [精华](https://www.iteye.com/magazines) [论坛](https://www.iteye.com/forums) [问答](https://www.iteye.com/ask) [博客](https://www.iteye.com/blogs) [专栏](https://www.iteye.com/blogs/subjects) [群组](https://www.iteye.com/groups) [下载](https://www.iteye.com/resources)

* __搜索

[您还未登录!](/login "登录") [登录](/login)

`

[![yangzb的博客](https://www.iteye.com/upload/logo/user/987595/911e3d2c-f27f-3041-af76-3d6e8fe21f87.jpg?1717537097)](https://www.iteye.com/blog/user/yangzb)

yangzb

  * 浏览: 3712208 次
  * 性别: ![Icon_minigender_1](https://www.iteye.com/images/icon_minigender_1.gif?1652290086)
  * 来自: 北京
  * ![](/images/status/offline.gif)

##### 最近访客  [更多访客>>](/blog/user_visits)

[![lizhensan的博客](https://www.iteye.com/upload/logo/user/446615/8b84c851-506e-3269-ba87-e1035f6b3744-thumb.gif?1717537309)](https://www.iteye.com/blog/user/lizhensan)

[lizhensan](https://www.iteye.com/blog/user/lizhensan "lizhensan")

[![morelily的博客](https://www.iteye.com/upload/logo/user/694981/41bde6ef-6d99-3162-9c46-a5113f02596d-thumb.jpg?1717536556)](https://www.iteye.com/blog/user/morelily)

[morelily](https://www.iteye.com/blog/user/morelily "morelily")

[![magicfish1981的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/magicfish1981)

[magicfish1981](https://www.iteye.com/blog/user/magicfish1981 "magicfish1981")

[![duquancool的博客](https://www.iteye.com/upload/logo/user/973121/cc7b582d-079f-3124-9233-472653b0a8cf-thumb.jpg?1717537286)](https://www.iteye.com/blog/user/duquancool)

[duquancool](https://www.iteye.com/blog/user/duquancool "duquancool")

##### 博主相关

* [博客](https://www.iteye.com/blog/user/yangzb)
* [微博](/weibo)
* [相册](/album)
* [收藏](/link)
* [留言](/blog/guest_book)
* [关于我](/blog/profile)

##### 文章分类

  * [全部博客 (822)](/blog/user/yangzb)
  * [Portal (3)](/category/37917)
  * [Framework (92)](/category/37918)
  * [C++ (19)](/category/37919)
  * [Java (172)](/category/37920)
  * [工作流 (1)](/category/37921)
  * [Security (22)](/category/37922)
  * [商务活动 (9)](/category/40444)
  * [Database (79)](/category/41069)
  * [CI (5)](/category/41207)
  * [QC (29)](/category/41285)
  * [PM (49)](/category/41292)
  * [服务器 (83)](/category/41672)
  * [开发工具 (26)](/category/44292)
  * [数字电视 (23)](/category/49448)
  * [网络 (21)](/category/50839)
  * [PaySys (38)](/category/54104)
  * [Game (2)](/category/54603)
  * [Ruby (12)](/category/95194)
  * [LAMP (5)](/category/68031)
  * [HA (10)](/category/68047)
  * [操作系统 (43)](/category/93428)
  * [其他 (70)](/category/56516)
  * [宇宇语录 (1)](/category/107699)
  * [GIS (1)](/category/108710)
  * [Hazelcast (4)](/category/139287)
  * [Grails (7)](/category/142673)

##### 社区版块

  * [我的资讯](/blog/news) ( 0)
  * [我的论坛](/blog/post) ( 3)
  * [我的问答](/blog/answered_problems) ( 0)

##### 存档分类

  * [2013-03](/blog/monthblog/2013-03) ( 1)
  * [2012-12](/blog/monthblog/2012-12) ( 2)
  * [2012-11](/blog/monthblog/2012-11) ( 1)
  * [更多存档...](/blog/monthblog_more)

##### 最新评论

  * [wanglf1207](https://www.iteye.com/blog/user/wanglf1207 "wanglf1207")： EJB的确是个不错的产品，只是因为用起来有点门槛，招来太多人吐 ...
[weblogic-ejb-jar.xml的元素解析 ](/blog/353924#bc2399976)
  * [qwfys200](https://www.iteye.com/blog/user/qwfys200 "qwfys200")： 总结的不错。
[Spring Web Flow 2.0 入门](/blog/377426#bc2398229)
  * [u011577913](https://www.iteye.com/blog/user/u011577913 "u011577913")： u011577913 写道也能给我发一份翻译文档？ 邮件437 ...
[Hazelcast 参考文档-4](/blog/862152#bc2392471)
  * [u011577913](https://www.iteye.com/blog/user/u011577913 "u011577913")： 也能给我发一份翻译文档？
[Hazelcast 参考文档-4](/blog/862152#bc2392469)
  * [songzj001](https://www.iteye.com/blog/user/songzj "songzj001")：
[DbUnit入门实战](/blog/947292#bc2385045)

[yangzb](https://www.iteye.com/blog/user/yangzb)

###  oracle复制表数据，复制表结构 __

**博客分类：**
  * [Database](/category/41069)

阅读更多

1.不同用户之间的表数据复制
对于在一个数据库上的两个用户A和B，假如需要把A下表old的数据复制到B下的new，请使用权限足够的用户登入sqlplus：
insert into B.new(select * from A.old);

如果需要加条件限制，比如复制当天的A.old数据
insert into B.new(select * from A.old where date=GMT);
蓝色斜线处为选择条件

2.同用户表之间的数据复制
用户B下有两个表：B.x和B.y，如果需要从表x转移数据到表y，使用用户B登陆sqlpus即可：
insert into 目标表y select * from x where log_id>'3049' -- 复制数据
注意：要示目标表y必须事先创建好
如insert into bs_log2 select * from bs_log where log_id>'3049'


3.B.x中个别字段转移到B.y的相同字段
\--如果两个表结构一样
insert into table_name_new select * from table_name_old
如果两个表结构不一样：
insert into y(字段1,字段2) select 字段1,字段2 from x

4.只复制表结构 加入了一个永远不可能成立的条件1=2，则此时表示的是只复制表结构，但是不复制表内容
create table 用户名.表名 as select * from 用户名.表名 where 1=2
如create table zdsy.bs_log2 as select * from zdsy.bs_log where 1=2

5完全复制表(包括创建表和复制表中的记录)
create table test as select * from bs_log --bs_log是被复制表


6 将多个表数据插入一个表中
insert into 目标表test(字段1。。。字段n) (select 字段1.。。。。字段n) from 表 union all select 字段1.....字段n from 表


=====================================================
oracle和mssql中复制表的比较

库内数据复制
MS SQL Server：
Insert into 复制表名称 select 语句 (复制表已经存在)
select 字段列表 into 复制表名称 from 表 (复制表不存在)

Oracle ：
Insert into 复制表名称 select 语句 (复制表已经存在)
create table 复制表名称 as select 语句 (复制表不存在)

多表更新、删除

一条更新语句是不能更新多张表的，除非使用触发器隐含更新，我这里说的意思是：根据其他表数据更新你要更新的表一般形式：
MS SQL Server
update ASET 字段1=B表字段表达式,字段2=B表字段表达式from BWHERE 逻辑表达式

Oracle
update ASET 字段1=(select 字段表达式 from B WHERE ...),字段2=(select 字段表达式 from B WHERE ...) WHERE 逻辑表达式
从以上来看，感觉oracle没有ms sql好，主要原因：假如A需要多个字段更新，MS_SQL 语句更简练你知道刚学数据库的人怎么做上面这件事情

吗，他们使用游标一条一条的处理

＝＝＝＝导入＝＝导出＝＝＝＝＝＝＝＝＝＝＝
（1）导出
exp [ff/ff@orcl](mailto:ff/ff@orcl) file='d:ff.dmp' tables=customers direct=y
使用exp 输出。输入的为需要备份的用户表的账号和密码,根据提示一直点回车就OK 结束后将会出现一个ff.DMP文件,此文件为备份数据。
导出时可以选择导出：1.整个数据库（需具备dba权限）；2.用户（包括表、视图和其它）；3.表（只包含表，不导出视图）；

（2）导入
create user ly identified by pw default tablespace users quota 10M on users;
创建新用户 用户名为ly 密码为pw 默认表空间为此空间,配额为10M
grant connect,resource,dba to ly;
赋予ly权限（1.连接；2.资源；3.dba权限，必须具备才能执行导入！）
grant create session,create table,create view,unlimited tablespaces to ly;
赋予ly其它常用权限(1.登陆到服务器,2.创建表,3.创建视图,4.无限表空间)
imp [ly/ly@ORCL](mailto:ly/ly@ORCL) fromuser=ff touser=ly file='d:ff.dmp' constraints=n
使用 imp 输入。输入需要导入的用户的用户名和密码 然后点回车,根据提示一直到再次要求你输入用户名的地方。

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

sql_server不同数据库间复制表

不同数据库表结构 和数据的复制 ：
目标数据库不存在要导入的表时：
example：
xuexiao为目标数据库，teaching为源数据库，dbo.course_list已经存在于teaching，想在没有此表的xuexiao库中复制一个用下面的语句完成

：
select * into xuexiao.dbo.course_list from teaching.dbo.course_list

不同数据库之间复制表的数据的方法

当表目标表存在时：
insert into 目的数据库..表 select * from 源数据库..表

当目标表不存在时：
select * into 目的数据库..表 from 源数据库..表
=================================================
如下，表a是数据库中已经存在的表，b是准备根据表a进行复制创建的表：

1、只复制表结构的sql
create table b as select * from a where 1<>1

2、即复制表结构又复制表中数据的sql
create table b as select * from a

3、复制表的制定字段的sql
create table b as select row_id,name,age from a where 1<>1//前提是row_id,name,age都是a表的列

4、复制表的指定字段及这些指定字段的数据的sql
create table b as select row_id,name,age from a

以上语句虽然能够很容易的根据a表结构复制创建b表，但是a表的索引等却复制不了，需要在b中手动建立。

5、insert into 会将查询结果保存到已经存在的表中
insert into t2(column1, column2, ....) select column1, column2, .... from t1

1、获得单个表和索引DDL语句的方法：

\-----------------------------------------------------------------------

set heading off;

set echo off;

Set pages 999;

set long 90000;



spool get_single.sql

select dbms_metadata.get_ddl( 'TABLE ', 'SZT_PQSO2 ', 'SHQSYS ') from dual;

select dbms_metadata.get_ddl( 'INDEX ', 'INDXX_PQZJYW ', 'SHQSYS ') from dual;

spool off;

分享到： [![](/images/sina.jpg)](javascript:; "分享到新浪微博") [![](/images/tec.jpg)](javascript:; "分享到腾讯微博")

  * 2011-07-25 21:19
  * 浏览 36714
  * 评论(0)
  * 分类:[数据库](https://www.iteye.com/blogs/category/database)
  * [查看更多](https://www.iteye.com/wiki/blog/1132591)

Global site tag (gtag.js) - Google Analytics
