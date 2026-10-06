---
source: "https://blog.csdn.net/weixin_33483304/article/details/165382187"
title: "Docker底层原理深度解析：从镜像分层到容器隔离-CSDN博客"
fetched_at: "2026-10-06 12:33"
---

说实话，很多人对Docker的理解一直停留在“会用命令”的层面，docker run、docker exec、docker-compose up这三板斧耍得挺熟，可真遇到virtualisation support not detected、容器期删数据没了、镜像拉不下来这类报错，就只能上网搜答案，搜一个改一个，下次换个报错又抓瞎。今天这篇我就把Docker的底层原理从头到尾拆一遍，把镜像、容器、仓库、网络、存储这些概念背后的逻辑讲透。看完你不仅能理解那些常见的热搜词到底是咋回事，还能自己推演出正确的排查思路。 

###  1\. 先搞清楚Docker到底解决了什么问题 

####  1.1 部署者的“环境地狱” 

在Docker出现以前，部署一套应用是真的折腾。举个最常见的例子：你在自己电脑上开发了一个Java项目，用的JDK 8、Tomcat 9、Redis 5，跑得好好的。到服务器上一看，机器上装的是CentOS 7，自带OpenJDK 11，Tomcat版本也不对，Redis也没有编译依赖的gcc，于是一通操作：卸载、重装、改环境变量、搞依赖……运气好一小时搞定，运气不好版本冲突直接劝退。 

这还只是单机。如果线上有十台机器，你就得保证这十台机器的系统版本、基础软件、环境变量完全一致。稍微差一点，就是典型的“在我电脑上是好的啊”翻车现场。传统虚拟机（比如VirtualBox、VMware）不是不能解决，但一个虚拟机是从内核开始虚拟化，光一个操作系统镜像就几个GB，启动还要半分钟，资源开销大得离谱。 

####  1.2 Docker的解法：把环境和应用一起打包 

Docker的核心理念只有一句话：把应用本身和应用运行所需的完整环境，当成一个整体来交付。这个整体就是“镜像”。镜像里面已经包含了操作系统的基础文件（但不包含内核）、运行时、依赖库、配置、代码。拿到镜像以后，在任何支持Docker的机器上启动，得到的环境都一模一样，不会再出现“这台机器缺个库”的问题。 

有人把Docker比作集装箱，我觉得挺贴切。传统软件交付是“散货码头”，各个依赖都是散装零件，到了目的地再拼装；Docker则是把所有的东西提前装到一个标准集装箱里，用标准工具直接吊起来走。只不过Docker集装箱里装的不是货物，而是一个“完整的运行环境快照”。 

###  2\. Docker的三层核心机制：镜像、容器、仓库 

####  2.1 镜像的分层设计原理 

先讲镜像。你拉过一个镜像就会发现，docker pull输出里会显示“Pull complete”，然后一串十六进制的sha256摘要。这其实暴露了镜像最重要的特性：分层存储。 

一个Docker镜像不是一块巨大的磁盘文件，而是由一组只读层堆叠起来的。每一条指令（RUN、COPY、ADD）在构建时都会产生一个新的只读层。比如一个最简单的MySQL镜像，它可能有这么几层：Debian基础系统层、MySQL软件层、初始化SQL脚本层。你在Dockerfile里写： 
    
    
    FROM ubuntu:22.04
    RUN apt-get update && apt-get install -y vim
    COPY app.py /app/
    CMD ["python", "app.py"]
    

构建完以后，ubuntu基础层、apt安装产物层、app.py文件层，全部是只读的。当你用这个镜像创建容器时，Docker会在最上面叠加一个可写层，这个可写层非常薄，容器运行期间的写入操作全部发生在这里。 

这个分层设计带来一个巨大的好处：层可复用。假如你本地已经有一个ubuntu:22.04基础镜像，现在要构建其他基于ubuntu的应用，就不用重新拉基础层了，只用下载新增的层。很多团队内部镜像巨大但实际拉取很快，就是利用了分层缓存。 

