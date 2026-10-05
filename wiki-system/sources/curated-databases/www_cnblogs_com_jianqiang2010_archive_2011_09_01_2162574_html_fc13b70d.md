---
source: "http://www.cnblogs.com/jianqiang2010/archive/2011/09/01/2162574.html"
title: "ORA-28000: the account is locked-的解决办法 - 世道 - 博客园"
fetched_at: "2026-10-05 15:29:43"
---

ORA-28000: the account is locked  
第一步：使用PL/SQL，登录名为system,数据库名称不变，选择类型的时候把Normal修改为Sysdba;  
第二步：选择myjob,查看users;  
第三步：选择system,右击点击“编辑”；  
第四步：修改密码，把“帐户被锁住”的勾去掉；  
第五步：点击“应用”再点击“关闭”；  
第六步：重新登录就可以通过验证了；  
第二种  
ALTER USER username ACCOUNT UNLOCK;

  
第三种

  
在plsql developer中要是以scott/tiger登录时提示ora-28000 the account is locked。

解决办法：

新装完Oracle10g后，用scott/tiger测试，会出现以下错误提示：  
oracle10g the account is locked  
oracle10g the password has expired  
原因：默认Oracle10g的scott不能登陆。  
解决：  
（1）conn sys/sys as sysdba; //以DBA的身份登录  
（2）alter user scott account unlock;// 然后解锁  
（3）conn scott/tiger //弹出一个修改密码的对话框，修改一下密码就可以了

在运行里面输入cmd在DOS模式下输入sqlplus，以system用户名登录，密码是刚装oracle时自己填写的密码orcl，登录进去以后。

SQL> conn sys/sys as sysdba; （分号是必须的但是我是以system登录的所在这不应该写conn sys/sys as sysdba应该写conn system/orcl as sysdba;）  
Connected.  
SQL> alter user scott account unlock;  
User altered.  
SQL> commit;  
Commit complete.  
SQL> conn scott/tiger//请输入新密码，并确认后OK  
Password changed  
Connected.

这时再到plsql developer里面以scott/tiger登录就可以了。。。。。

偶在数据库的问题处理过程中遇到了ORA-28000:the account is locked的错误，现将详细的处理情况介绍如下供大家参考：

1\. 查询failed_login_attempts参数默认值：  
Oracle**10g**(备注：9i环境中此参数的值为unlimited)

SQL>conn /as sysdba

Connected.

SQL> desc dba_profiles;  
名称 是否为空? 类型  
\----------------------------------------- -------- --------------

PROFILE NOT NULL VARCHAR2(30)  
RESOURCE_NAME NOT NULL VARCHAR2(32)  
RESOURCE_TYPE VARCHAR2(8)  
LIMIT VARCHAR2(40)

SQL> select resource_name,limit from dba_profiles where resource_name='FAILED_LOGIN_ATTEMPTS';

RESOURCE_NAME LIMIT  
\-------------------------------- ----------------------------------------  
FAILED_LOGIN_ATTEMPTS 10   
****

2\. 模拟账户被锁现象  
(为方便模拟lock现象，修改default profile failed_login_attempts=3 )  
a.修改参数failed_login_attempts=3

SQL> conn /as sysdba  
已连接。  
SQL> alter profile default limit failed_login_attempts 3;

配置文件已更改

SQL> select resource_name,limit from dba_profiles where resource_name='FAILED_LOGIN_ATTEMPTS';

RESOURCE_NAME LIMIT  
\-------------------------------- ----------------------------------------  
FAILED_LOGIN_ATTEMPTS 3   


b.重现错误登陆   
正确登陆

SQL> conn jd/jd  
已连接。

第一次登录失败  
SQL> conn jd/jh  
ERROR:  
ORA-01017: invalid username/password; logon denied

警告: 您不再连接到 ORACLE。

第二次登陆失败  
SQL> conn jd/ju  
ERROR:  
ORA-01017: invalid username/password; logon denied

第三次登录失败

SQL> conn jd/jl  
ERROR:  
ORA-01017: invalid username/password; logon denied

连续三次登录失败后，账户被锁定

SQL> conn jd/jy  
ERROR:  
ORA-28000: the account is locked

3\. 解锁

SQL> conn /as sysdba  
已连接。  
SQL> alter user jd account unlock;

用户已更改。  
  
4\. 解决方案  
(1) 可以考虑查询应用部署中错误的password或者数据库连接等可能导致错误password的地方，彻底的查询问题所在。  
(2) 修改参数failed_login_attempts=unlimited

SQL> alter profile default limit failed_login_attempts unlimited;

配置文件已更改

SQL> select resource_name,limit from dba_profiles where resource_name='FAILED_LO  
GIN_ATTEMPTS';

RESOURCE_NAME LIMIT  
\-------------------------------- ----------------------------------------  
FAILED_LOGIN_ATTEMPTS UNLIMITED  
  
5\. 扩展知识点及备注说明  
(1) Q: FAILED_LOGIN_ATTEMPTS=3 3的含义是什么？是累计失败次数还是连续失败次数？  
A: FAILED_LOGIN_ATTEMPTS=3的含义是从第一次登录失败开始计算，连续登陆失败的次数。而不是累计失败的次数。  
试验如下：

SQL> conn /as sysdba  
已连接。  
SQL> alter profile default limit failed_login_attempts 3;

配置文件已更改

SQL> conn jd/jd  
已连接。

第一次登录失败  
SQL> conn jd/jh  
ERROR:  
ORA-01017: invalid username/password; logon denied

警告: 您不再连接到 ORACLE。

第二次登陆失败  
SQL> conn jd/gh  
ERROR:  
ORA-01017: invalid username/password; logon denied

登录正确

SQL> conn jd/jd  
已连接。

第一次登录失败  
SQL> conn jd/df  
ERROR:  
ORA-01017: invalid username/password; logon denied

警告: 您不再连接到 ORACLE。

第二次登陆失败  
SQL> conn jd/sd  
ERROR:  
ORA-01017: invalid username/password; logon denied

第三次登录失败

SQL> conn jd/fg  
ERROR:  
ORA-01017: invalid username/password; logon denied

三次登录失败之后，用户被锁定

SQL> conn jd/hj  
ERROR:  
ORA-28000: the account is locked

(2) Q: 如何从数据库中查询当前FAILED_LOGIN_ATTEMPTS的值？dba_profiles是限额，并不代表当前值，如果查询当前失败的值怎么查？  
A: select NAME,LCOUNT from user$，user$为view dba_users的基表，通常可以查询一下试图对应的基表，oracle可能会隐藏一些参数。
