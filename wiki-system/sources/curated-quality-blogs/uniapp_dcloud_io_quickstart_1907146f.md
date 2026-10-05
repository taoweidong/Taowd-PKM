---
source: "https://uniapp.dcloud.io/quickstart"
title: "uni-app快速上手 | uni-app官网"
fetched_at: "2026-10-05 15:43:14"
---

[uni-app快速上手](/quickstart.html#uni-app快速上手 "uni-app快速上手")

[1\. 通过 HBuilderX 可视化界面](/quickstart.html#_1-通过-hbuilderx-可视化界面 "1. 通过 HBuilderX 可视化界面")

[创建uni-app](/quickstart.html#创建uni-app "创建uni-app")

[运行uni-app](/quickstart.html#运行uni-app "运行uni-app")

[发布uni-app](/quickstart.html#发布uni-app "发布uni-app")

[打包为原生App（云端）](/quickstart.html#打包为原生app-云端 "打包为原生App（云端）")

[打包为原生App（离线）](/quickstart.html#打包为原生app-离线 "打包为原生App（离线）")

[发布为H5](/quickstart.html#发布为h5 "发布为H5")

[发布为小程序](/quickstart.html#发布为小程序 "发布为小程序")

[环境安装](/quickstart.html#环境安装 "环境安装")

展示全部

## # uni-app快速上手

> `uni-app`支持通过 可视化界面、[`vue-cli`命令行 ](https://uniapp.dcloud.io/quickstart?id=%e9%80%9a%e8%bf%87vue-cli%e5%91%bd%e4%bb%a4%e8%a1%8c) 两种方式快速创建项目。

### # 1\. 通过 HBuilderX 可视化界面

可视化的方式比较简单，HBuilderX内置相关环境，开箱即用，无需配置nodejs。

开始之前，开发者需先下载安装如下工具：

  * HBuilderX：[官方IDE下载地址 ](https://www.dcloud.io/hbuilderx.html)

HBuilderX是通用的前端开发工具，但为`uni-app`做了特别强化。

下载App开发版，可开箱即用；如下载标准版，在运行或发行`uni-app`时，会提示安装`uni-app`插件，插件下载完成后方可使用。

如使用`cli`方式创建项目，可直接下载标准版，因为uni-app编译插件被安装到项目下了。

## # 创建uni-app

在点击工具栏里的文件 -> 新建 -> 项目：

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/create1.png)

选择`uni-app`类型，输入工程名，选择模板，点击创建，即可成功创建。

uni-app自带的模板有 Hello uni-app ，是官方的组件和API示例。还有一个重要模板是 uni ui项目模板，日常开发推荐使用该模板，已内置大量常用组件。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/create-uniapp.jpg)

## # 运行uni-app

  1. 浏览器运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到浏览器 -> 选择浏览器，即可在浏览器里面体验uni-app 的 H5 版。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/run-chrome.png)

  2. 真机运行：连接手机，开启USB调试，进入hello-uniapp项目，点击工具栏的运行 -> 真机运行 -> 选择运行的设备，即可在该设备里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/run-phone.png)

如手机无法识别，请点击菜单运行-运行到手机或模拟器-真机运行常见故障排查指南。 注意目前开发App也需要安装微信开发者工具。

  3. 在微信开发者工具里运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 微信开发者工具，即可在微信开发者工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-1.png)

**注意：**如果是第一次使用，需要先配置小程序ide的相关路径，才能运行成功。如下图，需在输入框输入微信开发者工具的安装路径。 若HBuilderX不能正常启动微信开发者工具，需要开发者手动启动，然后将uni-app生成小程序工程的路径拷贝到微信开发者工具里面，在HBuilderX里面开发，在微信开发者工具里面就可看到实时的效果。

uni-app默认把项目编译到根目录的unpackage目录。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/weixin-setting.png)

  4. 在支付宝小程序开发者工具里运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 支付宝小程序开发者工具，即可在支付宝小程序开发者工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-3.png)

  5. 在百度开发者工具里运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 百度开发者工具，即可在百度开发者工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-2.png)

  6. 在抖音开发者工具里运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 抖音开发者工具，即可在抖音开发者工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-4.png)

  7. 在360开发工具中导入：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 360开发工具，即可在360开发工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-app-debug-mp-360.png)

  8. 在快应用联盟工具里运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 快应用联盟工具，即可在快应用联盟工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-app-run-debug-quickapp-webview.png)

  9. 在华为开发者工具里运行：进入hello-uniapp项目，点击工具栏的运行 -> 运行到小程序模拟器 -> 华为开发者工具，即可在华为开发者工具里面体验uni-app。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-app-run-release-quickapp-webview-huawei.png)

  10. 在QQ小程序开发工具里运行：内容同上，不再重复。

