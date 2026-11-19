---
title: Jenkins 与 Kubernetes 集成（JKO）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - Kubernetes
  - JKO
  - CI/CD
  - 云原生
  - 流水线
aliases:
  - Jenkins Kubernetes Operator
  - Jenkins Kubernetes 集成
  - JKO
source: 网络资料整理
---

# Jenkins 与 Kubernetes 集成（JKO）

> [!摘要] 摘要
> 本文讲解 Jenkins 如何与 Kubernetes 集成：核心是 **Kubernetes 插件**通过 `kubernetes {}` / `podTemplate {}` 与 Pod 模板（推荐 YAML 的 `yamlFile`）按需动态创建一次性 Agent Pod，构建结束后自动销毁，实现弹性伸缩与资源隔离；在 Kubernetes 原生层面，**Jenkins Kubernetes Operator（JKO）** 以 Operator 方式声明式管理 Jenkins 实例，配合 JCasC 完成配置即代码与安全加固。内容涵盖基础概念、核心机制、可直接运行的 Jenkinsfile / JCasC / Helm 示例、最佳实践与常见坑。适合已在或准备在 K8s 上运行 Jenkins、希望把构建执行环境做成云原生弹性能力的运维与研发工程师。

## 一、最新动态（截至 2026-11）

- **Kubernetes 插件版本：最新 1.35（活跃，EOL 2027-02-28）**，**1.34 已 EOL**。2026 年 10 月 Jenkins 官方「Plugin of the Month」专题即 Kubernetes 插件，说明该集成是当前 Jenkins 生态的推广重点。[Kubernetes 插件页](https://plugins.jenkins.io/kubernetes/)
- **JKO（Jenkins Kubernetes Operator）v0.10.0-beta1（2026-11）** 新增 **Istio / Linkerd 服务网格支持**，以及**云身份注入保护**（AWS IRSA、EKS Pod Identity、Azure Workload Identity、Google ADC）。注意该版本为 **beta（测试性质）**，生产引入需谨慎评估。[JKO 仓库](https://github.com/jenkinsci/kubernetes-operator)
- **Jenkins 基线**：截至 2026-11，最新 **LTS 2.580.2**（2026-10-28，含重要安全修复）；最新 **Weekly 2.591**（2026-11-16，**默认启用内容安全策略 CSP**，该能力自 2.539 引入）。[LTS Changelog](https://www.jenkins.io/changelog-stable/)、[Weekly 2.591 Changelog](https://www.jenkins.io/changelog/2.591/)
- **Java 硬约束**：Jenkins 2.555.1 及以后要求 **Java 21 或 Java 25**，Java 17 不再支持。Kubernetes 上的 Agent 镜像与控制器镜像都应基于 JDK 21+ 构建，例如官方镜像 `jenkins/jenkins:2.580.2-jdk21`。[Jenkins Docker 安装文档](https://www.jenkins.io/doc/book/installing/docker/)
- **安全公告**：2026 年 Jenkins 共发布 **10 次**安全公告；其中 **CVE-2026-84651（2026-09-02）** 涉及更新代理配置的 REST API 与 CLI 端点存在授权绕过，可跨代理覆盖配置并获取**入站代理密钥**，影响 2.579 及更早 / LTS 2.568.2 及更早，修复于 **LTS 2.568.3 / Weekly 2.580**。K8s 动态 Agent 同样依赖入站密钥机制，需尽快升级。[Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)

> [!info] 版本锚点
> 本文以 **LTS 2.580.x（当前 2.580.2）** 为生产基线，以 **Weekly 2.591** 为最新特性参考。Jenkins 每周发布，版本号随时变化，落地前请以官方仓库为准。

## 二、基础概念

**1. 为什么需要集成。** 传统 Jenkins Agent 是长期驻留的虚拟机或容器，存在资源浪费、环境不一致、扩容慢的问题。Kubernetes 提供 Pod 级别的秒级调度与资源配额，把「构建执行环境」做成按需创建、用完即销毁的临时工作负载，是 Jenkins 云原生化的关键一步。

**2. 两个层次的集成，别混淆：**

| 层次 | 载体 | 作用 | 面向对象 |
| --- | --- | --- | --- |
| 构建执行层 | **Kubernetes 插件**（`kubernetes` agent 形态） | 在集群中按标签动态创建**一次性 Agent Pod**，构建结束销毁 | 每次构建的执行环境 |
| 实例管理层 | **Jenkins Kubernetes Operator（JKO）** | 以 Operator + CRD 声明式管理 Jenkins 控制器实例，配合 JCasC、备份、种子 Job | Jenkins 控制器本身的生命周期 |

**3. 关键术语**

- **Pod 模板（pod template）**：描述 Agent Pod 的 YAML/配置，是动态 Agent 的「图纸」。
- **`kubernetes {}` / `podTemplate {}`**：Pipeline 与步骤中定义、引用 Pod 模板的指令。
- **`yamlFile`**：把 Pod 模板放在仓库里的 YAML 文件中，为官方推荐的写法。
- **`container()`**：在已创建的 Agent Pod 内，指定进入某个容器执行步骤。
- **`imagePullSecrets`**：Pod 拉取私有镜像所需的镜像拉取凭据引用。
- **JCasC（Configuration as Code）**：用 YAML 管理 Jenkins 全局配置（含云、凭据、插件、Job）。

## 三、核心机制

**1. 动态 Agent 的生命周期。** 触发构建 → Kubernetes 插件向集群申请 Pod → Pod 就绪后连接控制器 → 容器内执行各 `stage` / `steps` → 构建结束 → Pod 按 `podRetention` / `idleMinutes` 策略保留或销毁。整个过程对用户透明，构建之间相互隔离。

**2. `agent` 的 `kubernetes` 形态。** 声明式流水线中可用 `agent { kubernetes { ... } }` 直接指定在集群 Pod 内运行，参数包括 `label`、`yamlFile`、`namespace`、`nodeSelector`、`nodeUsageMode`、`defaultContainer`、`imagePullSecrets`、`idleMinutes`、`podRetention`、`instanceCap` 等。

**3. `containerTemplate` 已弃用，改用 YAML。** 早期的 `containerTemplate` 写法已被官方标记为**弃用**，现在应使用 **YAML 格式**（`yamlFile`）定义完整 Pod 模板，可表达多容器、卷、安全上下文等更完整能力。这是从旧版本迁移时最容易踩的变更。

**4. 多容器的执行模型。** Pod 模板里可以定义多个容器（如 `jdk` + `docker`），Pipeline 用 `container('容器名') { ... }` 指定在哪个容器中执行步骤，等价于 `withDockerContainer` 的思路。

**5. JKO 的声明式管理。** JKO 通过 `Jenkins` CRD 描述控制器实例（镜像、ServiceAccount、配置、备份策略等），由 Operator 持续调和实际状态。它支持 JCasC 作为配置入口，并提供开箱即用的安全加固，适合在 K8s 上规模化管理多个 Jenkins 实例。

**6. 扩展能力。** **Kubernetes Ephemeral Container 插件**可在 Agent Pod 内运行临时容器执行步骤（用法类似 `withDockerContainer`），适用于没有 Docker 守护进程的集群，避免为跑一个命令再拉起一套容器环境。

## 四、实践步骤（含代码/命令示例）

### 4.1 前置条件

- 一个可用的 Kubernetes 集群，Controller 已具备创建 Pod 的权限（ServiceAccount + RBAC）。
- Jenkins 上安装 **Kubernetes 插件 1.35**（通过 `Manage Jenkins > Manage Plugins`）。
- 控制器与集群之间网络可达（推荐用 ClusterIP + `tunnel` 或 exec 方式）。
- 镜像使用 **JDK 21** 基线，避免 Java 版本不匹配。

### 4.2 用 JCasC 配置云（推荐）

在 `jenkins-casc.yaml` 中定义 Kubernetes 云与 Pod 模板：

```yaml
jenkins:
  clouds:
    kubernetes:
      name: kubernetes
      url: https://kubernetes.default.svc
      namespace: default
      tunnel: jenkins-agent
      containerCapStr: 8192m
      podTemplates:
        - yaml: |
            apiVersion: v1
            kind: Pod
            metadata:
              labels:
                jenkins-agent: 'true'
            spec:
              restartPolicy: Never
              containers:
                - name: jdk
                  image: eclipse-temurin:21-jdk
                  command: ['cat']
                  tty: true
                  resources:
                    requests: { cpu: '500m', memory: 1Gi }
                    limits: { cpu: '2', memory: 4Gi }
```

加载配置（在「Configure System」中启用 JCasC，或通过插件把该文件挂载到 `$JENKINS_HOME/casc.yaml`）：

```bash
kubectl apply -f jenkins-casc.yaml
kubectl rollout status deploy/jenkins -n jenkins
```

### 4.3 独立 Pod 模板文件（官方推荐写法）

`agent-pod.yaml`（放入 SCM 仓库）：

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins-agent: 'true'
spec:
  restartPolicy: Never
  nodeSelector:
    kubernetes.io/os: linux
  containers:
    - name: jdk
      image: eclipse-temurin:21-jdk
      command: ['cat']
      tty: true
    - name: docker
      image: docker:27-dind
      command: ['cat']
      tty: true
      securityContext:
        privileged: true
```

### 4.4 Jenkinsfile：声明式使用 Kubernetes Agent

```groovy
pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'
            yamlFile 'agent-pod.yaml'
            defaultContainer 'jdk'
            imagePullSecrets 'registry-secret'
            idleMinutes 30          // 空闲 30 分钟后回收
            instanceCap 100         // 限制同时创建的 Pod 上限
            nodeSelector 'kubernetes.io/os: linux'
        }
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Build') {
            steps {
                container('jdk') {
                    sh 'mvn -B clean package -DskipTests'
                }
            }
        }
        stage('Test') {
            steps {
                container('jdk') {
                    sh 'mvn -B test'
                }
                junit '**/build/test-reports/*.xml'
            }
        }
        stage('Docker Build') {
            steps {
                container('docker') {
                    sh 'docker build -t registry.example.com/app:${env.BUILD_TAG} .'
                }
            }
        }
    }

    post {
        always {
            echo "构建结束：${currentBuild.result}"
        }
        failure {
            echo '构建失败，检查 Pod 模板与镜像拉取权限'
        }
    }
}
```

### 4.5 脚本式：用 podTemplate 直接定义模板

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                podTemplate(label: 'builder', yamlFile: 'agent-pod.yaml') {
                    container('jdk') {
                        sh 'mvn -B clean package'
                    }
                }
            }
        }
    }
}
```

