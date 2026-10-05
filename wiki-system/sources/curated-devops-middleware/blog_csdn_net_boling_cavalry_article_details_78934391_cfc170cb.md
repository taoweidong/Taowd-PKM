---
source: "https://blog.csdn.net/boling_cavalry/article/details/78934391"
title: "maven构建docker镜像三部曲之三：推送到远程仓库(内网和阿里云)_maven 推送镜像-CSDN博客"
fetched_at: "2026-10-05 15:29:00"
---

原文地址：<http://blog.csdn.net/boling_cavalry/article/details/78934391>

在上一章[《maven构建docker镜像三部曲之二：编码和构建镜像》](http://blog.csdn.net/boling_cavalry/article/details/78872020)的实战中，我们将spring boot的web工程构建成docker镜像并在本地启动容器成功，今天我们把docker-maven-plugin插件的推送功能也用上，这样编译、构建、推送都能一次性完成了；

#### 源码和环境

本次实战的java web工程源码和环境都沿用上一章的，源码我已经上传到github上，地址是：git@github.com:zq2599/blog_demos.git，浏览器访问地址是：[https://github.com/zq2599/blog_demos，这里面有多个工程，本次实战用到的是mavendockerplugindemo，如下图红框所示：](https://github.com/zq2599/blog_demos%EF%BC%8C%E8%BF%99%E9%87%8C%E9%9D%A2%E6%9C%89%E5%A4%9A%E4%B8%AA%E5%B7%A5%E7%A8%8B%EF%BC%8C%E6%9C%AC%E6%AC%A1%E5%AE%9E%E6%88%98%E7%94%A8%E5%88%B0%E7%9A%84%E6%98%AFmavendockerplugindemo%EF%BC%8C%E5%A6%82%E4%B8%8B%E5%9B%BE%E7%BA%A2%E6%A1%86%E6%89%80%E7%A4%BA%EF%BC%9A)  
![image](https://img-blog.csdn.net/20171224000254192?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

#### 把构建的镜像推送到哪里去

本次实战有以下两个地方可以存放镜像，我们每个都要试试：

  1. 内网中，自己搭建的docker私有仓库；
  2. 阿里云的镜像仓库；



接下来我们分别推送到上述两个仓库，先推送到内网的私有仓库吧。

#### 如何搭建内网的私有仓库

  1. 在内网搭建和使用私有仓库的详细步骤，请看[《docker私有仓库搭建与使用实战》](http://blog.csdn.net/boling_cavalry/article/details/78818462)，就不在此赘述了；
  2. 用于编译和构建镜像的虚拟机上，记得配置/etc/default/docker和/lib/systemd/system/docker.service文件，使docker服务可以在http协议下工作，否则无法推送到内网私有仓库；



#### pom配置信息

用SecureCRT登录虚拟机，在工程的目录下新建一个pom_3_inner_server.xml文件，内容和pom_1_by_param.xml文件的一模一样，然后对pom_3_inner_server.xml文件做下列修改：

  * 新增registryUrl节点，内容是私有仓库地址和端口，如下：


    
    
    <registryUrl>192.168.119.148:5000</registryUrl>
    

  * 新增pushImage节点，内容如下：


    
    
    <pushImage>true</pushImage>
    

  * 修改imageName节点的内容，改为私有仓库地址和端口，再加上镜像id和TAG，如下：


    
    
    <imageName>192.168.119.148:5000/${project.artifactId}:${project.version}</imageName>
    

执行以下命令开始构建：
    
    
    mvn -f pom_3_inner_server.xml clean package -DskipTests docker:build
    

构建完毕后发现输出了报错信息，如下：
    
    
    [INFO] Building image 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    Step 1/3 : FROM java:8u111-jdk
     ---> d23bdf5b1b1b
    Step 2/3 : ADD /mavendockerplugindemo-0.0.1-SNAPSHOT.jar //
     ---> 634afbb47de5
    Removing intermediate container 8c165fad6a2c
    Step 3/3 : ENTRYPOINT java -jar /mavendockerplugindemo-0.0.1-SNAPSHOT.jar
     ---> Running in 1840b6345566
     ---> ff415c0f2d72
    Removing intermediate container 1840b6345566
    Successfully built ff415c0f2d72
    [INFO] Built 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    [INFO] Tagging 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT with 0.0.1-SNAPSHOT
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    [WARNING] Failed to push 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT, retrying in 10 seconds (1/5).
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    [WARNING] Failed to push 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT, retrying in 10 seconds (2/5).
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    [WARNING] Failed to push 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT, retrying in 10 seconds (3/5).
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    [WARNING] Failed to push 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT, retrying in 10 seconds (4/5).
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    [WARNING] Failed to push 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT, retrying in 10 seconds (5/5).
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD FAILURE
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 01:00 min
    [INFO] Finished at: 2017-12-28T17:26:46-08:00
    [INFO] Final Memory: 32M/90M
    [INFO] ------------------------------------------------------------------------
    [ERROR] Failed to execute goal com.spotify:docker-maven-plugin:0.4.12:build (default-cli) on project mavendockerplugindemo: Exception caught: Put http://192.168.119.148:5000/v1/repositories/mavendockerplugindemo/: dial tcp 192.168.119.148:5000: getsockopt: connection refused -> [Help 1]
    [ERROR] 
    [ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
    [ERROR] Re-run Maven using the -X switch to enable full debug logging.
    [ERROR] 
    [ERROR] For more information about the errors and possible solutions, please read the following articles:
    [ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
    

错误信息中有这么一句：Failed to push …，看起来是连不上私有仓库，登录到私有仓库的机器上去看了以下，果然，docker容器没有启动呢…

执行命令docker start docker-registry将私有仓库的服务容器启动，再回到构建服务的机器上，再执行一次构建命令，这次成功了，如下：
    
    
    [INFO] Building image 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    Step 1/3 : FROM java:8u111-jdk
     ---> d23bdf5b1b1b
    Step 2/3 : ADD /mavendockerplugindemo-0.0.1-SNAPSHOT.jar //
     ---> a033c632d0b0
    Removing intermediate container 1d702736fae4
    Step 3/3 : ENTRYPOINT java -jar /mavendockerplugindemo-0.0.1-SNAPSHOT.jar
     ---> Running in c3e4a2a41936
     ---> 649774e8dc21
    Removing intermediate container c3e4a2a41936
    Successfully built 649774e8dc21
    [INFO] Built 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    [INFO] Tagging 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT with 0.0.1-SNAPSHOT
    [INFO] Pushing 192.168.119.148:5000/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [192.168.119.148:5000/mavendockerplugindemo]
    7b4f222745df: Pushed 
    35c20f26d188: Layer already exists 
    c3fe59dd9556: Layer already exists 
    6ed1a81ba5b6: Layer already exists 
    a3483ce177ce: Layer already exists 
    ce6c8756685b: Layer already exists 
    30339f20ced0: Layer already exists 
    0eb22bfb707d: Layer already exists 
    a2ae92ffcd29: Layer already exists 
    0.0.1-SNAPSHOT: digest: sha256:4c8d5489bcb99ec1c0884adfdeeb25e5706de8f940c406c5a560243681b01831 size: 2212
    null: null 
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 12.760 s
    [INFO] Finished at: 2017-12-28T17:36:25-08:00
    [INFO] Final Memory: 32M/88M
    [INFO] ------------------------------------------------------------------------
    

在用于构建镜像的虚拟机和作为镜像仓库的虚拟机上，分别执行curl -X GET <http://192.168.119.148:5000/v2/_catalog>，查看私有仓库的镜像信息(192.168.119.148是私有仓库虚拟机的IP)，都能见到镜像mavendockerplugindemo，如下图：  
![这里写图片描述](https://img-blog.csdn.net/20171229192059908?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

推送到内网私有仓库的实战已经完成，接下来我们试试推送到阿里云镜像仓库吧；

#### 注册和登录阿里云

使用阿里云镜像仓库前，需要在阿里云网站注册一个账号，请您自行完成注册登录，此处不赘述了；

#### 创建命名空间和镜像仓库

  1. 在阿里云首页的”产品”菜单下，找到"容器镜像服务"，然后点击跳转，如下图：  
![这里写图片描述](https://img-blog.csdn.net/20171229192113208?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  2. 新的页面中，点击"管理控制台"，如下图：  
![这里写图片描述](https://img-blog.csdn.net/20171229192127251?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  3. 在控制台页面中，按照下图操作，创建一个命名空间bolingcavalry：  
![这里写图片描述](https://img-blog.csdn.net/20171229192406933?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  4. 在控制台页面中，按照下图操作，选一个近的仓库，再点击"创建镜像仓库"按钮开始创建镜像仓库：  
![这里写图片描述](https://img-blog.csdn.net/20171229192141256?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  5. 参考下图的步骤填写表单，创建一个仓库：  
![这里写图片描述](https://img-blog.csdn.net/20171229192424827?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  6. 如下图，创建完毕后就能在列表页面看见了，注意红框所示，一定要选择和创建时一样的地区，否则在列表中看不见刚刚创建的仓库：  
![这里写图片描述](https://img-blog.csdn.net/20171229192518822?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  7. 从列表中我们可以看见，仓库地址是 [registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo](http://registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo)，记下来后面会用到的；



#### 修改maven的配置文件

回到虚拟机上，打开文件/opt/apache-maven-3.3.3/conf/settings.xml，找到<servers>节点，在里面添加一个server节点，内容如下：
    
    
        <server>
          <!--maven的pom中可以根据这个id找到这个server节点的配置-->  
          <id>docker-aliyun</id>
          <!--这里是在阿里云注册的账号-->
          <username>12345678@qq.com</username>
          <!--这里是在阿里云注册的密码-->
          <password>abcdef</password>
          <configuration>
                <!--这是在阿里云注册时填写的邮箱-->
                <email>12345678@qq.com</email>
          </configuration>
        </server>
    

请参照注释的提示，将您在阿里云上的账号密码都填写到对应位置；

#### pom配置信息

在java web工程的目录下新建一个pom_4_ali_server.xml文件，内容和pom_1_by_param.xml文件的一模一样，然后再对pom_4_ali_server.xml文件做以下修改：

  * 阿里云镜像仓库列表页面中，我们创建的镜像仓库的地址是"[registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo](http://registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo)"，现在把这个字符串拆成三部分，将前面两部分作为两个属性放入pom文件的<properties>节点中，属性名分别是docker.repostory和[docker.registry.name](http://docker.registry.name)，此时properties节点的内容如下：


    
    
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
        <docker.repostory>registry.cn-shenzhen.aliyuncs.com</docker.repostory>
        <docker.registry.name>bolingcavalry</docker.registry.name>
    </properties>
    

  * 新增serverId节点，内容是之前修改的maven配置文件中，server节点的id，如下：


    
    
    <serverId>docker-aliyun</serverId>
    

  * 新增registryUrl节点，内容是私有仓库地址，如下：


    
    
    <registryUrl>${docker.repostory}</registryUrl>
    

  * 新增pushImage节点，内容如下：


    
    
    <pushImage>true</pushImage>
    

  * 修改imageName节点的内容，改为私有仓库地址和端口，再加上镜像id和TAG，如下：


    
    
    ${docker.repostory}/${docker.registry.name}/${project.artifactId}:${project.version}
    

#### 构建并推送到阿里云镜像仓库

执行以下命令开始构建：
    
    
    mvn -f pom_4_ali_server.xml clean package -DskipTests docker:build
    

构建完成后的输出信息如下，表示推送成功了：
    
    
    [INFO] Building image registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    Step 1/3 : FROM java:8u111-jdk
     ---> d23bdf5b1b1b
    Step 2/3 : ADD /mavendockerplugindemo-0.0.1-SNAPSHOT.jar //
     ---> f912a6c9134c
    Removing intermediate container a05fb50d6235
    Step 3/3 : ENTRYPOINT java -jar /mavendockerplugindemo-0.0.1-SNAPSHOT.jar
     ---> Running in 1c71545bdd60
     ---> fa4eee94dae6
    Removing intermediate container 1c71545bdd60
    Successfully built fa4eee94dae6
    [INFO] Built registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    [INFO] Tagging registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT with 0.0.1-SNAPSHOT
    [INFO] Pushing registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    The push refers to a repository [registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo]
    1efab0de4a7d: Pushed 
    35c20f26d188: Pushed 
    c3fe59dd9556: Pushed 
    6ed1a81ba5b6: Pushed 
    a3483ce177ce: Pushed 
    ce6c8756685b: Pushed 
    30339f20ced0: Pushed 
    0eb22bfb707d: Pushed 
    a2ae92ffcd29: Pushed 
    0.0.1-SNAPSHOT: digest: sha256:89062f267fe22df3acc5d6ca7405140162e43076aeda5f7584dbf80fcdc0c58b size: 2212
    null: null 
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 01:28 min
    [INFO] Finished at: 2017-12-29T02:45:05-08:00
    [INFO] Final Memory: 34M/83M
    [INFO] ------------------------------------------------------------------------
    

#### 在阿里云网页查看

  1. 打开阿里云镜像仓库管理页面，如下图：  
![这里写图片描述](https://img-blog.csdn.net/20171229193013939?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  2. 点击"镜像版本"，在列表中可以看到该镜像的版本，以及最后的上传时间，和我们的构建结果都是一致的，如下图：  
![这里写图片描述](https://img-blog.csdn.net/20171229193101171?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



#### 下载并验证镜像

  1. 在虚拟机上用docker rmi 镜像名称:镜像版本命令将所有的镜像删除干净，如果有容器还未删除，就要先删除容器再删除镜像，查看容器的命令是docker ps -a，删除容器的命令是docker rm 容器名；
  2. 如下图，在管理页面点击“基本信息”，可以看见登录阿里云镜像仓库和下载镜像的命令，在虚拟机上先执行登录命令，会要求输入密码，输入后登录成功：  
![这里写图片描述](https://img-blog.csdn.net/20171229193201042?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
  3. 执行下载镜像的命令，如下，将我们之前上传的镜像下载下来：


    
    
    docker pull registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    

输出信息如下，表示下载成功：
    
    
    root@docker-app:/usr/local/work/mavendockerplugindemo# docker pull registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    0.0.1-SNAPSHOT: Pulling from bolingcavalry/mavendockerplugindemo
    e12c678537ae: Already exists 
    8d9ed335b7db: Already exists 
    3318dd58ae60: Already exists 
    624ba6156166: Already exists 
    c7a02d193df7: Already exists 
    813b62320378: Already exists 
    81cf5426393a: Already exists 
    0a2b7222259b: Already exists 
    fadb940064b4: Pull complete 
    Digest: sha256:89062f267fe22df3acc5d6ca7405140162e43076aeda5f7584dbf80fcdc0c58b
    Status: Downloaded newer image for registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    

  * 执行如下命令，用下载的镜像创建一个容器：


    
    
    docker run --name demo003 -p 8080:8080 registry.cn-shenzhen.aliyuncs.com/bolingcavalry/mavendockerplugindemo:0.0.1-SNAPSHOT
    

输出信息会提示启动成功，这时候在当前电脑上打开浏览器，输入"<http://192.168.119.155:8080/>"，可以看见web工程的controller的返回信息了，如下图：  
![这里写图片描述](https://img-blog.csdn.net/20171229193233955?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

#### 结束

至此，maven构建docker镜像的三部曲就全部结束了，希望对您熟悉和使用docker-maven-plugin插件有所帮助，另外，本文中用到的pom_3_inner_server.xml和pom_4_ali_server.xml文件，我已上传到git上本次实战的web工程中，地址是：git@github.com:zq2599/blog_demos.git，浏览器访问地址是：[https://github.com/zq2599/blog_demos，这里面有多个工程，本次实战用到的是mavendockerplugindemo，如下图红框所示：](https://github.com/zq2599/blog_demos%EF%BC%8C%E8%BF%99%E9%87%8C%E9%9D%A2%E6%9C%89%E5%A4%9A%E4%B8%AA%E5%B7%A5%E7%A8%8B%EF%BC%8C%E6%9C%AC%E6%AC%A1%E5%AE%9E%E6%88%98%E7%94%A8%E5%88%B0%E7%9A%84%E6%98%AFmavendockerplugindemo%EF%BC%8C%E5%A6%82%E4%B8%8B%E5%9B%BE%E7%BA%A2%E6%A1%86%E6%89%80%E7%A4%BA%EF%BC%9A)  
![image](https://img-blog.csdn.net/20171224000254192?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYm9saW5nX2NhdmFscnk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

#### 欢迎关注我的公众号：程序员欣宸

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2333f08a28515d57a2806bd807f923c7.jpeg)
