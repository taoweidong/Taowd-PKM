---
source: "http://jingyan.baidu.com/article/380abd0a7190061d90192cce.html"
title: "如何修改Linux文件的属性与权限-百度经验"
fetched_at: "2026-10-05 15:35:49"
---

# 如何修改Linux文件的属性与权限

  * 原创
  * |
  * 浏览：23560
  * |
  * 更新：2014-09-02 19:31
  * |
  * 标签：[linux](/tag?tagName=linux)

  * [](/album/380abd0a7190061d90192cce.html?picindex=1)1

  * [](/album/380abd0a7190061d90192cce.html?picindex=2)2

  * [](/album/380abd0a7190061d90192cce.html?picindex=3)3

  * [](/album/380abd0a7190061d90192cce.html?picindex=4)4

  * [](/album/380abd0a7190061d90192cce.html?picindex=5)5

  * [](/album/380abd0a7190061d90192cce.html?picindex=6)6

[分步阅读](/album/380abd0a7190061d90192cce.html)

文件权限对于一个系统的安全是很重要的，那么如何修改一个文件的属性与权限呢？

## [](javascript:;)工具/原料

  * redhat6

## [](javascript:;)方法/步骤

  1. 1

打开Linux系统，建立一个目录。建立目录命令为【mkdir】。并用【ls】命令查看目录相关信息，如图，我们知道test的权限为rwxr-xr-x。

  2. 2

chgrp:改变文件所属用户组。命令格式为：chgrp 用户名 文件或目录。如图，用户组原为root，现在被修改到nerd用户组。

  3. 3

chown:改变文件所有者。命令格式为：chown 所有者 文件或目录。如图，目录所属者原来为root，用chown该所属者为bin。

  4. 4

chmod:改变文件的权限。命令格式为：chmod 权限属性 文件或目录。如图原来目录的权限为rwxr-xr-x，后来修改为rwxrwxrwx。

  5. 5

查看三个命令的具体用法，这里可以借助【man】命令，查看chgrp、chown、chmod的相关参数与具体用法。

END

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
