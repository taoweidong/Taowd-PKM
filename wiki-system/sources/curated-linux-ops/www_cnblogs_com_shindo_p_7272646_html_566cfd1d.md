---
source: "https://www.cnblogs.com/shindo/p/7272646.html"
title: "Intellij Idea 2017创建web项目及tomcat部署实战 - shindoyang - 博客园"
fetched_at: "2026-10-05 15:34:42"
---

相关软件：Intellij Idea2017、jdk16、tomcat7

Intellij Idea直接安装（可根据需要选择自己设置的安装目录），jdk使用1.6/1.7/1.8都可以，主要是配置好系统环境变量，tomcat7上tomcat的官网下载压缩包解压即可。

## 一、创建简单web项目

1、创建一个web project

File -> new Project ->选择project sdk 为1.6（如果没有sdk的同学请先配置）-> Next

create project from template 页面，不勾选任何选项 -> Next

输入项目名：webDemo -> Next -> Finish

## 二、创建一个Module

鼠标点中项目名称webDemo -> 右键选择New，选择Module -> Module SDK 选择1.6 -> 勾选JavaEE下的Web Application(3.1) ，注意窗口下的version对应为3.1，且Create web.xml已勾选 -> Next

输入Module name 为firstweb -> Finish

3、创建好的web项目

4、在web/WEB_INF 目录下创建两个文件夹：classes和lib

classes用来存放编译后输出的class文件，lib用于存放第三方jar包

5、配置文件夹路径

File -> Project Structure (ctrl + shift + Alt + s) 或者使用工具栏的快捷键 -> 选择Modules

-> 选择Paths -> 选择“Use module compile out path” -> 将Outputpath 和Test output path 都设置为刚刚创建的classes文件夹

选择当前窗口的Dependencies -> 将Module SDK选择为1.6 ->点击右边的 + 号 -> 选择 “1 JARS or directories ...”

-> 选择刚刚创建的lib文件夹 -> OK

-> 选择Jar Directory -> OK

-> Apply -> OK

## 三、配置Tomcat容器

打开菜单Run -> Edit Configurations...

点击 “+” ，选择 “Tomcat Server” -> 选择“Local”

在Name出输入新的服务器名，点击 "Application Server" 后面的 "Configure..."，弹出Application Servers窗口，在Tomcat Home 选择本地安装的tomcat目录 -> OK

在"Run/Debug Configurations"窗口中Name一栏输入服务器的名字tomcat7，在“Server”面板中，勾选取消“After Launch”，设置“HTTP port”和“JMX port”（默认值即可），点击Apply -> OK，至此tomcat配置完毕（左边列表中tomcat图标上小红叉是未部署项目的提示，部署项目后就会消失）。

## 四、在tomcat上部署并运行项目

在创建好tomcat后，可以通过工具栏快速打开tomcat的配置页面：

也可以通过菜单栏：Run -> Edit Configurations... ->选择刚创建的tomcat7 -> 选择Deployment ->点击右边的“ + ”号 -> 选择 Artifact

-> 选择web项目 -> Application Context可以填“/firstweb”(也可以不填) -> Apply

回到Server面板，将On 'update' action和On frame deactivation（这两个选项是tomcat配置了项目后才有的）改为update classes and resources -> Apply

开发web项目并运行tomcat查看效果

1、编辑index.jsp页面

2、运行tomcat
