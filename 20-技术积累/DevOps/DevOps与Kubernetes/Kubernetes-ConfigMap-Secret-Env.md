---
title: Kubernetes ConfigMap/Secret/Env
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 云原生
  - 配置管理
  - 安全
aliases:
  - K8s ConfigMap/Secret/Env
  - Kubernetes 配置与密钥管理
source: 网络资料整理
---

# Kubernetes ConfigMap/Secret/Env

> [!summary] 摘要
> 本文聚焦 Kubernetes 中「配置如何进容器」这一基础但关键的知识点：**ConfigMap 存非敏感配置、Secret 存敏感数据、Env/EnvFrom/Volume 是注入方式**。内容涵盖三者的角色分工、注入机制与更新传播规则、可运行的创建与注入示例，以及 Secret 静态加密、外部密钥管理等生产级安全实践，并汇总了最易踩的坑与速查要点，适合作为 [[DevOps与Kubernetes-从入门到精通]] 中「配置与密钥管理」模块的落地参考。

## 一、最新动态（截至 2026-11）

截至 2026 年 11 月，与配置/密钥注入直接相关的版本事实如下（以官方发布说明为准）：

- **Kubernetes 最新稳定版本为 v1.37（代号 Garhwal）**，于 2026-08-26 发布，当前补丁为 1.37.2，官方文档站点默认版本即 v1.37。与配置注入直接相关的变更：**v1.37 起禁止静态 Pod（静态 Pod manifest 位于 kubelet 目录）引用 Secret/ConfigMap**，静态 Pod 必须改用其他方式获取配置。来源：[Kubernetes v1.37 Release](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)
- **支持策略**：项目维护最近 **3 个次版本分支**（当前为 1.37 / 1.36 / 1.35），支持期约 14 个月（12 个月标准 + 2 个月维护期）。**1.34 已于 2026-10-27 EOL**，1.33 已于 2026-06-28 EOL。来源：[Kubernetes 补丁发布](https://kubernetes.io/releases/patch-releases/) · [版本偏差策略](https://kubernetes.io/releases/version-skew-policy/)
- **外部 ServiceAccount 令牌签名（ExternalJWTSigner）**：v1.34 引入，签名可移出 `kube-apiserver` 进程外，是工作负载身份与令牌治理的演进方向。来源：[Kubernetes v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **`.kuberc`（kubectl 偏好）**：v1.34 起 Beta 默认启用，可配置 kubectl 默认选项与别名，**不含**集群凭据。来源：[Kubernetes v1.34 Release](https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/)
- **Secret 静态加密（at rest）**：通过 KMS provider（gRPC）与 etcd 加密实现；云厂商托管集群（如 AKS）提供托管 KMS 集成。来源：[Kubernetes: Using a KMS provider](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/kms-provider/) · [Azure AKS: KMS 数据静态加密概念](https://learn.microsoft.com/en-us/Azure/AKS/kms-data-encryption-concepts)

> [!note] 说明
> 以上为 2026-11-19 检索结果，版本与 EOL 日期可能随官方调整变化，升级与迁移前请回源核对。

## 二、基础概念

**ConfigMap（配置映射）**：以键值对形式存储**非机密**配置，如环境变量、配置文件、命令行参数。它不依赖 etcd 加密，任何有读取权限的主体都能拿到原文。单个 ConfigMap 建议控制在 **1 MiB 以内**（受 etcd 请求大小限制约束），避免把大文件塞进去。

**Secret（密钥）**：存储**敏感数据**，如数据库口令、云厂商 AK/SK、TLS 私钥、镜像仓库凭证。Secret 的 `data` 字段值是 **Base64 编码**，但**编码不等于加密**——`kubectl get secret -o yaml` 可直接看到解码后的内容。常见类型：`Opaque`（通用）、`kubernetes.io/dockerconfigjson`、`kubernetes.io/tls`、`kubernetes.io/service-account-token`。

**Env（环境变量）**：容器运行时可读取的变量，是配置进入容器的**通道**而非存储对象。Env 可通过三种方式产生：

| 注入方式 | 说明 | 是否随 ConfigMap/Secret 更新 |
| --- | --- | --- |
| `env` + `valueFrom` | 精确引用单个键（`configMapKeyRef` / `secretKeyRef`） | 否，需重启容器 |
| `envFrom` | 批量导入整个 ConfigMap/Secret 的所有键 | 否，需重启容器 |
| 卷挂载（Volume） | 将 ConfigMap/Secret 挂载为文件/目录 | 由 kubelet 周期性同步 |

**三者关系**：ConfigMap/Secret 负责「存」，Env/EnvFrom/Volume 负责「取」，Pod 的 `spec.containers` 是最终的消费端。

## 三、核心机制

**1. 注入由 kubelet 完成。** `kube-apiserver` 保存 ConfigMap/Secret 的声明，kubelet 通过 watch 获取并在创建容器时把配置投射（project）到 Pod 的文件系统或环境。一切交互都经过 apiserver，这是理解排障路径的前提。

**2. 环境变量是「启动时快照」。** `env` 与 `envFrom` 在容器进程启动时一次性解析。**修改 ConfigMap/Secret 后，已经运行的容器环境变量不会自动更新**，必须重启 Pod 才生效。这是最常见的误解。

**3. 卷挂载按周期同步。** 以卷方式挂载时，kubelet 周期性同步内容，并通过带时间戳的符号链接切换实现原子更新。更新传播存在延迟（取决于 kubelet 的同步周期与挂载类型，通常在分钟级，甚至更久）。**使用 `subPath` 挂载时不会收到更新**，因为 `subPath` 直接绑定具体文件而非目录，这是高频踩坑点。

**4. Secret 静态加密（at rest）**。默认情况下 Secret 在 etcd 中以明文存储（仅 Base64）。开启静态加密需提供 `EncryptionConfiguration`，通过 KMS provider（gRPC）由外部密钥系统完成加密，再写入 etcd。

**5. 大小与配额。** 单个 ConfigMap/Secret 数据量建议 ≤ 1 MiB；Secret 默认总大小同样受 etcd 限制。把巨型配置拆分为多个对象，或改用外部配置中心（Apollo、Nacos）+ 侧车注入。

## 四、实践步骤（含代码/命令示例）

### 4.1 创建 ConfigMap

```bash
# 方式一：直接以字面量创建
kubectl create configmap app-config \
  --from-literal=APP_ENV=prod \
  --from-literal=LOG_LEVEL=info

# 方式二：从文件创建
kubectl create configmap app-config \
  --from-file=application.properties \
  --from-file=config.yaml

# 方式三：生成清单而不落集群（推荐，便于纳入 Git 管理）
kubectl create configmap app-config \
  --from-literal=APP_ENV=prod \
  --dry-run=client -o yaml > configmap.yaml
```

### 4.2 创建 Secret

```bash
# 通用 Secret（Opaque）
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password='S3cr#t!Pass'

# 私有镜像仓库凭证
kubectl create secret docker-registry registry-secret \
  --docker-server=registry.example.com \
  --docker-username=robot \
  --docker-password='registry-token'

# TLS 证书
kubectl create secret tls app-tls --cert=tls.crt --key=tls.key
```

> [!warning]
> Secret 的 `data` 只是 Base64 编码，`kubectl get secret db-secret -o yaml` 能直接读出明文。**切勿把 Secret 当作加密存储使用。**

### 4.3 注入到 Pod（Deployment 示例）

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-demo
spec:
  replicas: 2
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
          # 1) 精确引用单个键
          env:
            - name: APP_ENV
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: APP_ENV
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
          # 2) 批量导入全部键
          envFrom:
            - configMapRef:
                name: app-config
          # 3) 卷挂载为文件
          volumeMounts:
            - name: app-config
              mountPath: /etc/app/config
            - name: app-secret
              mountPath: /etc/app/secret
      volumes:
        - name: app-config
          configMap:
            name: app-config
        - name: app-secret
          secret:
            secretName: db-secret
```

### 4.4 校验与验证

```bash
# 查看对象内容
kubectl get configmap app-config -o yaml
kubectl get secret db-secret -o jsonpath='{.data.password}' | base64 -d; echo

# 进入容器确认环境变量与挂载文件
kubectl exec -it deploy/web-demo -- env | grep -E 'APP_ENV|DB_PASSWORD'
kubectl exec -it deploy/web-demo -- cat /etc/app/config/APP_ENV
kubectl describe pod -l app=web-demo   # 查看 Events 与挂载状态
```

### 4.5 更新配置与生效

```bash
kubectl edit configmap app-config        # 修改后
kubectl rollout restart deployment/web-demo   # env/envFrom 场景需重启才生效
kubectl rollout status deployment/web-demo
```

### 4.6 生产级：Vault + External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: db-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: db-secret
    creationPolicy: Owner
  data:
    - secretKey: password
      remoteRef:
        key: secret/data/app/db
        property: password
```

由 ESO 定期从 Vault 拉取并写入集群内 Secret，应用仍按常规 `secretKeyRef` 引用，避免静态凭据。

## 五、最佳实践与常见坑

**最佳实践**

1. **配置与密钥分离**：非敏感配置用 ConfigMap，敏感数据一律用 Secret，不要把口令放进 ConfigMap。
2. **生产使用外部密钥系统**：以 KMS 启用 Secret 静态加密，或用 Vault + External Secrets Operator / CSI provider 动态注入，不要依赖 Base64。
3. **清单纳入 Git，避免手改集群**：用 `kubectl create ... --dry-run=client -o yaml` 生成清单入库，交由 GitOps（Argo CD/Flux）对账，禁止人工直接改集群。
4. **RBAC 最小权限**：按需授予对 ConfigMap/Secret 的 `get`/`list`/`watch`，避免使用宽泛的 `cluster-admin`；Secret 的读取面要尽量小。
5. **按环境分层**：用 Helm values 分层管理不同环境的配置，把环境差异从模板中剥离。
6. **镜像内不写凭据**：数据库口令、AK/SK 等不得硬编码进镜像或启动脚本。

**常见坑**

| 坑 | 原因 | 处理 |
| --- | --- | --- |
| 改了 ConfigMap 但环境变量没变 | 环境变量是启动时快照 | 重启 Pod（`rollout restart`）或改用卷挂载 |
| `subPath` 挂载的文件不更新 | `subPath` 绑定具体文件，不走符号链接切换 | 去掉 `subPath`，或改用完整目录挂载 + 应用热加载 |
| `Secret` 以为已加密 | 仅 Base64，etcd 默认明文 | 开启 KMS 静态加密或接 Vault/ESO |
| `ImagePullBackOff`（私有仓库） | 未配置 `imagePullSecrets` | 创建 `docker-registry` 类型 Secret 并挂到 Pod/SA |
| ConfigMap 过大失败 | 超过 etcd 请求大小限制 | 拆分对象或改用外部配置中心 |
| 键名非法 | 键需符合环境变量命名规范 | 避免 `/`、`.`、首字符为数字等非法字符 |

## 六、核心要点速查

1. **分工**：ConfigMap 存非敏感配置，Secret 存敏感数据，Env/EnvFrom/Volume 是注入通道。
2. **Secret 仅 Base64 编码，不是加密**；生产必须配合 KMS 静态加密或 Vault/ESO。
3. **`env`/`envFrom` 是启动时快照**，ConfigMap/Secret 变更不会热更新，需重启 Pod。
4. **卷挂载**由 kubelet 周期同步，更新有分钟级延迟；**`subPath` 挂载不随配置更新**。
5. 三种注入：`valueFrom`（单键精确）、`envFrom`（批量）、卷挂载（文件化配置）。
6. 单个 ConfigMap/Secret 建议 ≤ 1 MiB，超大配置改用配置中心。
7. Secret 类型有 Opaque、docker-registry、tls、service-account-token 等，按需创建。
8. 私有仓库需 `imagePullSecrets`；RBAC 对 Secret 按最小权限授予读取。
9. 静态 Pod 自 v1.37 起**禁止**引用 Secret/ConfigMap。
10. 清单用 `--dry-run=client -o yaml` 生成入库，交由 GitOps 对账，避免手改集群。
11. 截至 2026-11 主线版本为 **v1.37（2026-08-26）**，维护分支为 1.37/1.36/1.35，1.34 已 EOL。

## 七、学习资源

1. [Kubernetes 官方文档：ConfigMap](https://kubernetes.io/zh-cn/docs/concepts/configuration/configmap/)
2. [Kubernetes 官方文档：Secret](https://kubernetes.io/zh-cn/docs/concepts/configuration/secret/)
3. [Kubernetes 官方：使用 KMS provider 加密 Secret](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/kms-provider/)
4. [Kubernetes 官方博客：Kubernetes v1.37 发布（Garhwal）](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/)
5. [Kubernetes 官方：补丁发布与支持策略](https://kubernetes.io/releases/patch-releases/)
6. [Kubernetes 官方：版本偏差策略](https://kubernetes.io/releases/version-skew-policy/)
7. [External Secrets Operator 官方文档](https://external-secrets.io/latest/)
8. [HashiCorp Vault 官方文档](https://developer.hashicorp.com/vault/docs)
9. [Kubernetes 官方文档：将 Secret 作为环境变量或卷使用](https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/configure-pod-with-environment-variables/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
