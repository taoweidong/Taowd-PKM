---
type: concept
tags: [wiki, 优质博客, 学习资源, 微服务, 算法, 前端工程化, 收藏夹Ingest]
created: 2026-10-05
updated: 2026-10-05
source: "[[topics/browser-bookmarks]]"
---

# 优质博客与学习资源（收藏夹 Ingest · 第 2 批）

> 从浏览器收藏夹「优质博客」主题（共 47 条）Ingest 的精选学习资源。覆盖**微服务/分布式架构、算法/LeetCode、Python/前端工程化、技术文档与社区**四类。已抓取 9 篇核心文章并提炼要点，其余按主题归类描述（完整 URL 见 [[topics/browser-bookmarks]]）。

## 摘要

这是一份「长期值得回看」的技术博客/文档清单。与 [[概念:全栈后台管理系统]]（KontainKeeper）最相关的有三类：
- **微服务架构**：单体→微服务拆分、API 网关、服务治理、容器化（直接对应本项目 500 台规模 MQTT 重构）
- **前端权限**：Vue 登录与 RBAC 动态路由（与本项目前端鉴权思路一致）
- **容器/协调**：Docker、Zookeeper（对应本项目容器化部署 + 服务协调）

## 详情

### 一、微服务与分布式架构

**1. 微服务从设计到部署（oopsguy 译 Chris Richardson 电子书）** ✅已抓
- 单体应用弊端：启动慢、难扩展、难持续部署、技术栈绑定 → 微服务按业务拆小服务
- 每服务独立数据库（多语言持久化 polyglot persistence）；Y 轴拆分 + X/Z 轴扩展
- 优点：模块化、独立部署/扩展、团队自治；缺点：分布式复杂度、数据最终一致、部署复杂（需服务发现/编排）

**2. 微服务架构设计（PetterLiu）** ✅已抓
- 特征：组件化、松耦合、自治、去中心化（小服务 / 独立部署 / 独立演进 / 独立团队）
- 通信：同步 REST/RPC + 异步消息（最终一致、需幂等）；**API 网关**作统一入口
- 服务治理：注册发现、限流容错、监控日志；系统底座 = 日志/监控/消息总线/注册发现/部署
- 容器(Docker)与微服务天然契合（小、独立、环境一致、可复制扩容）

**3. 基于微服务的软件架构模式（简书）** ⚠️抓取失败（访问权限页）
- 已知为微服务架构模式经典综述，建议手动补读：https://www.jianshu.com/p/546ef242b6a3

**4. Chris Richardson 微服务系列·服务发现（DaoCloud）** ⚠️抓取失败（fetch error）
- 服务发现可行方案与实践案例，源：http://blog.daocloud.io/microservices-4/

**5. Zookeeper 简单介绍（邬兴亮）** ✅已抓
- 分布式协调服务：分布式锁、配置维护、组服务、通知/协调
- 数据模型 **Znode**（stat/data/children）；节点类型：临时/永久/顺序；**Watcher** 一次性触发
- 典型应用：**Master 选举**解决单点故障/双 Master 问题

**6. keepalived 工作原理与配置（outofmemory）** ⚠️抓取失败（403）
- 已知基于 **VRRP** 的高可用方案，用于 VIP 漂移/双机热备，源：http://outofmemory.cn/wiki/keepalived-configuration

