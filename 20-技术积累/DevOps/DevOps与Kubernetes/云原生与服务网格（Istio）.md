---
title: 云原生与服务网格（Istio）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 服务网格
  - Istio
  - 可观测性
aliases:
  - 云原生与服务网格
  - Istio 服务网格
source:
  - 网络资料整理
---

# 云原生与服务网格（Istio）

> [!摘要] 本文是「DevOps 与 Kubernetes」体系中「云原生与服务网格」这一知识点的落地学习文档。它以服务网格要解决的真实问题（东西向流量治理、安全加密、可观测性与弹性）为线索，讲清 Istio 的 Sidecar 与 Ambient 两种数据面形态、控制平面 istiod 与 xDS 配置下发机制，并给出从安装、注入、mTLS、金丝雀到安全策略的完整实操步骤。适合已掌握 Kubernetes 基础、准备把服务网格引入生产环境的运维/SRE 与后端工程师阅读。

云原生是以容器化、声明式 API、可观测性、弹性与自愈为核心的工程范式，CNCF（云原生计算基金会）是该领域的事实标准组织，其生态以 Kubernetes 为编排内核，叠加 Prometheus、Istio、Envoy、OpenTelemetry 等组件。服务网格（Service Mesh）是云原生中负责「东西向流量与安全」的一层：把流量治理、熔断重试、mTLS 加密、遥测采集等能力从业务代码中剥离，下沉到基础设施，让应用回归业务逻辑。Istio 是目前生态最完整、社区最活跃的服务网格实现。

## 一、最新动态（截至 2026-11）

以下事实取自 2026-11-19 的调研，版本与 EOL 日期均以官方来源为准。