### 4.6 用 JKO 部署 Jenkins（Helm）

```bash
# 添加官方 Chart 仓库并安装 Operator
helm repo add jenkinsci https://charts.jenkins.io
helm repo update
helm install jenkins-operator jenkinsci/jenkins-operator \
  --namespace jenkins --create-namespace
```

对应的 `Jenkins` CRD（声明式实例定义，配置内容以官方仓库为准）：

```yaml
apiVersion: jenkins.io/v1alpha2
kind: Jenkins
metadata:
  name: jenkins
  namespace: jenkins
spec:
  controller:
    containers:
      - name: jenkins
        image: jenkins/jenkins:lts-jdk21
    serviceAccountName: jenkins
  configurationAsCode:
    codeAsConfig: |
      jenkins:
        clouds:
          kubernetes:
            name: kubernetes
            url: https://kubernetes.default.svc
```

## 五、最佳实践与常见坑

**最佳实践**

- **模板即代码**：Pod 模板写成仓库中的 YAML（`yamlFile`），纳入版本控制、可评审、可复用，避免在 UI 里堆配置。
- **收敛资源边界**：设置 `idleMinutes`、`instanceCap`、`podRetention`，防止空闲 Pod 堆积与并发失控。
- **镜像拉取凭据走凭据体系**：私有仓库用 `imagePullSecrets` 或 `registryCredentialsId` 引用 Jenkins 凭据，不要明文写进 YAML。
- **用 `container()` 明确执行容器**：多容器 Pod 里，步骤必须显式指定容器，否则会落到 `defaultContainer` 或报错。
- **控制 stage 超时**：Pod 的**供给时间计入 stage 超时**，`timeout` 要为拉镜像、建 Pod 预留余量，否则会出现「还没开始跑就超时」。
- **最小权限**：给 Jenkins ServiceAccount 仅授予创建/管理自身 Agent Pod 的 RBAC 权限，不要直接绑 `cluster-admin`。
- **统一 JDK 基线**：控制器与 Agent 镜像统一 Java 21+，避免 `containerTemplate` 时代常见的 Java 17 兼容问题。
- **安全基线**：升级到含 CVE-2026-84651 修复的版本（LTS 2.568.3 / 2.580 及以上），保护入站代理密钥。

