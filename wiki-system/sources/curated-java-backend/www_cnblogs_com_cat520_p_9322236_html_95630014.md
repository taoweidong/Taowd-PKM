---
source: "https://www.cnblogs.com/cat520/p/9322236.html"
title: "IntelliJ IDEA安装Activiti插件并使用 - 会偷袭的猫 - 博客园"
fetched_at: "2026-10-05 15:32:57"
---

### 一、安装Activiti插件

#### 1.搜索插件

点击菜单【File】-->【Settings...】打开【Settings】窗口。

点击左侧【Plugins】按钮，在右侧输出＂actiBPM＂，点击下面的【Search in repositories】链接会打开【Browse Repositories】窗口。

![](https://img-blog.csdn.net/2018051614380834)

#### 2.开始安装

进入【Browse Repositories】窗口，选中左侧的【actiBPM】，点击右侧的【Install】按钮，开始安装。

![](https://img-blog.csdn.net/201805161438219)

#### 3.安装进度

![](https://img-blog.csdn.net/20180516143829145)

#### 4.安装完成

安装完成后，会提示【Restart IntelliJ IDEA】，重启IDEA即可完成安装。

![](https://img-blog.csdn.net/20180516143835261)

#### 5.查看结果

打开【Settings】窗口，在【Plugins】中可看到安装的【actiBPM】插件，表示安装成功。

![](https://img-blog.csdn.net/20180516143902240)

### 二、使用Activiti

#### 1.创建BPMN文件

点击菜单【File】-->【New】-->【BpmnFile】

![](https://img-blog.csdn.net/20180516143919895)

输入文件名称，点击【OK】按钮

![](https://img-blog.csdn.net/20180516144004472)

会出现如下绘制界面

![](https://img-blog.csdn.net/20180516144011442)

#### 2.绘制流程图

鼠标左键拖拽右侧图标，将其拖下左侧界面上，同样的方式再拖拽其他图标

![](https://img-blog.csdn.net/20180516144018897)

鼠标移至图标的中心会变成黑白色扇形，拖拽到另一图标，即可连接

![](https://img-blog.csdn.net/20180516144024740)

双击图标，可修改名称

![](https://img-blog.csdn.net/20180516144032520)

#### 3.导出图片

右击bpmn文件，选择【Refactor】-->【Rename】，修改其扩展名为.xml，点击【Refactor】

![](https://img-blog.csdn.net/2018051614404063)

接着右击此xml文件，选择【Diagrams】-->【Show BPMN 2.0 Diagrams...】，打开如下界面

![](https://img-blog.csdn.net/20180516144047240)

点击上图中【Export to file】图标，弹出【Save as image】窗口，点击【OK】即可导出png图片

![](https://img-blog.csdn.net/20180516144054817)

#### 4.解决中文乱码问题

在IDEA的安装目录，在下面两个文件中加上-Dfile.encoding=UTF-8

![](https://img-blog.csdn.net/20180516144128943)

![](https://img-blog.csdn.net/20180516144141606)

重启IDEA，乱码问题解决

![](https://img-blog.csdn.net/20180516151001428)
