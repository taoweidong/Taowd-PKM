---
source: "https://yq.aliyun.com/articles/696132"
title: "使用CloudToolkit在IntelliJ IDEA中部署应用到服务器-开发者社区-阿里云"
fetched_at: "2026-10-05 15:34:32"
---

在之前的文章[《在 Intellij IDEA 中部署 Java 应用到 阿里云 ECS》](https://yq.aliyun.com/articles/673825)中讲解了如何将一个本地应用部署到阿里云 ECS 上去，有些读者反馈目前还有一些测试机器是在经典网络，甚至是在本地机房中，咨询是否可以通过 Cloud Toolkit 插件将应用部署到这些服务器上去？最新版本的 Cloud Toolkit 已经发布，完全支持啦。

# 本地开发

无论是编写云端运行的，还是编写本地运行的 Java 应用程序，代码编写本身并没有特别大的变化，因此本文采用一个及其基础的样例《在 Web 页面打印 HelloWorld 的 Java Servlet 》为例，做参考。

![image](https://yqfile.alicdn.com/0e3e037b58282a9cfeb9be24d1bac8c71b64fbc6.png?x-oss-process=image/resize,w_1400/format,webp)


    public class IndexServlet extends HttpServlet {
        private static final long serialVersionUID = -112210702214857712L;

        @Override
        public void doGet( HttpServletRequest req, HttpServletResponse resp ) throws ServletException, IOException {
            PrintWriter writer = resp.getWriter();
            //Demo：通过 Cloud Toolkit ，高效的将本地应用程序代码修改，部署到云上。
            writer.write("Deploy from alibaba cloud toolkit. 2018-10-24");
            return;
        }
        @Override
        protected void doPost( HttpServletRequest req, HttpServletResponse resp ) throws ServletException, IOException {
            return;
        }}

[源代码下载](https://yq.aliyun.com/attachment/download/?filename=IndexSer...%5B%E9%93%B6%E6%97%B6%5D.1540514368.zip)

上述代码就是一个标准的 Java 工程，用于在 Web 页面上打印一串“Hello World”的文案。

# 安装插件

阿里云提供了基于 Intellij IDEA 的插件，以方便开发人员能够高效的将本地 IDE 中编写的应用程序，极速部署到服务器中去。
插件主页：<https://www.aliyun.com/product/cloudtoolkit>

阿里云的这个 IntelliJ IDEA 插件的安装过程，和普通的插件大同小异，这里不再赘述，读者请自行安装。

# 添加服务器

![image](https://yqfile.alicdn.com/4518bf75af70cdb30054156b4397873ef88302db.png?x-oss-process=image/resize,w_1400/format,webp)

如上图所示，在菜单
` Tools - Alibaba Cloud - Alibaba Cloud View - Host`中打开机器视图界面，如下图：
![image](https://yqfile.alicdn.com/d424118b632c0eefa79c9908abf992b1e6241149.png?x-oss-process=image/resize,w_1400/format,webp)

点击右上角`Add Host`按钮，出现添加机器界面

![image](https://yqfile.alicdn.com/d6da0fbd2495470802418f41c543f1df3c032775.png?x-oss-process=image/resize,w_1400/format,webp)

# 部署

![image](https://yqfile.alicdn.com/36d07c3dd049639b6f25b88a773f107773201171.png?x-oss-process=image/resize,w_1400/format,webp)

在 IntelliJ IDEA 中，鼠标右键项目工程名，在出现的菜单中点击 **Alibaba Cloud - Deploy to Host...** ，会出现如下部署窗口：

![image](https://yqfile.alicdn.com/946f4b7e04e21b53cc6de67b5d87e0e251111912.png?x-oss-process=image/resize,w_1400/format,webp)

在 Deploy to Host 对话框设置部署参数，然后单击 Deploy，即可执行初次部署。

## 部署参数说明：

  * Deploy File：部署文件包含两种方式。

    * Maven Build：如果当前工程采用 Maven 构建，可以使用 Cloud Toolkit 直接构建并部署。
    * Upload File：如果当前工程并非采用 Maven 构建，或者本地已经存在打包好的部署文件，可以选择并直接上传本地的部署文件。
  * Target Deploy host：在下拉列表中选择Tag，然后选择要部署的服务器。
  * Deploy Location ：输入在 ECS 上部署路径，如 /root/tomcat/webapps。
  * Commond：输入应用启动命令，如 sh /root/restart.sh。表示在完成应用包的部署后，需要执行的命令 —— 对于 Java 程序而言，通常是一句 Tomcat 的启动命令。


[立即点击下载](https://yq.aliyun.com/articles/673560)


官网
<https://toolkit.aliyun.com>


![5685e931e06cd61faa41dee0ad46bf251fe56837](https://yqfile.alicdn.com/5685e931e06cd61faa41dee0ad46bf251fe56837.png?x-oss-process=image/resize,w_1400/format,webp)

交流群（钉钉）


![b35318a3e1a70775eee7dcb295468d50f5d21abb](https://yqfile.alicdn.com/b35318a3e1a70775eee7dcb295468d50f5d21abb.png?x-oss-process=image/resize,w_1400/format,webp)

交流群（微信）
