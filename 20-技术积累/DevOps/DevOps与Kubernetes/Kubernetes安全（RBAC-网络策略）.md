---
title: Kubernetes安全（RBAC-网络策略）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 安全
  - RBAC
  - 网络策略
aliases:
  - K8s安全
  - RBAC与NetworkPolicy
source:
  - 网络资料整理
---

# Kubernetes安全（RBAC-网络策略）

> [!摘要] 摘要
> 本文聚焦 Kubernetes 安全体系中最常落地的两块：**基于 RBAC 的访问控制**与**基于 NetworkPolicy 的网络隔离**。从概念模型与授权/网络机制讲起，给出可直接运行的 `Role`/`RoleBinding`/`ClusterRole`/`ClusterRoleBinding` 与 `NetworkPolicy` 清单示例，并梳理截至 2026-11 的权威版本动态（kubelet 细粒度授权、rootless、manifest 式准入控制等）、最佳实践与常见坑。它是 [[DevOps与Kubernetes-从入门到精通]] 中「安全」分支的落地展开，适合运维、SRE 与后端工程师在生产集群中直接参照实施。

## 一、最新动态（截至 2026-11）

- **Kubernetes v1.37（Garhwal，2026-08-26 发布）**为最新稳定版，截至 2026-11 已发布补丁 **1.37.2**，EOL 为 2027-10-28；官方文档默认版本即 v1.37。项目当前维护 **1.37 / 1.36 / 1.35** 三个次版本分支，1.34 已于 2026-10-27 EOL，1.33 于 2026-06-28 EOL。来源：[kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/)

