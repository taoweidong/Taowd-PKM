---
title: Kubernetes 监控（Prometheus）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - Prometheus
  - 监控
  - 可观测性
  - 云原生
aliases:
  - K8s监控
  - Prometheus监控
source:
  - 网络资料整理
---

# Kubernetes 监控（Prometheus）

> [!摘要] 摘要
> 本文聚焦 Kubernetes 集群监控的事实标准 Prometheus：从指标数据模型、拉取式采集机制、PromQL 查询、Alertmanager 告警链路，到在 K8s 上用 `kube-prometheus-stack` + `ServiceMonitor` 落地的完整步骤，并给出生产环境的版本选型、基数控制与常见坑。Prometheus 是 CNCF 毕业项目，与 Grafana（可视化）、Alertmanager（告警）、OpenTelemetry（统一采集）共同构成「指标」这一可观测性支柱，适合运维/SRE/后端工程师在学完 [[DevOps与Kubernetes-从入门到精通]] 后进入可观测性专题。

## 一、最新动态（截至 2026-11）

- **Prometheus 最新稳定版本为 3.16.0（2026-11-04）**，同时维护 **LTS 线 3.13.x（3.13.5，2026-10-21）**：追求新特性用最新版，生产稳定优先用 LTS 线。来源：[Prometheus Download](https://prometheus.io/download/)
- **Alertmanager 0.35.0（2026-11-09）**、**node_exporter 1.13.0（2026-11-19）**，均与 Prometheus 同属可观测性核心组件。来源：[Prometheus Download](https://prometheus.io/download/)
- **kube-prometheus-stack 88.6.0**：集成 Prometheus Operator + Grafana + Alertmanager + 告警规则的一站式 Helm Chart，是当前 K8s 上落地 Prometheus 的主流方式；Prometheus Operator 0.30+ 提供 `PrometheusRules` 准入 Webhook。来源：[Artifact Hub: kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack/88.6.0)
- **Kubernetes v1.37（Garhwal，2026-08-26）**：原生直方图（KEP-5808）进入 Beta，以稀疏直方图更高精度刻画 apiserver/etcd 延迟分布，支撑 SLI/SLO 高保真；CRI 统计取代 cAdvisor（Beta），节点/容器指标采集链路正在演进，Prometheus 是消费这些指标的主力。来源：[Kubernetes v1.37 Release](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)
- **OpenTelemetry Collector v0.161.0 / v1.67.0（2026-09）**：统一指标/日志/追踪的采集与转发，与 Prometheus 远程写入、日志后端（Loki 3.7.x）配合，推动「指标 + 日志 + 追踪」一体化。来源：[opentelemetry-collector v0.161.0](https://newreleases.io/project/github/open-telemetry/opentelemetry-collector/release/v0.161.0)

> [!note] 说明
> 上述版本号与日期来自官方下载页与发布说明（检索时间 2026-11-19）；升级与选型前请以官方仓库为准。

## 二、基础概念

**1. 指标与时间序列数据模型**：Prometheus 的最小单位是时间序列，由「指标名（metric name）+ 一组标签（labels）」唯一确定。例如 `container_cpu_usage_seconds_total{namespace="default",pod="web-demo-1"}` 就是一条时间序列；所有取值都带有时间戳。指标通常分四类：Counter（只增不减，如请求总数）、Gauge（可增可减，如内存使用量）、Histogram（分桶统计，用于延迟分布）、Summary（客户端直方图，无全局聚合）。

**2. 核心组件**：

| 组件 | 职责 | 一句话记忆 |
| --- | --- | --- |
| Prometheus Server | 抓取、存储、查询指标，产出告警 | 采集与查询中枢 |
| Exporter | 把目标系统的指标暴露成 `/metrics` | 指标的「翻译器」 |
| Alertmanager | 告警分组、静默、去重、抑制、路由 | 管「告警怎么发」 |
| Grafana | 可视化看板 | 管「看」 |
| Prometheus Operator | 用 CRD 声明式管理 Prometheus | 管「K8s 上的部署与发现」 |

常用 Exporter：`node_exporter`（节点）、`kube-state-metrics`（K8s 对象状态）、`cAdvisor`（容器，正被 CRI 统计取代）、`blackbox_exporter`（HTTP/TCP 探活）。

**3. 拉取式（pull）采集**：与日志的推送式不同，Prometheus 主动按固定间隔去抓取目标的 `/metrics`。服务发现是关键能力：Operator 模式下通过 `ServiceMonitor` / `PodMonitor` 声明「抓谁、抓哪个路径、多久抓一次」，Prometheus 会从 API Server 读取 Service/Endpoint/Pod 的标签自动发现目标。

**4. 在可观测性体系中的位置**：指标（Prometheus）、日志（Loki/EFK）、链路追踪（OpenTelemetry/Jaeger）是三支柱，Prometheus 负责**指标**这一环，与 [[Prometheus监控入门]] 的基础概念互为补充。

## 三、核心机制

**1. 采集链路**：`job` 定义一类抓取目标，`scrape_interval` 控制抓取周期，`metrics_path` 指定暴露路径。K8s 场景下，Prometheus 通过 Operator 注入的服务发现配置，依据 Service/Pod 标签自动生成抓取目标，新增副本无需改配置。

**2. 存储与长期化**：Prometheus 本地使用时序数据库（TSDB）按约 2 小时切块存储，单机能力有限。生产环境通过 **remote_write** 把数据写到 Thanos / Mimir / Cortex 等长期存储，再用统一的查询前端实现跨实例、跨周期的全局查询。

**3. 查询语言 PromQL**：即时查询（某时刻的值）与区间查询（一段时间内按步长取值）。核心函数如 `rate()`（Counter 的每秒增长率）、`sum()`/`avg()`（聚合）、`histogram_quantile()`（由直方图算分位数，如 P99 延迟）。

**4. 告警链路**：Prometheus 根据 `PrometheusRule` / 规则文件生成 Alert 事件，交给 **Alertmanager** 做分组（同组告警合并）、静默（silence）、去重、抑制（inhibition）与多渠道路由（邮件、Slack、Webhook、企业微信等）。

**5. 标签重写（Relabeling）**：在抓取前后对 target 与样本标签做增删改，例如把实例标签规范为 `instance=<pod>:<port>`、剔除高基数标签，是控制存储与查询成本的核心手段。

**6. 原生直方图**：K8s v1.37 的原生直方图（KEP-5808）以稀疏直方图形式上报，能以更高精度刻画延迟分布，是 SLI/SLO 度量的演进方向。

## 四、实践步骤（含代码/命令示例）

**1. 部署一体化栈（含 Prometheus Operator、Grafana、Alertmanager）**：

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set prometheus.prometheusSpec.retentionSize=10GB \
  --set grafana.enabled=true

kubectl get pods -n monitoring
```

**2. 用 ServiceMonitor 声明抓取目标**（放在 `monitoring` 命名空间，配合 Operator 的 `serviceMonitorSelectorNilUsesHelmValues` 配置，注意 Selector 要能匹配到目标）：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: web-demo-monitor
  namespace: monitoring
  labels:
    app.kubernetes.io/name: web-demo-monitor
spec:
  selector:
    matchLabels:
      app: web-demo
  namespaceSelector:
    matchNames:
      - default
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

**3. 编写 PromQL 查询**：

```promql
# 容器 CPU 使用率（cores）
rate(container_cpu_usage_seconds_total{namespace="default",container!=""}[5m])

# 容器内存使用量（MiB）
container_memory_working_set_bytes{namespace="default",container!=""} / 1024 / 1024

# 节点 CPU 使用率（%）
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Pod 容器重启次数
kube_pod_container_status_restarts_total
```

**4. 定义告警规则 PrometheusRule**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: web-demo-alerts
  namespace: monitoring
spec:
  groups:
    - name: web-demo.rules
      rules:
        - alert: WebDemoHighCPU
          expr: rate(container_cpu_usage_seconds_total{namespace="default",container="web"}[5m]) > 0.8
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "web-demo CPU 使用率过高"
            description: "容器 web 的 CPU 使用率持续 10 分钟超过 0.8 core"
```

**5. 访问 Grafana 与 Prometheus 验证**：

```bash
# Grafana 看板（默认账号 admin/admin，首次登录强制改密）
kubectl port-forward -n monitoring svc/prometheus-stack-grafana 3000:80

# Prometheus 查询界面
kubectl port-forward -n monitoring svc/prometheus-stack-prometheus 9090:9090

# 确认抓取目标与规则已生效
kubectl get prometheusrule -n monitoring
kubectl get servicemonitor -n monitoring
```

## 五、最佳实践与常见坑

- **资源 requests/limits 必须设置**：容器指标（尤其 CPU/内存）依赖 cgroup 限制，不设 requests/limits 时指标无意义、也不参与调度，是入门最常见错误。
- **控制标签基数**：不要把高基数值（Pod UID、随机 ID、请求 ID）放进标签，序列爆炸会耗尽存储与查询资源；用 Relabeling 剔除或降维。
- **生产选 LTS 线**：追求稳定用 Prometheus 3.13.x LTS，而非盲目追最新 3.16.0；kube-prometheus-stack 的版本与 Prometheus 版本要匹配，升级前看 Chart 兼容性。
- **关注采集链路变化**：K8s v1.37 起 CRI 统计取代 cAdvisor（Beta），存量看板中 `container_*` 系列指标的来源在变，升级前先验证指标可用性。
- **告警分级与抑制**：用 `for` 窗口过滤瞬时抖动，用 Alertmanager 分组/静默避免告警风暴；核心服务设更高优先级。
- **Prometheus 不鉴权**：默认 9090 无鉴权，**切勿公网裸暴露**；生产通过 Ingress/Gateway API 加鉴权、或仅在集群内访问，并配合 RBAC 限制查询与写入。
- **单机有规模上限**：大量节点、长保留期场景请启用 remote_write 到 Thanos/Mimir，或做分片（sharding），不要指望单机长期存储。
- **抓取间隔权衡**：间隔越短越实时但抓取压力与存储成本越高；核心服务 15–30s，一般服务 60s 起步。

## 六、核心要点速查

1. Prometheus 用「指标名 + 标签」定义时间序列，数据模型分 Counter/Gauge/Histogram/Summary 四类。
2. 采用**拉取式**采集，Prometheus 主动抓取目标的 `/metrics`；K8s 上通过 `ServiceMonitor`/`PodMonitor` 做服务发现。
3. 核心组件：Prometheus Server（采集/存储/查询）、Exporter（暴露指标）、Alertmanager（告警路由）、Grafana（可视化）、Prometheus Operator（CRD 声明式管理）。
4. PromQL 核心：`rate()` 求增长率、`histogram_quantile()` 算分位数、`sum()/avg()` 聚合。
5. 告警链路：Prometheus 产出 Alert → Alertmanager 分组/静默/去重/抑制/路由。
6. Relabeling 是控制标签基数、规范标签的核心手段。
7. 长期存储走 **remote_write** 到 Thanos/Mimir/Cortex，单机 TSDB 仅适合小规模。
8. 生产建议用 kube-prometheus-stack（88.6.0）一键部署 Prometheus Operator + Grafana + Alertmanager。
9. 截至 2026-11：Prometheus 最新 3.16.0（2026-11-04）、LTS 3.13.5（2026-10-21）；Alertmanager 0.35.0、node_exporter 1.13.0。
10. K8s v1.37 原生直方图（KEP-5808）Beta、CRI 统计取代 cAdvisor（Beta），指标采集链路持续演进。

## 七、学习资源

1. [Prometheus 官方文档：Overview（数据模型与架构）](https://prometheus.io/docs/introduction/overview/)
2. [Prometheus 官方文档：Installation（安装）](https://prometheus.io/docs/prometheus/latest/installation/)
3. [Prometheus 官方文档：Alerting（告警与 Alertmanager）](https://prometheus.io/docs/alerting/latest/)
4. [Prometheus Download（版本下载与最新版本号）](https://prometheus.io/download/)
5. [Artifact Hub：kube-prometheus-stack 88.6.0](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack/88.6.0)
6. [Prometheus Operator 官方仓库](https://github.com/prometheus-operator/prometheus-operator)
7. [OpenTelemetry 官方站点（统一遥测采集）](https://opentelemetry.io/)
8. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]（本知识点在 DevOps 与 Kubernetes 体系中的位置与全局框架）
- [[Prometheus监控入门]]（指标采集与告警的基础概念，与本文互补）
- [[DevOps]]（DevOps 理念与可观测性的整体背景）

## 九、变更记录

- 2026-11-19：首次创建。