**常见坑**

- **`containerTemplate` 已弃用**：老教程里的写法会告警或失效，务必迁移到 `yamlFile` 的完整 Pod YAML。
- **私有镜像拉取失败**：多为 `imagePullSecrets` 未配置或凭据作用域不对，先在控制器侧验证镜像拉取权限。
- **构建卡在排队/Pod 创建**：检查执行器数量、`instanceCap` 上限、标签是否匹配，以及集群资源配额。
- **升级后插件缺失**：2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件，从 2.356 之前升级或检测到面向旧版本的插件时，需通过插件管理器**手动安装**。
- **自定义 CA 证书问题**：JKO 部署时自定义 CA 需用 Init 容器准备信任库，否则控制器与集群通信会因证书不被信任而失败。
- **不要假设多活 HA**：Jenkins 核心为单 Controller，**无原生多 Controller 高可用**，JKO 提供的是声明式管理与备份恢复，并非双活自动切换；高可用需依赖外部编排 + 持久化存储 + 负载均衡。
- **JKO 版本状态**：`v0.10.0-beta1` 为 beta，生产使用需谨慎验证。

## 六、核心要点速查

1. Kubernetes 集成分两层：**Kubernetes 插件**管构建执行环境，**JKO** 管 Jenkins 实例生命周期。
2. 截至 2026-11，**Kubernetes 插件最新 1.35**（活跃，EOL 2027-02-28），**1.34 已 EOL**。
3. **JKO v0.10.0-beta1（2026-11）** 新增 Istio/Linkerd 服务网格支持与云身份注入保护，属 beta 版本。
4. 动态 Agent 的载体是**一次性 Agent Pod**，用 `kubernetes {}` / `podTemplate {}` 定义，构建后按策略回收。
5. **`containerTemplate` 已弃用**，官方推荐 **YAML（`yamlFile`）** 定义 Pod 模板。
6. Pod 模板关键字段：`label`、`namespace`、`nodeSelector`、`nodeUsageMode`、`defaultContainer`、`imagePullSecrets`、`idleMinutes`、`podRetention`、`instanceCap`。
7. 多容器 Pod 中用 **`container('名称') { ... }`** 指定执行容器。
8. **Kubernetes Ephemeral Container 插件**可在 Pod 内运行临时容器，替代 Docker 守护进程场景。
9. JKO 用 `Jenkins` CRD + JCasC 声明式管理实例，提供开箱安全加固，但**不提供原生多活 HA**。
10. Jenkins **2.555.1 起要求 Java 21 / Java 25**，Agent 与控制器镜像应统一 JDK 21+。
11. 需尽快升级以修复 **CVE-2026-84651**（入站代理密钥授权绕过）。
12. 2.580.x 移除默认捆绑插件（JUnit、Mailer、Matrix 等），升级后可能需手动补齐。

