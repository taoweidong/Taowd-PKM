---
title: Jenkinsfile 编写实践
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - Jenkinsfile
  - Pipeline
  - Pipeline-as-Code
  - CI/CD
aliases:
  - Jenkinsfile
  - Jenkins 流水线文件
source:
  - 网络资料整理
---

# Jenkinsfile 编写实践

> [!摘要] 摘要
> Jenkinsfile 是 Jenkins 流水线的源码文件，用 Groovy 写成、纳入版本控制，即 **Pipeline as Code**。本文聚焦「怎么写好一个 Jenkinsfile」：先厘清声明式与脚本式两种语法的取舍，再拆解 `agent` / `stages` / `options` / `parameters` / `post` 等核心指令，随后给出从「最简流水线」到「参数化、凭据化、阶段级容器、Kubernetes Agent、共享库复用」的完整实践路径，并汇总常见坑与安全红线。适合已经了解 Jenkins 基本概念、准备把流水线代码化落地的研发与运维工程师；本主题的完整体系定位见 [[CI-CD与Jenkins-从入门到精通]]。

## 一、最新动态（截至 2026-11）

Jenkins 采用 **Weekly（每周）+ LTS（长期支持）** 双发布线，写 Jenkinsfile 前需先对齐运行环境的版本口径：

- **Weekly 最新：2.591（2026-11-16 发布）**。主打变更为**默认启用内容安全策略（CSP）**，该能力自 2.539 引入、2.591 起默认生效，对 Jenkinsfile 本身无直接影响，但涉及 Jenkins UI 与脚本执行环境的默认安全姿态。
- **LTS 最新：2.580.2（2026-10-28 发布）**，为安全修复版本；**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25 发布**。
- **下一个 LTS 基线定于 2027-01-06**，新 Manage Jenkins UI 将随该基线正式进入 LTS。
- **Java 硬约束**：**Jenkins 2.555.1 及以后要求 Java 21 或 Java 25，Java 17 不再支持**。Jenkinsfile 里所有构建步骤最终都在 JVM 上执行，若运行环境仍是 Java 17，流水线会直接启动失败。
- **2.580.x 移除了一批默认捆绑插件**（如 JUnit、Mailer、Matrix 等），`jenkins.war` 体积缩减 40 MB+。**从 2.356 之前升级，或检测到面向旧版本的插件时，需在插件管理器中手动补齐**。这一点直接影响 Jenkinsfile：若流水线里用了 `junit` 步骤发布测试报告，插件缺失时该步骤将无法解析。
- **安全公告**：2026 年全年共发布 10 次安全公告。其中 **CVE-2026-84651（2026-09-02）** 涉及更新代理配置的 REST API / CLI 端点授权绕过，修复于 LTS 2.568.3 / Weekly 2.580，若 Jenkinsfile 依赖动态 Agent，建议尽快升级。
- **Kubernetes 插件最新 1.35（活跃，EOL 2027-02-28）**；`containerTemplate` 已弃用，官方推荐改用 **YAML 模板（`yamlFile`）** 定义 Pod。
- **官方 Docker 镜像**：LTS 线为 `jenkins/jenkins:2.580.2-lts`（jdk21 / jdk25），官方文档示例使用 `FROM jenkins/jenkins:2.580.2-jdk21`。

> 版本号与日期均以调研文件为准；如写作时间晚于 2026-11，请以官方仓库最新版本重新核对。

## 二、基础概念

**Jenkinsfile 是什么**：一份用 **Groovy** 语言编写的 Pipeline 源码文件，把构建流程描述为代码。它随源码一起纳入 SCM（Git / SVN 等），从而让流水线具备**可评审、可版本化、可复用、可审计**的特性，这就是官方所强调的 **Pipeline as Code**。

**与自由风格任务的区别**：传统 Freestyle Job 通过 Web UI 或 XML 配置，适合单任务、步骤简单、无需版本化的场景；Jenkinsfile 是代码化方案，适合复杂、多阶段、需要统一规范与复用的工作流，官方对复杂场景主推 Pipeline。

**两种语法，同一套子系统**：

- **Declarative Pipeline（声明式）**：结构严格、语法固定、可读性强，官方推荐大多数场景使用。
- **Scripted Pipeline（脚本式）**：基于 Groovy 的通用 DSL，自由度与复杂度高，适合条件复杂、逻辑动态的场景。

二者底层共用同一套 Pipeline 子系统，都是可持久化的 Pipeline as Code，并且都支持 Shared Library 复用。选择原则：**声明式为主，脚本式用于局部复杂逻辑**。

