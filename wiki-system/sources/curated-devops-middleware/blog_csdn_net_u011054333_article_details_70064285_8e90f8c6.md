---
source: "http://blog.csdn.net/u011054333/article/details/70064285"
title: "在Windows平台上搭建Docker开发环境_windows怎么创建dockerspace-CSDN博客"
fetched_at: "2026-10-05 15:29:03"
---

本文介绍的是如何在Windows系统上安装Docker运行环境。Docker官方提供了Windows平台上的安装包，这个安装包会打开Windows平台上的HyperV虚拟机。所以如果不喜欢使用HyperV虚拟机或者有需要使用其他虚拟机软件的话，可以自己在Linux虚拟机中安装Docker。

### 安装Docker

#### 安装Docker For Windows

首先打开[Docker下载页面](https://store.docker.com/editions/community/docker-ce-desktop-windows?tab=description)，然后下载Docker For Windows安装包。注意这个安装包是针对最新的Windows 10系统的，如果使用Windows 8之类的，请下载旧版本的Docker。

安装之后可能会弹出这么一个对话框，提示我们说HyperV未开启，询问我们是否要开启HyperV，我们选择是，然后电脑会重启。之后一切就准备就绪了。
![未开启HyperV](https://i-blog.csdnimg.cn/blog_migrate/f248207c7b032b9453a2a605cd5abaa3.webp?x-image-process=image/format,png)

电脑重启之后，我们应该可以在任务栏上找到一个Docker图标，右键点击选择version会弹出这样的对话框。如此一来，Docker就安装完毕了。

![Docker版本](https://i-blog.csdnimg.cn/blog_migrate/d348411453b3a3f90c06a4b131af164f.webp?x-image-process=image/format,png)

#### 安装Kitematic

右键点击Docker图标，会看到有一项名字叫 Kitematic，这是一个Docker可视化工具，推荐大家安装。我们点击这个菜单项，就会弹出一个对话框提示我们下载Kitematic，然后放到`C:\Program Files\Dockder\Kitematic`中。

然后打开Kitematic，我们可以看到如下的样子。在这里可以非常方便的下载、开启、关闭Docker镜像。如果你注册了Docker账号的话，还可以上传自己的Docker镜像，让大家一起使用。

![Kitematic](https://i-blog.csdnimg.cn/blog_migrate/8d1bf458b7d49b8e59d72735fe3639c4.webp?x-image-process=image/format,png)

### 使用Docker

#### 设置阿里云加速器

在下载Docker之前，我们需要先配置一下加速器。由于Docker的服务器在国外，所以下载镜像的速度不太理想。国内因此有了很多加速服务，其中最好用的还是阿里云的。我们打开[Docker 镜像服务](http://dev.aliyun.com/search.html)，登录账号之后，获取自己创加速器地址。然后使用`docker-machine`创建一个新的虚拟机并使用加速器来加速。


    docker-machine create --engine-registry-mirror=https://XXX.mirror.aliyuncs.com -d hyperv default

当然如果你有自己的代理的话，也可以直接在Docker设置中设置代理。

#### 安装镜像

我们在Kitematic中搜索`hello-world`，然后安装。当然如果使用命令行的话也可以，输入`docker pull hello-world`即可。
![docker hello-world](https://i-blog.csdnimg.cn/blog_migrate/cffc192d55dfc82dfd89606d2c49b1a4.webp?x-image-process=image/format,png)

安装完成之后运行`docker run hello-world`即可看到如下的输出。

![hello-world](https://i-blog.csdnimg.cn/blog_migrate/c1bffaf5e72a3ae9e98abc9b1b4d10c8.webp?x-image-process=image/format,png)

#### 进入镜像执行环境

在Kitematic中点击一个正在运行的镜像，然后点击右边的EXEC，就可以打开对应的执行环境了。

![redis](https://i-blog.csdnimg.cn/blog_migrate/a9d0980f1ac8108e8d021be7183cc752.webp?x-image-process=image/format,png)

默认情况下的shell是sh，不太好用。我们可以点击Kitematic下面的docker-cli右边的齿轮图标，然后将shell设置为bash。
![docker-cli设置](https://i-blog.csdnimg.cn/blog_migrate/5adb09ff5d7fe452d275da0a8e7fef13.webp?x-image-process=image/format,png)

#### 配置镜像

在镜像右边还有一个车Settings标签，点进来之后可以对镜像进行各种配置，如设置端口号、设置数据分区等等。

![配置镜像](https://i-blog.csdnimg.cn/blog_migrate/c7f723a0d17ab76d10b6e2805f756663.webp?x-image-process=image/format,png)

利用Docker，我们可以做很多事情。由于很多软件例如Redis之类的，主要设计为在Linux下工作，虽然有Windows下的版本，但是仍然有很多不足之处。利用Docker，我们可以在Linux环境下运行这些程序，又可以在Windows下开发，简直两全其美！
