---
type: concept
tags: [wiki, 收藏夹Ingest, android]
created: 2026-10-05
updated: 2026-10-06
source: "[[topics/browser-bookmarks]]"
---

# Android 开发（收藏夹 Ingest）

> 编译自 [[topics/browser-bookmarks]] 的「Android 开发」主题（共 13 条）。本页为分类知识页：按子类别归类书签，便于回看与检索。

## 摘要

本主题共 13 条，早期 Android 开发收藏：Eclipse+SDK 环境、百度地图/LBS 定位、源码下载、毕业设计参考与多线程基础。体量小，属历史技术栈。

## 详情

### 环境 / 工具（4）

- [Android开发之位置定位详解与实例解析（GPS定位、Google网络定位，BaiduLBS（SDK）定位） - Android移动开发技术文章_手机开发 - 红黑联盟](http://www.2cto.com/kf/201407/321688.html)
- [Android离线打包 - DCloud问答](http://ask.dcloud.net.cn/article/38)
- [android开发工具 Eclipse+Android SDK+ADT](http://txlong-onz.iteye.com/blog/870650)
- [在Eclipse下搭建Android开发环境教程](http://mobile.51cto.com/android-227548.htm)

### 定位 / 地图 / LBS（2）

- [Android百度地图开发（一）之初体验 - crazy_jack - 博客频道 - CSDN.NET](http://blog.csdn.net/crazy1235/article/details/42614603)

### 源码 / 教程 / 毕业设计（3）

- [Android毕业设计题目_文库163毕业设计(论文)网](http://www.wenku163.com/computer/android/1.html)
- [安卓源码,android源码下载,app源码 - A5源码](http://down.admin5.com/android/)

### 其他 / 综合（4）

- [http://blog.csdn.net/yzhj2005/article/details/6980676/](http://blog.csdn.net/yzhj2005/article/details/6980676/)
- [ssi框架学习总结 - OPEN 开发经验库](http://www.open-open.com/lib/view/open1377581482589.html)
- [安卓设计类 - 免费_毕业课程范例设计_双鱼林毕业课程范例设计网 - 双鱼林毕业课程范例设计网](http://www.shuangyulin.com/article/list_27.html)
- [生产者消费者多线程pthread_百度文库](http://wenku.baidu.com/view/091dacd03186bceb19e8bbdb.html)

## 网络精选（高质量博客 · 2026-10-06 增补）

> 2026-10-06 网络检索并下载 10 篇仍在线的高质量博客（覆盖 Kotlin 协程/Flow、Jetpack Compose、架构、性能/冷启动、模块化/Gradle、JNI/NDK 等子方向），本地镜像目录见 [[wiki-system/sources/curated-android]]。

### 摘要

- **Kotlin 协程 / Flow**：结构化并发是边界纪律——协程必须挂在 `viewModelScope`/`lifecycleScope` 等生命周期作用域，绝不用 `GlobalScope`；UI 状态用 `StateFlow`（热流、始终持有当前值），一次性事件（导航、Snackbar）用 `SharedFlow`（不重放）；并行且需失败隔离用 `supervisorScope`。
- **架构选型（MVVM / MVI / Clean）**：MVVM 是 Google 一手支持的默认基线（ViewModel + StateFlow），适合约 80% 屏幕；复杂交互状态用 MVI（单向数据流、单一不可变状态）；Clean Architecture 按表现/领域/数据分层解耦，不替代 MVVM/MVI 而是叠加其上；生产实践多为「按 feature 模块局部选用」的务实混合。
- **Jetpack Compose 状态**：Compose 是声明式 UI，UI 是 state 的函数；用 `remember` + `mutableStateOf` 在重组间保留并观察状态；状态提升（state hoisting）把状态上移到最近公共祖先，使可组合项无状态、可复用；重组只重绘读取了变化状态的节点。
- **冷启动 / 性能**：冷启动是第一印象指标（用户约 1.5s 内决定留存），优先优化；先用 `adb am start -W` 取中位数、再用 Macrobenchmark 跟踪；最大头是 `Application.onCreate`（瘦身、延迟非必要初始化、用 App Startup 库减少 ContentProvider）；Baseline Profiles 在安装时让 ART 预编译热路径，常带来 20–40% 冷启动提升，是性价比最高的优化之一。
- **模块化 / Gradle 构建**：用 `build-logic` 复合构建 + Convention Plugins 替代 `buildSrc`（避免每次改动使整个配置缓存失效），配合 TOML Version Catalogs 的 bundles；模块化是「依赖图问题」而非「模块数量问题」——扁平化依赖图才能让 Gradle 真正并行编译（某 42 模块项目增量构建从 47s 降到 28s，CI 墙钟时间降 55%）。

### 高质量博客镜像

| 主题 | 博客标题 | 本地镜像 |
| --- | --- | --- |
| 架构 | Android Architecture: MVVM, Clean Architecture, and MVI | [[wiki-system/sources/curated-android/blog_hashhackers_com_blog_android-architecture-guide_f2d72bf7.md\|Android Architecture 指南(MVVM/Clean/MVI)]] |
| 架构 | Android App Architecture — MVVM vs MVI vs Clean Architecture | [[wiki-system/sources/curated-android/anaksor_com_learning-center_guides_android-app-architecture-mvvm-vs-mvi-vs-clean-a_4bee3529.md\|MVVM vs MVI vs Clean 对比]] |
| Gradle 构建 | Gradle Kotlin DSL Tips — Version Catalogs, Convention Plugins & Build Optimization | [[wiki-system/sources/curated-android/pcsalt_com_android_gradle-kotlin-dsl-tips_092ed3c5.md\|Gradle Kotlin DSL 技巧]] |
| 模块化/Gradle | Modularizing Your Android Build with Convention Plugins and Version Catalogs | [[wiki-system/sources/curated-android/mvpfactory_io_blog_modularizing-your-android-build-with-convention-plugins-and-versi_a390c6e3.md\|Convention Plugins 模块化构建]] |
| Kotlin 协程/Flow | Scalable Kotlin Coroutines and Flow Patterns for Android | [[wiki-system/sources/curated-android/blog_michaelsam94_com_kotlin-coroutines-flow-patterns_383758d9.md\|可扩展的协程与 Flow 模式]] |
| JNI/NDK | Understanding JNI in Android | [[wiki-system/sources/curated-android/www_basantasapkota026_com_np_2025_06_understanding-jni-in-android_html_36f563b1.md\|理解 Android JNI]] |
| JNI/NDK | 【Android NDK 开发】Visual Studio 2019 使用 CMake 开发 JNI 动态库 | [[wiki-system/sources/curated-android/cloud_tencent_com_developer_article_2246756_b3e00ba6.md\|VS2019+CMake 开发 JNI 动态库]] |
| Jetpack Compose | Jetpack Compose Tutorial #5: State — The Most Important Concept | [[wiki-system/sources/curated-android/kemalcodes_com_posts_jetpack-compose-tutorial-state_fbf9dbdc.md\|Compose 状态管理教程]] |
| 性能/冷启动 | App Startup Optimization — Measure, Trim, and Ship Baseline Profiles | [[wiki-system/sources/curated-android/www_androidnewworld_com_post_app-startup-optimization-measure-trim-and-ship-baseline-profiles_a2552980.md\|冷启动优化与 Baseline Profiles]] |
| 性能/冷启动 | Android Baseline Profiles: the CI pipeline that cut cold start by 35% | [[wiki-system/sources/curated-android/mvpfactory_io_blog_android-baseline-profiles-beyond-the-basics-custom-macro-benchmar_509cd8b7.md\|Baseline Profiles CI 流水线]] |

## 关联

- 来源索引：[[topics/browser-bookmarks]]（Android 开发 主题共 13 条）

## 引用来源

- 各原始链接见上文，编目于 2026-10-05
- 原始收藏：[[90-待整理与临时笔记/favorites_2026_10_5]]

## 变更记录

- 2026-10-05：Ingest「Android 开发」主题 13 条，按子类别归类（分类知识页）。
- 2026-10-06：网络检索并下载 10 篇仍在线的高质量博客至 sources/curated-android/，新增「网络精选」合成知识段。