**执行模型**：Jenkins 采用 **Controller（控制器，负责调度、配置、认证授权与 Web 服务）+ Agent（代理，负责实际执行构建）** 的分布式架构。Jenkinsfile 中的 `agent` 指令决定整条流水线或某个阶段在哪个执行环境上运行。

## 三、核心机制

### 3.1 声明式语法骨架

声明式 Jenkinsfile 的标准骨架为 `pipeline` → `stages` → `stage` → `steps`，并支持 `agent`、`environment`、`options`、`parameters`、`triggers`、`when`、`parallel`、`matrix`、`post` 等指令。

```groovy
pipeline {
    agent any                      // 执行环境
    options { ... }                // 全局选项
    parameters { ... }             // 参数
    environment { ... }            // 环境变量 / 凭据绑定
    stages {
        stage('Build') { steps { ... } }
        stage('Test')  { steps { ... } }
        stage('Deploy'){ steps { ... } }
    }
    post { ... }                   // 结束状态动作
}
```

### 3.2 关键指令

- **`agent`**：指定执行环境，可选 `any` / `none` / `label` / `node` / `docker` / `dockerfile` / `kubernetes`。`agent none` 表示不预先分配节点，再在 `stage` 级用 `container` / `kubernetes` 指定运行容器，可减少调度开销。
- **`options`**：控制资源与行为，常用 `timeout(time: 30, unit: 'MINUTES')`、`retry(2)`、`buildDiscarder(logRotator(...))`、`disableConcurrentBuilds()`、`timestamps()`、`skipDefaultCheckout()`。**注意：`stage` 级 options 仅支持 `retry`、`timeout`、`timestamps`、`skipDefaultCheckout` 等**，其余需放在顶层。
- **`parameters`**：`string`、`booleanParam`、`choice`、`password`、`file` 等，运行时通过 `params` 对象访问。
- **`when`**：条件执行，如 `when { expression { params.ENV != 'prod' } }`，避免用大段 `script` 写分支。
- **`parallel` / `matrix`**：并行与多维矩阵构建，`parallel` 支持 `failFast true`（任一失败则中止全部）。
- **`post`**：`always`、`success`、`failure`、`unstable`、`changed`、`aborted`、`cleanup` 等，用于按结束状态执行通知与清理。

### 3.3 加载与执行

- **加载方式**：Jenkinsfile 可存放在 SCM 仓库根目录，由「Pipeline script from SCM」加载；也可通过 `build` / `checkout` 参数指定路径；**Multibranch Pipeline 会按分支自动发现**对应分支上的 Jenkinsfile，天然适配多分支开发。
- **执行过程**：Jenkins 从 SCM 拉取 Jenkinsfile → Groovy 解析与编译 → 按 `agent` 调度到目标节点执行各 `steps`。声明式流水线存在**代码体量上限**，脚本式无此限制，体量过大时应拆分到 Shared Library。
- **步骤校验**：编写时可对照官方 **Pipeline Steps reference** 确认可用步骤及其参数，避免使用不存在或已弃用的步骤。

### 3.4 凭据绑定机制

凭据由 Credentials Plugin / Credentials Binding 插件提供，支持 Secret Text、用户名密码、Secret File、SSH 私钥、证书、Token 等类型。Pipeline 中**只按凭据 ID 引用**，敏感值在控制台日志中显示为 `****`。

```groovy
environment {
    REGISTRY = credentials('registry-credentials-id')   // 绑定为环境变量
}

// 或在作用域内临时使用
withCredentials([usernamePassword(credentialsId: 'deploy-cred',
                                   username: 'u', password: 'p')]) {
    sh './deploy.sh'
}
```

> [!warning] 凭据安全边界
> 掩码机制**仅降低意外泄露风险，无法阻止恶意用户通过其他途径获取凭据值**。因此不要把受信任凭据暴露给不受信任的流水线，并通过全局 / 系统 / 用户级作用域限制凭据的访问范围。

## 四、实践步骤（含代码/命令示例）

### 步骤 1：准备运行环境

Jenkinsfile 由 Jenkins 解释执行，先确认 Jenkins 版本与 JDK 版本满足要求（2.555.1 起需 Java 21 或 Java 25）。推荐用官方 Docker 镜像快速起步：

```bash
# 启动 Jenkins 容器：映射 Web(8080) 与入站 Agent(50000) 端口，挂载数据卷
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  jenkins/jenkins:2.580.2-lts
```

