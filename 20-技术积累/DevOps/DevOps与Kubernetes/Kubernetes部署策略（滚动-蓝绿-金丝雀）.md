---
title: Kubernetes 部署策略（滚动/蓝绿/金丝雀）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 部署策略
  - 持续交付
aliases:
  - Kubernetes部署策略
  - 滚动更新
  - 蓝绿部署
  - 金丝雀发布
source:
  - 网络资料整理
---

# Kubernetes 部署策略（滚动/蓝绿/金丝雀）

> [!summary] 摘要
> 本文系统梳理 Kubernetes 中三种主流发布策略——**滚动更新（Rolling Update）、蓝绿部署（Blue/Green）、金丝雀发布（Canary）**：先讲清三者的适用场景与心智模型，再深入各自的控制器与流量切换机制，最后给出可直接运行的 YAML 清单与 `kubectl`/Argo CD 命令示例。核心结论：滚动更新是无状态应用的默认默认选择，蓝绿适合需要一键回滚、可承受双份资源的场景，金丝雀适合面向真实流量、需要按比例渐进验证的场景；三者并非互斥，可借助 Gateway API、服务网格与 GitOps 组合出更精细的渐进式交付闭环。

## 一、最新动态（截至 2026-11）

部署策略本身是 Kubernetes 的经典能力，但在 2026 年，支撑它的周边生态发生了几处结构性变化，直接改变了蓝绿与金丝雀的落地方式：

