---
source: "https://cloud.tencent.com/developer/article/1152362"
title: "分享几个IP获取地理位置的API接口-腾讯云开发者社区-腾讯云"
fetched_at: "2026-10-05 15:44:37"
---

[](https://cloud.tencent.com/developer/user/1284689)

[夏时](https://cloud.tencent.com/developer/user/1284689)

## 分享几个IP获取地理位置的API接口

 __关注作者

[ _腾讯云_](https://cloud.tencent.com/?from=20060&from_column=20060)

[ _开发者社区_](https://cloud.tencent.com/developer)

[文档](https://cloud.tencent.com/document/product?from=20702&from_column=20702)[建议反馈](https://cloud.tencent.com/voc/?from=20703&from_column=20703)[控制台](https://console.cloud.tencent.com/?from=20063&from_column=20063)

登录/注册

文章/答案/技术大牛搜索 __

搜索 __关闭 __

发布

夏时

 __

__

__

__

__

[社区首页](https://cloud.tencent.com/developer) >[专栏](https://cloud.tencent.com/developer/column) >分享几个IP获取地理位置的API接口

# 分享几个IP获取地理位置的API接口

![作者头像](https://ask.qcloudimg.com/custom-avatar/1284689/9g9qfibklp.jpg)

夏时

 __关注

修改于 2025-11-10 11:04:04

修改于 2025-11-10 11:04:04

64.7K

举报

 __文章被收录于专栏：[夏时](https://cloud.tencent.com/developer/column/3271)夏时

全网首发，最全的IP接口，不服来辩！博主找了几个小时的资料，又手动抓取到了几个接口补充进来，应该不能再全了……

###  360获取本机IP、地区及运营商

接口地址：http://ip.360.cn/IPShare/info

传递参数：无

返回类型：json

返回值：

  * greetheader：提示语(如上午好、中午好等)
  * nickname：本机已登录的360账号
  * ip：本机IP地址
  * location：IP所对应的地理位置(中间会有“\t”分隔地区与运营商)
  * loc_client：作用不明

请求示例：

  1. Request URL:http://ip.360.cn/IPShare/info

返回示例：

  1. {
  2. "greetheader":"中午好,",
  3. "nickname":"null",
  4. "ip":"115.159.152.210",
  5. "location":"上海市\t电信 ",
  6. "loc_client":""
  7. }

备注：本接口抓包自360IP分享计划网站

###  360获取指定IP的地区及运营商

接口地址：http://ip.360.cn/IPQuery/ipquery

传递参数：

  * ip：要查询的IP地址

参数传递方式：GET/POST

返回类型：json

返回值：

  * errno：错误编号(为零则代表成功)
  * errmsg：错误信息
  * data：查询的IP所对应的地理位置(中间会有“\t”分隔地区与运营商)

请求示例：

  1. Request URL:http://ip.360.cn/IPQuery/ipquery?ip=115.159.152.210

返回示例：

  1. {
  2. "errno":0,
  3. "errmsg":"",
  4. "data":"上海市\t电信"
  5. }

备注：本接口抓包自360IP分享计划网站

###  ip508获取指定IP、地区及所处位置

接口地址：http://www.ip508.com/ip

传递参数：

  * q：要查询的IP地址(为空则查询本机IP)

参数传递方式：GET/POST

返回类型：json

返回值：

  * r：是否请求成功
  * i：查询到的IP地址
  * c：查询到的IP所对应的地理位置
  * a：查询到的详细位置(如XX公司)

请求示例：

  1. Request URL:http://www.ip508.com/ip?q=115.159.152.210

返回示例：

  1. {
  2. "r":true,
  3. "d":{
  4. "i":"115.159.152.210",
  5. "c":"上海市",
  6. "a":"腾讯云BGP数据中心"
  7. }
  8. }

备注：本接口抓包自ip508.com

###  淘宝获取本机IP地址

接口地址：http://www.taobao.com/help/getip.php

传递参数：无

返回类型：jsonp

callback：ipCallback

返回值：

  * ip：本机IP地址

请求示例：

  1. Request URL:http://www.taobao.com/help/getip.php

返回示例：

  1. ipCallback({ip:"115.159.152.210"})

备注：本接口只有返回IP地址的功能

###  淘宝获取IP详细信息

接口地址：http://ip.taobao.com/service/getIpInfo.php

传递参数：

  * ip：要查询的IP地址

参数传递方式：GET/POST

返回类型：json

返回值：

  * code：错误码(为零代表请求成功)
  * country：国名
  * country_id：国名(英文缩写)
  * area：地域(如：华东)
  * area_id：地域ID
  * region：行政区
  * region_id：行政区ID
  * city：城市名
  * city_id：城市ID
  * isp：网络提供商
  * isp_id：网络提供商ID
  * ip：请求的IP地址

请求示例：

  1. Request URL:http://ip.taobao.com/service/getIpInfo.php?ip=115.159.152.210

返回示例：

  1. {
  2. "code":0,
  3. "data":{
  4. "country":"中国",
  5. "country_id":"CN",
  6. "area":"华东",
  7. "area_id":"300000",
  8. "region":"上海市",
  9. "region_id":"310000",
  10. "city":"上海市",
  11. "city_id":"310100",
  12. "county":"",
  13. "county_id":"-1",
  14. "isp":"腾讯网络",
  15. "isp_id":"1000153",
  16. "ip":"115.159.152.210"
  17. }
  18. }

备注：本接口来自[淘宝IP地址库](https://cloud.tencent.com/developer/tools/blog-entry?target=https%3A%2F%2Fmkblog.cn%2Fgo%2F%3Furl%3Dhttp%3A%2F%2Fip.taobao.com%2Findex.php&objectId=1152362&objectType=1&contentType=undefined)

###  太平洋网络IP地址查询Web接口

这个玩法很多，官网介绍也很详细☞ 传送门

###  搜狐IP地址查询接口

接口地址：http://pv.sohu.com/cityjson

传递参数：

  * ie：编码(默认为GBK)

参数传递方式：GET

返回类型：js

返回值：

  * cip：本机IP地址
  * cid：城市编号
  * cname：城市名称

请求示例：

  1. Request URL:http://pv.sohu.com/cityjson?ie=utf-8

返回示例：

  1. var returnCitySN = {"cip": "115.159.152.220", "cid": "410100", "cname": "广州市"};

###  新浪IP地址查询接口

接口地址：http://int.dpool.sina.com.cn/iplookup/iplookup.php

传递参数：

  * format：数据返回格式
  * ip：欲查询的IP(空则查询本机)

参数传递方式：GET

返回类型：js/json

返回值：

  * country：国名
  * province：省份
  * city：城市名

注：还有一些参数无法获取数据，作用未知。

请求示例：

  1. Request URL:http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js&ip=115.159.152.210

返回示例

  1. var remote_ip_info = {
  2. "ret": 1,
  3. "start": -1,
  4. "end": -1,
  5. "country": "中国",
  6. "province": "上海",
  7. "city": "上海",
  8. "district": "",
  9. "isp": "",
  10. "type": "",
  11. "desc": ""
  12. };

###  站长之家IP地址接口

使用方式：

  1.

###  中国黑客联盟IP地址接口

接口地址：http://www.fbisb.com/ip.php

传递参数：

  * ip：要查询的IP地址

参数传递方式：GET

返回类型：html

备注：本接口抓包自中国黑客联盟IP定位查询系统

###  附录

还可以通过抓取源码从几个网站获取IP信息

  * http://www.hao7188.com/ 此网站获取到的数据比较详细，推荐。
  * http://www.ip138.com/ 老牌的IP查询网站
  * http://www.ip.cn/ 比较知名的IP查询网站
  * http://myip.com.tw/ 来自中国台湾的IP查询网站
  * http://www.net.cn/static/customercare/yourip.asp 万网获取本地公网IP地址
  * http://ip.qq.com/ 腾讯IP分享计划(估计要挂了，不推荐)

以下还有些收费的API接口(不推荐)：

  * 百度地图高精度定位API：http://lbsyun.baidu.com/index.php?title=webapi/high-acc-ip
  * 百度的API：http://apistore.baidu.com/apiworks/servicedetail/114.html
  * NowAPI：https://www.nowapi.com/api/ip.get
  * 91查API：http://www.91cha.com/api/ip.html

本文参与 [腾讯云自媒体同步曝光计划](https://cloud.tencent.com/developer/support-plan)，分享自作者个人站点/博客。

如有侵权请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除

前往查看

[api](https://cloud.tencent.com/developer/tag/10292)

[json](https://cloud.tencent.com/developer/tag/10207)

目录

  * 360获取本机IP、地区及运营商

  * 360获取指定IP的地区及运营商

  * ip508获取指定IP、地区及所处位置

  * 淘宝获取本机IP地址

  * 淘宝获取IP详细信息

  * 太平洋网络IP地址查询Web接口

  * 搜狐IP地址查询接口

  * 新浪IP地址查询接口

  * 站长之家IP地址接口

  * 中国黑客联盟IP地址接口

  * 附录

相关产品与服务

弹性公网 IP

弹性公网 IP（Elastic IP，EIP）是可以独立购买和持有，且在某个地域下固定不变的公网 IP 地址，可以与 CVM、NAT 网关、弹性网卡和高可用虚拟 IP 等云资源绑定，提供访问公网和被公网访问能力；还可与云资源的生命周期解耦合，单独进行操作；同时提供多种计费模式，您可以根据业务特点灵活选择，以降低公网成本。

[ __产品介绍](https://cloud.tencent.com/product/eip?from=21341&from_column=21341)[ __产品文档](https://cloud.tencent.com/document/product/1199?from=21342&from_column=21342)

[ __2026上云采购 | AI焕新·智启新局](https://cloud.tencent.com/act/pro/featured-202607?from=21344&from_column=21344)

[问题归档](https://cloud.tencent.com/developer/ask/archives.html)[专栏文章](https://cloud.tencent.com/developer/column/archives.html)[快讯文章归档](https://cloud.tencent.com/developer/news/archives.html)[关键词归档](https://cloud.tencent.com/developer/information/all.html)[开发者手册归档](https://cloud.tencent.com/developer/devdocs/archives.html)[开发者手册 Section 归档](https://cloud.tencent.com/developer/devdocs/sections_p1.html)