####  2.2 容器的本质：进程、命名空间与cgroups 

镜像是个静态文件，只有跑起来才叫容器。但容器的本质到底是什么？很多人想当然地觉得容器是个“轻量虚拟机”，这是误解。容器并不是一个完整的操作系统实例，它本质上就是宿主机上的一个普通进程，只不过这个进程被做了手脚，让它以为自己运行在一个独立的机器里。 

这个“手脚”就是Linux内核的两种特性： 

  * 命名空间（namespace）：负责隔离视野。它让容器内的进程只能看到属于自己的PID、网络栈、挂载点、主机名、进程间通信等。比如PID命名空间里，容器内第一个进程的PID是1，但在宿主机上它可能实际上是12345。进程杀不掉，很多时候就是因为你没找到真正PID。 
  * 控制组（cgroups）：负责限制资源。它能限制某个进程组最多能用多少CPU、多少内存、多少磁盘IO。 



你可以把容器理解成一个“带围栏的单间宿舍”：命名空间决定了你在宿舍里只能看到自己这点东西，cgroups决定了你最多能吃几碗饭，不能把整个食堂搬到屋里。容器与宿主机共享同一个内核，所以它不需要虚拟化硬件，启动只是一个进程启动，快如闪电。 

####  2.3 仓库与镜像分发 

镜像造好了怎么让别人用？答案是仓库（Registry）。Docker Hub是最常用的公共仓库，但它在国外，所以你在国内docker pull的时候经常会发现速度像蜗牛。这个在后面我会讲怎么解决。企业里一般用自建的Harbor或者Docker Registry来存私有镜像。 

镜像在仓库里的存储方式也不是一个巨大的文件，而是按层存储。Docker Engine从仓库拉取镜像时，会先获取镜像的manifest（清单），里面记录了镜像由哪些层组成、每一层的sha256校验和。客户端根据清单一层层下载，然后用这些层堆叠出完整的镜像。理解了这一点，就能理解为什么docker save导出的tar包比仓库里的镜像大很多——因为导出时通常把所有层合并卷成了一个完整文件，失去了分层的去重能力。 

###  3\. 常用命令背后的原理 

####  3.1 docker run到底发生了什么 

很多人敲了上千次docker run，不一定知道这个命令背后做了多少事。以最经典的命令为例： 
    
    
    docker run -d -p 3306:3306 \
      --name mysql8 \
      -e MYSQL_ROOT_PASSWORD=123456 \
      -v /my/data:/var/lib/mysql \
      mysql:8.0
    

你敲下这个命令后，Docker Engine大约会做这么几步： 

  1. 检查本地有没有mysql:8.0这个镜像，没有就去仓库拉取。 
  2. 用镜像创建一个容器，也就是在镜像的所有只读层之上挂载一个可写层。 
  3. 配置网络。默认情况下，容器会进入一个bridge网络，并申请一个172.17.0.x的IP。因为你加了 ` -p 3306:3306 ` ，Docker还会在宿主机上设置两条iptables规则，把宿主机的3306端口流量转发到容器的3306端口。 
  4. 设置环境变量。MYSQL_ROOT_PASSWORD被写入容器，MySQL进程启动时会读取它来初始化root密码。 
  5. 挂载数据卷。 ` -v /my/data:/var/lib/mysql ` ，把宿主机目录和容器目录做绑定，宿主机目录变成了容器内这个路径的“真身”。 
  6. 启动容器的主进程。主进程是什么？就是Dockerfile里CMD或ENTRYPOINT定义的进程，MySQL镜像里就是mysqld。 



值得注意的是，Docker容器只关心主进程是否活着。如果主进程退出了，容器就进入exited状态。很多人写Dockerfile时习惯最后加一句 ` /bin/bash ` ，结果发现容器一启动就秒退，就是因为bash执行完就退出，没有常驻进程。 

####  3.2 docker exec与attach：进入容器的不同方式 

