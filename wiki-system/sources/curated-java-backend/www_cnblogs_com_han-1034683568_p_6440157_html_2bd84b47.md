---
source: "http://www.cnblogs.com/han-1034683568/p/6440157.html"
title: "Spring+SpringMVC+MyBatis整合基础篇（二）牛刀小试 - 程序员十三 - 博客园"
fetched_at: "2026-10-05 15:32:36"
---

## 前言

承接上文，该篇即为项目整合的介绍了。

废话不多说，先把源码和项目地址放上来，重点要写在前面。

项目展示地址，点这里[http://ssm-demo.13blog.site](http://ssm-demo.13blog.site/)，账号：admin 密码：123456

当然，也可以直接导入源码， [点击这里](http://download.csdn.net/download/zhenfengshisan/9765855)下载代码。

Github地址在这里：<https://github.com/ZHENFENG13>

从构思这个博客，一直到最终确定以这个项目为切入点，中间也是各种问题出现，毕竟是新人，所以也是十分的小心，修改代码以及搬上GitHub其实花了不少时间，但也特别的认真，不知道是怎么回事，感觉这几天的过程比逼死产品经理还要精彩和享受。

**或许是博客路上的第一站吧，有压力也有新奇，希望自己能坚持下去，也希望自己的博客质量越来越好。**

## 简介

本项目实现了一个简单的后台管理系统，可以作为ssm项目学习的脚手架，主要包含以下功能：

  * 管理员的注册功能，登录功能，删除功能。
  * 文章的增删改查功能，图片的增删改查功能。
  * 图片上传功能。
  * 多文本编辑器UEditor整合。

项目框架包括：

  * Spring
  * SpringMVC
  * MyBatis
  * 后台管理界面则使用easyui进行搭建

## 项目截图

###### Picture Page

![picture](https://raw.githubusercontent.com/ZHENFENG13/resource/master/images/2017-07-19/picture.png)

###### Login Page

![login](https://raw.githubusercontent.com/ZHENFENG13/resource/master/images/2017-07-19/login.png)

###### Main Page

![panel](https://raw.githubusercontent.com/ZHENFENG13/resource/master/images/2017-07-19/panel.png)

###### Article Page

![article](https://raw.githubusercontent.com/ZHENFENG13/resource/master/images/2017-07-19/article.png)

## 项目架构

ssm-demo为基础和优化篇的代码，项目架构也较为简单，为最基础的架构：

![架构简图](https://raw.githubusercontent.com/ZHENFENG13/resource/master/images/2017-08-05/ssm%E6%9E%B6%E6%9E%84%E5%9B%BE-%E7%AE%80%E7%89%88.png)

## 结语

**网站的持续运行需要各项基础设施的搭建，而服务期的续费和维护及各种配套服务的购买也需要一定的费用，希望朋友们给予一点支持，谢谢！**

**支付宝：![](http://resources.hanshuai.xin/person/zhifubao1.jpg)****微信支付：![](http://resources.hanshuai.xin/person/wxpay.jpg)**

源码地址和实际运行效果的展示地址都在上方，可以先看一下网站的实际内容，如果有兴趣再去看一下源码。

接下来的几篇会详细的介绍，希望大家提出问题，也希望大家给我这个博客园的新人一些建议。
