---
title: DevOps 与 Kubernetes-从入门到精通
date: 2026-11-18
updated: 2026-11-18
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 容器编排
  - Helm
  - 服务网格
  - GitOps
aliases:
  - DevOps与Kubernetes
  - K8s 从入门到精通
source:
  - https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/
  - https://helm.sh/blog/helm-4-released/
  - https://istio.io/latest/news/releases/1.28.x/announcing-1.28/
  - https://kubernetes.io/releases/version-skew-policy/
---

# DevOps 与 Kubernetes-从入门到精通

> [!summary] 摘要
> 本文以「声明式、自动化、可观测、可回滚」为主线，串起云原生全栈的完整知识链路：从容器与 Docker 基础、Kubernetes 核心对象与 kubectl 操作，到控制面机制、Helm 生产实践、可观测性与安全体系，再到多集群高可用、DRA/AI 调度与 GitOps 前沿。适合准备系统建立云原生知识框架的后端/运维/SRE 工程师按「入门 → 进阶 → 精通」三阶路径阅读。

DevOps 与 Kubernetes 是以「声明式、自动化、可观测、可回滚」为核心的云原生工程体系：以容器（Docker/containerd/CRI）为交付单元，以 Kubernetes 为集群编排内核，通过 Helm 做应用打包、服务网格（Istio 等）做流量与安全治理、配置与密钥管理（ConfigMap/Secret/Vault/External Secrets Operator）做环境解耦、可观测性（Prometheus/Grafana/日志）做闭环反馈，并以 GitOps（Argo CD/Flux）与 CI/CD 实现「代码即基础设施」的持续交付，再通过多集群与高可用、云原生安全策略支撑规模化生产。

> [!note] 版本时间线
> 截至 2026-11，Kubernetes 主线为 **v1.37**（2026-08-26 发布，项目维护 1.37/1.36/1.35 三个次要版本分支），Helm 已发布 6 年来首个大版本 **Helm 4**（2025-11-12），Istio 进入 **1.28**，Docker Engine 进入 **v29**，生态整体向 DRA/GPU 调度、原生可观测性、WASM 插件与 Gateway API 方向演进。

## 一、最新动态（截至 2026-11）

> [!note] 说明
> 下表仅收录可从官方发布说明确认的内容，升级与迁移前请以官方文档为准。

