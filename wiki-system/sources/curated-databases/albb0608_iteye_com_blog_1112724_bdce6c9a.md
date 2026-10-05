---
source: "http://albb0608.iteye.com/blog/1112724"
title: "Oracle 查看索引表空间 -  - ITeye博客"
fetched_at: "2026-10-05 15:27:50"
---

[首页](https://www.iteye.com/) [资讯](https://www.iteye.com/news) [精华](https://www.iteye.com/magazines) [论坛](https://www.iteye.com/forums) [问答](https://www.iteye.com/ask) [博客](https://www.iteye.com/blogs) [专栏](https://www.iteye.com/blogs/subjects) [群组](https://www.iteye.com/groups) [下载](https://www.iteye.com/resources)

* __搜索

[您还未登录!](/login "登录") [登录](/login)

` 

[![albb0608的博客](https://www.iteye.com/upload/logo/user/330660/8ef8a423-2f44-3adc-ab7c-93fd5c57e380.png?1717536912)](https://www.iteye.com/blog/user/albb0608)

albb0608

  * 浏览: 66628 次
  * 性别: ![Icon_minigender_1](https://www.iteye.com/images/icon_minigender_1.gif?1652290086)
  * 来自: 北京 
  * ![](/images/status/offline.gif)



##### 最近访客  [更多访客>>](/blog/user_visits)

[![xubukang的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/xubukang)

[xubukang](https://www.iteye.com/blog/user/xubukang "xubukang")

[![bookboy008的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/bookboy008)

[bookboy008](https://www.iteye.com/blog/user/bookboy008 "bookboy008")

[![fangyong2006的博客](https://www.iteye.com/upload/logo/user/929770/633e0ca1-4e81-3eeb-8789-f1b1324df5d5-thumb.jpg?1717536686)](https://www.iteye.com/blog/user/fangyong2006)

[fangyong2006](https://www.iteye.com/blog/user/fangyong2006 "fangyong2006")

[![qnanii的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/qnanii)

[qnanii](https://www.iteye.com/blog/user/qnanii "qnanii")

##### 博主相关

* [博客](https://www.iteye.com/blog/user/albb0608)
* [微博](/weibo)
* [相册](/album)
* [收藏](/link)
* [留言](/blog/guest_book)
* [关于我](/blog/profile)

##### 文章分类

  * [全部博客 (9)](/blog/user/albb0608)
  * [Spring (1)](/category/127199)
  * [Java (2)](/category/150183)
  * [Oracle (4)](/category/150184)
  * [Lucene (0)](/category/150185)
  * [Struts (0)](/category/150186)
  * [software (0)](/category/150187)
  * [Thread (1)](/category/162488)
  * [Hadoop (2)](/category/191967)
  * [jsp (1)](/category/231661)



##### 社区版块

  * [我的资讯](/blog/news) ( 0)
  * [我的论坛](/blog/post) ( 33) 
  * [我的问答](/blog/answered_problems) ( 10)



##### 存档分类

  * [2012-07](/blog/monthblog/2012-07) ( 1)
  * [2011-12](/blog/monthblog/2011-12) ( 1)
  * [2011-11](/blog/monthblog/2011-11) ( 1)
  * [更多存档...](/blog/monthblog_more)



##### 最新评论

  * [wxno1](https://www.iteye.com/blog/user/wxno1 "wxno1")： 阳光晒晒 写道wxno1 写道decode 解决一切行转列，可 ...  
[前天笔试碰到的一个题，是列转行的，大家帮看看](/blog/980212#bc2047852)
  * [阳光晒晒](https://www.iteye.com/blog/user/sunyday "阳光晒晒")： wxno1 写道decode 解决一切行转列，可惜只有orac ...  
[前天笔试碰到的一个题，是列转行的，大家帮看看](/blog/980212#bc2044620)
  * [xici_magic](https://www.iteye.com/blog/user/qianzui "xici_magic")： Case函数能解决。  
[前天笔试碰到的一个题，是列转行的，大家帮看看](/blog/980212#bc2042294)
  * [ganjp](https://www.iteye.com/blog/user/ganjp "ganjp")： 咦……哈哈  
[前天笔试碰到的一个题，是列转行的，大家帮看看](/blog/980212#bc2041651)
  * [qiang106](https://www.iteye.com/blog/user/qiang106 "qiang106")： 好像Oracle、MySQL 用case可以，SQLServe ...  
[前天笔试碰到的一个题，是列转行的，大家帮看看](/blog/980212#bc2041457)



[albb0608](https://www.iteye.com/blog/user/albb0608)

###  Oracle 查看索引表空间 __

**博客分类：**
  * [Oracle](/category/150184)



[Oracle](http://www.iteye.com/blogs/tag/Oracle)

阅读更多

引用

摘要： Oracle 查看索引表空间，Oracle 查看索引表空间语句，包括查看表空间的使用情况、查看数据库库对象、查看数据库的版本、查看数据库创建日期和归档方式、查询数据库中索引占用表空间的大小。 Oracle 查看表空间的使用情况或表空间的大小，应该如何实现呢？下面就为您介

  
  
Oracle 查看索引表空间，Oracle 查看索引表空间语句，包括查看表空间的使用情况、查看数据库库对象、查看数据库的版本、查看数据库创建日期和归档方式、查询数据库中索引占用表空间的大小。   
  
Oracle 查看表空间的使用情况或表空间的大小，应该如何实现呢？下面就为您介绍实现 Oracle 查看表空间方面的语句。   
  
1、查看表空间的使用情况   
  

    
    
     
    select sum(bytes)/(1024*1024) as free_space,tablespace_name 
    from dba_free_space
    group by tablespace_name;
    
    
    SELECT A.TABLESPACE_NAME,A.BYTES TOTAL,B.BYTES USED, C.BYTES FREE,
    (B.BYTES*100)/A.BYTES "% USED",(C.BYTES*100)/A.BYTES "% FREE"
    FROM SYS.SM$TS_AVAIL A,SYS.SM$TS_USED B,SYS.SM$TS_FREE C
    WHERE A.TABLESPACE_NAME=B.TABLESPACE_NAME AND A.TABLESPACE_NAME=C.TABLESPACE_NAME;

  
  
2、查看数据库库对象   
  

    
    
    select owner, object_type, status, count(*) count# from all_objects group by owner, object_type, status;

  
  
3、查看数据库的版本   

    
    
    Select version FROM Product_component_version 
    Where SUBSTR(PRODUCT,1,6)='Oracle';

  
  
4、查看数据库创建日期和归档方式   

    
    
    Select Created, Log_Mode, Log_Mode From V$Database;

  
  
5、查询数据库中索引占用表空间的大小   

    
    
    select a.segment_name,a.tablespace_name,b.table_name,a.bytes/1024/1024 mbytes,a.blocks
    from user_segments a, user_indexes b
    where a.segment_name = b.index_name
    and a.segment_type = 'INDEX' --索引
    and a.tablespace_name='APPINDEX' --表空间
    and b.table_name like '%PREP%' --索引所在表
    order by table_name,a.bytes/1024/1024 desc

分享到： [![](/images/sina.jpg)](javascript:; "分享到新浪微博") [![](/images/tec.jpg)](javascript:; "分享到腾讯微博")

  * 2011-07-01 17:27
  * 浏览 20921
  * 评论(0)
  * 分类:[数据库](https://www.iteye.com/blogs/category/database)
  * [查看更多](https://www.iteye.com/wiki/blog/1112724)



Global site tag (gtag.js) - Google Analytics 
