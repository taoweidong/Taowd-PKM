---
source: "http://czmmiao.iteye.com/blog/2041703"
title: "ORACLE expdp/impdp详解(原创) - CzmMiao的博客生活 - ITeye博客"
fetched_at: "2026-10-05 15:28:02"
---

[首页](https://www.iteye.com/) [资讯](https://www.iteye.com/news) [精华](https://www.iteye.com/magazines) [论坛](https://www.iteye.com/forums) [问答](https://www.iteye.com/ask) [博客](https://www.iteye.com/blogs) [专栏](https://www.iteye.com/blogs/subjects) [群组](https://www.iteye.com/groups) [下载](https://www.iteye.com/resources)

* __搜索

[您还未登录!](/login "登录") [登录](/login)

`

[![czmmiao的博客](https://www.iteye.com/upload/logo/user/570797/c6897931-33fe-394d-9192-3fd18bad1dfd.jpg?1717537095)](https://www.iteye.com/blog/user/czmmiao)

czmmiao

  * 浏览: 4635665 次
  * 性别: ![Icon_minigender_1](https://www.iteye.com/images/icon_minigender_1.gif?1652290086)
  * 来自: 厦门
  * ![](/images/status/offline.gif)

##### 最近访客  [更多访客>>](/blog/user_visits)

[![morelily的博客](https://www.iteye.com/upload/logo/user/694981/41bde6ef-6d99-3162-9c46-a5113f02596d-thumb.jpg?1717536556)](https://www.iteye.com/blog/user/morelily)

[morelily](https://www.iteye.com/blog/user/morelily "morelily")

[![amwfngt的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/amwfngt)

[amwfngt](https://www.iteye.com/blog/user/amwfngt "amwfngt")

[![zzbing的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/201406305012)

[zzbing](https://www.iteye.com/blog/user/201406305012 "zzbing")

[![sky3063的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/sky3063)

[sky3063](https://www.iteye.com/blog/user/sky3063 "sky3063")

##### 博主相关

* [博客](https://www.iteye.com/blog/user/czmmiao)
* [微博](/weibo)
* [相册](/album)
* [收藏](/link)
* [留言](/blog/guest_book)
* [关于我](/blog/profile)

##### 文章分类

  * [全部博客 (634)](/blog/user/czmmiao)
  * [Oracle日常管理 (142)](/category/192591)
  * [Oracle体系架构 (45)](/category/143940)
  * [Oracle Tuning (52)](/category/212693)
  * [Oracle故障诊断 (35)](/category/143942)
  * [RAC/DG/OGG (64)](/category/198476)
  * [Oracle11g New Features (48)](/category/293960)
  * [DataWarehouse (15)](/category/263856)
  * [SQL, PL/SQL (14)](/category/267464)
  * [DB2日常管理 (9)](/category/198031)
  * [Weblogic (11)](/category/235855)
  * [Shell (19)](/category/143943)
  * [AIX (12)](/category/168842)
  * [Linux/Unix高可用性 (11)](/category/178145)
  * [Linux/Unix日常管理 (66)](/category/143957)
  * [Linux桌面应用 (37)](/category/143941)
  * [Windows (2)](/category/295220)
  * [生活和工作 (13)](/category/143945)
  * [私人记事 (0)](/category/143944)
  * [Python (9)](/category/360614)
  * [CBO (15)](/category/317053)
  * [Cognos (2)](/category/330673)
  * [ORACLE 12c New Feature (2)](/category/333121)
  * [PL/SQL (2)](/category/333767)
  * [SQL (1)](/category/346096)
  * [C++ (2)](/category/363941)
  * [Hadoop大数据 (5)](/category/382138)
  * [机器学习 (3)](/category/362745)
  * [非技术 (1)](/category/371151)

##### 社区版块

  * [我的资讯](/blog/news) ( 0)
  * [我的论坛](/blog/post) ( 2)
  * [我的问答](/blog/answered_problems) ( 56)

##### 存档分类

  * [2020-03](/blog/monthblog/2020-03) ( 2)
  * [2020-02](/blog/monthblog/2020-02) ( 3)
  * [2019-11](/blog/monthblog/2019-11) ( 1)
  * [更多存档...](/blog/monthblog_more)

##### 最新评论

  * [di1984HIT](https://www.iteye.com/blog/user/di1984hit "di1984HIT")： xuexilee!!!
[Oracle 11g R2 RAC高可用连接特性 – SCAN详解](/blog/2124373#bc2402601)
  * [aneyes123](https://www.iteye.com/blog/user/aneyes123 "aneyes123")： 谢谢非常有用那
[PL/SQL的存储过程和函数(原创)](/blog/1815000#bc2398548)
  * [jcjcjc](https://www.iteye.com/blog/user/jcjcjc "jcjcjc")： 写的很详细
[Oracle中Hint深入理解(原创)](/blog/1478465#bc2396475)
  * [di1984HIT](https://www.iteye.com/blog/user/di1984hit "di1984HIT")： 学习了，学习了
[Linux NTP配置详解 (Network Time Protocol)](/blog/2124535#bc2392004)
  * [avalonzst](https://www.iteye.com/blog/user/avalonzst "avalonzst")： 大写的赞..
[AIX内存概述(原创)](/blog/1152476#bc2390515)

[czmmiao](https://www.iteye.com/blog/user/czmmiao)

###  ORACLE expdp/impdp详解(原创) __

**博客分类：**
  * [Oracle日常管理](/category/192591)

阅读更多

ORCALE10G提供了新的导入导出工具，数据泵。
Oracle官方对此的形容是：Oracle DataPump technology enables Very High-Speed movement of data and metadata from one database to another.其中Very High-Speed是亮点。
先说数据泵提供的主要特性（包括，但不限于）：
1\. 支持并行处理导入、导出任务
2\. 支持暂停和重启动导入、导出任务
3\. 支持通过Database Link的方式导出或导入远端数据库中的对象
4\. 支持在导入时通过Remap_schema、Remap_datafile、Remap_tablespace几个参数实现导入过程中自动修改对象属主、 数据文件或数据所在表空间。
5\. 导入/导出时提供了非常细粒度的对象控制。通过Include、Exclude两个参数，甚至可以详细制定是否包含或不包含某个对象。
Warning:
1\. 什么是Directory对象
Directory对象是Oracle10g版本提供的一个新功能。他是一个 指向，指向了操作系统中的一个路径。每个Directory都包含 Read,Write两个权限，可以通过Grant命令授权给指定的用户或角色。拥有读写权限的用户就可以读写该Directory对象指定的操作系统路 径下的文件。
2\. 除了使用network_link参数意外，expdp生成的文件都是在服务器上(Directory指定的位置)
**如何调用**
1\. 命令行方式
最简单的调用，但是写的参数有限，建议使用参数文件的方式。
2\. 参数文件方式
最常用的方式。通常需要先编写一个参数文件。指定导出时需要的各种参数。然后以如下方式调用。
expdp user/pwd parfile=xxx.par
这个xxx.par即是我们编辑的参数文件。注意，在这个命令行后面，同样可以再跟别的参数， 甚至是在par参数文件中指定过的参数。如果执行命令中附加 的参数与参数文件中的参数有重复，最终采用哪个参数，会以参数最后出现的位置而定。如：expdp user/pwd parfile=xxx.par logfile=a.log，如果在参数文件中也指定了logfile，这里会以命令行中的logfile为准；如：expdp user/pwd logfile=a.log parfile=xxx.par，而这个，则会以参数文件中的为准，因为parfile=xxx.par写在命令行的后面。
3\. 交互方式
Data Pump导入导出任务支持停止，重启等状态操作。如用户执行导入或者导出任务，执行了一半时，使用Crtl+C中断了任务（或其他原因导致的中断），此时 任务并不是被取消，而是被转移到后台。可以再次使用expdp/impdp命令，附加attach参数的方式重新连接到中断的任务中，并选择后续的操作。 这就是交互方式。
Warning : 什么是attach参数，每执行一个导入，或者导出，在命令的第一行，会有以下信息：Starting “BAM”.”SYS_EXPORT_SCHEMA_01″: bam/******** parfile=expdp_tbs.par，这个SYS_EXPORT_SCHEMA_01就是我们的attach参数。
-bash-3.00$ expdp bam/bam parfile=expdp_tbs.par
Export: Release 10.2.0.4.0 – 64bit Production on Friday, 13 August, 2010 16:35:18
Copyright (c) 2003, 2007, Oracle. All rights reserved.
Connected to: Oracle Database 10g Enterprise Edition Release 10.2.0.4.0 – 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
Starting “BAM”.”SYS_EXPORT_SCHEMA_01″: bam/******** parfile=expdp_tbs.par
如果想使用交互方式，可以使用如：expdp attach SYS_EXPORT_SCHEMA_01 进入到交互模式
**操作模式**
1\. 全库模式
导入或者导出整个数据库，对应impdp/expdp命令中的full参数，只有拥有dba或者 exp_full_database和imp_full_database权限的用户才能执行。
2\. Schema模式
导出或导入Schema下的自有对象，对应impdp/expdp命令中的Schema参数，这是默认的操作模式。 如果拥有dba或者 exp_full_database和imp_full_database权限的用户执行的话，就可以导出或导入多个Schema中的对象。
3\. 表模式
导出指定的表或者表分区（如果有分区的话）以及依赖该表的对象（如该表的索引，约束等，不过前提是这些对象在同一个 Schema中，或者执行的用户有相应的权限）。对应impdp/expdp命令中的Table参数。
4\. 表空间模式
导出指定的表空间中的内容。对应impdp/expdp中的Tablespaces参数，这种模式类似于表模式和 Schema模式的补充。
5\. 传输表空间模式
对应impdp/expdp中的Transport_tablespaces参数。这种模式与前面几种模式最显著的区 别是生成的Dump文件中并不包含具 体的逻辑数据，而只导出相关对象的元数据(即对象的定义，可以理解成表的创建语句)，逻辑数据仍然在表空间的数据文件中，导出时需要将元数据和数据文件同 时复制到目标端服务器。
这种导出方式效率很高，时间开销主要是花在复制数据文件产生的I/O上。expdp执行传输表空间模式的导出，用户必须 拥有 exp_full_database角色或者DBA角色。而通过传输表空间模式导入时，用户必须拥有imp_full_database角色或者DBA角 色。
**过滤数据**
过滤数据主要依赖于Query和Sample两个参数。其中Sample参数主要针对expdp导出功能。
1\. Query
与exp命令中的Query功能类似，不过Expdp中，该参数功能得到了增强，控制的粒度更细。Expdp中的Query也是指定类 似where语句来限定记录。语法如下：
Query = [Schema.][Table_name:] Query_clause
默认 情况如果不指定Schema.table_name,则Query_clause针对所有导出的表有效，或者你可以为每一个表指定不同的 Query_clause，如：导出a表中所有id<5的记录，导出b表中所有name=’a’的记录，则Query的参数应该如下：
Query=A:”Where id<5″,B:”Where name=’a’”
如果Where条件前没有指定Schema名或者表名的话，默认就是针对当前所有要被 导出的表。如：Query=Where id <5
Warning: 建议把Query参数放入到参数文件中使用，以避免转义符带来的麻烦。
2\. Sample
该参数用来指定导出数据的百分比，可指定的值的范围从0.000001到99.999999，语法如下：
Sample=[[Schema_name.]Table_name:]sample_percent
指 定该参数以后，EXPDP导出将自动控制导出的记录量，如导出A表中50%的记录，设置的Sample参数如下：
Sample=A:50
Warning: Sample_percent指定的值只是一个参考值，EXPDP会根据数据量算出一个近似值。
**过滤对象**
过滤对象主要依赖于Include和Exclude两个参数。这两个参数作用正好相反，在这两个参数中，可以指定你知道的任何对象 类型（如：Package、Procedure、Table等等）或者对象名称（支持通配符）
1\. Exclude 反规则
指定不被包含的对象类型或者对象名称。指定了该参数以后，指定的对象类型对应的所有对象都不会被导入或导出。 如果被排除的对象有依赖的对象，那么其依赖的 对象也不会被导入或导出。如：通过Exclude参数指定不导出表对象的话，不仅指定的表不会被导出，连这些表关联的Index、Check等都不会被导出。Warning: 建议把Exclude参数放入到参数文件中使用，以避免转义符带来的麻烦。
2\. Include 正规则
与Exclude正好相反。指定包含的对象类型或者对象名称。
Warning: 由于两个参数功能正好相反，因此在执行导入或导出命令时，两个参数不能同时使用，否则Oracle也不知道你想要干什么啦。

**exclude/include参数用法：**
EXCLUDE=[object_type]:[name_clause],[object_type]:[name_clause] -->排出特定对象
INCLUDE=[object_type]:[name_clause],[object_type]:[name_clause] -->包含特定对象
object_type子句用于指定对象的类型，如table,sequence,view,procedure,package等等
name_clause子句可以为SQL表达式用于过滤特定的对象名字。它由SQL操作符以及对象名(可使用通配符)来过滤指定对象类型中的特定对象。
当未指定name_clause而仅仅指定object_type则所有该类型的对象都将被过滤或筛选。多个[object_type]:[name_clause]中间以逗号分割。
示例：
expdp <other_parameters> SCHEMAS=scott EXCLUDE=SEQUENCE,TABLE:"IN ('EMP','DEPT')"
impdp <other_parameters> SCHEMAS=scott INCLUDE=PACKAGE,FUNCTION,PROCEDURE,TABLE:"='EMP'"
常用的过滤SQL表达式
EXCLUDE=SEQUENCE,VIEW  \--过滤所有的SEQUENCE,VIEW
EXCLUDE=TABLE:"IN ('EMP','DEPT')"  \--过滤表对象EMP,DEPT
EXCLUDE=SEQUENCE,VIEW,TABLE:"IN ('EMP','DEPT')" \--过滤所有的SEQUENCE,VIEW以及表对象EMP,DEPT
EXCLUDE=INDEX:"= 'INDX_NAME'"  \--过滤指定的索引对象INDX_NAME
INCLUDE=PROCEDURE:"LIKE 'PROC_U%'"  \--包含以PROC_U开头的所有存储过程(_ 符号代表任意单个字符)
INCLUDE=TABLE:"> 'E' "  \--包含大于字符E的所有表对象
其它常用操作符 NOT IN, NOT LIKE, <, != 等等
直接将过滤操作符封装到参数文件中，如下面的例子
Parameter file:exp_scott.par
DIRECTORY = dump_scott
DUMPFILE = exp_scott_%U.dmp
LOGFILE = exp_scott.log
SCHEMAS = scott
PARALLEL= 2
EXCLUDE = TABLE:"IN ('EMP', 'DEPT')"
expdp system/manager parfile=exp.par
命令行下转义符的处理
Windows平台:
D:\> expdp system/manager DIRECTORY=my_dir DUMPFILE=exp_tab.dmp LOGFILE=exp_tab.log SCHEMAS=scott
INCLUDE=TABLE:\"IN ('EMP', 'DEPT')\"
在Windows平台下，需要对象双引号进行转义，使用转义符\
Unix平台:
在未使用parfile文件的情形下，所有的符号都需要进行转义，包括括号，双引号，单引号等
% expdp system/manager DIRECTORY=my_dir DUMPFILE=exp_tab.dmp LOGFILE=exp_tab.log SCHEMAS=scott
INCLUDE=TABLE:\"IN \\(\'EMP\', \'DEP\'\\)\"
exclude/include常见的错误
任意需要转义的字符如果未转义或转义错误，都会产生ORA错误。下面给出几种常见的ORA错误。
ORA-39001: invalid argument value
ORA-39071: Value for INCLUDE is badly formed.
ORA-00936: missing expression
ORA-39001: invalid argument value
ORA-39071: Value for EXCLUDE is badly formed.
ORA-00904: “DEPT”: invalid identifier
ORA-39001: invalid argument value
ORA-39041: Filter “INCLUDE” either identifies all object types or no object types.
ORA-39001: invalid argument value
ORA-39041: Filter “EXCLUDE” either identifies all object types or no object types
ORA-39001: invalid argument value
ORA-39038: Object path “USER” is not supported for TABLE jobs.
**高级过滤**
在导出/导入的时候，我们常常有这样的需求，只想导出/导入表结构，或者只想导出/导入数据。幸运的是数据泵也提供了该功能。使用 Content参数。该参数有三个属性
1) ALL : 导出/导入对象定义和数据，该参数的默认值就是ALL
2) DATA_ONLY : 只导出/导入数据。
3) METADATA_ONLY : 只导出/导入对象定义。
Warning: 有一点值得注意的时，在执行导出的时候，如果使用了高级过滤，如只导出了数据，那么导入时，需要确保数据定义已经存在。否则数据都变成没有主子了。如果数 据定义已经存在，导入时最好指定data_only，否则会触发ORA-39151错误，因为对象已经存在了。
过滤已经存在的数据
我们知道，导入的表对象在目标库中已经存在，并且目标端没有创建数据完整性约束条件(RI)来检验数据的话，就有可能造 成数据被重复导入。数据泵提供了一 个新的参数Table_exists_action,可以一定程度上降低重复数据的产生。该参数用来控制如果要导入的表对象存在，执行什么操作。有以下几 个参数值：
1) SKIP : 跳过该表，继续处理下一个对象。该参数默认就是SKIP。值得注意的是，如果你同时指定了CONTENT参数为Data_only的话，SKIP参数无 效，默认为APPEND。
2) APPEND : 向现有的表中添加数据。
3) TRUNCATE : TRUNCATE当前表，然后再添加记录。使用这个参数需要谨慎，除非确认当前表中的数据确实无用。否则可能造成数据丢失。
4) REPLACE : 删除并重建表对象，然后再向其中添加数据。值得注意的是，如果同时指定了CONTENT参数为Data_only的话，REPLACE参数无效。
**重定义表的Schema或表空间**
我们还可能会遇到这样的需求，把A用户的对象转移到B用户，或者更换数据的表空间。数据泵通过 Remap_Schema和Remap_tablespace参数实现了该功能。
1) REMAP_SCHEMA : 重定义对象所属Schema
该参数的作用类似IMP中的Fromuser+Touser,支持多个Schema的转换，语法如下：
REMAP_SCHEMA=Source_schema:Target_schema[,Source_schema:Target_schema]
如 把A的对象转换到C用户，将C转换到D用户。Remap_schema=a:b,c:d
Warning: 不能在同一个IMPDP命令中指定remap_schema=a:b,a:c.
2) REMAP_TABLESPACE : 重定义对象所在的表空间。
该参数用来重映射导入对象存储的表空间，支持同时对多个表空间进行 转换，相互间用逗号分割。语法如下：
REMAP_TABLESPACE=Source_tablespace:Target_tablespace[,Source_tablespace:Target_tablespace]
Warning: 如果使用Remap_tablespace参数，则要保证导入的用户对目标表空间有读写权限。
**优化导入/导出效率**
对于大数据量来说，我们不得不考虑效率问题。数据泵对效率也提出了更高的要求。甚至官方的描述就是Oracle Data Pump technology enables Very High-Speed movement of data and metadata from one database to another.这里的Very High-Speed依赖我们的parallel参数。
所 有的优化操作都会有三种结果：变得更好、没有变化、变得更差。Parallel参数也是这样，并不是指定一个大于1的参数，性能就会有提升。
1) 对于导出的parallel
对于导出来说，由于dump文件只能由一个线程进行操作（包 括I/O处理），因此如果输出的DUMP文件只有一个，即使你指定再多的并行，实际工作仍然是 一个，而且还会触发ORA-39095错误。因此，建议设置该参数小于或等于生成的DUMP文件数量。那么，如何控制生成的DUMP文件数量呢？
EXPDP 命令提供了一个FILESIZE参数，用来指定单个DUMP文件的最大容量，要有效的利用parallel参数，filesize参数必不可少。
举 例：某用户对象占用了4G左右的空间，实际导出后的DUMP文件约为3G，我们尝试在导出该用户时指定并行度为4，设置单个文件不超过500M，则语法如 下：
$ expdp user/pwd directory=dump_file dumpfile=expdp_20100820_%U.dmp logfile=expdp_20100820.log filesize=500M parallel=4
2) 对于导入的parallel
对于导入来说，使用parallel参数则要简单的多，我认为导入更能体现parallel参数的优势。 参数设置为几，则认为同时将几张表的内容导入到库中。
举例：某dmp文件中包含了200张表，我们尝试在导入该DMP文件时指定并行度为10，则 语法如下：
$ impdp user/pwd directory=dump_file dumpfile=expdp_20100820.dmp logfile=impdp_20100820.log parallel=10

**如何进入交互模式**
在这里，我正在执行导入，我想进入交互模式，查看导入的状态。进入交互模式有两种方式，操作步骤如下：
i 使用Ctrl+C退出当前模式
ii 在命令行模式下，执行Expdp/Impdp命令，同时指定attach参数连接到当前正在制定的导入/导出任务。如：
expdp bam/bam attach=SYS_IMPORT_FULL_01
Warning:如果没有指定Attach参数，则默认进入当前正在运行的 任务。不过如果当前没有正在指定的任务，而且也没有给Attach赋值，那么就会报Ora-31626错误。
当命令行进入交互模式后，会显示如下 界面：
Export>
7) 交互模式的操作
在交互模式中，支持下面几种操作。
i 查看JOB的运行状态
Export> status
ii 回退到命令行
Export> continue_client
iii 增加并行
Export> parallel=4
Warning: 在使用导出时，不能直接指定parallel参数，否则可能会遇到ORA-39095错误，因为如果要并行导出，则必须指定多个导出文件，这里的并行导出 是指，多个线程同时工作，同时从数据库中导出多个dmp文件来。
在Oracle Database Utilities中有如下解释：
Because each active worker process or I/O server process writes exclusively to one file at a time, an insufficient number of files can have adverse effects. Some of the worker processes will be idle while waiting for files, thereby degrading the overall performance of the job. More importantly, if any member of a cooperating group of parallel I/O server processes cannot obtain a file for output, then the export operation will be stopped with an ORA-39095 error. Both situations can be corrected by attaching to the job using the Data Pump Export utility, adding more files using the ADD_FILE command while in interactive mode, and in the case of a stopped job, restarting the job.
You can supply multiple file_name specifications as a comma-delimited list or in separate DUMPFILE parameter specifications. If no extension is given for the filename, then Export uses the default file extension of .dmp. The filenames can contain a substitution variable (%U), which implies that multiple files may be generated. The substitution variable is expanded in the resulting filenames into a 2-digit, fixed-width, incrementing integer starting at 01 and ending at 99. If a file specification contains two substitution variables, both are incremented at the same time. For example, exp%Uaa%U.dmp would resolve to exp01aa01.dmp, exp02aa02.dmp, and so forth.
iv 停止JOB
Export> stop_job
v 启动JOB
Export> start_job
vi 杀掉JOB
Export> kill_job
vii 退出交互模式
Export> exit_client
viii 指定文件大小
Export> filesize=1G
ix 帮助
Export> Help

JOB_NAME
指定要导出作用的名称,默认为SYS_XXX
JOB_NAME=jobname_string
SELECT * FROM DBA_DATAPUMP_JOBS;--查看存在的job
**NETWORK_LINK导出文件到本地**
远程：
IP:192.168.10.55,OS:RHEL4.8 64bit,Oracle:10.2.0.5 64bit
被导出用户:monitor
本地：
ip: 172.*，WINDOWS XP,oracle 10.2.0.4。
本地tns :cheniwo
本地配置的联系到远程的tns:lobom55
1)确定本地可访问远程
F:\oracle\product\10.2.0\db_2\network\admin\sqlnet.ora
已使用 TNSNAMES 适配器来解析别名
Attempting to contact (DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP
(HOST = 192.168.10.55)(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME = lobomb)))
OK (40 毫秒)
2）在本地建立dblink到远程
F:\Documents and Settings\Administrator>sqlplus / as sysdba
SQL*Plus: Release 10.2.0.4.0 - Production on 星期四 9月 6 14:25:44 2012
Copyright (c) 1982, 2007, Oracle. All Rights Reserved.
连接到:
Oracle Database 10g Enterprise Edition Release 10.2.0.4.0 - Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
SQL> create database link dl_monitor connect to monitor identified by monitor using 'lobom55';
数据库链接已创建。
SQL> select sysdate from dual@dl_monitor;
SYSDATE
\--------------
06-9月 -12
3）数据泵导出
F:\Documents and Settings\Administrator>expdp network_link=dl_monitor dumpfile=n
etwork_monitor.dmp
/*--------------------------------------------------
说明：network_link是你建立的到远程的database link
下边输入的用户名是你本地数据库的认证
dumpfile 将放在data_pump_dir目录定义的本地目录下
\-------------------------------*/
Export: Release 10.2.0.4.0 - Production on 星期四, 06 9月, 2012 14:40:17
Copyright (c) 2003, 2007, Oracle. All rights reserved.
用户名: / as sysdba
连接到: Oracle Database 10g Enterprise Edition Release 10.2.0.4.0 - Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
启动 "SYS"."SYS_EXPORT_SCHEMA_01": /******** AS SYSDBA network_link=dl_monitor
dumpfile=network_monitor.dmp
正在使用 BLOCKS 方法进行估计...
处理对象类型 SCHEMA_EXPORT/TABLE/TABLE_DATA
使用 BLOCKS 方法的总估计: 81.68 MB
处理对象类型 SCHEMA_EXPORT/USER
.............................省略若干行.............................
处理对象类型 SCHEMA_EXPORT/TABLE/INDEX/STATISTICS/FUNCTIONAL_AND_BITMAP/INDEX_ST
ATISTICS
已成功加载/卸载了主表 "SYS"."SYS_EXPORT_SCHEMA_01"
******************************************************************************
SYS.SYS_EXPORT_SCHEMA_01 的转储文件集为:
F:\ORACLE\PRODUCT\10.2.0\ADMIN\CHENIWO\DPDUMP\NETWORK_MONITOR.DMP
作业 "SYS"."SYS_EXPORT_SCHEMA_01" 已于 14:51:41 成功完成
4）检查结果：
SQL> set head off
SQL> select * from dba_directories where directory_name='DATA_PUMP_DIR';
SYS DATA_PUMP_DIR F:\oracle\product\10.2.0\admin\cheniwo\dpdump\
F:\Documents and Settings\Administrator>cd F:\oracle\product\10.2.0\admin\cheniwo\dpdump
F:\oracle\product\10.2.0\admin\cheniwo\dpdump>dir /w
驱动器 F 中的卷是 新加卷
卷的序列号是 88F0-A421
F:\oracle\product\10.2.0\admin\cheniwo\dpdump 的目录
[.] [..] cheniwo.sql
CHENIWO_DP.DMP dp.log EXPDAT.DMP
export.log FULL_CHENIWO.DMP import.log
NETWORK_MONITOR.DMP TABLES_CHENIWO.DMP TABLES_CHENIWO2.DMP
TS_CHENIWO.DMP USER_CHENIWO.DMP
12 个文件 128,977,860 字节
2 个目录 155,032,698,880 可用字节

参考至:http://loveboth.iteye.com/blog/1745801

http://bbs.chinaunix.net/thread-3643706-1-1.html

http://www.cnblogs.com/iImax/p/oracle-11g-expdp-interactive.html
http://blog.csdn.net/liqfyiyi/article/details/7248911

本文原创，转载请注明作者、出处

如有错误，欢迎指正

邮箱:czmcj@163.com

**2**
顶

**0**
踩

分享到： [![](/images/sina.jpg)](javascript:; "分享到新浪微博") [![](/images/tec.jpg)](javascript:; "分享到腾讯微博")

  * 2014-04-07 10:17
  * 浏览 64825
  * 评论(0)
  * 分类:[数据库](https://www.iteye.com/blogs/category/database)
  * [查看更多](https://www.iteye.com/wiki/blog/2041703)

Global site tag (gtag.js) - Google Analytics