**Tips**

  * 如果是第一次使用，需要配置开发工具的相关路径。点击工具栏的运行 -> 运行到小程序模拟器 -> 运行设置，配置相应小程序开发者工具的路径。
  * 支付宝/百度/抖音/360小程序工具，不支持直接指定项目启动并运行。因此开发工具启动后，请将 HBuilderX 控制台中提示的项目路径，在相应小程序开发者工具中打开。
  * 如果自动启动小程序开发工具失败，请手动启动小程序开发工具并将 HBuilderX 控制台提示的项目路径，打开项目。

运行的快捷键是`Ctrl+r`。 HBuilderX 还提供了快捷运行菜单，可以按数字快速选择要运行的设备：

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/runtool.png)

如需调试，可参考：[uni-app调试](/tutorial/run-and-debug.html)

## # 发布uni-app

### # 打包为原生App（云端）

在HBuilderX工具栏，点击发行，选择原生app-云端打包，如下图：

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-11.png)

出现如下界面，点击打包即可。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-pack-cloud.png)

### # 打包为原生App（离线）

`uni-app` 支持离线打包，在 HBuilderX 发行菜单里生成离线打包资源，然后参考离线打包文档操作，可以从HBuilderX的发行菜单里找到文档链接，也可以直接访问：<https://nativesupport.dcloud.net.cn/AppDocs/README>[ ](https://nativesupport.dcloud.net.cn/AppDocs/README)。

在HBuilderX工具栏，点击发行，选择本地打包，如下图，点击即可生成离线打包资源。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-12.png)

### # 发布为H5

  1. 在 `manifest.json` 的可视化界面，进行如下配置（发行在网站根目录可不配置应用基本路径），此时发行网站路径是 www.xxx.com/h5，如：<https://hellouniapp.dcloud.net.cn>[ ](https://hellouniapp.dcloud.net.cn)。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/build-h5-1.png)

  2. 在HBuilderX工具栏，点击发行，选择网站-H5手机版，如下图，点击即可生成 H5 的相关资源文件，保存于 unpackage 目录。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-10.png)

