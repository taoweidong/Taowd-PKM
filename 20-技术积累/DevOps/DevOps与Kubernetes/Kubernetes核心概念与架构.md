---
title: Kubernetes 核心概念与架构
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 容器编排
  - 架构
aliases:
  - K8s核心概念
  - Kubernetes架构
source:
  - 网络资料整理
---

# Kubernetes 核心概念与架构

> [!摘要] 摘要
> 本文聚焦 Kubernetes 的**控制平面/工作节点架构、核心对象模型与声明式对账机制**，是进入云原生体系的第一块基石。内容以截至 2026-11 的 Kubernetes v1.37 官方口径为准，覆盖控制平面组件、节点组件、Pod 与工作负载、Service 与网络、存储与调度等核心机制，并给出可直接运行的 kubectl 实践步骤与生产避坑清单。适合已完成 Docker 基础、准备系统掌握集群编排的后端/运维/SRE 工程师。

## 一、最新动态（截至 2026-11）

- **Kubernetes 最新稳定版 v1.37（代号 Garhwal）**，于 **2026-08-26** 发布，截至 2026-11 已发布补丁 **1.37.2**，官方文档站点默认版本即为 v1.37。v1.37 是近年来与 AI/批量工作负载最相关的版本：**动态资源分配（DRA）扩展资源支持进入 GA**、**HPA scale-to-zero 转 Beta（默认启用）**、**Pod 级 checkpoint/restore 转 Beta**、**KubeletInUserNamespace（rootless）转 Beta**、工作负载感知调度继续演进（CompositePodGroup 多级编组、全有或全无调度）。来源：[Kubernetes v1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)、[kubernetes.io 补丁发布页](https://kubernetes.io/releases/patch-releases/)
- **支持策略**：项目维护最近 **3 个次版本分支**，支持期约 **14 个月**（12 个月标准期 + 2 个月维护期，补丁每月一次、目标每月 28 日）。截至 2026-11 活跃分支为 **1.37 / 1.36 / 1.35**；**1.34 已于 2026-10-27 EOL**（最后补丁 1.34.13），**1.33 于 2026-06-28 EOL**（最后补丁 1.33.13）。来源：[kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/)、[kubernetes.io/docs/home/supported-doc-versions](https://kubernetes.io/docs/home/supported-doc-versions/)
- **控制平面增强**：v1.34 引入 `ListFromCacheSnapshot`（默认启用，降低 etcd 直接访问压力）与**外部 ServiceAccount 令牌签名（ExternalJWTSigner）**（签名可移出 kube-apiserver 进程）；v1.37 继续增强控制平面韧性（Resilient Watch Cache、manifest-based admission control Beta）。
- **网络与运行时**：**Ingress-NGINX 已于 2026-03 归档/退役**，官方转向 **Gateway API**（GatewayClass / Gateway / HTTPRoute 等核心资源已 GA）；**kube-proxy ipvs 模式在 v1.35 被弃用**；**v1.35 起移除 cgroup v1 支持**，节点必须启用 cgroup v2；**v1.33 起 Endpoints API v1 废弃**，应改用 EndpointSlice。
- **周边生态**：Helm 4 已正式发布（v4.0.0 于 2025-11-12），**Helm 3 最后功能版为 2026-09-09、安全补丁延长至 2027-02-10**；Docker Engine 29.x 内嵌 containerd 2.x。系统脉络见 [[DevOps与Kubernetes-从入门到精通]]。

## 二、基础概念

**Kubernetes 是什么**：一个开源的容器编排系统，核心是把「声明式的期望状态」转化为「集群里真实运行的状态」。用户提交 YAML 清单，控制器持续对账，实际状态最终收敛到声明状态——这也是它与脚本式运维最根本的区别。

**集群的两半：控制平面与工作节点**

| 分层 | 组件 | 职责 |
| --- | --- | --- |
| 控制平面 | kube-apiserver | 唯一入口与聚合层，所有读写都经它，负责认证、鉴权与准入 |
| 控制平面 | etcd | 分布式键值存储，持久化集群全部状态 |
| 控制平面 | kube-controller-manager | 运行各类控制器（Deployment、Node 等）执行对账 |
| 控制平面 | kube-scheduler | 为新 Pod 选择合适节点 |
| 控制平面 | cloud-controller-manager | 对接云厂商资源（负载均衡、路由等） |
| 工作节点 | kubelet | 节点代理，确保容器按 PodSpec 运行并汇报节点状态 |
| 工作节点 | kube-proxy | 维护 Service 的负载均衡规则 |
| 工作节点 | 容器运行时 + CNI | containerd 等 CRI 运行时负责跑容器，CNI 负责网络 |

**核心对象模型**

| 对象 | 职责 | 一句话记忆 |
| --- | --- | --- |
| Pod | 最小调度单元，一个或多个共享网络/存储的容器 | 调度与网络的最小粒度 |
| Deployment | 无状态应用的副本数与滚动更新 | 管「无状态、要扩缩」 |
| StatefulSet | 有状态应用的顺序与稳定标识 | 管「有状态、要顺序」 |
| DaemonSet | 每个节点运行一份 | 管「每节点一个」 |
| Job / CronJob | 批处理与定时任务 | 管「跑完即止」 |
| Service / EndpointSlice | 稳定访问与四层负载均衡 | 管「找得到、分得匀」 |
| ConfigMap / Secret | 配置与密钥 | 管「配置与凭据」 |

**声明式工作流**：`kubectl apply -f` 提交期望状态 → apiserver 校验并写入 etcd → 控制器通过 watch/informer 感知变化 → 驱动实际状态收敛。理解这条链路，是排查绝大多数集群问题的钥匙。

> [!warning] 易混淆点
> 集群中真正运行容器的是满足 CRI 的运行时（containerd 等），**不是 Docker**。Kubernetes 已移除 dockershim，`docker` 命令只是开发者本地工具，不要与集群运行时混为一谈。

## 三、核心机制

**控制平面：apiserver 是唯一入口**。所有组件（kubelet、控制器、kubectl）都不直接操作 etcd，而是统一经 apiserver 完成读写。这样认证、鉴权、准入控制、审计就被收敛到一个点，`etcd` 则专注保存全部集群状态，需要定期快照、压缩与监控。

**声明式对账（reconcile loop）**：控制器持续对比「实际状态」与「etcd 中的期望状态」，发现不一致就采取行动，直到收敛。因此"状态不对"的根因，绝大多数是控制器未完成对账，排查时应先看 `kubectl describe` 的事件。

**Pod 生命周期与探针**：容器具备 Init、Startup、Readiness、Liveness 以及 PostStart/PreStop 钩子。`readinessProbe` 决定「是否接流量」，`livenessProbe` 决定「是否重启」，**二者不可混用**；再配合 `terminationGracePeriodSeconds` 与 `preStop` 钩子实现优雅终止，保证发布与缩容不丢请求。

**资源治理与调度**：`requests` 决定调度依据，`limits` 决定上限，二者共同决定 QoS 等级（Guaranteed / Burstable / BestEffort）。kube-scheduler 按资源请求、亲和/反亲和、污点/容忍、节点选择器等打分选节点。v1.37 的**工作负载感知调度**与 **DRA 扩展资源支持 GA**，面向 AI/批处理的整组调度与硬件管理。

**网络模型**：Service（ClusterIP / NodePort / LoadBalancer / ExternalName）提供稳定访问与四层负载均衡，由 EndpointSlice 支撑、kube-proxy 实现；Gateway API 承接南北向七层入口；NetworkPolicy 做东西向隔离。

**存储模型**：PV（持久卷）/ PVC（持久卷声明）/ StorageClass 配合 **CSI（容器存储接口）** 实现动态供给，无需手工创建存储。

## 四、实践步骤（含代码/命令示例）

**1. 准备单节点集群（学习/开发环境）**

```bash
# 用 Kind 拉起本地单节点集群，无需虚拟机
kind create cluster --name k8s-basic

kubectl get nodes        # 状态为 Ready 即集群可用
kubectl get pods -A      # 观察系统组件是否正常调度
```

**2. 声明一个 Deployment（`deployment.yaml`）**

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
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { cpu: 500m, memory: 256Mi }
          readinessProbe:
            httpGet: { path: /, port: 80 }
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet: { path: /, port: 80 }
            initialDelaySeconds: 15
            periodSeconds: 20
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]
      terminationGracePeriodSeconds: 30
```

**3. 暴露稳定访问（`service.yaml`）**

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

**4. 提交、观察与回滚**

```bash
# 声明式提交
kubectl apply -f deployment.yaml -f service.yaml

# 观察滚动更新
kubectl get pods -l app=web-demo -o wide
kubectl rollout status deployment/web-demo
kubectl describe deployment/web-demo          # 重点看 Events

# 发布历史与回滚（K8s 内置能力）
kubectl rollout history deployment/web-demo
kubectl rollout undo deployment/web-demo --to-revision=1

# 临时暴露到本机端口验证，仅开发环境使用
kubectl port-forward svc/web-demo 8080:80
```

**5. 配置与密钥注入**

```bash
kubectl create configmap app-config --from-literal=LOG_LEVEL=info
kubectl create secret generic app-secret --from-literal=DB_PASSWORD=secret123

# 确认清单中的注入方式（env / envFrom / 卷挂载）
kubectl get pods -l app=web-demo -o yaml | grep -A3 "configMapKeyRef\|envFrom"
```

> [!warning] Secret 不是加密
> Secret 仅做 Base64 编码，**不是加密**。生产环境的数据库口令、云厂商 AK/SK 必须配合 KMS/Vault 等外部密钥系统（如 External Secrets Operator）与 etcd 静态加密，切勿把 Secret 当作加密存储使用。

**6. 排障分层顺序**：先看事件（`kubectl describe`）→ 再看日志（`kubectl logs <pod> --previous`）→ 再看状态与资源（`kubectl get -o wide`、`kubectl top`）→ 最后怀疑调度与准入链路。

## 五、最佳实践与常见坑

**资源与 QoS**

- 务必设置 `requests`/`limits`，否则 Pod 处于 BestEffort，既无法准确调度也容易被驱逐。
- 需要高保障的 Pod，让 CPU 与内存的 requests 等于 limits，落到 **Guaranteed** 等级。

**清单与配置**

- 镜像 tag 生产环境使用**摘要（digest）**而非可变 tag，避免同 tag 覆盖导致「改了代码却没换镜像」。
- ConfigMap 存非敏感配置、Secret 存敏感数据；Secret 不要明文写入清单，交由外部密钥系统下发。

**安全**

- RBAC 最小权限，避免宽泛的 `cluster-admin`；用 Pod Security Standards 与准入策略（Kyverno / OPA / MutatingAdmissionPolicies）治理可部署内容。
- 镜像供应链做漏洞扫描、签名（cosign）与拉取策略校验，并启用 Secret 静态加密。

**升级前先清弃用项（2026-11 重点）**

| 弃用/移除项 | 涉及版本 | 迁移动作 |
| --- | --- | --- |
| Endpoints API v1 | v1.33 废弃 | 改用 EndpointSlice |
| Git-Repo 卷插件 | v1.33 起默认禁用 | 改用其他卷源 |
| cgroup v1 | v1.35 移除 | 节点启用 cgroup v2 |
| kube-proxy ipvs | v1.35 弃用 | 评估 iptables / nftables |
| ValidatingAdmissionPolicy v1alpha1 | v1.33 移除 | 改用稳定版 |
| Ingress-NGINX | 2026-03 退役 | 迁移至 Gateway API（可用 Ingress2Gateway 1.0） |
| Helm 3 | 最后功能版 2026-09-09 | 迁移 Helm 4（`--atomic`→`--rollback-on-failure`、`--force`→`--force-replace`） |

**版本偏差硬约束**：kubelet/kube-proxy 不得比 kube-apiserver 新、最多旧 3 个次版本；controller-manager / scheduler 须与 apiserver 同版或旧 1 个；kubectl 与 apiserver 相差 1 个次版本即可（可新可旧）。**升级顺序**：apiserver → 控制面组件 → kubelet/kube-proxy。

> [!tip] 命令速记
> 日常高频：`kubectl get / describe / logs / exec / apply -f`；排障看 `Events` 与 `--previous` 日志；发布回滚用 `rollout history` + `rollout undo`。

## 六、核心要点速查

1. **控制平面**：kube-apiserver（唯一入口）、etcd（状态存储）、kube-controller-manager（对账）、kube-scheduler（选节点）、cloud-controller-manager（云资源）。
2. **工作节点**：kubelet、kube-proxy、容器运行时（containerd）、CNI。
3. **Pod 是最小调度单元**；Deployment / StatefulSet / DaemonSet / Job 是不同负载形态的控制器抽象。
4. **声明式对账**：控制器持续把实际状态收敛到 YAML 声明的期望状态，这是 Kubernetes 的核心机制。
5. **Service / EndpointSlice / kube-proxy** 提供稳定访问与四层负载均衡；Gateway API 处理南北向入口；NetworkPolicy 做东西向隔离。
6. **ConfigMap 存配置、Secret 存敏感数据**，Secret 仅 Base64 编码非加密，生产需外部密钥系统。
7. **requests 决定调度、limits 决定上限**，二者共同决定 QoS（Guaranteed / Burstable / BestEffort）。
8. **截至 2026-11 主线为 v1.37（Garhwal，2026-08-26 发布）**，活跃分支 1.37 / 1.36 / 1.35，1.34 已 EOL。
9. **读多用 kubectl**：`get` 看状态、`describe` 看事件、`logs` 看日志、`rollout` 做发布与回滚。

## 七、学习资源

1. [Kubernetes 官方文档：概念（Concepts）](https://kubernetes.io/zh-cn/docs/concepts/)
2. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
3. [kubernetes.io：补丁发布与支持策略（Patch Releases）](https://kubernetes.io/releases/patch-releases/)
4. [kubernetes.io：版本偏差策略（Version Skew Policy）](https://kubernetes.io/releases/version-skew-policy/)
5. [kubernetes.io：受支持的文档版本](https://kubernetes.io/docs/home/supported-doc-versions/)
6. [Kubernetes 官方文档：RBAC 鉴权](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/)
7. [Kubernetes 官方文档：Network Policies](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/)
8. [Kubernetes 官方博客：v1.37 动态资源分配（DRA）更新](https://kubernetes.io/zh-cn/blog/2026/09/03/kubernetes-v1-37-dra-updates/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]
- [[Kubernetes部署实践]]
- [[Prometheus监控入门]]

## 九、变更记录

- 2026-11-19：首次创建。
