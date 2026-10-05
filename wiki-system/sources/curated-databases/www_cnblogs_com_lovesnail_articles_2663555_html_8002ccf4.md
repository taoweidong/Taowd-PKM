---
source: "http://www.cnblogs.com/lovesnail/articles/2663555.html"
title: "尝试加载 Oracle 客户端库时引发 BadImageFormatException。如果在安装 32 位 Oracle 客户端组件的情况下以 64 位模式运行 - 一只小蜗牛 - 博客园"
fetched_at: "2026-10-05 15:28:19"
---

详细分析：

[使用C# 连接不同版本的Oracle.DataAccess](http://www.cnblogs.com/zetee/articles/2003192.html)

平时我们开发使用的是32位的PC机，所以安装的也是Oracle32位的客户端。但是一般服务器都是64位的，安装的也是64位的Oracle客户端，如果要部署使用Oracle.DataAccess连接Oracle的应用程序时，可能会遇到版本上的问题。

主 要版本问题有两种，一种是32位版和64位版的问题，如果我们开发出来的应用是32位的，那么就必须使用32位的客户端，如果是64位的应用程序当然对应 64位的客户端。这里需要注意：在64位的环境中使用VS开发Web程序，其运行的Web服务“WebDev.WebServer.exe”是32位的， 所以如果要调试64位的Oracle连接程序，最好是部署到IIS中，使用IIS来连接Oracle数据库。

另一个版本问题是 Oracle.DataAccess的版本号问题，我的本机就是32位的XP，安装了Oracle11gR2客户端后，在安装目录下的 ODP.NET\bin\2.x目录中可以找到Oracle.DataAccess.dll文件，可以看到其版本号是：2.112.1.2。所以我开发出 来的程序，引用的也是这个版本的库。

但是在64位下的Oracle.DataAccess.dll却不一样，安装后的版本是2.112.1.0，如图是Windows2008X64上的Oracle.DataAccess.dll。

现在把开发环境的程序发布部署到服务器上，就会抛出异常

_未能加载文件或程序集“Oracle.DataAccess, Version=2.112.1.2, Culture=neutral, PublicKeyToken=89b483f429c47342”或它的某一个依赖项。_

_或者是_

Could not load file or assembly 'Oracle.DataAccess, Version=2.112.1.2, Culture=neutral, PublicKeyToken=89b483f429c47342' or one of its dependencies. An attempt was made to load a program with an incorrect format之类的话。

总之就是找不到对应的程序集。显然，这里系统找的是2.112.1.2版本的 Oracle.DataAccess，而服务器上只有2.112.1.0版本的，所以才报错，解决办法就是在web.config中修改，在 configSections节点结束之后增加如下内容：

<runtime>
<assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
<dependentAssembly>
<assemblyIdentity name="Oracle.DataAccess"
publicKeyToken="89B483F429C47342"
culture="neutral" />
<bindingRedirect
oldVersion="2.112.1.2"
newVersion="2.112.1.0"/>
</dependentAssembly>
</assemblyBinding>
</runtime>

这样就可以让IIS调用2.112.1.0的Oracle.DataAccess了。添加这个配置后便可正常运行

上述添加配置节点的方法，可以在取消特定版本的属性之后避免。

开发环境：VS2008+64位ORACLE+64位oracleclient,64位WIN7 ，本地IIS调试程序的时候总是提示：**尝试加载 Oracle 客户端库时引发 BadImageFormatException。如果在安装 32 位 Oracle 客户端组件的情况下以 64 位模式运行，将出现此问题。**

**将IIS连接程序池中项目所对应程序池的32位模式为false，就OK了。注意 生成项目的属性，目标平台为任何cpu**

****

****

****