- **Istio 最新次版本为 1.32，于 2026-11-09 发布**。来源：[Istio Releases](https://istio.io/latest/news/releases/)。
- **1.30 将于 2026-12-16 EOL**：Istio 遵循「N+2」支持规则，1.32 发布约 6 周后终止对 1.30 的支持，升级前需尽快规划迁移。来源：[Istio 1.30 EOL](https://istio.io/latest/news/support/announcing-1.30-eol/)。
- **Ambient 模式自 Istio 1.24（2024-11）起 GA**：ztunnel、waypoint 与相关 API 均已 Stable，官方正推进 sidecar → ambient 的数据面迁移。来源：[CNCF：Ambient 模式 GA](https://www.cncf.io/blog/2024/11/07/fast-secure-and-simple-istios-ambient-mode-reaches-general-availability-in-v1-24/) · [Istio Roadmap 2025-2026](https://preliminary.istio.io/latest/blog/2025/roadmap/)。
- **Gateway API 与 Telemetry API 在 Istio 1.22 晋升 Stable**，服务网格整体向「标准 API + 无 sidecar」方向演进。
- **Istio 1.28 引入 InferencePool v1**（Gateway API Inference Extension），面向生成式 AI 推理流量管理，是服务网格切入 AI 负载的标志性能力。来源：[Announcing Istio 1.28](https://istio.io/latest/news/releases/1.28.x/announcing-1.28/)。
- 云原生生态持续向 DRA/GPU 调度、原生可观测性、WASM 插件与 Gateway API 演进；Kubernetes 主线为 v1.37（2026-08-26 发布），Istio 与 K8s 版本存在兼容矩阵，升级前应核对对应关系（以官方仓库为准）。

## 二、基础概念

**云原生**：以容器为交付单元、以声明式 API 描述期望状态、以自动化控制器对账收敛、以可观测性形成反馈闭环的一整套工程实践，CNCF 技术图谱是其能力全景。

**服务网格**：把服务间（东西向）的流量管理、安全加密、可观测性与弹性能力，从业务代码中抽离到独立基础设施层。业务只需访问对端服务名，其余治理逻辑由网格统一完成。

**Istio 的两种数据面形态**：

| 模式 | 形态 | 治理层次 | 特点 |
| --- | --- | --- | --- |
| **Sidecar 模式** | 每个 Pod 注入一个 Envoy 边车 | L4 + L7 | 成熟稳定，治理粒度细，但占用额外资源、注入有约束 |
| **Ambient 模式** | 节点级 ztunnel + 可选 waypoint | ztunnel 做 L4/mTLS，waypoint 做 L7 | 无需改 Pod、原生 nftables、支持双栈，1.24 起 GA，官方主推迁移方向 |

**核心组件**：控制平面 `istiod`（配置与证书管理）、数据平面 Envoy（sidecar 或 waypoint）、`ztunnel`（ambient 下节点级 L4 代理）、入口网关 `istio-ingressgateway`。

**核心 CRD**：`VirtualService`（路由/重试/超时/故障注入）、`DestinationRule`（目标负载均衡、连接与熔断策略）、`Gateway` / `GatewayClass`（南北向入口）、`EnvoyFilter`（Envoy 底层扩展）、`Sidecar`（限定命名空间可见性）、`PeerAuthentication`（服务间 mTLS）、`RequestAuthentication`（JWT 校验）、`AuthorizationPolicy`（授权）。

## 三、核心机制

**控制平面 istiod**：负责服务发现、配置转换与证书签发。它把用户声明的 `VirtualService`、`DestinationRule` 等 CRD 转换为 Envoy 可识别的 xDS 配置，并通过 gRPC 长连接（**xDS 协议**：LDS/RDS/CDS/EDS/NDS/SDS）增量下发，实现配置热更新而无需重启代理。

**数据面请求链路**：以 sidecar 为例，入站流量经 Envoy 的 inbound listener 处理（重试、熔断、指标、访问日志），再转发给本地应用；出站流量经 outbound listener 按 `VirtualService` 做路由与负载均衡，同时完成 mTLS 与遥测埋点。`Sidecar` 资源通过 `egress`/`ingress` 字段限定该命名空间可访问的服务，是网格内服务发现与流量隔离的边界。

**流量治理**：`VirtualService` 定义匹配条件与目标（按权重/Header/URI 分流），`DestinationRule` 定义目标侧的负载均衡算法、连接池与熔断阈值，二者配合即可实现金丝雀、蓝绿、多版本并存。重试与超时需谨慎配置，避免叠加放大故障（见第五节）。

**安全机制**：`PeerAuthentication` 控制服务间是否启用 mTLS（STRICT/PERMISSIVE/DISABLE），`RequestAuthentication` 校验外部 JWT，`AuthorizationPolicy` 基于请求属性做授权，三者构成「加密 + 认证 + 授权」的纵深防御。

**Ambient 机制**：ztunnel 以节点为单位终结 L4 流量与 mTLS，实现无 sidecar 的加密；需要 L7 治理（重试、路由）的命名空间再部署 waypoint 作为代理，流量经 HBONE 隧道在 ztunnel 之间转发。

## 四、实践步骤（含代码/命令示例）

以下示例以 `istioctl` 安装、sidecar 模式为主，命令需结合集群实际版本核对。

**1. 安装 Istio（控制平面 + 数据面）**

```bash
# 下载对应平台的 istioctl，并加入 PATH
istioctl version

# 以 default profile 安装（含 istiod、入口网关与注入 Webhook）
istioctl install --set profile=default

# 查看组件状态
kubectl get pods -n istio-system
kubectl get svc -n istio-system istio-ingressgateway
```

**2. 为命名空间开启自动注入并部署示例应用**

```bash
kubectl create namespace demo
kubectl label namespace demo istio-injection=enabled

kubectl apply -f - <<'YAML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bookinfo
  namespace: demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: bookinfo
  template:
    metadata:
      labels:
        app: bookinfo
    spec:
      containers:
        - name: app
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: bookinfo
  namespace: demo
spec:
  selector:
    app: bookinfo
  ports:
    - port: 80
      targetPort: 80
YAML

# 确认 sidecar 已注入（每个 Pod 应有 2 个容器）
kubectl get pods -n demo -o jsonpath='{.items[*].spec.containers[*].name}'; echo
```

**3. 开启服务间 mTLS**

```yaml
# peer-auth.yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: demo
spec:
  mtls:
    mode: PERMISSIVE   # 过渡期允许明文与 mTLS 并存，验证后再改 STRICT
```

```bash
kubectl apply -f peer-auth.yaml
# 灰度验证无异常后切换为 STRICT
```

**4. 配置金丝雀路由（VirtualService + DestinationRule）**

```yaml
# canary.yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: bookinfo
  namespace: demo
spec:
  hosts:
    - bookinfo
  http:
    - route:
        - destination:
            host: bookinfo
            subset: v1
          weight: 90
        - destination:
            host: bookinfo
            subset: v2
          weight: 10
      timeout: 2s
      retries:
        attempts: 2
        perTryTimeout: 1s
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: bookinfo
  namespace: demo
spec:
  host: bookinfo
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

**5. 配置授权策略**

```yaml
# authz.yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-get
  namespace: demo
spec:
  selector:
    matchLabels:
      app: bookinfo
  action: ALLOW
  rules:
    - to:
        - operation:
            methods: ["GET"]
```

**6. 可观测性**

```bash
# 网格默认通过 Envoy 暴露指标，接入 Prometheus 抓取
kubectl get svc -n istio-system prometheus

# 通过 Kiali 查看网格拓扑与流量，Grafana 查看 Envoy 指标
# 部署方式参考官方文档：https://istio.io/latest/docs/tasks/observability/
```

**7. 清理**

```bash
kubectl delete namespace demo
istioctl uninstall
```

## 五、最佳实践与常见坑

**最佳实践**

- **版本与支持窗口**：紧跟 1.32，尽快完成 1.30 之前版本的迁移（1.30 于 2026-12-16 EOL），避免使用临近 EOL 的版本承担生产流量。
- **mTLS 渐进开启**：先用 `PERMISSIVE` 观察，确认无明文残留后统一切 `STRICT`，避免一刀切导致依赖未改造的服务大面积失败。
- **配置分层**：路由（`VirtualService`）与策略（`DestinationRule`）分离，按命名空间收敛 `Sidecar` 边界，降低跨网格误访。
- **可观测先行**：上线前先打通指标、访问日志与分布式追踪，否则网格故障时缺乏定位手段。
- **资源预留**：为注入的 Envoy 预留 CPU/内存，配合 HPA 与 Request/Limit 设置，避免与业务争抢资源。

**常见坑**

- **配置不生效**：CRD 修改后 Envoy 需要几秒级 xDS 收敛，先 `kubectl get vs/dr -n <ns>` 确认对象已就绪，再观察 Envoy 日志，勿急于回滚。
- **探针与重试叠加**：应用健康检查失败叠加网格重试会放大请求风暴，务必为重试设置 `perTryTimeout` 与总超时，并排除非幂等接口。
- **注入冲突**：命名空间已配置 `istio-injection` 但 Pod 有不可注入的调度约束（如 hostNetwork、特权容器）时，sidecar 可能无法注入，需显式调整或使用 `sidecar.istio.io/inject: "false"`。
- **Ambient 迁移**：sidecar → ambient 并非零成本，需要清理旧 `Sidecar` 资源并评估 waypoint 的 L7 能力边界，建议先在灰度命名空间验证。
- **与 NetworkPolicy 的关系**：Istio 的授权策略不替代 K8s `NetworkPolicy`，两者互补，网络层隔离仍应由 CNI 的 NetworkPolicy 负责。

## 六、核心要点速查

1. 服务网格把东西向流量治理、mTLS、可观测性下沉到基础设施，Istio 是当前生态最完整的实现。
2. Istio 架构 = 控制平面 `istiod` + 数据平面 Envoy；istiod 经 **xDS 协议**增量下发配置，实现热更新。
3. 核心 CRD：`VirtualService`（路由）、`DestinationRule`（策略）、`Gateway`（入口）、`PeerAuthentication`（mTLS）、`AuthorizationPolicy`（授权）。
4. 两种数据面形态：**Sidecar**（Envoy 边车，L4+L7）与 **Ambient**（ztunnel L4/mTLS + 可选 waypoint L7），Ambient 自 1.24（2024-11）GA。
5. 截至 2026-11：Istio 最新次版本 **1.32（2026-11-09）**，**1.30 将于 2026-12-16 EOL**。
6. mTLS 开启顺序：`PERMISSIVE` → 验证 → `STRICT`，不要直接切 STRICT。
7. 重试/超时必须设上限，避免与探针、非幂等请求叠加放大故障。
8. 网格可观测性依赖指标、访问日志与追踪三件套，先观测后上治理策略。

## 七、学习资源

1. [Istio 官方文档：概念（Concepts）](https://istio.io/latest/docs/concepts/)
2. [Istio 官方文档：安装（Install）](https://istio.io/latest/docs/setup/install/)
3. [Istio 官方文档：流量管理任务（Traffic Management）](https://istio.io/latest/docs/tasks/traffic-management/)
4. [Istio 官方文档：安全（Security）](https://istio.io/latest/docs/tasks/security/)
5. [Istio 官方文档：Ambient 模式](https://istio.io/latest/docs/ops/ambient/)
6. [Istio Releases（版本与发布说明）](https://istio.io/latest/news/releases/)
7. [Istio 1.30 EOL 公告](https://istio.io/latest/news/support/announcing-1.30-eol/)
8. [CNCF：Ambient 模式在 v1.24 达到 GA](https://www.cncf.io/blog/2024/11/07/fast-secure-and-simple-istios-ambient-mode-reaches-general-availability-in-v1-24/)
9. [Announcing Istio 1.28（InferencePool v1）](https://istio.io/latest/news/releases/1.28.x/announcing-1.28/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
