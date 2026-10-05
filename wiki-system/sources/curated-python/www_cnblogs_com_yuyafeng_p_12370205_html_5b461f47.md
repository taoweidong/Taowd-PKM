---
source: "https://www.cnblogs.com/yuyafeng/p/12370205.html"
title: "Django使用cookiecutter - yyfgrd - 博客园"
fetched_at: "2026-10-05 15:42:24"
---

cookiecutter是一款快https://github.com/pydanny/cookiecutter-django.git速搭建项目的命令行工具

cookiecuter是用来建立项目的工程模板， 也就是在开始创建项目的时候不需要手动创建一大堆东西， cookiecutter可以将初始化项目的时候需要的东西全部集成出来， 这样效率就可以高很多

安装


     pip install cookiecutter

使用

在github的<https://github.com/cookiecutter/cookiecutter>中找到django-cookiecutter把他的模板复制下来

https://github.com/pydanny/cookiecutter-django.git


    $ cookiecutter https://github.com/pydanny/cookiecutter-django.git

然后出现配置过程


    project_name [My Awesome Project]: myproject  # 项目名称
    project_slug [myproject]: app01  # slug
    description [Behold My Awesome Project!]: This is the first application!  # 项目描述
    author_name [Daniel Roy Greenfeld]: yourname  # 作者
    domain_name [example.com]: example.com  # 部署的域名
    email [__jack__@example.com]: imooc@imooc.com  # 邮箱
    version [0.1.0]:  # 版本号，默认为0.1.0
    Select open_source_license:  # 选择项目License
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 (1, 2, 3, 4, 5) [1]: 5
    timezone [UTC]: Asia/Shanghai  # Django settings中的TIME_ZONE
    windows [n]: n # 是否是Windows环境
    use_pycharm [n]: y  # 是否使用Pycharm开发
    use_docker [n]: y  # 是否使用Docker容器
    Select postgresql_version:  # 选择Postgres数据库版本，cookiecutter-django默认只支持Postgres
    1 - 10.5
    2 - 10.4
    3 - 10.3
    4 - 10.2
    5 - 10.1
    6 - 9.6
    7 - 9.5
    8 - 9.4
    9 - 9.3
    Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 (1, 2, 3, 4, 5, 6, 7, 8, 9) [1]: 1
    Select js_task_runner:  # js运行方式
    1 - None
    2 - Gulp
    Choose from 1, 2 (1, 2) [1]: 1
    custom_bootstrap_compilation [n]: n  # 是否自定义bootstrap压缩
    use_compressor [n]: n  # 是否使用压缩
    use_celery [n]: n  # 是否使用celery，一个异步任务队列
    use_mailhog [n]: n  # 是否使用mailhog，Django项目中发送邮件的，也可以使用Mailgun代替
    use_sentry [n]: n  # 是否使用错误日志日志监控，sentry也是不错的开源python项目
    use_whitenoise [n]: y  # 是否使用whitenoise
    use_heroku [n]: n  # 是否使用heroku，heroku是国外著名的云服务厂商之一，提供PaaS
    use_travisci [n]: n  # 是否使用travisci，类似于jekins，用于DevOps中的持续集成与发布
    keep_local_envs_in_vcs [y]: y  # 对于本地环境变量使用版本控制
    debug [n]: y  # 是否开启debug模式，settings中配置
     [SUCCESS]: Project initialized, keep up the good work!
