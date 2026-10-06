---
source: "https://cloud.tencent.com/developer/article/2246756"
title: "【Android NDK 开发】Visual Studio 2019 使用 CMake 开发 JNI 动态库 ( 动态库编译配置 | JNI 头文件导入 | JNI 方法命名规范 )-腾讯云开发者社区-腾讯云"
fetched_at: "2026-10-06 12:38"
---

[社区首页](https://cloud.tencent.com/developer) >[专栏](https://cloud.tencent.com/developer/column) >【Android NDK 开发】Visual Studio 2019 使用 CMake 开发 JNI 动态库 ( 动态库编译配置 | JNI 头文件导入 | JNI 方法命名规范 )

#### 文章目录

复制
    
    
            - [I . JNI 与 NDK 区别](https://cloud.tencent.com/developer)
            - [II . Visual Studio 编译动态库](https://cloud.tencent.com/developer)
            - [III. 配置 导入 jni.h 头文件](https://cloud.tencent.com/developer)
            - [IV . IntelliJ IDEA Community Edition 创建 Java 项目](https://cloud.tencent.com/developer)
            - [V . Java 定义的 Native 方法](https://cloud.tencent.com/developer)
            - [VI . C++ 中实现上面定义的 Native 方法](https://cloud.tencent.com/developer)
            - [VII . CMake 项目生成 dll 动态库](https://cloud.tencent.com/developer)
            - [VIII . Java 中加载调用动态库](https://cloud.tencent.com/developer)
            - [IX . 使用 javah 工具生成 C++ 中需要实现的 Native 方法 ( 仅做参考 )](https://cloud.tencent.com/developer)
            - [X . 总结](https://cloud.tencent.com/developer)

##### I . JNI 与 NDK 区别

* * *

**1 . JNI 简介 : JNI 是一套框架 , 能够让开发者在 Java 中调用 C / C++ 代码 , JNI 范围较广 , 凡是可以运行 Java 代码的地方 ( 如 Linux , UNIX , Windows , Android 等平台 ) , 都可以通过 JNI 接口 调用 C/C++ 代码 ;**

> **NDK 只是 Android 平台的 JNI 规范 , 属于 JNI 的一个分支 ;**

**2 . NDK 简介 : NDK 是 Android 提供的开发工具包 , 其中包含了**

**① Android 平台的交叉编译器 ;**

**② Android 平台的一系列动态库 及 静态库 ;**

> **本篇博客只介绍 JNI , 不涉及 NDK 相关概念;**

##### II . Visual Studio 编译动态库

* * *

> **前提 : 需要搭建 Visual Studio 的 CMake 开发环境 ;** [**【Visual Studio】Visual Studio 2019 社区版 CMake开发环境安装 ( 下载 | 安装相关组件 | 创建编译执行项目 | 错误处理 )**](https://cloud.tencent.com/developer/article/2246662?from_column=20421&from=20421)

**在 Visual Studio 2019 中创建 CMake 项目 :**

**① 创建项目 : 在欢迎界面中 , 点击创建新项目 ;**

**② 选择 CMake 项目 , 点击下一步 ;**

**③ 设置项目名称 , 选择项目位置 , 点击 “创建” 按钮 ;**

**④ 项目创建完毕 ;**

**⑤ 配置 CMakeList.txt 配置文件 , 设置生成动态库选项 ;**

**默认生成的是可执行文件 , 但是此处我们要生成动态库 , 因此将默认的配置注释掉 ;**

**生成动态库的配置格式 : add_library( 库名称 库类型 包含的源文件 ) ;**

复制
    
    
    # CMakeList.txt: 009_Cmake 的 CMake 项目，在此处包括源代码并定义
    # 项目特定的逻辑。
    #
    cmake_minimum_required (VERSION 3.8)
    
    
    # 设置生成 动态库
    # 配置格式是 : 动态库名称 动态库标识( SHARED ) 包含的源文件( 如果有多个就写多个 )
    add_library( 009_Cmake SHARED 009_Cmake.cpp 009_Cmake.h )
    
    
    
    # 将源代码添加到此项目的可执行文件。
    #add_executable (009_Cmake "009_Cmake.cpp" "009_Cmake.h")
    
    # TODO: 如有需要，请添加测试并安装目标。

**⑥ 生成动态库 : 使用 “Ctrl + Shift + B” 快捷键 , 编译项目 , 即可生成动态库 ;**

**⑦ 查看动态库 : 在项目的 “项目根目录\out\build\x64-Debug\009_Cmake” 目录下有生成的 009_Cmake.dll 动态库 , 这是个 Windows 动态库 ;**

**动态库生成目录 : Y:\002_WorkSpace\002_VS\009_Cmake\out\build\x64-Debug\009_Cmake**

##### III. 配置 导入 jni.h 头文件

* * *

**1 . jni.h 头文件位置 : JNI 的头文件在 JDK 的安装目录中 的 include 文件夹下 ;**

> **D:\Program Files\Java\jdk1.8.0_221\include** **D:\Program Files\Java\jdk1.8.0_221\include\win32**

**2 . 将 JNI 头文件配置到 CMake 中 :**

复制
    
    
    #配置 JNI 头文件
    include_directories("D:/Program Files/Java/jdk1.8.0_221/include")
    include_directories("D:/Program Files/Java/jdk1.8.0_221/include/win32")

**配置完后的 CMakeList.txt 文件 :**

复制
    
    
    # CMakeList.txt: 009_Cmake 的 CMake 项目，在此处包括源代码并定义
    # 项目特定的逻辑。
    #
    cmake_minimum_required (VERSION 3.8)
    
    #配置 JNI 头文件
    include_directories("D:/Program Files/Java/jdk1.8.0_221/include")
    include_directories("D:/Program Files/Java/jdk1.8.0_221/include/win32")
    
    
    # 设置生成 动态库
    # 配置格式是 : 动态库名称 动态库标识( SHARED ) 包含的源文件( 如果有多个就写多个 )
    add_library( 009_Cmake SHARED 009_Cmake.cpp 009_Cmake.h )
    
    
    
    # 将源代码添加到此项目的可执行文件。
    #add_executable (009_Cmake "009_Cmake.cpp" "009_Cmake.h")
    
    # TODO: 如有需要，请添加测试并安装目标。

**3 . 导入 JNI 头文件 : 使用 #include <jni.h> 导入JNI头文件 , 点击生成 , 没有报错 , 说明导入成功 ;**

复制
    
    
    // 009_Cmake.cpp: 定义应用程序的入口点。
    
    
    //导入 JNI 的头文件 , 该头文件在 D:/Program Files/Java/jdk1.8.0_221/include 目录中
    //	JDK 的安装目录 , 每个人的安装目录可能不一致
    #include <jni.h>

##### IV . IntelliJ IDEA Community Edition 创建 Java 项目

* * *

> **不做 J2EE 开发 , 只是跑一些 Java , Kotlin 项目 , 使用社区版 ( Community ) 即可 ;**

**IntelliJ IDEA 创建 Java 项目 :**

**① 在 IntelliJ IDEA 的欢迎界面中 , 点击创建新工程 " Create New Project " 按钮 :**

**② 选择 Java 选项卡 , 然后点击 " Next " 按钮 ;**

**③ 选择一个 模板 :**

**④ 设置项目参数 : 在最后一个对话框中设置 工程名称 ( Project name ) , 选择工程位置 ( Project location ) , 以及 包名 ( Base package ) ;**

##### V . Java 定义的 Native 方法

* * *

**在 Java 项目的代码中 , 定义 Native 方法 , 包名为 " kim.hsl.jni " , 类名为 " Main " ;**

**定义的 Native 方法如下 :**

复制
    
    
        /**
         * 定义一个 Native 方法
         * @param i
         * @param s
         */
        public native void jniTest(int i, String s);

**完整的 Java 入口类代码如下 :**

复制
    
    
    package kim.hsl.jni;
    
    public class Main {
    
        public static void main(String[] args) {
    
        }
    
    
        /**
         * 定义一个 Native 方法
         * @param i
         * @param s
         */
        public native void jniTest(int i, String s);
    }

##### VI . C++ 中实现上面定义的 Native 方法

* * *

**1 . C++ 中实现上述 Java 中声明的 Native 方法 : 实现的 JNI 方法如下 , 下面会逐条讲解每个 关键字 或 格式的含义 ;**

复制
    
    
    extern "C"
    JNIEXPORT void JNICALL
    Java_kim_hsl_jni_Main_jniTest(JNIEnv* env, jobject instance, jint i, jstring s_) {
    
        const char* s = env->GetStringUTFChars(s_, 0);
    
        // 打印传入的 两个参数
        printf("Java_kim_hsl_jni_Main_jniTest : %d , %s\n", i , s);
    
        env->ReleaseStringUTFChars(s_, s);
    }

**2 . C++ 兼容 C 语言设置 : extern “C” , 作用是在 C++ 代码中 , 兼容 C 代码 ;**

**① 如果是在 C++ 文件 ( .cpp 后缀源码 ) 中实现 Native 方法 , 需要兼容 C 语言 ;**

**② 如果在 C 文件 ( .c 后缀源码 ) 中 , 则不用添加该选项 ;**

**3 . JNI 方法基本格式 : JNIEXPORT 返回值类型 JNICALL 方法名 ( 参数列表 ) ;**

**4 . 方法名规范 : Java_包名_类名_方法名 , 如包名为 " kim.hsl.jni " , 类名为 " Main " , 方法名为 " jniTest " , 那么 C/C++ 中对应的 Native 方法名为 " Java_kim_hsl_jni_Main_jniTest " ;**

**5 . 参数列表 : 分析该参数列表 ( JNIEnv* env, jobject instance, jint i, jstring s_ ) ;**

**① JNIEnv* env : 第一个参数必定是 JNI 环境参数 , 即 JNIEnv 类型的 指针 ;**

**② jobject instance : 第二个参数必定是 定义 Native 方法的 Java 类对象 ;**

**③ jint i, jstring s_ : 从第三个开始就是定义的 Java 中的 Native 方法的参数 , 注意要使用 java 的替代数据类型 ;**

##### VII . CMake 项目生成 dll 动态库

* * *

**1 . 在上面实现了 JNI 对应的 Native 方法 :**

**2 . 配置 CMakeList.txt 配置文件 , 设置生成动态库选项 ;**

**默认生成的是可执行文件 , 但是此处我们要生成动态库 , 因此将默认的配置注释掉 ;**

**生成动态库的配置格式 : add_library( 库名称 库类型 包含的源文件 ) ;**

复制
    
    
    # CMakeList.txt: 009_Cmake 的 CMake 项目，在此处包括源代码并定义
    # 项目特定的逻辑。
    #
    cmake_minimum_required (VERSION 3.8)
    
    
    # 设置生成 动态库
    # 配置格式是 : 动态库名称 动态库标识( SHARED ) 包含的源文件( 如果有多个就写多个 )
    add_library( 009_Cmake SHARED 009_Cmake.cpp 009_Cmake.h )
    
    
    
    # 将源代码添加到此项目的可执行文件。
    #add_executable (009_Cmake "009_Cmake.cpp" "009_Cmake.h")
    
    # TODO: 如有需要，请添加测试并安装目标。

**3 . 生成动态库 : 使用 “Ctrl + Shift + B” 快捷键 , 编译项目 , 即可生成动态库 ;**

**4 . 查看动态库 : 在项目的 “项目根目录\out\build\x64-Debug\009_Cmake” 目录下有生成的 009_Cmake.dll 动态库 , 这是个 Windows 动态库 ;**

**动态库生成目录 : Y:\002_WorkSpace\002_VS\009_Cmake\out\build\x64-Debug\009_Cmake\009_Cmake.dll**

> **" Y:\002_WorkSpace\002_VS\009_Cmake\out\build\x64-Debug\009_Cmake\009_Cmake.dll " 这个目录很重要 , 一会儿还要在 Java 代码中通过该绝对路径加载动态库 ;**

##### VIII . Java 中加载调用动态库

* * *

**1 . 操作步骤 : Java 中首先要加载动态库 , 然后才能调用动态库中实现的 Native 方法 ;**

**① 加载动态库 :**

复制
    
    
        static {
            //Visual Studio 中生成的 DLL 动态库路径是
            //  Y:\002_WorkSpace\002_VS\009_Cmake\out\build\x64-Debug\009_Cmake\009_Cmake.dll
            //  直接使用该绝对路径加载动态库即可
            System.load(
                    "Y:\\002_WorkSpace\\002_VS\\009_Cmake\\out\\build\\x64-Debug\\009_Cmake\\009_Cmake.dll");
        }

**② 调用 Native 方法 :**

复制
    
    
        public static void main(String[] args) {
    
            //打印结果 : Java_kim_hsl_jni_Main_jniTest : 1 , Hello JNI
            jniTest(1 , "Hello JNI");
    
        }

**2 . 完整 Java 代码 :**

复制
    
    
    package kim.hsl.jni;
    
    public class Main {
    
        static {
            //Visual Studio 中生成的 DLL 动态库路径是
            //  Y:\002_WorkSpace\002_VS\009_Cmake\out\build\x64-Debug\009_Cmake\009_Cmake.dll
            //  直接使用该绝对路径加载动态库即可
            System.load(
                    "Y:\\002_WorkSpace\\002_VS\\009_Cmake\\out\\build\\x64-Debug\\009_Cmake\\009_Cmake.dll");
        }
    
        public static void main(String[] args) {
    
            //打印结果 : Java_kim_hsl_jni_Main_jniTest : 1 , Hello JNI
            jniTest(1 , "Hello JNI");
    
        }
    
        /**
         * 定义一个 Native 方法
         * @param i
         * @param s
         */
        public static native void jniTest(int i, String s);
    }

**3 . 执行结果 :**

复制
    
    
    Java_kim_hsl_jni_Main_jniTest : 1 , Hello JNI

##### IX . 使用 javah 工具生成 C++ 中需要实现的 Native 方法 ( 仅做参考 )

* * *

> **上面根据 Java_包名_类名_方法名 的方式比较繁琐 , 容易出错 , Java 中提供的 javah 工具 , 专门用于生成 实现 Native 方法的头文件 ;**

**1 . 相关目录说明 :**

**① Java 文件绝对路径 : Y:\002_WorkSpace\003_IDEA\001_JNI_Hello\src\kim\hsl\jni\Main.java ;**

**② javah 命令执行路径 : Y:\002_WorkSpace\003_IDEA\001_JNI_Hello\src\ ;**

**③ 需要进入的目录 : 在命令行工具中 , 进入 javah 命令执行路径 , 不要进错目录 ;**

**2 . 执行 Javah 命令 : 使用 javah -o Main.h kim.hsl.jni.Main 命令 , 生成对应的 C / C++ 头文件 , 该头文件中定义有要实现的 Native 方法声明 ;**

**① 指定输出文件 : 其中 -o Main.h 用于指定生成的目标文件 , 即在当前执行命令的目录生成 Main.h 头文件 ;**

**② 指定源文件 : kim.hsl.jni.Main 用于指定要生成的参考类文件 ;**

**3 . 查看生成 Main.h 头文件 :**

**生成的 Main.h 头文件 :**

复制
    
    
    /* DO NOT EDIT THIS FILE - it is machine generated */
    #include <jni.h>
    /* Header for class kim_hsl_jni_Main */
    
    #ifndef _Included_kim_hsl_jni_Main
    #define _Included_kim_hsl_jni_Main
    #ifdef __cplusplus
    extern "C" {
    #endif
    /*
     * Class:     kim_hsl_jni_Main
     * Method:    jniTest
     * Signature: (ILjava/lang/String;)V
     */
    JNIEXPORT void JNICALL Java_kim_hsl_jni_Main_jniTest
      (JNIEnv *, jclass, jint, jstring);
    
    #ifdef __cplusplus
    }
    #endif
    #endif

##### X . 总结

* * *

**1 . 创建 Java 代码 : IntelliJ IDEA Community 中创建 Java 项目 , 并定义 Native 方法 ;**

复制
    
    
        /**
         * 定义一个 Native 方法
         * @param i
         * @param s
         */
        public static native void jniTest(int i, String s);

**2 . C++ 实现 Native 方法 : 在 Visual Studio Community 2019 中创建 CMake 项目 , 使用 C++ 开发 , 实现上面 Java 中声明的 Native 方法 , 并在 CMake 中配置生成动态库 ;**

① C++ 代码 :

复制
    
    
    // 009_Cmake.cpp: 定义应用程序的入口点。
    
    
    //导入 JNI 的头文件 , 该头文件在 D:/Program Files/Java/jdk1.8.0_221/include 目录中
    //	JDK 的安装目录 , 每个人的安装目录可能不一致
    #include <jni.h>
    
    //C++ 中实现 Java 的 Native 方法
    
    //JNI 方法格式 : 
    //  extern "C" : 如果是在 C++ 文件 ( .cpp 后缀源码 ) 中实现 Native 方法 , 需要兼容 C 语言
    //               如果在 C 文件 ( .c 后缀源码 ) 中 , 则不用添加该选项
    // 	JNIEXPORT 返回值类型 JNICALL 方法名 ( 参数列表 )
    //  方法名规范 : Java_包名_类名_方法名
    //  参数列表 : 
    //      第一个参数必定是 JNI 环境参数 , 即 JNIEnv 类型的 指针
    //      第二个参数必定是 定义 Native 方法的 Java 类对象
    //      从第三个开始就是定义的 Java 中的 Native 方法的参数 , 注意要使用 java 的替代数据类型
    
    extern "C"
    JNIEXPORT void JNICALL
    Java_kim_hsl_jni_Main_jniTest(JNIEnv* env, jobject instance, jint i, jstring s_) {
    
        const char* s = env->GetStringUTFChars(s_, 0);
    
        // 打印传入的 两个参数
        printf("Java_kim_hsl_jni_Main_jniTest : %d , %s\n", i , s);
    
        env->ReleaseStringUTFChars(s_, s);
    }

**② CMake 动态库配置 :**

复制
    
    
    # CMakeList.txt: 009_Cmake 的 CMake 项目，在此处包括源代码并定义
    # 项目特定的逻辑。
    #
    cmake_minimum_required (VERSION 3.8)
    
    #配置 JNI 头文件
    include_directories("D:/Program Files/Java/jdk1.8.0_221/include")
    include_directories("D:/Program Files/Java/jdk1.8.0_221/include/win32")
    
    
    # 设置生成 动态库
    # 配置格式是 : 动态库名称 动态库标识( SHARED ) 包含的源文件( 如果有多个就写多个 )
    add_library( 009_Cmake SHARED 009_Cmake.cpp 009_Cmake.h )
    
    
    
    # 将源代码添加到此项目的可执行文件。
    #add_executable (009_Cmake "009_Cmake.cpp" "009_Cmake.h")
    
    # TODO: 如有需要，请添加测试并安装目标。

**3 . Java 加载 动态库 : 通过动态库的绝对路径加载该动态库 , 并执行 ;**

复制
    
    
    package kim.hsl.jni;
    
    public class Main {
    
        static {
            //Visual Studio 中生成的 DLL 动态库路径是
            //  Y:\002_WorkSpace\002_VS\009_Cmake\out\build\x64-Debug\009_Cmake\009_Cmake.dll
            //  直接使用该绝对路径加载动态库即可
            System.load(
                    "Y:\\002_WorkSpace\\002_VS\\009_Cmake\\out\\build\\x64-Debug\\009_Cmake\\009_Cmake.dll");
        }
    
        public static void main(String[] args) {
    
            //打印结果 : Java_kim_hsl_jni_Main_jniTest : 1 , Hello JNI
            jniTest(1 , "Hello JNI");
    
        }
    
        /**
         * 定义一个 Native 方法
         * @param i
         * @param s
         */
        public static native void jniTest(int i, String s);
    }

> **关于项目两个工程的说明 , 相关的路径有可能改变 , 如 CMake 中配置 jni.h 头文件路径 , Java 中加载 VS 中生成的动态库路径 , 注意要修改成自己的项目路径 ;**

本文参与 [腾讯云自媒体同步曝光计划](https://cloud.tencent.com/developer/support-plan)，分享自作者个人站点/博客。

原始发表：2020-01-22，如有侵权请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除

[java](https://cloud.tencent.com/developer/tag/10164)

[编译](https://cloud.tencent.com/developer/tag/17190)

[工具](https://cloud.tencent.com/developer/tag/17276)

[开发](https://cloud.tencent.com/developer/tag/17337)

[配置](https://cloud.tencent.com/developer/tag/17393)

目录

  *     *     *     *     *     *     *     *     *     *     * 


[问题归档](https://cloud.tencent.com/developer/ask/archives.html)[专栏文章](https://cloud.tencent.com/developer/column/archives.html)[快讯文章归档](https://cloud.tencent.com/developer/news/archives.html)[关键词归档](https://cloud.tencent.com/developer/information/all.html)[开发者手册归档](https://cloud.tencent.com/developer/devdocs/archives.html)[开发者手册 Section 归档](https://cloud.tencent.com/developer/devdocs/sections_p1.html)