排查问题时经常要进容器，常用命令是 ` docker exec -it <容器名> bash ` 。好多人会问，我能不能用 ` docker attach ` ？这两个有本质区别。 

` docker attach ` 是直接连接到容器的主进程标准输入输出上。你可以看到主进程的输出，并且能往主进程的输入里敲东西。但如果你不小心按了Ctrl+C，可能会把主进程给终止掉，容器就停了。而 ` docker exec ` 是在容器里再启动一个新进程，这个新进程和主进程是并列关系，只不过因为共享了PID、Network等命名空间，它能看到和主进程一样的容器视图。 ` docker exec ` 里执行exit只会退出你自己这个进程，完全不影响主进程。 

所以日常调试，除非你要看主进程的交互输出，否则一律用exec，别碰attach。 

####  3.3 Docker Compose：编排并非魔法 

当你的应用有多个容器时（比如后端、MySQL、Redis、Nginx），一个个docker run太累，于是有了Docker Compose。它做的事情本质上就是阅读docker-compose.yml，然后批量帮你执行socker run/network create/volume create。 
    
    
    version: '3.8'
    services:
      mysql:
        image: mysql:8.0
        container_name: mysql8
        environment:
          MYSQL_ROOT_PASSWORD: root123
        volumes:
          - mysql_data:/var/lib/mysql
        ports:
          - "3306:3306"
      redis:
        image: redis:6.2
        command: redis-server --appendonly yes
        volumes:
          - redis_data:/data
    volumes:
      mysql_data:
      redis_data:
    

` docker-compose up ` 执行的本质，是自动创建了一个默认网络，把你定义的服务全部连进去，然后再按depends_on的顺序逐个创建容器。之所以要搞一个默认网络，是为了让容器之间能通过服务名互相访问。比如后端Java连接MySQL时，jdbc:mysql://mysql:3306/xxx，这个mysql不是宿主机IP，而是compose网络里MySQL容器的DNS名字。理解了底层是“一个批量docker run工具”，你遇到compose报错时，心里就踏实很多：先 ` docker-compose config ` 检查配置，再单独 ` docker-compose logs ` 看日志。 

###  4\. 网络与存储原理 

####  4.1 Docker网络模式：bridge、host、none、container 

Docker的网络隔离也是靠命名空间实现的。每个容器创建时会拿到一个虚拟网卡，通过veth pair技术，一头插在容器里，另一头插在docker0这个虚拟网桥上。容器之间通信，就是通过这个网桥做二三层交换。默认的bridge模式让容器有自己独立的网络栈，IP是172.17.0.0网段。 

` host ` 模式下，容器不再使用自己的网络命名空间，而是直接共享宿主机的网络栈。好处是性能好，没有NAT转发；坏处是端口没法隔离，容器里绑了8080，宿主机也占用8080，容易冲突。 ` none ` 模式是彻底不配网络，适合离线任务场景。 ` container ` 模式是复用另一个容器的网络栈，比如sidecar容器可以通过localhost直接访问主容器。 

那 ` -p ` 端口映射又是怎么实现的？根源是iptables DNAT。宿主机监听3306端口，任何到达宿主机3306的包，都会被DNAT规则改写目标地址为容器的IP:3306，然后转发到docker0网桥。所以你能访问到容器里的MySQL服务。如果改了防火墙规则，或者重启了docker防火墙链，端口映射失效，大概率就是iptables规则被清了。 

####  4.2 存储驱动与数据卷 

默认情况下，容器内写入的数据全在可写层，而可写层是短暂的：容器删除，数据就没了。这也就是为什么MySQL容器重建后数据消失的原因。解决数据持久化的方案就是挂载数据卷。Docker里有两类挂载： 

  * 卷（volume）：由Docker管理，存放在 ` /var/lib/docker/volumes/ ` 下。 ` -v mysql_data:/var/lib/mysql ` 就是创建一个volume。 
  * 绑定挂载（bind mount）：直接把宿主机某个目录映射进容器， ` -v /my/data:/var/lib/mysql ` 。 



