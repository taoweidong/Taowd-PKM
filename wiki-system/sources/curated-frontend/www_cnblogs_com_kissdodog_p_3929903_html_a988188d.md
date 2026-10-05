---
source: "http://www.cnblogs.com/kissdodog/p/3929903.html"
title: "Bootstrap <第一篇> - 逆心 - 博客园"
fetched_at: "2026-10-05 15:31:34"
---

# 一、使用Bootstrap要引用的文件

要使用Bootstrap，基本架构要引用如下文件：


        <link href="bootstrap.min.css" rel="stylesheet" type="text/css" />



最简单的页面示例代码如下：


    <!doctype html>
    <head>
        <meta charset="utf-8">
        <title>js</title>
        <link href="ace.min.css" rel="stylesheet" type="text/css" />


    </head>
    <body>

        <h1 class="btn btn-success btn-large"><i class="icon-user icon-white"></i>Hello,World</h1>

    </body>
    </html>

显示效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/221723241594584.jpg)

# 二、使用前要点

**1、DOCTYPE**

Bootstrap使用了HTML5元素，所以HTML头部要加上


    <!DOCTYPE html>
    <html>
    ....
    </html>

**2、viewport**


    <meta name="viewport" content="width=device-width, initial-scale=1.0">

  * Width=device-width => 表示页面宽度是设备屏幕的宽度；确保网页能被不同屏幕分辨率的设备正确呈现；
  * user-scalable=no => 是否可以调整缩放比例(yes/no)；
  * initial-scale=1.0 => 表示初始的缩放比例 ，以 1:1 的比例呈现，不会有任何的缩放；minimum-scale=0.5：最小允许的缩放比例；
  * maximum-scale=2.0：最大允许的缩放比例；

如果maximum-scale=1.0 与 user-scalable=no 一起使用。这样禁用缩放功能后，用户只能滚动屏幕，就能让您的网站看上去更像原生应用的感觉。

这样设置后，图片或元素也设置style="width:100%"，那么图片看起来也是全屏的了。

**3、img-responsive响应式图像**

为图片加上img-responsive属性，可以让图片对响应式布局更加好。其样式如下：


    .img-responsive {
    　　display: inline-block;
    　　height: auto;
    　　max-width: 100%;
    }

添加了此属性的图片会按比例缩小，但不能方法。

而上面的直接设置width:100%会放大，可能会出现失真的情况。

# 三、Bootstrap网格系统

**1、网格系统是什么东西**

Bootstrap把一个页面分为12列，通过指定数字就能够设置宽度。简单的示例:



             3
             6
             3


显示效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/221905544717473.jpg)

当浏览器的宽度缩小时(为下面说明响应式做铺垫)，显示效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/221907104714558.jpg)

要点：

1、row是容器，网格样式要放在row容器里面。

2、1个网页是12列。

3、一共有4个前缀的网格class前缀，分别应用于分辨率的设备。

图表如下：

![](https://images0.cnblogs.com/blog/347600/201408/221857453318536.jpg)

**2、响应式网格**

示例说明：



             3
             3
             3
             3


显示效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/221925010185883.jpg)

当浏览器缩小时：

![](https://images0.cnblogs.com/blog/347600/201408/221925130033476.jpg)

当再进一步缩小时：

![](https://images0.cnblogs.com/blog/347600/201408/221927043468860.jpg)

这就是所谓的响应式，说白了"响应式"就是根据浏览器的宽度来决定使用哪一个class，以上效果展示了响应式布局的原理:

  * **当屏幕宽度u≥1200px时，bootstrap会自动选用col-lg-*这个class；**
  * **当屏幕宽度u≥992px时，bootstrap会自动选用col-sm-*这个class；**
  * **当屏幕宽度u≥768px时，bootstrap会自动选用col-md-*这个class；**
  * **当屏幕宽度u <768px时，bootstrap会自动选用col-lg-*这个class；**

**3、偏移列**

偏移列的意思是隔开多少个列。

示例：


         3 　　//向右偏移2列了
         3

显示效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/221936028151332.jpg)

**.col-xs=*** 类不支持偏移，它们可以简单地通过使用一个空的单元格来实现该效果。

这个样式相当于设置了margin:宽度*列数。

**4、嵌套列**

在网格里嵌套网格




                 2
                 2
                 2
                 2



输出效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/221945087841095.jpg)

**5、列排序**

通过使用".col-md-push-*"和".col-md-pull-*"能够互换顺序。其中*的范围从1到11。

示例如下：



        无排序：

             First
             Second

        有排序：

             First
             Second


显示效果如下：

![](https://images0.cnblogs.com/blog/347600/201408/222007180493927.jpg)

以上class使用的理解为：本来First占据4列，Second占据8列，如果要互换位置，则First要向右推(push)8个列，而Second要向左拉4个列。