- 与本知识点直接相关的安全与网络动态：
  - **v1.37 `KubeletInUserNamespace`（rootless 模式）转 Beta**：kubelet、CRI、CNI、kube-proxy 均可在非 root 用户命名空间中运行，显著缩小节点被攻破后的横向影响面。来源：[K8s v1.37: Rootless Beta](https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/)
  - **v1.37 manifest-based admission control 转 Beta**：支持从磁盘清单加载 admission webhook 与 CEL 策略，便于把准入策略纳入 GitOps 声明式管理。来源：[K8s 1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
  - **v1.36（2026-04-22）kubelet 细粒度 API 授权（KEP-2862）GA**：可对 kubelet 的 `/run`、`/exec`、`/attach` 等子资源做更精细授权，取代过去粗粒度的节点级权限，是 RBAC 授权粒度的关键升级。来源：[K8s v1.36 Release](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
  - **v1.36 用户命名空间（KEP-127）GA**，配合 Pod Security Standards 强化容器隔离；**ConstrainedImpersonation 转 Beta**，限制通过 `impersonate` 提权式伪装，收紧 RBAC 身份冒充路径。来源：[K8s v1.36 Release](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
  - **v1.35 起 kube-proxy ipvs 模式被弃用**，网络数据面向 iptables/nftables 收敛，升级前需评估迁移影响。来源：[K8s v1.35 Sneak Peek](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
  - **v1.33 已移除 `ValidatingAdmissionPolicy v1alpha1`**，声明验证策略须使用稳定版 `v1`。来源：[Volcengine K8s v1.34 版本说明](https://docs.volcengine.com/docs/vke/vke-for-kubernetes-v1-34?lang=zh)

- 网络入口方向：**Ingress-NGINX 已于 2026-03 归档退役**，官方转向 **Gateway API**（核心资源已 GA）。它与 NetworkPolicy 同属网络治理，做隔离方案设计时建议一并规划。来源：[K8s Blog: Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)

## 二、基础概念

**RBAC（基于角色的访问控制）**：Kubernetes 的授权机制，采用 **allow/deny 模型**，通过「角色（Role）+ 绑定（RoleBinding）」把权限授予主体（User、Group、ServiceAccount）。它回答的问题是「**谁能对哪些资源做什么操作**」。官方建议最小权限、避免滥用宽泛的 `cluster-admin`。来源：[Kubernetes 官方文档：RBAC 鉴权](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/)

- **Role / RoleBinding**：作用域在**命名空间内**，用于限定某一 namespace 的资源。
- **ClusterRole / ClusterRoleBinding**：作用域在**集群级**，用于集群范围资源（如 `nodes`、`persistentvolumes`、`namespaces`）。
- **RoleBinding 也可引用 ClusterRole**：把集群级角色**收敛**到某个命名空间内使用，这是实践中最常用、也最容易写错的组合。

**NetworkPolicy**：基于**标签**的 L3/L4 流量隔离机制，通过 `podSelector`、`namespaceSelector`、`ipBlock` 定义 ingress/egress 规则，回答「**Pod 之间、Pod 与外部之间允许哪些网络流量**」。它**需要集群 CNI 支持**（如 Calico、Cilium 等），且**不提供 L7 治理**，与服务网格（Istio 等）互补。来源：[Kubernetes 官方文档：Network Policies](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/)

**相关概念**：ServiceAccount 是 Pod 的身份载体，RBAC 中常以 `ServiceAccount` 作为主体授予权限；Pod Security Standards（PSS）/Pod Security Admission 负责容器运行级安全（Privileged、HostNetwork 等）；准入控制（MutatingAdmissionPolicy、ValidatingAdmissionPolicy、Kyverno/OPA）负责在请求落库前做策略校验；审计日志记录 apiserver 的访问行为。

## 三、核心机制

**RBAC 授权链路**：所有经 `kube-apiserver` 的请求，在认证（Authentication，确认「你是谁」）之后进入授权（Authorization，判断「你能做什么」）。RBAC 的核心是 **Role → RoleBinding → Subject** 的三元组：`Role` 定义一组规则（`rules`，含 `apiGroups`、`resources`、`verbs`），`RoleBinding` 把该规则绑定到主体。`verbs` 常见取值：`get`、`list`、`watch`、`create`、`update`、`patch`、`delete`、`exec`、`impersonate` 等。

**ClusterRole 的两种用法**：一是经 `ClusterRoleBinding` 授予集群级权限（强权限，慎用）；二是经命名空间内的 `RoleBinding` 引用，从而把集群级角色**降域**使用（如把 `view` 这个 ClusterRole 只绑定到某个 namespace 的普通用户）。角色聚合（`aggregateTo`）可将多个 ClusterRole 合并，便于复用内置角色。

**NetworkPolicy 的匹配逻辑**：每条规则由选择器与规则项组成。`podSelector` 匹配目标 Pod 标签（空选择器表示该命名空间全部 Pod）；`namespaceSelector` 匹配目标 Pod 所在命名空间的标签；`ipBlock` 限定来源/目标 IP 段（含 CIDR 与排除项）。**没有匹配任何策略时，默认放行全部流量**；一旦某个 Pod 被任意 NetworkPolicy 的 `podSelector` 选中，则其**未被规则明确允许的出入站流量会被拒绝**。这也是「default-deny」策略的实现方式。

**NetworkPolicy 的边界**：它只约束 Pod 的网络流量，**不覆盖节点自身流量**（如 kubelet 与 Pod 的通信、节点到 apiserver 的访问）；对 DNS 的访问也需在 egress 中显式放行，否则可能因无法解析域名导致业务异常。

## 四、实践步骤（含代码/命令示例）

**1. 创建命名空间级 Role 与 RoleBinding**（授予对某个 namespace 内 Deployment 的只读权限）：

```yaml
apiVersion: v1
kind: Role
metadata:
  name: deploy-viewer
  namespace: team-a
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: deploy-viewer-binding
  namespace: team-a
subjects:
  - kind: User
    name: zhangsan
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: deploy-viewer
  apiGroup: rbac.authorization.k8s.io
```

**2. 用 ClusterRole + 命名空间 RoleBinding 做「降域」授权**（把集群级只读角色收敛到单个 namespace）：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-only-in-team-a
  namespace: team-a
subjects:
  - kind: ServiceAccount
    name: ci-bot
    namespace: team-a
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

**3. 验证与排查授权**：

```bash
# 以某个用户身份，检查能否执行某操作
kubectl auth can-i list deployments --as=zhangsan -n team-a

# 查看某命名空间的绑定关系，定位权限来源
kubectl get rolebinding,clusterrolebinding -A | grep team-a

# 列出用户/服务账号在集群内的所有权限（排查越权或权限缺失）
kubectl auth reconcile
kubectl get role,rolebinding -n team-a -o wide
```

**4. 创建 NetworkPolicy，默认拒绝并仅放行 80 端口**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-default-deny
  namespace: team-a
spec:
  podSelector: {}            # 选中该 namespace 全部 Pod
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector: {}     # 仅允许同 namespace 内 Pod 访问
      ports:
        - protocol: TCP
          port: 80
  egress:
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns   # 放行 DNS，避免解析失败
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

**5. 验证网络策略生效**（需集群 CNI 支持，如 Calico/Cilium）：

```bash
# 查看策略
kubectl get networkpolicy -n team-a
kubectl describe networkpolicy web-default-deny -n team-a

# 在另一个 namespace 起临时 Pod，测试访问是否被拒绝
kubectl run test-client --rm -it --image=busybox:1.36 -- nc -zv web-demo 80
# 预期：同 namespace 内访问成功，跨 namespace 或未放行端口应超时/拒绝
```

## 五、最佳实践与常见坑

**最佳实践**

- **最小权限优先**：先给最小集合，再按需加权限；杜绝把 `cluster-admin` 绑给普通用户或 CI 账号。优先使用命名空间级 `Role`/`RoleBinding`，必要时用「ClusterRole + 命名空间 RoleBinding」降域。
- **以 ServiceAccount 为主体**：为应用建立独立 ServiceAccount，并配合 Pod Security Standards 限制其 `automountServiceAccountToken`，避免令牌被滥用。
- **网络策略默认拒绝**：对核心命名空间先落 `podSelector: {}` + `policyTypes: [Ingress, Egress]` 的空规则，再逐条放行必要端口，**务必同时放行 DNS**。
- **Secret 静态加密**：Secret 仅 Base64 编码、**并非加密**，生产应开启 etcd 静态加密（KMS provider），并配合外部密钥系统（Vault + External Secrets Operator）。来源：[K8s: Using a KMS provider](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/kms-provider/)
- **策略纳入版本管理**：RBAC 与 NetworkPolicy 都应作为清单纳入 GitOps，配合准入控制与审计日志，形成「策略—部署—审计」闭环。

**常见坑**

- **ClusterRoleBinding 权限过宽**：误用集群级绑定会让权限跨命名空间扩散，是权限泄漏的高频来源。
- **NetworkPolicy 不覆盖 DNS**：只写 ingress 放行、漏写 egress 的 DNS 规则，会导致 Pod 无法解析域名，表现为「网络策略一上业务就挂」。
- **CNI 不支持 NetworkPolicy**：并非所有 CNI 都实现该特性，未支持时策略会被忽略，误以为「已隔离」实则全放行；上线前需确认 CNI 能力。
- **NetworkPolicy 不约束节点流量**：kubelet、kube-proxy、节点到 apiserver 的访问不受其约束，节点级隔离需依赖节点网络与安全组。
- **Secret 当成加密存储**：把真实口令直接写进 Secret 且未开静态加密，等于明文存放。
- **忽略弃用项**：v1.35 弃用 kube-proxy ipvs、v1.33 移除 `ValidatingAdmissionPolicy v1alpha1`、Ingress-NGINX 已退役，升级前应先完成迁移，避免升级后被动回滚。

## 六、核心要点速查

1. **RBAC 是 K8s 的授权机制**：`Role/RoleBinding` 命名空间级，`ClusterRole/ClusterRoleBinding` 集群级；`RoleBinding` 可引用 `ClusterRole` 做降域授权。
2. **授权链路**：认证确认身份 → RBAC 按规则（apiGroups/resources/verbs）判断是否放行，所有请求都经 `kube-apiserver`。
3. **主体三类**：User、Group、ServiceAccount；应用优先用独立 ServiceAccount 作为主体。
4. **NetworkPolicy 基于标签做 L3/L4 隔离**：用 `podSelector`/`namespaceSelector`/`ipBlock` 定义 ingress/egress，需 CNI 支持，不做 L7 治理。
5. **默认放行、选中即收紧**：未被任何策略选中的 Pod 默认全放行；被选中后仅放行规则明确允许的流量。
6. **默认拒绝要放行 DNS**：空 `podSelector` + `policyTypes: [Ingress, Egress]` 是最稳妥的基线，egress 别忘了 53 端口。
7. **Secret 仅 Base64 编码，非加密**：生产必须开静态加密并配合 KMS/Vault。
8. **权限排查三件套**：`kubectl auth can-i`、`kubectl get rolebinding -A`、`kubectl auth reconcile`。
9. **v1.36 起 kubelet 细粒度授权 GA**（KEP-2862）、用户命名空间 GA，RBAC 与容器隔离能力同步增强。
10. **v1.37 安全要点**：`KubeletInUserNamespace`（rootless）Beta、manifest-based admission control Beta，均可作为 2026-11 后的安全基线升级项。
11. **升级前置项**：kube-proxy ipvs 弃用、`ValidatingAdmissionPolicy v1alpha1` 已移除、Ingress-NGINX 退役，迁移需提前规划。

## 七、学习资源

1. [Kubernetes 官方文档：基于角色的访问控制（RBAC）](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/)
2. [Kubernetes 官方文档：Network Policies](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/)
3. [Kubernetes 官方：版本与补丁发布说明](https://kubernetes.io/releases/patch-releases/)
4. [K8s v1.36 发布说明（kubelet 细粒度授权、用户命名空间等）](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
5. [K8s v1.37：Rootless Beta（KubeletInUserNamespace）](https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/)
6. [Kubernetes v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
7. [K8s v1.35 Sneak Peek（kube-proxy ipvs 弃用、cgroup v1 弃用）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
8. [Kubernetes 官方：使用 KMS provider 实现 Secret 静态加密](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/kms-provider/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
