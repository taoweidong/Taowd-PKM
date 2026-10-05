---
source: "https://www.cnblogs.com/jingridong/p/6385661.html"
title: "WPF性能调试系列 – 内存监测 - want - 博客园"
fetched_at: "2026-10-05 15:44:36"
---

**WPF性能调试系列文章：**

 _[WPF页面渲染优化：Application Timeline](http://www.cnblogs.com/jingridong/p/6097240.html)_

[ _WPF页面业务加载优化：Ants Performance Profiler_](http://www.cnblogs.com/jingridong/p/6382676.html)

_[WPF内存优化：Ants Memory Profiler](http://www.cnblogs.com/jingridong/p/6385661.html)_

内存监测(Ants Memory Profiler)

Ants Memory Profiler是专门针对于.net程序的内存动态分析工具，通过实时监测WPF程序中每个对象分配的内存空间大小，来提供多样式报告展示内存的使用情况。我们可根据分析结果进行指定对象的优化。

从RedGate官网下载，下载地址为<http://www.red-gate.com/products/dotnet-development/ants-memory-profiler/>

模拟分析应用程序

打开Ants Memory Profiler，通过菜单File -> New Profiling Session...（Ctrl+N）打开新的监测会话，在可监测程序类型中选择.Net executable。

![](https://images2015.cnblogs.com/blog/45506/201702/45506-20170210111416666-218954005.png)

开始执行后，wpf应用会打开执行，操作应用并实时监测内存使用情况，对于内存使用较高地方进行Take Memory Snapshot：

![](https://images2015.cnblogs.com/blog/45506/201702/45506-20170210111508541-177670933.png)

注:一次内存分析可进行多次内存点拍照。比如程序刚运行进行拍照，运行一段时间之后再次拍照，这样可通过对比两次拍照的内存差别分析出对象占用内存情况，更便于分析问题。

****

一个拍照监测点结果分析：

![](https://images2015.cnblogs.com/blog/45506/201702/45506-20170210111554682-1011489287.png)

**可参考具体详解：**<https://documentation.red-gate.com/display/AMP8/The+summary+page>

注:1. 托管对象如果内存使用过高，考虑是否缓存数据过大，托管资源一般无需过多考虑，可等待.net垃圾回收器进行自行回收。

2\. 非托管资源如果占用内存过高，需要进行手动释放，因为费托管资源是无法自动被.net垃圾回收器回收 – 非托管资源包括：GUI+，图片操作，文件操作，win32调用等

多个拍照监测点结果对比分析：

![](https://images2015.cnblogs.com/blog/45506/201702/45506-20170210113726307-1635492018.png)

具体类视图分析：

![](https://images2015.cnblogs.com/blog/45506/201702/45506-20170210113747213-479684421.png)

**可参考具体详解：**<https://documentation.red-gate.com/display/AMP8/The+class+list>

****

具体对象分析：

![](https://images2015.cnblogs.com/blog/45506/201702/45506-20170210113829682-277605652.png)

**可参考具体详解：**<https://documentation.red-gate.com/display/AMP8/The+instance+list>

****

**内存泄露主要原因分析：静态引用、未注销的事件绑定、非托管代码资源使用等。对于静态对象尽量小或者不用，非托管资源可通过手动Dispose来释放。**
