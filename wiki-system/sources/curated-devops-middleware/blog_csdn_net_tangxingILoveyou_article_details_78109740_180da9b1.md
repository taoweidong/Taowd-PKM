---
source: "https://blog.csdn.net/tangxingILoveyou/article/details/78109740"
title: "Jenkins自动部署Maven 多个子项目_jenkins 多个项目构成一个-CSDN博客"
fetched_at: "2026-10-05 15:30:05"
---

# Jenkins自动部署Maven 多个子项目

最新推荐文章于 2026-07-18 15:50:05 发布

原创 最新推荐文章于 2026-07-18 15:50:05 发布 · 1.1w 阅读

· ![](https://csdnimg.cn/release/blogv2/dist/pc/img/newHeart2023Active.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/newHeart2023Black.png) 1 

· ![](https://csdnimg.cn/release/blogv2/dist/pc/img/tobarCollect2.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/tobarCollectionActive2.png) 4  ·

本内容遵循CC 4.0 BY-SA版权协议

版权声明：本文为博主原创文章，遵循[ CC 4.0 BY-SA ](http://creativecommons.org/licenses/by-sa/4.0/)版权协议，转载请附上原文出处链接和本声明。 

·

收录于

![](https://i-blog.csdnimg.cn/columns/default/20201014180756925.png?x-oss-process=image/resize,m_fixed,h_224,w_224) Jenkins

当前文章被收录于：

[ ![](https://i-blog.csdnimg.cn/columns/default/20201014180756925.png?x-oss-process=image/resize,m_fixed,h_224,w_224) ](https://blog.csdn.net/tangxingiloveyou/category_7052321.html)

[ Jenkins ](https://blog.csdn.net/tangxingiloveyou/category_7052321.html "Jenkins")

_4_ 篇文章 _0_ 人学习

订阅专栏 [查看详情](https://blog.csdn.net/tangxingiloveyou/category_7052321.html)

当前文章被以下社区和专栏收录：

![](https://i-operation.csdnimg.cn/images/a7311a21245d4888a669ca3155f1f4e5.png)本文介绍了一次使用Jenkins进行应用部署过程中遇到的问题及解决办法。首次部署成功，但在二次部署时出现错误。通过修改Tomcat配置文件解决了该问题。 

AI 驱动代码审查实战

Claude code-review 插件深度解析，把 AI 智能审查接进 CI/CD 流水线

[一键订阅](https://blog.csdn.net/zhangmeijia5/article/details/159392877?utm_source=blog_codereview_top_top&spm=1001.2101.3001.11781)

一、打开Jenkins管理页面   
![这里写图片描述](https://img-blog.csdn.net/20170927100123612?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

二、填写配置信息   
![这里写图片描述](https://img-blog.csdn.net/20170927100151104?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![这里写图片描述](https://img-blog.csdn.net/20170927100204751?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![这里写图片描述](https://img-blog.csdn.net/20170927100215445?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

备注：   
1。修改Tomcat文件夹（conf）下面的tomcat-users.xml文件。   
![这里写图片描述](https://img-blog.csdn.net/20170927100224897?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)   
2.问题描述：第一次部署没有问题，第二次部署报错，错误如下：

解决办法：conf=>context.xml文件下面添加如下配置（）   
![这里写图片描述](https://img-blog.csdn.net/20171219160114031?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

3、服务器IP填写问题；   
![这里写图片描述](https://img-blog.csdn.net/20180102105133644?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFuZ3hpbmdJTG92ZXlvdQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

AI 驱动代码审查实战

Claude code-review 插件深度解析，把 AI 智能审查接进 CI/CD 流水线

[一键订阅](https://blog.csdn.net/zhangmeijia5/article/details/159392877?utm_source=blog_codereview_top_bottom&spm=1001.2101.3001.11782)

![](https://csdnimg.cn/release/blogv2/dist/pc/img/vip-limited-close-newWhite.png)

确定要放弃本次机会？ 

福利倒计时

_:_ _:_

![](https://csdnimg.cn/release/blogv2/dist/pc/img/vip-limited-close-roup.png) 立减 ¥

普通VIP年卡可用

[立即使用](https://mall.csdn.net/vip)

[![](https://profile-avatar.csdnimg.cn/ff65bdea2f854906b2d8972722fab786_tangxingiloveyou.jpg!1) 星光之微  ](https://blog.csdn.net/tangxingILoveyou)

[关注](javascript:;) 关注

  * ![](https://csdnimg.cn/release/blogv2/dist/pc/img/tobarThumbUpactive.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/like-active.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/like.png) 1 

点赞

  * ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/unlike-active.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/unlike.png)

踩

  * [ ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/collect-active.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/collect.png) ![](https://csdnimg.cn/release/blogv2/dist/pc/img/newCollectActive.png) 4  ](javascript:;)

收藏 

觉得还不错?  一键收藏  ![](https://csdnimg.cn/release/blogv2/dist/pc/img/collectionCloseWhite.png)

  * ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/comment.png) 0 

评论

  * [ ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/share.png) 分享 ](javascript:;)

复制链接

分享到 QQ

分享到新浪微博

![](https://csdnimg.cn/release/blogv2/dist/pc/img/share/icon-wechat.png)扫一扫 

  * ![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/more.png)

![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/report.png) 举报

![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/report.png) 举报




专栏目录

[ _Jenkins_ _自动_ 化 _部署_ _Maven_ _项目_ ](https://loveddz.blog.csdn.net/article/details/148460646)

[Java老兵的后端进阶与AI前沿探索之路。](https://blog.csdn.net/weixin_45626288)

06-05 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 2087 

[ 本文详细介绍了使用 _Jenkins_ _自动_ 化 _部署_ _Maven_ _项目_ 的完整流程。主要内容包括：环境准备（JDK、 _Maven_ 、Docker）、 _Jenkins_ 插件安装（Gitee、 _Maven_ 、Docker等）、Gitee代码仓库连接配置、 _Maven_ _项目_ 创建与Git源码管理设置，以及关键的Docker构建 _部署_ 步骤（包含镜像构建、容器启动等shell脚本）。文章还提供了高级Pipeline方案和常见问题解决方案，如权限配置、镜像版本管理和敏感信息保护，并建议后续可集成Kubernetes、SonarQube等技术扩展功能。 ](https://loveddz.blog.csdn.net/article/details/148460646)

0 条评论 

写评论

[ _Jenkins_ 安装及 _自动_ _部署_ _Maven_ _项目_ ](https://blog.csdn.net/iamniconico/article/details/82023173)

[Nico专栏](https://blog.csdn.net/iamniconico)

08-24 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 3万+ 

[ 一、环境配置 OS版本 [root@VM_0_11_centos /]# rpm -qa | grep centos-release centos-release-7-4.1708.el7.centos.x86_64 Java版本 [root@VM_0_11_centos /]# java -version openjdk version &quot;1.8.0_181&quot; OpenJ... ](https://blog.csdn.net/iamniconico/article/details/82023173)

[ _jenkins_ 构建 _部署_ 多工程 _项目_ ](https://blog.csdn.net/qq_37936542/article/details/104793325)

[飞翔的鸡肉](https://blog.csdn.net/qq_37936542)

03-11 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 4011 

[ 刚接触 _jenkins_ 的时候， _项目_ 构建和 _部署_ 用的是单个 _maven_ _项目_ ，这次需要 _部署_ _多个_ _maven_ _项目_ ， _项目_ 之间彼此依赖，无形中增加了 _部署_ 的难度，特此做以记录 前提：多 _项目_ 介绍 主工程，依赖模块工程、公共模块、父工程 模块工程，依赖公共模块、父工程 公共模块，依赖父工程 从模块之间的关系，我们可以大致知道使用 _jenkins_ 构建顺序为 父工程 >> 公共模块 &... ](https://blog.csdn.net/qq_37936542/article/details/104793325)

[ CentOS 使用 _jenkins_ _自动_ 化 _部署_ _项目_ SpringBoot _Maven_ Github ](https://blog.csdn.net/qq_41727666/article/details/121398007)

[夏至是个程序媛](https://blog.csdn.net/qq_41727666)

11-18 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1769 

[ 文章目录背景step1 在服务器上下载工具已存在 ssh、vim、jdk、yum下载 _maven_ 3.8.3下载并配置 git 1.8.3.1step2 在服务器上下载 jetkinsstep3 在服务器上运行 jetkins1 运行 _jenkins_ 2 访问 _jenkins_ , 解决报错1 换源 update-center2 解决 unable to find valid certification, PKIX path building failed, SSLHandshakeException 等报错3  ](https://blog.csdn.net/qq_41727666/article/details/121398007)

[ 高效使用 _Jenkins_ ：同时上线 _多个_ _项目_ 的实践 ](https://moxiao.blog.csdn.net/article/details/124927297)

[漠效的博客](https://blog.csdn.net/GX_1_11_real)

05-24 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 5011 

[ 前言 如果是初学者或公司上线的 _项目_ 少节奏慢时，大多数的工作人员都是 _部署_ 和使用 _一个_ _jenkins_ ，满足要求即可。但是当你所在的公司有很多的上线服务(例如springboot等微服务架构的服务)或者很多的分站，短时间内要求进行大量上线，如果你要是还简单的使用 _一个_ _jenkins_ ,就会出现忙不过来的问题.同一台 _jenkins_ 上进行的服务过多，还会导致服务器负载过高，拖慢上线速度或超时导致上线失败。于是，我们要想办法加大 _jenkins_ 的并发工作。 下面介绍一些很实用的操作， _Jenkins_ 怎么加快工作/发布效率？  ](https://moxiao.blog.csdn.net/article/details/124927297)

[ _Jenkins_ 多模块打包 _部署_ ](https://blog.csdn.net/xyz9353/article/details/111451866)

[永无止境](https://blog.csdn.net/xyz9353)

07-31 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 4195 

[ 文章目录脚本 mall-docker-start.sh脚本修改mall-admin 打包mall-portal 打包mall-search 打包 脚本 mall-docker-start.sh docker stop mysql echo '----stop mysql container----' docker rm mysql echo '----rm mysql container----' docker rmi `docker images | grep none | awk '{print $3} ](https://blog.csdn.net/xyz9353/article/details/111451866)

[ _Jenkins_ 构建:多 _项目_ 构建，1个Multijob _项目_ 按顺序执行其它job ](https://blog.csdn.net/fen_fen/article/details/115333278)

[fen_fen的专栏](https://blog.csdn.net/fen_fen)

03-30 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 6839 

[ _Jenkins_ 构建：多 _项目_ 构建，1个Multijob _项目_ 按顺序执行其它job ](https://blog.csdn.net/fen_fen/article/details/115333278)

[ _jenkins_ _多个_ _项目_ 之间串并联执行 ](https://blog.csdn.net/sunsgne_AC/article/details/80098231)

[sunsgne_AC的专栏](https://blog.csdn.net/sunsgne_AC)

04-26 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1万+ 

[ 在现实场景中可能会出现这么一种情况就是 _一个_ 分布式的 _项目_ _部署_ 测试的时候需要发布顺序，后面发布的依赖于前面发布的，那么 _一个_ 分布式的 _项目_ 就会出现如下拓扑图的情况这样的话就可以建立 _一个_ _Jenkins_ 的MultiJob ，将相应的job加进来，不同的任务顺序执行，相同任务中的job并发执行。那么下面我们就建立 _一个_ multijob（2）对该MultiJob类型的任务进行配置：在构建标签下： “增加构建步骤”... ](https://blog.csdn.net/sunsgne_AC/article/details/80098231)

[ 腾讯混元3D世界模型2.0实战：从AI生成到Unity/UE引擎集成全指南 最新发布 ](https://blog.csdn.net/cnracht8153/article/details/100357528)

[cnracht8153的博客](https://blog.csdn.net/cnracht8153)

07-18 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 630 

[ 生成式AI正在重塑3D内容创作流程，其核心原理是通过大语言模型理解自然语言描述，并驱动多阶段生成流水线 _自动_ 创建3D资产与场景。这项技术为游戏开发、虚拟仿真和数字孪生领域带来了革命性的效率提升，能够将传统需要数周的美术协作流程压缩至几分钟。在实际应用中，开发者需要掌握本地环境 _部署_ 、模型推理优化以及生成资产与主流游戏引擎的集成工作流。本文以腾讯开源的混元3D世界模型为例，详细解析如何将AI生成的场景通过插件高效导入Unity和Unreal Engine，并针对光照烘焙、材质调整、性能优化等工程实践问题提供解决方 ](https://blog.csdn.net/cnracht8153/article/details/100357528)

[ _Jenkins_ 中使用Git和 _Maven_ 之 _多个_ _项目_ ](https://blog.csdn.net/fduffyyg/article/details/83585106)

[fduffyyg的博客](https://blog.csdn.net/fduffyyg)

10-31 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1187 

[ 分享一下我老师大神的人工智能教程！零基础，通俗易懂！http://blog.csdn.net/jiangjunshow也欢迎大家转载本篇文章。分享知识，造福人民，实现我们中华民族伟大复兴！&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1.应用Aggrega ](https://blog.csdn.net/fduffyyg/article/details/83585106)

[ _jenkins_ 用流水线Pipeline构建 _maven_ _项目_ 实例 ](https://feixiang.blog.csdn.net/article/details/119649984)

[秃了也弱了](https://blog.csdn.net/A_art_xiang)

08-12 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1308 

[ node { def workspace = pwd() def gitUrl="https://gitee.com/y_project/RuoYi.git" def gitBranch="master" def _maven_ Path="/app/_jenkins_ /apache-_maven_ -3.8.1" def subp = ['ruoyi-common','ruoyi-system','ruoyi-framework','ruoyi-quartz'. ](https://feixiang.blog.csdn.net/article/details/119649984)

[ 时间卷积网络(TCN)：结构+pytorch代码 热门推荐 ](https://blog.csdn.net/leon_winter/article/details/100124146)

[Leon_winter的博客](https://blog.csdn.net/Leon_winter)

08-29 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 11万+ 

[ 文章目录TCNTCN结构1-D FCN的结构因果卷积(Causal Convolutions)膨胀因果卷积(Dilated Causal Convolutions)膨胀非因果卷积(Dilated Non-Causal Convolutions)残差块结构pytorch代码讲解 TCN TCN(Temporal Convolutional Network)是由Shaojie Bai et al.... ](https://blog.csdn.net/leon_winter/article/details/100124146)

[ _Jenkins_ 安装及使用 （ _Jenkins_ _部署_ _Maven_ _项目_ 、 _Jenkins_ _部署_ Vue _项目_ ） ](https://blog.csdn.net/achi010/article/details/93708768)

[Z](https://blog.csdn.net/achi010)

06-26 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 5万+ 

[ _Jenkins_ 安装 _部署_ 及使用。包括 _Jenkins_ _部署_ Vue _项目_ ， _Jenkins_ _部署_ _Maven_ _项目_ 。 ](https://blog.csdn.net/achi010/article/details/93708768)

[ Java电商秒杀系统性能优化(一)——电商秒杀系统框架回顾 ](https://blog.csdn.net/ghw15221836342/article/details/100027024)

[ghw15221836342的博客](https://blog.csdn.net/ghw15221836342)

08-23 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 2648 

[ 电商秒杀系统框架回顾 _项目_ 简介外部依赖框架回顾 _项目_ 要点 _项目_ 中存在的问题小结 课程是免费的，课程地址如下：SpringBoot搭建电商秒杀 _项目_ ，课程真的很棒，作者的思路很清晰，建议各位读者可以跟着视频练习一下这个 _项目_ ； _项目_ 简介 通过SpringBoot快速搭建的前后端分离的电商基础秒杀 _项目_ 。 _项目_ 通过应用领域驱动型的分层模型设计方式去完成：用户otp注册、登陆、查看、商品列表、进入商品详情以及倒计时秒... ](https://blog.csdn.net/ghw15221836342/article/details/100027024)

[ _Jenkins_ 学习笔记（一）：Docker安装 _Jenkins_ 及 _自动_ _部署_ _Maven_ _项目_ ](https://blog.csdn.net/weixin_44249490/article/details/103687307)

[潇洒哥的博客](https://blog.csdn.net/weixin_44249490)

12-25 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1万+ 

[ _Jenkins_ 安装Docker下安装 _Jenkins_ 镜像加速器拉取镜像运行容器合理的创建标题，有助于目录的生成如何改变文本的样式插入链接与图片如何插入一段漂亮的代码片生成 _一个_ 适合你的列表创建 _一个_ 表格设定内容居中、居左、居右SmartyPants创建 _一个_ 自定义列表如何创建 _一个_ 注脚注释也是必不可少的KaTeX数学公式新的甘特图功能，丰富你的文章UML 图表FLowchart流程图导出与导入导出导入 Do...... ](https://blog.csdn.net/weixin_44249490/article/details/103687307)

[ 关于 _Jenkins_ _自动_ 化 _部署_ _Maven_ _项目_ : ](https://blog.csdn.net/gzx233/article/details/140737747)

[gzx233的博客](https://blog.csdn.net/gzx233)

07-27 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1888 

[ 测试工程:_Jenkins_ _自动_ 化 _部署_ _maven_ _项目_ 全流程 ](https://blog.csdn.net/gzx233/article/details/140737747)

[ 2026四款AI原生IDE实测：Trae、Qoder、CodeBuddy、Cursor能力边界深度解析 ](https://blog.csdn.net/ctk87443/article/details/100244353)

[ctk87443的博客](https://blog.csdn.net/ctk87443)

06-15 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1091 

[ AI原生IDE正从代码编辑器演进为开发者智能工作流中枢，其核心在于对上下文理解、AST编辑意图建模与多模态任务调度的工程化实现。区别于传统插件式AI辅助，真正的AI原生IDE需具备知识库嵌入、符号图索引、操作链固化等底层能力，从而支撑Figma转码、N+1查询修复、跨语言迁移等复杂场景。Trae强调中文语境与企业规范的强绑定，Qoder聚焦AST级编辑轨迹预测，CodeBuddy通过IDE/插件/CLI三态划分控制权边界，Cursor则以云端Agent实现开发任务的时空并行。本文基于真实 _项目_ 压测，揭示免费版 ](https://blog.csdn.net/ctk87443/article/details/100244353)

[ _jenkins_ _部署_ _Maven_ 和NodeJS _项目_ ](https://blog.csdn.net/henanchenxuyuan/article/details/142626126)

[henanchenxuyuan的博客](https://blog.csdn.net/henanchenxuyuan)

09-29 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 3618 

[ 每 _一个_ 开发工具(IDE)都有自己不同的 _项目_ 结构，它们互相之间不通用。比如我再 eclipse 中创建的目录，无法在 idea 中进行使用，这就造成了很大的不方便。 _Maven_ 提供了一套标准化的 _项目_ 结构，所有的 IDE 使用 _Maven_ 构建的 _项目_ 完全一样，所以 IDE 创建的 _Maven_ _项目_ 可以通用。 _Maven_ 是 Apache 软件基金会组织维护的一款 _自动_ 化构建工具，专注服务于 ava 平台的 _项目_ 构建和 依赖管理。 _Maven_ 这个单词的本意是:专家，内行。读音是['merv(ə)n]或['mevn] ](https://blog.csdn.net/henanchenxuyuan/article/details/142626126)

[ 全面解析：时延扩展与相干带宽、多普勒扩展与相干时间——无线通信基础 ](https://blog.csdn.net/qq_34070723/article/details/100119767)

[king阿金](https://blog.csdn.net/qq_34070723)

08-29 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 4万+ 

[ 时延扩展与相干带宽 多径时延扩展与多径衰落 接收机所接收到的信号是通过不同的直射、反射、折射等路径到达接收机。由于电波通过各个路径的距离不同， 因而各条路径中发射波的到达时间不同，造成多径时延扩展。距离不同所以到达接收机的相位也不相同，不同相位的 _多个_ 信号在接收端叠加， 如果同相叠加则会使信号幅度增强， 而反相叠加则会削弱信号幅度。 这样，接收信号的幅度将会发生急剧变化，就会产生多径衰落。 ... ](https://blog.csdn.net/qq_34070723/article/details/100119767)

[ Linux快速安装 _Jenkins_ 一键 _部署_ _Maven_ _项目_ ](https://lingbomanbu.blog.csdn.net/article/details/139940734)

[lingbomanbu_lyl的博客](https://blog.csdn.net/lingbomanbu_lyl)

07-29 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 2628 

[ 以上的场景是 _Jenkins_ 和应用服务在同一台服务器上，如果应用服务不在同一台服务器上，可以通过插件来实现远程构建和 _自动_ 化 _部署_ ，具体后面章节再做详细介绍。 ](https://lingbomanbu.blog.csdn.net/article/details/139940734)

[ linux之 _Jenkins_ _自动_ 化 _项目_ _部署_ ](https://blog.csdn.net/buzhi______/article/details/142217201)

[buzhi______的博客](https://blog.csdn.net/buzhi______)

09-13 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 4124 

[ CI/CD CI (continuous integration-CI) -- 持续集成 代码合并，构建， _部署_ ，测试都在一起，不断的执行的过程，并对结构反馈。 CD（continuous Deloyments）-- 持续交付 把代码 _部署_ 到测试环境，预生产环境。 CD（continous Delivery）-- 持续 _部署_ 将最终的产品发布到生产环境，给用户使用。 实现持续集成/持续发布的产品 开发(git) -->git远程仓 ](https://blog.csdn.net/buzhi______/article/details/142217201)

[ DAVIS前言：事件相机资料调研 ](https://blog.csdn.net/qq_29797957/article/details/100576373)

[Ian的博客](https://blog.csdn.net/qq_29797957)

09-06 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 4101 

[ Event-Camera 资料集锦 1\. 官网资料 假设了你买了事件相机，就可以在以下几个链接了解相关的参数和gui界面安装，如果不喜欢gui界面安装，可以第2节，安装相关的源码驱动。 DVS/DAVIS产品说明 等相关产品的软硬件介绍。 iniVation DV教程文档 给出在不同平台下的dvs-gui界面，可按照其说明进行相应的操作。 另外，Neuromorphic vision com... ](https://blog.csdn.net/qq_29797957/article/details/100576373)

[ _Jenkins_ _自动_ _部署_ _Maven_ _项目_ 详细教程 ](https://blog.csdn.net/Ukulilion/article/details/129399033)

[Ukulilion的博客](https://blog.csdn.net/Ukulilion)

03-08 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 1万+ 

[ _Jenkins_ 从安装到使用，详细介绍 _Jenkins_ 拉取代码、编译 _部署_ 、流水线搭建等每 _一个_ 步骤，已排雷。 ](https://blog.csdn.net/Ukulilion/article/details/129399033)

[ lwip-2.0.3 ](https://download.csdn.net/download/strugglelg/10029269)

[ lwip是瑞典计算机科学院(SICS)的Adam Dunkels 开发的 _一个_ 小型开源的TCP/IP协议栈。实现的重点是在保持TCP协议主要功能的基础上减少对RAM 的占用。 ](https://download.csdn.net/download/strugglelg/10029269)

[ CentOS7安装 _Jenkins_ _自动_ 化 _部署_ _maven_ _项目_ ](https://blog.csdn.net/weixin_43839635/article/details/140433232)

[weixin_43839635的博客](https://blog.csdn.net/weixin_43839635)

07-16 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 3035 

[ #_jenkins_ _部署_ _maven_ _项目_ ](https://blog.csdn.net/weixin_43839635/article/details/140433232)

[ _jenkins_ \+ docker _自动_ 化 _部署_ _maven_ _项目_ ](https://blog.csdn.net/weixin_43909881/article/details/118277543)

[Ying的博客](https://blog.csdn.net/weixin_43909881)

09-11 ![](https://csdnimg.cn/release/blogv2/dist/pc/img/readCountWhite.png) 2761 

[ 添加凭据 有两种方式，第一种直接用git的账号密码获取代码 第二种用SSH私钥和账号获取代码 ssh-keygen -t rsa 然后会要输入保存地址，我这里保存在/root/id_rsa，需要保存在其他地方自行更改 然后要输入密码，可以为空 生成完毕后，会产生两个文件id_rsa和id_rsa.pub，带.pub的是公钥，把这个文件的内容复制到git上，我用的是gitee，github也一样 因为我只需要 _jenkins_ 能够拉取代码就够了，所以在仓库上添加公钥，而不是git账户上添加全局的公钥，... ](https://blog.csdn.net/weixin_43909881/article/details/118277543)

[ IMSL CNL 7.0.0 (x86-64)Crack ](https://download.csdn.net/download/code_my_life/10018281)

[ IMSL CNL 7.0.0 (x86-64)Crack intel的算法库破解文件，这是C++版本的破解文件 ](https://download.csdn.net/download/code_my_life/10018281)
