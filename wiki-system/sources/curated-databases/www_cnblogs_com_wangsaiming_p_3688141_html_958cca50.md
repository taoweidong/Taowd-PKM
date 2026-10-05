---
source: "http://www.cnblogs.com/wangsaiming/p/3688141.html"
title: "Oracle ORA-01033: ORACLE initialization or shutdown in progress 错误解决办法 - 亿典通柄棋 - 博客园"
fetched_at: "2026-10-05 15:28:02"
---

今早刚上班、客户打电话过来说系统访问不了，输入用户名、用户号不能加载出来！听到这个问题，第一时间想到的是不是服务器重新启动了，Oracle数据库的相关服务没有启动的原因、查看服务的时候，发现相关的服务都是启动的状态。第二想法就是查看的程序配置文件是否被修改过、也没有异常；第三个就是用PL/SQL连接Oracle数据库，输入登录名和密码后，提示如下错误：ora-01033:oracle initialization or shutdown in progress；

在网上搜索了一圈，终于发现几个比较有详细步骤的解决方案，参考如下：

第一种解决方法：

第一步，运行cmd

![](http://dl.iteye.com/upload/attachment/0078/3870/797255ca-a706-3098-8724-97fd7839533d.png) 第一步、sqlplus /NOLOG

第二步、SQL>connect sys/change_on_install as sysdba

提示：已成功

第三步、SQL>shutdown normal

提示：[数据库](http://www.2cto.com/database/)已经关闭 已经卸载数据库 ORACLE 例程已经关闭

第四步、SQL>startup mount

第五步、SQL>alter database open;

提示：（我在操作的时候没有遇到下边着中错误）

第1 行出现错误: ORA-01157: 无法标识/锁定数据文件19 - 请参阅DBWR 跟踪文件

ORA-01110: 数据文件19: ''''C:\oracle\oradata\oradb\FYGL.ORA''

这个提示文件部分根据每个人不同情况有点差别。

继续输入 第六步、SQL>alter database datafile 19 offline drop;

第七步、重复使用第五第六步，直到出现“数据库已更改”的提示，然后如下图，

继续输入shutdown normal，startup mount就OK啦

![](http://dl.iteye.com/upload/attachment/0078/3878/a76fd3ca-4cbe-3819-9c69-479b9acd0566.png)

内容来源：<http://www.2cto.com/database/201202/118194.html>

<http://yuxisanren.iteye.com/blog/1754018>

测试了一遍，发现还是没有解决我这个问题；

第二种方法：

把Oracle的相关服务都停止后、在重新启动、发现可以正常登录。
