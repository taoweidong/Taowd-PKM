---
source: "http://www.cnblogs.com/chinhr/archive/2011/11/14/2248221.html"
title: "Oracle中快速删除某个用户下的所有表数据 - 莫问奴归处 - 博客园"
fetched_at: "2026-10-05 15:27:51"
---

一、禁止所有的外键约束  


  


在pl/sql developer下执行如下语句：  
SELECT 'ALTER TABLE ' || table_name || ' disable CONSTRAINT ' || constraint_name || ';' FROM user_constraints where CONSTRAINT_TYPE = 'R';  
把查询出来的结果拷出来在pl/sql developer时执行。  
若没有pl/sql developer，可以在sqlplus里操作，方法如下:  
1\. 打开sqlplus，并用相应的用户连接。  
2\. 把pagesize设大点，如set pagesize 20000  
3\. 用spool把相应的结果导到文件时，如  
SQL> spool /home/oracle/constraint.sql  
SQL> SELECT 'ALTER TABLE ' || table_name || ' disable CONSTRAINT ' || constraint_name || ';' FROM user_constraints where CONSTRAINT_TYPE = 'R';  
SQL> spool off  
4\. 已经生成了包含相应语句的脚本，不过脚本文件里的最前和最后面有多余的语句，用文本编辑器打开，并删除没用的语句即可  
5\. 重新用相应的用户登录sqlplus，执行如下命令  
SQL> @/home/oracle/constraint.sql  


  


二、用delete或truncate删除所有表的内容  


  


SELECT 'DELETE FROM '|| table_name || ';' FROM USER_TABLES  
ORDER BY TABLE_NAME;  
或  
SELECT 'TRUNCATE TABLE '|| table_name || ';' FROM USER_TABLES  
ORDER BY TABLE_NAME;  
用第一步类似的方法操作。要注意的一点是，若表的数据有触发器相关联，只能用truncate语句，不过truncate语句不能回滚，所以时要注意  


  


三、把已经禁止的外键打开  


  


SELECT 'ALTER TABLE ' || table_name || ' enable CONSTRAINT ' || constraint_name || ';' FROM user_constraints where CONSTRAINT_TYPE = 'R';  


[http://ouds.biz/blog/2011/05/10/oracle-clean-data-user/](http://ouds.biz/blog/2011/05/10/oracle-clean-data-user/)
