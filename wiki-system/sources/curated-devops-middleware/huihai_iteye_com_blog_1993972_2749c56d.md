---
source: "http://huihai.iteye.com/blog/1993972"
title: "3、Maven学习之MyEclipse10与Maven3.0.5集成 - 悔海 - ITeye博客"
fetched_at: "2026-10-05 15:30:13"
---

[首页](https://www.iteye.com/) [资讯](https://www.iteye.com/news) [精华](https://www.iteye.com/magazines) [论坛](https://www.iteye.com/forums) [问答](https://www.iteye.com/ask) [博客](https://www.iteye.com/blogs) [专栏](https://www.iteye.com/blogs/subjects) [群组](https://www.iteye.com/groups) [下载](https://www.iteye.com/resources)

* __搜索

[您还未登录!](/login "登录") [登录](/login)

`

[![huihai的博客](https://www.iteye.com/upload/logo/user/378917/06929773-0b28-3f50-965c-3ac211f1a98c.jpg?1717537392)](https://www.iteye.com/blog/user/huihai)

huihai

  * 浏览: 548789 次
  * 性别: ![Icon_minigender_1](https://www.iteye.com/images/icon_minigender_1.gif?1652290086)
  * 来自: 北京
  * ![](/images/status/offline.gif)

##### 最近访客  [更多访客>>](/blog/user_visits)

[![ptb1982的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/ptb1982)

[ptb1982](https://www.iteye.com/blog/user/ptb1982 "ptb1982")

[![lishuangquan22的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/lishuangquan22)

[lishuangquan22](https://www.iteye.com/blog/user/lishuangquan22 "lishuangquan22")

[![womoney7的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/womoney7)

[womoney7](https://www.iteye.com/blog/user/womoney7 "womoney7")

[![sunpengshabi的博客](https://www.iteye.com/images/user-logo-thumb.gif?1652290086)](https://www.iteye.com/blog/user/sunpengshabi)

[sunpengshabi](https://www.iteye.com/blog/user/sunpengshabi "sunpengshabi")

##### 博主相关

* [博客](https://www.iteye.com/blog/user/huihai)
* [微博](/weibo)
* [相册](/album)
* [收藏](/link)
* [留言](/blog/guest_book)
* [关于我](/blog/profile)

##### 文章分类

  * [全部博客 (84)](/blog/user/huihai)
  * [Spring (19)](/category/138364)
  * [Tomcat (4)](/category/138365)
  * [hibernate (16)](/category/139262)
  * [总结 (3)](/category/139326)
  * [java基础 (24)](/category/139601)
  * [sql (9)](/category/140959)
  * [Spring MVC (2)](/category/296075)
  * [svn (6)](/category/299384)
  * [tortoisesvn (2)](/category/299490)
  * [junit (2)](/category/299647)
  * [SC (1)](/category/300587)
  * [maven (3)](/category/300845)

##### 社区版块

  * [我的资讯](/blog/news) ( 0)
  * [我的论坛](/blog/post) ( 0)
  * [我的问答](/blog/answered_problems) ( 0)

##### 存档分类

  * [2013-12](/blog/monthblog/2013-12) ( 12)
  * [2013-10](/blog/monthblog/2013-10) ( 2)
  * [2013-05](/blog/monthblog/2013-05) ( 1)
  * [更多存档...](/blog/monthblog_more)

##### 最新评论

  * [Zhouchenyu](https://www.iteye.com/blog/user/zhouchenyu "Zhouchenyu")： 谢谢
[1、junit学习之junit的基本介绍](/blog/1986568#bc2396903)
  * [wenjieyatou](https://www.iteye.com/blog/user/wenjieyatou "wenjieyatou")：
[1、junit学习之junit的基本介绍](/blog/1986568#bc2395337)
  * [huabengao](https://www.iteye.com/blog/user/huabengao "huabengao")： 不错 很好
[1、junit学习之junit的基本介绍](/blog/1986568#bc2387730)
  * [prayjourney](https://www.iteye.com/blog/user/prayjourney "prayjourney")： 写的不错，很有启发！
[1、junit学习之junit的基本介绍](/blog/1986568#bc2387392)
  * [wangzhenyu1260](https://www.iteye.com/blog/user/wangzhenyu1260 "wangzhenyu1260")： assertEqualspublic static void ...
[1、junit学习之junit的基本介绍](/blog/1986568#bc2385520)

[huihai](https://www.iteye.com/blog/user/huihai)

###  3、Maven学习之MyEclipse10与Maven3.0.5集成 __

**博客分类：**
  * [maven](/category/300845)

[Maven](http://www.iteye.com/blogs/tag/Maven)

阅读更多

在作项目开发的时候一般要用到MyEclipse或Eclipse等IDE工具，所以如果要想用Maven，那么就要想办法把两者集成到一起。在MyEclipse10中已经把Maven集成到插件管理里，但是MyEclipse默认使用的Maven可能并不是我们所想用的，这时就需要把自己想要的Maven与MyEclipse进行集成。

1、打开MyEclipse10，然后Window-->Preferences，在出现的对话框中，搜索Maven，然后出现如下信息，选择Installations，然后选择add，在出现的对话框中选择本地Maven安装的目录，就可以把MyEclipse中的Maven插件改成使用自己的Maven，如下图所示：
![](http://dl2.iteye.com/upload/attachment/0092/4256/69b51e05-5c6e-35b8-9d2a-e69d5b39dd76.png)
2、然后点击左面的User Settings，在右面User Settings里进行设置，选择Browse，选择Maven本地的的仓库所在的位置。然后点击Apply。然后再点OK。就可以
![](http://dl2.iteye.com/upload/attachment/0092/4254/3280c357-9e71-35ba-b83a-84b52680bfac.png)

通过以上两步，已经成功的把MyEclipse10自带的Maven插件，改成使用本地的Maven。

3、这时就可以建一个Maven的测试项目，在MyEclipse中File---New---other，在出现的对话框中输入Maven，如下图

![](http://dl2.iteye.com/upload/attachment/0092/4259/55171444-3a6e-3c32-b899-985e505d90d4.png)

4、选择Next-->Next。在出现的对话框中如下选择，如下图：
![](http://dl2.iteye.com/upload/attachment/0092/4265/ae50f6df-9534-3185-8ee1-b3ad0c1a7e4e.png)

5、Next后，在出现的对话框中进行如下填写。其中

Group Id：代表的是项目组织唯一的标识符，实际对应JAVA的包的结构，是main目录里java的目录结构。
ArtifactID：代表的是项目的唯一的标识符，实际对应项目的名称，就是项目根目录的名称。

Version：代表的是当前项目的版本。

package:代表项目的包路径。
![](http://dl2.iteye.com/upload/attachment/0092/4268/1d4b0a43-d214-3a7f-b6cb-a02789c424e5.png)

6、然后点击Finish。这样一个Maven项目就构建完成。如下图所示：
![](http://dl2.iteye.com/upload/attachment/0092/4279/f307e133-a51f-38c0-84a9-e7a13c63ec7c.png)

7、一般在做项目开发时，配制文件一般会新建一个资源包， 进行存放，src/main/resources里，发下图示。在这个包里一般用来存放我们的资源文件，如hibernate的配制文件、log4j的配置文件等等。
![](http://dl2.iteye.com/upload/attachment/0092/4284/8b328517-de87-3509-9999-749d428898d7.png)

8、同理，测试的配置文件也要新建一个资源包，进行存放，如下图示。这个叫约束优于配置，我们先把很多东西都约束好。


![](http://dl2.iteye.com/upload/attachment/0092/4288/d33f101c-4c2e-3ee2-af6f-5ff56cefa530.png)



  * [![](http://dl2.iteye.com/upload/attachment/0092/4254/3280c357-9e71-35ba-b83a-84b52680bfac-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4254/3280c357-9e71-35ba-b83a-84b52680bfac.png)
  * 大小: 33 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4256/69b51e05-5c6e-35b8-9d2a-e69d5b39dd76-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4256/69b51e05-5c6e-35b8-9d2a-e69d5b39dd76.png)
  * 大小: 40.6 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4259/55171444-3a6e-3c32-b899-985e505d90d4-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4259/55171444-3a6e-3c32-b899-985e505d90d4.png)
  * 大小: 30.5 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4265/ae50f6df-9534-3185-8ee1-b3ad0c1a7e4e-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4265/ae50f6df-9534-3185-8ee1-b3ad0c1a7e4e.png)
  * 大小: 48.5 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4268/1d4b0a43-d214-3a7f-b6cb-a02789c424e5-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4268/1d4b0a43-d214-3a7f-b6cb-a02789c424e5.png)
  * 大小: 39.8 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4279/f307e133-a51f-38c0-84a9-e7a13c63ec7c-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4279/f307e133-a51f-38c0-84a9-e7a13c63ec7c.png)
  * 大小: 11.6 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4284/8b328517-de87-3509-9999-749d428898d7-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4284/8b328517-de87-3509-9999-749d428898d7.png)
  * 大小: 8.2 KB

  * [![](http://dl2.iteye.com/upload/attachment/0092/4288/d33f101c-4c2e-3ee2-af6f-5ff56cefa530-thumb.png)](http://dl2.iteye.com/upload/attachment/0092/4288/d33f101c-4c2e-3ee2-af6f-5ff56cefa530.png)
  * 大小: 8.6 KB

  * 查看图片附件

分享到： [![](/images/sina.jpg)](javascript:; "分享到新浪微博") [![](/images/tec.jpg)](javascript:; "分享到腾讯微博")

  * 2013-12-23 15:03
  * 浏览 14300
  * 评论(0)
  * 分类:[研发管理](https://www.iteye.com/blogs/category/develop)
  * [查看更多](https://www.iteye.com/wiki/blog/1993972)

Global site tag (gtag.js) - Google Analytics
