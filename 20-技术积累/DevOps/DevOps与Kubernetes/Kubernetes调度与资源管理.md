---
title: Kubernetes调度与资源管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 调度
  - 资源管理
aliases:
  - K8s调度
  - K8s资源管理
source: 网络资料整理
---

# Kubernetes调度与资源管理

> [!摘要] 摘要
> 本文聚焦 Kubernetes 的两条主线：**调度**（kube-scheduler 如何把 Pod 放置到合适的节点）与**资源管理**（requests/limits、QoS、HPA/VPA、DRA、工作负载感知调度等）。从基础概念与调度流程讲起，落到可直接运行的命令与清单示例，并给出最佳实践与常见坑，适合需要在实际集群中做容量规划、弹性伸缩与 GPU/AI 负载调度的运维与后端工程师。

## 一、最新动态（截至 2026-11）

> [!note] 说明
> 以下版本事实均来自截至 2026-11-19 的官方调研，升级或采用新特性前请以官方仓库为准。

- **Kubernetes v1.37（Garhwal）**：最新稳定版，2026-08-26 发布，截至 2026-11 已发布补丁 **1.37.2**。与调度/资源直接相关的变更：**动态资源分配（DRA）扩展资源支持进入 GA**、DRA 设备污点/容忍转 **Stable**、**HPA scale-to-zero 转 Beta 且默认启用**、Pod 级 checkpoint/restore（Beta）、工作负载感知调度继续演进（CompositePodGroup 多级编组、全有或全无调度）。来源：[Kubernetes v1.37 发布说明](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md) · [K8s v1.37 DRA Updates](https://kubernetes.io/zh-cn/blog/2026/09/03/kubernetes-v1-37-dra-updates/) · [K8s v1.37：Advancing Workload-Aware Scheduling](https://kubernetes.io/zh-cn/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/)
- **支持策略**：Kubernetes 维护**最近 3 个次版本分支 + 约 14 个月支持期**（12 个月标准期 + 2 个月维护期）。截至 2026-11 活跃分支为 **1.37 / 1.36 / 1.35**；**1.34 已于 2026-10-27 EOL**（最后补丁 1.34.13），**1.33 已于 2026-06-28 EOL**。来源：[kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/)
- **DRA 成熟度路线**：KEP 自 v1.34 获批，v1.35 Alpha、v1.36 Beta、**v1.37 GA**，正在成为替代传统设备插件的下一代硬件管理主线。应用侧仍可使用 `example.com/gpu` 这类扩展资源语法。
- **HPA scale-to-zero**：v1.37 中 `HPAScaleToZero`（KEP-2021）转 Beta 并默认启用，`minReplicas: 0` 可作用于 Object/External 指标；KEDA 仍是常用的指标适配与 scale-to-zero 路径。
- **节点与内核基线**：**cgroup v1 支持在 v1.35 被移除**，节点必须启用 cgroup v2；v1.35 引入**节点声明特性（Node Declared Features）**。
- **Pod 资源演进**：Pod 级资源请求/限制在 **v1.34 转 Beta**；**Pod 资源原地更新（Resize 子资源）自 v1.35 起 GA**，VPA 的 `InPlaceOrRecreate` 模式可借此在不重启 Pod 的前提下调整资源。

## 二、基础概念

- **调度（Scheduling）**：把尚未运行的 Pod 绑定到某个节点的过程，由控制平面中的 **kube-scheduler** 完成。调度器读取 Pod 的资源配置、亲和/反亲和、污点/容忍、节点选择器等约束，为每个候选节点打分，选出最优节点并写入 etcd。
- **资源请求与限制**：
  - `requests`：容器**期望**的最少资源，是**调度的依据**；调度器只考虑 `requests` 总和不超过节点可分配资源（`allocatable`）的节点。
  - `limits`：容器**允许使用**的上限；超过后由内核按 cgroup 约束（CPU 节流、内存 OOM Kill）。
- **QoS 等级**：由 requests 与 limits 共同决定，用于决定 Pod 在资源争抢或节点压力下的驱逐优先级：
  | QoS | 判定条件 | 驱逐优先级 |
  | --- | --- | --- |
  | **Guaranteed** | 每个容器的 CPU、内存 requests == limits | 最低（最不易被驱逐） |
  | **Burstable** | 至少一个容器有 requests，但不满足 Guaranteed | 中 |
  | **BestEffort** | 所有容器均未设置 requests/limits | 最高（最易被驱逐） |
- **节点可分配资源**：节点 `allocatable = 节点总容量 − 系统预留（kubelet、kube-proxy、DaemonSet 等占用）。`kubectl describe node` 中的 `Allocatable` 是调度的权威依据。
- **扩展资源**：如 `nvidia.com/gpu`，由设备插件（device plugin）或 **DRA** 上报，属于节点级不可超卖资源。
- **工作负载感知调度（Workload-Aware Scheduling, WAS）**：面向 AI/批处理负载的整组调度能力，v1.35 引入首批 Workload API，v1.37 继续演进，支持 CompositePodGroup 多级编组与全有或全无（gang）调度。

## 三、核心机制

### 3.1 调度主流程

kube-scheduler 采用「过滤（Filter）→ 打分（Score）→ 绑定（Bind）」的两阶段流程：

1. **过滤（PreFilter / Filter）**：排除不满足硬性约束的节点，如资源不足、`nodeSelector` 不匹配、污点未容忍、拓扑约束不满足等。
2. **打分（Score）**：对剩余候选节点按内置插件打分（资源均衡、节点亲和、Pod 亲和/反亲和、污点容忍、拓扑分布等），取最高分节点。
3. **绑定（Bind）**：通过 kube-apiserver 将 Pod 的 `spec.nodeName` 写入 etcd，完成调度。

> [!tip] 机制要点
> 调度器只认 **requests**，不看 limits；节点超卖 CPU 是常见误解——只要 requests 之和不超 allocatable，节点即可承载，而 limits 是运行期上限。

### 3.2 常用调度约束

- **nodeSelector / nodeAffinity**：把 Pod 固定到带特定标签的节点。
- **podAffinity / podAntiAffinity**：控制 Pod 之间的同节点共置或分散。
- **taints / tolerations**：节点通过污点排斥 Pod，Pod 需声明容忍才能调度。
- **topologySpreadConstraints**：跨拓扑域（如可用区）均匀分布，提升容灾能力。
- **DRA 设备污点/容忍**：v1.37 转 Stable，允许按设备维度做污点约束，是传统节点污点的设备级延伸。

### 3.3 资源治理三件套

| 组件 | 作用 | 关键参数 |
| --- | --- | --- |
| **HPA** | 按指标自动扩缩副本数 | `minReplicas` / `maxReplicas` / `metrics` |
| **VPA** | 按历史用量自动调整 requests/limits | `updateMode`（`InPlaceOrRecreate` / `Recreate`） |
| **DRA** | 面向 GPU 等可分区硬件的动态分配 | `resource.k8s.io/v1` 资源 |

- HPA 依赖指标：CPU 利用率、自定义资源指标、Object/External 指标。v1.37 的 scale-to-zero 允许 `minReplicas: 0`，但需注意冷启动。
- VPA 的 `InPlaceOrRecreate` 在 K8s ≥ 1.35 可配合 **Pod 资源原地更新（Resize）**，减少重启。
- 挂起的 Job 可在 v1.35 通过 `MutablePodResourcesForSuspendedJobs` 修改资源后再恢复，避免删除重建。

## 四、实践步骤（含代码/命令示例）

### 4.1 声明资源并观察 QoS

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
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

```bash
# 提交并确认调度结果、节点与 QoS
kubectl apply -f deployment.yaml
kubectl get pods -l app=web-demo -o wide
kubectl get pod web-demo-xxxx -o jsonpath='{.status.qosClass}'; echo
kubectl describe node | grep -A 8 Allocatable
```

### 4.2 用亲和与污点控制放置

```yaml
spec:
  template:
    spec:
      nodeSelector:
        disktype: ssd
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: web-demo
              topologyKey: kubernetes.io/hostname
      tolerations:
        - key: gpu
          operator: Equal
          value: "true"
          effect: NoSchedule
```

### 4.3 HPA 自动扩缩

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-demo
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-demo
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

```bash
kubectl apply -f hpa.yaml
kubectl get hpa web-demo
kubectl top pods -l app=web-demo
```

### 4.4 DRA：分配 GPU（v1.37 GA）

```yaml
apiVersion: resource.k8s.io/v1
kind: ResourceClaim
metadata:
  name: gpu-0
spec:
  resourceClassName: nvidia.com/gpu
  allocation:
    resources:
      - name: nvidia.com/gpu
        quantity: 1
---
apiVersion: v1
kind: Pod
metadata:
  name: gpu-job
spec:
  containers:
    - name: trainer
      image: registry/trainer:1.0
      resources:
        claims:
          - name: gpu-0
  resourceClaims:
    - name: gpu-0
```

### 4.5 用脚本判定 QoS（Python）

```python
def qos_class(containers):
    if not containers:
        return "BestEffort"
    if all(
        c.get("resources", {}).get("requests") == c.get("resources", {}).get("limits")
        and c.get("resources", {}).get("requests")
        for c in containers
    ):
        return "Guaranteed"
    if any(c.get("resources", {}).get("requests") for c in containers):
        return "Burstable"
    return "BestEffort"

pod = {"containers": [{"resources": {"requests": {"cpu": "100m", "memory": "128Mi"},
                                     "limits": {"cpu": "100m", "memory": "128Mi"}}]}
print(qos_class(pod["containers"]))  # Guaranteed
```

### 4.6 用 Groovy 模拟调度打分（理解打分插件）

```groovy
// 简化的调度打分：资源均衡 = 剩余可分配资源越多得分越高
def score(long nodeAllocatableCpu, long usedCpu) {
    long free = nodeAllocatableCpu - usedCpu
    return free < 0 ? 0 : free
}

def nodes = [[name: "node-a", allocatable: 8000, used: 4000],
             [name: "node-b", allocatable: 8000, used: 1000]]

nodes.each { n -> println("${n.name} score=${score(n.allocatable, n.used)}") }
// node-a score=4000 / node-b score=7000 → 调度器倾向 node-b
```

## 五、最佳实践与常见坑

**最佳实践**

- **先设 requests，再设 limits**：requests 决定能否被调度，limits 决定运行上限。建议 requests 贴合真实基线，limits 留合理余量。
- **生产按 QoS 分层**：关键服务用 **Guaranteed** 提升稳定性，非关键可接受 Burstable。
- **跨可用区分布**：用 `topologySpreadConstraints` 而非简单反亲和，避免单区故障导致整体不可用。
- **版本对齐 v1.37**：示例与清单尽量对齐 v1.37 官方文档；引用新特性时确认其成熟度（Alpha/Beta 不建议直接用于核心生产）。
- **弹性与成本平衡**：scale-to-zero 省成本但引入冷启动，对延迟敏感服务应设合理的 `minReplicas`。
- **GPU/AI 负载走 DRA + WAS**：v1.37 起 DRA 扩展资源 GA，配合工作负载感知调度实现整组调度，减少资源碎片。

**常见坑**

- **把 limits 当调度依据**：调度只看 requests，limits 不参与放置决策。
- **requests 虚高导致节点碎片化**：requests 远大于实际用量，会让节点"看起来满"，降低整体装箱率。
- **Guaranteed 误判**：必须 CPU 与内存**同时** requests == limits 才是 Guaranteed，仅一项相等仍为 Burstable。
- **scale-to-zero 冷启动**：`minReplicas: 0` 时流量突增可能触发明显延迟，需评估业务容忍度。
- **污点/容忍缺失**：Pod 长期 `Pending`，多为节点污点未容忍或 PVC 未绑定，用 `kubectl describe pod` 查看 Events 定位。
- **内核基线不符**：v1.35 起必须 cgroup v2，升级前先确认节点内核与运行时（containerd 2.x）基线，否则节点无法就绪。

## 六、核心要点速查

1. 调度三阶段：**过滤 → 打分 → 绑定**，由 kube-scheduler 完成，最终写入 etcd。
2. `requests` 决定**调度**，`limits` 决定**运行上限**；调度器只看 requests。
3. QoS 三级：**Guaranteed / Burstable / BestEffort**，Guaranteed 驱逐优先级最低、最稳定。
4. 常用约束：`nodeSelector`、`nodeAffinity`、`podAffinity/AntiAffinity`、`taints/tolerations`、`topologySpreadConstraints`。
5. 资源治理三件套：**HPA（扩缩副本）+ VPA（调 requests/limits）+ DRA（硬件动态分配）**。
6. **DRA**：v1.34 获批 → v1.35 Alpha → v1.36 Beta → **v1.37 GA**，是替代设备插件的下一代硬件管理主线。
7. **工作负载感知调度**：v1.35 首批 Workload API，v1.37 支持 CompositePodGroup 与全有或全无调度。
8. **HPA scale-to-zero**：v1.37 `HPAScaleToZero` 转 Beta 且默认启用，`minReplicas: 0` 需警惕冷启动。
9. **Pod 资源原地更新**自 v1.35 GA，VPA `InPlaceOrRecreate` 可减少重启。
10. 节点必须 **cgroup v2**（v1.35 移除 cgroup v1）；v1.37 活跃分支为 1.37 / 1.36 / 1.35。
11. 核心命令：`kubectl get/describe pod -o wide`、`kubectl top`、`kubectl get hpa`、`kubectl describe node | grep Allocatable`。

## 七、学习资源

1. [Kubernetes 官方文档：调度（Scheduling）](https://kubernetes.io/zh-cn/docs/concepts/scheduling-eviction/)
2. [Kubernetes 官方文档：分配资源（Requests, Limits, and QoS）](https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/)
3. [Kubernetes 官方博客：K8s v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
4. [Kubernetes 官方博客：K8s v1.37 DRA Updates](https://kubernetes.io/zh-cn/blog/2026/09/03/kubernetes-v1-37-dra-updates/)
5. [Kubernetes 官方博客：K8s v1.37 Advancing Workload-Aware Scheduling](https://kubernetes.io/zh-cn/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/)
6. [Kubernetes 官方：Version Skew Policy（版本偏差策略）](https://kubernetes.io/releases/version-skew-policy/)
7. [Kubernetes 官方：Patch Releases（补丁与 EOL 时间线）](https://kubernetes.io/releases/patch-releases/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