两者的核心区别是：volume由Docker托管，支持backup和迁移；bind mount则完全暴露宿主机目录，方便你直接看文件，但要注意权限问题。容器内MySQL进程运行时，是容器内用户（通常是mysql UID为999），如果宿主机挂载目录的所有者不是999，或者权限为755而不是775/700，就会报权限拒绝，MySQL起不来。这种问题在Windows上用Docker Desktop挂载C盘目录时尤其常见，因为NTFS权限和Linux权限的映射本身就麻烦。 

再往下说存储驱动。Docker默认使用overlay2，它利用overlayfs把多个下层只读目录合并成一个视图。每当你需要读取文件时，它会先查可写层；有就直接读，没有就到下一层找。正因为有这个路径，镜像层才能共享，容器启动时不会把所有层拷一遍。如果某个容器疯狂写数据，可写层迅速膨胀，最终可能占满磁盘。这解释了为什么生产环境一定要把数据挂到外部卷。 

###  5\. 排查问题要从原理出发 

####  5.1 virtualisation support not detected 的根源 

这个报错在Windows上出现频率极高。Docker Desktop默认依赖硬件虚拟化。如果你用的是WSL2后端，它需要CPU的虚拟化支持（VT-x/AMD-V）来控制一个轻量级虚拟机，在这个虚拟机里跑Linux内核，再跑容器。如果BIOS里没开启虚拟化开关，或者Windows功能里没启用"适用于Linux的Windows子系统"和"虚拟机平台"，Docker Desktop启动时就会提示virtualisation support not detected。 

排查思路： 

  1. 打开任务管理器 -> 性能 -> CPU，看“虚拟化”是不是“已启用”。没有就先重启进BIOS，找到Intel Virtualization Technology或AMD SVM Mode，设为Enabled。 
  2. 在“启用或关闭Windows功能”里勾选“虚拟机平台”和“适用于Linux的Windows子系统”。 
  3. 老CPU如果不支持VT-x/AMD-V，基本无解，装Docker也没用，只能换机器。 



理解原理的好处在于，你不会去乱装驱动或重装Docker Desktop。这个问题根本不在Docker软件本身。 

####  5.2 镜像下载慢怎么办 

镜像下载慢的原因，从原理上讲就一句话：默认仓库Docker Hub在全球分布不均，国内访问经常路由绕远。解决方案是配置镜像加速器，也就是告诉Docker Engine，拉镜像时先去这些国内可访问的registry mirror里找。 

Linux下修改 ` /etc/docker/daemon.json ` ： 
    
    
    {
      "registry-mirrors": [
        "https://docker.m.daocloud.io",
        "https://dockerproxy.com"
      ]
    }
    

修改后 ` systemctl daemon-reload && systemctl restart docker ` 。Windows下则在Docker Desktop设置里的Docker Engine里直接修改JSON配置，保存后重启。 

注意，镜像加速器只对Docker Hub的拉取生效。如果你配置了私有仓库， ` docker pull myregistry.com/app:1.0 ` ，它不会走mirror，而是直接访问私有仓库。这也是为什么企业里要自建Harbor，从内网拉镜像速度极快。 

####  5.3 权限错误与启动失败 

装完Docker后执行docker ps，报 ` Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock ` 。这句话的意思是，你的用户没有权限访问Docker守护进程监听的Unix socket。Docker装好后默认只有root和docker组里的用户能访问。解决方法是把当前用户加进docker组： 
    
    
    sudo usermod -aG docker $USER
    newgrp docker
    

加完组以后，不用sudo就能执行docker命令。 

还有一种常见情况： ` docker服务启动失败 ` 。别着急卸载重装，先去查日志： 
    
    
    journalctl -u docker --no-pager | tail -50
    

daemon.json配置写错了（比如多加了注释、JSON格式错误）最容易导致Docker服务启动失败。用 ` dockerd --debug ` 手动启动控制台能看到明确提示。等你能定位到具体原因后再处理，而不是一股脑重装。 