首次访问 8080，从 `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword` 获取初始管理员密码，完成安装向导。

### 步骤 2：创建任务并加载 Jenkinsfile

在 Jenkins 中新建 **Pipeline** 类型任务，在配置页将「Definition」设为 **Pipeline script from SCM**，填写仓库地址、凭据与脚本路径（默认 `Jenkinsfile`）。多分支场景直接使用 **Multibranch Pipeline**，让 Jenkins 按分支自动发现 Jenkinsfile。

### 步骤 3：最简声明式流水线

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

声明式语法需安装 **Pipeline: Declarative Plugin**。跑通这一步，即完成了 Pipeline as Code 的最小闭环。

### 步骤 4：参数化 + 凭据 + 多阶段

一个贴近实战的起点，包含参数、环境变量、条件阶段与收尾动作：

```groovy
pipeline {
    agent { label 'builder' }

    parameters {
        string(name: 'APP_VERSION', defaultValue: '1.0.0', description: '部署的应用版本号')
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '部署环境')
    }

    environment {
        // 凭据只按 ID 引用，不要硬编码明文
        REGISTRY = credentials('registry-credentials-id')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
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
                junit '**/build/test-reports/*.xml'   // 需安装 JUnit 插件（2.580.x 起需手动安装）
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
            emailext to: 'team@example.com',
                    subject: '构建失败',
                    body: "${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
```

### 步骤 5：`agent none` + 阶段级容器

当不同阶段需要不同工具链时，可用 `agent none` 避免整条流水线绑定固定节点，再在阶段内按需拉起容器，减少调度与资源占用：

```groovy
pipeline {
    agent none
    stages {
        stage('Build') {
            agent { docker { image 'maven:3.9-eclipse-temurin-21' } }
            steps {
                sh 'mvn -B clean package'
            }
        }
        stage('Scan') {
            agent { docker { image 'aquasec/trivy:latest' } }
            steps {
                sh 'trivy image --exit-code 1 --severity HIGH my-app:1.0.0'
            }
        }
    }
}
```

### 步骤 6：Kubernetes 动态 Agent

在 Kubernetes 上用 Kubernetes 插件动态创建一次性 Pod 作为 Agent，构建完成后销毁。**推荐使用 YAML 模板（`yamlFile`）**，旧的 `containerTemplate` 已弃用：

```groovy
pipeline {
    agent {
        kubernetes {
            label 'jnlp-pod'
            yamlFile 'agent-pod.yaml'
        }
    }
    stages {
        stage('Build') {
            steps {
                container('builder') {
                    sh 'mvn -B clean package'
                }
            }
        }
    }
}
```

`agent-pod.yaml` 中通过 `containerTemplate`（YAML 形式）定义构建容器、镜像拉取凭据（`imagePullSecrets`）、`idleMinutes`、`podRetention`、`instanceCap` 等参数。

### 步骤 7：复用共享库

把可复用逻辑下沉到 Shared Library，让 Jenkinsfile 只描述「做什么」：

```groovy
// 静态导入，可带版本号
@Library('my-shared-library@1.0') _

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildPlugin(module: 'service-a', version: params.APP_VERSION)
            }
        }
    }
}
```

共享库目录约定：`src/`（Groovy 类）、`vars/`（全局变量脚本，文件名即变量名）、`resources/`（外部库可用 `libraryResource` 加载的资源）。

## 五、最佳实践与常见坑

**最佳实践**

1. **声明式优先**：结构规范、可读性强、便于标准化与评审；仅在复杂动态逻辑处局部使用 `script`，避免在声明式里堆砌大段脚本而突破体量上限。
2. **凭据不落明文**：一律通过 `credentials('id')` 或 `withCredentials` 引用，并设置合适的作用域；不要在 Jenkinsfile 中硬编码任何密钥、密码。
3. **控制资源与留存**：用 `options { timeout(...) }` 防构建挂死，用 `buildDiscarder(logRotator(...))` 控制日志与构建留存，用 `disableConcurrentBuilds()` 避免并发冲突。
4. **按阶段分配环境**：`agent none` + 阶段级 `container` / `kubernetes`，减少固定节点占用与调度开销。
5. **逻辑下沉到共享库**：通用构建、测试、部署封装为高层 DSL，业务流水线只描述业务语义，便于统一规范与维护。
6. **版本统一口径**：生产以 LTS 2.580.x 为基线，新特性参考 Weekly 2.591；用分支 / 标签 / 固定 commit 控制共享库版本。

