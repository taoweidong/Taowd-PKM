---
title: Jenkins Agent 与分布式构建
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 分布式构建
  - 流水线
aliases:
  - Jenkins 分布式构建
  - Jenkins Agent
source: 网络资料整理
---

# Jenkins Agent 与分布式构建

> [!摘要] 摘要
> 本文聚焦 Jenkins 的 **Controller + Agent** 分布式构建模型：先讲清 Agent 的角色、入站/出站两种接入方式与标签调度机制，再拆解执行器、Remoting、入站密钥等核心机制，并给出 SSH、Docker、Kubernetes 三类动态 Agent 的完整可运行示例。随后归纳标签规划、密钥保护、资源治理等最佳实践与常见坑。适合已掌握 Pipeline 基础、需要把 Jenkins 从单节点扩展到多 Agent、多集群生产环境的运维与研发工程师。

## 一、最新动态（截至 2026-11）

- **版本基线**：生产推荐 **LTS 2.580.x，当前为 2.580.2（2026-10-28 发布）**；Weekly 最新为 **2.591（2026-11-16 发布）**，该版本起**默认启用内容安全策略（CSP）**。
- **Java 硬约束**：**2.555.1 起要求 Java 21 或 Java 25，Java 17 已弃用**，控制器与所有 Agent 的 JDK 版本需统一。
- **Agent 默认连接方向**：**Outbound（出站）自 2.492 起成为默认**，Agent 通过 Remoting 反向连接控制器，可显著减少控制器端口暴露面。
- **最低 Remoting 版本**：**2.555.x 起最低支持 `remoting.jar` 版本 `3176.v207ec082a_8c0`**，旧 Agent 必须先升级 Remoting 才能接入。
- **安全公告**：**CVE-2026-84651（2026-09-02）**——更新代理配置的 REST API 与 CLI 端点存在授权绕过，可跨代理覆盖配置并获取入站代理密钥，影响 2.579 及更早 / LTS 2.568.2 及更早，**修复于 LTS 2.568.3 与 Weekly 2.580**，任何涉及 Agent 配置的实例都应尽快升级。
- **Kubernetes 集成**：Kubernetes 插件最新 **1.35（活跃，EOL 2027-02-28）**；`containerTemplate` 已**弃用**，官方推荐改用 **`yamlFile`/YAML** 定义 Pod 模板。JKO（Jenkins Kubernetes Operator）**v0.10.0-beta1（2026-11）** 新增 Istio/Linkerd 服务网格与云身份注入保护，但为 beta 状态，生产使用需谨慎。

## 二、基础概念

**1. Controller 与 Agent 的职责划分。** Jenkins 采用经典的 **Controller（控制器）+ Agent（代理/节点）** 架构。Controller 是「大脑」，承担调度、队列、配置、认证授权与 Web 服务；Agent 负责实际执行构建任务。构建任务被分配到某个 Agent 上运行，从而构成**分布式构建**：控制器本身不必承担所有编译、测试压力，可按需横向扩展执行节点。

**2. 两种接入方式。**

- **Inbound（入站）**：传统模式，Agent 主动连接 Controller，典型载体是 **JNLP** 与 **WebSocket**。Controller 需暴露 Agent 入站端口（默认 **50000**），网络策略要求控制器到 Agent 方向通常也需放通。
- **Outbound（出站）**：Agent 通过 **Remoting** 反向连接控制器，**2.492 起为默认**。只需保证 Agent 能访问控制器的 **8080**，无需把控制器端口暴露给所有 Agent，安全与网络拓扑上更友好。

**3. 入站与出站对比。**

| 维度 | Inbound（入站） | Outbound（出站） |
| --- | --- | --- |
| 连接方向 | Agent 主动连 Controller | Agent 反向连 Controller（Remoting） |
| 典型载体 | JNLP、WebSocket | Remoting |
| 端口要求 | 控制器需放通 50000 | 只需 Agent 能访问控制器 8080 |
| 默认状态 | 传统方式 | **2.492 起默认** |
| 适用场景 | 控制器可被 Agent 访问的传统机房 | 控制器在防火墙内、Agent 分布广的云环境 |

**4. 动态 Agent。** Agent 不一定常驻，可由云（Docker、Kubernetes、SSH 等）在任务到达时**按需动态创建**，构建结束即销毁，实现弹性伸缩。这类 Agent 对应 Pipeline 中 `docker`、`kubernetes` 等 `agent` 形态，是中大型团队控制资源成本与隔离构建环境的主要手段。

**5. 关键术语。** `label`（节点标签，用于任务与 Agent 匹配）、`executor`（执行器，单个 Agent 上的并发构建槽位）、`Remoting`（控制器与 Agent 之间的通信框架）、`nodeUsageMode`（节点使用方式，如 `exclusive` / `preferential`）。

## 三、核心机制

