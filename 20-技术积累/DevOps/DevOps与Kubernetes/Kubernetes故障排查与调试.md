---
title: Kubernetes 故障排查与调试
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 故障排查
  - 调试
  - 云原生
aliases:
  - K8s 故障排查
  - Kubernetes 调试
source: 网络资料整理
---

# Kubernetes 故障排查与调试

> [!摘要] 摘要
> 本文聚焦 Kubernetes 集群与应用出问题时「怎么查、查哪里、怎么修」的完整方法论。以「现象 → 分层定位 → 证据 → 修复」为主线，覆盖 Pod、网络、存储、调度、控制平面与可观测性六大排查域，给出可直接执行的 `kubectl` 命令清单、典型故障（`ImagePullBackOff`、`CrashLoopBackOff`、`Pending`、访问不通等）的定位路径，以及 2026 年最新版本下需要特别留意的排查工具与弃用项。适合后端/运维/SRE 工程师日常排障与知识体系补齐。

## 一、最新动态（截至 2026-11）

- **Kubernetes 主线为 v1.37（Garhwal）**，2026-08-26 发布，当前补丁 1.37.2；活跃支持分支为 **1.37 / 1.36 / 1.35**，1.34 已于 2026-10-27 EOL。排障时先确认集群实际版本，避免用旧版行为解释新集群现象。来源：[Kubernetes 补丁发布说明](https://kubernetes.io/releases/patch-releases/)
- **调试端点 z-pages**：v1.32 以 Alpha 引入，**v1.35 起提供结构化、机器可解析的响应**，便于把调试信息自动化接入排障流程。来源：[Kubernetes 1.35 z-pages API](https://kubernetes.io/zh-cn/blog/2025/12/31/kubernetes-1-35-z-pages/)
- **Pod 级 checkpoint/restore**：**v1.37 转 Beta**，对有状态负载的调试与快速恢复有意义。来源：[Kubernetes v1.37 发布](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
- **`kubectl` 偏好配置 `.kuberc`**：v1.34 起 Beta 且默认启用，可固化默认输出与别名，减少排障时反复敲长命令。来源：[Kubernetes v1.34 发布](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **可观测性工具版本**：Prometheus 最新 **3.16.0**（LTS 线 **3.13.x**）、Alertmanager 0.35.0、node_exporter 1.13.0；日志侧 **Loki 3.7.x**、**Fluent Bit 5.1.4**；一体化 Helm Chart **kube-prometheus-stack 88.6.0**。来源：[Prometheus 下载页](https://prometheus.io/download/) · [Loki v3.7 Release Notes](https://grafana.com/docs/loki/latest/release-notes/v3-7/) · [Fluent Bit v5.1.4](https://fluentbit.io/announcements/v5.1.4/)
- **网络方向的结构变化**：**Ingress-NGINX 已于 2026-03 归档退役**，官方转向 **Gateway API**；**kube-proxy ipvs 模式在 v1.35 被弃用**。网络层排障需结合 Gateway API 与 nftables 后端进行。来源：[K8s Blog: Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/) · [Kubernetes v1.35 Sneak Peek](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)

> [!note] 版本口径提示
> 版本号与 EOL 日期可能随官方调整变化，升级与排障前请以官方仓库/发布说明为准；托管集群（EKS/AKS/GKE/CCE）的 EOL 策略可能与上游不同，勿混用口径。

## 二、基础概念

**Kubernetes 排障的底层心智模型**：集群所有状态都由**控制器对账（reconcile loop）**驱动——控制器持续观察实际状态并把其收敛到 YAML 声明的期望状态。因此绝大多数「状态不对」的现象，本质是**对账没成功**：要么是条件不满足（资源、亲和、污点），要么是被准入控制拦截，要么是控制器/依赖组件本身异常。

**六层排查域**（按出现频率从高到低）：

| 排查域 | 关注对象 | 主要工具 |
| --- | --- | --- |
| 工作负载 | Pod 状态、事件、探针、日志 | `kubectl get/describe/logs/exec` |
| 网络 | Service、EndpointSlice、kube-proxy、NetworkPolicy、入口 | `kubectl exec` + `curl`/`nslookup`、`kubectl get endpoints` |
| 调度与资源 | requests/limits、污点容忍、亲和、节点容量 | `kubectl describe`、`kubectl top` |
| 存储 | PV/PVC/StorageClass、CSI 驱动 | `kubectl describe pvc/pv`、StorageClass 状态 |
| 控制平面 | kube-apiserver、etcd、scheduler、controller-manager | `kubectl get --raw`、z-pages、etcd 工具 |
| 可观测性 | 指标、日志、告警 | Prometheus/Grafana、Loki/EFK、Alertmanager |

**三个必读信息源**：

1. **Events（事件）**：`kubectl describe` 输出的 Events 段，直接给出失败原因的官方线索，是排障第一入口。
2. **Pod 状态（Phase）**：`Pending` / `Running` / `Succeeded` / `Failed` / `Unknown`，决定下一步查向。
3. **容器状态与重启原因**：`CrashLoopBackOff`、`ImagePullBackOff`、`CreateContainerConfigError` 等状态本身已高度提示方向。

## 三、核心机制

**1. 事件与对账。** 控制器通过 watch/informer 异步对账，`kube-apiserver` 是唯一入口，`etcd` 持久化全部状态。排障时如果「改了清单却没生效」，优先怀疑控制器未收敛或请求被准入策略拦截，而不是立刻怀疑集群损坏。

**2. Pod 生命周期与探针。** `readinessProbe` 决定「是否接入流量」，`livenessProbe` 决定「是否重启容器」，二者不可混用：把启动慢的依赖误配为 liveness，会导致容器被反复重启而永远起不来。配合 `terminationGracePeriodSeconds` 与 `preStop` 钩子实现优雅终止。

**3. 调度与资源。** `requests` 是调度依据，`limits` 是上限，二者共同决定 QoS 等级（Guaranteed/Burstable/BestEffort）。Pod 长期 `Pending` 的常见根因是资源不足、亲和性/污点不满足、PVC 未绑定。v1.35 起 `requests` 可配合原地调整（in-place resize，GA），调整资源时注意 `limits` 小于 `requests` 会造成资源超卖。

**4. 网络模型。** Service 通过 **EndpointSlice**（**v1.33 起 Endpoints API v1 已废弃**）暴露后端；kube-proxy 提供 iptables/ipvs/nftables 三种后端，**ipvs 在 v1.35 弃用**。南北向入口已由 Gateway API 接替 Ingress-NGINX，NetworkPolicy 做东西向隔离。

**5. 存储。** PVC 由 StorageClass 动态供给，依赖 CSI 驱动；PVC 卡在 `Pending` 多因未找到匹配的 StorageClass、无可用容量或驱动异常。v1.33 起 Git-Repo 卷插件默认禁用，涉及该类卷的清单需手动开启特性门控。

**6. 可观测性闭环。** 指标（Prometheus）、日志（Loki/EFK）、告警（Alertmanager）构成反馈闭环；排障时应由「指标确认现象 → 日志定位原因 → 事件确认处置」，避免只盯着单点。

## 四、实践步骤（含代码/命令示例）

### 4.1 排障前置：确认上下文与版本

```bash
# 确认当前上下文与集群，避免操作错集群
kubectl config current-context
kubectl config get-contexts

# 确认客户端与服务端版本是否匹配（版本偏斜会直接导致命令异常）
kubectl version --client
kubectl get --raw /version

# 确认集群整体健康与系统组件
kubectl get nodes -o wide
kubectl get pods -A --field-selector=status.phase!=Running
```

### 4.2 通用排查流程（固定顺序）

```bash
# 第一步：看事件，90% 的问题在 Events 段已有答案
kubectl get pod <pod> -o yaml | grep -A 20 events   # 或直接
kubectl describe pod <pod>
kubectl get events -n <namespace> --sort-by=.lastTimestamp

# 第二步：看日志，必要时看上一轮
kubectl logs <pod> --previous
kubectl logs <pod> -c <container> --tail=200

# 第三步：看状态与资源
kubectl get pod <pod> -o wide
kubectl get resource <资源> -n <namespace>
```

### 4.3 典型 Pod 故障定位

```bash
# ImagePullBackOff：镜像名/标签错误、私有仓库缺凭证、节点网络不通
kubectl describe pod <pod> | tail -30        # 查看拉取失败的具体报错
kubectl get secret <pull-secret>             # 确认 imagePullSecrets 是否存在

# CrashLoopBackOff：启动命令/配置/依赖问题，看上一轮日志
kubectl logs <pod> --previous --tail=500

# Pending（长期不调度）：资源、亲和、污点、PVC
kubectl describe pod <pod> | sed -n '/Events/,$p'
kubectl get pvc -n <namespace>
```

对应清单层面的快速排查：

```yaml
# 排查资源与调度：确认 requests 是否过高、污点是否容忍
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
spec:
  containers:
    - name: app
      image: nginx:1.27-alpine
      resources:
        requests:
          cpu: 500m
          memory: 256Mi
  nodeSelector:
    disktype: ssd          # 若节点无此标签，Pod 会一直 Pending
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "app"
      effect: "NoSchedule"
```

### 4.4 网络排障

```bash
# 从集群内部验证服务可达性（最常用）
kubectl run -it --rm debug --image=busybox:1.36 --restart=Never -- /bin/sh
# 容器内执行：
nslookup web-demo.default.svc.cluster.local
wget -qO- http://web-demo.default.svc.cluster.local

# 检查 Service 与后端是否匹配（标签一致才有 Endpoint）
kubectl get svc,endpoints,endpointslices -n <namespace>
kubectl describe svc <svc>

# 检查 NetworkPolicy 是否拦截
kubectl get networkpolicy -n <namespace>
```

### 4.5 节点与控制平面排障

```bash
# 节点资源压力与状态
kubectl top nodes
kubectl top pods -A --sort-by=memory
kubectl describe node <node> | sed -n '/Conditions/,$p'

# 节点级日志：v1.36 起支持 NodeLogQuery（需开 enableSystemLogQuery）
kubectl get --raw "/api/v1/nodes/<node>/proxy/logs/kubelet"

# 控制平面调试端点：z-pages（v1.35 起结构化输出，可脚本化消费）
curl -s https://<apiserver>/debug/zpages/
```

### 4.6 使用调试工具

```bash
# 临时挂载一个临时容器到目标 Pod，做诊断而不改业务镜像
kubectl debug -it <pod> --image=busybox:1.36 --target=<container>

# v1.37 起 Pod 级 checkpoint/restore（Beta），用于有状态负载快速恢复
# 需集群启用对应特性门控，具体以官方文档为准
kubectl get pods <pod> -o yaml
```

### 4.7 日志与指标聚合

```bash
# 用 PromQL 验证现象：查看某 Deployment 的请求成功率与 Pod 数
sum(rate(http_requests_total{deployment="web-demo"}[5m])) by (status)
kubectl get prometheus -n monitoring        # kube-prometheus-stack 部署时
```

## 五、最佳实践与常见坑

**排查纪律**

- **先看事件，再看日志，最后看状态**。顺序颠倒容易在日志里打转，而事件段往往一句话就点破根因。
- **保留证据再动手**：改动前先 `kubectl get -o yaml` 留存当前状态，出问题可快速回滚对比。
- **一次只改一个变量**：同时改镜像、资源、亲和，出问题时无法定位变量来源。

**常见坑**

- **`Secret` 只做 Base64 编码、不是加密**：不要把真实数据库口令、云 AK/SK 只放在 Secret 里；生产需配合外部密钥系统（Vault + External Secrets Operator、KMS 静态加密）。
- **镜像 tag 不要用 `latest`**：同 tag 被覆盖会导致「改了代码却没换镜像」，排查时极易被误导；生产用摘要（digest）。
- **kube-proxy ipvs 已弃用（v1.35）**：仍在使用 ipvs 的集群应规划迁移至 nftables/iptables，避免升级后行为变化。
- **Endpoints API v1 已废弃**：依赖 `kubectl get endpoints` 脚本的排障流程，应改用 `endpointslices`。
- **cgroup v1 在 v1.35 已移除**：节点内核必须启用 cgroup v2，否则节点无法正常加入集群。
- **Ingress-NGINX 已退役**：网络排障若仍基于旧 Ingress 控制器日志，需切换到 Gateway API 对应的 controller 与日志来源。
- **版本偏斜**：`kubelet`/`kube-proxy` 不得比 `kube-apiserver` 新、最多旧 3 个次版本；控制面组件须与 apiserver 同版或旧 1 个。版本不匹配会造成难以复现的异常，先核对版本再查逻辑。
- **生产禁止绕过声明式流程直接改**：直接 `kubectl edit`/`delete` 会污染对账基准，应改清单后重新 `apply`，让 GitOps/CI 保持唯一事实来源。
- **Helm 3 进入 EOL 倒计时**（最后功能版 2026-09-09，安全补丁至 2027-02-10）：排障与迁移建议尽早切到 Helm 4，注意 `--atomic`→`--rollback-on-failure`、`--force`→`--force-replace` 等旗标重命名。来源：[Helm 3 End of Life](https://v3.helm.sh/blog/helm-v3-end-of-life/)

## 六、核心要点速查

1. 排障心智模型：控制器对账未收敛是绝大多数「状态不对」的根因，先怀疑对账与准入，再怀疑集群损坏。
2. 固定顺序：**事件 → 日志 → 状态与资源 → 调度与准入链路**，`kubectl describe` 是第一入口。
3. 典型状态即方向：`ImagePullBackOff` 查镜像与凭证，`CrashLoopBackOff` 查启动日志（`--previous`），`Pending` 查资源/亲和/污点/PVC。
4. `readinessProbe` 管流量、`livenessProbe` 管重启，不可混用；启动慢的依赖误配 liveness 会导致反复重启。
5. Service 后端以 **EndpointSlice** 为准（Endpoints v1 已废弃）；`kubectl get svc,endpointslices` 是网络排查标配。
6. 网络排障优先用集群内部 `kubectl exec` + `curl/nslookup`，绕开外部因素直接验证 Service 与 DNS。
7. `requests` 决定调度、`limits` 决定上限；`limits` 小于 `requests` 会造成资源超卖，是常见隐患。
8. **Secret 仅 Base64 编码、非加密**，生产必须配合 Vault/KMS 等外部密钥系统与 RBAC 最小权限。
9. 节点级日志用 v1.36 的 **NodeLogQuery**，控制平面调试用 **z-pages**（v1.35 起结构化、可机器解析）。
10. v1.37 提供 **Pod 级 checkpoint/restore（Beta）**，适合有状态负载的快速恢复与调试。
11. 弃用项需提前迁移：kube-proxy ipvs、Endpoints v1、cgroup v1、Git-Repo 卷、Ingress-NGINX（→ Gateway API）、Helm 3。
12. 升级前核对版本偏斜与 EOL：活跃分支 1.37/1.36/1.35，1.34 已 EOL。
13. 可观测闭环：Prometheus 定现象、Loki/EFK 定位原因、Alertmanager 告警，三者联动而非各自为战。
14. 生产改动走声明式：改清单 → `kubectl apply` → 由 GitOps 对账，避免直接改集群导致对账基准漂移。

## 七、学习资源

1. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
2. [Kubernetes 官方：补丁发布说明（Patch Releases）](https://kubernetes.io/releases/patch-releases/)
3. [Kubernetes 官方：版本偏差策略（Version Skew Policy）](https://kubernetes.io/releases/version-skew-policy/)
4. [Kubernetes 官方博客：Kubernetes 1.35 版本化 z-pages API](https://kubernetes.io/zh-cn/blog/2025/12/31/kubernetes-1-35-z-pages/)
5. [Kubernetes 官方博客：Kubernetes v1.35 Sneak Peek（弃用与移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
6. [Kubernetes 官方博客：Announcing Ingress2Gateway 1.0](https://kubernetes.io/blog/2026/03/20/announcing-ingress2gateway-1-0/)
7. [Kubernetes 官方文档：Kubernetes 调试（Debugging Pods / Nodes）](https://kubernetes.io/zh-cn/docs/tasks/debug/)
8. [Prometheus 官方下载页（版本与发布说明）](https://prometheus.io/download/)
9. [Loki v3.7 Release Notes](https://grafana.com/docs/loki/latest/release-notes/v3-7/)
10. [Fluent Bit v5.1.4 发布说明](https://fluentbit.io/announcements/v5.1.4/)
11. [Helm 官方：Helm 3 End of Life（支持期时间线）](https://v3.helm.sh/blog/helm-v3-end-of-life/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]
- [[Kubernetes部署实践]]
- [[Prometheus监控入门]]

## 九、变更记录

- 2026-11-19：首次创建。
