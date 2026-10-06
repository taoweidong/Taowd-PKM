---
type: concept
tags: [wiki, 收藏夹Ingest, python]
created: 2026-10-05
updated: 2026-10-06
source: "[[topics/browser-bookmarks]]"
---

# Python 技术（收藏夹 Ingest）

> 编译自 [[topics/browser-bookmarks]] 的「Python」主题（共 21 条）。本页为分类知识页：按子类别归类书签，便于回看与检索。

## 摘要

本主题共 21 条，Python 入门到工程化：廖雪峰基础、Django/Flask/FastAPI 选型、SQLAlchemy、Scrapy 爬虫、Pandas、paramiko 运维、pip/多进程。与作者现用 Python(FastAPI) 技术栈衔接。

## 详情

### 基础 / 教程（3）

- [Python基础 - 廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/897692888725344/897693149004224)
- [《Think Python 2e》最新版中文翻译 — 《Think Python 2e》中译本 1.0 文档](https://codingpy.com/books/thinkpython2/index.html)
- [数据类型和变量 - 廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/897692888725344/897693179535744)

### Web 框架（4）

- [(130条消息) SQLAlchemy简明教程_stone0823的博客-CSDN博客_sqlalchemy](https://blog.csdn.net/stone0823/article/details/112344065)
- [Django使用cookiecutter - yyfgrd - 博客园](https://www.cnblogs.com/yuyafeng/p/12370205.html)
- [Django，Flask ，FastAPI的区别有哪些 - 开发技术 - 亿速云](https://www.yisu.com/zixun/483075.html)
- [欢迎来到 Jinja2 — Jinja2 2.7 documentation](http://docs.jinkan.org/docs/jinja2/)

### 爬虫 / 数据（3）

- [Pandas是什么](http://c.biancheng.net/pandas/what-is-pandas.html)
- [Scrapy 0.24 文档](https://scrapy-chs.readthedocs.io/zh_CN/0.24/index.html)
- [Scrapy 中文网](http://www.scrapyd.cn/)

### 运维 / 部署（5）

- [(6条消息)python利用paramiko库远程连接Linux服务器上传文件并执行命令_运维_实践求真知-CSDN博客](https://blog.csdn.net/chengqiuming/article/details/86515656)
- [windows下设置pip国内源_pip 源 windows_zhoyuwo的博客-CSDN博客](https://blog.csdn.net/zhoyuwo/article/details/100140034)
- [关于command 'gcc' failed with exit status 1 解决方法 - gerrydeng - 博客园](https://www.cnblogs.com/gerrydeng/p/7159021.html)
- [详解Linux安装GCC方法 - 习惯沉淀 - 博客园](https://www.cnblogs.com/yadongliang/p/6100003.html)

### 包管理 / 并发（3）

- [PyPI – the Python Package Index · PyPI](https://pypi.org/)
- [multiprocessing --- 基于进程的并行 — Python 3.10.5 文档](https://docs.python.org/zh-cn/3/library/multiprocessing.html#using-a-pool-of-workers)
- [【Python】Python多进程详解 - 知乎](https://zhuanlan.zhihu.com/p/493699150)

### 其他 / 综合（3）

- [Downloads for win32](http://dl.mongodb.org/dl/win32/x86_64)
- [MongoDB Download Center | MongoDB](https://www.mongodb.com/download-center/community)
- [Welcome to Python.org](https://www.python.org/)

## 网络精选（高质量博客 · 2026-10-06 增补）

> 从全网检索并下载 10 篇仍在线的高质量博客（覆盖 asyncio 异步、装饰器/元编程、类型注解、性能/内存、Web 框架），本地镜像见 [[wiki-system/sources/curated-python]]。

### 摘要

- **asyncio 异步编程**：asyncio 是单线程协作式并发——事件循环在 `await` 点切换协程，一次阻塞调用（`requests.get`、`time.sleep`）会冻结整个事件循环、所有协程停顿；生产模式用 `gather(return_exceptions=True)`、超时（`wait_for`/`asyncio.timeout`）、`run_in_executor` 卸载阻塞/CPU 工作，Python 3.11+ 优先用 `TaskGroup` 做结构化并发。
- **装饰器 / 元编程**：装饰器是高阶函数，用 `@functools.wraps` 保留原函数 `__name__`/`__doc__`/注解；带参装饰器需三层嵌套（工厂）；类装饰器适合有状态场景；典型用途为日志、重试、缓存（`lru_cache`）、鉴权。
- **类型注解 / typing**：`typing` 模块提供类型提示词汇（`type` 语句类型别名、`NewType`、`Generic`、`Callable`、`Protocol` 等），类型提示仅由静态检查器（mypy）强制执行、运行时不强制；PEP 484/585/604 等标准化，新特性经 `typing_extensions` 向下移植。
- **性能 / 内存**：先测量再优化——`cProfile` 定位耗时函数、`timeit` 做微基准、`tracemalloc` 追踪内存分配；常见修复为列表推导/生成器、`"".join` 替代 `+=`、`__slots__` 与生成器显著降低内存占用。
- **Web 框架（FastAPI）**：FastAPI 以 async 优先 + Pydantic v2 校验 + `Depends` 依赖注入见长；生产要点包括 `lifespan` 管理连接池、router/service/repository 分层、全局异常处理、结构化日志、Gunicorn+Uvicorn 部署。

### 下载清单

| 主题 | 博客标题 | 本地镜像 |
| --- | --- | --- |
| asyncio | Developing with asyncio — Python 3.14.8 文档 | [[wiki-system/sources/curated-python/docs_python_org_3_library_asyncio-dev_html_25ec51b0.md\|asyncio 官方开发指南]] |
| asyncio | Asynchronous Programming in Python: From asyncio Basics to Production Patterns | [[wiki-system/sources/curated-python/pythoneo_com_asynchronous-programming-in-python_47b8a151.md\|异步编程：从基础到生产模式]] |
| asyncio | Python Concurrency: Python asyncio — 47-Second Freeze | [[wiki-system/sources/curated-python/thecodeforge_io_python_python-asyncio-deep-dive_4484d51c.md\|asyncio 深入：47 秒冻结事故]] |
| asyncio | Complete Guide to Python Asyncio | [[wiki-system/sources/curated-python/stackpractices_com_guides_complete-guide-python-asyncio_a18ffec6.md\|Python Asyncio 完全指南]] |
| 装饰器 | Mastering Advanced Decorator Patterns | [[wiki-system/sources/curated-python/course4all_com_python_py-decorators-mastery_04ec5c28.md\|进阶装饰器模式]] |
| 类型注解 | typing — 对类型提示的支持（Python 3.13.16 文档） | [[wiki-system/sources/curated-python/docs_python_org_zh-cn_3_13_library_typing_html_bfa847f7.md\|typing 官方文档]] |
| 类型注解 | Getting started — mypy 2.4.0 documentation | [[wiki-system/sources/curated-python/mypy_readthedocs_io_en_stable_getting_started_html_d8253346.md\|mypy 入门]] |
| 性能/内存 | Python Performance Profiling: Find Bottlenecks and Optimize Slow Code | [[wiki-system/sources/curated-python/www_worldprogramming_org_posts_python-performance-profiling-find-bottlenecks-and-optimize-slow-_a2243bc5.md\|性能剖析：定位瓶颈]] |
| 性能/内存 | How do I profile memory usage in Python? | [[wiki-system/sources/curated-python/codemia_io_knowledge-hub_path_how_do_i_profile_memory_usage_in_python_fbf99248.md\|内存分析方法]] |
| Web 框架 | FastAPI Backend Patterns: DI, Error Handling, and Async | [[wiki-system/sources/curated-python/openllm_wavise_com_blog_fastapi-backend-patterns_cfd3556e.md\|FastAPI 后端模式]] |

## 关联

- 来源索引：[[topics/browser-bookmarks]]（Python 主题共 21 条）
- 项目体系：[[entities/project-fullstack-admin]]、[[concepts/curated-opensource-projects]]

## 引用来源

- 各原始链接见上文，编目于 2026-10-05
- 原始收藏：[[90-待整理与临时笔记/favorites_2026_10_5]]

## 变更记录

- 2026-10-05：Ingest「Python」主题 21 条，按子类别归类（分类知识页）。
- 2026-10-06：网络检索并下载 10 篇仍在线的高质量博客至 sources/curated-python/，新增「网络精选」合成知识段（原 12 篇中 2 篇 techoral.com 仅抓到目录为 JS 渲染空壳，已剔除）。