## 七、学习资源

1. [Kubernetes Plugin for Jenkins（Jenkins 插件站，含版本与 EOL 信息）](https://plugins.jenkins.io/kubernetes/)
2. [Kubernetes Pipeline Steps（Jenkins 官方 Pipeline 步骤文档）](https://www.jenkins.io/doc/pipeline/steps/kubernetes/)
3. [Jenkins Kubernetes Operator（JKO 官方仓库）](https://github.com/jenkinsci/kubernetes-operator)
4. [Jenkins Operator 官方文档](https://jenkinsci.github.io/kubernetes-operator/)
5. [Plugin of the Month – Kubernetes Plugin（2026-10，Jenkins 官方博客）](https://www.jenkins.io/blog/2026/10/18/plugin_month_october/)
6. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
7. [Jenkins Weekly 2.591 Changelog](https://www.jenkins.io/changelog/2.591/)
8. [Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)
9. [Using credentials（Jenkins 官方·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
10. [Jenkins Docker 安装文档](https://www.jenkins.io/doc/book/installing/docker/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]
- [[DevOps与Kubernetes-从入门到精通]]
- [[Kubernetes核心概念与架构]]
- [[Kubernetes部署策略（滚动-蓝绿-金丝雀）]]
- [[容器镜像与仓库管理]]
- [[Kubernetes安全（RBAC-网络策略）]]

## 九、变更记录

- 2026-11-19：首次创建。
