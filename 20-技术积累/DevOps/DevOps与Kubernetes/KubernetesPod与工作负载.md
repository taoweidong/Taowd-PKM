---
title: Kubernetes Pod 与工作负载
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - Pod
  - 工作负载
  - 云原生
aliases:
  - K8s Pod 与工作负载
  - Kubernetes 工作负载
source:
  - 网络资料整理
---

# Kubernetes Pod 与工作负载

> [!摘要] 摘要
> 本文聚焦 Kubernetes 中最基础也最重要的一层抽象——**Pod 与各类工作负载控制器**。内容从 Pod 的结构与生命周期讲起，逐一拆解 Deployment、StatefulSet、DaemonSet、Job/CronJob 的职责与选择依据，覆盖核心机制、声明式部署步骤、资源治理与常见坑，并同步截至 2026-11 的 v1.37 关键变更（Pod 级资源、原地更新、checkpoint/restore、工作负载感知调度）。本文是 [[DevOps与Kubernetes-从入门到精通]] 体系中「对象与负载」这一环的落地展开，适合已具备容器基础、准备动手编排应用的工程师阅读。

## 一、最新动态（截至 2026-11）

以下版本号均以官方发布说明为准，检索时间 2026-11-19。

- **Kubernetes 当前主线为 v1.37（代号 Garhwal）**，于 **2026-08-26** 发布，截至 2026-11 已发布补丁 **1.37.2**。官方文档站点默认版本即 v1.37。该版本与工作负载相关的关键点：动态资源分配（DRA）扩展资源支持进入 **GA**、HPA scale-to-zero 转 **Beta**、**Pod 级 checkpoint/restore 转 Beta**、工作负载感知调度（CompositePodGroup 多级编组）继续演进。来源：[Kubernetes v1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)、[Kubernetes 补丁发布说明](https://kubernetes.io/releases/patch-releases/)。
- **支持策略**：项目维护最近 **3 个次版本分支** + 约 14 个月支持期（12 个月标准 + 2 个月维护期）。截至 2026-11 活跃分支为 **1.37 / 1.36 / 1.35**；**1.34 已于 2026-10-27 EOL**，1.33 于 2026-06-28 EOL。来源：[Kubernetes 补丁发布说明](https://kubernetes.io/releases/patch-releases/)。
- **Pod 资源相关版本演进**：Pod 级资源请求/限制 v1.32 Alpha → **v1.34 Beta**；**Pod 资源原地更新（`Resize` 子资源）自 v1.35 起 GA**；v1.35 还引入挂起 Job 可变资源（`MutablePodResourcesForSuspendedJobs`）、Pod 证书与节点声明特性。来源：[Kubernetes v1.35 Release](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)、[Kubernetes v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)。

## 二、基础概念

**Pod 是 Kubernetes 的最小调度与网络单元。** 一个 Pod 可以包含一个或多个共享网络命名空间（同一 IP、端口空间）与存储卷的容器，这些容器被打包在一起调度到同一个节点上，通常用来承载「主容器 + 边车（sidecar）」的协作关系，例如主应用 + 日志采集、流量代理等辅助容器。Pod 内的容器通过 `localhost` 直接通信，无需经过 Service；跨 Pod 通信则依赖 Service 的稳定访问与 DNS。

> [!tip] 何时拆 Pod、何时合 Pod
> 需要独立扩缩、独立生命周期、独立故障的组件，应拆成不同 Pod；强耦合、必须同节点部署、共享本地缓存或低延迟通信的组件，可以合在一个 Pod 内。拆分的边界决定了后续扩缩容与发布策略的粒度。

**工作负载控制器**是对「长期运行 / 有状态 / 每节点一份 / 跑完即止」等不同运行形态的抽象，全部位于稳定的 `apps/v1` API 下：

| 控制器 | 适用负载 | 核心职责 |
| --- | --- | --- |
| Pod | 最小单元，一般不单独使用 | 封装容器、定义共享环境 |
| Deployment | 无状态应用 | 管理副本数与滚动更新/回滚 |
| StatefulSet | 有状态应用 | 保证稳定网络标识与有序启停/扩缩 |
| DaemonSet | 系统级/采集类 | 每个节点运行一份 |
| Job / CronJob | 批处理、定时任务 | 跑完即止，按次数/周期运行 |

> [!note] 心智模型
> 控制器通过**声明式对账（reconcile loop）**持续工作：你用 YAML 声明期望状态，控制器把集群的实际状态不断收敛回期望状态。理解这一点，绝大多数「状态不对」的现象本质都是对账没有收敛。

## 三、核心机制

**Pod 的生命周期。** 容器具备 Init、Startup、Readiness、Liveness 以及 PostStart/PreStop 钩子。其中 `readinessProbe` 决定「是否接入流量」，`livenessProbe` 决定「是否重启容器」，二者不能混用；配合 `terminationGracePeriodSeconds` 与 `preStop` 钩子实现优雅终止，避免发布或缩容时丢请求。

**控制器的对账与滚动。** Deployment 通过 `ReplicaSet` 实现副本管理，滚动更新由 `maxSurge` / `maxUnavailable` 控制节奏与可用性。StatefulSet 通过 `spec.serviceName` 与 `podManagementPolicy` 保证稳定标识与顺序；DaemonSet 依赖节点污点/容忍保证每个节点恰好一份。

**资源调度与 QoS。** `kube-scheduler` 依据资源请求、亲和/反亲和、污点/容忍、节点选择器等维度打分，选出最合适的节点。`requests` 是调度依据，`limits` 是资源上限，二者共同决定 Pod 的 QoS 等级：Guaranteed / Burstable / BestEffort；当节点资源不足时，BestEffort 的 Pod 会最先被驱逐。v1.35 起 `Resize` 子资源 GA，允许**不重启 Pod** 原地调整 CPU/内存请求与限制；VPA 的 `InPlaceOrRecreate` 模式可借此减少重启，v1.37 的 Pod 级 checkpoint/restore 则面向有状态负载的调试与快速恢复。面向 AI/批处理场景，v1.37 的工作负载感知调度（CompositePodGroup 多级编组、全有或全无调度）让一组任务能作为整体被调度，避免部分成功、部分等待的资源浪费。

## 四、实践步骤（含代码/命令示例）

**1. 声明一个无状态 Deployment**（`deployment.yaml`）：

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
kubectl apply -f deployment.yaml -f service.yaml
kubectl get pods -l app=web-demo -o wide
kubectl rollout status deployment/web-demo
kubectl describe deployment/web-demo
kubectl port-forward svc/web-demo 8080:80   # 仅开发环境验证
```

**4. 回滚**：

```bash
kubectl rollout history deployment/web-demo
kubectl rollout undo deployment/web-demo --to-revision=1
```

**5. 有状态与批处理示例**：StatefulSet 需声明 `serviceName` 与稳定的 `volumeClaimTemplates`；批处理用 Job：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-demo
spec:
  parallelism: 2
  completions: 4
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: work
          image: busybox:1.36
          command: ["sh", "-c", "echo done"]
```

**6. 用 `kubectl` 做原地资源调整**（需 v1.35+，`Resize` 子资源）：

```bash
kubectl patch pod <pod-name> --type=merge -p '{"spec":{"containers":[{"name":"web","resources":{"requests":{"cpu":"200m","memory":"256Mi"},"limits":{"memory":"512Mi"}}}]}}'
```

## 五、最佳实践与常见坑

- **镜像 tag 用摘要（digest）而非可变标签**，避免同 tag 被覆盖导致「改了代码却没换镜像」。生产镜像还需接入私有仓库（如 Harbor）做扫描与签名。
- **探针职责要清晰**：`readinessProbe` 决定流量、`livenessProbe` 决定重启，不要都指向同一端点、也不要漏配，否则发布期会出现「流量已切走但容器被反复重启」。
- **资源必须显式声明 `requests`**。只写 `limits` 会导致调度器无法预估、容易产生 Pending；QoS 等级会直接影响被驱逐时的优先级。
- **优雅终止**：给长连接应用配置 `preStop` + `terminationGracePeriodSeconds`，否则滚动更新会丢请求。
- **StatefulSet 不要随意改 `spec.serviceName` 与 PVC 模板**，变更往往触发整体重建，需要规划好迁移。
- **版本迁移提示**：cgroup v1 在 v1.35 被弃用，节点须为 cgroup v2；containerd 1.X 自 v1.35 起不再受支持，需迁移到 containerd 2.0+。升级前先清理这些弃用项，避免被动回滚。

> [!warning] 易混淆点
> Pod 不是「进程」，删除 Pod 后由控制器重建，IP 与节点都可能变化；需要稳定访问必须依赖 Service（或 StatefulSet 的稳定网络标识），不要直接依赖 Pod IP。

## 六、核心要点速查

1. **Pod 是最小调度单元**，工作负载控制器（Deployment/StatefulSet/DaemonSet/Job/CronJob）稳定 API 均为 `apps/v1`。
2. 控制器通过**声明式对账**把实际状态收敛到 YAML 声明的期望状态。
3. `readinessProbe` 管流量，`livenessProbe` 管重启，配合 `preStop` 与 `terminationGracePeriodSeconds` 实现优雅终止。
4. `requests` 决定调度、`limits` 决定上限，二者共同决定 QoS 等级。
5. 截至 2026-11 主线为 **K8s v1.37（2026-08-26）**，活跃分支 1.37/1.36/1.35；1.34 已 EOL。
6. Pod 资源**原地更新自 v1.35 GA**（`Resize` 子资源）；v1.37 提供 Pod 级 checkpoint/restore（Beta）与工作负载感知调度。
7. 常用命令：`kubectl apply/get/describe/logs/rollout status/rollout undo`。

## 七、学习资源

1. [Kubernetes 官方文档：工作负载（Workloads）](https://kubernetes.io/zh-cn/docs/concepts/workloads/)
2. [Kubernetes 官方文档：Pod](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/)
3. [Kubernetes v1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
4. [Kubernetes v1.35 Release（Pod 资源原地更新 GA）](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)
5. [Kubernetes v1.34 Release（Pod 级资源 Beta）](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
6. [Kubernetes 补丁发布说明与支持策略](https://kubernetes.io/releases/patch-releases/)
7. [Kubernetes 版本偏差策略](https://kubernetes.io/releases/version-skew-policy/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]
- [[CI-CD与Jenkins-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
