---
title: DevOps 与 Kubernetes 调研
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 容器
  - 云原生
  - 调研
---

> 调研范围：为「DevOps 与 Kubernetes」方向 18 个知识点核实截至 **2026 年 11 月**的官方支持状态、关键版本号与弃用/变更事实。所有事实均附官方来源 URL，供后续撰写 18 篇详细文档引用。检索时间：2026-11-19。

## 一、主题最新动态（截至 2026-11）

- **Kubernetes 最新稳定版本为 v1.37（代号 Garhwal）**，于 2026-08-26 发布；截至 2026-11 已发布补丁 1.37.2。当前官方文档站点默认版本即为 v1.37。1.37 是近年来与 AI/批量工作负载最相关的版本：动态资源分配（DRA）扩展资源支持进入 **GA**、HPA scale-to-zero 转 **Beta**、Pod 级 checkpoint/restore、根less（KubeletInUserNamespace）转 Beta、工作负载感知调度继续演进。
- **Kubernetes 支持策略为「最近 3 个次版本分支 + 约 14 个月支持期」**（12 个月标准 + 2 个月维护期）。截至 2026-11 活跃分支为 **1.37 / 1.36 / 1.35**；1.34 已于 2026-10-27 结束生命周期（EOL），1.33 于 2026-06-28 EOL。
- **Helm 4 已正式发布**：v4.0.0 于 2025-11-12（KubeCon + CloudNativeCon 期间）发布，是 6 年来首个大版本。**Helm 3 进入 EOL 倒计时**：最后一次（受限）功能版为 **2026-09-09**，安全补丁延长至 **2027-02-10**；之后彻底停止更新。写作时必须提示读者迁移到 Helm 4。
- **Ingress-NGINX 项目已于 2026-03 归档/退役**，官方转向 **Gateway API**（核心资源 GatewayClass / Gateway / HTTPRoute / GRPCRoute / TLSRoute / ReferenceGrant 已 GA）。这是 2026 年网络方向最重要的事实之一。
- **服务网格**：Istio 最新次版本 **1.32（2026-11-09 发布）**；1.30 将于 **2026-12-16 EOL**；Ambient 模式自 **1.24（2024-11）起 GA**，官方推进 sidecar → ambient 迁移。
- **可观测性**：Prometheus 最新 **3.16.0（2026-11-04）**，同时维护 LTS 线 **3.13.x**；Loki 最新 **3.7.x**，其 Helm chart 自 2026-03-16 起移交社区仓库 `grafana-community/helm-charts`；Fluent Bit 最新 **5.1.4（2026-10-12）**。
- **Docker 生态**：Docker Engine 最新 **29.9.2（2026-10-20）**，内嵌 containerd **v2.4.2**；Docker Desktop 最新 **4.98.0**。Dockerfile/构建最佳实践基于 BuildKit + containerd 镜像存储。
- **备份与 GitOps**：Velero 最新 **1.18.x（1.18.4，2026-10-12）**；Argo CD 最新次版本 **3.5.x（3.5.3，2026-09-14）**，v3.6 计划 2026-12-15 出 RC。

## 二、版本与关键事实表

### 2.1 Kubernetes

