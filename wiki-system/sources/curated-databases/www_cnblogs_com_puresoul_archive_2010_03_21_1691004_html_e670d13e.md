---
source: "http://www.cnblogs.com/puresoul/archive/2010/03/21/1691004.html"
title: "Sql Server中判断表或者数据库是否存在 - 贺满 - 博客园"
fetched_at: "2026-10-05 15:29:10"
---

**SQL Server中判断数据库是否存在：**
法(一):

select * From master.dbo.sysdatabases where name='数据库名'

法(二):
if db_id('数据库名') is not null

drop database 。。。
go

create 。。。

**SQL Server中判断表对象是否存在：**
select count(*) from sysobjects where id = object_id('数据库名.Owner.表名')

if exists

(select count(*) from sysobjects where id = object_id('数据库名.Owner.表名'))
print '存在'
else
print '不存在'

**SQL Server中判断表中字段是否存在：**
if exists

(select * from syscolumns where name='colname1' and id=object_id('数据库名.Owner.表名'))
print '存在'
else
print '不存在'
(代表表tablename1中存在colname1字段 )
例：
select * from syscolumns where name='Test' and id=object_id('dbo.test')

**SQL Server中判断存储过程或视图是否存在：**

if object_id('视图或存储过程名') is not null
drop proc/view 。。。
go

create proc/view 。。。

或

if Exists(select * from sysobjects where name='视图或存储过程名' AND type = 'P/V')
drop proc/view 。。。
go

create proc/view 。。。
