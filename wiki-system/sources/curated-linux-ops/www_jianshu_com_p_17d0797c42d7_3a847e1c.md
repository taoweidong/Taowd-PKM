---
source: "http://www.jianshu.com/p/17d0797c42d7"
title: "git在github远程仓库的克隆和上传使用教程 - 简书"
fetched_at: "2026-10-05 15:36:13"
---

最近公司要做一个资产管理软件后台工程创建出来，用eclipse、用git做一下版本控制。

#### Git库中由三部分组成

Git 仓库就是那个.git 目录，其中存放的是我们所提交的文档索引内容，Git 可基于文档索引内容对其所管理的文档进行内容追踪，从而实现文档的版本控制。.git目录位于工作目录内。
1） 工作目录：用户本地的目录；
2） Index（索引）：将工作目录下所有文件（包含子目录）生成快照，存放到一个临时的存储区域，Git 称该区域为索引。
3） 仓库：将索引通过commit命令提交至仓库中，每一次提交都意味着版本在进行一次更新。

#### git命令系统安装

  1. 下载git控制台, 选择操作系统对应的版本下载；
  2. 运行下载的安装程序, 除安装路径外, 其余安装选项一律按默认值即可。

#### git命令行系统启动

安装完成后,在开始菜单中有三个快捷方式可选,分别是:
git gui: 图形化管理系统, 比较简陋, 不推荐使用；
git bash: linux风格控制台系统, 支持的命令全面, 推荐使用 (需要注意,少量命令和windows不同,如ls,dir)；
git cmd: windows风格控制台系统, 不支持ssh相关命令, 完成ssh key创建后可以使用该模式替代 git bash；

#### git 创建用于远程访问项目仓库的ssh key

  1. 启动 git bash, 如下图:



  2. 输入 ssh-keygen,回车, 记住括号中的路径,如下图:



  3. 继续输入3个回车, 完成key创建，最后得到了两个文件：id_rsa和id_rsa.pub；



密钥id_rsa.pub

4.github添加SSH keys;
将id_rsa.pub里面的内容复制下来，在github上的settings里面找到 SSH and GPG keys，将其粘贴到key即可，title唯一即可随便填，建议写有意义的;
具体过程如图：



点击settings

点击New SSH key

最后点击Add SSH key

输入完登录密码会看到如图，但工作还没结束！！！

#### 测试

在Git Bash控制台上测试一下，输入：ssh -T [git@github.com](https://link.jianshu.com?t=mailto:git@github.com)

选择yes

只要看到最后一行Hi wqcreed! You've successfully authenticated, but GitHub does not provide shell access.
说明验证成功了





发现红线部分发生变化，说明已经成功建立连接，可以进行克隆和上传文件了。

#### 创建库

1、创建一个新的git库



点击New repository

2、根据你的项目需求填写相应内容



点击Create repository

这就已经创建好了一个Test.git仓库；



3、点击“Clone or download”,复制：[git@github.com](https://link.jianshu.com?t=mailto:git@github.com):wqcreed/Test.git，后面有用；

#### 克隆仓库到本地

1、找个自己工作目录下，空白处右键选择“Git Bash Here”；
输入命令： git clone [git@github.com](https://link.jianshu.com?t=mailto:git@github.com):wqcreed/Test.git
能看到后面就是刚才复制的SSH地址，看到如下图所示，就可以到自己工作目录下看到库文件克隆到本地了。


此时能看到Test仓库啦

命令cd Test进入仓库

2、上传添加文件到仓库，依次输入以下命令；


    $ git add .                                       这个点不要忘了！
    $ git commit -m "test log"                        上传日志
    $ git push origin master                          推送到GitHub仓库


成功

此时就可以到GitHub仓库看看有没有这个 测试文档.txt

OK

git的使用还有很多需要学习，我也是只掌握一点皮毛，廖雪老师的[Git教程](https://link.jianshu.com?t=http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)挺不错的，推荐大家学习！如有什么问题请多多批评指教，谢谢！！！