| 版本号 | 发布日期 | 关键变化 | 官方来源 URL |
|---|---|---|---|
| **1.37（Garhwal）** | 2026-08-26 | 最新稳定版；DRA 扩展资源支持 GA、DRA 设备污点/容忍 Stable、HPAScaleToZero Beta、Pod 级 checkpoint/restore Beta、KubeletInUserNamespace（rootless）Beta、manifest-based admission control Beta、工作负载感知调度（CompositePodGroup 多级编组）；当前补丁 1.37.2；EOL 2027-10-28 | [kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/) · [K8s 1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md) · [K8s 1.37 DRA Updates](https://kubernetes.io/zh-cn/blog/2026/09/03/kubernetes-v1-37-dra-updates/) |
| **1.36（Haru）** | 2026-04-22 | 共 70 项增强（18 GA / 25 Beta / 25 Alpha）；SELinux 卷标签变更计划；当前补丁 1.36.6 | [kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/) · [K8s v1.36 Sneak Peek](https://kubernetes.io/blog/2026/03/30/kubernetes-v1-36-sneak-peek/) |
| **1.35（Timbernetes / 世界树）** | 2025-12-17 | KYAML 由 Alpha 升 Beta 且**默认启用**（`KUBECTL_KYAML=false` 可关）；挂起 Job 可修改资源（MutablePodResourcesForSuspendedJobs）；Pod 证书、节点声明特性、Pod 资源 in-place 更新（GA）、taints 支持数值；cgroup v1 支持被移除 | [kubernetes.io v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/) · [v1.35 Sneak Peek（弃用与移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/) |
| **1.34（Of Wind & Will / O' WaW）** | 2025-08-27 | Pod 级资源请求/限制 Beta、`.kuberc`（kubectl 偏好）Beta 默认启用、外部 ServiceAccount 令牌签名、`ListFromCacheSnapshot` 默认启用、MutatingAdmissionPolicy Beta；无关键 API 移除 | [kubernetes.io v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/) · [Fairwinds 1.34 解读](https://www.fairwinds.com/blog/kubernetes-1.34-released-whats-new-upgrade) |
| **1.33** | 2025-04-23 | **Endpoints API v1 废弃**（改用 EndpointSlice）；`resource.k8s.io/v1beta1` 废弃；ValidatingAdmissionPolicy v1alpha1 移除；Git-Repo 卷插件默认禁用；`DisableNodeKubeProxyVersion` 默认启用 | [Volcengine K8s v1.34 版本说明（含 1.33 变更）](https://docs.volcengine.com/docs/vke/vke-for-kubernetes-v1-34?lang=zh) · [kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/) |
| **1.34 EOL** | 2026-10-27 | 已进入维护模式并结束生命周期（最后补丁 1.34.13） | [kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/) |
| **1.33 EOL** | 2026-06-28 | 最后补丁 1.33.13 | [kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/) |

**支持策略要点**：补丁每月一次；支持约 14 个月（12 个月标准期 + 2 个月维护期，维护期仅处理 CVE、依赖/基础镜像、关键核心问题）；目标日期固定在每月 28 日。当前维护的文档版本为 **v1.37**。来源：[kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/)、[kubernetes.io/docs/home/supported-doc-versions](https://kubernetes.io/docs/home/supported-doc-versions/)、[kubernetes.io/releases/version-skew-policy](https://kubernetes.io/releases/version-skew-policy/)。

### 2.2 Helm

| 版本号 | 发布日期 | 关键变化 | 官方来源 URL |
|---|---|---|---|
| **Helm 4.x（v4.0.0）** | 2025-11-12 | 6 年来首个大版本；插件系统重做（可选 WebAssembly 插件运行时）、post-renderer 改为插件、**server-side apply 为新 release 默认**、kstatus 资源状态追踪、多文档 values、稳定 SDK API；破坏性变更：`--atomic`→`--rollback-on-failure`、`--force`→`--force-replace`、`helm registry login` 仅接受域名 | [Helm 4 Released](https://github.com/helm/helm-www/blob/main/blog/2025-11-17-helm-4-released/index.md) · [Helm 3 EOL（含 Helm 4 新特性）](https://v3.helm.sh/blog/helm-v3-end-of-life/) |
| **Helm 3（EOL）** | 最后功能版 **2026-09-09**；安全补丁至 **2027-02-10** | 最后一次受限功能版仅限 Kubernetes 客户端库更新（支持新 K8s 版本）；此后仅安全补丁，无功能、无 bug 修复 | [Helm 3 End of Life](https://v3.helm.sh/blog/helm-v3-end-of-life/) |

### 2.3 Docker / 容器运行时

| 版本号 | 发布日期 | 关键变化 | 官方来源 URL |
|---|---|---|---|
| **Docker Engine 29.9.2** | 2026-10-20 | 29.x 最新补丁；内嵌 containerd v2.4.2（修复 CVE-2026-95839 等安全漏洞）；BuildKit v0.32.2 | [Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/) |
| **Docker Desktop 4.98.0** | 2026-11（最新） | 桌面端最新；内置 Docker Compose v5.0.2、Docker Buildx v0.31.1、Docker Sandbox；`--user` 模式成为 Windows 新安装默认 | [Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/) |
| **containerd 2.4.x** | 2.x（2.4.0 于 2026-09） | 被 Docker Engine 29.9.1+ 内嵌；上游 Kubernetes 默认容器运行时 | [Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/) |

### 2.4 可观测性 / 日志 / 服务网格 / 其他

| 组件 | 最新版本 | 发布日期 | 关键变化 / 来源 URL |
|---|---|---|---|
| **Prometheus** | 3.16.0（最新）/ 3.13.5（LTS） | 2026-11-04 / 2026-10-21 | 时序数据库与监控核心；LTS 线供生产稳定使用 | [prometheus.io/download](https://prometheus.io/download/) |
| **Alertmanager** | 0.35.0 | 2026-11-09 | 告警路由/分组/静默 | [prometheus.io/download](https://prometheus.io/download/) |
| **node_exporter** | 1.13.0 | 2026-11-19 | 节点指标采集 | [prometheus.io/download](https://prometheus.io/download/) |
| **kube-prometheus-stack** | 88.6.0 | 2026 | Prometheus Operator + Grafana + 告警规则的一体化 Helm Chart | [Artifact Hub](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack/88.6.0) |
| **Grafana Loki** | 3.7.x（3.7.0/3.7.1 2026-03-26，3.7.2 2026-05-14） | 2026 | 日志聚合；**Helm chart 自 2026-03-16 移交 `grafana-community/helm-charts`** | [Loki v3.7 Release Notes](https://grafana.com/docs/loki/latest/release-notes/v3-7/) |
| **Fluent Bit** | 5.1.4 | 2026-10-12 | 轻量日志/指标/追踪采集 Agent | [Fluent Bit v5.1.4](https://fluentbit.io/announcements/v5.1.4/) |
| **Istio** | 1.32（最新） | 2026-11-09 | 最新次版本；1.30 将于 2026-12-16 EOL；Ambient 模式自 1.24（2024-11）GA | [Istio Releases](https://istio.io/latest/news/releases/) · [Istio 1.30 EOL](https://istio.io/latest/news/support/announcing-1.30-eol/) · [CNCF: Ambient GA](https://www.cncf.io/blog/2024/11/07/fast-secure-and-simple-istios-ambient-mode-reaches-general-availability-in-v1-24/) |
| **Argo CD** | 3.5.3 | 2026-09-14 | GitOps 持续交付；v3.5.0 于 2026-08-04；v3.6 计划 2026-12-15 RC | [Argo CD Release Process](https://argo-cd.readthedocs.io/en/stable/developer-guide/release-process-and-cadence/) |
| **Velero** | 1.18.x（1.18.4） | 2026-10-12 | 备份/恢复/迁移（含 CSI 快照、PV 迁移） | [Velero 变更](https://images.minimus.io/images/velero/changelog/latest/versions/1.17.2/digest-history) |
| **Harbor** | 2.16.0 | 2026-11 | 私有镜像仓库（OCI、漏洞扫描、复制、签名） | [Harbor v2.16.0](https://github.com/goharbor/harbor/releases/tag/v2.16.0) |
| **OpenTelemetry Collector** | v0.161.0 / v1.67.0 | 2026-09 | 遥测数据采集/转发 | [opentelemetry-collector v0.161.0](https://newreleases.io/project/github/open-telemetry/opentelemetry-collector/release/v0.161.0) |

## 三、分知识点关键事实

### 1. DevOps 理念与实践体系

- **DORA（DevOps Research and Assessment）**：2025 年报告主题为《State of AI-Assisted Software Development》，基于约 **5,000 名**技术从业者问卷与 100+ 小时访谈。核心结论：**AI 是「放大器」而非「魔法」**——工程文化、平台能力、工作流、内部知识体系强时 AI 加速交付，反之放大问题；约 **90%** 开发者已在日常工作中以某种形式使用 AI 辅助。经典四项关键指标：**部署频率、变更前置时间（Lead Time）、变更失败率、故障恢复时间（MTTR）**。来源：[Splunk: State of DevOps 2025](https://www.splunk.com/en_us/blog/learn/state-of-devops.html) · [DevOps.com: DORA 2025](https://devops.com/dora-2025-faster-but-are-we-any-better) · [InfoQ（日文，含 2025 DORA 要点）](https://www.infoq.com/jp/news/2026/07/ai-dora-report/)
- **实践体系要点**：CI/CD、基础设施即代码（IaC）、监控与告警、SRE（服务等级目标 SLO/错误预算）、平台工程（Internal Developer Platform）、GitOps（Argo CD / Flux）、云原生（CNCF 技术图谱）。CNCF 为云原生事实标准组织。
- 写作建议：把 DORA 四指标与「平台工程 + AI 放大」作为 2026 年的时代背景，避免停留在传统 CI/CD 老框架。

### 2. 容器与 Docker 基础

- Docker 核心组件：**Docker Engine（daemon）、containerd（镜像/容器运行时）、BuildKit（构建）、Docker CLI、镜像仓库**。Docker Engine 29.x 内嵌 containerd **v2.4.2**。来源：[Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
- 容器本质：基于 **namespace（隔离）+ cgroups（资源限制）+ 联合文件系统（镜像分层）**；现代内核要求 **cgroup v2**（Kubernetes 1.35 已移除 cgroup v1 支持，节点必须启用 cgroup v2）。来源：[K8s v1.35 Sneak Peek（cgroup v1 移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
- Docker Desktop 最新 **4.98.0**；Linux 发行版包如 Debian `docker.io 28.5.2`（不同发行版版本号体系与 Docker 官方 Engine 29 不同，写作时区分「官方 Engine 版本」与「发行版打包版本」）。来源：[Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/) · [Debian docker.io 新闻](https://tracker.debian.org/pkg/docker.io/news/)

### 3. Dockerfile 最佳实践

- 官方最佳实践核心：多阶段构建（multi-stage builds）、使用 `.dockerignore`、最小基础镜像（distroless/alpine）、按层合并减少镜像层、固定基础镜像 tag 避免 `latest`、以非 root 用户运行、用 BuildKit 缓存（`--mount=type=cache`）。来源：[Dockerfile 最佳实践（docs.docker.com）](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- Docker Engine 29.x 默认启用 containerd 镜像存储（containerd image store）与 BuildKit **v0.32.2**；构建产物默认使用 BuildKit。来源：[Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
- 写作提示：2026 年应强调「容器镜像的供应链安全」（签名、SBOM、Trivy 扫描、Harbor），与 Harbor 2.16、Trivy v0.69 等结合。

### 4. 容器镜像与仓库管理

- **OCI（Open Container Initiative）** 规范是镜像/制品的通用标准；Helm 4 亦默认走 OCI registry 工作流，`helm registry login` 现仅接受**域名**。来源：[Helm 3 EOL（Helm 4 变更）](https://v3.helm.sh/blog/helm-v3-end-of-life/)
- 私有仓库代表 **Harbor 2.16.0**：支持 OCI、漏洞扫描（Trivy）、跨仓库复制、内容信任/签名。来源：[Harbor v2.16.0](https://github.com/goharbor/harbor/releases/tag/v2.16.0)
- 镜像管理要点：tag 策略、多阶段精简、镜像签名（cosign）、GC/清理、镜像加速与安全扫描；Docker Desktop 4.98 已内置相关能力。来源：[Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)

### 5. Kubernetes 核心概念与架构

- 控制平面：**kube-apiserver、etcd、kube-controller-manager、kube-scheduler、cloud-controller-manager**；工作节点：**kubelet、kube-proxy、容器运行时（containerd）、CNI**。来源：[Kubernetes 官方文档](https://kubernetes.io/zh-cn/docs/concepts/)
- **版本偏斜策略**：项目维护最近 **3 个次版本分支**；不同组件间存在最大偏斜限制（kube-apiserver/kubelet 等），集群工具可能更严格。来源：[kubernetes.io/releases/version-skew-policy](https://kubernetes.io/releases/version-skew-policy/)
- **1.34 引入 `ListFromCacheSnapshot`**（默认启用）以减轻 etcd 压力、提升稳定性；**1.34 引入外部 ServiceAccount 令牌签名（ExternalJWTSigner）**。来源：[K8s v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **1.37** 增强控制平面韧性：Resilient Watch Cache、Pod 级 checkpoint/restore、manifest-based admission control Beta。来源：[K8s 1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)

### 6. Kubernetes Pod 与工作负载

- 工作负载资源：**Pod、Deployment、StatefulSet、DaemonSet、Job/CronJob**；稳定 API 版本均为 `apps/v1`。Pod 是最小调度单元。
- **Pod 级资源请求/限制**：v1.32 Alpha → **v1.34 Beta**，允许为多容器 Pod 声明总体资源预算，HPA 亦支持 Pod 级规格。来源：[K8s v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **Pod 资源 in-place 更新**：**v1.35 起 GA**（`Resize` 子资源），VPA 的 `InPlaceOrRecreate` 模式可借此在不重启 Pod 的情况下调整资源。来源：[K8s v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/) · [K8s v1.34 Release（Pod 级资源）](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **挂起 Job 可变资源**：v1.35 引入 `MutablePodResourcesForSuspendedJobs`，暂停后可修改资源再恢复，避免删除重建。来源：[K8s v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
- **Pod 证书、节点声明特性**：v1.35 引入，用于工作负载身份与节点能力声明。来源：[K8s v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)

### 7. Kubernetes Service 与网络

- **Service 类型**：ClusterIP / NodePort / LoadBalancer / ExternalName；Endpoints 由 **EndpointSlice** 支撑（**1.33 起 Endpoints API v1 废弃**，应迁移 EndpointSlice）。来源：[Volcengine K8s v1.34 版本说明](https://docs.volcengine.com/docs/vke/vke-for-kubernetes-v1-34?lang=zh)
- **Ingress-NGINX 已于 2026-03 归档退役**；官方网络方向转向 **Gateway API**，核心资源（GatewayClass、Gateway、HTTPRoute、GRPCRoute、TLSRoute、ReferenceGrant）**已 GA**，TCPRoute/UDPRoute 仍为实验性。官方提供 **Ingress2Gateway 1.0** 迁移工具。来源：[K8s Blog: Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/) · [K8s Blog: Ingress-NGINX 退役](https://kubernetes.io/blog/?p=241) · [Ingress vs Gateway API（2026）](https://raw.githubusercontent.com/OneUptime/blog/refs/heads/master/posts/2026-02-20-kubernetes-ingress-vs-gateway-api/README.md)
- **kube-proxy ipvs 模式在 v1.35 被弃用**（deprecation），写作时提示 iptables/ipvs 选型与迁移影响。来源：[K8s v1.35 Sneak Peek](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
- 网络模型要点：ClusterIP/Service DNS、四层与七层负载均衡、CNI 插件、NetworkPolicy、双栈 IPv6。

### 8. Kubernetes 存储与 PV/PVC

- 核心对象：**PV（持久卷）、PVC（持久卷声明）、StorageClass、Volume**；存储插件通过 CSI（Container Storage Interface）实现，支持动态供给。
- **Git-Repo 卷插件自 v1.33 起默认禁用**（需手动开启 `GitRepoVolumeDriver` 特性门控）。来源：[Volcengine K8s v1.34 版本说明](https://docs.volcengine.com/docs/vke/vke-for-kubernetes-v1-34?lang=zh)
- **SELinux 卷标签变更**：未来版本（预计 v1.37 起默认启用 `SELinuxMount` 特性门控）将改变卷标签行为，v1.36 是审计集群并修复/选择退出的合适版本。来源：[K8s Blog: SELinux 卷标签变更](https://v1-36.docs.kubernetes.io/zh-cn/blog/page/4/)
- **备份**：Velero 1.18.x 支持 CSI 快照、PV 备份/迁移。来源：[Velero 1.18.4](https://images.minimus.io/images/velero/changelog/latest/versions/1.17.2/digest-history)
- 写作提示：区分「静态供给 vs 动态供给」「本地卷/网络存储」「CSI 驱动选型」。

### 9. Kubernetes 调度与资源管理

- 调度核心：**kube-scheduler** 按资源请求/限制、亲和/反亲和、污点/容忍、节点选择器等打分；资源对象 `requests`/`limits`、QoS 等级（Guaranteed/Burstable/BestEffort）。
- **工作负载感知调度**：v1.35 引入 Workload API 首批能力，**v1.37 继续演进**（CompositePodGroup 多级编组、全有或全无调度），面向 AI/批处理。来源：[K8s v1.37: Advancing Workload-Aware Scheduling](https://kubernetes.io/zh-cn/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/) · [K8s v1.35 Sneak Peek](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
- **动态资源分配（DRA）**：**v1.37 DRA 扩展资源支持 GA**（设备插件可逐步被 DRA 替代，应用侧仍可用 `example.com/gpu` 这类扩展资源语法），DRA 设备污点/容忍 Stable；KEP 自 v1.34 获批，1.35 Alpha、1.36 Beta、1.37 GA。来源：[K8s v1.37: DRA Updates](https://kubernetes.io/zh-cn/blog/2026/09/03/kubernetes-v1-37-dra-updates/)
- **HPA scale-to-zero**：**v1.37 中 `HPAScaleToZero`（KEP-2021）转 Beta 且默认启用**，`minReplicas: 0` 可作用于 Object/External 指标；KEDA 仍是常用指标适配与 scale-to-zero 路径。来源：[K8s 1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md) · [Cloud Native Kubernetes 变更日志（HPA/VPA/KEDA）](https://raw.githubusercontent.com/mcorbett51090/RavenClaude/refs/heads/main/plugins/cloud-native-kubernetes/CHANGELOG.md)
- **VPA**：`InPlaceOrRecreate` 更新模式在 K8s ≥ 1.35 可配合 in-place resize 减少重启。来源：[Cloud Native Kubernetes 变更日志](https://raw.githubusercontent.com/mcorbett51090/RavenClaude/refs/heads/main/plugins/cloud-native-kubernetes/CHANGELOG.md)
- **节点资源**：cgroup v1 在 v1.35 被移除，节点必须 cgroup v2；v1.35 引入节点声明特性（Node Declared Features）。

### 10. Kubernetes ConfigMap/Secret/Env

- **ConfigMap** 存储非机密配置；**Secret** 存储敏感数据（base64 编码，非加密）；通过 Env、EnvFrom、卷挂载注入 Pod。
- **Secret 加密（静态加密 at rest）**：通过 KMS provider（gRPC）与 etcd 加密实现，云厂商托管集群（如 AKS）提供托管 KMS 集成。来源：[K8s: Using a KMS provider](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/kms-provider/) · [Azure AKS: KMS 数据静态加密概念](https://learn.microsoft.com/en-us/Azure/AKS/kms-data-encryption-concepts)
- **外部 ServiceAccount 令牌签名（ExternalJWTSigner）**：v1.34 引入，签名可移出 kube-apiserver 进程外。来源：[K8s v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **kuberc**：v1.33 Alpha（`KUBECTL_KUBERC`）→ **v1.34 Beta 默认启用**，可配置 kubectl 默认选项与别名，**不含**集群凭据（v1.35 又新增凭据插件策略配置）。来源：[K8s v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/) · [K8s v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
- 写作提示：Secret 应配合外部密钥管理（KMS/Vault）、RBAC 最小权限、避免明文写入清单。

### 11. Kubernetes 安全（RBAC/网络策略）

- **RBAC**：Role/RoleBinding（命名空间内）与 ClusterRole/ClusterRoleBinding（集群级），基于 allow/deny 模型；官方建议最小权限、避免宽泛 `cluster-admin`。来源：[Kubernetes 官方文档：RBAC 鉴权](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/)
- **NetworkPolicy**：基于标签的 L3/L4 流量隔离，需集群 CNI 支持；与服务网格（Istio）互补。来源：[Kubernetes 官方文档：Network Policies](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/)
- **v1.33 移除 ValidatingAdmissionPolicy v1alpha1**（需用稳定版）；**v1.37 manifest-based admission control 转 Beta**，支持从磁盘清单加载 admission webhook 与 CEL 策略。来源：[Volcengine K8s v1.34 版本说明](https://docs.volcengine.com/docs/vke/vke-for-kubernetes-v1-34?lang=zh) · [K8s 1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
- **节点安全**：v1.37 `KubeletInUserNamespace`（rootless 模式）转 Beta，kubelet/CRI/CNI/kube-proxy 均可非 root 运行。来源：[K8s v1.37: Rootless Beta](https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/)
- 安全清单：Secret 静态加密、镜像签名与拉取策略、Pod 安全标准（PSA）、准入控制、审计日志、漏洞扫描。

### 12. Helm 包管理

- **Helm 4 是当前主版本**：2025-11-12 发布 v4.0.0；**Helm 3 最后功能版 2026-09-09，安全补丁至 2027-02-10**，之后彻底停止。写作必须提示迁移。来源：[Helm 3 End of Life](https://v3.helm.sh/blog/helm-v3-end-of-life/) · [Helm 4 Released](https://github.com/helm/helm-www/blob/main/blog/2025-11-17-helm-4-released/index.md)
- **Helm 4 关键新特性**：WebAssembly 插件运行时（可选）、post-renderer 即插件、**server-side apply 为新 release 默认**（升级时沿用原 apply 方式，可用 `--server-side=false` 覆盖）、kstatus 状态追踪、多文档 values、稳定 SDK API、更快的依赖解析与基于内容的缓存。来源：[Helm 3 EOL（含 Helm 4 特性）](https://v3.helm.sh/blog/helm-v3-end-of-life/)
- **破坏性变更**：`--atomic`→`--rollback-on-failure`、`--force`→`--force-replace`（旧旗标仍可用但告警）；`helm registry login` 仅接受域名。来源：[Helm 3 EOL](https://v3.helm.sh/blog/helm-v3-end-of-life/)
- **迁移建议**：先在非生产环境用 Helm 4 部署现有 chart；更新 CI/CD 脚本中的重命名旗标；迁移 post-renderer；验证 OCI registry 登录；Helm 4 可管理既有 Helm 3 release，无需重建。来源：[Helm 3 EOL](https://v3.helm.sh/blog/helm-v3-end-of-life/)

### 13. Kubernetes 监控（Prometheus）

- **Prometheus 3.16.0（2026-11-04）最新，LTS 线 3.13.5（2026-10-21）**；Alertmanager 0.35.0（2026-11-09）；node_exporter 1.13.0（2026-11-19）。来源：[prometheus.io/download](https://prometheus.io/download/)
- **kube-prometheus-stack 88.6.0**：Prometheus Operator + Grafana + Alertmanager + 告警规则的一站式 Helm Chart；Prometheus Operator 0.30+ 提供 PrometheusRules 准入 Webhook。来源：[Artifact Hub: kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack/88.6.0)
- 关键概念：ServiceMonitor/PodMonitor 服务发现、PromQL、Relabeling、抓取间隔、长期存储（远端写入）、告警分级。
- 写作提示：Prometheus 是 CNCF 毕业项目，是 K8s 监控事实标准；建议与 Grafana、Alertmanager、OTel 结合讲现代可观测性（指标+日志+追踪）。

### 14. Kubernetes 日志（EFK/Loki）

- **Loki 3.7.x** 为当前主流（3.7.0/3.7.1 于 2026-03-26，3.7.2 于 2026-05-14）；**其 Helm chart 自 2026-03-16 移交 `grafana-community/helm-charts`**，Grafana Labs 继续维护企业版 GEL chart。来源：[Loki v3.7 Release Notes](https://grafana.com/docs/loki/latest/release-notes/v3-7/)
- **Fluent Bit 5.1.4（2026-10-12）**：轻量采集 Agent，支持日志/指标/追踪。来源：[Fluent Bit v5.1.4](https://fluentbit.io/announcements/v5.1.4/)
- **EFK（Elasticsearch + Fluentd/Fluent Bit + Kibana）** 仍是经典组合，但 Elastic 许可证与资源开销较大；Loki 以「索引标签、日志低成本存储」为卖点，常作为 EFK 的替代/补充。
- **OpenTelemetry Collector v0.161.0 / v1.67.0（2026-09）** 用于统一采集与转发遥测数据。来源：[opentelemetry-collector v0.161.0](https://newreleases.io/project/github/open-telemetry/opentelemetry-collector/release/v0.161.0)
- 写作提示：讲清「采集（Fluent Bit/Fluentd）→ 聚合（Loki/Elasticsearch）→ 可视化（Grafana/Kibana）」链路与各自适用场景。

### 15. Kubernetes 部署策略（滚动/蓝绿/金丝雀）

- **滚动更新（Rolling Update）**：Deployment 默认策略，通过 `maxSurge` / `maxUnavailable` 控制更新节奏与可用性。
- **蓝绿（Blue/Green）**：两个 Deployment + Service 切换，靠 Service 选择器或入口层切换流量；可结合 Argo CD/入口实现。
- **金丝雀（Canary）**：按权重/流量比例逐步放量，常用 Ingress/Gateway API 权重或服务网格（Istio）实现精细流量切分。
- **GitOps 持续部署**：Argo CD 3.5.x（v3.5.0 2026-08-04，3.5.3 2026-09-14；v3.6 计划 2026-12-15 RC）为当前主流，支持多集群、同步策略、渐进式发布。来源：[Argo CD Release Process](https://argo-cd.readthedocs.io/en/stable/developer-guide/release-process-and-cadence/)
- **流量管理新事实**：Gateway API 核心资源 GA，成为 Ingress 后继标准，利于蓝绿/金丝雀的标准化权重路由。来源：[K8s Blog: Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
- **HPA 联动**：v1.37 的 scale-to-zero 可与部署策略结合做弹性，但需注意冷启动。

### 16. Kubernetes 故障排查与调试

- **kubectl 排障**：`get/describe/logs/exec/events`、`kubectl debug`、`kubectl top`、`kubectl get --raw`；`kubectl` 偏好可用 `.kuberc`（v1.34 起 Beta 默认启用）配置。来源：[K8s v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **z-pages 调试端点**：v1.32 Alpha 引入，**v1.35 提供结构化、机器可解析的响应**，便于自动化排障。来源：[K8s Blog: v1.35 版本化 z-pages API](https://kubernetes.io/zh-cn/blog/2025/12/31/kubernetes-1-35-z-pages/)
- **Pod checkpoint/restore**：v1.37 支持 Pod 级 checkpoint/restore（Beta），对有状态工作负载调试与快速恢复有意义。来源：[K8s 1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
- **排查体系**：事件与状态、Pod 生命周期、日志聚合（Loki/EFK）、指标（Prometheus）、网络（kube-proxy/NetworkPolicy）、准入控制与审计；Ingress-NGINX 退役后，网络排障应结合 Gateway API。
- 写作提示：按「现象 → 分层定位（工作负载/网络/存储/控制平面）→ 证据 → 修复」组织，给出 kubectl 命令清单。

### 17. 云原生与服务网格（Istio）

- **Istio 最新次版本 1.32（2026-11-09）**；**1.30 将于 2026-12-16 EOL**（N+2 规则：1.32 发布后 6 周终止对 1.30 的支持）。来源：[Istio Releases](https://istio.io/latest/news/releases/) · [Istio 1.30 EOL](https://istio.io/latest/news/support/announcing-1.30-eol/)
- **Ambient 模式自 Istio 1.24（2024-11）起 GA**（ztunnel、waypoint、API 均 Stable），官方推进 sidecar → ambient 数据面迁移。来源：[CNCF: Ambient GA](https://www.cncf.io/blog/2024/11/07/fast-secure-and-simple-istios-ambient-mode-reaches-general-availability-in-v1-24/) · [Istio Roadmap 2025-2026](https://preliminary.istio.io/latest/blog/2025/roadmap/)
- **Gateway API 与 Telemetry API** 在 Istio 1.22 晋升 Stable；服务网格向「标准 API + 无 sidecar」演进。
- 云原生要点：CNCF 生态（Kubernetes、Prometheus、Istio、Envoy、OpenTelemetry）、容器化、声明式 API、可观测性、弹性与自愈。

### 18. Kubernetes 生产运维与备份

- **备份/恢复**：**Velero 1.18.x（1.18.4，2026-10-12）** 支持备份/恢复/迁移，含 CSI 快照、PV 迁移、跨集群迁移。来源：[Velero 1.18.4](https://images.minimus.io/images/velero/changelog/latest/versions/1.17.2/digest-history)
- **etcd 运维**：etcd 是控制平面状态存储，需定期快照、压缩、监控；v1.34 `ListFromCacheSnapshot` 默认启用，降低对 etcd 的直接访问压力。来源：[K8s v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **升级与生命周期管理**：遵循版本偏斜策略，滚动升级控制平面/工作节点；活跃分支 1.37/1.36/1.35，1.34 已 EOL。来源：[kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/) · [kubernetes.io/releases/version-skew-policy](https://kubernetes.io/releases/version-skew-policy/)
- **生产要点**：多副本控制平面、etcd 备份与演练、镜像与依赖安全、RBAC 最小权限、监控/告警/日志、SLO 与错误预算、变更管理、容量规划、灾难恢复（RPO/RTO）。
- **备份生态**：除 Velero 外，可结合 CSI 快照、云厂商快照、etcd 快照、GitOps（Argo CD）实现配置与状态分层备份。

## 四、写作要点与风险提示

**写作要点**

1. **以 v1.37 为「当前默认视角」**：所有示例、命令与 API 建议尽量对齐 v1.37 官方文档；旧版本差异用表格或迁移小贴士标注。
2. **把「弃用/移除」作为 18 篇文档的统一暗线**：Endpoints v1、Git-Repo 卷、kube-proxy ipvs、cgroup v1、ValidatingAdmissionPolicy v1alpha1、Helm 3、Ingress-NGINX——每篇涉及相关概念时都要提示「已废弃/已退役/需迁移」。
3. **版本号务必标注「发布日期 + 是否 LTS/最新」**：如 Prometheus 需区分 3.16.0（最新）与 3.13.x（LTS）；Docker 需区分官方 Engine 29.x 与发行版打包版本。
4. **突出 2025–2026 的结构性变化**：Helm 3→4、Ingress-NGINX→Gateway API、sidecar→Istio Ambient、DRA 与 AI 工作负载调度、AI 对 DevOps 的「放大器」效应。
5. **每篇附「权威来源」区**：优先官方文档/官方博客/GitHub Release，其次 CNCF，避免使用过时博客。

**风险提示**

- **事实时效风险**：本文截至 2026-11-19 检索，版本与 EOL 日期可能随官方调整变化；写作前应回源核对，尤其 Helm 3 EOL（2027-02-10）、Istio 1.30 EOL（2026-12-16）等临近节点。
- **版本混淆风险**：Kubernetes 次版本支持期与各托管集群（EKS/AKS/GKE）策略不同，托管集群的 EOL 可能更晚或更严，不要混用上游与云厂商口径。
- **Docker 版本口径风险**：官方 Docker Engine（29.x）与发行版包（如 Debian `docker.io 28.x`）版本号体系不同，勿直接对比。
- **Helm 4 兼容性风险**：官方称 Helm 4 兼容多数 Helm 3 chart/release，但破坏性旗标重命名与 post-renderer 插件化仍可能影响既有流水线，需按官方迁移清单验证。
- **Ingress-NGINX 退役风险**：大量存量集群仍运行该控制器，迁移到 Gateway API 需评估默认行为差异（官方博客已提示多个易被忽略的默认行为）。
- **来源可信度**：部分搜索结果来自聚合/二手站点（如 Artifact Hub、发行版镜像站、博客），引用时优先回链官方页面；二手信息仅用于佐证版本号。

**主要官方来源汇总**

- Kubernetes 官方：https://kubernetes.io/releases/patch-releases/ · https://kubernetes.io/releases/version-skew-policy/ · https://kubernetes.io/docs/home/supported-doc-versions/ · https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/ · https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/ · https://kubernetes.io/blog/2026/03/30/kubernetes-v1-36-sneak-peek/
- Helm：https://v3.helm.sh/blog/helm-v3-end-of-life/ · https://github.com/helm/helm-www/blob/main/blog/2025-11-17-helm-4-released/index.md
- Docker：https://docs.docker.com/engine/release-notes/29/ · https://docs.docker.com/desktop/release-notes/
- Prometheus：https://prometheus.io/download/
- Istio：https://istio.io/latest/news/releases/ · https://istio.io/latest/news/support/announcing-1.30-eol/
- Loki / Fluent Bit：https://grafana.com/docs/loki/latest/release-notes/v3-7/ · https://fluentbit.io/announcements/v5.1.4/
- Argo CD / Velero / Harbor：https://argo-cd.readthedocs.io/en/stable/developer-guide/release-process-and-cadence/ · https://github.com/goharbor/harbor/releases/tag/v2.16.0 · Velero 变更页