| 版本 / 动态 | 发布时间 | 关键更新点 | 来源 |
| --- | --- | --- | --- |
| **Kubernetes v1.37（Garhwal）** | 2026-08-26 | 67 项增强（16 Stable / 23 Beta / 27 Alpha）+ 1 项弃用/移除。Stable：Resilient watch cache 初始化、KYAML（KEP-5295）、`metrics.k8s.io` 指标 API、Pod 证书与 ClusterTrustBundles（KEP-4317/3257）、节点声明特性（KEP-5328）、存储版本迁移 `storagemigration.k8s.io/v1`（KEP-4192）、DRA 扩展资源请求/设备污点与容忍/NUMA 属性。Beta：HPA scale to zero（`ScaledToZero` 条件）、manifest 式准入配置（KEP-5793）、gang scheduling（KEP-4671）、原生直方图（KEP-5808）、内存 QoS（cgroups v2）、Pod 级资源管理、CRI 统计取代 cAdvisor。Alpha：Pod 级 checkpoint/restore、StatefulSet `Recreate` 策略、DRA 派生属性/设备兼容组、WAS 复合 PodGroup 等。弃用/移除：kube-dns 弃用、静态 Pod 引用 Secret/ConfigMap 被禁止、`kubectl run -f` 弃用、cgroup v1 持续退出。 | [Kubernetes v1.37 发布](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/) |
| **Kubernetes v1.36（ハル / Haru）** | 2026-04-22 | 70 项增强（18 Stable / 25 Beta / 25 Alpha）。Stable：kubelet 细粒度 API 授权（KEP-2862）、用户命名空间（KEP-127）、基于 cgroup v2 的 PSI 指标（KEP-4205）、OCI artifact/image 卷源（KEP-4639）、NodeLogQuery（KEP-2258，需开 `enableSystemLogQuery`）、VolumeGroupSnapshot（KEP-3476）、可变 CSINode allocatable（KEP-4876）、外部 ServiceAccount token 签名（KEP-740）、MutatingAdmissionPolicies（KEP-3962）、validation-gen 声明式校验（KEP-5073）、移除 gogo protobuf（KEP-5589）。Beta：allocatedResourcesStatus、StrictIPCIDRValidation、`.kuberc`（默认启用）、可变 Job 资源、ConstrainedImpersonation、ComponentStatusz/ComponentFlagz（默认启用）、Mixed Version Proxy、cgroup v2 内存 QoS。Alpha：Workload Aware Scheduling（WAS）、HPA scale to zero（默认关闭）、原生直方图指标（KEP-5808）、manifest 式准入控制配置、CRI list streaming。弃用/移除：Service `.spec.externalIPs` 弃用（计划 v1.43 移除，CVE-2020-8554）、gitRepo 卷驱动永久移除（KEP-5040）；Ingress NGINX 已于 2026-03-24 退役。发布周期 15 周（2026-01-12 至 2026-04-22）。 | [Kubernetes v1.36 发布](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/) |
| **Kubernetes v1.35（Timbernetes / World Tree Release）** | 2025-12-17 | 60 项增强（17 Stable / 19 Beta / 22 Alpha）。Stable：Pod 资源原地更新（KEP-1287）、Job managedBy（KEP-4368）、Pod metadata.generation/status.observedGeneration（KEP-5067）、Service `trafficDistribution: PreferSameNode`（KEP-3015）。Beta：Pod 证书 PodCertificateRequest（KEP-4317）、节点拓扑标签经 Downward API、原生存储版本迁移、HPA tolerance、容器级重启规则、enforced kubelet 镜像凭证校验、StatefulSet maxUnavailable、KYAML（默认启用）。Alpha：gang scheduling（KEP-4671）、ConstrainedImpersonation、`/flagz` 与 `/statusz` 结构化 JSON。弃用：cgroup v1 弃用（KEP-5573，v1.35 起 `failCgroupV1` 默认 true，移除后续跟进）、kube-proxy ipvs 弃用（KEP-5495）、containerd 1.X 为最后支持版本（需迁 containerd 2.0+）、Ingress NGINX 将在 2026-03 后归档。 | [Kubernetes v1.35 发布](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/) |
| **Kubernetes v1.34（Of Wind & Will）** | 2025-08-27 | 58 项增强（23 Stable / 22 Beta / 13 Alpha）。DRA 核心（`resource.k8s.io/v1`，KEP-4381）GA；KYAML（KEP-5295）Alpha；Pod 证书（KEP-4317）Alpha。Stable：延迟创建 Job 替换 Pod、卷扩容失败恢复、VolumeAttributesClass、结构化认证配置、匿名访问细粒度控制、流式列表响应、Linux 节点 swap（LimitedSwap）、环境变量放宽。Beta：Pod 级资源请求/限制（KEP-2837，HPA 支持）、`.kuberc`、外部 ServiceAccount token 签名、MutatingAdmissionPolicies、WatchList 流式 informer、Windows 优雅关机。弃用：kubelet `cgroupDriver` 配置弃用、containerd 1.X 支持将在 v1.35 后结束。 | [Kubernetes v1.34 发布](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/) |
| **Kubernetes v1.33（Octarine）** | 2025-04-23 | 64 项增强（18 Stable / 20 Beta / 24 Alpha），周期 15 周。Sidecar 容器（KEP-753）Stable；Pod 资源原地扩缩容（KEP-1287）Beta；用户命名空间默认启用 Beta。Stable：Indexed Job 每索引退避上限、Job successPolicy、`kubectl --subresource`、Multiple Service CIDRs、kube-proxy nftables 后端、trafficDistribution 拓扑感知路由、VolumePopulators、PV reclaim policy 强制。Beta：DSR（Windows kube-proxy）、DRA 结构化参数 v1beta2、异步抢占、ClusterTrustBundles、OCI 镜像卷、ProcMount、NUMA CPUManager。弃用/移除：Endpoints API 弃用、Node `.status.nodeInfo.kubeProxyVersion` 移除、in-tree gitRepo 卷驱动移除。 | [Kubernetes v1.33 发布](https://kubernetes.io/blog/2025/04/23/kubernetes-v1-33-release/) |
| **Kubernetes v1.32（Penelope）** | 2024-12-11 | 44 项增强（13 Stable / 12 Beta / 19 Alpha），周期 14 周。自定义资源字段选择器（KEP-4358）Stable；StatefulSet PVC 自动清理（KEP-1847）Stable；结构授权配置（KEP-3221）Stable；DRA 结构化参数、Job managedBy Beta；CEL 变更准入策略、Pod 级资源规格 Alpha；`/statusz` 与 `/flagz` 端点。移除 `flowcontrol.apiserver.k8s.io/v1beta3`。 | [Kubernetes v1.32 发布](https://kubernetes.io/blog/2024/12/11/kubernetes-v1-32-release/) |
| **Helm v4.0.0** | 2025-11-12 | 6 年来首个大版本（于 KubeCon + CloudNativeCon 的 Helm 4 发布演讲中发布）。重新设计的插件系统（支持基于 WebAssembly 的插件）、post-renderer 变为插件、支持 Server Side Apply、基于 kstatus 的改进资源等待、本地内容缓存（如 chart）、通过 `slog` 记录日志、可复现/幂等的 chart 归档构建、更新 SDK API（支持多 chart API 版本，实验性 v3 chart API 即将推出）。Helm v3 支持期：缺陷修复至 2026-09-09（最终受限功能版本），安全修复延长至 2027-02-10，不回填功能特性（仅回填 K8s 客户端库以支持新 K8s 版本）。 | [Helm 4 Released](https://helm.sh/blog/helm-4-released/) |
| **Istio 1.28.0** | 2025-11-05 | InferencePool v1（Gateway API Inference Extension，面向生成式 AI 推理流量管理）；Ambient 多集群改进（waypoint 可跨网络路由，仍为 Alpha）；Ambient 模式原生 nftables 支持；双栈支持升级 Beta；安全增强（JWT `spaceDelimitedClaims`、istiod NetworkPolicy、`seccompProfile`、FrontendTLSValidation）；Gateway API v1.4 的 BackendTLSPolicy v1；Helm chart 新增 `resourceScope`（persona 化安装）。 | [Announcing Istio 1.28](https://istio.io/latest/news/releases/1.28.x/announcing-1.28/) |
| **Docker Engine v29** | 29.5.0 于 2026-05-14 | `gvisor-tap-vsock` 成为新的默认 rootless 网络驱动，`slirp4netns` 不再随 Docker 打包；支持容器默认启用私有 time namespace（受支持内核）；local 日志驱动支持自定义属性（`label`、`label-regex`、`env`、`env-regex`、`tag`）；`docker ps --format` 支持 `.HealthStatus` 占位符。注意：K8s 自 v1.24 移除 dockershim 后不再支持 Docker 容器运行时。 | [Docker Engine v29 Release Notes](https://docs.docker.com/engine/release-notes/29/) |
| **Kubernetes 版本支持与偏差策略** | 官方（2026-11 抓取） | 项目维护最近三个次要版本的发布分支，抓取时页面显示为「1.37、1.36、1.35」，v1.37 已于 2026-08-26 正式发布（Garhwal）；Kubernetes 1.19 及以后每个次要版本约 1 年补丁支持。版本偏差：HA 集群 kube-apiserver 新旧实例最多相差 1 个次要版本；kubelet/kube-proxy 不得比 kube-apiserver 新、最多旧 3 个次要版本（<1.25 最多 2 个）；kubectl 与 apiserver 相差 1 个次要版本（可新可旧）；controller-manager/scheduler/cloud-controller-manager 须与 apiserver 同版或旧 1 个。 | [Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/) |

## 二、入门篇

### 2.1 基础概念

**容器与 Docker 基础**：镜像是交付单元，容器提供进程级隔离与可移植运行环境。Kubernetes 自 v1.24 移除 dockershim 后以 containerd/CRI 为运行时，Docker Engine 需与容器运行时区分看待——`docker` 命令是开发者本地工具，集群中真正跑容器的是满足 CRI 的运行时。

**Kubernetes 核心心智模型**：集群由控制平面与节点组成。控制平面含 `kube-apiserver`、`etcd`、`controller-manager`、`scheduler`；节点含 `kubelet`、`kube-proxy`、容器运行时。**一切交互都通过 `kube-apiserver`**，这是理解整套体系的钥匙。

**核心对象入门**：

| 对象 | 职责 | 一句话记忆 |
| --- | --- | --- |
| Pod | 最小调度单元，一个或多个共享网络/存储的容器 | 调度与网络的最小粒度 |
| Deployment | 无状态应用的副本数与滚动更新 | 管「无状态、要扩缩」 |
| StatefulSet | 有状态应用的顺序与稳定标识 | 管「有状态、要顺序」 |
| DaemonSet | 每个节点运行一份 | 管「每节点一个」 |
| Job / CronJob | 批处理与定时任务 | 管「跑完即止」 |
| Service / EndpointSlice | 稳定访问与四层负载均衡 | 管「找得到、分得匀」 |
| ConfigMap / Secret | 配置与密钥 | 管「配置与凭据」 |

**声明式工作流**：以 YAML 声明期望状态，`kubectl apply -f` 提交，控制器持续对账（reconcile loop）使实际状态收敛到期望状态。这是 K8s 与「脚本式运维」最根本的区别。

> [!warning] 易混淆点
> Secret 仅做 Base64 编码、**不是加密**。凡涉及真实凭据（数据库口令、云厂商 AK/SK），生产环境必须配合外部密钥系统（如 Vault + External Secrets Operator），不能把 Secret 当作加密存储用。

### 2.2 环境准备

- **本地快速起步**：Minikube、Kind、Docker Desktop 都能在几分钟内拉起单节点集群。开发与学习场景首选 Kind（跑在容器里，无需虚拟机）。
- **生产集群**：常用 `kubeadm` 自建，或直接用云厂商托管集群（EKS/AKS/GKE/ACK/CCE），也可使用 K3s、RKE 等发行版降低运维成本。
- **版本基线**：动手前先确认 K8s 与运行时版本。v1.35 起 containerd 1.X 不再受支持，需迁移到 containerd 2.0+；K8s v1.24 起不再内置 Docker 运行时支持。

> [!tip] 验证集群就绪
> `minikube start` 完成后，执行 `kubectl get nodes`，看到节点状态为 `Ready` 即说明集群可用；再执行 `kubectl get pods -A` 观察系统组件是否正常调度。

### 2.3 第一个实践（含代码示例）

下面以「部署一个无状态 Web 应用」走一遍完整声明式流程：写清单 → 提交 → 校验 → 观察 → 访问。

**1. 声明期望状态**（`deployment.yaml`）：

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
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
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
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]
      terminationGracePeriodSeconds: 30
```

**2. 暴露稳定访问**（`service.yaml`）：

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

**3. 提交并观察**：

```bash
# 应用清单（声明式提交）
kubectl apply -f deployment.yaml -f service.yaml

# 查看资源与事件，确认滚动是否正常
kubectl get pods -l app=web-demo -o wide
kubectl rollout status deployment/web-demo
kubectl describe deployment/web-demo

# 临时暴露到本机端口，便于验证（仅开发环境）
kubectl port-forward svc/web-demo 8080:80
```

**4. 回滚（K8s 的可回滚是内置能力）**：

```bash
kubectl rollout history deployment/web-demo
kubectl rollout undo deployment/web-demo --to-revision=1
```

> [!tip] 关于镜像 tag
> 示例中 `nginx:1.27-alpine` 是为方便演示的可变标签。生产环境镜像 tag 应使用**摘要（digest）**而非可变标签，避免同 tag 覆盖导致“改了代码却没换镜像”的问题。

## 三、进阶篇

### 3.1 核心机制

**控制面与数据面机制**：`kube-apiserver` 是唯一入口，`etcd` 持久化全部状态，控制器与调度器通过 watch/informer 异步对账。理解该机制是排查集群问题的钥匙——绝大多数“状态不对”的现象，本质都是控制器没把实际状态收敛回声明状态。

**工作负载控制器**：按负载特性选择控制器并配好镜像拉取策略与滚动参数。Deployment 管副本与滚动更新，StatefulSet 管有状态应用的顺序与稳定标识（`spec.serviceName` + `podManagementPolicy`），DaemonSet 管每节点一份，Job/CronJob 管批处理。

**Pod 生命周期与探针**：容器具备 Init、Startup、Readiness、Liveness、PostStart/PreStop 钩子。`readinessProbe` 决定「是否接流量」，`livenessProbe` 决定「是否重启」，二者不可混用；配合 `terminationGracePeriodSeconds` 与 `preStop` 钩子实现优雅终止，保证发布与缩容不丢请求。

**资源治理**：`requests` 决定调度依据，`limits` 决定上限，二者共同决定 QoS 等级（Guaranteed/Burstable/BestEffort）。HPA/VPA 实现自动扩缩，v1.36 起 cgroup v2 PSI（Pressure Stall Information）指标成为 Stable，建议结合真实压力信号而非仅看 CPU 利用率调优。

**网络与流量**：Service 类型含 ClusterIP/NodePort/LoadBalancer/ExternalName，配合 EndpointSlice 与 kube-proxy 模式（iptables/ipvs/nftables）做四层负载均衡。Ingress 与更现代的 Gateway API 负责南北向入口，NetworkPolicy 做东西向隔离。

**存储**：PVC/PV/StorageClass/CSI 实现动态供给，配合 VolumeSnapshot、VolumeAttributesClass、VolumeGroupSnapshot 做数据保护与性能分级。

**可观测性三件套**：Prometheus 采集指标、Grafana 可视化、Alertmanager 告警，日志用 Fluent Bit/Loki 等组件汇聚，再与指标、链路统一关联（OpenTelemetry 作为统一采集层）。

**CI/CD 入门链路**：在 CI 中构建镜像 → 推送镜像仓库 → 触发部署；可由 GitOps 工具（Argo CD/Flux）以声明方式把仓库变更同步到集群，实现可审计的自动交付。详见 [[Jenkins流水线配置]]。

### 3.2 最佳实践

**Helm 生产最佳实践**：

- **values 分层**：默认值（`values.yaml`）→ 环境值 → 覆盖值，用 `-f` 逐层叠加，避免把环境差异写死在模板里。
- **`_helpers.tpl` 统一命名与标签**：把 `fullname`、`selectorLabels`、`labels` 等抽成模板，保证所有资源标签一致，便于按标签筛选与治理。
- **把 `helm lint` / `helm template` / `helm diff` 纳入 CI**：渲染前先校验、比对变更，避免把错误清单发布到集群。
- **抽取库 chart 复用片段**：公共的 Pod 注解、监控配置、资源模板沉淀为库 chart，减少重复。
- **镜像 tag 生产用摘要（digest）**，见 2.3 的提示。

```bash
# Helm 常用命令组合
helm create my-app
helm lint my-app
helm template my-app my-app --set replicaCount=3   # 本地渲染，不落集群
helm install my-app my-app -f values-prod.yaml
helm upgrade my-app my-app -f values-prod.yaml
helm rollback my-app 1
helm dependency update my-app
```

**GitOps 实践**：Flux 与 Argo CD 均为 CNCF 毕业项目，以轮询式对账把 Git 仓库状态同步到集群。Flux 是 AKS 原生集成的集群扩展（支持 K8s 清单、Helm chart、Kustomization）；Argo CD 支持原生 Cosign 签名校验。二者都把「Git 仓库」当作唯一事实来源，人工直接改集群的行为应被禁止或限制。

**配置与密钥**：ConfigMap 存非敏感配置，Secret 存敏感信息；生产接入 HashiCorp Vault + External Secrets Operator（`ClusterSecretStore` / `ExternalSecret`，支持 Vault、AWS Secrets Manager 与 IRSA），或用 CSI provider 动态注入，避免静态凭据。

**安全配置**：RBAC 最小权限、Pod Security Standards / 准入控制（Kyverno、OPA/Gatekeeper、MutatingAdmissionPolicies）做策略治理，镜像供应链做扫描、签名、Cosign 与镜像凭证校验。

> [!warning] 版本升级前先清弃用项
> 重点关注各版本弃用与移除项：Service `externalIPs`（计划 v1.43 移除）、gitRepo 卷驱动（已永久移除）、cgroup v1（v1.35 弃用，后续版本移除）、containerd 1.X（v1.35 后不支持）、kube-proxy ipvs（v1.35 弃用）、Ingress NGINX（2026-03-24 退役）。**提前迁移，避免升级后被动回滚。**

### 3.3 常见问题与排查

| 现象 | 典型原因 | 排查动作 |
| --- | --- | --- |
| `ImagePullBackOff` | 镜像名/标签错误、私有仓库未配凭证、节点网络不通 | `kubectl describe pod` 看事件；确认 image 拼写、`imagePullSecrets` 与仓库凭证 |
| `CrashLoopBackOff` | 启动命令错误、配置缺失、依赖未就绪 | `kubectl logs <pod> --previous` 看上一轮日志；检查探针与环境变量 |
| `Pending`（长期不调度） | 资源不足、亲和性/污点不满足、PVC 未绑定 | `kubectl describe pod` 看 Events；核对 requests、nodeSelector、tolerations、PVC 状态 |
| Pod 崩溃且无日志 | 硬件故障导致容器异常退出 | v1.36 可用 `kubectl describe pod` 查看 `allocatedResourcesStatus` 中的设备健康状态 |
| 节点级问题难定位 | kubelet/kube-proxy 日志不在容器里 | v1.36 的 NodeLogQuery（KEP-2258，需开 `enableSystemLogQuery`）可直接查询节点日志 |
| 变更后状态不收敛 | 控制器对账失败、被准入策略拦截 | `kubectl describe` 看事件；检查 MutatingAdmissionPolicies / Kyverno 等准入策略日志 |

**排查口诀**：先看事件（`describe`），再看日志（`logs`，必要时 `--previous`），再看状态与资源（`get -o wide`），最后怀疑调度与准入链路。

## 四、精通篇

### 4.1 架构与设计

**控制平面高可用架构**：多 `etcd` + 多 `kube-apiserver` 前置负载均衡，跨故障域（可用区/机房）部署节点。HA 集群内 kube-apiserver 新旧实例最多相差 1 个次要版本，这是安全滚动升级控制面的前提。

**升级顺序（硬约束）**：先 apiserver，再控制面组件（controller-manager/scheduler/cloud-controller-manager，须与 apiserver 同版或旧 1 个），最后 kubelet/kube-proxy（不得比 apiserver 新，最多旧 3 个次要版本）。kubectl 与 apiserver 相差 1 个次要版本即可（可新可旧）。

**多集群与联邦化**：Karmada、Cluster API、Fleet、Liqo 等面向多集群的编排、纳管与跨集群服务发现；多集群可结合服务网格 Ambient（waypoint 跨网络路由，仍为 Alpha）实现跨网络的统一流量与策略治理。

**服务网格架构选型**：Istio 提供 Sidecar 与 Ambient 两种模式——Ambient 以 waypoint 做 L4/L7 治理、原生 nftables、支持双栈 Beta；Linkerd 以轻量数据面见长。服务网格解决东西向流量、熔断重试、mTLS 与可观测性，需权衡性能开销与运维成本。

**DRA 与 AI/GPU 负载前沿**：动态资源分配（DRA）已从 v1.34 核心 GA（`resource.k8s.io/v1`）演进到 v1.36 的多项 Beta/Alpha（可分区设备、可消耗容量、设备污点与容忍、资源健康状态），是替代传统设备插件的下一代硬件管理主线；配合 Workload Aware Scheduling（WAS）、gang scheduling（KEP-4671）与 Kueue 等批处理调度，支撑大模型训练等分布式负载。

### 4.2 生产实践

**云原生安全体系（4C 纵深防御）**：按生命周期分层控制——

- **开发阶段（Code）**：零信任、威胁建模、模糊测试与安全混沌工程。
- **分发阶段（Container/制品）**：镜像/制品供应链安全——扫描、签名、信任链、私有仓库。
- **部署阶段（Cluster）**：限制可部署内容/人员/位置、镜像制品加密身份校验、RBAC 与准入控制。
- **集群与云层（Cloud/Cluster）**：最小权限、网络策略、密钥隔离、审计。

**密钥管理高阶实践**：生产避免静态凭据与仅 Base64 的 Secret，采用 HashiCorp Vault 配合 External Secrets Operator（`ClusterSecretStore` / `ExternalSecret`，支持 Vault/AWS Secrets Manager 与 IRSA）或 CSI provider 动态注入，并结合 Pod 证书（KEP-4317）、外部 ServiceAccount token 签名（KEP-740）等机制实现工作负载身份。

**可观测性规模化**：Prometheus 单机自治但受规模限制，大规模场景用分片、长周期存储（Thanos/Cortex/Mimir）与 Prometheus Operator；v1.36 引入原生直方图（KEP-5808）提供稀疏直方图，以更高精度刻画 apiserver 延迟分布，推动 SLI/SLO 高保真；OpenTelemetry 作为统一指标/日志/链路采集标准，降低多组件采集成本。详见 [[Prometheus监控入门]]。

**GitOps 与供应链一体化**：Git 仓库即唯一事实来源，用 Flux/Argo CD 做持续对账，结合 Cosign 对镜像与清单签名校验、Kyverno/OPA 准入策略，实现「签名—策略—部署」闭环，降低人工操作与越权风险。

**CI/CD 架构演进**：构建阶段产出镜像与 OCI 制品。v1.36 OCI artifact/image 卷源 GA，使模型、静态资源也能作为 OCI 制品随镜像同源分发，简化数据交付与 CI/CD 流水线；配合可复现/幂等构建与 Helm 4 的 `slog` 日志，提升交付可审计性。详见 [[Jenkins流水线配置]] 与 [[Dockerfile编写指南]]。

**性能与规模调优**：关注 kubelet/CRI 的大规模节点内存与延迟（v1.36 CRI list streaming Alpha 用流式 RPC 降低内存峰值）、调度器与 watch cache 的韧性（流式列表响应、watch cache 初始化韧性），以及 cgroup v2 内存 QoS 的分层保护。

**发行版与云厂商支持周期**：Kubernetes 上游维护最近三个次要版本；云厂商策略各异——Azure AKS 提供约 1 年社区支持 + 1 年 LTS，Amazon EKS 每版本 14 个月标准支持 + 12 个月延期支持，华为云 CCE 新集群自 v1.34 起不支持 Docker 运行时（此类厂商策略以各厂商官方文档为准）。

### 4.3 生态与前沿

- **插件化与工具链**：Helm 4 重写插件系统并支持 WebAssembly 插件，post-renderer 亦成为插件，配合本地内容缓存与 SDK API 更新，为平台工程提供可扩展的定制能力。
- **可观测性标准化**：OpenTelemetry 统一指标/日志/链路采集，Prometheus 原生直方图提升 SLO 保真度。
- **网络入口演进**：Ingress NGINX 已于 2026-03-24 退役，官方建议迁移至 **Gateway API**；kube-proxy 向 nftables 演进、IPVS 弃用。
- **运行时与内核基线**：containerd 2.x 成为必需、cgroup v1 退出，升级前需完成运行时与内核基线改造。
- **AI 推理流量治理**：Istio 1.28 的 InferencePool v1 面向生成式 AI 推理流量管理，是服务网格切入 AI 负载的标志性能力。

> [!tip] 前沿技术的取舍
> Alpha/Beta 特性（如 WAS、HPA scale to zero、Ambient 跨网络路由）适合早期验证与技术储备，**不建议直接用于核心生产链路**。引入前先在灰度环境验证，并准备回滚方案。

## 五、核心要点速查

1. Kubernetes 是云原生的集群编排内核：控制平面（apiserver/etcd/controller-manager/scheduler）+ 节点（kubelet/kube-proxy/CRI）构成完整运行体系。
2. Pod 是最小调度单元，Deployment/StatefulSet/DaemonSet/Job 是不同负载形态的控制器抽象。
3. 声明式对账（reconcile loop）是 K8s 核心机制：控制器持续把实际状态收敛到 YAML 声明的期望状态。
4. Service/EndpointSlice/kube-proxy 提供稳定访问与四层负载均衡，Ingress/Gateway API 处理南北向入口，NetworkPolicy 做网络隔离。
5. ConfigMap 存配置、Secret 存敏感数据，但 Secret 仅 Base64 编码非加密，生产需外部密钥系统。
6. Helm 是 K8s 应用打包与分发标准，Chart 由 Chart.yaml/values.yaml/templates 等组成；v4.0.0（2025-11-12）支持 WASM 插件与 Server Side Apply。
7. GitOps 以 Git 为唯一事实来源，Flux 与 Argo CD（均为 CNCF 毕业项目）做声明式持续对账，实现可审计交付。
8. 可观测性三支柱：Prometheus 指标（PromQL、拉模型）+ Grafana 可视化 + Alertmanager 告警，日志与链路经 OpenTelemetry 统一采集。
9. 安全以 RBAC 最小权限、Pod Security Standards、准入策略（Kyverno/OPA/MutatingAdmissionPolicies）与镜像供应链签名为核心。
10. 截至 2026-11，Kubernetes 主线为 v1.37（2026-08-26 发布，Garhwal），项目维护 1.37/1.36/1.35 三个次要版本分支。
11. v1.36 关键 GA：kubelet 细粒度授权、用户命名空间、cgroup v2 PSI、OCI 卷源、NodeLogQuery、VolumeGroupSnapshot、MutatingAdmissionPolicies。
12. v1.36 弃用/移除：Service externalIPs 弃用（计划 v1.43 移除）、gitRepo 卷驱动永久移除、Ingress NGINX 已于 2026-03-24 退役。
13. 升级必须遵守版本偏差策略：kubelet/kube-proxy 不得比 apiserver 新，最多旧 3 个次要版本；控制面组件须同版或旧 1 个。
14. DRA（动态资源分配）成为 GPU/AI 硬件管理主线：v1.34 核心 GA，v1.36 扩展可分区设备、设备污点等能力。
15. 服务网格：Istio 提供 Sidecar 与 Ambient 两种模式，1.28 引入 InferencePool v1 面向 AI 推理流量。
16. 高可用要点：多 etcd、多 apiserver 负载均衡、跨故障域部署，并按「apiserver → 控制面组件 → kubelet/kube-proxy」顺序滚动升级。
17. 容器运行时：K8s 自 v1.24 移除 dockershim，运行时以 containerd 等 CRI 实现为主；v1.35 起 containerd 1.X 不再受支持。
18. 生产交付应固化 Helm 最佳实践：values 分层、`_helpers.tpl` 统一标签、lint/template/diff 进 CI、镜像用摘要。
19. 可观测性与成本：以 OpenTelemetry 统一采集，配合集中后端与分布式采集器，避免多套采集链路重复投入。
20. 核心命令：`kubectl get/describe/logs/exec/apply -f`；Helm 的 `helm create/lint/template/install/upgrade/rollback`。

## 六、学习资源

以下为外部官方文档与权威来源，建议以官方说明为准。

1. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)
2. [Kubernetes 官方博客：Kubernetes v1.36 发布（ハル / Haru）](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
3. [Kubernetes 官方博客：Kubernetes v1.35 发布（Timbernetes）](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
4. [Kubernetes 官方博客：Kubernetes v1.34 发布（Of Wind & Will）](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
5. [Kubernetes 官方博客：Kubernetes v1.33 发布（Octarine）](https://kubernetes.io/blog/2025/04/23/kubernetes-v1-33-release/)
6. [Kubernetes 官方博客：Kubernetes v1.32 发布（Penelope）](https://kubernetes.io/blog/2024/12/11/kubernetes-v1-32-release/)
7. [Kubernetes 官方：Version Skew Policy（版本偏差策略）](https://kubernetes.io/releases/version-skew-policy/)
8. [Helm 官方博客：Helm 4 Released](https://helm.sh/blog/helm-4-released/)
9. [Helm 官方博客：Helm 3 End of Life（支持期时间线）](https://helm.sh/blog/helm-v3-end-of-life/)
10. [Helm 官方文档：Charts（Chart 结构与约定）](https://helm.sh/docs/topics/charts/)
11. [Istio 官方：Announcing Istio 1.28](https://istio.io/latest/news/releases/1.28.x/announcing-1.28/)
12. [Prometheus 官方文档：Overview（数据模型与架构）](https://prometheus.io/docs/introduction/overview/)
13. [Kubernetes 官方文档：云原生安全和 Kubernetes](https://v1-34.docs.kubernetes.io/docs/concepts/security/cloud-native-security/)
14. [Microsoft Learn：在 AKS 上使用 GitOps 的蓝图（Flux 与 Argo CD）](https://learn.microsoft.com/zh-cn/azure/architecture/example-scenario/gitops-aks/gitops-blueprint-aks)
15. [Docker 官方文档：Engine v29 Release Notes](https://docs.docker.com/engine/release-notes/29/)

## 七、关联笔记

- [[DevOps]]
- [[Dockerfile编写指南]]
- [[Docker-compose示例]]
- [[Kubernetes部署实践]]
- [[Jenkins流水线配置]]
- [[Prometheus监控入门]]
- [[Linux-从入门到精通]]

## 八、变更记录

- 2026-11-18 首次创建
- 2026-11-18 审校：新增 v1.37（Garhwal，2026-08-26）最新动态与资源；更新 Helm v3 支持期为缺陷修复至 2026-09-09、安全修复至 2027-02-10；修正 v1.35 的 cgroup v1 表述（弃用而非已移除）、KEP-5495 ipvs 弃用归属，并将主线表述更新为 v1.37。
