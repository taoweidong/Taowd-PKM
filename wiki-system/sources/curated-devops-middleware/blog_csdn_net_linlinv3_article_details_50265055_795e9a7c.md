---
source: "http://blog.csdn.net/linlinv3/article/details/50265055"
title: "docker【2】 docker安装  Install Docker Engine_docker install-CSDN博客"
fetched_at: "2026-10-05 15:28:58"
---

上一篇： [docker【1】docker简介（入门知识）](http://blog.csdn.net/linlinv3/article/details/50251539)

**docker安装 Install Docker Engine**

* * *

**前言：**

运行任何应用程序，都需要有两个基本步骤：构建一个镜像、运行容器。

这些步骤都是从Docker Client的命令开始的。

第1步：构建镜像

如前所述，Docker Image是一个构建容器的只读模板，它包含了容器启动所需的所有信息，包括运行程序和配置数据。

每个镜像都源于一个基本的镜像，然后根据Dockerfile中的指令创建模板。对于每个指令，在镜像上创建一个新的层面。

第2步：运行容器

运行容器源于我们在第一步中创建的镜像。当容器被启动后，一个读写层会被添加到镜像的顶层。当分配到合适的网络和IP地址后，需要的应用程序就可以在容器中运行了。

接下来，让我们一起安装Docker！

* * *



**ubuntu 系列安装docker**

  * ## 系统准备：

官方安装文档 <http://docs.docker.com/engine/installation/#installation>

注意：官网对版本要求写的很清楚，而且对于不同版本命令也少许不一样，大家根据自己的版本选择合适的命令；

这里使用最新版本ubutun15.10 下载地址 <http://releases.ubuntu.com/wily/>

下面给出查看ubutun内核和版本号和位数命令：







        1. $ uname -r


         4.2.0-16-generic

        2. $ sudo lsb_release -a


         Distributor ID: Ubuntu


         Description:    Ubuntu 15.10
         Release:        15.10
         Codename:       wily

        3. $ file /sbin/init (有的版本是这个命令，有的是下面的那个命令)


         /sbin/init: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x7aa29ded613e503fb09fb75d94026f3256f01e7a, stripped


        4. $ file /lib/systemd/systemd
         /lib/systemd/systemd: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=832cea0e7a1230fd7ebf93bba1858888ecb9b4d1, stripped





若是内核版本比较低则更新一下内核；

  * ## docker安装：

**第一种方式：**

操作系统默认的apt源有docker包，我们可以直接使用下面的apt-get命令安装docker:







        1. $ sudo apt-get install -y docker.io



但是ubutun仓库自带的往往不是最新的；为了获取最新的docker使用curl



**第二种方式：**

网站 [https://get.docker.com](https://get.docker.com/) 提供了curl-able的安装脚本install.sh，我们可以通过curl的方式进行安装docker。

我们先安装curl:




        1. $ sudo apt-get update
        2. $ sudo apt-get install curl



然后进行docker的安装：




        1. $ curl -k -sSl https://get.docker.com | sudo sh



查看docker版本：




        1. $ docker version
          Client:
          Version:      1.9.1
          API version:  1.21
          Go version:   go1.4.2
          Git commit:   a34a1d5
          Built:        Fri Nov 20 13:08:59 UTC 2015
          OS/Arch:      linux/amd64



建议使用第二种方式；

可以通过 https://get.docker.com 查看脚本命令。可以知道卸载方式是




        1. sudo apt-get remove docker-engine



  * ## docker验证

若上述命令执行成功后，就要验证一下docker是否安装成功了：

执行下面命令




        1. sudo docker run hello-world


        2. 若显示如下信息：
         Hello from Docker.
         This message shows that your installation appears to be working correctly.

         To generate this message, Docker took the following steps:
          1. The Docker client contacted the Docker daemon.
          2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
          3. The Docker daemon created a new container from that image which runs the
             executable that produces the output you are currently reading.
          4. The Docker daemon streamed that output to the Docker client, which sent it
             to your terminal.

         To try something more ambitious, you can run an Ubuntu container with:
          $ docker run -it ubuntu bash

         Share images, automate workflows, and more with a free Docker Hub account:
          https://hub.docker.com

         For more examples and ideas, visit:
          https://docs.docker.com/userguide/




证明docker正常工作！下面我们就可以开始docker之旅啦~



补充命令：可以使用命令查看容器状态

1、查看正在运行的容器




        1. sudo docker ps



         CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES




2、查看所有的容器




        1. sudo docker ps -a



         CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                         PORTS               NAMES
         5ddce0ca3e4f        hello-world         "/hello"            2 minutes ago       Exited (0) 2 minutes ago                           serene_jennings
         551e257cbc08        hello-world         "/hello"            2 minutes ago       Exited (0) 2 minutes ago                           drunk_sammet
         584c3a343739        hello-world         "/hello"            About an hour ago   Exited (0) About an hour ago                       trusting_hypatia
         005c31a4cd49        hello-world         "/hello"            About an hour ago   Exited (0) About an hour ago                       goofy_easley
         b865dac40a66        hello-world         "/hello"            About an hour ago   Exited (0) About an hour ago                       furious_borg





3、查看本地镜像




        1. sudo docker images



         REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
         hello-world         latest              0a6ba66e537a        8 weeks ago         960 B




4、从镜像中运行/停止一个新实例




        1. sudo docker run/stop --help




通过help查询一些参数，根据自己的id启动/停止实例

* * *

注意：

每次 使用docker命令都需要使用sudo

这里把当前用户加入到docker组就可以直接使用命令，而不用每次都加sudo




        1. $ sudo groupadd docker



         #改完后需要重新登陆用户

        2. $ sudo gpasswd -a ${USER} docker
