---
source: "https://www.cnblogs.com/gerrydeng/p/7159021.html"
title: "关于command 'gcc' failed with exit status 1 解决方法 - gerrydeng - 博客园"
fetched_at: "2026-10-05 15:42:37"
---

# Python踩坑之路

* * *

## Setup script exited with error: command 'gcc' failed with exit status 1

由于没有正确安装Python开发环境导致。

### Debin/Ubuntu

  * Python2
`sudo apt-get install python-dev`
  * Python3
`sudo apt-get install python3-dev`
可能需要libevent库
`sudo apt-get install libevent-dev`
最后更新下开发环境
`sudo apt-get groupinstall 'development tools'`

### Centos/Fedora

`sudo yum install python-devel`
`sudo yum install libevent-devel`
`easy_install gevent`
或者
`pip install gevent`
把环境更新下
`sudo yum install groupinstall 'development tools'`
