---
source: "http://dubbo.apache.org/zh-cn/"
title: "Apache Dubbo"
fetched_at: "2026-10-05 15:30:32"
---

## 一款云原生微服务开发框架

构建具备内置 RPC、流量管控、安全、可观测能力的应用，支持Kubernetes和VM部署环境。

[快速开始 ](overview/mannual/java-sdk/quick-start/starter/)[商城 Demo](overview/demo/)

### 选择您喜欢的语言并快速体验

[Java ](overview/mannual/java-sdk)[Go ](overview/mannual/golang-sdk)[Node.js ](overview/mannual/nodejs-sdk)[Web ](overview/mannual/web-sdk)[Rust ](overview/mannual/rust-sdk)[...](overview/mannual/)

# Why Dubbo?

![images/framework.svg](/zh-cn/_common-resources/images/framework.svg)

#### [快速上手](/zh-cn/overview/what/advantages/usability/)，让开发者专注业务开发

多语言 SDK 定义微服务开发范式，通信协议灵活切换，支持 HTTP/2、gRPC、REST、Thrift、TCP 等任一协议。

![images/governance.svg](/zh-cn/_common-resources/images/governance.svg)

#### [服务治理](/zh-cn/overview/what/advantages/governance/)，实时监测、管控集群状态

内置服务发现、负载均衡、路由等流量管控策略，提供全链路追踪、限流降级、一致性事务、日志、Metrics、服务网格、Admin 可视化控制台等一站式微服务生态。

![images/performance.svg](/zh-cn/_common-resources/images/performance.svg)

#### [超高性能](/zh-cn/overview/what/advantages/performance/)，面向百万实例集群设计

阿里巴巴每年双十一数百万实例、万亿次调用跑在 Dubbo 之上，从设计之初即将低延迟、高吞吐量、可伸缩性放在第一位。

![images/usecase.png](/zh-cn/_common-resources/images/usecase.png)

#### [企业级解决方案](/zh-cn/overview/what/advantages/production-ready/)，多年企业生产环境检验

用户群体遍布各行各业，典型代表包括工商银行、携程、海尔、金蝶、云厂商 (阿里云、腾讯云、华为云) 等，2022年 Dubbo3 在阿里巴巴已全面升级 HSF2 实现了框架统一。

## 快速掌握基于 Apache Dubbo 的微服务开发与治理

By 刘军，Apache Dubbo PMC Chair

观看视频

[跟随示例任务学习 Dubbo！](./overview/tasks/) [探索 Dubbo 生态、社区动态并参与线下活动！](./blog/news/)

### 核心特性

#### [服务发现](/zh-cn/overview/what/core-features/service-discovery/)

Dubbo 提供了高性能、可伸缩的服务发现机制，面向百万集群实例规模设计，默认提供 Nacos、Zookeeper 等注册中心适配并支持自定义扩展。

#### [多语言 SDK](/zh-cn/overview/mannual/)

提供 Java、Golang、Rust、Node.js、Python 等多语言 SDK 实现，支持基于 IDL 的跨语言服务定义和基于 Protobuf、Json 的数据编码

#### [流量管控](/zh-cn/overview/what/core-features/traffic/)

Dubbo 提供的基于路由规则的流量管控策略，可以帮助实现全链路灰度、金丝雀发布、按比例流量转发、动态调整调试时间、设置重试次数等服务治理能力。

#### [灵活部署模式](/zh-cn/overview/mannual/java-sdk/tasks/deploy/)

一键拉起服务治理体系，屏蔽底层跨平台的微服务基础设施复杂度，支持虚拟机、Docker、Kubernetes、服务网格等多种部署模式。

#### [通信协议](/zh-cn/overview/what/core-features/protocols/)

支持 HTTP/2、gRPC、TCP、REST 等任意通信协议，切换协议只需要修改一行配置，支持单个端口上的多协议发布。

#### [可扩展性](/zh-cn/overview/what/core-features/extensibility/)

一切皆可扩展，通过扩展 (Filter、Router、Service Discovery、Configuration 等) 自定义调用、管控行为，适配开源微服务生态。

#### [可观测性](/zh-cn/overview/what/core-features/observability/)

多维度的可观测指标（Metrics、Tracing、Accesslog）帮助了解服务运行状态，Admin 控制台、Grafana 等帮助实现数据指标可视化展示。

#### [认证鉴权](/zh-cn/overview/what/core-features/security/)

支持基于 TLS 的传输链路认证与加密通信以及基于请求身份的权限校验，帮助构建零信任分布式微服务体系。

#### [服务网格(Service Mesh)](/zh-cn/overview/what/core-features/service-mesh/)

灵活的数据面 (Proxy & Proxyless) 部署形态支持，无缝接入 Istio 控制面治理体系。

#### [丰富生态](/zh-cn/overview/what/core-features/ecosystem/)

一站式微服务生态适配：注册中心、网关、限流降级、负载均衡、一致性事务、异步消息、Tracing 等。

关注我们

请通过以下任一或多个渠道关注社区动态，与社区开发者保持密切沟通。

微信

![WeChat QR Code](https://img.alicdn.com/imgextra/i2/O1CN010ygTmZ1tp9a2Zii3b_!!6000000005950-0-tps-258-258.jpg)

钉钉

![DingTalk QR Code](https://img.alicdn.com/imgextra/i4/O1CN01buuadT274Lj33QZWQ_!!6000000007743-0-tps-1170-1477.jpg)

[GitHub](https://github.com/apache/dubbo/)

  * 文档
  * [概览](/zh-cn/overview/home/)
  * [快速开始](/zh-cn/overview/quickstart/)
  * [开发者指南](/zh-cn/contact/contributor/software-donation-guide_dev/)

  * 资源
  * [社区](/zh-cn/contact/)

© 2026 The Apache Software Foundation. Apache Dubbo, Dubbo, Apache, the Apache feather logo, and the Apache Dubbo project logo are either registered trademarks or trademarks of The Apache Software Foundation in the United States and other countries. 保留所有权利

[Foundation](https://www.apache.org/) | [License](https://www.apache.org/licenses/) | [Events](https://www.apache.org/events/current-event.html) | [Security](https://www.apache.org/security/) | [Sponsorship](https://www.apache.org/foundation/sponsorship.html) | [Thanks](https://www.apache.org/foundation/thanks.html) | [Privacy](https://privacy.apache.org/policies/privacy-policy-public.html)
