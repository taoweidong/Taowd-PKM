---
source: "http://www.2cto.com/database/201410/344003.html"
title: "2.使用windows下的客户端连接虚拟机上的oracle连不上的时候的解决方案 - Oracle - 红黑联盟"
fetched_at: "2026-10-05 15:27:35"
---

# 2.使用windows下的客户端连接虚拟机上的oracle连不上的时候的解决方案

﻿当虚拟机可以连通本机，但是发现远程还是不可以连通，这时候要在防火墙处添加规则，添加的方式是：

A : 以root登录

B : 在终端上输入setup，对防火墙进行配置。截图如下：

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090851111.png)

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090851114.png)

C : 查看oracle相关端口是否进行了配置。（上下键进行查看，左右键进行转发或关闭）

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090851116.png)

D 如果没有定义相关的规则，重新定义。

接着选择转发：

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090851117.png)

E 同样的对mysql的规则进行配置（配置方式如上）

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090852118.png)

F 最后一直点击确定，直至完成。记着再通过PLSQL进行远程连接的时候就可以连接了。

配置Linux下oracle 的 *.ora

/home/oracle_11/app/oracle/product/11.2.0/db_1/network/admin/listener.ora,内容如下：

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090852120.png)

G 配置windows客户端下的tnsnames.ora文件，文件目录是：

F:\app\to-to\product\11.2.0\dbhome_1\NETWORK\ADMIN\tnsnames.ora

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090852122.png)

PLSQL连接后的效果

![](http://www.2cto.com/uploadfile/Collfiles/20141016/20141016090853126.png)
