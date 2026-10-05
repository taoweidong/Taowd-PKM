---
source: "https://www.cnblogs.com/frankyou/p/5283539.html"
title: "RabbitMQ与AMQP协议详解 - FrankYou - 博客园"
fetched_at: "2026-10-05 15:29:45"
---

**1\. 消息队列的历史**   
了解一件事情的来龙去脉，将不会对它感到神秘。让我们来看看消息队列（Message Queue）这项技术的发展历史。

Message Queue的需求由来已久，80年代最早在金融交易中，高盛等公司采用Teknekron公司的产品，当时的Message queuing软件叫做：the information bus（TIB）。 TIB被电信和通讯公司采用，路透社收购了Teknekron公司。之后，IBM开发了MQSeries，微软开发了Microsoft Message Queue（MSMQ）。这些商业MQ供应商的问题是厂商锁定，价格高昂。2001年，Java Message queuing试图解决锁定和交互性的问题，但对应用来说反而更加麻烦了。

于是2004年，摩根大通和iMatrix开始着手Advanced Message Queuing Protocol （AMQP）开放标准的开发。2006年，AMQP规范发布。2007年，Rabbit技术公司基于AMQP标准开发的RabbitMQ 1.0 发布。

目前RabbitMQ的最新版本为3.5.7，基于AMQP 0-9-1。   
RabbitMQ采用Erlang语言开发。Erlang语言由Ericson设计，专门为开发concurrent和distribution系统的一种语言，在电信领域使用广泛。OTP（Open Telecom Platform）作为Erlang语言的一部分，包含了很多基于Erlang开发的中间件／库／工具，如mnesia／SASL，极大方便了Erlang应用的开发。OTP就类似于Python语言中众多的module，用户借助这些module可以很方便的开发应用。

**2\. AMQP messaging 中的基本概念**

  * **Broker** : 接收和分发消息的应用，RabbitMQ Server就是Message Broker。
  * **Virtual host** : 出于多租户和安全因素设计的，把AMQP的基本组件划分到一个虚拟的分组中，类似于网络中的namespace概念。当多个不同的用户使用同一个RabbitMQ server提供的服务时，可以划分出多个vhost，每个用户在自己的vhost创建exchange／queue等。
  * **Connection** : publisher／consumer和broker之间的TCP连接。断开连接的操作只会在client端进行，Broker不会断开连接，除非出现网络故障或broker服务出现问题。
  * **Channel** : 如果每一次访问RabbitMQ都建立一个Connection，在消息量大的时候建立TCP Connection的开销将是巨大的，效率也较低。Channel是在connection内部建立的逻辑连接，如果应用程序支持多线程，通常每个thread创建单独的channel进行通讯，AMQP method包含了channel id帮助客户端和message broker识别channel，所以channel之间是完全隔离的。Channel作为轻量级的Connection极大减少了操作系统建立TCP connection的开销。
  * **Exchange** : message到达broker的第一站，根据分发规则，匹配查询表中的routing key，分发消息到queue中去。常用的类型有：direct (point-to-point), topic (publish-subscribe) and fanout (multicast)。
  * **Queue** : 消息最终被送到这里等待consumer取走。一个message可以被同时拷贝到多个queue中。
  * **Binding** : exchange和queue之间的虚拟连接，binding中可以包含routing key。Binding信息被保存到exchange中的查询表中，用于message的分发依据。



概念图 - 1

概念图 - 2 

**3\. 典型的“生产／消费”消息模型**   
生产者发送消息到broker server（RabbitMQ）。在Broker内部，用户创建Exchange／Queue，通过Binding规则将两者联系在一起。Exchange分发消息，根据类型／binding的不同分发策略有区别。消息最后来到Queue中，等待消费者取走。

**4\. Exchange类型**   
Exchange有多种类型，最常用的是Direct／Fanout／Topic三种类型。

**Direct** （point 2 point 点对点模式）  
Message中的“routing key”如果和Binding中的“binding key”一致， Direct exchange则将message发到对应的queue中。

**Fanout** （多播模式）  
每个发到Fanout类型Exchange的message都会分到所有绑定的queue上去。

**Topic** （发布-订阅模式）  
根据routing key，及通配规则，Topic exchange将分发到目标queue中。

Routing key中可以包含两种通配符，类似于正则表达式：
    
    
    “#”通配任何零个或多个word
    “*”通配任何单个word

这里也推荐给想要了解RabbitMQ的同学一个网站，[http://tryrabbitmq.com](http://tryrabbitmq.com/) ，它提供在线RabbitMQ 模拟器，可以帮助理解Exchange／queue／binding概念。 

至此，我们对于消息队列的发展，RabbitMQ的产生，以及AMQP协议中的重要概念做了一个完整的介绍。
