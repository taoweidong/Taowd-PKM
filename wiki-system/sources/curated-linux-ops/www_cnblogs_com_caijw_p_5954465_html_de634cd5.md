---
source: "http://www.cnblogs.com/caijw/p/5954465.html"
title: "Git在tortoiseGit以及eclipse的使用方法 - IT-caijw - 博客园"
fetched_at: "2026-10-05 15:36:09"
---

# 一、Git安装与简单使用

### 1.安装git，tortoiseGit

### 2.创建SSH Key


    打开Git Bash,然后输入ssh-keygen生成公钥和私钥：





### 3.生成ppk文件。


    打开puttykeygen，点击load按钮，然后选择所有文件，选择私钥生成private key生成ppk文件





### 4.git在命令行的简单使用。


    第一步:要克隆一个仓库，首先必须知道仓库的地址，然后使用git clone命令克隆（详见：二、Git本地仓库创建及操作）
    第二步：用命令git add .(.代表所有的文件，也可以只写文件名)告诉Git，把文件添加到仓库（实际上就是把文件修改添加到暂存区）
    第三步：用命令git commit -m ‘你提交的信息’告诉Git，把文件提交到仓库（实际上	就是把暂	存区的所有内容提交到当前分支）
    第四步：git status命令可以让我们时刻掌握仓库当前的状态
     	第五步：git pull 拉取服务器上更新文件
    第六步： git push 把文件提交到服务器(要push前一定要先pull下来看下，然后在git status看下有没有冲突)


### 5.冲突解决：


    5.1git的回退
    HEAD指向的版本就是当前版本，因此，Git允许我们在版本的历史之间穿梭，	使用命令git reset --hard commit_id。
    穿梭前，用git log可以查看提交历史，以便确定要回退到哪个版本。
    要重返未来，用git reflog查看命令历史，以便确定要回到未来的哪个版本

    5.2git的撤销修改
    场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，	用命令git checkout -- file。
    场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想	丢弃修改，分两步，第一步用命令git reset HEAD file，就回到了场景1，第	二	步按场景1操作。
    场景3：已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版	本回退一节，不过前提是没有推送到远程库。


### 6.git在window上直接使用tortoiseGit界面操作使用，（推荐使用window的操作）


    修改篇：
    第一步：详细见（二、Git本地仓库创建及操作）
    第二步：修改了文件后，右键选择commit，输入Message后，点Commit提交到本地仓库。



    第三步：拉取服务器文件，git pull，点击OK，后点击close



    如果文件出现感叹号则表示有冲突，必须先解决冲突。
    冲突解决方法：
    1.在点击close后可以直接在弹出的窗口中点击yes来查看冲突，也可以通过点击Diff看本地仓库文件和服务器上面的文件哪里冲突了。
    2.在弹出的窗口中双击打开冲突文件，解决冲突问题。
    3.冲突解决完之后，删除在目录下生成出的多余文件，再次commit。



    第四步：提交代表到服务器， git push




    新增篇：
    第一步：在仓库中新增文件后，先pull，然后可以在diff中查看和仓库区别
    第二步：右键->commit，选择你需要提交的文件，然后点击commit
    第三步：push文件


# 二、Git本地仓库创建及操作


    1.创建Git本地仓库文件夹
    2.打开文件夹，右键->Git Clone...
    3.输入URL，Load Putty Key选择前面存放的ppk文件，点击OK
    4.对.gitignore中提到的文件进行取消跟踪（一般工程文件执行此步骤）

    取消跟踪方法：
    1.例如取消readme1.txt文件的跟踪，右键->git Bash Here，输入git rm --cached readme1.txt
    2.例如取消.setting文件夹的跟踪，右键->git Bash Here，输入git rm -r --cached .settings/


# 三、eclipse中使用Git导入工程


    1.打开Git Repositories窗口，点击右上角Add an existing local Git Repository to this view图标
    2.在Directory中选择你本地Git总仓库，在下方选择你想导入的Git仓库目录
    3.打开你导入的仓库->Working Tree，选择你想导入的工程，右键->Import Projects...
    4.调整选项，导入工程
    5.右键已导入工程->Gradle->Refresh Gradle Project


# 四、eclipse中使用Git同步工程


    1.右键工程->Team->Synchronize Workspace进入同步窗口
    2.对双向红箭头文件，打开，进行代码合并操作，操作完成后 右键->Mark asMerged
    3.选择要上传的文件，右键->Add to Index/在Unstaged Changes中右键->Add to Index
    4.在Staged Changes中可以查看要提交的文件，在Commit Message中输入提交内容备注，以及作者相关，点击commit至本地
    5.Pull拉取服务器上更新文件
    6.最后Push至服务器


# 五、冲突合并解决


    1.首先标红的文件提交到本地库，然后pull下来，这个时候你会发现不能push上去。
    2.然后你就要解决那些标红的文件的冲突，然后再commit到本地库
    3.最后你再push上去
