---
source: "http://www.imooc.com/article/16448"
title: "在Centos和Redhat上安装Docker_慕课手记"
fetched_at: "2026-10-05 15:29:54"
---

[ 0 ](https://order.imooc.com/pay/cart)

  * [登录](https://www.imooc.com/user/newlogin) / [注册](https://www.imooc.com/user/newsignup)

新人专属元礼包[ | 查看](https://www.imooc.com/act/newcomer) __

[ ![](/static/img/article/article-logo.png?v=1) ![](/static/img/article/article-desc.png) ](/article)

[写文章](/article/publish)

__

为了账号安全，请及时绑定邮箱和手机[立即绑定](/user/setbindsns)

[ ](javascript:;)

[首页](https://www.imooc.com) __[手记](/article) __ 在Centos和Redhat上安装Docker

  * 145

102

分享

#  在Centos和Redhat上安装Docker

标签：

[Java](/article/tag/3) [Docker](/article/tag/73) [Kubernetes](/article/tag/105)

[收藏](javascript: "收藏")

**1\. 前置条件**

  * 64-bit 系统
  * kernel 3.10+
**1.检查内核版本，返回的值大于3.10即可。**



    $ uname -r


**2\. 使用 sudo 或 root 权限的用户登入终端。**

**3\. 卸载旧版本(如果安装过旧版本的话)**


    $ yum remove docker \
                 docker-client \
                 docker-client-latest \
                 docker-common \
                 docker-latest \
                 docker-latest-logrotate \
                 docker-logrotate \
                 docker-engine


**4\. 安装需要的软件包**


    #yum-util提供yum-config-manager功能
    #另外两个是devicemapper驱动依赖的
    $ yum install -y yum-utils \
      device-mapper-persistent-data \
      lvm2


**5\. 设置yum源**


    $ yum-config-manager \
        --add-repo \
        https://download.docker.com/linux/centos/docker-ce.repo


**6\. 安装docker**

_**6.1. 安装最新版本**_


    $ yum install -y docker-ce


_**6.2. 安装指定版本**_


    #查询版本列表
    $ yum list docker-ce --showduplicates | sort -r
    已加载插件：fastestmirror, langpacks
    已安装的软件包
    可安装的软件包
     * updates: mirrors.163.com
    Loading mirror speeds from cached hostfile
     * extras: mirrors.163.com
    docker-ce.x86_64            17.09.1.ce-1.el7.centos            docker-ce-stable
    docker-ce.x86_64            17.09.0.ce-1.el7.centos            docker-ce-stable
    ...
    #指定版本安装(这里的例子是安装上面列表中的第二个)
    $ yum install -y docker-ce-17.09.0.ce


**7\. 启动docker**


    $ systemctl start docker.service


**8\. 验证安装是否成功(有client和service两部分表示docker安装启动都成功了)**


    $ docker version
    Client:
     Version:      17.09.0-ce
     API version:  1.32
     Go version:   go1.8.3
     Git commit:   afdb6d4
     Built:        Tue Sep 26 22:41:23 2017
     OS/Arch:      linux/amd64

    Server:
     Version:      17.09.0-ce
     API version:  1.32 (minimum version 1.12)
     Go version:   go1.8.3
     Git commit:   afdb6d4
     Built:        Tue Sep 26 22:42:49 2017
     OS/Arch:      linux/amd64
     Experimental: false


# What’s Next?

想学习更多docker的进阶知识，以及k8s等服务编排工具的实战。快去看看慕课网的实战课程吧！
[《Docker+k8s微服务容器化实践》](https://coding.imooc.com/class/198.html?mc_marking=8b170ca27cd52bfc812a909ebfddb2a3&mc_channel=shouji)

点击查看更多内容

_145_ 人点赞

若觉得本文不错，就分享一下吧！

评论加载中...

作者其他优质文章

__正在加载中

  * 145
  *   * 收藏
  *

感谢您的支持，我会继续努力的～

扫码打赏，你说多少就多少

![]() ![]()

赞赏金额会直接到老师账户

支付方式

打开微信扫一扫，即可进行扫码打赏哦

今天注册有机会得

100积分直接送

付费专栏免费学

大额优惠券免费领

[立即参与](javascript:;) [放弃机会](javascript:;)

[点击
抽奖](javascript:;)

慕课手记新用户专享福利

恭喜你，你的运气太好了，居然抽中了 100个积分！

恭喜你，抽中了价值  元的专栏 ！

太棒了，  直接落到你账户里！

积分商城里的罗技鼠标、机械键盘、
Kindle 阅读器、小米平衡车
Apple iPad （10.2英寸）、大额优惠券
在等着你去兑换了噢

作者：

[](javascript:;) 免费赠送

兑换码：1111222211 [复制](javascript:;)

优惠券可用于购买实战课、体系课
无门槛使用

[先去看看，有什么好东西](https://www.imooc.com/mall/index) [马上兑换](https://order.imooc.com/ma) [我爱学习，选课去](https://coding.imooc.com)



[ __ 微信客服 购课补贴
联系客服咨询优惠详情 ](javascript:void\(0\)) [ __ 帮助反馈 ](/help) [ __ APP下载 慕课网APP
您的移动学习伙伴 ](https://www.imooc.com/mobile/app) [ __ 公众号 扫描二维码
关注慕课网微信公众号 ](javascript:void\(0\)) [ __ 返回顶部 ](javascript:void\(0\))

举报

0/150

提交

取消
