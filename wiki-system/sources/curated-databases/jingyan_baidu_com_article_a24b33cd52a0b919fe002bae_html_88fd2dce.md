---
source: "http://jingyan.baidu.com/article/a24b33cd52a0b919fe002bae.html"
title: "sql server2008安装时提示重启计算机失败怎么办-百度经验"
fetched_at: "2026-10-05 15:29:12"
---

# sql server2008安装时提示重启计算机失败怎么办

  * 原创
  * |
  * 浏览：83590
  * |
  * 更新：2014-04-26 11:15

  * [](/album/a24b33cd52a0b919fe002bae.html?picindex=1)1

  * [](/album/a24b33cd52a0b919fe002bae.html?picindex=2)2

  * [](/album/a24b33cd52a0b919fe002bae.html?picindex=3)3

  * [](/album/a24b33cd52a0b919fe002bae.html?picindex=4)4

  * [](/album/a24b33cd52a0b919fe002bae.html?picindex=5)5

[分步阅读](/album/a24b33cd52a0b919fe002bae.html)

安装SQL Server 2008时，经常会遇到这样一个问题，软件提示“重启计算机失败”，如果忽略的话，会给后面的安装带来很大的麻烦，这里如何解决呢？

## [](javascript:;)工具/原料

  *   注册表

## [](javascript:;)解决方法

  1. 1

在键盘上按下组合键【Win】+【R】，调出运行窗口。

  2. 2

在窗口中输入“regedit”，点击确定，打开注册表管理界面。

  3. 3

在注册表左侧目录栏中找到如下位置：“HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager”

然后在右侧选择删除“PendingFileRenameOperations”项即可。

  4. 4

回到SQL安装界面，点击【重新运行】即可。

END

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