**同主题其余资源（描述）**
- [Spring Cloud 中文网](https://springcloud.cc/) — 官方文档中文版
- [Spring Cloud 教程](https://github.com/forezp/SpringCloudLearning) — forezp 实战系列
- [Spring Cloud | 周立](http://www.itmuch.com/) — 周立（程序员 DD 同人）Spring Cloud 专家博客
- [Spring For All](http://www.spring4all.com/) — Spring 民间技术组织
- [Java 和微服务 第3部分：微服务通信](https://www.ibm.com/developerworks/cn/java/j-cn-java-and-microservice-3/index.html) — IBM 开发者works
- [Eureka 简介](https://www.cnblogs.com/wangdaijun/p/6851027.html) — 服务注册发现
- [mPaaS 简介](https://tech.antfin.com/docs/2/49549) — 蚂蚁金服移动开发平台
- [Transwarp 产品列表](http://www.transwarp.cn/product/tdh) — 星环 TDH 大数据平台

### 二、算法与 LeetCode

**7. 单调栈（OI Wiki）** ✅已抓
- 满足单调性的栈，只在一端进出；插入时弹出破坏单调性的元素
- 应用：POJ3250 Bad Hair Day；离线 RMQ（按右端点排序 + 二分）
- 习题：洛谷 P5788（模板）/ P1901（发射站）

**8. 十大经典排序算法（郭耀华）** ✅已抓
- 比较排序（冒泡/选择/插入/希尔/归并/快排/堆）与非比较（计数/桶/基数）
- 比较类平均 O(n²)~O(nlogn)；非比较更低但需额外空间、对数据分布有要求

**9. 动态规划·多重背包（弗兰克的猫）** ✅已抓
- 每种物品有数量上限 M[i]；递推 `ks(i,t)=max{ks(i-1,t-V[i]*k)+P[i]*k}`
- 优化：M[i]*V[i]≥T 当完全背包；否则枚举 k≤M[i]；可拆为 01 背包
- 同作者还有 01 背包/完全背包系列

**同主题其余资源（描述）**
- [labuladong 知乎](https://www.zhihu.com/people/fdl-72) — 算法/LeetCode 图解套路（高星）
- [负雪明烛 CSDN](https://blog.csdn.net/fuxuemingzhu) — 算法/LeetCode/考研机试
- [Grandyang 博客园](https://www.cnblogs.com/grandyang/) — LeetCode 题解
- [LeetCode 刷题视频·花花酱 Bilibili](https://space.bilibili.com/9880352) — 算法视频讲解

### 三、Python 与前端工程化

**10. Python 项目工程化开发指南（pyloong）** ✅已抓
- 流程：功能 → pylint/isort → pytest；commit 规范；PEP8
- 目录：`src/` + `tests/`；配置 `pyproject.toml`/`tox.ini`/`.pre-commit-config.yaml`
- 工具链：Poetry 打包、cookiecutter 初始化、isort/pylint/pytest/tox/mkdocs

**11. 手摸手，用 vue 撸后台·登录权限篇（花裤衩）** ✅已抓
- 登录：账号密码 → 后端返回 token → 存 cookie → token 拉 user_info(role)
- 权限：token 取 role → 动态算可访问路由 → `router.addRoutes` 动态挂载；前端页面级 + 后端请求级（token 校验）
- axios 拦截器统一塞 token；按钮级用 v-if；两步验证（OAuth2 第三方）
- ★ **与 KontainKeeper 前端 RBAC 思路完全一致**（token + 动态路由 + 后端鉴权）

**12. 什么是 Docker（知乎干货）** ✅已抓
- 容器 vs 虚拟机：容器共享 OS、更轻量（数 M）、秒级启动；docker 屏蔽环境差异（build once, run everywhere）
- 概念：dockerfile(源码)→image(可执行)→container(进程)；build/run/pull；底层 Namespace + cgroup
- ★ 与本项目**容器化部署（MQTT + 开源组件）**直接相关

**同主题其余资源（描述）**
- [廖雪峰官方网站](https://www.liaoxuefeng.com/) — Python/Java/Git/JS 国民级教程
- [Scala 教程·菜鸟](http://www.runoob.com/scala/scala-tutorial.html) — 菜鸟教程
- [Docker 部署 Django](https://pythondjango.cn/django/advanced/16-docker-deployment/) — 大江狗
- [uni-app 官网](https://uniapp.dcloud.io/quickstart) — 跨端开发框架
- [mpvue.com](http://mpvue.com/) — 美团 Vue 小程序框架
- [Cordova 中文网](http://cordova.axuer.com/docs/zh-cn/latest/) — 混合开发
- [Tencent/wepy](https://github.com/Tencent/wepy) — 小程序组件化框架
- [Vue.js SSR 指南](https://ssr.vuejs.org/zh/) — 服务端渲染官方
- [vue-element-admin 顶部菜单栏](https://blog.csdn.net/qq_36365860/article/details/120073481) — 后台菜单切换实践
- [Java 软件工程师简历](https://zhousiwei.gitee.io/cv/) / [anires 动态简历](https://gitee.com/zhousiwei/anires) — 简历模板
- [GitHub 2FA 中国认证及 TOTP](https://zhuanlan.zhihu.com/p/657035724) — 两步验证

### 四、技术文档 / 社区 / 个人博客

- [SegmentFault 思否](https://segmentfault.com/) — 技术问答社区
- [程序猿DD](http://blog.didispace.com/) — 纯皓，Spring Boot 实战（翟永超）
- [静觅·崔庆才](https://cuiqingcai.com/) — Python 爬虫权威博客
- [waylau (Way Lau)](https://github.com/waylau) — 多语言技术译文/开源
- [DaoCloud 博客](http://blog.daocloud.io/) — 容器/微服务
- [Alexia 博客园](http://www.cnblogs.com/lanxuezaipiao/) — 个人技术博客
- [花钱的年华 CSDN](http://blog.csdn.net/calvinxiu) — 阿里技术专家（架构/Java）
- [老赵点滴](http://blog.zhaojie.me/) — 赵劼，追求编程之美（.NET/函数式）
- [Hadoop 快速入门](http://hadoop.apache.org/docs/r1.0.4/cn/quickstart.html) — 官方中文
- [Quick Guide to Java Stack | Baeldung](http://www.baeldung.com/java-stack) — Java/Spring 高质量教程站

## 关联

- 来源索引：[[topics/browser-bookmarks]]（优质博客主题共 47 条，本页为精选归类）
- 上一批：[[concepts/curated-opensource-projects]]（开源项目脚手架，与前端/后端框架互补）
- 项目体系：[[entities/project-fullstack-admin]]、[[concepts/slowapi-rate-limiting]]

## 引用来源

- 各博客/文档站（见上文链接），核心 9 篇抓取于 2026-10-05
- 原始收藏：[[90-待整理与临时笔记/favorites_2026_10_5]]

## 变更记录

- 2026-10-05：第 2 批 Ingest「优质博客」主题 47 条。抓取 9 篇核心文章（微服务×2、算法×3、Python工程化、Vue权限、Docker、Zookeeper）并提炼要点；3 篇抓取失败（简书权限页 / daocloud fetch error / keepalived 403）已标注待补。
