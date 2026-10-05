---
source: "https://blog.whsir.com/post-2325.html"
title: "jenkins更新后出现JNLP-connect,JNLP2-connect警告 - 吴昊博客"
fetched_at: "2026-10-05 15:30:10"
---

# jenkins更新后出现JNLP-connect,JNLP2-connect警告

__2018年1月20日  __[wuhao](https://blog.whsir.com/post-author/wuhao "显示 wuhao 作者所有文章")

__[1条评论](https://blog.whsir.com/post-2325.html#comments)  __11,500次浏览

[](https://blog.whsir.com/post-2325.html "jenkins更新后出现JNLP-connect,JNLP2-connect警告")

在更新jenkins后出现提示

This Jenkins instance uses deprecated protocols: JNLP-connect,JNLP2-connect. It may impact stability of the instance. If newer protocol versions are supported by all system components (agents, CLI and other clients), it is highly recommended to disable the deprecated protocols. Protocol Configuration

这段话大概意思

这个Jenkins实例使用了废弃的协议:JNLP-connect,JNLP2-connect。这可能会影响实例的稳定性。如果所有系统组件(代理、CLI和其他客户端)均支持较新的协议版本，那么强烈建议禁用已弃用的协议。

解决办法：

点击Protocol Configuration→Agents→点击Agent protocols...→取消勾选Protocol/1和Protocol/2→保存即可

![](https://cdn.whsir.com/wp-content/themes/wh-blog/images/loading.gif)

![](https://cdn.whsir.com/wp-content/uploads/2018/01/jenkinsw.png)

[![](https://cdn.whsir.com/wp-content/themes/wh-blog/images/loading.gif)](https://www.aliyun.com/minisite/goods?userCode=8dtjsmgb) ![](/image/2019111160097.jpg)

原文链接：[jenkins更新后出现JNLP-connect,JNLP2-connect警告](https://blog.whsir.com/post-2325.html)，转载请注明来源！

~微信打赏~

![](https://blog.whsir.com/image/wxpay.png)

![](https://blog.whsir.com/image/alipay.png)

![](https://blog.whsir.com/image/alihb.png)

  *   *   * 


[赏](javascript:void\(0\);)

[__赞 4 ](javascript:;)

分享到：