**常见坑**

- **Java 版本不符**：仍用 Java 17 会直接启动失败，2.555.1 起必须 Java 21 或 25。
- **`junit` 步骤找不到**：2.580.x 移除了 JUnit 等默认捆绑插件，从旧版本升级需在插件管理器手动安装。
- **声明式体量超限**：`pipeline` 块代码量过大时会报错，应拆分到 Shared Library。
- **stage 超时「还没开始就超时」**：Pod / 容器的供给时间**计入** stage 超时，动态供给场景要预留时间，否则容器还没拉起就触发超时。
- **凭据绑定失败**：确认凭据类型、作用域，以及调用方对该凭据有读取权限。
- **`containerTemplate` 已弃用**：Kubernetes 集成应改用 `yamlFile` / YAML 模板，避免使用废弃语法。
- **构建卡在排队**：检查执行器数量、全局并发上限与节点标签是否匹配。
- **脚本式流水线重启后报错**：脚本式流水线需可序列化，部分 Groovy 闭包写法受限，复杂逻辑应下沉到共享库。

## 六、核心要点速查

1. Jenkinsfile 是用 **Groovy** 编写的流水线源码，纳入 SCM 即实现 **Pipeline as Code**。
2. 两种语法：**声明式**（官方推荐，结构规范）与**脚本式**（自由度高，适合复杂逻辑），共用同一 Pipeline 子系统。
3. 声明式骨架：`pipeline` → `stages` → `stage` → `steps`，辅以 `agent`、`options`、`parameters`、`environment`、`when`、`parallel`、`matrix`、`post`。
4. `agent` 可选 `any` / `none` / `label` / `node` / `docker` / `dockerfile` / `kubernetes`。
5. **`stage` 级 options 仅支持** `retry`、`timeout`、`timestamps`、`skipDefaultCheckout` 等，其余放在顶层。
6. 加载方式：SCM 中的 `Jenkinsfile`、`build` / `checkout` 指定路径、Multibranch 按分支自动发现。
7. 凭据**只按 ID 引用**，敏感值日志显示为 `****`；掩码仅降低意外泄露，无法防止恶意获取。
8. 共享库目录约定：`src/`（类）、`vars/`（全局变量）、`resources/`（资源）。
9. 引用共享库：`@Library('lib@版本') _` 静态导入，或 `library` 步骤运行时动态加载。
10. 截至 2026-11，最新 LTS 为 **2.580.2**（2026-10-28），Weekly 为 **2.591**（2026-11-16）。
11. **2.555.1 起要求 Java 21 或 25**，Java 17 已弃用。
12. **2.580.x 移除默认捆绑插件**，升级后需手动补齐 JUnit 等被移除的插件。
13. Kubernetes 集成用 `yamlFile` 定义 Pod 模板，`containerTemplate` 已弃用。
14. Kubernetes 插件当前 **1.35**（活跃，EOL 2027-02-28）。
15. 部署风险点：**CVE-2026-84651** 代理配置授权绕过，修复于 LTS 2.568.3 / Weekly 2.580，建议及时升级。

## 七、学习资源

以下为官方或权威来源：

1. [Using Jenkinsfile（Jenkins 官方手册·使用 Jenkinsfile）](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
2. [Pipeline Syntax（Jenkins 官方手册·流水线语法）](https://www.jenkins.io/doc/book/pipeline/syntax/)
3. [Pipeline（Jenkins 官方手册·流水线概览）](https://www.jenkins.io/doc/book/pipeline/)
4. [Extending with Shared Libraries（Jenkins 官方手册·共享库）](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
5. [Using credentials（Jenkins 官方手册·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
6. [Pipeline Steps reference（Jenkins 官方·流水线步骤参考）](https://www.jenkins.io/doc/book/pipeline/steps/)
7. [Kubernetes Plugin for Jenkins（Jenkins 插件站）](https://plugins.jenkins.io/kubernetes/)
8. [Kubernetes Pipeline Steps（Jenkins 官方·Kubernetes 流水线步骤）](https://www.jenkins.io/doc/pipeline/steps/kubernetes/)
9. [JUnit Plugin（Jenkins 插件站）](https://plugins.jenkins.io/junit/)
10. [JUnit Pipeline Step（Jenkins 官方·JUnit 步骤）](https://www.jenkins.io/doc/pipeline/steps/junit/)
11. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
12. [Jenkins 安全公告（官方安全公告索引）](https://www.jenkins.io/security/advisories/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
