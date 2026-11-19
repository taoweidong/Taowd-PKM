---
title: Kubernetes 生产运维与备份
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 生产运维
  - 备份恢复
aliases:
  - K8s生产运维与备份
  - Kubernetes备份与灾难恢复
source:
  - 网络资料整理
---

# Kubernetes 生产运维与备份

> [!summary] 摘要
> 本文聚焦 Kubernetes 从「能跑起来」到「能放心用」的生产级能力：以控制平面与 etcd 的可靠性为底座，覆盖版本生命周期管理、高可用部署、备份与灾难恢复（Velero / CSI 快照 / etcd 快照 / GitOps 分层备份）以及可观测性闭环。适合负责生产集群的运维、SRE 与平台工程师，作为日常运维与应急演练的实操手册。

Kubernetes 的生产运维，本质是围绕「**控制平面可靠 + 状态数据可恢复 + 变更可控 + 故障可观测**」建立一套可预期的运行体系。它与开发阶段的区别在于：开发关注功能跑通，生产关注的是升级失败能否回退、节点宕机能否自愈、误删资源能否恢复、故障能否在 SLO 内定位。

## 一、最新动态（截至 2026-11）

以下事实均来自官方发布说明，升级与迁移前请以官方文档为准。

- **Kubernetes v1.37（Garhwal）**：2026-08-26 发布的最新稳定版，截至 2026-11 已发布补丁 **1.37.2**，也是官方文档站点的默认版本。它增强了控制平面韧性，包括 Resilient Watch Cache、Pod 级 checkpoint/restore（Beta）、manifest-based admission control（Beta）。来源：[Kubernetes 补丁发布说明](https://kubernetes.io/releases/patch-releases/) · [Kubernetes v1.37 Release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
- **支持策略**：项目维护**最近 3 个次版本分支**，支持期约 14 个月（12 个月标准 + 2 个月维护期）。截至 2026-11 活跃分支为 **1.37 / 1.36 / 1.35**；**1.34 已于 2026-10-27 EOL**（最后补丁 1.34.13），1.33 已于 2026-06-28 EOL。来源：[Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/) · [Patch Releases](https://kubernetes.io/releases/patch-releases/)
- **etcd 压力优化**：v1.34 起 `ListFromCacheSnapshot` **默认启用**，通过 watch cache 快照做列表，降低对 etcd 的直接访问压力，对大规模集群的稳定性有实际意义。来源：[Kubernetes v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **备份工具 Velero**：最新 **1.18.x（1.18.4，2026-10-12）**，支持备份/恢复/迁移，含 CSI 快照、PV 备份与跨集群迁移。来源：[Velero 变更记录](https://images.minimus.io/images/velero/changelog/latest/versions/1.17.2/digest-history)
- **GitOps**：Argo CD 最新次版本 **3.5.x（3.5.3，2026-09-14）**，v3.6 计划 2026-12-15 出 RC，是生产配置与状态分层备份的重要一环。来源：[Argo CD Release Process](https://argo-cd.readthedocs.io/en/stable/developer-guide/release-process-and-cadence/)

## 二、基础概念

**生产运维的四个目标**：可用性（SLO 与错误预算）、可恢复性（RPO / RTO）、可控性（变更管理与回滚）、可观测性（指标、日志、告警）。

- **RPO（恢复点目标）**：允许丢失的最长数据时间窗口，决定备份频率；**RTO（恢复时间目标）**：故障后要求多久恢复，决定演练与工具选型。
- **控制平面**：`kube-apiserver`（唯一入口）、`etcd`（全量状态存储）、`kube-controller-manager`、`kube-scheduler`；**etcd 是生产备份的第一优先级**，它丢了整个集群的声明状态都无从恢复。
- **工作节点**：`kubelet`、`kube-proxy`、容器运行时（containerd）、CNI。节点可替换，状态在存储与仓库中。
- **备份分层**：
  1. **配置层**：集群清单、Helm release、GitOps 仓库——可由 Git 仓库重建。
  2. **数据层**：PV 数据、CSI 快照、数据库——需快照/备份工具。
  3. **控制平面层**：etcd 快照——控制平面状态本身。
  4. **镜像层**：镜像仓库（Harbor/OCI registry）——保证可重新拉取。

## 三、核心机制

**声明式对账**：控制器持续把实际状态收敛到 YAML 声明的期望状态。生产运维中「状态不收敛」的根因，绝大多数是控制器对账失败或被准入策略拦截，而非直接写坏数据。

**etcd 的可靠性机制**：etcd 是强一致 KV 存储，多副本通过 Raft 共识。生产必须多副本跨故障域部署，并定期快照 + 压缩（`auto-compaction`）+ 监控。etcd 一旦数据损坏，优先用最近快照恢复，再靠控制器对账补齐工作负载状态。

**版本偏斜与升级硬约束**：升级顺序必须是 **apiserver → 控制面组件（controller-manager / scheduler，须与 apiserver 同版或旧 1 个）→ kubelet / kube-proxy（不得比 apiserver 新，最多旧 3 个次版本）**。HA 集群中 kube-apiserver 新旧实例最多相差 1 个次版本。这是安全滚动升级控制面的前提。

**Velero 备份机制**：Velero 在集群内运行，通过**基于清单的备份**（backup 集群内的 Kubernetes 对象）与**基于 CSI 快照的数据备份**（对支持快照的存储卷做快照）两部分能力，把「对象 + 数据」打包成备份归档，存储到对象存储或 S3 兼容后端，恢复时按归档重建。

**GitOps 对账**：Argo CD / Flux 以 Git 仓库为唯一事实来源，持续把仓库声明同步到集群；集群内的人工直接修改会被对账覆盖。生产上应限制直接改集群，让 Git 成为配置的可审计备份源。

## 四、实践步骤（含代码/命令示例）

### 4.1 版本基线与集群巡检

```bash
# 确认节点、控制平面组件与版本
kubectl get nodes -o wide
kubectl get pods -n kube-system
kubectl version --output=yaml | grep -E 'gitVersion|gitCommit'

# 检查关键组件版本偏斜是否合规
kubectl -n kube-system get pod -l component=kube-apiserver -o jsonpath='{.items[*].spec.containers[*].image}'
```

### 4.2 etcd 快照（控制平面状态备份）

```bash
# 在任一控制平面节点执行（按需调整 ETCDCTL_API 与证书路径）
export ETCDCTL_API=3
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key

# 保存快照（按时间戳命名，保留多份）
etcdctl snapshot save /backup/etcd-$(date +%Y%m%d-%H%M%S).db

# 查看快照状态（确认大小与修订版本）
etcdctl snapshot status /backup/etcd-20261119-090000.db --write-out=table
```

恢复时停止 apiserver 与 etcd，替换数据目录后以快照启动，再逐台拉起控制平面组件，最后确认工作负载对账。

### 4.3 使用 Velero 备份与恢复

```bash
# 1. 准备对象存储后端（以 S3 兼容为例，也可用阿里云 OSS / 腾讯云 COS 等）
velero install --provider aws --bucket velero-backup \
  --secret-file credentials-velero \
  --use-volume-snapshots=true \
  --namespace velero

# 2. 备份整个命名空间
kubectl -n velero create backup prod-app --include-namespaces prod-app
# 也可全集群备份
kubectl -n velero create backup cluster-full

# 3. 查看与下载备份
kubectl -n velero get backup
kubectl -n velero describe backup prod-app

# 4. 恢复（可指定命名空间或恢复到新命名空间）
kubectl -n velero create restore prod-app-restore \
  --from-backup prod-app
kubectl -n velero create restore prod-app-copy \
  --from-backup prod-app --namespace prod-app-dr
```

### 4.4 基于 CSI 的数据快照

Velero 备份要真正保护数据，需底层存储支持 CSI VolumeSnapshot：

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: pg-data-snap
  namespace: prod-app
spec:
  volumeSnapshotClassName: csi-snap-class
  source:
    persistentVolumeClaimName: pg-pvc
```

```bash
kubectl apply -f volumesnapshot.yaml
kubectl get volumesnapshot -n prod-app -o yaml
```

### 4.5 GitOps 配置备份（Argo CD）

```bash
# 将生产集群清单与 Helm values 固化为 Git 提交，Git 即配置备份
git add deploy/prod && git commit -m "backup: prod manifests 2026-11-19"
git push origin main

# 确认同步状态
kubectl -n argocd get applications
argocd app sync prod-app --prune
```

### 4.6 升级前检查与回滚

```bash
# 升级前先确认弃用项（如已 EOL 分支、被弃用的 kube-proxy 模式）
kubectl get nodes
kubectl -n kube-system get pods -l component=kube-proxy

# 滚动升级控制平面与节点，遵循版本偏斜顺序
kubeadm upgrade plan
kubeadm upgrade apply v1.37.2

# 失败时回滚（控制平面回退到上一版本，节点逐台回退）
kubeadm upgrade apply v1.36.6
```

## 五、最佳实践与常见坑

**最佳实践**

- **etcd 三副本 + 跨故障域**：单副本 etcd 是生产集群最大的单点风险；备份与恢复演练至少每季度一次。
- **备份必须演练**：备份存在 ≠ 可恢复。定期在隔离环境做一次完整恢复演练，验证 RTO。
- **版本生命周期前置管理**：在分支 EOL 前完成升级，避免被动。1.34 已 EOL，仍在使用需尽快迁移。
- **镜像与依赖安全**：生产镜像用摘要（digest）而非可变 tag；配合扫描、签名（cosign）与镜像拉取策略。
- **RBAC 最小权限**：避免宽泛 `cluster-admin`，配置类操作纳入审计。
- **监控告警闭环**：Prometheus 采集 + Alertmanager 告警，配合 SLO 与错误预算决定是否允许变更。
- **分层备份**：Git 管配置、Velero 管对象与快照、etcd 管控制平面、云厂商快照管底层磁盘，各层互为补充。

**常见坑**

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 升级后 Pod 大面积 `Pending` | 版本偏斜超限、调度资源不足 | 检查 apiserver 与 kubelet 版本差；核对 requests 与污点/亲和 |
| Velero 恢复后 PV 数据丢失 | 未启用 CSI 快照或快照类未匹配 | 确认 `--use-volume-snapshots=true` 且 `volumeSnapshotClassName` 存在 |
| 备份文件巨大、恢复极慢 | 未做存储压缩与保留策略 | 定期压缩 etcd、配置 Velero 过期清理、限制快照保留份数 |
| 恢复后 Service 无法访问 | EndpointSlice/网络策略未随备份恢复 | 恢复后核对 `EndpointSlice`、NetworkPolicy 与 kube-proxy 状态 |
| 误删命名空间无法直接恢复 | 控制器级联删除已清理对象 | 依赖 etcd 快照或 Velero 定期备份，尽快从归档恢复 |
| `ImagePullBackOff` 在升级后集中出现 | 节点清理、镜像仓库凭证失效 | 检查 `imagePullSecrets` 与节点到仓库的连通性 |

> [!warning] 生产红线
> 不要在未备份等情况下直接执行破坏性操作（`delete namespace`、`kubeadm upgrade --force`、etcd 数据目录替换）。任何破坏性变更前，先确认最近一次可验证的备份。

## 六、核心要点速查

1. 生产运维四目标：**SLO 可用性、RPO/RTO 可恢复、变更可控、故障可观测**。
2. **etcd 是控制平面状态的唯一存储**，备份第一优先级是 etcd 快照，且需定期演练恢复。
3. 备份分层：**Git/Argo CD 管配置、Velero 管对象、CSI 快照管数据、云快照管磁盘**。
4. Velero 1.18.x 支持备份/恢复/迁移与 CSI 快照；生产需启用 `--use-volume-snapshots=true`。
5. 升级硬约束：**apiserver → 控制面组件 → kubelet/kube-proxy**，且 kubelet 不得比 apiserver 新。
6. 截至 2026-11 活跃分支为 **1.37 / 1.36 / 1.35**，**1.34 已于 2026-10-27 EOL**，需尽快迁移。
7. v1.34 起 `ListFromCacheSnapshot` 默认启用，降低 etcd 直接访问压力，利于大规模集群稳定。
8. GitOps 以 Git 为唯一事实来源，既是交付机制，也是配置层备份与审计源。
9. 恢复 ≠ 只回对象：需核对 EndpointSlice、NetworkPolicy、证书与镜像仓库连通性。
10. 核心命令：`etcdctl snapshot save/status`、`kubectl -n velero create backup/restore`、`kubeadm upgrade plan/apply`。

## 七、学习资源

1. [Kubernetes 官方：补丁发布与支持策略](https://kubernetes.io/releases/patch-releases/)
2. [Kubernetes 官方：Version Skew Policy（版本偏差策略）](https://kubernetes.io/releases/version-skew-policy/)
3. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
4. [Kubernetes 官方博客：Kubernetes v1.34 发布](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
5. [Velero 官方文档（备份与恢复）](https://velero.io/docs/main/)
6. [Argo CD 官方：Release Process and Cadence](https://argo-cd.readthedocs.io/en/stable/developer-guide/release-process-and-cadence/)
7. [Kubernetes 官方文档：云原生安全和 Kubernetes](https://v1-34.docs.kubernetes.io/docs/concepts/security/cloud-native-security/)
8. [Prometheus 官方文档：Overview](https://prometheus.io/docs/introduction/overview/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]
- [[CI-CD与Jenkins-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
