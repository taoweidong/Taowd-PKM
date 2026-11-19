---
title: CI/CD 与 Jenkins
date: 2026-11-18
updated: 2026-11-18
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 流水线
  - 持续集成
  - 持续交付
aliases:
  - Jenkins 从入门到精通
  - CI/CD 与 Jenkins
source:
  - https://www.jenkins.io/changelog-stable/
  - https://www.jenkins.io/doc/book/pipeline/syntax/
---

# CI/CD 与 Jenkins

> [!summary] 摘要
> 本文系统梳理 CI/CD（持续集成 / 持续交付 / 持续部署）的流水线方法论，以及 Jenkins——这一插件生态最广的开源自动化服务器——从环境准备、第一支流水线、Jenkinsfile 语法、Shared Library 治理，到控制器/代理分布式架构、Kubernetes 生产部署、安全与选型的完整知识体系。适合刚接触 Jenkins 的运维与研发工程师，也适合需要落地生产级流水线、做技术选型的团队负责人。全文按「入门篇 → 进阶篇 → 精通篇」递进，并附版本动态、核心要点速查与官方资源清单。

## 一、最新动态（截至 2026-11）

以下仅记录可从官方渠道确认的版本与变更，涉及安全修复的条目建议尽快升级。

| 版本 | 更新点 | 来源 |
| --- | --- | --- |
| 2.580.2 (LTS) | 截至 2026-11 的最新 Jenkins LTS，2026-10-28 发布；含重要安全修复（security advisory）；测试平台覆盖 Linux、Windows，JDK 21、25。 | [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/) |
| 2.580.1 (LTS) | 2026-09-30 发布；升级 Winstone 8.1050.x、Eclipse Jetty 12.1.13、slf4j 2.0.19，延续自 2.568.3 起的增强（如 `jenkins.war` 体积缩减 40MB+、停用一批默认插件）；新增默认禁止 Object 字段反序列化、密码复杂度规则等安全强化。 | [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/) |
| 2.568.3 (LTS) | 2026-09-02 发布，含重要安全修复；升级 Winstone 8.1047.x / Jetty 12.1.12。 | [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/) |
| 2.555.1 (LTS) | 2026-04-15 发布，正式要求 Java 21 或 Java 25，不再支持 Java 17（依据「2+2+2 Java 支持计划」）；新增 API Token 过期、CSRF crumb 不再纳入客户端 IP 等安全增强。 | [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/) |
| 2.541.1 (LTS) | 2026-01-21 发布，新增 Java 25 支持、为 Jenkins UI 引入 Content-Security-Policy 保护、Linux RPM 仓库启用新 GPG 签名密钥；后续 2.541.2（2026-02-18）、2.541.3（2026-03-18）延续安全修复。 | [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/) |
| jenkins/jenkins:2.580.2-jdk21 | 官方 Docker 镜像当前 LTS 标签示例；`lts-jdk21` 等标签指向稳定 LTS，`latest` 对应每周版；官方镜像**不含 Docker CLI**，需自定义镜像或插件。 | [Jenkins Docker 安装文档](https://www.jenkins.io/doc/book/installing/docker/) |
| 2.545 (Weekly) | 2026-01-06 发布的每周版，重要增强为要求 Java 21 或更高版本，并引入 Java properties 遥测、提高最低支持的 `remoting.jar` 版本。 | [Jenkins 官方社区会议记录](https://community.jenkins.io/t/documentation-office-hours-january-8-2026/36053) |
| Blue Ocean（已弃用） | 自 2026 年 7 月起官方弃用，不再获得安全或功能更新；官方建议改用活跃维护的 Pipeline Graph View 插件与 Pipeline: Stage View 插件。 | [Jenkins Blue Ocean 文档](https://www.jenkins.io/doc/book/blueocean/) |

> [!warning] 升级前必读
> 2.555.1 起强制 Java 21 / Java 25，若生产环境仍停留在 Java 17，升级前必须先完成 JDK 迁移；同时 2.580.x 起默认禁止 Object 字段反序列化，可能影响依赖反序列化的旧插件，需在插件清单中提前排查兼容性。

## 二、入门篇

### 2.1 基础概念

CI/CD 是把「代码提交 → 构建 → 测试 → 发布 → 部署」这一过程自动化的工程实践，核心载体是**流水线（Pipeline）**。它由三个层次构成：

- **CI（持续集成，Continuous Integration）**：关注代码合并后的自动构建与测试，尽早发现集成问题，缩短反馈回路。
- **CD 之持续交付（Continuous Delivery）**：在 CI 基础上把交付物（镜像、包、制品）随时维持在「可发布」状态，发布动作仍可由人工触发。
- **CD 之持续部署（Continuous Deployment）**：在持续交付之上自动发布到生产，无需人工介入，对流水线成熟度与回滚能力要求最高。

Jenkins 的定位是这套流程的自动化服务器：用户以代码形式（Jenkinsfile）描述流水线，即 **Pipeline as Code**，从而让流水线可评审、可版本化、可复用、可审计。

> [!note] Jenkins 组件模型
> **控制器（Controller）** 是「大脑」，负责调度、配置、认证授权、任务调度与 Web 服务；**代理（Agent / Node）** 通过执行器（Executor）运行构建任务，二者通过 Remoting 通信，构成分布式构建。构建产物默认写入控制器文件系统，也可外包给 Nexus / Artifactory 等制品库。

### 2.2 环境准备

**运行环境要求**：安装 Jenkins 需要 Java。2.555.1 及以后要求 **Java 21 或 Java 25**（不再支持 Java 17）；Java 25 自 2.541.1 起获得支持。

**可选安装方式**：

- `jenkins.war`：最轻量，`java -jar jenkins.war` 直接启动，便于快速试用与升级。
- Linux RPM / DEB 包：适合纳入系统包管理与软件源版本。
- Windows MSI：适合 Windows 主机。
- 官方 Docker 镜像：`jenkins/jenkins`，LTS 标签如 `jenkins/jenkins:lts-jdk21`。
- Kubernetes：Helm Chart 或 Jenkins Operator。

**Docker 部署要点**（推荐起步方式）：

```bash
# 启动 Jenkins 容器：映射 Web 与入站 Agent 端口，挂载数据卷持久化 JENKINS_HOME
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  jenkins/jenkins:lts-jdk21
```

**硬件建议**：Docker 安装最低约 256MB 内存、1GB 磁盘（容器场景建议至少 10GB）；小团队推荐 **4GB+ 内存、50GB+ 磁盘**。

**首次初始化（安装向导）**：访问 `8080` 端口，从控制台或 `/var/jenkins_home/secrets/initialAdminPassword`（Docker 中用 `docker exec` 读取）获取初始管理员密码解锁 Jenkins，随后安装建议插件并创建第一个管理员用户。

> [!tip] 先想清楚再装
> 若只是跑通一个单分支的三段流水线，单节点 + 单 Agent 完全够用；等出现「多团队共用、资源隔离、弹性伸缩」需求时再引入分布式 Agent 与 Kubernetes，能显著降低初期维护成本。

### 2.3 第一个实践（含代码示例）

**步骤**：新建 Pipeline 任务 → 将 Jenkinsfile 以「Pipeline script from SCM」或 Multibranch Pipeline 方式加载 → 运行。

最简声明式 Jenkinsfile：

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Hello World'
            }
        }
    }
}
```

**Jenkinsfile 是流水线的代码载体，必须纳入版本控制**。声明式语法需安装 `Pipeline: Declarative Plugin`。推荐入门路径：先以单节点 / 单 Agent 跑通「构建 → 测试 → 部署」三段流水线，再逐步引入参数、凭据、多分支与并行。

带参数、环境变量与构建阶段的一个实用起点：

```groovy
pipeline {
    agent { label 'builder' }

    parameters {
        string(name: 'APP_VERSION', defaultValue: '1.0.0', description: '部署的应用版本号')
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '部署环境')
    }

    environment {
        // 凭据只按 ID 引用，不要在此硬编码明文
        REGISTRY = credentials('registry-credentials-id')
    }

    stages {
        stage('Build') {
            steps {
                sh "echo '构建版本 ${params.APP_VERSION} 到环境 ${params.ENV}'"
            }
        }
        stage('Test') {
            steps {
                sh './run-tests.sh'
            }
        }
        stage('Deploy') {
            when { expression { params.ENV != 'prod' } }
            steps {
                sh "./deploy.sh --env ${params.ENV} --version ${params.APP_VERSION}"
            }
        }
    }

    post {
        always {
            echo "流水线结束：${currentBuild.result}"
        }
        failure {
            emailext to: 'team@example.com', subject: '构建失败', body: "${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
```

## 三、进阶篇

### 3.1 核心机制

**1. 两种 Pipeline 语法。**

- **声明式（Declarative）**：结构严格、语法固定，适合常规交付流水线，可读性强、易于标准化。
- **脚本式（Scripted）**：基于 Groovy 的通用 DSL，灵活度高，适合复杂条件与动态逻辑。

二者底层是**同一套 Pipeline 子系统**，均为可持久化的 Pipeline as Code，并都支持 Shared Library。

**2. 声明式主要指令。** `agent`、`stages`、`stage`、`steps`、`post`、`environment`、`options`、`parameters`、`when`、`triggers`、`tools`、`input`、`script`，以及并行结构 `parallel` 与矩阵结构 `matrix`。

**3. agent 的多种形态。**

| 形态 | 说明 |
| --- | --- |
| `any` | 任一可用代理 |
| `none` | 不分配代理，需在 `stage` 级指定 |
| `label` | 按标签匹配指定代理 |
| `node` | 指定节点，支持 `customWorkspace` |
| `docker` | 动态拉起容器执行 |
| `dockerfile` | 从仓库中的 Dockerfile 构建容器 |
| `kubernetes` | 在集群 Pod 内运行 |

`agent` 还可支持 `registryUrl` / `registryCredentialsId` 等参数，便于拉取私有镜像。

**4. post 条件块。** `always`、`changed`、`fixed`、`regression`、`aborted`、`failure`、`success`、`unstable`、`unsuccessful`、`cleanup`，用于按结束状态执行清理与通知等动作。

**5. 常用 options。**

- 全局级：`buildDiscarder`、`timeout`、`retry`、`timestamps`、`disableConcurrentBuilds`、`skipDefaultCheckout`、`newContainerPerStage`、`preserveStashes`、`parallelsAlwaysFailFast`、`disableResume` 等。
- **stage 级 options 仅支持** `retry`、`timeout`、`timestamps`、`skipDefaultCheckout` 等，其余指令需放在顶层。

**6. 凭据机制。** 凭据由 **Credentials Binding 插件**提供，类型包括 Secret Text、用户名 + 密码、Secret File、SSH 私钥、PKCS#12 证书、Docker Host 证书认证。在 Pipeline 中通过 `credentials('id')` 绑定。

> [!warning] 凭据安全红线
> 凭据以控制器 ID 加密存储在控制器上，流水线中**只按凭据 ID 引用**，切勿硬编码明文。可设置 Global / System / 用户级作用域，限制凭据与流水线的访问范围，降低泄露与在控制器间复制的风险。

### 3.2 最佳实践

**Shared Library 目录结构**：

- `src/`：Groovy 类，进 classpath。
- `vars/`：暴露为全局变量的脚本，**文件名即变量名**。
- `resources/`：外部库可用 `libraryResource` 加载的资源文件。

**使用方式**：

```groovy
// 静态导入，可带版本号
@Library('my-lib@1.0') _

// 运行时动态加载
library identifier: 'my-lib@1.0', retriever: $(checkout scm)
```

被标记为「Load implicitly」的库可被所有流水线直接使用。

**库的信任模型**：

- **trusted**：可调用 Java / Groovy / Jenkins 内部 API，不受 Groovy 沙箱限制，需 `Overall/RunScripts` 权限配置。
- **untrusted**：在沙箱内运行，仅 `Overall/Manage` 权限可配置。

**库开发要点**：

- 库类需实现 `Serializable` 才能保存状态。
- 全局变量应**保持无状态**（仅作函数集合），这是生产级库治理的强制要求。
- 库变更可用 **Replay** 在构建中试运行；也可通过 `@Library('lib@pull/<PR>/head')` 在构建中测试 PR 变更。
- 统一版本策略，通过分支 / 标签 / 固定 commit 控制版本，配合 CI 校验库变更并强制「全局变量无状态」。

**Docker / Kubernetes 集成**：

- Docker 插件提供 `docker` 与 `dockerfile` agent；常配 `docker:dind` 提供 Docker 守护进程。
- Kubernetes 插件通过 `podTemplate` 或 `yamlFile` 定义 Pod 模板，按标签动态创建**一次性 Pod 作为 Agent**，实现弹性伸缩。旧的 `containerTemplate` 已被 yaml 方式取代。

**插件治理**：插件是 Jenkins 的核心扩展方式，但版本升级常引发兼容性问题。应只保留必要插件、控制更新节奏，并关注插件健康评分与安全公告。

### 3.3 常见问题与排查

- **控制器重启后脚本式流水线报错**：脚本式流水线需可序列化，某些 Groovy 闭包用法（如 `collection.each` 的部分写法）受限，应将复杂逻辑下沉到 Shared Library。
- **声明式 `pipeline` 块代码体量超限**：声明式存在代码体量上限，脚本式无此限制；体量过大时应重构为库。
- **stage 级 agent 的 `timeout` 行为**：Pod / 容器的供给时间会**计入** stage 超时，给动态供给预留时间，否则会出现「还没开始跑就超时」。
- **构建卡在排队**：检查执行器数量、全局并发上限与代理标签是否匹配，避免 CPU / 内存 / IO 被打满。
- **凭据绑定失败**：确认凭据类型与作用域，确认调用方对凭据拥有读取权限。
- **插件升级后流水线异常**：回滚插件版本，对照插件健康评分与安全公告定位兼容性问题，建立版本锁定机制。

## 四、精通篇

### 4.1 架构与设计

**控制器与代理架构**：控制器同时是 Web 服务器与调度中枢，负责配置、认证授权、任务调度与状态展示；代理 / 节点通过执行器执行任务，构建产物默认写入控制器文件系统，亦可外包给 Nexus / Artifactory 等制品库。

**Agent 接入方式**：

- 入站 Agent 经 TCP（默认 **50000** 端口）以 JNLP 连接。
- 也可使用 **SSH**、**WebSocket**。WebSocket Agent **无需映射 50000 端口**，在受限网络下更友好。
- 建议统一各节点时钟，并按属性对 Agent 分类，以匹配不同构建负载（如编译型 / 测试型 / 部署型）。

**声明式与脚本式的取舍**：声明式用于标准化、可读性优先的流水线；脚本式用于复杂条件与动态逻辑。**复杂逻辑应下沉到 Shared Library**，避免在声明式里堆砌大块 `script`，否则既丧失可读性，也突破体量上限。

> [!tip] 架构设计原则
> 把「通用构建、测试、部署」封装为高层 DSL（如 `buildPlugin`），让业务流水线只描述「做什么」，把「怎么做」沉淀在库里。这是 Jenkins 项目从能用走向可维护的关键一步。

### 4.2 生产实践

**配置即代码（CasC）**：使用 Configuration as Code 插件，将 Jenkins 全局配置、凭据、插件、Job 定义以代码形式管理，配合 Jenkins Operator 在 Kubernetes 上实现声明式部署与**可恢复的种子 Job**。

**Kubernetes 生产部署**：Jenkins Operator（Kubernetes Native Operator）与官方 Helm Chart 是主流方案，支持镜像 / 插件 / 配置的声明式管理、备份恢复、种子 Job 与 Pipeline。注意**自定义 CA 证书需用 Init 容器准备信任库**，否则控制器与集群之间会因证书不被信任而通信失败。

**JVM 与资源优化**：

- 将 `-Xms` 与 `-Xmx` **设为相同值**，减少堆抖动；堆建议占物理内存约 **50%**，并预留系统内存。
- 控制**全局 / 节点并发构建数与执行器数量**，避免 CPU、内存、IO 被打满。

**性能优化方向**：官方持续优化类缓存、插件 ClassLoader 内存、队列维护、构建日志端点内存占用、大日志 / 产物渲染的异步化，并新增 `/health` 健康检查端点。实践中应定期清理旧构建与制品，配置构建丢弃策略（`buildDiscarder`）。

**高可用与稳定性**：

- 控制器前部署负载均衡（HAProxy / Nginx）做健康检查与故障摘除。
- 控制器数据持久化并定期备份。
- **Jenkins 原生不提供简单多活 HA**，通常需借助插件或外部存储实现，规划时不要假设「双活自动切换」。

**安全纵深**：启用 UI 的 Content-Security-Policy（2.541.1 起引入）、CSRF crumb、密码复杂度规则；默认禁止 Object 字段反序列化、校验集合反序列化类型；API Token 支持过期时间；敏感逻辑受 Script Security Plugin 沙箱约束。

**RBAC 与最小权限**：用 Matrix-based / Role-based 授权策略精确分配权限（如 `Credentials > Create`、`Overall/Manage`、`Overall/RunScripts`），配合用户与文件夹级作用域限制凭据与流水线访问。

### 4.3 生态与前沿

**插件生态与成熟度**：Jenkins 拥有覆盖面最广的插件生态（社区文章称 **1800+ 插件**，具体数量以插件更新站点为准），可集成几乎全部工具链；但插件质量与兼容性参差，需建立**插件准入与版本锁定机制**。

**生态动向**：Blue Ocean 自 2026 年 7 月**官方弃用**，官方推荐以 **Pipeline Graph View**、**Pipeline: Stage View** 与 Pipeline 语法片段生成器替代，新项目应**避免依赖 Blue Ocean**。

**选型对比**：

| 维度 | Jenkins | GitLab CI | GitHub Actions |
| --- | --- | --- | --- |
| 部署方式 | 自托管（war / Docker / K8s） | 自托管或 SaaS，配 Runner | 托管为主，支持自托管 Runner |
| 流水线表达 | Groovy 流水线（Jenkinsfile） | `.gitlab-ci.yml` | YAML 工作流 |
| 优势 | 插件生态最广、定制性最强 | 代码与 CI 一体化、YAML 易用、内置制品与安全扫描 | YAML 工作流、托管 / 自托管 Runner、丰富 Marketplace 生态 |
| 代价 | 维护成本与资源占用较高 | 生态与扩展性受平台约束 | 与 GitHub 托管场景绑定较深 |

> [!note] 选型结论
> 三者并无绝对优劣。**Jenkins 重定制与生态，GitLab CI 重一体化与易用，GitHub Actions 重 YAML 与托管生态**。应按团队技术栈、运维能力与现有平台底座权衡：已有 K8s 与平台化能力、需要深度定制，选 Jenkins；已用 GitLab 全家桶，选 GitLab CI；以 GitHub 为代码主阵地，选 GitHub Actions。

**迁移考量**：GitHub 官方提供从 Jenkins 迁移到 GitHub Actions 的指南，二者在工作流结构上存在对应关系——Jenkins `stage` ↔ GitHub `job`、Jenkins `steps` ↔ `job steps`、`parallel` ↔ `jobs.<id>.strategy.max-parallel`、`matrix` ↔ `jobs.<id>.strategy.matrix`，迁移时可逐项映射。但需注意**语法差异（Groovy vs YAML）**与**运行方式差异（自托管 vs 托管 / 自托管）**，迁移后需重新验证凭据、制品与部署链路。

## 五、核心要点速查

1. CI/CD 以**流水线（Pipeline）**为核心，把「提交 → 构建 → 测试 → 发布 → 部署」自动化。
2. Jenkins 采用 **Controller（调度 / 配置 / 安全）+ Agent（执行构建）** 的分布式架构，通过 Remoting 通信。
3. 截至 2026-11，最新 Jenkins LTS 为 **2.580.2**（2026-10-28 发布）。
4. **2.555.1（2026-04-15）起要求 Java 21 或 Java 25**，正式弃用 Java 17。
5. **2.541.1** 起支持 Java 25，并为 Jenkins UI 引入 Content-Security-Policy 保护。
6. 2.555.1 起新增 API Token 过期、CSRF crumb 不纳入客户端 IP 等安全能力；2.580.x 起默认禁止 Object 字段反序列化、新增密码复杂度规则。
7. 官方 Docker 镜像用 `lts-jdk21` 标签指向稳定 LTS，**镜像不含 Docker CLI**。
8. Jenkinsfile 有**声明式**与**脚本式**两种语法，共用同一 Pipeline 子系统，均支持 Shared Library。
9. 声明式核心指令：`agent`、`stages`、`stage`、`steps`、`post`、`environment`、`options`、`parameters`、`when`、`parallel`、`matrix`、`script`。
10. `agent` 支持 `any` / `none` / `label` / `node` / `docker` / `dockerfile` / `kubernetes` 等多种执行环境。
11. Shared Library 目录约定：`src/`（类）、`vars/`（全局变量）、`resources/`（资源）。
12. 使用库：`@Library('lib@版本') _` 静态导入，或 `library` step 运行时动态加载。
13. 信任模型：**trusted** 库可调用任意 API（需 `Overall/RunScripts`），**untrusted** 在 Groovy 沙箱内运行。
14. 凭据由 **Credentials Binding 插件**提供，支持 Secret Text、用户名密码、Secret File、SSH 私钥、证书、Docker Host 认证。
15. 凭据以控制器 ID 加密存储，流水线中**只按 ID 引用**，避免明文硬编码。
16. Kubernetes 集成通过 `podTemplate` / `yamlFile` 定义 Pod 模板，按标签动态创建一次性 Agent。
17. Docker 集成用 `docker` / `dockerfile` agent，常配 `docker:dind` 提供守护进程。
18. **Blue Ocean 自 2026-07 起弃用**，由 Pipeline Graph View / Stage View 承接。
19. 插件生态是 Jenkins 的核心优势，但需治理版本兼容性与安全更新，建立版本锁定机制。
20. 选型：Jenkins 重定制与生态，GitLab CI 重一体化与易用，GitHub Actions 重 YAML 与托管生态。

## 六、学习资源

以下均为官方或权威来源：

1. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
2. [Pipeline Syntax（Jenkins 官方用户手册·流水线语法）](https://www.jenkins.io/doc/book/pipeline/syntax/)
3. [Extending with Shared Libraries（Jenkins 官方·共享库）](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
4. [Docker（Jenkins 官方用户手册·Docker 安装）](https://www.jenkins.io/doc/book/installing/docker/)
5. [Using credentials（Jenkins 官方用户手册·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
6. [Credentials（Jenkins 官方用户手册·凭据安全）](https://www.jenkins.io/doc/book/security/credentials/)
7. [Managing Nodes（Jenkins 官方用户手册·节点管理）](https://www.jenkins.io/doc/book/managing/nodes/)
8. [Blue Ocean（Jenkins 官方用户手册·弃用公告）](https://www.jenkins.io/doc/book/blueocean/)
9. [Kubernetes Plugin for Jenkins（Jenkins 插件站）](https://plugins.jenkins.io/kubernetes/)
10. [Jenkins Operator 官方文档（Kubernetes 原生 Operator）](https://jenkinsci.github.io/kubernetes-operator/)
11. [Migrating from Jenkins to GitHub Actions（GitHub 官方文档）](https://docs.github.com/en/actions/migrating-to-github-actions/manually-migrating-to-github-actions/migrating-from-jenkins-to-github-actions)
12. [GitLab Runner 官方文档](https://docs.gitlab.com/runner/)
13. [Jenkins War Packages（官方 WAR 包仓库）](https://mirrors.jenkins.io/war-stable/)
14. [Documentation office hours - January 8, 2026（Jenkins 官方社区会议记录）](https://community.jenkins.io/t/documentation-office-hours-january-8-2026/36053)

## 七、关联笔记

- [[DevOps]]
- [[Jenkins流水线配置]]
- [[Jenkins资源高效利用方案]]
- [[Dockerfile编写指南]]
- [[Kubernetes部署实践]]
- [[DevOps与Kubernetes-从入门到精通]]

## 八、变更记录

- 2026-11-18 首次创建
- 2026-11-18 审校：修正 2.545（Weekly）发布日期为 2026-01-06；将「默认禁止 Object 字段反序列化」「密码复杂度规则」的归属从 2.555.1 改为 2.580.x（官方 changelog 将其列入 2.580.1 的 Notable changes since 2.568.3），并同步更新升级警告与核心要点表述。