###  6\. Windows与Linux下Docker的底层差异 

####  6.1 Windows上Docker为什么需要WSL2或Hyper-V 

Linux容器本质上是Linux进程，它依赖Linux内核的namespace和cgroups特性。Windows系统没有Linux内核，所以Docker Desktop只能在Windows上跑一个轻量级虚拟机，在这个虚拟机里面启动一个Linux内核，然后容器跑在这个Linux内核之上。WSL2的出现让这种虚拟机更加轻量、启动更快，而且和Windows文件系统之间的集成更好。 

所以在Windows上装Docker，前置条件是“虚拟化”开启。这也就是前面那个virtualisation报错的来源。在Linux上，Docker直接使用宿主机内核，没有虚拟机这一层，所以几乎不需要什么硬件虚拟化支持。 

顺便说一句，Windows上的容器有两种模式：Linux容器和Windows容器。默认装的是Linux容器模式。只有当你要部署的是Windows容器（比如跑.NET Framework）时，才需要切到Windows容器模式，但那需要Windows Server核心这类基础镜像，体积大很多，应用面也窄。 

####  6.2 Docker Desktop与Linux原生的不同 

Docker Desktop本质是一个带图形界面的管理器，底层运行在一个精简虚拟机里。它和Linux原生Docker相比，多了文件共享映射、端口转发、资源限制（可以直接在设置里调整CPU和内存）等一整套集成。这些功能方便是方便，但性能上有损耗，尤其是文件IO。把大量小文件放在Windows目录下挂载到容器里，读取速度可能比Linux原生慢一倍以上。原因就是文件系统之间需要做转换，Docker Desktop通过9p或virtiofs协议做共享，跨系统访问难免有开销。 

所以个人开发调试用Docker Desktop没问题，真正上了生产服务器，还是建议直接用Linux，直接把Docker Engine装到CentOS、Ubuntu或者Debian里，避免中间那层虚拟机的开销。 

###  7\. 从原理到实践：几点心得 

最后分享几个我踩过坑之后才真正理解的经验，希望你在动手之前先把这些刻在脑子里。 

第一，不要把容器当成会持久运行的虚拟机。容器的主进程挂了，容器就退出。凡是需要保存的数据，一定要挂卷。我用Docker部署MySQL的时候，最早就吃了没挂卷的亏，容器一重建数据全没了，那种抓狂的感觉不希望你也体会。 

第二，镜像能小就小。原理上，镜像越大，每一层下载和解析时间越长，而且层级越多，对overlay2的读取性能影响也越大。尽量用alpine或者slim基础镜像，构建时把多个RUN合并，用 ` .dockerignore ` 排除无关文件。 

第三，生产环境一定要限制资源。Docker不加资源限制，某个容器出现内存泄漏时，可能把整个宿主机的内存占满，最后OOM killer直接干掉所有进程，包括sshd，你连机器都登不上。所以docker run时尽量加上 ` --memory=2g ` 、 ` --cpus=2 ` 这类的限制，即使你用的机器性能很充裕。 

第四，不要在生产容器里随意更新软件包。容器是可丢弃的，要升级依赖应该在Dockerfile里改，重新构建镜像，而不是进入容器里apt update然后跑几个月。否则容器一重建，你又得重新手敲一遍，等于把可复现性全丢了。 

第五，遇到问题先看日志，再查资料。Docker相关的报错，90%都能通过 ` docker logs ` 、 ` docker inspect ` 、 ` docker-compose logs ` 找到具体原因。信息量不够时，再加 ` journalctl -u docker ` 或者 ` dockerd --debug ` 。顺着原理排查，比到处搜“xxx怎么解决”要靠谱得多。 

Docker原理说穿了，就是“利用Linux内核特性做轻量隔离，通过分层镜像做环境一致性交付”。把这个底层逻辑捋顺了，你会发现命令行、配置文件、各种报错都变得有迹可循。这篇也算是把这些年实操中积累的理解浓缩了一遍，希望能帮你少走弯路。 