**注意**

  * `history` 模式发行需要后台配置支持，详见：[history 模式的后端配置 ](https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E5%90%8E%E7%AB%AF%E9%85%8D%E7%BD%AE%E4%BE%8B%E5%AD%90)
  * 打包部署后，在服务器上开启 gzip 可以进一步压缩文件。具体的配置，可以参考网上的分享：[服务器端开启GZIP压缩 ](https://juejin.im/post/5af003286fb9a07aac24611b)

### # 发布为小程序

**发布为微信小程序：**

  1. 申请微信小程序AppID，参考：[微信教程 ](https://developers.weixin.qq.com/miniprogram/dev/#%E7%94%B3%E8%AF%B7%E5%B8%90%E5%8F%B7)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "小程序-微信"，输入小程序名称和appid点击发行即可在 `unpackage/dist/build/mp-weixin` 生成微信小程序项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-6.png)

  3. 在微信小程序开发者工具中，导入生成的微信小程序项目，测试项目代码运行正常后，点击“上传”按钮，之后按照 “提交审核” => “发布” 小程序标准流程，逐步操作即可，详细查看：[微信官方教程 ](https://developers.weixin.qq.com/miniprogram/dev/quickstart/basic/release.html)。

**发布为百度小程序：**

  1. 入驻小程序并申请百度小程序AppID，参考：[百度小程序教程 ](https://smartprogram.baidu.com/docs/introduction/enter_application/)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "小程序-百度"，输入小程序名称和appid点击发行即可在 `/unpackage/dist/build/mp-baidu` 生成百度小程序项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-7.png)

  3. 在百度小程序开发者工具中，导入生成的百度小程序项目，测试项目代码运行正常后，点击“上传”按钮上传代码，之后在百度小程序的 [管理中心 ](https://smartprogram.baidu.com/developer/applist.html) 选择创建的应用点击前往发布，选择对应的版本然后提交审核。

**发布为支付宝小程序：**

  1. 入驻支付宝小程序，参考：[支付宝小程序教程 ](https://docs.alipay.com/mini/introduce)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "小程序-支付宝"，即可在 `/unpackage/dist/build/mp-alipay` 生成支付宝小程序项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni20190222-8.png)

  3. 在支付宝小程序开发者工具中，导入生成的支付宝小程序项目，测试项目代码运行正常后，点击“上传”按钮上传代码，在 [支付宝小程序后台 ](https://open.alipay.com/platform/mini.htm#/app)，选择刚提交的版本点击提交审核，详见：[支付宝小程序文档 ](https://docs.alipay.com/mini/developer/publish)。

**发布为抖音小程序：**

  1. 入驻抖音小程序，参考：[抖音小程序教程 ](https://developer.open-douyin.com/docs/resource/zh-CN/developer/join/register)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "小程序-抖音"，即可在 `/unpackage/dist/build/mp-toutiao` 生成抖音小程序项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/zjdance.jpg)

  3. 在抖音小程序开发者工具中，导入生成的抖音小程序项目，测试项目代码运行正常后，点击“上传”按钮上传代码，在 [抖音小程序后台 ](https://microapp.bytedance.com/applist)，选择刚提交的版本点击提交审核，详见：[抖音小程序文档 ](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/guide/release/package-audit/)。

**发布为360小程序：**

  1. 入驻360小程序，参考：[360小程序教程 ](https://mp.360.cn/doc/miniprogram/dev/#/)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "小程序-360"，即可在 `/unpackage/dist/build/mp-360` 生成360小程序项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-app-release-mp-360.png)

  3. 在360浏览器中，导入生成的360小程序项目

**注意**

  * 目前仅windows平台支持。360浏览器自身不支持mac平台。

**发布为快应用(webview)：**

  1. 入驻快应用(webview)，参考：[快应用(webview)教程 ](https://www.quickapp.cn/)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "快应用联盟"，即可在 `/unpackage/dist/build/quickapp-webview` 生成快应用(webview)项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-app-run-release-quickapp-webview.png)

  3. 在快应用联盟工具中，导入生成的快应用联盟项目，测试项目代码运行正常后，点击”构建“打包正式版，在[快应用联盟后台 ](https://www.quickapp.cn/)上传

**发布为快应用(webview) - 华为：**

  1. 入驻华为快应用，参考：[华为快应用教程 ](https://developer.huawei.com/consumer/cn/quickApp?ha_source=Dcloud&ha_sourceId=89000448)。
  2. 在HBuilderX中顶部菜单依次点击 "发行" => "快应用-华为"，即可在 `/unpackage/dist/build/quickapp-webview` 生成华为快应用项目代码。

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/uni-app-run-release-quickapp-webview-huawei.png)

  3. 在华为开发者工具中，导入生成的华为快应用项目，测试项目代码运行正常后，点击”构建“打包正式版，在 [华为快应用后台 ](https://developer.huawei.com/consumer/cn/quickApp?ha_source=Dcloud&ha_sourceId=89000448)上传

**发布为QQ小程序：** 内容同上，不再重复。

发布的快捷键是`Ctrl+u`。同样可拉下快速发布菜单并按数字键选择。

# # 2\. 通过vue-cli命令行

除了HBuilderX可视化界面，也可以使用 `cli` 脚手架，可以通过 `vue-cli` 创建 `uni-app` 项目。

## # 环境安装

全局安装vue-cli


    npm install -g @vue/cli


示例源码如下，请查看 pre > code 标签中的内容


    npm install -g @vue/cli

## # 创建uni-app

**使用正式版** （对应HBuilderX最新正式版）


    vue create -p dcloudio/uni-preset-vue my-project


示例源码如下，请查看 pre > code 标签中的内容


    vue create -p dcloudio/uni-preset-vue my-project

**使用Alpha版** （对应HBuilderX最新Alpha版）


    vue create -p dcloudio/uni-preset-vue#alpha my-alpha-project


示例源码如下，请查看 pre > code 标签中的内容


    vue create -p dcloudio/uni-preset-vue#alpha my-alpha-project

此时，会提示选择项目模板，初次体验建议选择 `hello uni-app` 项目模板，如下所示：

![](https://img.cdn.aliyun.dcloud.net.cn/guide/uniapp/h5-cli-01.png)

#### # 自定义模板

选择自定义模板时，需要填写 uni-app 模板地址，这个地址其实就是托管在云端的仓库地址。以 GitHub 为例，地址格式为 `userName/repositoryName`，如 `dcloudio/uni-template-picture` 就是下载图片模板。

更多支持的下载方式，请参考这个插件的说明：[download-git-repo ](https://www.npmjs.com/package/download-git-repo)

#### # 修改依赖为指定版本

  1. 查看 HBuilderX 对应的 NPM 依赖版本: 打开 [NPM版本记录 ](https://www.npmjs.com/package/@dcloudio/vue-cli-plugin-hbuilderx)，版本号 2.0.0- 后面是与 HBuilderX 对应的版本号且小版本不会超过9，比如 HBuilderX 2.7.5.20200518 对应的版本号 2.0.0-27520200518001，2.0.0-271420200618 对应的为 2.0.0-27920200618002。

  2. 批量修改 package.json 中 uni 相关依赖为指定的版本号（去掉版本号前面 ^）。

  3. 对于有变化的依赖进行增删，提示不存指定版本的依赖可以保留原始版本或者删除，运行时提示缺少的依赖自行安装。

## # 运行、发布uni-app


    npm run dev:%PLATFORM%
    npm run build:%PLATFORM%


示例源码如下，请查看 pre > code 标签中的内容


    npm run dev:%PLATFORM%
    npm run build:%PLATFORM%

`%PLATFORM%` 可取值如下：

值 | 平台
---|---
app-plus | app平台生成打包资源（支持npm run build:app-plus，可用于持续集成。不支持run，运行调试仍需在HBuilderX中操作）
h5 | H5
mp-alipay | 支付宝小程序
mp-baidu | 百度小程序
mp-weixin | 微信小程序
mp-toutiao | 抖音小程序
mp-lark | 飞书小程序
mp-qq | qq 小程序
mp-360 | 360 小程序
mp-kuaishou | 快手小程序
mp-jd | 京东小程序
mp-xhs | 小红书小程序
mp-harmony | 鸿蒙元服务
quickapp-webview | 快应用(webview)
quickapp-webview-union | 快应用联盟
quickapp-webview-huawei | 快应用华为

可以自定义更多条件编译平台，比如钉钉小程序，参考[package.json文档 ](https://uniapp.dcloud.io/collocation/package)。

## # 运行并发布快应用

快应用有两种开发方式，uni-app均支持：

  * 类小程序webview渲染方式：<https://ask.dcloud.net.cn/article/37182>[ ](https://ask.dcloud.net.cn/article/37182)
  * 原生渲染方式：<https://ask.dcloud.net.cn/article/37145>[ ](https://ask.dcloud.net.cn/article/37145)

#### # 运行并发布快应用(webview)

HBuilderX 2.7.12+ 版支持

#### # 运行并发布快应用(webview)-华为

HBuilderX 2.7.10+ 版支持

华为快应用文档-小程序转快应用 [https://developer.huawei.com/consumer/cn/doc/development/quickApp-References/quickapp-filestructure ](https://developer.huawei.com/consumer/cn/doc/development/quickApp-References/quickapp-filestructure?ha_source=Dcloud&ha_sourceId=89000448)

**其他：**

  * 目前使用`npm run build:app-plus`会在`/dist/build/app-plus`下生成app打包资源。如需制作wgt包，将`app-plus`中的文件压缩成zip（注意：不要包含`app-plus目录`），再重命名为`${appid}.wgt`， `appid`为`manifest.json`文件中的`appid`。
  * dev 模式编译出的各平台代码存放于根目录下的 `/dist/dev/`目录，打开各平台开发工具选择对应平台目录即可进行预览（h5 平台不会在此目录，存在于缓存中）；
  * build 模式编译出的各平台代码存放于根目录下的 `/dist/build/` 目录，发布时选择此目录进行发布；
  * dev 和 build 模式的区别：
    1. dev 模式有 SourceMap 可以方便的进行断点调试；
    2. build 模式会将代码进行压缩，体积更小更适合发布为正式版应用；
    3. 进行 [环境判断](/worktile/running-env.html#判断平台) 时，dev 模式 process.env.NODE_ENV 的值为 development，build 模式 process.env.NODE_ENV 的值为 production。

## # 使用cli创建项目和使用HBuilderX可视化界面创建项目有什么区别

#### # 编译器的区别

  * `cli` 创建的项目，编译器安装在项目下。并且不会跟随HBuilderX升级。如需升级编译器，执行 `npm update`，或者手动修改 package.json 中的 uni 相关依赖版本后执行 `npm install`。更新后可能会有新增的依赖并不会自动安装，手动安装缺少的依赖即可。
  * HBuilderX可视化界面创建的项目，编译器在HBuilderX的安装目录下的plugin目录，随着HBuilderX的升级会自动升级编译器。
  * 已经使用`cli`创建的项目，如果想继续在HBuilderX里使用，可以把工程拖到HBuilderX中。注意如果是把整个项目拖入HBuilderX，则编译时走的是项目下的编译器。如果是把src目录拖入到HBuilderX中，则走的是HBuilderX安装目录下plugin目录下的编译器。
  * `cli`版如果想安装less、scss、ts等编译器，需自己手动npm安装。在HBuilderX的插件管理界面安装无效，那个只作用于HBuilderX创建的项目。

#### # 开发工具的区别

  * `cli`创建的项目，内置了d.ts，同其他常规npm库一样，可在[vscode ](https://ask.dcloud.net.cn/article/36286)、[webstorm ](https://ask.dcloud.net.cn/article/36307)等支持d.ts的开发工具里正常开发并有语法提示。
  * 使用HBuilderX创建的项目不带d.ts，HBuilderX内置了uni-app语法提示库。如需把HBuilderX创建的项目在其他编辑器打开并且补充d.ts，可以在项目下先执行 `npm init`，然后`npm i @types/uni-app -D`，来补充d.ts。
  * 但vscode等其他开发工具，在vue或uni-app领域，开发效率比不过HBuilderX。详见：<https://ask.dcloud.net.cn/article/35451>[ ](https://ask.dcloud.net.cn/article/35451)
  * 发布App时，仍然需要使用HBuilderX。其他开发工具无法发布App，但可以发布H5、各种小程序。如需开发App，可以先在HBuilderX里运行起来，然后在其他编辑器里修改保存代码，代码修改后会自动同步到手机基座。
  * 如果使用`cli`创建项目，那下载HBuilderX时只需下载10M的标准版即可。因为编译器已经安装到项目下了。
  * 对 `cli` 使用有疑问，欢迎扫码加入 uni-app 微信交流群讨论：
![](https://img.cdn.aliyun.dcloud.net.cn/guide/uniapp/wx-barcode.png)

注意：HBuilderX创建的项目，一样可以使用npm，参考：<https://uniapp.dcloud.io/frame?id=npm%e6%94%af%e6%8c%81>[ ](https://uniapp.dcloud.io/frame?id=npm%e6%94%af%e6%8c%81)

[帮助我们改善此页面！](https://gitcode.com/dcloud/unidocs-zh/edit/master/docs/quickstart.md)

上次更新: 2025/9/4 14:37:55

开发产品

[HBuilderX](https://www.dcloud.io/hbuilderx.html)[uni-app](https://uniapp.dcloud.net.cn/)[uni-app x](https://doc.dcloud.net.cn/uni-app-x/)[uniCloud](https://doc.dcloud.net.cn/uniCloud/)[uniMPsdk](https://nativesupport.dcloud.net.cn/)[5+Runtime](https://www.dcloud.io/runtime.html)[wap2app](https://www.dcloud.io/wap2app.html?platform=wap2app)[MUI](https://www.dcloud.io/mui.html)[uni-id](https://doc.dcloud.net.cn/uniCloud/uni-id/summary.html)[uni-cdn](https://doc.dcloud.net.cn/uniCloud/uni-cdn/intro.html)[uni-pay](https://doc.dcloud.net.cn/uniCloud/uni-pay/uni-app.html)[uni-push](https://uniapp.dcloud.net.cn/unipush)[uni一键登录](https://uniapp.dcloud.io/univerify)[uni实人认证](https://doc.dcloud.net.cn/uniCloud/frv/intro.html)[sms](https://doc.dcloud.net.cn/uniCloud/send-sms)[uni-starter](https://ext.dcloud.net.cn/plugin?id=5057)[uni-admin](https://doc.dcloud.net.cn/uniCloud/admin)[uni-upgrade-center](https://uniapp.dcloud.io/uniCloud/upgrade-center)[uni-im](https://doc.dcloud.net.cn/uniCloud/uni-im)[uni-ai](https://doc.dcloud.net.cn/uniCloud/uni-ai)[uni-cms](https://doc.dcloud.net.cn/uniCloud/uni-cms)[uniCloud-map](https://doc.dcloud.net.cn/uniCloud/unicloud-map.html)[uni-search](https://ext.dcloud.net.cn/plugin?id=3851)

运营产品

[uni-ad](https://uniad.dcloud.net.cn/login)[uni统计](https://tongji.dcloud.net.cn/)[uni发行](https://www.dcloud.io/dportal.html)[uni安全专题](https://uniapp.dcloud.net.cn/tutorial/safe.html)

开发者服务

[问答社区](https://ask.dcloud.net.cn/explore/)[开发者后台](https://dev.dcloud.net.cn/)

技术文档

[uni-app文档](https://uniapp.dcloud.io/)[uniCloud文档](https://uniapp.dcloud.io/uniCloud/README)[原生开发者支持文档](https://nativesupport.dcloud.net.cn/)[HBuilder文档](https://hx.dcloud.net.cn/)

生态服务

[插件市场](https://ext.dcloud.net.cn/)[OAuth用户开放平台](https://open.dcloud.net.cn/pages/login/login)

关于我们： [ DCloud官网 ](https://dcloud.io/)[ 案例 ](https://uniapp.dcloud.io/case)[ 需求墙 ](https://dev.dcloud.net.cn/wish/?channel=uniapp)[ 许可协议 ](https://dcloud.io/license/DCloud.html)[ 加入我们 ](https://www.dcloud.io/hr/)[ 赞助我们 ](https://dev.dcloud.net.cn/sponsor/)

联系我们： [ 商务合作：bd@dcloud.io ](mailto:bd@dcloud.io)[ 广告合作：uniad@dcloud.io ](mailto:uniad@dcloud.io)

DCloud.io 数字天堂（北京）网络技术有限公司是

[HTML5中国产业联盟](https://www.html5plus.org/) 发起单位

[ ](https://beian.miit.gov.cn/#/Integrated/index)

![](https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/jgwab.png) [京公网安备：11010802035340号 ](http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802035340)

国家信息安全等级保护三级，证书编号：11010813802-20001