**1. 标签调度。** 声明式流水线通过 `agent { label 'xxx' }` 声明需求，Jenkins 从可用 Agent 中挑选带该标签的节点，找不到则任务进入**排队**。标签应按职责划分，例如 `linux-builder`、`java21`、`windows-test`，避免所有任务都挤到同一节点。

**2. 执行器与并发。** 每个 Agent 的 `executors` 决定并发构建数。资源治理的核心是：控制器全局并发上限 × 各 Agent 执行器数 = 系统总并发，需与物理 CPU、内存、IO 匹配，否则会出现构建排队或节点 OOM。

**3. Remoting 通信。** Agent 与控制器通过 Remoting 交换构建任务、工作区与日志。Agent 端必须运行与控制器兼容的 `remoting.jar`；**2.555.x 起最低支持 `3176.v207ec082a_8c0`**，版本不匹配会导致 Agent 离线或任务失败。

**4. 入站密钥。** 入站 Agent 接入时使用**入站代理密钥（inbound agent secret）**校验身份。**CVE-2026-84651** 表明更新代理配置的 REST API / CLI 曾存在授权绕过，攻击者可跨代理覆盖配置并窃取该密钥，因此必须升级到修复版本，并避免将该密钥暴露给不受信任用户。

**5. 动态供给流程。** 以 Kubernetes 为例：任务需要 Agent → 插件按 `podTemplate`/`yamlFile` 创建一次性 Pod → Pod 内启动 Remoting 连接控制器 → 执行构建 → 任务结束按 `podRetention`/`idleMinutes` 回收。供给时间会**计入 stage 超时**，需为动态拉起预留时间。

**6. Agent 状态与离线原因。** Agent 在控制器上呈现**在线/离线**两种状态，离线时任务无法分配。常见原因：Remoting 版本不兼容、Agent 进程退出或重启、网络链路中断、执行器被占满或被手动断开。可通过节点页面查看离线原因与重连时间，静态 Agent 建议统一各节点时钟并配置自动重启，动态 Agent 则依赖 Pod 模板的健康配置。

## 四、实践步骤（含代码/命令示例）

**1. 静态 Agent：SSH / JNLP 接入。** 在 `Manage Jenkins > Manage Nodes and Computers > New Node` 新建节点，选择「Launch via SSH」或「Launch via inbound Java WebSocket」并配置凭据。Agent 端启动命令（出站方式，推荐）：

```bash
# 出站：Agent 反向连接控制器，无需映射控制器 50000 端口
java -jar remoting.jar -handler http://jenkins.example.com:8080/

# 入站（JNLP）：需控制器放通 50000 端口，密钥由节点页面的 slave-agent.jnlp 提供
java -jar remoting.jar -jnlpUrl http://jenkins.example.com:8080/computer/agent-builder/slave-agent.jnlp
```

**2. Docker Agent。** 使用官方 Agent 镜像启动常驻或一次性 Agent：

```bash
docker run -d --name jenkins-agent \
  -e JENKINS_URL=http://jenkins.example.com:8080/ \
  -e JENKINS_AGENT_WORKDIR=/home/jenkins/agent/workspace \
  jenkins/agent:lts-jdk21
```

流水线中直接以容器作为执行环境：

```groovy
pipeline {
    agent {
        docker {
            image 'maven:3.9-eclipse-temurin-21'
            args '-v $HOME/.m2:/root/.m2'
        }
    }
    stages {
        stage('Build') {
            steps { sh 'mvn -B clean package' }
        }
    }
}
```

**3. Kubernetes 动态 Agent。** 用 `yamlFile` 定义 Pod 模板（`containerTemplate` 已弃用），构建时按模板动态拉起 Pod。

```yaml
# agent-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    agent: jnlp
spec:
  containers:
    - name: jdk
      image: maven:3.9-eclipse-temurin-21
      command: ['cat']
      tty: true
      workingDir: /home/jenkins/agent/workspace
      volumeMounts:
        - name: workspace
          mountPath: /home/jenkins/agent/workspace
  volumes:
    - name: workspace
      persistentVolumeClaim:
        claimName: jenkins-agent-workspace
```

```groovy
pipeline {
    agent {
        kubernetes {
            label 'jnlp'
            yamlFile 'agent-pod.yaml'
            idleMinutes 10      // 空闲回收
            instanceCap 10      // Pod 上限，防止失控
        }
    }
    stages {
        stage('Build') {
            steps {
                container('jdk') { sh 'mvn -B clean package' }
            }
        }
    }
}
```

**4. 标签匹配与阶段级执行。** 用 `agent none` 降低调度开销，在需要时于 stage 级指定容器：

```groovy
pipeline {
    agent none
    stages {
        stage('Compile') {
            agent { label 'java21-builder' }
            steps { sh 'mvn -B compile' }
        }
        stage('Test') {
            agent { docker { image 'maven:3.9-eclipse-temurin-21' } }
            steps { sh 'mvn -B test' }
        }
    }
}
```

