---
source: "http://www.cnblogs.com/shanyou/archive/2011/05/20/2052354.html"
title: "MongoDB 客户端 MongoVue - 张善友 - 博客园"
fetched_at: "2026-10-05 15:29:19"
---

今天在同事那里看到了一个很不错的MongoDB的客户端工具MongoVue，地址是<http://www.mongovue.com/>。做的不错，1.0版本的开始收费了，费用也不贵才35＄。真正需要的同学可以掏点钱买个吧，也算是支持这个工具，如果只是学习研究用的话我这里还有一个0.9.7版本，虽然比起1.0版来说有些bug，平常使用也够了，需要的同学可以单独联系我。

1.0版之后超过15天后功能受限。可以通过删除以下注册表项来解除限制：

[HKEY_CURRENT_USER\Software\Classes\CLSID\\{B1159E65-821C3-21C5-CE21-34A484D54444}\4FF78130]

把这个项下的值全删掉就可以了。

下面上图给大家感受下强大的MongoVue，可以提高你使用MongoDB的幸福指数好几十点，上图是王道：

1、配置连接

[![image](https://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202156425175.png)](http://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202156379291.png)

2、试下新建一个名为AccessLog的Collection ：

[![image](https://images.cnblogs.com/cnblogs_com/shanyou/201105/20110520215648644.png)](http://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202156459404.png)

[![image](https://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202156569851.png)](http://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202156514807.png)

3、插入一个Document

[![image](https://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202157041435.png)](http://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202157028144.png)

4、查看我们插入的数据，数据可以通过多种方式展示（树形、表格、文本）

[![image](https://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202157113806.png)](http://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202157089643.png)

上面我们都是通过图形界面的操作的吧，下面有一个窗口列出了上述操作的客户端命令哦，这是学习的好资源，在用图形界面的时候依然可以学习熟悉下命令行。

[![image](https://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202157132462.png)](http://images.cnblogs.com/cnblogs_com/shanyou/201105/201105202157122038.png)

当然上述只是介绍了下最基本的功能，还有更新，删除数据库，从mysql数据库导入数据等等功能，想了解更详细的内容请访问官方网站：<http://www.mongovue.com/>

需要的同学到这里下吧
<http://download.csdn.net/detail/shanyou/4129950>

<http://blog.nosqlfan.com/tags/mongodb>
