---
source: "https://blog.guizimo.com/archives/x36CnPAP"
title: "Obsidian 通过 Git 实现全平台自动同步 | 归子莫的博客"
fetched_at: "2026-10-05 15:44:46"
---

本文最后更新于 2025-04-01，请注意辨别文章的编写时间哦。

# Obsidian 通过 Git 实现全平台自动同步

最近为了多平台的同步本地文章，目前把 Markdown 的编辑器从 Typora 转移到了 Obsidian。Obsidian 比 Typora 的优势就是多了同步的功能，可以在多设备之间流转。

需要实现同步的设备有： Mac、Windows、Android、IOS 等四个平台。主要借助的是 Git 的能力，刚好可以实现版本的管理。

## Mac 端配置

### 新建仓库

新建一个仓库，这里我以 WorkSpaceMD 创建一个仓库，并在 Obsidian 中打开。

![WorkSpaceMD](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326165223661.png)

在新的仓库中导入一篇文章，这里我导入了之前写的一篇文章。

![导入一篇文章](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326165550848.png)

### 安装插件

在设置中找到第三方插件，选择关闭安全模式，关闭安全模式之后，就可以安装插件了。

![关闭安全模式](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326170715969.png)

找到 Git 插件并启用，注意不要找错了。

![ Git 插件](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326171041319.png)

启用之后可以重新启动一下软件，防止插件未启动生效。

### 创建 Git 仓库

在 Github 上创建同名仓库，当然可以使用自己搭建的 Git 服务器以及直接使用国内的 Gitee。注意我这里选择的是私有的库。

![创建同名仓库](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326171227570.png)

进入到本地仓库 WorkSpaceMD 的文件目录下，执行以下命令：


    git init  // 初始化 git 项目
    git remote add origin git@github.com:Guizimo/WorkSpaceMD.git // 添加远程仓库


添加 gitignore 配置，防止一些配置文件被提交上去了。（主要是不同设备的配置导致冲突，会影响自动同步）


     .idea
     .obsidian
     .vscode


首次提交通过命令推送。


     git commit -m "first commit"
     git push -u origin main


### Git 插件配置

打开自动同步的开关，我这里是把检查的时间间隔设置为了 5 分钟。

![打开自动同步的开关](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326172300196.png)

每次启动时立即拉取远程仓库，保持最新的内容。

![拉取远程仓库](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/image-20250326172327728.png)

## Windows 端配置

由于 Windows 端的配置大致和 Mac 是一致的，这里就讲一下大致的区别点。

### 拉取 Git 项目

由于带 Mac 端已经创建了 Git 项目，这里直接拉取远程的仓库代码，然后使用 Obsidian 打开就可以了，同样的需要安装 Git 插件以及相应的配置。


    git clone git@github.com:Guizimo/WorkSpaceMD.git // 拉取远程仓库


### 同步 Git 异常

在 Windows 时常会出现 Git 相关的报错，我这是 Github 的认证方式使用的是 SSH 的方式，目前是设置了密码，导致每次操作时都需要输入密码，导致插件的 Git 无法正常拉取和提交。这里可以把 SSH 的密码设置为空，就可以不用每次输入密码了。

## IOS 端配置

在了解过很多 IOS 端的配置后，看到很多都是使用了 Working Copy，使用 Working Copy 来实现手动同步远程 Git 仓库。 但是这种方案有两个缺点：1、Working Copy 关键功能是收费的；2、需要手动同步。因此还是想借助 Obsidian 的 Git 插件能力来实现自动同步。

### 创建仓库

在 IOS 端要先创建一个仓库，这里的名称还是叫 WorkSpaceMD 。

### 配置 iSH

iSH 是一个IOS 端的 Linux Shell 工具，我们用它来拉取 git 的远程仓库。

直接在 Apple Store下载 iSH


    apk update  // 更新软件包
    apk install git   // 安装 git


### 挂载目录

在 IOS 端找到 Obsidian 的目录，在 ISH 中挂载到相应的目录，主要是把远程的 Git 仓库连接到对应目录下。


    mount -t ios obsidian /mnt


此时会让你选择目录，选择 Obsidian 目录就好。


    cd /mnt/WorkSpaceMD


### 配置

配置 Git
​


    git config --global user.name "Guizimo"
    git config --global user.email "17680262548@163.com"
    git config --global --add safe.directory /mnt/WorkSpaceMD  // 添加安全目录


​
配置远程仓库


    git init   // 初始化 git​
    git branch -M main  // 调整分支为 main
    git remote add origin https://github.com/Guizimo/WorkSpaceMD.git  // 添加远程仓库​
    git pull origin main // 拉取远程代码


​
注意我这里没有使用 SSH，这里使用的是 Https，使用的是账号 + Token 的认证方式。可以通过：
<https://github.com/settings/tokens> 创建一个 Token，后面也会用到。

### 配置 Git 插件

打开 Obsidian 此时已经存在远程的文件了，在手机端也需要安装 Git 插件，同样在第三方插件中关闭安全模式后可以安装。

打开 Git 插件的配置栏，自动同步的配置保持和 Mac 端的一致，需要配置 Git 的栏目，因为自动同步其实是靠 Git 插件来同步的。依次把以下的配置完成同步即可。

在 Git 插件的配置中，找到 Username、Token、name、email，填入正确的值即可。

![Git 插件](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/dd46201c6394e8ffdcf38bfcc88888b6.png)

## Android 端配置

在 IOS 端有 Working Copy，Android 也有类似的软件叫做 MGit，它是 Android 上的 Git 客户端，可以实现手动同步，但是为了和 IOS 端保持一致，还是选择了 Termux，Termux 是 Android 上的 Linux Shell 工具，通过它来安装 Git。

### 安装 Termux

在 Termux 官网或者 Google Play 中搜索下载。

下载安装之后，打开Termux，在 Termux 中申请本机存储访问权限，之后使Termux可访问本机存储。


    termux-setup-storage


下载依赖


    pkg update
    pkg install git


### 配置目录

创建存放目录，Android 中是可以直接打开一个目录作为仓库的，可以自定义目录，这里我选择的是 Documents/Obsidian/WorkSpaceMD，注意这个目录和后续有关，需要记住。

通过cd命令，进入本机 Obsidian 文件夹的 WorkSpaceMD 文件夹内。不同手机型号地址位置可能有所不同，例如：


    cd ~/storage/documents/Obsidian/WorkSpaceMD


### 配置Git

通过以下命令拉取远程仓库的代码。


    git init  // 初始化 git
    git branch -M main  // 调整分支为 main
    git remote add origin https://github.com/Guizimo/WorkSpaceMD.git // 添加远程仓库
    git config --global --add safe.directory /storage/emulated/0/Documents/Obsidian/WorkSpaceMD  // 添加安全目录

    git config --global user.name "Guizimo"
    git config --global user.email "17680262548@163.com"
    git pull origin main  // 拉取远程代码


### 配置 Git 插件

在 Obsidian 打开刚才拉取的远程仓库，在 Git 插件的配置中，找到 Username、Token、name、email，填入正确的值即可。

![Git 插件](https://guizimo.oss-cn-shanghai.aliyuncs.com/img/e4ed0c10e3ac8aa8e759b2e2cdbe2a91.jpg)

## 注意事项

在使用多设备同步时，需要注意串行使用，如果多台设备同时操作同一个文件，可能会造成冲突，导致同步异常，因为本身是借助 Git 的能力来实现同步的。遇到同步时，需要强行推上去进行覆盖。
