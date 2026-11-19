---
title: Kubernetes 日志（EFK/Loki）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 日志
  - Loki
  - EFK
  - 可观测性
  - 云原生
aliases:
  - K8s日志
  - EFK与Loki
source:
  - 网络资料整理
---

# Kubernetes 日志（EFK/Loki）

> [!summary] 摘要
> 本文聚焦 Kubernetes 集群中的日志体系：讲清「采集（Fluent Bit/Fluentd）→ 聚合（Loki/Elasticsearch）→ 可视化（Grafana/Kibana）」的完整链路，对比经典 **EFK** 与轻量 **Loki** 两条技术路线的适用场景，并给出基于 Helm 的落地部署步骤、LogQL/查询示例与常见坑。定位为 [[DevOps与Kubernetes-从入门到精通]] 体系中「可观测性」的日志专篇，适合已经掌握 Pod/Service 基础、准备为集群补齐日志能力的后端与运维/SRE 工程师。

## 一、最新动态（截至 2026-11）

| 组件 / 动态 | 版本 / 时间 | 关键信息 | 来源 |
| --- | --- | --- | --- |
| **Grafana Loki** | **3.7.x**（3.7.0/3.7.1 于 2026-03-26，3.7.2 于 2026-05-14） | 当前主流日志聚合方案；**其 Helm chart 自 2026-03-16 起移交社区仓库 `grafana-community/helm-charts`**，Grafana Labs 继续维护企业版 GEL chart | [Loki v3.7 Release Notes](https://grafana.com/docs/loki/latest/release-notes/v3-7/) |
| **Fluent Bit** | **5.1.4**（2026-10-12） | 轻量采集 Agent，同时支持日志、指标与追踪 | [Fluent Bit v5.1.4](https://fluentbit.io/announcements/v5.1.4/) |
| **OpenTelemetry Collector** | v0.161.0 / v1.67.0（2026-09） | 统一采集并转发指标/日志/链路，可作为 Fluent Bit 之后的标准化出口 | [opentelemetry-collector v0.161.0](https://newreleases.io/project/github/open-telemetry/opentelemetry-collector/release/v0.161.0) |
| **Prometheus** | 3.16.0（2026-11-04，最新）/ 3.13.5（LTS） | 日志与指标需联动时，注意区分最新线与 LTS 线 | [prometheus.io/download](https://prometheus.io/download/) |
| **kube-prometheus-stack** | 88.6.0 | Prometheus Operator + Grafana + Alertmanager 一体化 Chart，可与 Loki 同仓部署 | [Artifact Hub](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack/88.6.0) |
| **Kubernetes 排障相关** | v1.36 NodeLogQuery（KEP-2258，GA，需开启 `enableSystemLogQuery`）；v1.37 Pod 级 checkpoint/restore（Beta） | 节点系统日志可直接查询，Pod 崩溃现场更易保留与恢复 | [K8s v1.36 Release](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/) · [K8s 1.37 Release](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/) |

> [!note] 说明
> 上表版本号与日期均来自 2026-11-19 检索的调研资料；Helm chart 归属、各组件后续版本变化较快，动手部署前请以官方仓库与发布说明为准。

**生态趋势**：EFK（Elasticsearch + Fluentd/Fluent Bit + Kibana）仍是经典组合，但 Elastic 许可证与资源开销较大；Loki 以「索引标签、日志低成本存储」为卖点，且与 Prometheus 共享标签体系，越来越常作为 EFK 的替代或补充。二者不是二选一——规模大、需要全文检索与复杂分析时选 Elasticsearch，以标签过滤为主、追求低成本与 Grafana 一体化时选 Loki。

## 二、基础概念

**完整链路**：无论选哪条路线，日志都要经过三个环节——

1. **采集**：容器内应用写日志 → 容器运行时落盘/写驱动 → 节点上的采集 Agent（Fluent Bit / Fluentd / Promtail）读取。
2. **聚合与存储**：后端聚合层接收并存储（Loki 的 Distributor/Ingester，或 Elasticsearch 的倒排索引），负责标签、压缩与长期保存。
3. **可视化与检索**：Grafana（配 Loki 数据源）或 Kibana（配 Elasticsearch）做查询、看板与告警。

**容器日志来源**：应用应写 **stdout/stderr**，由容器运行时（containerd 等）按驱动落盘，kubelet 负责轮转，不要直接在容器内写本地文件。K8s 自 v1.24 移除 dockershim，集群中真正运行容器的是满足 CRI 的运行时，本地 `docker logs` 的思维要转换为「节点上运行时日志 + 采集 Agent」。

**核心组件**：

| 组件 | 角色 | 特点 |
| --- | --- | --- |
| Fluent Bit | 采集 Agent（Tail 文件 + 解析 + 过滤 + 输出） | 极轻量、C 实现，适合大规模节点，可同时输出指标/追踪 |
| Fluentd | 采集/缓冲 Agent | 插件生态丰富、功能强大，资源占用高于 Fluent Bit |
| Promtail | Loki 官方采集器 | 与 Loki 深度集成，配置简单，适合 Loki 路线 |
| Loki | 日志聚合与存储 | 只索引标签、不索引日志正文，存储与查询成本低 |
| Elasticsearch | 全文检索与存储 | 倒排索引，全文检索能力强，资源与运维成本高 |
| Kibana | 可视化 | Elastic 生态默认前端，适合日志分析与挖掘 |
| Grafana | 可视化 | 同时对接指标、日志、链路，是 Loki 路线的自然前端 |
| OpenTelemetry Collector | 统一采集转发 | 标准化遥测出口，可做多后端分发与脱敏 |

**Loki 的核心思想**：与 Elasticsearch「索引每个词」相反，Loki **只对标签（labels）建索引，日志正文以压缩块（chunk）形式存放**。因此标签基数必须控制，否则索引膨胀；而正文检索通过流式扫描完成，在「按标签过滤 + 关键字搜索」场景下成本极低。

## 三、核心机制

**1. 容器日志如何从 Pod 到后端**

应用写 stdout/stderr → CRI 按配置的日志驱动落盘（默认多为 `json-file`，kubelet 参数 `--container-log-rotate-size` / `--container-log-rotate-max-age` 控制轮转）→ 采集 Agent 以 **Tail 方式**持续读取节点日志文件，按行解析成结构化记录，打上 `namespace`、`pod`、`container`、`app` 等标签后发送到聚合层。

**2. Fluent Bit 的采集流程**

`Input`（tail 容器日志文件）→ `Parser`（解析 json 或正则）→ `Filter`（重命名、脱敏、丢弃）→ `Output`（推送到 Loki 或 Elasticsearch）。多行异常栈（Java 堆栈等）需要 `multiline` 解析规则，否则一行一记录会打散上下文。

**3. Loki 的写入与查询架构**

写入路径：`Distributor`（校验标签、分片）→ `Ingester`（内存中组装成 chunk，落对象存储/文件系统）。查询路径：`Querier` 按标签定位流，再对 chunk 做 LogQL 过滤与解析。标签是 Loki 的命脉，建议沿用 Prometheus 标签习惯，保证「指标 + 日志」可按同一套标签关联。

**4. Elasticsearch 的存储机制**

ES 建立**倒排索引**，支持全文检索、聚合分析，代价是索引与堆内存开销大，需要分片、副本、滚动索引与定期清理策略。

**5. LogQL 与 Kibana 查询的差异**

LogQL 是 Loki 的查询语言，形如 `{namespace="default", app="web-demo"} |= "error"`，先按标签选流再按内容过滤；Kibana 则基于 ES 的 DSL 做全文检索与聚合。两者都能做过滤与统计，但 Loki 的过滤发生在扫描阶段，成本与标签基数直接相关。

## 四、实践步骤（含代码/命令示例）

**方案选择**：

| 场景 | 推荐 |
| --- | --- |
| 中小集群、成本敏感、已用 Grafana | Loki + Promtail/Fluent Bit |
| 需要全文检索、复杂分析、日志量大 | Elasticsearch + Fluent Bit + Kibana |
| 已有统一可观测平台 | OpenTelemetry Collector 统一出口，按数据类型分发 |

**步骤 1：用 Helm 部署 Loki**（Loki chart 已迁至社区仓库，部署前核对仓库地址）

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 创建命名空间
kubectl create namespace monitoring

# 安装 Loki（含 Promtail 子 chart，可按集群规模决定是否启用）
helm install loki grafana/loki \
  --namespace monitoring \
  --set loki.enabled=true \
  --set promtail.enabled=true \
  --set promtail.config.extraScrapeConfigs=... \
  --values loki-values.yaml
```

**步骤 2：配置采集（Fluent Bit DaemonSet 示例）**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: monitoring
data:
  fluent-bit.conf: |
    [SERVICE]
    Flush        5
    Daemon       Off
    Log_Level    info

    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Tag              container.*
        Mem_Buf_Limit     5MB
        Restart_On_Retry  true
        Refresh_Interval  5

    [PARSER]
        Name         json
        Format       json
        Time_Key     time
        Time_Format  %Y-%m-%dT%H:%M:%S.%L%z

    [FILTER]
        Name          modify
        Match         container.*
        Add          log_level    INFO
        Add          namespace     *

    [OUTPUT]
        Name          loki
        Match         container.*
        Labels        {job=fluent-bit, cluster=prod}
        Line_Format   json
        Label_Keys    time,namespace,pod,container
```

```bash
# 部署采集器
kubectl apply -f fluent-bit-daemonset.yaml
kubectl -n monitoring get pods -l app=fluent-bit -o wide
```

**步骤 3：验证与查询**

```bash
# 先看 Pod 自身日志，确认采集链路没有报错
kubectl -n monitoring logs -l app=loki --tail=100

# Loki 就绪后用 Grafana 添加 Loki 数据源，或在命令行用 LogQL 验证
```

LogQL 常用查询（在 Grafana Explore 或 `loki-cli` 中使用）：

```logql
# 按标签过滤并搜索关键字
{namespace="default", app="web-demo"} |= "error"

# 最近 5 分钟、不区分大小写匹配 panic/fatal，取前 100 行
{namespace="kube-system"} |~ "(?i)(panic|fatal)" [5m] | limit 100

# 解析 JSON 正文并提取字段
{namespace="default"} | json | label_format level=.level, msg=.msg

# 统计每个 Pod 的错误日志速率
sum(rate({namespace="default"} |= "error" [5m])) by (pod)
```

**步骤 4：需要全文检索时部署 EFK（简例）**

```bash
# Elasticsearch（生产需配置持久化、分片与资源限制）
helm install elasticsearch elastic/elasticsearch \
  --namespace logging --create-namespace

# Kibana
helm install kibana kibana/kibana \
  --namespace logging \
  --set service.type=ClusterIP

# Fluent Bit 的 Elasticsearch 输出段
```

Fluent Bit 输出到 ES 的配置片段：

```ini
[OUTPUT]
    Name            es
    Match           container.*
    Host            ${ES_HOST}
    Port            9200
    Index           k8s-logs
    Type            _doc
    Retry_Limit     false
    Log_ES_Error    true
```

若使用 Logstash 做清洗，可用 Groovy 过滤器做结构化打标：

```groovy
filter {
  groovy {
    def msg = event.get("message").toLowerCase()
    if (msg.contains("error") || msg.contains("fatal")) {
      event.set("severity", "error")
    } else if (msg.contains("warn")) {
      event.set("severity", "warn")
    } else {
      event.set("severity", "info")
    }
  }
}
```

**步骤 5：基础排障命令**

```bash
kubectl logs <pod>                       # 当前容器日志
kubectl logs <pod> --previous            # 上一个崩溃容器的日志
kubectl logs <pod> -c <container>        # 多容器时指定容器
kubectl logs <pod> --timestamps --tail=200
kubectl get events --sort-by=.lastTimestamp
kubectl describe pod <pod>               # 看事件，含日志相关异常
```

## 五、最佳实践与常见坑

**标签设计（Loki 最关键的坑）**：Loki 只索引标签，**标签基数过高会导致索引膨胀、查询变慢甚至写入被拒**。不要把 `user_id`、`request_id`、`trace_id` 这类高基数字段做成标签，正文里搜即可。建议标签控制在 `namespace`、`pod`、`container`、`app`、`env` 这类低基数维度，符合 Prometheus 标签习惯以便与指标联动。

**采集与存储的常见坑**：

- **磁盘被日志打满**：限制 `Mem_Buf_Limit`，合理设置日志轮转；避免 Pod 内应用无界写本地日志文件，优先走 stdout。
- **多行堆栈被打散**：Java/Go 异常栈需要配置 `multiline` 解析，否则上下文断裂。
- **采集器资源失控**：Fluent Bit 要设置 CPU/内存 requests/limits，避免日志洪峰时抢占业务资源。
- **敏感信息泄漏**：日志中常出现令牌、口令、手机号，应在 Filter 层做脱敏或丢弃，避免原样落入存储。
- **保留期与对象存储**：Loki 适合把长期数据放对象存储（S3/MinIO）并配好保留期，ES 则需按天建索引并定期删除/归档，否则磁盘与堆内存压力大。
- **权限与安全**：采集 Agent 通常需要读取节点日志，注意 RBAC 与节点访问控制；不要给采集器过大的集群权限。

**部署与版本注意**：

- Loki 的 Helm chart 自 **2026-03-16** 起在 `grafana-community/helm-charts` 维护，升级前核对仓库与版本，不要沿用旧的拉取地址。
- 生产环境 Prometheus 建议使用 **LTS 线 3.13.x** 而非最新 3.16.0，与日志链路联调时注意版本对应关系。
- Fluent Bit 5.x 的配置项与 1.x/2.x 有差异，从旧版本迁移时需按官方变更说明核对。
- K8s 侧排障能力也在增强：v1.36 的 NodeLogQuery（需开 `enableSystemLogQuery`）可直接查节点系统日志，v1.37 的 Pod checkpoint/restore 有助于保留崩溃现场，可结合日志链路一起使用。

## 六、核心要点速查

1. 日志链路统一为「**采集（Fluent Bit/Fluentd/Promtail）→ 聚合（Loki/Elasticsearch）→ 可视化（Grafana/Kibana）**」，三步缺一不可。
2. 容器应用日志写 **stdout/stderr**，由 CRI 落盘、kubelet 轮转，采集 Agent 以 Tail 方式读取。
3. **EFK** 是 Elasticsearch + Fluentd/Fluent Bit + Kibana，全文检索强、资源开销大；**Loki** 只索引标签、正文压缩存储，成本低，是中小集群与 Grafana 体系的常见选择。
4. Loki 的命脉是**标签基数**：只保留低基数维度标签，高基数内容放正文。
5. LogQL 先按标签选流再按内容过滤，形如 `{namespace="default"} |= "error"`；ES 则是倒排索引全文检索。
6. 多行异常日志需配 **multiline 解析**，否则上下文被打散。
7. 采集器必须设资源限额，日志洪峰时避免抢占业务资源。
8. 日志中必须做**敏感信息脱敏**，存储需配置**保留期与归档策略**。
9. 版本基线（截至 2026-11）：Loki **3.7.x**（chart 已移交 `grafana-community/helm-charts`）、Fluent Bit **5.1.4**、OpenTelemetry Collector v0.161.0/v1.67.0。
10. 排障口诀：先 `kubectl logs`（必要时 `--previous`）→ `kubectl describe` 看事件 → 再看采集与后端链路是否正常。

## 七、学习资源

1. [Grafana Loki 官方文档（含 v3.7 Release Notes）](https://grafana.com/docs/loki/latest/)
2. [Loki v3.7 Release Notes](https://grafana.com/docs/loki/latest/release-notes/v3-7/)
3. [Grafana Loki LogQL 官方文档](https://grafana.com/docs/loki/latest/query/logql/)
4. [Fluent Bit v5.1.4 发布公告](https://fluentbit.io/announcements/v5.1.4/)
5. [Fluent Bit 官方文档：Tail 输入与多行解析](https://docs.fluentbit.io/manual/input/tail)
6. [Elasticsearch 官方文档：日志与索引管理](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
7. [Kubernetes 官方文档：Logging Architecture（集群日志架构）](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
8. [Kubernetes v1.36 发布说明（NodeLogQuery）](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
9. [OpenTelemetry Collector v0.161.0](https://newreleases.io/project/github/open-telemetry/opentelemetry-collector/release/v0.161.0)
10. [Artifact Hub：kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack/88.6.0)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[Kubernetes核心概念与架构]]
- [[Prometheus监控入门]]
- [[Kubernetes部署实践]]

## 九、变更记录

- 2026-11-19：首次创建。
