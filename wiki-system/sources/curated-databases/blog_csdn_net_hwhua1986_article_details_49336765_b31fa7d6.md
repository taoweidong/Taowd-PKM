---
source: "http://blog.csdn.net/hwhua1986/article/details/49336765"
title: "oracle导入提示“IMP-00010：不是有效的导出文件，头部验证失败”的解决方案_imp-00010: 不是有效的导出文件, 标头验证失败-CSDN博客"
fetched_at: "2026-10-05 15:27:58"
---

这是由于导出的dmp文件与导入的数据库的版本不同造成的  
用Notepad++查看了dmp文件，在头部具修改成你将导入目标数据库的版本号  
以下对应的版本号：  
11g R2：V11.02.00  
11g R1：V11.01.00

10g：V10.02.01

  


**解决步骤：**

1、查看dmp文件的版本号

![](https://img-blog.csdn.net/20151022180627452?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  


  


2、查询导入oracle数据库的版本号

通过select * from v$version查看版本号，如下图

![](https://img-blog.csdn.net/20151117135259524?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  


  


3、修改dmp文件的版本号

![](https://img-blog.csdn.net/20151117135519169?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  


  


4、重新执行导入sql即可完成导入工作。
