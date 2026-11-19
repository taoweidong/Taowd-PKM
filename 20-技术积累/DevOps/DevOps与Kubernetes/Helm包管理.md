---
title: Helm包管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - Helm
  - 云原生
  - 包管理
aliases:
  - Helm
  - Helm Chart
source: 网络资料整理
---

# Helm包管理

> [!summary] 摘要
> Helm 是 Kubernetes 的应用打包、分发与生命周期管理标准，用 **Chart（图表）** 把一套多资源的 Kubernetes 清单抽象为可复用、可参数化、可版本化的「应用包」，把「部署一组 YAML」变成「安装一个 release」。本文围绕 Helm 的概念模型、渲染与状态管理机制、从创建到发布回滚的完整实践，以及从 Helm 3 迁移到 Helm 4 的要点展开，适合在掌握 Kubernetes 基础后作为应用交付层的进阶阅读。

## 一、最新动态（截至 2026-11）

> [!warning] 重要：Helm 3 已进入生命周期末期
> 写作与使用前务必确认版本。截至 2026-11，**Helm 4 已是当前主版本**，Helm 3 应尽快迁移。

- **Helm 4 正式发布**：**v4.0.0 于 2025-11-12**（KubeCon + CloudNativeCon 期间）发布，是 6 年来首个大版本。
- **Helm 3 的 EOL 时间线**：最后一次（受限）功能版为 **2026-09-09**，仅更新 Kubernetes 客户端库以兼容新版本 K8s；**安全补丁延长至 2027-02-10**，此后彻底停止更新。该时间线与版本号以官方仓库为准。
- **Helm 4 关键新特性**：插件系统重做，可选 **WebAssembly（WASM）插件运行时**；**post-renderer 改为插件**；**server-side apply 成为新 release 的默认 apply 方式**；基于 **kstatus** 的资源状态追踪；支持**多文档 values**；**SDK API 稳定化**；依赖解析更快并引入基于内容的缓存。
- **破坏性变更（升级必看）**：`--atomic` 更名为 `--rollback-on-failure`；`--force` 更名为 `--force-replace`（旧旗标仍可用但会告警）；`helm registry login` **仅接受域名**。
- 官方说明 Helm 4 可管理既有的 Helm 3 release，无需重建，但旗标重命名与 post-renderer 插件化仍可能影响既有流水线，需按官方迁移清单验证。

