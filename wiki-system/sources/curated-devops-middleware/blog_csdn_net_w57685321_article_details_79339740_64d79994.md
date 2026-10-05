---
source: "https://blog.csdn.net/w57685321/article/details/79339740"
title: "从零开始通过idea插件将一个spring boot项目部署到docker容器里运行_idea插件rancher-CSDN博客"
fetched_at: "2026-10-05 15:29:02"
---

#### 实操：将一个spring boot项目部署到docker容器里运行

##### 实验需要的环境：

腾讯云+Ubuntu 16.04 x64+idea+插件docker integration+daocloud

##### 第一步，安装操作系统

首先在腾讯云上安装一个干净的Ubuntu系统
系统使用Ubuntu 16.04 64位
这里服务市场虽然有docker，但是版本都太低（1.8.2左右），现在的一些镜像都不支持这些低版本的了，所以自己手动装个
![这里写图片描述](https://img-blog.csdn.net/2018022013563814?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
腾讯云推荐使用ssh连接，配置好后就不用输入登入密码了
![这里写图片描述](https://img-blog.csdn.net/20180220135824393?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
秘钥可以在腾讯云上创建，也可以在Xshell上创建
创建好密钥之后，腾讯云会给你一个私钥下载，这个应该保存好
然后找到密钥，绑定到主机
![这里写图片描述](https://img-blog.csdn.net/20180220135931253?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
然后在xshell里面建立ssh连接，把用户秘钥配置上去，就是腾讯云发给你的私钥
![这里写图片描述](https://img-blog.csdn.net/20180220140005450?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
然后成功连接上
![这里写图片描述](https://img-blog.csdn.net/20180220140036659?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

##### 第二步，搭建docker环境

由于网络的原因。。。推荐在DaoCloud里安装docker，国内镜像快

首先安装docker：
登录到daocloud
这里可以使用一键脚本，方便快捷
下载地址，按照它的说明安装
<https://download.daocloud.io/Docker_Mirror/Docker>
![这里写图片描述](https://img-blog.csdn.net/20180220140201927?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
我使用了这个脚本安装docker
这里可能会卡在-qq这个地方，这是网络的原因，因为是外链。。ctrl+c，在运行，多试多等待就可以了
然后运行脚本
![这里写图片描述](https://img-blog.csdn.net/20180220140306533?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
安装完成后，提示如果想用非root用户使用docker，应该将其加入docker组里面
![这里写图片描述](https://img-blog.csdn.net/20180220140402341?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
把普通用户加入组后，查看docker版本，发现安装的是最新的版本，有点高。都18去了

然后配置镜像加速器（不然pull镜像会很慢）
也是使用的daocloud
**地址：**
<http://www.daocloud.io/mirror#accelerator-doc>
![这里写图片描述](https://img-blog.csdn.net/20180220140500260?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
这里当时遇到了一个坑，由于使用的是腾讯云服务市场里的镜像（偷了装docker的懒），然后由于版本太低，它这个脚本是无法正常执行的，它好像需要1.12版本以上吧。。

然后愉快的pull images了，这里run了一个rancher（docker编排用的，图形化界面，方便管理）
这里提供一个rancher的中文文档，有兴趣研究研究：
<http://rancher.com/docs/rancher/v1.6/zh/>
![这里写图片描述](https://img-blog.csdn.net/20180220140543542?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
发现pull的很快
需要注意docker的版本，不然安装rancher会出问题，这点文档里写的很清楚
![这里写图片描述](https://img-blog.csdn.net/20180220140624275?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
成功运行了rancher，当然，现在什么都还没配置，但是说明docker是安装好了的
![这里写图片描述](https://img-blog.csdn.net/20180220140647379?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

##### 第三步，给docker开启远程访问

参考一份网上的资料
![这里写图片描述](https://img-blog.csdn.net/20180220140730200?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
这里我把端口设置为了2375
![这里写图片描述](https://img-blog.csdn.net/20180220140802359?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
然后保存文件，重启服务即可

**需要注意的是，如果在centOS7上搭建的docker，这个远程连接应该这样配置**


    ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock

![这里写图片描述](https://img-blog.csdn.net/20180220140821610?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
查看网络连接，发现**2375端口已经被打开**
如果发现还是远程连不上，可以设置一些腾讯云的安全策略和防火墙

**至此，在Ubuntu上搭建docker环境完成！**

#### 附：

由于我系统是win7的，所以也来试试安装docker，其实docker对win7的支持并不好（都是以虚拟机的形式运行的），推荐win10的系统

关于win7的安装
首先下载Docker Toolbox

还是在daoyun下载的
然后运行这个安装上去
![这里写图片描述](https://img-blog.csdn.net/20180220140930408?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
这里也有个坑，需要注意virtualbox要5版本以上的，以往安装过ensp，有个4版本的virtualbox，所以当时没选virtualbox，所以会出问题
![这里写图片描述](https://img-blog.csdn.net/20180220140956836?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
安装完成！
如果点击这个会提示找不到bash，在属性里把自己的bash设置上去即可
![这里写图片描述](https://img-blog.csdn.net/20180220141019193?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
**更改c盘文件的路径**
运行起来，发现它的虚拟机默认位置在c盘
![这里写图片描述](https://img-blog.csdn.net/201802201411185?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
随着pull的image越来越多，c盘空间越来越少，所以我把虚拟机磁盘文件移动到了e盘
在管理里面，找到虚拟介质管理器，选择move，移动到其他盘上
这里不要直接文件操作，把disk.vmdk文件移动到其他盘，然后在导入，这样会报错，说uuid冲突的
![这里写图片描述](https://img-blog.csdn.net/20180220141235355?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
然后配置镜像源
在我的文档里找到config.json
![这里写图片描述](https://img-blog.csdn.net/20180220141312350?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![这里写图片描述](https://img-blog.csdn.net/20180220141335916?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
然后配置images源
![这里写图片描述](https://img-blog.csdn.net/20180220141505113?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
**成功运行docker！**

##### 第四步，在IDEA上安装docker插件

Idea中可以下载docker插件，功能强大
官方文档
<https://www.jetbrains.com/help/idea/docker.html>

在setting里找到这个插件，安装上去
![这里写图片描述](https://img-blog.csdn.net/20180220141608781?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
成功安装插件

![这里写图片描述](https://img-blog.csdn.net/20180220141903696?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
点击+，新增一个docker服务器连接

需要注意的是win7的地址输入，是https，并且是2376端口！这点官方文档有写到
![这里写图片描述](https://img-blog.csdn.net/20180220141724862?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
要输入相应的ip
![这里写图片描述](https://img-blog.csdn.net/2018022014192340?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
win7的配置！！！
这样子就可以啦
同理，云服务器的，tcp连接，2375端口
![这里写图片描述](https://img-blog.csdn.net/201802201419577?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
连接成功
![这里写图片描述](https://img-blog.csdn.net/201802201420192?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

##### 第五步，在IDEA上操作docker

这里我准备把一个小实验放进docker容器跑

先写一个dockerFile
![这里写图片描述](https://img-blog.csdn.net/20180220142103803?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
这里注意到add写的是相对路径，所以jar包要在docker目录下，不然build镜像的时候会找不到文件
为了方便，干脆直接把dockerfile文件放在项目根目录里，然后写绝对路径找到打包好的jar包

![这里写图片描述](https://img-blog.csdn.net/20180220142140957?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![这里写图片描述](https://img-blog.csdn.net/20180220142200727?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
这里给了一个**前置任务** ，先打包为jar包，再构建image

配置好就可以run了
![这里写图片描述](https://img-blog.csdn.net/20180220142253560?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
运行方式选择docker
![这里写图片描述](https://img-blog.csdn.net/20180220142329495?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
构建镜像中，由于是云服务器，这里上传镜像需要一段时间，还是蛮快的
**构建成功**
通过docker ps命令可以看到当前上传上去的镜像已经被运行
![这里写图片描述](https://img-blog.csdn.net/20180220142409185?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

成功访问云服务器！
![这里写图片描述](https://img-blog.csdn.net/20180220142602596?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
Spring boot项目已经运行在docker上了！

**补充：**
docker插件更新之后更加方便部署了
选择dockerfile
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/9225b0e38de45dede5828218774230c0.jpeg)
给run built image打钩，然后绑定上端口，还可以预览命令行
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/9ed5cdcedff5fd591d63fb952c348959.jpeg)
这样配置好了之后，直接点idea的run，完成后云服务器就自动运行这个spring boot应用了

#### 附：

Spring boot项目打包成docker image

没有这款插件也不要紧
使用一个mvn plugin，可以构建docker image，前提是要安装docker环境



       <groupId>com.spotify</groupId>
       <artifactId>docker-maven-plugin</artifactId>
       <version>0.4.13</version>
       <configuration>
          <imageName>${docker.image.prefix}/${project.artifactId}</imageName>
          <dockerDirectory>src/main/docker</dockerDirectory>

          <!-- 解决win7 Connect to localhost:2375的问题的其中一种方式，注意要跟docker-machine env相一致 -->
          <dockerHost>https://192.168.99.100:2376</dockerHost>
          <dockerCertPath>C:\Users\admin\.docker\machine\machines\default</dockerCertPath>

          <resources>
             <resource>
                <targetPath>/</targetPath>
                <directory>${project.build.directory}</directory>
                <include>${project.build.finalName}.jar</include>
             </resource>
          </resources>
       </configuration>



在win7环境下的配置，需要指定ip（因为是虚拟机）
云服务器类似
![这里写图片描述](https://img-blog.csdn.net/20180220142711179?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
**执行maven命令**
![这里写图片描述](https://img-blog.csdn.net/20180220142734536?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![这里写图片描述](https://img-blog.csdn.net/20180220142750984?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdzU3Njg1MzIx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
原理差不多，也是使用了一个插件，在package打包成jar包后，使用docker的mvn插件构建一个镜像
