---
source: "https://blog.csdn.net/w7569133507/article/details/80372892"
title: "Jenkins中换了maven地址后，一直使用原来的maven地址_jenkins修改maven项目的打包地址-CSDN博客"
fetched_at: "2026-10-05 15:29:59"
---

可能maven需要升级更换版本，然后Jenkins中跟着换，你可能会这样处理:

**[系统管理](http://localhost:8080/manage)\--->[系统设置](http://localhost:8080/configure)**

![](https://i-blog.csdnimg.cn/blog_migrate/4db085263ba1af63b781e7904eb8a0eb.png)

或者

[系统管理](http://localhost:8080/manage)\--->[](http://localhost:8080/configure)[](http://localhost:8080/manage)[全局工具配置](http://localhost:8080/configureTools)[](http://localhost:8080/configure)

![](https://i-blog.csdnimg.cn/blog_migrate/624c6b4428fc1ae7efdcb9dacbce2a84.png)

本以为这样就可以了，结果构建项目的时候一直用的是原来的maven地址，会出现以下错误

![](https://i-blog.csdnimg.cn/blog_migrate/38c26d5c9603b584522c4fd509d9d72b.png)

解决办法：

除了以上的修改，还得改一个地方，就是E:\jenkins\hudson.tasks.Maven.xml ,其中E:\jenkins是jenkins环境变量中设置的地址，确实是个大坑。

![](https://i-blog.csdnimg.cn/blog_migrate/9038fd4c6fd6354ead7ce53337866347.png)
