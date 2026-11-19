---
title: Kubernetes 存储与 PV/PVC
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 存储
  - PV
  - PVC
  - CSI
  - 云原生
aliases:
  - Kubernetes存储与PV-PVC
  - PV与PVC
  - Kubernetes持久化存储
source:
  - 网络资料整理
---

# Kubernetes 存储与 PV/PVC

> [!摘要] 摘要
> 本文聚焦 Kubernetes 持久化存储子系统，讲解 **PV、PVC、StorageClass、CSI** 四类核心对象，覆盖静态/动态供给、回收/扩容/快照机制，并给出可运行的 YAML 与 `kubectl` 步骤、生产最佳实践与常见坑。版本基线对齐 2026-11 的 **Kubernetes v1.37（Garhwal）**，适合已掌握 Pod/Deployment 基础、需为有状态应用落地持久化存储的运维与后端工程师。

## 一、最新动态（截至 2026-11）

存储子系统近期变化集中在动态供给、快照/数据保护、存储版本迁移三条线，均来自官方发布说明：

- **Kubernetes 主线为 v1.37（Garhwal，2026-08-26 发布，补丁 1.37.2）**。项目维护最近 **3 个次版本分支**（**1.37 / 1.36 / 1.35**），支持期约 14 个月；**1.34 已于 2026-10-27 EOL**，1.33 已于 2026-06-28 EOL。来源：[kubernetes.io/releases/patch-releases](https://kubernetes.io/releases/patch-releases/)
- **v1.37 存储相关**：**存储版本迁移 `storagemigration.k8s.io/v1`（KEP-4192）转 Stable**，用于不同版本间迁移存储运行时状态，降低升级风险。来源：[Kubernetes v1.37 发布说明](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
- **v1.36 存储相关**：**VolumeGroupSnapshot（KEP-3476）转 Stable**，支持多卷一致性快照；**OCI artifact/image 卷源（KEP-4639）GA**，模型、静态资源可作为 OCI 制品挂载；**可变 CSINode allocatable（KEP-4876）** 可运行时更新节点存储容量声明。来源：[Kubernetes v1.36 发布说明](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
- **v1.33 起 `gitRepo` 卷插件默认禁用**（需手动开启 `GitRepoVolumeDriver` 门控），v1.36 已**永久移除（KEP-5040）**，存量清单必须迁移。来源：[Kubernetes v1.36 发布说明](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
- **SELinux 卷标签变更**：未来版本（预计自 **v1.37 起默认启用 `SELinuxMount` 特性门控**）将改变卷的 SELinux 标签行为，**v1.36 是审计集群并修复或选择退出的合适版本**。来源：[K8s SELinux 卷标签变更说明](https://v1-36.docs.kubernetes.io/zh-cn/blog/page/4/)
- **备份/迁移工具 Velero 最新 1.18.x（1.18.4，2026-10-12）**，支持 CSI 快照、PV 备份/恢复与跨集群迁移。来源：[Velero 变更日志](https://images.minimus.io/images/velero/changelog/latest/versions/1.17.2/digest-history)

> [!note] 版本基线
> 本文示例与命令均对齐 v1.37 官方文档；涉及旧版本差异处会单独标注。升级前请回源核对，存储驱动（CSI）与云厂商托管集群的 PV 生命周期可能与上游存在差异。

## 二、基础概念

Kubernetes 存储的设计目标是：**把底层存储（本地盘、云盘、NAS、对象存储等）抽象成统一的声明式对象**，应用声明「要多少、怎么访问」，集群负责绑定与挂载。

| 对象 | 职责 | 一句话记忆 |
| --- | --- | --- |
| **PV（PersistentVolume）** | 集群级存储资源，由管理员或动态供给器创建，是真实存储的抽象 | 「集群里的一块存储」 |
| **PVC（PersistentVolumeClaim）** | 用户对存储的请求，声明容量与访问模式 | 「用户申请存储」 |
| **StorageClass** | 定义存储类别：供给器、回收策略、绑定模式、参数 | 「存储的模板/配方」 |
| **Volume** | Pod 内挂载点，可为 PVC、emptyDir、hostPath、ConfigMap、Secret 等 | 「Pod 上挂的卷」 |
| **CSI（Container Storage Interface）** | 容器存储接口，第三方存储驱动接入 K8s 的标准 | 「存储驱动的插座」 |

**核心心智模型**：PV 与 PVC 是「供给方」与「需求方」的匹配，通过**绑定**一一对应；PV 生命周期独立于 Pod，Pod 删除后 PVC/PV 默认仍保留（取决于回收策略）。

**访问模式（AccessModes）**：

- `RWO`（ReadWriteOnce）：可被单个节点以读写方式挂载，最常用。
- `ROX`（ReadOnlyMany）：多节点只读。
- `RWX`（ReadWriteMany）：多节点读写，依赖底层存储（如 NFS、CephFS）支持。
- `RWOP`（ReadWriteOncePod，v1.27+）：仅允许单个 Pod 挂载，比 RWO 更严格。

**卷类型**：除 PVC 外，`emptyDir`（临时缓存）、`hostPath`（节点本地目录，慎用）、`configMap`/`secret`、`nfs`、`csi` 等，`csi` 是现代动态供给的统一入口。

## 三、核心机制

**1. 静态供给（手工创建 PV）**：管理员先建 PV，用户再建 PVC，K8s 按容量与访问模式自动绑定。适合运维统一管理或使用不支持动态供给的驱动。

**2. 动态供给（推荐）**：用户只需创建 PVC 与 StorageClass，**外部供给器（external-provisioner）**监听到未绑定 PVC 后，自动调用 CSI 驱动创建后端存储、生成 PV 并完成绑定，是生产主流方式。

**3. StorageClass 关键字段**：

- `provisioner`：指定 CSI 驱动名（如 `csi.alibabacloud.com/csi-disk`、`ebs.csi.aws.com`）。
- `parameters`：传给驱动的参数（如磁盘类型、加密、拓扑）。
- `reclaimPolicy`：PVC 删除后对 PV 的处理，**`Retain`（保留数据）或 `Delete`（删除）**；`Recycle` 已弃用。
- `volumeBindingMode`：`Immediate`（立即绑定）或 **`WaitForFirstConsumer`（等调度器选节点后再绑定）**。

**4. 绑定模式与拓扑**：`WaitForFirstConsumer` 让 PVC 在 Pod 调度前不绑定，避免 PV 落在错误的节点/可用区；配合 CSI 拓扑感知（topology）可跨可用区创建存储，提升可用性。

**5. CSI 架构**：CSI 驱动以独立进程（sidecar：`csi-provisioner`、`csi-node-driver-registrar`）运行，对外暴露 `Identity`、`Controller`、`Node` 三组服务。Controller 负责创建/删除卷，Node 负责节点上的挂载/卸载。

**6. 卷扩容**：PVC 支持原地扩容（改 `spec.resources.requests.storage`），但要求 StorageClass `allowVolumeExpansion: true` 且底层存储支持；扩容只对已绑定 PVC 生效。

**7. 数据保护**：`VolumeSnapshot`/`VolumeSnapshotClass` 负责快照，**VolumeAttributesClass**（v1.34）切换性能等级，**VolumeGroupSnapshot**（v1.36）支持多卷一致性快照。

**8. StatefulSet 与存储**：StatefulSet 通过 `volumeClaimTemplates` 为每个副本创建独立、命名稳定的 PVC（如 `data-mysql-0`）；v1.32 起 **StatefulSet PVC 自动清理（KEP-1847）** 已 Stable。

## 四、实践步骤（含代码/命令示例）

### 4.1 创建 StorageClass（动态供给）

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-demo
provisioner: csi.example.com/demo
parameters:
  type: standard
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

> [!warning] 回收策略
> 生产环境若数据重要，**优先使用 `reclaimPolicy: Retain`**，避免误删 PVC 导致底层卷被连带删除、数据不可恢复。

### 4.2 创建 PVC 并挂载到 Pod

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: csi-demo
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
    spec:
      containers:
        - name: app
          image: nginx:1.27-alpine
          volumeMounts:
            - name: data
              mountPath: /var/www/html
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: demo-pvc
```

```bash
# 提交并观察绑定状态
kubectl apply -f storageclass.yaml -f pvc.yaml -f deployment.yaml

# PVC 状态：Pending → Bound 表示绑定成功
kubectl get pvc demo-pvc
kubectl get pv

# 确认 Pod 挂载点与卷信息
kubectl get pod -l app=demo-app -o wide
kubectl get pod -l app=demo-app -o jsonpath='{.items[0].spec.volumes[*].persistentVolumeClaim.claimName}'
```

### 4.3 静态供给（先建 PV，再建 PVC）

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-demo
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:                 # 仅用于演示；生产用真实存储驱动
    path: /mnt/data/demo
    type: DirectoryOrCreate
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc-static
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: manual   # 与 PV 的 storageClassName 一致才会绑定
```

```bash
kubectl apply -f pv.yaml -f pvc-static.yaml
kubectl get pv -o wide
kubectl get pvc demo-pvc-static
```

### 4.4 PVC 扩容

```bash
# 编辑 PVC 存储请求（需 allowVolumeExpansion: true）
kubectl patch pvc demo-pvc --type merge -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'

# 观察进度，文件系统扩展需在 Pod 内执行
kubectl get pvc demo-pvc
kubectl exec -it deploy/demo-app -- resize2fs /dev/<device>   # ext4
# xfs_growfs /var/www/html  # xfs 场景
```

### 4.5 备份与恢复（Velero）

```bash
# 备份指定 PVC
velero backup create demo-backup --include-namespaces demo-ns --selector app=demo-app

# 恢复
velero restore create demo-restore --from-backup demo-backup
```

## 五、最佳实践与常见坑

**最佳实践**

1. **默认动态供给 + `WaitForFirstConsumer`**：避免 PVC 提前绑到不合适节点或可用区，提升调度灵活性与容灾。
2. **容量与性能提前规划**：PVC 的 `storage` 按实际数据量留 20%~30% 余量，并按 IO 需求选择底层存储（本地 SSD、云盘、NAS）。
3. **重要数据用 `Retain`**：先备份或迁移，再人工删除 PV，防止误删即失。
4. **StatefulSet 用 `volumeClaimTemplates`**，为每个副本提供独立持久卷，避免多副本争用同一 RWO 卷。
5. **备份分层**：应用层 Velero（含 CSI 快照）、控制面 etcd 快照、配置层 GitOps，各管一段。
6. **敏感数据不落 PVC 明文**：口令等用 Secret + 外部密钥系统（KMS/Vault），不要写进卷内文件。

**常见坑**

- **PVC 长期 `Pending`**：多为无匹配 PV、StorageClass 不存在或无供给器、容量/访问模式不匹配。用 `kubectl describe pvc` 看事件，核对 `storageClassName`、`accessModes` 与容量。
- **`WaitForFirstConsumer` 下 Pod 一直 Pending**：PVC 未绑定会导致依赖它的 Pod 无法调度。检查存储驱动、节点拓扑与调度约束。
- **扩容不生效**：StorageClass 未开启 `allowVolumeExpansion`、底层卷不支持扩容，或文件系统未在容器内扩展。
- **`RWX` 期望落空**：底层存储不支持多节点写时，PVC 无法绑定或挂载失败，须先确认后端能力。
- **`hostPath` 与 `local` 的风险**：`hostPath` 不随节点漂移、有安全与一致性问题；`local` 卷需手动供给且无法跨节点，仅适合单副本或有状态专用节点。
- **删除 PVC 后数据丢失**：`Delete` 回收策略下，PVC 删除即删底层卷，**先备份、再删**。
- **gitRepo 卷**：v1.33 起默认禁用、v1.36 已永久移除，存量清单需迁移到 ConfigMap、Init 容器拉取或 CSI。

## 六、核心要点速查

1. PV 是集群级存储资源，PVC 是用户存储请求，二者通过绑定一一对应；Pod 通过 Volume 引用 PVC。
2. **动态供给**是生产主流：PVC + StorageClass → external-provisioner 调用 CSI 驱动 → 自动创建 PV 并绑定。
3. StorageClass 四要素：`provisioner`、`parameters`、`reclaimPolicy`、`volumeBindingMode`；`Retain` 保数据，`WaitForFirstConsumer` 保调度灵活性。
4. 访问模式决定挂载语义：`RWO`/`ROX`/`RWX`/`RWOP`，需与后端存储能力匹配。
5. **卷扩容**需 StorageClass `allowVolumeExpansion: true`，且要手动扩展文件系统才生效。
6. **快照**：`VolumeSnapshot`/`VolumeSnapshotClass`，v1.36 起 `VolumeGroupSnapshot` 支持多卷一致性快照。
7. StatefulSet 用 `volumeClaimTemplates` 为每个副本提供独立 PVC，是有状态应用标准做法。
8. **数据保护**：Velero（含 CSI 快照）做备份迁移，etcd 快照保控制面，GitOps 保配置。
9. 存储版本迁移随 v1.37 `storagemigration.k8s.io/v1` 转 Stable，升级涉存储运行时变化时优先评估。
10. 排查口诀：**先看 PVC/PV 状态（`get`/`describe`），再看事件，最后核对 StorageClass 与驱动参数**。

## 七、学习资源

1. [Kubernetes 官方文档：Persistent Volumes](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)
2. [Kubernetes 官方文档：Storage Classes](https://kubernetes.io/zh-cn/docs/concepts/storage/storage-classes/)
3. [Kubernetes 官方文档：Container Storage Interface (CSI)](https://kubernetes.io/zh-cn/docs/concepts/storage/plugins/)
4. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)
5. [Kubernetes 官方博客：Kubernetes v1.36 发布](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/)
6. [Kubernetes 官方博客：SELinux 卷标签变更说明](https://v1-36.docs.kubernetes.io/zh-cn/blog/page/4/)
7. [CSI 官方文档：Container Storage Interface](https://github.com/container-storage-interface/spec)
8. [Velero 官方文档](https://velero.io/docs/main/)
9. [kubernetes.io：Patch Releases（版本支持策略）](https://kubernetes.io/releases/patch-releases/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
