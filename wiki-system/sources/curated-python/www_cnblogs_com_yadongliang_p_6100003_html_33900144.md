---
source: "https://www.cnblogs.com/yadongliang/p/6100003.html"
title: "详解Linux安装GCC方法 - 习惯沉淀 - 博客园"
fetched_at: "2026-10-05 15:42:37"
---

## **写在前面**

捞nginx的时候回过头来看gcc的安装，才发现这篇怎么这么长，还是转载的。看不下去了，现重新总结一下，简单粗暴的两行命令。

## 操作步骤

### **一.安装(基于Centos6.5, 其他系列Linux系统命令有所不同)**

**yum -y install gcc gcc-c++ autoconf pcre pcre-devel make automake
yum -y install wget httpd-tools vim**

1.就把gcc当成c语言编译器, g++当成c++语言编译器用就是了.(知乎)

2.wget是一个从网络上自动下载文件的自由工具, 可以在用户退出系统的之后在后台继续执行, 直到下载任务完成.(百度百科)

### **二.测试(查看版本信息, 编译Helloworld)**

**1.查看gcc版本信息**

gcc --version

![](https://images2018.cnblogs.com/blog/917633/201802/917633-20180228111053881-1770385495.png)

**2.编写Helloworld**

**创建名为ctest.c文件**

touch ctest.c

**编辑该文件**

![](https://images2018.cnblogs.com/blog/917633/201802/917633-20180228111004509-647978296.png)


    #include <stdio.h>

    int main()
    {
    printf("hello world!\n");
    return 0;
    }

**编译gcc ctest.c**

可以看到生成了a.out文件

![](https://images2018.cnblogs.com/blog/917633/201802/917633-20180228111152224-794249129.png)

**执行a.out**

./a.out

**输出结果**

![](https://images2018.cnblogs.com/blog/917633/201802/917633-20180228111243727-2009393241.png)

****

**提示:**

  * **若遇到虚拟机无法上网问题, 这篇可能会帮到你:[ 解决Centos6.5虚拟机上网问题](https://www.cnblogs.com/yadongliang/p/6099949.html).**

## **感谢**

  * **[centos中执行apt-get命令提示apt-get command not found](https://www.cnblogs.com/yadongliang/p/8660046.html)**

## 转载部分

**=======****=======********=======**** 以下为转载内容(太长,忽略不看了)****=======********=======********=======******

如果为没有联网状态下, 那就耐着性子看吧.

本文转自:<http://blog.csdn.net/bulljordan23/article/details/7723495/>

下载： <http://ftp.gnu.org/gnu/gcc/gcc-4.5.1/gcc-4.5.1.tar.bz2>
浏览： <http://ftp.gnu.org/gnu/gcc/gcc-4.5.1/>
查看Changes： <http://gcc.gnu.org/gcc-4.5/changes.htm>

现在很多程序员都应用GCC，怎样才能更好的应用GCC。目前，GCC可以用来编译C/C++、FORTRAN、[Java](http://lib.csdn.net/base/javaee "Java EE知识库")、OBJC、ADA等语言的程序，可根据需要选择安装支持的语言。本文以在Redhat [Linux](http://lib.csdn.net/base/linux "Linux知识库")安装GCC4.1.2为例(因在项目开发过程中要求使用，没有用最新的GCC版本)，介绍Linux安装GCC过程。

安装之前，系统中必须要有cc或者gcc等编译器，并且是可用的，或者用环境变量CC指定系统上的编译器。如果系统上没有编译器，不能安装源代码形式的GCC 4.1.2。如果是这种情况，可以在网上找一个与你系统相适应的如RPM等二进制形式的GCC软件包来安装使用。本文介绍的是以源代码形式提供的GCC软件包的安装过程，软件包本身和其安装过程同样适用于其它Linux和Unix系统。

系统上原来的GCC编译器可能是把gcc等命令文件、库文件、头文件等分别存放到系统中的不同目录下的。与此不同，现在GCC建议我们将一个版本的GCC安装在一个单独的目录下。这样做的好处是将来不需要它的时候可以方便地删除整个目录即可(因为GCC没有uninstall功能);缺点是在安装完成后要做一些设置工作才能使编译器工作正常。在本文中采用这个方案安装GCC 4.1.2，并且在安装完成后，仍然能够使用原来低版本的GCC编译器，即一个系统上可以同时存在并使用多个版本的GCC编译器。

按照本文提供的步骤和设置选项，即使以前没有安装过GCC，也可以在系统上安装上一个可工作的新版本的GCC编译器。

**1 下载**

在GCC网站上(http://gcc.gnu.org)或者通过网上搜索可以查找到下载资源。目前GCC的最新版本为 4.2.1。可供下载的文件一般有两种形式：gcc-4.1.2.tar.gz和gcc-4.1.2.tar.bz2，只是压缩格式不一样，内容完全一致，下载其中一种即可。

**2\. 解压缩**

拷贝gcc-4.1.2.tar.bz2(我下载的压缩文件)到/usr/local/src(根据自己喜好选择)下,根据压缩格式，选择下面相应的一种方式解包(以下的“%”表示命令行提示符)：

% tar zxvf gcc-4.1.2.tar.gz

或者

% bzcat gcc-4.1.2.tar.bz2 | tar xvf -

新生成的gcc-4.1.2这个目录被称为源目录，用${srcdir}表示它。以后在出现${srcdir}的地方，应该用真实的路径来替换它。用pwd命令可以查看当前路径。

在${srcdir}/INSTALL目录下有详细的GCC安装说明，可用浏览器打开index.html阅读。

**3\. 建立目标目录**

目标目录(用${objdir}表示)是用来存放编译结果的地方。GCC建议编译后的文件不要放在源目录${srcdir]中(虽然这样做也可以)，最好单独存放在另外一个目录中，而且不能是${srcdir}的子目录。

例如，可以这样建立一个叫 /usr/local/gcc-4.1.2的目标目录：

% mkdir /usr/local/gcc-4.1.2

% cd gcc-4.1.2

以下的操作主要是在目标目录 ${objdir} 下进行。(否则会出错，后面有解释)

**4\. 配置**

配置的目的是决定将GCC编译器安装到什么地方(${destdir})，支持什么语言以及指定其它一些选项等。其中，${destdir}不能与${objdir}或${srcdir}目录相同。

配置是通过执行${srcdir}下的configure来完成的。其命令格式为(记得用你的真实路径替换${destdir})：

% ${srcdir}/configure --prefix=${destdir} [其它选项]

例如，如果想将GCC 4.1.2安装到/usr/local/gcc-4.1.2目录下，则${destdir}就表示这个路径。

在我的机器上，我是这样配置的：

% ../gcc-4.1.2/configure --prefix=/usr/local/gcc-4.1.2 --enable-threads=posix --disable-checking --enable--long-long --host=i386-redhat-linux--with-system-zlib --enable-languages=c,c++,java

将GCC安装在/usr/local/gcc-4.1.2目录下，支持C/C++和JAVA语言，其它选项参见GCC提供的帮助说明。

**5\. 编译**

% make

**6\. 安装**

执行下面的命令将编译好的库文件等拷贝到${destdir}目录中(根据你设定的路径，可能需要管理员的权限)：

% make install

至此，GCC 4.1.2安装过程就完成了。

**7\. 其它设置**

GCC 4.1.2的所有文件，包括命令文件(如gcc、g++)、库文件等都在${destdir}目录下分别存放，如命令文件放在bin目录下、库文件在 lib下、头文件在include下等。由于命令文件和库文件所在的目录还没有包含在相应的搜索路径内，所以必须要作适当的设置之后编译器才能顺利地找到并使用它们。

7.1 gcc、g++、gcj的设置

要想使用GCC 4.1.2的gcc等命令，简单的方法就是把它的路径${destdir}/bin放在环境变量PATH中。我不用这种方式，而是用符号连接的方式实现，这样做的好处是我仍然可以使用系统上原来的旧版本的GCC编译器。

首先，查看原来的gcc所在的路径：

% which gcc

在我的系统上，上述命令显示：/usr/bin/gcc。因此，原来的gcc命令在/usr/bin目录下。我们可以把GCC 4.1.2中的gcc、g++、gcj等命令在/usr/bin目录下分别做一个符号连接：

% cd /usr/bin

% ln -s ${destdir}/bin/gcc gcc412

% ln -s ${destdir}/bin/g++ g++412

% ln -s ${destdir}/bin/gcj gcj412

这样，就可以分别使用gcc412、g++412、gcj412来调用GCC 4.1.2的gcc、g++、gcj完成对C、C++、JAVA程序的编译了。同时，仍然能够使用旧版本的GCC编译器中的gcc、g++等命令。

(cool，我感觉棒极了!!1)

7.2 库路径的设置

将${destdir}/lib路径添加到环境变量LD_LIBRARY_PATH中，例如，如果GCC 4.1.2安装在/usr/local/gcc-4.1.2目录下，在RH Linux下可以直接在命令行上执行

% export LD_LIBRARY_PATH=/usr/local/gcc-4.1.2/lib

最好添加到系统的配置文件中，这样就不必要每次都设置这个环境变量了,在文件$HOME/.bash_profile中添加下面两句：

LD_LIBRARY_PATH=/usr/local/gcc-4.1.2/lib:$LD_LIBRARY_PATH

export LD_LIBRARY_PATH

重启系统设置生效，或者执行命令

% source $HOME/.bash_profile

用新的编译命令(gcc412、g++412等)编译你以前的C、C++程序，检验新安装的GCC编译器是否能正常工作。

完成了Linux安装GCC，之后你就能轻松地编辑了。

from:os.51cto.com/art/200912/168804.htm

在RHLinux下安装gcc-4.0.1方法比较简单，但是安装过程中有些环节是需要注意的，否则，可能会导致安装不成功，或者安装报错。具体安装过程如下：

首先，下载并解压缩gcc的RPM包至源目录(如/opt/gcc-4.0.1)

**1、解压缩RPM包：**

[root@linuxopt]# tar xjvf gcc-4.0.1.tar.bz2 (解压后生成源目录/opt/gcc-4.0.1)

**2、创建安装目标目录：**

[root@linux opt]# mkdir /usr/local/gcc-4.0.1/

**3、进入安装目标目录：**

[root@linux opt]# cd /usr/local/gcc-4.0.1/ (这一步很重要，配置安装文件时，需要在目标目录下执行configure命令)

[root@linux opt]# pwd

/usr/local/gcc-4.0.1

**4、配置安装文件：**

[root@linux gcc-4.0.1]# /opt/gcc-4.0.1/configure --prefix=/usr/local/gcc-4.0.1/ (这一步非常重要，需要在安装的目标目录下，执行源目录 /opt/gcc-4.0.1/中的configure命令，配置将gcc安装到目标目录/usr/local/gcc-4.0.1/)

creating cache ./config.cache

checking host system type... i686-pc-linux-gnu

**5、编译安装文件：**

[root@linux gcc-4.0.1]# pwd

/usr/local/gcc-4.0.1

[root@linux gcc-4.0.1]# make (在目标目录下执行编译)

**6、安装gcc：**

[root@linux gcc-4.0.1]# pwd

/usr/local/gcc-4.0.1

[root@linux gcc-4.0.1]# make install (在目标目录下执行安装)

如果安装过程中步骤和命令没有错误，你肯定能安装成功。
