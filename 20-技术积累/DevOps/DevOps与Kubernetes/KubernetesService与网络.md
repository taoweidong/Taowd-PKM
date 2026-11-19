---
title: Kubernetes Service 与网络
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 网络
  - Service
  - GatewayAPI
aliases:
  - K8s Service 与网络
  - Kubernetes 网络
source:
  - 网络资料整理
  - [Kubernetes 官方文档：Service](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/)
  - [Kubernetes 官方文档：Network Policies](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/)
  - [Kubernetes 官方博客：Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
---

# Kubernetes Service 与网络

> [!summary] 摘要
> 本文聚焦 Kubernetes 的「稳定访问 + 网络治理」链路：从 Service 四种类型、EndpointSlice 与 kube-proxy 的四层负载均衡机制，到 DNS 解析、NetworkPolicy 东西向隔离、Ingress → Gateway API 的南北向入口演进。以 v1.37 为默认视角，覆盖可直接运行的清单与命令，并重点标注 2026 年必须处理的弃用项（Endpoints v1、Ingress-NGINX、kube-proxy ipvs）。定位为「DevOps 与 Kubernetes」体系中的网络专题，承接 [[DevOps与Kubernetes-从入门到精通]] 的入口层知识，适合后端、运维与 SRE 落地参考。

Service 是 Kubernetes 给一组 Pod 提供**稳定访问入口**与**四层负载均衡**的核心抽象：Pod 会被重建、漂移、扩缩，IP 随之变化，而 Service 通过标签选择器（selector）持续追踪后端 Pod，并借助 EndpointSlice 与 kube-proxy 把访问流量分发到健康的实例。理解 Service，关键不是背四个类型，而是看清「选择器 → EndpointSlice → 转发规则 → 流量」这条对账链路。

## 一、最新动态（截至 2026-11）

- **Kubernetes v1.37（Garhwal）**：2026-08-26 发布，是当前最新稳定版，官方文档默认版本即为 v1.37，当前补丁为 1.37.2。项目维护 **1.37 / 1.36 / 1.35** 三个次版本分支，**1.34 已于 2026-10-27 EOL**。来源：[Kubernetes Patch Releases](https://kubernetes.io/releases/patch-releases/)
- **Endpoints API v1 已废弃**：v1.33 起 `Endpoints` 资源的 v1 版本进入弃用，官方改用 **EndpointSlice** 承载服务端点。存量清单与监控、运维脚本需迁移到 EndpointSlice。来源：[Volcengine K8s v1.34 版本说明](https://docs.volcengine.com/docs/vke/vke-for-kubernetes-v1-34?lang=zh)
- **Ingress-NGINX 已于 2026-03 归档退役**：官方网络入口方向全面转向 **Gateway API**，核心资源 GatewayClass / Gateway / HTTPRoute / GRPCRoute / TLSRoute / ReferenceGrant **已 GA**，TCPRoute / UDPRoute 仍为实验性。官方提供 **Ingress2Gateway 1.0** 迁移工具。来源：[K8s Blog: Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
- **kube-proxy ipvs 模式在 v1.35 被弃用（deprecation）**：选型与迁移需关注 iptables / nftables 的替代方案（kube-proxy nftables 后端自 v1.33 起已 Stable）。来源：[K8s v1.35 Sneak Peek](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
- **v1.37 弃用/移除相关网络项**：`kube-dns` 弃用（转向 CoreDNS 等 DNS 方案）、Service `.spec.externalIPs` 弃用（计划 v1.43 移除，关联 CVE-2020-8554）；v1.35 起 Service `trafficDistribution: PreferSameNode`（KEP-3015，拓扑感知就近路由）Stable。来源：[Kubernetes v1.37 发布](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/) · [Kubernetes v1.36 发布](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)

> [!warning] 迁移提醒
> 以上弃用/退役项不是「将来再说」：Ingress-NGINX 已归档，Endpoints v1、externalIPs、ipvs 均有明确移除时间点，升级前应先完成迁移，避免升级后被动回滚。

## 二、基础概念

**Service 的四类类型**，按暴露范围区分：

| 类型 | 作用范围 | 典型场景 | 访问方式 |
| --- | --- | --- | --- |
| **ClusterIP** | 集群内部 | 微服务间调用、内部依赖 | 仅集群内通过虚拟 IP 访问，默认类型 |
| **NodePort** | 集群节点端口 | 本地调试、无云负载均衡时对外 | `节点IP:NodePort`（30000-32767） |
| **LoadBalancer** | 集群外部 | 云上生产、需要公网入口 | 云厂商负载均衡器分配公网/内网 IP |
| **ExternalName** | 集群内部映射 | 把集群内名称指向外部域名 | 返回 CNAME，不创建 ClusterIP |

**关键配套对象**：

- **EndpointSlice**：真正的端点列表载体，由 EndpointSlice 控制器根据 Service 的 selector 对账生成，支持大规模端点分片与增量更新。
- **kube-proxy**：运行在每个节点的代理，把 Service 虚拟 IP 的流量按转发规则分发到后端 Pod。支持 `userspace`、`iptables`、`ipvs`、`nftables` 等模式。
- **DNS**：CoreDNS 为 Service 提供集群内域名（如 `my-svc.my-ns.svc.cluster.local`），集群内名称解析依赖它。
- **NetworkPolicy**：基于标签的 L3/L4 流量隔离，需 CNI 支持，属于东西向（Pod 之间）治理。
- **Ingress / Gateway API**：负责南北向（外部 → 集群）的七层入口与路由。

## 三、核心机制

**1. 选择器与对账**：Service 通过 `spec.selector` 匹配 Pod 标签，控制器持续对账，把匹配到的、处于 Ready 状态的 Pod 地址写入 EndpointSlice。EndpointSlice 更新后，kube-proxy 监听变化并刷新转发规则，整个过程无需人工干预。Pod 崩溃或被删除后，端点会被及时摘除，这就是「Service 让不稳定 Pod 获得稳定访问」的底层机制。

**2. kube-proxy 转发模式**：

- **iptables**：通过规则链做 DNAT，规则数量随 Service/端点增多而线性膨胀，规模大时规则匹配变慢。
- **ipvs**：基于内核 IPVS 的哈希表，大规模下转发性能与规则查找效率更优，但**已在 v1.35 被弃用**。
- **nftables**：新一代内核规则引擎，v1.33 起提供 Stable 后端，是 ipvs 退役后的主流替代方向。

**3. 四层与七层边界**：Service + kube-proxy 只做四层（TCP/UDP）负载均衡；需要基于路径、Host、Header 的七层路由，则交由 Ingress 或 Gateway API 处理。

**4. 网络隔离**：NetworkPolicy 以 `podSelector` / `namespaceSelector` + 方向（ingress/egress）定义白名单，实现「默认拒绝、按需放行」的东西向隔离；它与 Service 互补——Service 管「怎么访问」，NetworkPolicy 管「谁能访问」。

## 四、实践步骤（含代码/命令示例）

**1. 部署工作负载并创建 ClusterIP Service**（`service-clusterip.yaml`）：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-demo
  labels:
    app: web-demo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-demo
  template:
    metadata:
      labels:
        app: web-demo
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            periodSeconds: 10
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-demo
spec:
  type: ClusterIP
  selector:
    app: web-demo
  ports:
    - name: http
      port: 80
      targetPort: 80
```

**2. 提交并核对端点链路**：

```bash
kubectl apply -f service-clusterip.yaml

# 观察 Service 分配的虚拟 IP
kubectl get svc web-demo

# 核对 EndpointSlice（取代旧的 Endpoints）
kubectl get endpointslices -l kubernetes.io/service-name=web-demo -o wide

# 集群内访问验证
kubectl run -it --rm debug --image=busybox -- sh
# 在容器内执行：nslookup web-demo.default.svc.cluster.local
```

**3. NodePort 对外暴露**（本地调试）：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-demo-nodeport
spec:
  type: NodePort
  selector:
    app: web-demo
  ports:
    - name: http
      port: 80
      targetPort: 80
      nodePort: 30080
```

应用后用 `http://<节点IP>:30080` 访问；`kubectl get svc web-demo-nodeport` 可看到 `PORT(S)` 列。

**4. LoadBalancer（云上）与 ExternalName（映射外部域名）**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-demo-lb
spec:
  type: LoadBalancer
  selector:
    app: web-demo
  ports:
    - port: 80
      targetPort: 80
```

```yaml
apiVersion: v1
kind: ExternalName
metadata:
  name: external-db
spec:
  externalName: db.example.com
```

**5. Headless Service（有状态/需直连 Pod）**：设置 `clusterIP: None`，不为 Service 分配虚拟 IP，DNS 直接返回各 Pod IP，常用于 StatefulSet。

**6. 使用 kube-proxy（查看与验证）**：

```bash
# 查看各节点 kube-proxy 工作模式（iptables / ipvs / nftables）
kubectl -n kube-system get pods -l k8s-app=kube-proxy -o wide
kubectl -n kube-system exec ds/kube-proxy -- iptables-save | grep web-demo
```

**7. NetworkPolicy 隔离示例**（默认拒绝入站、仅放行 80 端口）：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-demo-allow-http
spec:
  podSelector:
    matchLabels:
      app: web-demo
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: backend
      ports:
        - protocol: TCP
          port: 80
```

```bash
kubectl apply -f networkpolicy.yaml
kubectl get networkpolicy -A
```

**8. Gateway API 迁移示例**（替代 Ingress，核心资源已 GA）：

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: prod
spec:
  controller: istio.io/gateway-controller
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: prod-gateway
  namespace: prod
spec:
  gatewayClassName: prod
  listeners:
    - name: http
      port: 80
      protocol: HTTP
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
  namespace: prod
spec:
  parentRefs:
    - name: prod-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: web-demo
          port: 80
```

## 五、最佳实践与常见坑

**最佳实践**：

- **统一用 EndpointSlice 对接监控与运维**，不要再依赖已废弃的 Endpoints v1。
- **为所有入站服务配置 NetworkPolicy**，遵循「默认拒绝 + 最小放行」，配合 RBAC 形成纵深防御。
- **生产入口统一用 Gateway API**，新项目直接按 GatewayClass/Gateway/HTTPRoute 设计，存量 Ingress 用 Ingress2Gateway 1.0 迁移。
- **Service 命名与命名空间规划清晰**，集群内以 `svc.ns.svc.cluster.local` 全限定名访问，避免跨命名空间歧义。
- **选择器保持稳定**，避免随意修改标签导致 Service 选择到错误的 Pod；标签治理要统一。
- **面向拓扑感知**：对多节点集群启用 `trafficDistribution: PreferSameNode`，减少跨节点流量、降低延迟。

**常见坑**：

| 现象 | 典型原因 | 排查动作 |
| --- | --- | --- |
| 集群内访问 Service 超时 | selector 与 Pod 标签不匹配、EndpointSlice 为空 | `kubectl get endpointslices -l kubernetes.io/service-name=<svc>`；核对标签 |
| NodePort 不通 | 安全组/防火墙未放行端口、节点 kube-proxy 异常 | 检查安全组 30000-32767 入站；`kubectl -n kube-system logs` 查 kube-proxy |
| LoadBalancer 长时间 `Pending` | 云厂商负载均衡器配额/权限不足 | `kubectl describe svc`；核对云账号权限与配额 |
| Service 规则太多导致转发变慢 | iptables 规则膨胀 | 评估迁移 nftables；减少冗余 Service |
| NetworkPolicy 不生效 | CNI 不支持、命名空间/标签写错 | 确认 CNI 支持 NetworkPolicy；核对 podSelector 标签 |
| 升级后 ipvs 相关告警/异常 | v1.35 起 ipvs 弃用 | 规划迁移到 nftables/iptables，验证转发行为 |

> [!warning] 易踩的迁移坑
> Ingress-NGINX 退役后，直接平移配置到 Gateway API 会遇到默认行为差异（官方已提示多个易被忽略之处），迁移前务必用 Ingress2Gateway 工具并做逐条对比与灰度验证。

## 六、核心要点速查

1. Service 四种类型：ClusterIP（内部）/ NodePort（节点端口）/ LoadBalancer（云上）/ ExternalName（外部映射）。
2. 端点载体是 **EndpointSlice**，Endpoints v1 已废弃，运维与监控必须迁移。
3. kube-proxy 做四层负载均衡，模式有 iptables / ipvs / nftables；**ipvs 已在 v1.35 弃用**，nftables 是替代方向。
4. Service 通过 selector 对账生成 EndpointSlice，再由 kube-proxy 刷新转发规则，形成「稳定访问」的闭环。
5. DNS 由 CoreDNS 提供，集群内 Service 名按 `svc.ns.svc.cluster.local` 解析。
6. NetworkPolicy 做东西向 L3/L4 隔离，与 Service 互补，需 CNI 支持，生产应默认拒绝、最小放行。
7. 南北向七层入口从 Ingress 转向 **Gateway API**，核心资源已 GA，Ingress-NGINX 已于 2026-03 退役。
8. 当前版本基线 v1.37（2026-08-26），维护 1.37/1.36/1.35；升级前先处理 Endpoints v1、externalIPs、ipvs 等弃用项。

## 七、学习资源

1. [Kubernetes 官方文档：Services（Service 概念与类型）](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/)
2. [Kubernetes 官方文档：Network Policies（网络策略）](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/)
3. [Kubernetes 官方文档：EndpointSlice（端点切片）](https://kubernetes.io/zh-cn/docs/concepts/services-networking/endpoint-slice/)
4. [Kubernetes 官方文档：Service（Service 类型与负载均衡）](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/)
5. [Kubernetes 官方博客：Ingress2Gateway 1.0 发布](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
6. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)
7. [Kubernetes 官方博客：Kubernetes v1.35 发布（Timbernetes）](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
8. [Gateway API 官方站点（GatewayClass / Gateway / HTTPRoute）](https://gateway-api.io/)
9. [Kubernetes 官方文档：Patch Releases（补丁与支持策略）](https://kubernetes.io/releases/patch-releases/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