来源：[Helm 3 End of Life](https://v3.helm.sh/blog/helm-v3-end-of-life/) · [Helm 4 Released](https://github.com/helm/helm-www/blob/main/blog/2025-11-17-helm-4-released/index.md)

## 二、基础概念

| 概念 | 含义 |
| --- | --- |
| **Chart** | Helm 的应用包，一个目录，内含清单模板与元数据，描述「要部署什么」 |
| **Release** | Chart 在集群中安装后的一份运行实例，可有名称、可升级/回滚/卸载 |
| **Repository** | Chart 的仓库，分为 HTTP 仓库与 **OCI registry** 两类分发渠道 |
| **values** | 可覆盖的参数，由用户在安装/升级时注入，模板据此渲染 |
| **templates** | 用 Go 模板语法编写的 Kubernetes 资源 YAML，渲染后才是最终清单 |
| **Hook** | 在 release 生命周期特定节点执行的模板（如安装前/升级后跑 Job） |
| **Library Chart** | 只提供模板片段、自身不产生资源的库 chart，供其他 chart 复用 |

一个标准 Chart 目录结构：

```text
my-app/
├── Chart.yaml          # 元数据：名称、版本、app 版本、依赖
├── values.yaml         # 默认参数
├── values-prod.yaml    # 环境覆盖值（常按环境拆分）
├── charts/             # 依赖的子 chart 压缩包
├── templates/          # 资源模板
│   ├── _helpers.tpl    # 公共模板片段（命名、标签）
│   ├── deployment.yaml
│   ├── service.yaml
│   └── NOTE.txt        # 安装后的提示信息
└── README.md
```

## 三、核心机制

**1. 渲染流程（template → manifest → apply）**

Helm 并非直接执行 YAML，而是先做**模板渲染**：把 `values.yaml` + `-f` 传入的覆盖值合并，套用 `templates/` 中的 Go 模板，产出最终清单，再提交给集群。这个「参数化渲染」是 Helm 复用能力的根本。

**2. Helm 3/4 的架构演进（去掉 Tiller）**

Helm 2 依赖集群内的 **Tiller**（一个负责 release 管理的控制器）并拥有集群级权限，是历史安全短板。**Helm 3 起彻底移除 Tiller**，改为**客户端直接调用 kube-apiserver**，release 元数据以 Secret 形式存放在集群中。Helm 4 延续该架构，并进一步把 apply 与插件体系做深。

**3. apply 方式与状态追踪（Helm 4）**

- **server-side apply 默认化**：Helm 4 为**新 release** 默认采用 server-side apply，能更好保留字段所有权、减少冲突；升级已存在 release 时沿用其原有 apply 方式，可用 `--server-side=false` 覆盖。
- **kstatus 状态追踪**：通过 kstatus 判断资源是否「已应用、健康」，改进升级时的等待逻辑，避免盲目轮询。

**4. 插件与 post-renderer**

Helm 4 将 **post-renderer 也做成插件**，允许在渲染后、提交前对清单做二次加工（如注入监控注解、做策略修补），配合可选的 WASM 插件运行时实现可扩展的工具链。

**5. OCI 仓库**

Helm 4 默认走 **OCI registry** 工作流，chart 可像镜像一样用 `oci://` 地址拉取；`helm registry login` 仅接受域名，要求仓库地址不带协议前缀。

## 四、实践步骤（含代码/命令示例）

**1. 安装与升级 Helm**

```bash
# 查看当前版本（确认是否为 Helm 4）
helm version

# 官方安装脚本（示例，具体以官方文档为准）
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4 | bash

# 升级到最新
helm upgrade --install helm https://get.helm.sh/helm-v4.x.x-linux-amd64.tar.gz
```

**2. 创建与校验 Chart**

```bash
helm create my-app           # 生成标准目录结构
helm lint my-app             # 校验 chart 合法性
helm dependency update my-app # 拉取 Chart.yaml 中声明的依赖
```

`Chart.yaml` 示例：

```yaml
apiVersion: v2
name: my-app
description: A sample Helm chart
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
  - name: common
    version: "1.2.0"
    repository: "oci://registry.example.com/charts"
```

**3. 本地渲染（不落集群，推荐进 CI）**

```bash
# 渲染最终清单，便于审查变更
helm template my-app ./my-app -f values-prod.yaml

# 查看与上一版的差异（可配合 helm diff 插件）
helm diff upgrade my-app ./my-app -f values-prod.yaml
```

**4. 安装、升级、回滚**

```bash
# 安装（命名空间 + 覆盖值）
helm install my-app ./my-app \
  --namespace my-ns --create-namespace \
  -f values-prod.yaml

# 升级
helm upgrade my-app ./my-app \
  --namespace my-ns \
  -f values-prod.yaml \
  --install --timeout 10m

# 失败自动回滚（Helm 4 使用 --rollback-on-failure，旧旗标为 --atomic）
helm upgrade my-app ./my-app -f values-prod.yaml --rollback-on-failure

# 回滚到指定版本
helm rollback my-app 1

# 查看 release 状态与历史
helm list -n my-ns
helm history my-app

# 卸载
helm uninstall my-app -n my-ns
```

**5. 使用 OCI 仓库**

```bash
# 登录（仅接受域名）
helm registry login registry.example.com --username=user --password=***

# 推送与拉取
helm push ./my-app oci://registry.example.com/charts
helm pull oci://registry.example.com/charts/my-app --version 0.1.0
```

**6. 用 Hook 做安装前后动作**

在模板中用注解声明 hook，例如升级后跑数据库迁移 Job：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include \"my-app.fullname\" . }}-migrate"
  annotations:
    # 仅在升级完成后执行一次
    "helm.sh/hook": post-upgrade
    "helm.sh/hook-weight": "5"
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: my-app:1.0.0
          command: ["/app/migrate"]
```

## 五、最佳实践与常见坑

**最佳实践**

- **values 分层**：默认值写在 `values.yaml`，环境差异用 `-f values-prod.yaml` 叠加，不要把环境参数写死进模板。
- **`_helpers.tpl` 统一命名与标签**：抽出 `fullname`、`selectorLabels`、`labels`，保证资源标签一致，便于按标签筛选与治理。
- **lint/template/diff 进 CI**：渲染前先校验、比对变更，避免把错误清单直接发布到集群。
- **镜像 tag 用摘要（digest）**：生产环境避免使用可变标签，防止同 tag 覆盖。
- **Library Chart 复用**：公共的 Pod 注解、监控配置、资源模板沉淀为库 chart，减少重复维护。
- **先在非生产验证迁移**：升级到 Helm 4 前，在测试环境完整跑一遍既有 chart，再更新 CI/CD 脚本中的重命名旗标、迁移 post-renderer。

**常见坑**

| 现象 / 场景 | 原因与处理 |
| --- | --- |
| 升级到 Helm 4 后 `--atomic` 报错 | 已更名为 `--rollback-on-failure`，同步替换脚本中的旗标 |
| `--force` 行为与预期不符 | 已更名为 `--force-replace`，旧旗标仍可用但会告警 |
| `helm registry login` 报地址非法 | 只接受域名，去掉 `https://`、`http://` 等前缀 |
| 升级卡住、状态不健康 | 确认是否为 server-side apply 相关差异，必要时 `--server-side=false` 验证 |
| release 信息找不到 | Helm 3/4 的 release 记录以 Secret 存储，确认命名空间与 `helm list -n` 正确 |
| 模板渲染结果与预期不符 | 用 `helm template` 本地渲染核对，逐层检查 values 覆盖与模板逻辑 |
| Helm 3 无后续功能更新 | 功能版止于 2026-09-09，应规划迁移到 Helm 4，避免临近 2027-02-10 安全补丁终止后被动升级 |

## 六、核心要点速查

1. Helm = Kubernetes 应用包管理标准，核心抽象是 **Chart / Release / Repository / values**。
2. **Chart** 是目录包：`Chart.yaml`（元数据与依赖）+ `values.yaml`（默认值）+ `templates/`（模板）+ `charts/`（依赖）。
3. **渲染机制**：values 合并 → Go 模板渲染 → 清单 → apply 到集群。
4. **Helm 3 起无 Tiller**，客户端直连 kube-apiserver，release 记录存为集群内 Secret。
5. **Helm 4（v4.0.0，2025-11-12）**：WASM 插件、post-renderer 插件化、**server-side apply 为新 release 默认**、kstatus 状态追踪、多文档 values、稳定 SDK API。
6. **Helm 3 EOL**：最后功能版 2026-09-09，安全补丁至 2027-02-10，应尽快迁移 Helm 4。
7. 破坏性变更：`--atomic`→`--rollback-on-failure`、`--force`→`--force-replace`、`helm registry login` 仅接受域名。
8. 高频命令：`helm create/lint/template/dependency/install/upgrade/rollback/history/list/uninstall`，加 `-f` 覆盖值。
9. 生产建议：values 分层、`_helpers.tpl` 统一标签、lint/template/diff 纳入 CI、镜像用摘要、先在非生产验证迁移。

## 七、学习资源

1. [Helm 官方博客：Helm 4 Released](https://github.com/helm/helm-www/blob/main/blog/2025-11-17-helm-4-released/index.md)
2. [Helm 官方博客：Helm 3 End of Life（支持期时间线）](https://v3.helm.sh/blog/helm-v3-end-of-life/)
3. [Helm 官方文档：Charts（Chart 结构与约定）](https://helm.sh/docs/topics/charts/)
4. [Helm 官方文档：Using Helm（安装、升级、release 管理）](https://helm.sh/docs/helm/)
5. [Helm 官方文档：Chart Template 指南（模板函数与管道）](https://helm.sh/docs/charts/templates/)
6. [Helm 官方文档：Chart 最佳实践（自定义资源命名与标签）](https://helm.sh/docs/charts/best_practices/)
7. [Kubernetes 官方文档：版本支持与补丁发布](https://kubernetes.io/releases/patch-releases/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
