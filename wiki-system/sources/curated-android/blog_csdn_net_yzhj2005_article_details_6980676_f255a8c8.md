---
source: "http://blog.csdn.net/yzhj2005/article/details/6980676/"
title: "Windows下搭建Eclipse+Android4.0开发环境_哪个版本的eclipse 有eclipse ide for android-CSDN博客"
fetched_at: "2026-10-05 15:26:55"
---

官方搭建步骤： <http://developer.android.com/index.html>

搭建环境之前需要[下载](http://www.2cto.com/soft)下面几个文件包：

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024214186.png)

一、安装Java运行环境JRE（没这个Eclipse运行不起来）和JDK

官网下载 [ http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html)，

先装JRE，再装JDK，这个没什么说的，直接点击下一步就好了。。。。

二、安装Android SDK

下载地址：<http://developer.android.com/sdk/index.html>

离线包地址：<http://3x007.verycd.com/topics/2887449/>

将下载下来的android_sdk_r14包解压出来，哪儿都管放，我通常是解压到Eclipse文件下，随便放。。。

解压后运行SDK Manager.exe文件，运行后如下图，建议将Android1.5到Android4.0全选，一共是33个包，点击Install 33 Packages按钮，安装SDK需要花点 时间，我的带宽是4M还好，大约50mins。

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024214198.png)

下载完成效果如下图：

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024217971.png)

**OK，SDK 安装完成了。。。。**

  * 在用户变量中新建PATH值为：Android SDK中的tools绝对路径（本机为D:\AndroidDevelop\android-sdk-windows\tools）。

[![image](https://i-blog.csdnimg.cn/blog_migrate/cfa5cb15d5eb89afdc99532122d6ea22.png)](http://images.cnblogs.com/cnblogs_com/skynet/WindowsLiveWriter/Android1_552/image_4.png)图2、设置Android SDK的环境变量

“确定”后，重新启动计算机。重启计算机以后，进入cmd命令窗口，检查SDK是不是安装成功。
运行 android –h 如果有类似以下的输出，表明安装成功：

[![image](https://i-blog.csdnimg.cn/blog_migrate/06486321001bd01e2ccbddf1878a5be5.png)](http://images.cnblogs.com/cnblogs_com/skynet/WindowsLiveWriter/Android1_552/image_10.png)图3、验证Android SDK是否安装成功

三： 安装Android ADT（eclipse插件）

Eclipse官方下载<http://www.eclipse.org/downloads/>，选择Eclipse IDE for Java EE Developers, 212 MB，原来名字是helios，现在叫indigo，升级太快了，运行eclipse界面，选择菜单栏 Help > Install New Software

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024217561.png)

弹出对话框要求输入Name和Location：Name自己随便取，Location输入[http://dl-ssl.google.com/android/eclipse](http://dl-ssl.google.com/android/eclipse "http://dl-ssl.google.com/android/eclipse") 或

[https://dl-ssl.google.com/android/eclipse/](https://dl-ssl.google.com/android/eclipse/)如下图所示：

[![image](https://i-blog.csdnimg.cn/blog_migrate/d1081ddeff128117a4d60b6d91e7c64c.png)](http://images.cnblogs.com/cnblogs_com/skynet/WindowsLiveWriter/Android1_552/image_12.png)

注：许多国内的网友都无法完成这样的升级，通常是进行到一半就没有任何反映了（其他插件，例如pydev也是这样）。

没关系，我们直接到Android官网去下载这个ADT插件（ADT-15.0.0.zip）：<http://developer.android.com/sdk/eclipse-adt.html>

也可以点击Archive离线安装。

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024218611.jpg)

安装完成后需要重启Eclipse，重启后eclipse会自动弹出指定SDK的路径，选择 Use existing SDKs ，Existing Location 是第二步骤中SDK的路径，

然后 Next > Finish 。

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024221726.jpg)

**ADT安装完成了。。。。**

跟以前的版本不一样的是，SDK 管理和ADT管理分开了，有两个图标

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024221859.png)。

四、 配置Android模拟器

点击上图右边的按钮（像个手机一样的），打开AVD管理器后，点击 New 新建一个模拟器，输入Name 叫 avd4.0，指定 Target 选择 Android4.0 ，然后再分配 SD Card的大小 256M，最后 Create AVD。

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024221156.png)

**AVD创建完成了。。。。**

五、 我们的 Hello World（We run it together!）

选择 File > New > Android Project，命名为HelloWorld。

写点代码：

package allen.liu.helloworld;

import android.app.Activity;

import android.os.Bundle;

import android.widget.TextView;

public class HelloWorldActivity extends Activity {

private TextView txtView;

/** Called when the activity is first created. */

@Override

public void onCreate(Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

setContentView(R.layout.main);

this.txtView = (TextView) findViewById(R.id.txtView);

if(this.txtView!=null){

this.txtView.setText("Hello World");

}

}

}

//运行起来

![\\](http://www.2cto.com/uploadfile/2011/1114/20111114024222257.png)

android4.0 Api文档、模拟器等 下载链接

ed2k://|file|[Android开发环境搭建].android-sdk_r15-windows.7z|626349500|5ed5d36562e047889ec8a79449962620|h=r6ltf5wmm2lcffotyiqent76pd4nvx7r|/
