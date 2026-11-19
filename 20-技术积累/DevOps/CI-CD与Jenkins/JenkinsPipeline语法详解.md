---
title: Jenkins Pipeline 语法详解
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 流水线
  - Jenkinsfile
  - Groovy
aliases:
  - Jenkins Pipeline 语法
  - Jenkinsfile 语法
source: 网络资料整理
---

# Jenkins Pipeline 语法详解

> [!摘要] 摘要
> 本文详解 Jenkins Pipeline 的两种语法（声明式 Declarative 与脚本式 Scripted）、核心指令（`agent`/`stages`/`stage`/`steps`/`options`/`parameters`/`environment`/`triggers`/`parallel`/`matrix`/`post`/`when` 等），并给出可直接运行的 Jenkinsfile 示例与常见坑。Jenkins Pipeline 是一套插件套件，把构建流程描述为「流水线」，并以 Jenkinsfile 形式纳入版本控制，即 **Pipeline as Code**。适合已装好 Jenkins、准备编写和维护流水线的运维与研发工程师。本文版本事实以 [Jenkins 官方文档](https://www.jenkins.io/doc/book/pipeline/syntax/) 与 [[CI-CD与Jenkins-从入门到精通]] 为准。

## 一、最新动态（截至 2026-11）

- **Jenkins 采用双发布线**：Weekly（每周）与 LTS（长期支持，基线每 12 周选取，随后每 4 周打补丁）。生产建议以 **LTS 2.580.x** 为基线。
- **当前版本**：Weekly 最新 **2.591（2026-11-16 发布）**，主打**默认启用内容安全策略（CSP）**（该能力自 2.539 引入，2.591 起默认生效）；LTS 最新 **2.580.2（2026-10-28 发布）**，为安全修复版本。**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25**；下一个 LTS 基线定于 **2027-01-06**。
- **影响 Pipeline 的变更**：**2.555.1（2026-04-15）起要求 Java 21 或 Java 25，Java 17 不再支持**，运行 Jenkinsfile 的 JDK 必须同步升级；**API Token 支持过期日期**（2.555.x 起）；**2.580.x 移除一批默认捆绑插件**（如 JUnit、Mailer、Matrix Project 等），`jenkins.war` 体积缩减 40MB+，从 2.356 之前升级需在插件管理器手动补齐。
- **安全**：2026 年共发布 **10 次**安全公告；**CVE-2026-84651（2026-09-02）**为更新代理配置的 REST API/CLI 授权绕过，修复于 LTS 2.568.3 / Weekly 2.580，建议尽快升级。
- **Kubernetes 集成**：Kubernetes 插件最新 **1.35（活跃，EOL 2027-02-28）**，`containerTemplate` 已**弃用**，官方推荐改用 **YAML 模板（`yamlFile`）**。

> [!note] 口径说明
> 本文写作时点的版本号均来自调研文件（截至 2026-11）。Jenkins 每周发布，如使用时间晚于该时点，请以官方 [Jenkins Changelog](https://www.jenkins.io/changelog-stable/) 与 [Jenkins 下载页](https://www.jenkins.io/download/) 为准。

## 二、基础概念

**Pipeline（流水线）**：把「代码提交 → 构建 → 测试 → 发布 → 部署」描述为可执行流程的抽象。Jenkins Pipeline 由一组插件提供，核心抽象层级为：

```text
pipeline
 └─ stages
     └─ stage
         └─ steps
```

- **Pipeline as Code**：用 Groovy 编写 **Jenkinsfile** 描述流水线，纳入版本控制后可评审、可复用、可审计。Jenkinsfile 支持 **声明式**与**脚本式**两种语法，底层是同一套 Pipeline 子系统，均支持 Shared Library。
- **声明式（Declarative）**：结构严格、语法固定，可读性强、便于标准化，官方推荐用于大多数场景。
- **脚本式（Scripted）**：基于 Groovy 的通用 DSL，自由度高，适合复杂条件与动态逻辑。
- **执行模型**：`agent` 指定在哪里跑，`stages/stage/steps` 描述按什么顺序跑，`post` 处理结束动作，`options`/`parameters`/`environment`/`triggers`/`when` 提供控制与参数化能力。

> [!tip] 选型口诀
> **常规交付用声明式，复杂分支与动态逻辑用脚本式，复杂逻辑尽量下沉到 Shared Library**。不要在声明式里堆大段 `script`，否则既丢可读性，也易触及声明式代码体量上限。

## 三、核心机制

**1. `agent`：指定执行环境。** 支持 `any`、`none`、`label`、`node`、`docker`、`dockerfile`、`kubernetes`，以及 `registryUrl`/`registryCredentialsId` 等拉取私有镜像的参数。

**2. 结构指令。** `stages`/`stage`/`steps` 定义阶段与步骤；`post` 提供 `always`、`success`、`failure`、`unstable`、`changed`、`aborted`、`cleanup` 等条件块。

**3. `options`：全局与阶段级控制。** 常用 `timeout`、`retry`、`buildDiscarder`、`disableConcurrentBuilds`、`timestamps`、`skipDefaultCheckout`、`newContainerPerStage`、`preserveStashes`、`parallelsAlwaysFailFast`。**stage 级仅支持** `retry`、`timeout`、`timestamps`、`skipDefaultCheckout` 等，其余须放顶层。

**4. `parameters` 与 `when`。** `parameters` 支持 `string`、`booleanParam`、`choice`、`password`、`file` 等，通过 `params` 对象访问；`when` 支持 `expression`、`branch`、`environment`、`changelog`、`beforeAgent` 等条件，决定某阶段是否执行。

**5. `environment` 与凭据。** 绑定环境变量；凭据以 ID 引用（`credentials('id')`）或 `withCredentials` 作用域内使用，敏感值在日志中显示为 `****`。

**6. `parallel` 与 `matrix`。** `parallel` 并行执行多个分支阶段，`failFast true` 时任一失败即中止全部；`matrix` 按多个轴（`axes`）与排除项（`excludes`）展开多维并行。

**7. `triggers`、`input`、`script`。** `triggers` 支持 `cron`、`pollSCM`、`upstream`；`input` 实现部署等人工审批门禁（可配 `submitter`）；`script` 在声明式中嵌入脚本式逻辑。

**8. 构建生命周期与状态。** 一次构建经历 `QUEUED`（排队）→ `RUNNING`（执行）→ 结束态（`SUCCESS`、`FAILURE`、`ABORTED`、`UNSTABLE`、`NOT_BUILT`）。`currentBuild` 对象暴露 `state`/`result`/`result` 等属性，`post` 各条件块正是按结束态与变化情况（`changed`、`fixed`、`regression`）触发的，理解状态流转是写好 `post` 与告警的前提。

## 四、实践步骤（含代码/命令示例）

**步骤 1：安装依赖。** 声明式语法需安装 `Pipeline: Declarative Plugin`，凭据绑定需 `Credentials Binding Plugin`，测试报告需 `JUnit Plugin`（注意 2.580.x 起 JUnit 已从默认捆绑中移除，需手动安装）。

**步骤 2：最简声明式流水线。**

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

**步骤 3：带参数、环境与条件阶段的实用起点。**

```groovy
pipeline {
    agent { label 'builder' }

    parameters {
        string(name: 'APP_VERSION', defaultValue: '1.0.0', description: '应用版本号')
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '部署环境')
    }

    environment {
        REGISTRY = credentials('registry-credentials-id') // 只按 ID 引用
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        retry(2)
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepPerBuild: 10))
        timestamps()
    }

    stages {
        stage('Build') {
            steps {
                sh "echo '构建 ${params.APP_VERSION} 到 ${params.ENV}'"
            }
        }
        stage('Test') {
            steps {
                sh './run-tests.sh'
                junit '**/build/test-reports/*.xml'
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
        always { echo "流水线结束：${currentBuild.result}" }
        failure {
            emailext to: 'team@example.com',
                     subject: '构建失败',
                     body: "${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        cleanup { echo '清理资源' }
    }
}
```

**步骤 4：并行与矩阵。**

```groovy
stages {
    stage('Parallel Test') {
        parallel {
            stage('Unit')  { steps { sh './test-unit.sh' } }
            stage('E2E')   { steps { sh './test-e2e.sh'  } }
        }
    }
    stage('Matrix Build') {
        matrix {
            axes {
                string(name: 'PLATFORM', values: ['linux', 'windows'])
                string(name: 'JDK',      values: ['21', '25'])
            }
            excludes {
                // 排除不需要的组合
            }
            steps {
                sh "echo 'build on ${PLATFORM} with JDK ${JDK}'"
            }
        }
    }
}
```

**步骤 5：Docker / Kubernetes 执行环境。** Docker 用 `docker` 或 `dockerfile` agent；Kubernetes 用 `yamlFile` 定义 Pod 模板（`containerTemplate` 已弃用）。

```groovy
agent {
    kubernetes {
        label 'jenkins-agent'
        yamlFile 'agent-pod.yaml'
    }
}
```

**步骤 6：凭据在作用域内使用。**

```groovy
stage('Push') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'git-cred',
                                           usernameVariable: 'GIT_USER',
                                           passwordVariable: 'GIT_PASS')]) {
            sh 'git push https://$GIT_USER:$GIT_PASS@example.com/repo.git'
        }
    }
}
```

**步骤 7：用 `input` 做部署审批门禁。**

```groovy
stage('Deploy to Prod') {
    when { branch 'main' }
    options { timeout(time: 60, unit: 'MINUTES') }
    steps {
        input message: "确认将 ${params.APP_VERSION} 发布到生产？",
              submitter: 'release-admins',
              parameters: [
                  string(name: 'CONFIRM_VERSION', defaultValue: params.APP_VERSION,
                         description: '确认发布的版本号')
              ]
        sh "./deploy.sh --env prod --version ${params.APP_VERSION}"
    }
}
```

**步骤 8：在 Jenkins 中加载。** 新建 Pipeline 任务，选择「Pipeline script from SCM」指向仓库中的 Jenkinsfile；或使用 **Multibranch Pipeline** 按分支自动发现。

## 五、最佳实践与常见坑

- **凭据不硬编码**：只按 ID 引用，敏感值日志显示为 `****`。官方明确**掩码仅降低意外泄露风险，无法阻止恶意用户**，不要允许不受信任的流水线使用受信任凭据。
- **`agent none` + 阶段级 `container`**：可减少调度与供给开销；但 **Pod/容器的供给时间计入 stage 超时**，需预留余量，否则「还没开跑就超时」。
- **控制资源与日志**：用 `options { timeout(...) }`、`buildDiscarder(logRotator(...))`、`disableConcurrentBuilds()` 防资源堆积与日志膨胀。
- **声明式体量上限**：声明式存在代码体量上限，脚本式无此限制；过大时重构为 Shared Library，`vars/` 全局变量**保持无状态**。
- **脚本式需可序列化**：部分 Groovy 闭包用法（如 `collection.each` 的部分写法）在控制器重启后可能报错，复杂逻辑下沉到库。
- **升级兼容**：2.555.1 起 Java 21/25 为硬约束；2.580.x 移除默认捆绑插件，从旧版本升级需手动补齐 JUnit、Mailer、Matrix 等。
- **安全**：受信任流水线配合 Script Security Plugin 沙箱约束；关注 CVE-2026-84651 并升级到 2.568.3 / 2.580 及以上。
- **构建卡在排队**：检查执行器数量、全局并发上限与 `label` 是否匹配，避免 CPU/内存/IO 被打满。

## 六、核心要点速查

1. Pipeline 抽象：`pipeline` → `stages` → `stage` → `steps`，配合 `agent`、`options`、`parameters`、`environment`、`triggers`、`post`。
2. 两种语法：**声明式**（结构规范、官方推荐）与**脚本式**（灵活、适合复杂逻辑），共用同一 Pipeline 子系统。
3. `agent` 形态：`any` / `none` / `label` / `node` / `docker` / `dockerfile` / `kubernetes`。
4. `post` 条件：`always`、`success`、`failure`、`unstable`、`changed`、`cleanup` 等。
5. `when` 条件：`expression`、`branch`、`environment`、`changelog`、`beforeAgent`。
6. `parallel` 支持 `failFast true`；`matrix` 用 `axes` + `excludes` 展开多维并行。
7. `options` 常用：`timeout`、`retry`、`buildDiscarder`、`disableConcurrentBuilds`、`timestamps`；stage 级仅支持 `retry`/`timeout`/`timestamps`/`skipDefaultCheckout` 等。
8. 凭据按 ID 引用（`credentials('id')` 或 `withCredentials`），日志掩码为 `****`。
9. Kubernetes 插件用 `yamlFile`（`containerTemplate` 已弃用）。
10. 截至 2026-11：LTS 最新 **2.580.2**，Weekly 最新 **2.591**；2.555.1 起要求 **Java 21/25**。

## 七、学习资源

1. [Pipeline Syntax（Jenkins 官方用户手册·流水线语法）](https://www.jenkins.io/doc/book/pipeline/syntax/)
2. [Pipeline（Jenkins 官方用户手册·流水线概览）](https://www.jenkins.io/doc/book/pipeline/)
3. [Using Jenkinsfiles（Jenkins 官方·Jenkinsfile 使用）](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
4. [Extending with Shared Libraries（Jenkins 官方·共享库）](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
5. [Using credentials（Jenkins 官方·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
6. [Pipeline Steps reference（Pipeline 步骤参考）](https://www.jenkins.io/doc/book/pipeline/developing/)
7. [Kubernetes Pipeline Steps（Kubernetes 流水线步骤）](https://www.jenkins.io/doc/pipeline/steps/kubernetes/)
8. [JUnit Pipeline Step（JUnit 步骤）](https://www.jenkins.io/doc/pipeline/steps/junit/)
9. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
10. [Jenkins 安全公告](https://www.jenkins.io/security/advisories/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]
- [[Jenkins流水线配置]]

## 九、变更记录

- 2026-11-19：首次创建。