**5. 接入验证与排查。** 节点创建后，在控制器 `Manage Nodes and Computers` 查看其状态与日志；用一个最简流水线验证标签匹配与执行器可用性：

```groovy
pipeline {
    agent { label 'java21-builder' }
    stages {
        stage('Verify') {
            steps {
                echo "Agent: ${env.NODE_NAME}, Executors: ${env.NODE_NUMBER}"
                sh 'java -version'
            }
        }
    }
}
```

若任务长时间排队，依次检查：标签是否命中、执行器是否被占满、Agent 是否在线、Remoting 版本是否匹配、控制器与 Agent 之间的网络与端口是否放通。

## 五、最佳实践与常见坑

- **标签即契约**：标签要按「工具链 + JDK + 平台」维度规划，并在流水线中显式声明 `label`，不要依赖 `any` 导致构建随机落到不合适的节点。
- **入站密钥最小授权**：妥善保管入站代理密钥，升级到修复 **CVE-2026-84651** 的版本（LTS 2.568.3 / 2.580 及以上），不要将 Agent 管理权限下放给不受信任用户。
- **Remoting 版本对齐**：升级控制器后检查各 Agent 的 `remoting.jar` 版本，**2.555.x 起需不低于 `3176.v207ec082a_8c0`**，否则 Agent 会离线。
- **动态供给预留超时**：Pod/容器拉取与镜像拉取时间会**计入 stage 超时**，给动态 Agent 预留 `timeout`，避免「还没开始跑就超时」。
- **并发与资源匹配**：控制全局并发与执行器数量，动态 Agent 必须设置 `instanceCap` / `idleMinutes`，防止拉起过多 Pod 打满集群资源。
- **凭据不硬编码**：Agent 相关凭据通过 `credentials('id')` 或 `withCredentials` 使用，日志中敏感值以 `****` 掩码，但掩码仅降低意外泄露风险，不能替代权限隔离。
- **动静结合**：编译型长任务用静态 Agent（常驻、执行器稳定）；突发、隔离性要求高的任务用动态 Agent（用完即毁）。通过 `nodeUsageMode` 与标签区分，避免互相抢占。
- **统一时钟**：构建时间戳、日志与依赖缓存对时间敏感，静态 Agent 应统一时区与时钟，否则会出现难以定位的超时与缓存异常。
- **常见坑**：构建卡在排队（查标签、执行器、并发上限）；Agent 反复离线（Remoting 版本或网络不通）；Kubernetes Pod 里命令为 `cat`/`tty` 未配好导致 Agent 启动即退出；镜像使用可变标签导致 Agent 行为漂移。

## 六、核心要点速查

1. Jenkins 采用 **Controller（调度/配置）+ Agent（执行构建）** 架构，构建分布在 Agent 上即**分布式构建**。
2. Agent 接入分 **Inbound**（JNLP/WebSocket，Agent 主动连控制器）与 **Outbound**（Remoting 反向连接，**2.492 起默认**）。
3. 关键端口：UI 默认 **8080**，入站 Agent 默认 **50000**；**WebSocket Agent 无需映射 50000**。
4. 调度靠 **`label` 标签**匹配，找不到匹配节点则任务**排队**。
5. 并发由 **`executors`（执行器数）** 决定，需与物理资源匹配。
6. Agent 端 `remoting.jar` **2.555.x 起最低支持 `3176.v207ec082a_8c0`**。
7. 入站 Agent 使用**入站代理密钥**；**CVE-2026-84651** 揭示的授权绕过需升级到 LTS 2.568.3 / 2.580 及以上修复。
8. 动态 Agent 由云按需创建，支持 **Docker / Kubernetes / SSH** 等，构建后即回收。
9. Kubernetes 用 **`podTemplate`/`yamlFile`** 定义 Pod，**`containerTemplate` 已弃用**。
10. 动态供给时间计入 stage 超时，务必预留并设置 `instanceCap`、`idleMinutes`。

## 七、学习资源

1. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
2. [Jenkins 官方手册（Using Jenkins）](https://www.jenkins.io/doc/book/using/)
3. [Managing Nodes（Jenkins 官方·节点管理）](https://www.jenkins.io/doc/book/managing/nodes/)
4. [Kubernetes Pipeline Steps（Jenkins 官方·Kubernetes 步骤）](https://www.jenkins.io/doc/pipeline/steps/kubernetes/)
5. [Kubernetes Plugin for Jenkins（Jenkins 插件站）](https://plugins.jenkins.io/kubernetes/)
6. [Jenkins Security Advisories（官方安全公告）](https://www.jenkins.io/security/advisories/)
7. [Jenkins Remoting（Agent 通信框架）](https://github.com/jenkinsci/remoting)
8. [Jenkins Docker 镜像仓库](https://github.com/jenkinsci/docker)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