- **Kubernetes 主线为 v1.37（Garhwal，2026-08-26 发布）**，当前补丁 1.37.2；项目维护 **1.37 / 1.36 / 1.35** 三个次版本分支，1.34 已于 2026-10-27 EOL。部署相关能力（Deployment 滚动参数、探针、`rollout` 子命令）均为稳定 API，可放心在 v1.37 使用。来源：[Kubernetes 补丁发布说明](https://kubernetes.io/releases/patch-releases/)
- **v1.37 的 `HPAScaleToZero` 转 Beta 并默认启用**，`minReplicas: 0` 可作用于 Object/External 指标，部署策略可与弹性伸缩联动做「无流量时缩到零」，但需注意冷启动延迟。来源：[Kubernetes v1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
- **Ingress-NGINX 已于 2026-03 归档退役**，官方转向 **Gateway API**，核心资源（GatewayClass / Gateway / HTTPRoute / GRPCRoute / TLSRoute / ReferenceGrant）已 GA，官方提供 **Ingress2Gateway 1.0** 迁移工具。金丝雀/蓝绿的权重路由由此有了标准化、跨厂商一致的入口层实现。来源：[Kubernetes Blog: Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
- **Helm 4 已正式发布**（v4.0.0 于 2025-11-12），**Helm 3 最后功能版为 2026-09-09、安全补丁延至 2027-02-10**；部署脚本需注意 `--atomic`→`--rollback-on-failure`、`--force`→`--force-replace` 等破坏性旗标重命名。来源：[Helm 3 End of Life](https://v3.helm.sh/blog/helm-v3-end-of-life/) · [Helm 4 Released](https://github.com/helm/helm-www/blob/main/blog/2025-11-17-helm-4-released/index.md)
- **GitOps 持续部署**：Argo CD 最新次版本 **3.5.x（3.5.3，2026-09-14）**，v3.6 计划 2026-12-15 出 RC，支持多集群、同步策略与渐进式发布，是当前蓝绿/金丝雀落地的主流载体。来源：[Argo CD Release Process](https://argo-cd.readthedocs.io/en/stable/developer-guide/release-process-and-cadence/)
- **服务网格**：Istio 最新次版本 **1.32（2026-11-09）**，Ambient 模式自 1.24（2024-11）起 GA；借助服务网格可实现比入口层更精细的流量切分与按请求特征分流。来源：[Istio Releases](https://istio.io/latest/news/releases/)

> [!note] 说明
> 以上版本与 EOL 日期来自 2026-11-19 的调研快照，升级或迁移前请以官方仓库为准。

## 二、基础概念

发布策略要解决的问题只有一个：**如何在把新版本送上线的过程中，尽量不中断服务、尽量降低风险，并保留可回滚能力**。三种策略的区别本质在于「新版本和旧版本同时存在多少、流量如何切换」。

| 维度 | 滚动更新（Rolling Update） | 蓝绿（Blue/Green） | 金丝雀（Canary） |
| --- | --- | --- | --- |
| 核心思路 | 逐个替换旧副本，边换边服务 | 全套新环境就绪后一次性切换流量 | 先让少量流量进入新版本，逐步放量 |
| 新旧并存 | 过渡期少量并存 | 始终两套完整并存 | 按比例并存，比例逐步放大 |
| 回滚速度 | 回滚也走一次滚动，较慢 | 秒级切回旧环境，最快 | 需再次调权重，较快 |
| 资源成本 | 最低（基本不额外占资源） | 最高（需双份资源） | 中等（随放量比例增长） |
| 流量控制精度 | 只能控制节奏，不能控制比例 | 只能整体切换，不能按比例 | 可按权重/请求特征精确切分 |
| 典型适用 | 无状态常规发布、资源敏感 | 关键业务、需快速回滚 | 高风险变更、面向真实流量验证 |

**关键术语**：

- **maxSurge / maxUnavailable**：滚动更新的两个控制阀。`maxSurge` 表示更新过程中最多能多创建的副本数（可超过期望副本数），`maxUnavailable` 表示最多允许多少副本不可用（少于期望副本数）。二者共同决定发布节奏与可用性下限。
- **就绪探针（readinessProbe）**：决定 Pod 是否接入流量。滚动/蓝绿/金丝雀都依赖它保证「只有真正就绪的新副本才会被放进流量」。
- **流量切换面**：蓝绿/金丝雀需要依赖一个「流量入口」来切流——Service 选择器（集群内）、Ingress/Gateway API（南北向）、服务网格（东西向按请求分流）。

> [!tip] 记忆法
> 滚动＝「边换边开」，蓝绿＝「先备好再换挡」，金丝雀＝「先放一小撮再逐步加量」。先想清楚「回滚容忍时间」和「资源预算」，策略就定了。

## 三、核心机制

### 3.1 滚动更新：Deployment 的控制器对账

Deployment 控制器通过 ReplicaSet 实现滚动：创建新 ReplicaSet 逐步扩到目标副本，同时把旧 ReplicaSet 缩到 0。整个过程是**声明式对账**——你只需声明期望状态（副本数、镜像、滚动参数），控制器持续把实际状态收敛过去。

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1          # 更新时最多比期望副本多 1 个（可为百分比）
    maxUnavailable: 0    # 更新时不允许任何副本不可用，保证容量不降
```

- `maxSurge: 1, maxUnavailable: 0`：最稳，全程容量不降，但发布较慢（先扩后缩）。
- `maxSurge: 0, maxUnavailable: 1`：最快，先缩后扩，适合非关键服务，但更新瞬间容量略降。
- 滚动期间，`readinessProbe` 决定新副本何时被 Service 的 EndpointSlice 纳入流量，因此**探针没通过就不会接流量**，这是滚动更新不中断服务的关键。

### 3.2 蓝绿：两个 Deployment + 一个流量入口

蓝绿不是 Kubernetes 内建的控制器，而是一种**模式**：部署两套完全相同的 Deployment（蓝、绿），二者共用同一组标签选择器之外的区分标签，通过**切换 Service 的 selector** 或**入口层路由**把流量整体指向新版本。旧环境保持不动，一旦异常可瞬间切回。

- **集群内切流**：两个 Deployment 用不同标签（`version: blue|green`），Service 的 `selector` 指向谁，流量就去谁。切流即改一行 selector。
- **入口层切流**：由 Ingress/Gateway API 或负载均衡器把入口指向新环境，Service 不必改，适合跨命名空间或多集群。

### 3.3 金丝雀：按权重或请求特征分流

金丝雀同样是模式而非内建能力，主流实现分三层：

- **入口层权重**：Gateway API 的 `HTTPRoute` 用 `match` 把流量按权重分配到新旧两组后端（`weight` 字段，Kubernetes 1.30+ 支持按权重负载均衡），标准化且跨厂商一致。
- **服务网格**：Istio 等通过 `VirtualService` 的 `weight` 或基于请求头/用户维度的 `match` 做更精细的分流，可按「内部用户先试用」等真实特征切流。
- **渐进发布控制器**：Argo Rollouts、Flagger 等 CRD 控制器，把「按权重放量 → 观察指标 → 自动晋升或回滚」编排成一条流水线，可与 Prometheus 指标联动做自动决策。

## 四、实践步骤（含代码/命令示例）

以下示例以 `web-demo` 无状态应用为例，镜像与标签按环境替换即可。

### 4.1 滚动更新：最常规的发布

**1. 声明 Deployment（含滚动参数与就绪探针）**

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
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
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
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 15
            periodSeconds: 20
```

**2. 发布新版本并观察滚动过程**

```bash
# 更新镜像（声明式更新）
kubectl set image deployment/web-demo web=registry.example.com/web-demo:v2 --record

# 实时观察 rollout 进度，直到 "successfully completed"
kubectl rollout status deployment/web-demo

# 查看每次变更的 Revision 记录
kubectl rollout history deployment/web-demo
kubectl rollout history deployment/web-demo --revisions=5
```

**3. 回滚（滚动更新内置回滚能力）**

```bash
kubectl rollout undo deployment/web-demo --to-revision=2
kubectl rollout status deployment/web-demo
```

> [!warning] 生产镜像 tag
> 示例中 `nginx:1.27-alpine` 为演示用可变标签。生产环境应使用**镜像摘要（digest）**或不可变版本号，避免同 tag 覆盖导致「代码变了镜像没换」。

### 4.2 蓝绿：两套环境一键切换

**1. 部署「蓝」环境**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-demo-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-demo
      slot: blue
  template:
    metadata:
      labels:
        app: web-demo
        slot: blue
    spec:
      containers:
        - name: web
          image: registry.example.com/web-demo:v1
          ports:
            - containerPort: 80
```

**2. 部署「绿」环境（同模板，仅改 `slot: green` 与镜像）**

```bash
kubectl apply -f deployment-green.yaml
kubectl rollout status deployment/web-demo-green
```

**3. 让 Service 指向蓝环境**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-demo
spec:
  selector:
    app: web-demo
    slot: blue        # ← 切流时只需把 blue 改成 green
  ports:
    - name: http
      port: 80
      targetPort: 80
```

**4. 切换与回滚**

```bash
# 切流到绿环境（新版本）
kubectl patch svc web-demo -p '{"spec":{"selector":{"slot":"green"}}}'
kubectl get svc web-demo -o yaml | grep -A2 selector   # 确认已切换

# 验证无误后保留绿环境；若异常，一行命令切回蓝环境
kubectl patch svc web-demo -p '{"spec":{"selector":{"slot":"blue"}}}'

# 验证完成后下线旧环境
kubectl delete deployment web-demo-blue
```

### 4.3 金丝雀：Gateway API 权重放量

**1. 先部署新环境（slot: canary），与稳定版（slot: stable）并存**

```bash
kubectl apply -f deployment-stable.yaml
kubectl apply -f deployment-canary.yaml
```

**2. 用 Gateway API 的 HTTPRoute 按权重分流**

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-demo
spec:
  parentRefs:
    - name: web-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: web-demo-stable
          port: 80
          weight: 90        # 90% 流量进稳定版
        - name: web-demo-canary
          port: 80
          weight: 10        # 10% 流量进金丝雀
```

**3. 逐步放量**

```bash
# 观察金丝雀无异常后，把权重改为 30:70
kubectl patch httproute web-demo -p '{"spec":{"rules":[{"backendRefs":[{"name":"web-demo-stable","port":80,"weight":70},{"name":"web-demo-canary","port":80,"weight":30}]}]}}'

# 继续放大到 50:50、100:0，全部完成后下线稳定版
kubectl patch httproute web-demo -p '{"spec":{"rules":[{"backendRefs":[{"name":"web-demo-canary","port":80,"weight":100}]}]}}'
```

> [!tip] 进阶
> 若需「观察指标自动决定放量」，可使用 **Argo Rollouts**：其 `Canary` 策略支持按权重步进、基于 Prometheus 指标做分析与自动回滚，是金丝雀的自动化版本；只需先安装 Argo Rollouts CRD。

### 4.4 GitOps 方式：Argo CD 统一编排

将上述清单放入 Git 仓库，用 Argo CD 做声明式对账，蓝绿/金丝雀可叠加 Argo CD 的同步策略（如 `SyncWindow` 限制窗口、多集群同步）。

```bash
# 安装 Argo CD（以官方 Helm chart 为例，注意 Helm 4 旗标差异）
helm repo add argo https://argo-helm.github.io/argo-helm
helm install argocd argo/argo-cd --namespace argocd --create-namespace

# 创建 Application，指向包含部署清单的 Git 仓库
kubectl apply -f - <<'YAML'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-demo
spec:
  project: default
  source:
    repoURL: https://github.com/example/web-demo
    targetRevision: main
    path: deploy/k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
YAML
```

## 五、最佳实践与常见坑

**通用实践**

1. **就绪探针先行**：无论哪种策略，都要配 `readinessProbe`（必要时加 `startupProbe`），否则新副本未就绪就被纳入流量，蓝绿/金丝雀再精细也救不了。
2. **优雅终止**：设置 `terminationGracePeriodSeconds` 与 `preStop` 钩子，保证发布与缩容时不丢在途请求。
3. **镜像用不可变 tag/digest**：避免可变 tag 导致的「版本漂移」，这是三类策略回滚判断正确性的前提。
4. **资源预留**：蓝绿需双份资源，金丝雀按最大放量比例预留，发布前做容量确认，避免因资源不足导致 Pod 调度不上去。
5. **观测先行**：金丝雀放量前先明确观测指标（错误率、延迟、业务指标），放量每一档都设检查点；最好接入指标自动分析（Argo Rollouts / Flagger）。
6. **保持回滚路径**：蓝绿要保证旧环境在验证期内不被删除；滚动要保证 `rollout undo` 可用、ReplicaSet 历史未被清理。
7. **声明式、可审计**：切流、改权重等操作通过清单与 GitOps 完成，避免手工 `kubectl patch` 散落各处、难以追溯。

**常见坑**

| 现象 / 坑 | 原因 | 规避方法 |
| --- | --- | --- |
| 滚动更新后服务短暂报错 | `maxUnavailable` 过大，或新副本未配就绪探针就接流量 | 关键服务用 `maxUnavailable: 0`，必配 `readinessProbe` |
| 蓝绿切流后旧流量仍有残留 | 客户端长连接、缓存、或 Service 会话保持未处理 | 入口层加超时/优雅下线，或结合会话亲和评估 |
| 金丝雀权重不生效 | 后端未注册到 EndpointSlice、或入口未启用权重负载均衡 | 确认两个 Deployment 均 Ready、Gateway/网关支持 weight 分流 |
| 回滚后仍报错 | 数据库迁移等有状态变更不可回滚 | 发布前确认变更的可回滚性，兼容性优先于「一次性改完」 |
| Helm 4 升级脚本报错 | 使用已重命名的旗标（`--atomic`/`--force`） | 按官方迁移清单改为 `--rollback-on-failure` / `--force-replace` |
| Ingress 迁移后行为变化 | Ingress-NGINX 已退役，迁移到 Gateway API 存在默认行为差异 | 迁移前对比默认行为，用官方 Ingress2Gateway 工具核对 |

> [!warning] 有状态应用需谨慎
> 蓝绿/金丝雀对无状态应用最顺；涉及数据库迁移、状态写入时，需先保证迁移的可回滚与兼容性，否则「秒级切流」反而会放大故障。

## 六、核心要点速查

1. 三种策略本质是「新旧副本并存方式与流量切换方式」不同：滚动＝逐个替换，蓝绿＝整体切换，金丝雀＝按比例放量。
2. 滚动更新由 Deployment 控制器对账实现，`maxSurge` / `maxUnavailable` 控制发布节奏与可用性下限。
3. 蓝绿不是内建控制器，而是「两套 Deployment + 流量入口切流」的模式，回滚最快、资源成本最高。
4. 金丝雀的分流面有三层：Gateway API 权重、服务网格按请求分流、Argo Rollouts/Flagger 渐进发布控制器。
5. 所有策略都依赖 `readinessProbe` 决定副本是否接入流量，配好探针是安全发布的地基。
6. 截至 2026-11，K8s 主线为 **v1.37**（2026-08-26），支持 1.37/1.36/1.35 三个分支；部署相关 API 均为稳定版本。
7. 入口层方向为 **Gateway API**（核心资源 GA，Ingress-NGINX 已于 2026-03 退役），金丝雀权重路由应优先采用。
8. GitOps 以 Argo CD 3.5.x 为主流载体，用 Git 作为唯一事实来源，让切流与放量可审计、可回滚。
9. 镜像一律使用不可变 tag/digest；滚动更新用 `kubectl rollout`，蓝绿用改 Service selector，金丝雀用改 HTTPRoute weight。
10. 策略可组合：滚动打底、蓝绿保回滚、金丝雀控风险，按业务对「回滚速度」与「资源预算」的取舍选择。

## 七、学习资源

1. [Kubernetes 官方文档：Deployments（滚动更新与 rollout 命令）](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/deployment/)
2. [Kubernetes 官方文档：Service（selector 与流量）](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/)
3. [Kubernetes Blog：Ingress2Gateway 1.0（Gateway API 迁移工具）](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
4. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
5. [Gateway API 官方文档（GatewayClass / Gateway / HTTPRoute）](https://gateway-api.io/)
6. [Argo CD 官方文档：应用同步与渐进式发布](https://argo-cd.readthedocs.io/en/stable/user-guide/progressive-delivery/)
7. [Argo Rollouts 官方文档（金丝雀/蓝绿渐进发布）](https://argo-rollouts.readthedocs.io/)
8. [Helm 官方博客：Helm 3 End of Life（Helm 4 迁移时间线）](https://v3.helm.sh/blog/helm-v3-end-of-life/)
9. [Istio 官方文档：流量管理（VirtualService 权重分流）](https://istio.io/latest/docs/concepts/traffic-management/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
