---
source: "https://blog.csdn.net/lovelife527386108/article/details/51697081"
title: "IntelliJ IDEA中Docker使用_intellij idea docker-CSDN博客"
fetched_at: "2026-10-05 15:28:56"
---

## Docker Plugin

简单记录下我在**IntelliJ IDEA** 中如何使用**Docker**

* * *

#### 文章目录

  * Docker Plugin
  *     * Intellij Idea 配置Docker
    *       * 启动Docker Daemon
      * Certificates
      * 连接Docker
    * Deploy on Docker
    *       * Run/Debug Configurations
      * Start Docker

### Intellij Idea 配置Docker

> **Docker** ：Docker是目前比较流行的容器，帮你管理应用服务 —— [Docker官网](https://www.docker.com/)

###下载Docker插件

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/ea583c14e1f8df1c592602db610fcd6a.png)

#### 启动Docker Daemon

> 启用TCP连接：
>  _**sudo docker daemon -H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock**_

#### Certificates

> 将Docker登录证书拷贝到本地，准备连接

![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/2d006334671ace88ef9b516ec1a23985.png)

#### 连接Docker

> **Intellij Idea 15.0**
>  ![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/56f5b3e41b14a7242e080eddb38be382.png)
>  **Intellij Idea 2016**
>  ![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/6b2a49f9929c94ff6111b02d3cc39771.png)

###配置Docker Registry
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/02f5c60f4bdeee2960c97e4ad57adc2e.png)

### Deploy on Docker

#### Run/Debug Configurations

> 构建Docker镜像 Dockerfile（build image）
>  _**Dockerfile:**_
>  FROM tomcat
>  ADD HelloWorld.war /usr/local/tomcat/webapps

> * * *
>
> Docker容器参数配置
>  _**Container.json:**_
>  {
>  “HostConfig”: {
>  “PortBindings”:{ “8080/tcp”: [{ “HostIp”: “0.0.0.0”, “HostPort”: “18080” }] }
>  }
>  }

> **发布镜像**
>  ![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/10f8f9f6b36cde9b397311d49ad4464e.png)

> _**加载容器配置JSON file**_
>  ![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/2b0c9af6da022b4ec2c9836248e1e282.png)

#### Start Docker

**localhost:18080/HelloWorld**
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/30187b63caaa733a55f67f5dd67ca3ae.png)

##参考
[我的博客](https://whathowhy.com/2018/03/30/Docker-Plugin/)
[Docker](https://www.docker.com/)
[IntelliJ IDEA](https://www.jetbrains.com/help/idea/2016.1/run-debug-configuration-docker-deployment.html)
