---
title: CI/CD 理念与流水线模型
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - CI/CD
  - Jenkins
  - 流水线
  - 持续集成
  - 持续交付
aliases:
  - CI/CD 理念
  - 流水线模型
  - Pipeline as Code
source: 网络资料整理
---

# CI/CD 理念与流水线模型

> [!摘要] 摘要
> 本文是「CI/CD 与 Jenkins」知识体系中的第一块基石，聚焦**理念层**与**模型层**：先厘清 CI、持续交付、持续部署三者在目标与自动化程度上的差异，再拆解 Jenkins 以**流水线（Pipeline）**为核心的抽象模型——从 `pipeline → stages → stage → steps` 的骨架，到 `agent`、`environment`、`options`、`parameters`、`triggers`、`post` 等指令，以及 **Pipeline as Code** 与 Jenkinsfile 的落地方式。适合刚接触 Jenkins、想先理解「流水线到底是什么、为什么要代码化」的读者；具体的语法细节、共享库与部署实践见关联笔记。

## 一、最新动态（截至 2026-11）

以下版本与变更均来自 Jenkins 官方渠道，可作为写作与选型的事实锚点：

- **Jenkins 采用双发布线**：Weekly（每周）与 LTS（长期支持）。LTS 基线每 12 周从 Weekly 流中选取一次，随后每 4 周发布一个补丁（bug / 安全 / 小功能回移）。
- **Weekly 最新：2.591（2026-11-16 发布）**，主打变更为**默认启用内容安全策略（CSP）**——该能力自 2.539 引入，2.591 起默认生效。
- **LTS 最新：2.580.2（2026-10-28 发布）**，为安全修复版本；**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25 发布**。
- **下一个 LTS 基线定于 2027-01-06**，届时新 Manage Jenkins UI 将随该基线正式进入 LTS。
- **Java 硬约束收紧**：**Jenkins 2.555.1 及以后要求 Java 21 或 Java 25，Java 17 不再支持**。写示例与部署命令时不要沿用 JDK 17。
- **2.580.x 移除一批默认捆绑插件**（如 JUnit、Mailer、Matrix 等），`jenkins.war` 体积缩减 40 MB+；从 2.356 之前升级或检测到面向旧版本的插件时，需通过插件管理器手动补齐。
- **Kubernetes 插件最新 1.35（活跃，EOL 2027-02-28）**；JKO（Jenkins Kubernetes Operator）**v0.10.0-beta1（2026-11）**为测试性质，新增 Istio/Linkerd 服务网格支持与云身份注入保护。
- **官方 Docker 镜像**：LTS 线为 `jenkins/jenkins:2.580.2-lts`，官方文档示例使用 `FROM jenkins/jenkins:2.580.2-jdk21`。

> [!note] 版本口径
> 本文统一以 **LTS 2.580.x（当前 2.580.2）** 为生产推荐基线，以 **Weekly 2.591** 为最新特性参考。Jenkins 每周发布，版本号随时变化，临近节点请以官方仓库为准。

## 二、基础概念

### 2.1 CI/CD 的三层含义

CI/CD 是把「代码提交 → 构建 → 测试 → 发布 → 部署」这一过程自动化的工程实践，核心载体是**流水线（Pipeline）**。它实际由三个递进层次构成：

- **CI（持续集成，Continuous Integration）**：聚焦代码合并后的**自动构建与测试**。目标是尽早发现集成问题、缩短反馈回路，让「合入」成为一件低风险、高频次的小事。
- **CD 之持续交付（Continuous Delivery）**：在 CI 基础上把交付物（镜像、包、制品）**随时维持在「可发布」状态**，但最终的发布动作仍可由人工触发，多一道审批门禁。
- **CD 之持续部署（Continuous Deployment）**：在持续交付之上**自动发布到生产**，无需人工介入，对流水线的成熟度、测试覆盖率与回滚能力要求最高。

三者是**自动化程度递增**的关系：CI 解决「能不能自动验证」，持续交付解决「能不能随时安全地发布」，持续部署解决「能不能完全无人值守地发布」。

### 2.2 Jenkins 的定位与流水线模型

Jenkins 是这套流程的**自动化服务器**：通过 Web UI 与 REST 接口承接触发、调度与结果展示，把「怎么做构建和发布」交给流水线描述。Jenkins 官方文档将 Pipeline 定义为一套**插件套件**，它把构建流程抽象为一条**流水线（Pipeline）**，并支持将定义**代码化（Pipeline as Code）**——用 **Jenkinsfile** 描述过程，并纳入版本控制（SCM）。

代码化带来四个直接收益：

- **可评审**：流水线随代码一起走 PR / MR 评审；
- **可版本化**：历史可追溯，改动可回滚；
- **可复用**：通过 Shared Library 跨项目共享；
- **可审计**：谁在何时改了什么，一清二楚。

## 三、核心机制

### 3.1 流水线的抽象骨架

Jenkins Pipeline 的关键抽象是**四层嵌套结构**：

```text
pipeline
  └─ stages
        └─ stage
              └─ steps
```

- **`pipeline`**：顶层，一条流水线的根；
- **`stages`**：阶段集合，包含若干个 `stage`；
- **`stage`**：一个逻辑阶段（如 Build、Test、Deploy）；
- **`steps`**：阶段内的实际动作（如 `sh`、`echo`、`junit`）。

### 3.2 配套指令

围绕骨架，声明式流水线还提供一组指令，用于描述执行环境、控制行为与条件：

| 指令 | 作用 | 常见取值 / 用法 |
| --- | --- | --- |
| `agent` | 指定执行环境 | `any` / `none` / `label` / `docker` / `dockerfile` / `kubernetes` |
| `environment` | 定义环境变量、绑定凭据 | `REGISTRY = credentials('id')` |
| `options` | 控制流水线行为 | `timeout`、`retry`、`buildDiscarder`、`disableConcurrentBuilds`、`timestamps` |
| `parameters` | 定义构建参数 | `string`、`booleanParam`、`choice`、`password`、`file` |
| `triggers` | 定义触发方式 | `cron`、`pollSCM`、`upstream` |
| `when` | 阶段条件执行 | `expression`、`equals`、`branch`、`changelog` |
| `post` | 按结果执行收尾动作 | `always`、`success`、`failure`、`unstable`、`changed`、`cleanup` |
| `parallel` / `matrix` | 并行与矩阵构建 | `failFast true`；`axes` / `excludes` |

### 3.3 两种语法：声明式与脚本式

- **声明式（Declarative）**：结构严格、语法固定，可读性强、易于标准化，**官方推荐大多数场景**使用。
- **脚本式（Scripted）**：基于 Groovy 的通用 DSL，灵活度高，适合复杂条件与动态逻辑。

二者底层是**同一套 Pipeline 子系统**，都可持久化为 Pipeline as Code，都支持 Shared Library。差异主要在于约束强弱：声明式有结构校验与体量上限，脚本式无此限制但可读性更依赖作者水平。**原则：常规交付用声明式，复杂逻辑下沉到 Shared Library，而不是在声明式里堆大段 `script`。**

### 3.4 执行模型：控制器与代理

流水线实际执行依赖 Jenkins 的分布式模型：**Controller（控制器）**负责调度、队列、配置与 Web 服务；**Agent（代理 / 节点）**通过执行器运行构建任务，二者经 Remoting 通信。`agent` 指令正是把流水线的某个阶段绑定到具体执行环境。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境准备与启动

Jenkins 需要 **Java 21 或 Java 25**（2.555.1 起，Java 17 不再支持）。推荐用官方 Docker 镜像快速起步：

```bash
# 启动 Jenkins：映射 Web 与入站 Agent 端口，持久化 JENKINS_HOME
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  jenkins/jenkins:2.580.2-lts-jdk21

# 首次初始化：读取初始管理员密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 4.2 第一支声明式流水线

新建 Pipeline 任务 → 以「Pipeline script from SCM」或 Multibranch Pipeline 方式加载 Jenkinsfile → 运行。最简声明式 Jenkinsfile：

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

### 4.3 完整可落地的流水线

下面是一个带参数、环境变量、多阶段、条件与收尾的实用模板，可直接作为团队起点：

```groovy
pipeline {
    agent { label 'builder' }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    parameters {
        string(name: 'APP_VERSION', defaultValue: '1.0.0', description: '部署的应用版本号')
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '部署环境')
    }

    environment {
        // 凭据只按 ID 引用，不要硬编码明文
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
        always {
            echo "流水线结束：${currentBuild.result}"
        }
        failure {
            echo "构建失败，通知团队 #${env.BUILD_NUMBER}"
        }
        cleanup {
            echo '清理临时文件'
        }
    }
}
```

> [!tip] 加载方式
> Jenkinsfile 放入仓库根目录即可被 SCM 加载；也可在 Pipeline 任务中指定仓库与 `Jenkinsfile` 路径；**Multibranch Pipeline** 会自动按分支发现并各自执行，是多分支团队的标准做法。

### 4.4 脚本式写法对比

当需要复杂分支逻辑时，脚本式更直接，例如：

```groovy
node {
    stage('Build') {
        if (env.BRANCH_NAME == 'main') {
            sh './build-release.sh'
        } else {
            sh './build-snapshot.sh'
        }
    }
}
```

## 五、最佳实践与常见坑

**最佳实践：**

1. **默认用声明式**：结构清晰、便于评审与标准化；仅在复杂动态逻辑时切换脚本式，并尽量下沉到 Shared Library。
2. **Jenkinsfile 必须进版本控制**：它是流水线的源码，与业务代码同生命周期管理。
3. **凭据只按 ID 引用**：用 `credentials('id')` 或 `withCredentials` 绑定，敏感值在日志中显示为 `****`。
4. **用 `options` 兜底资源与稳定性**：`timeout` 防止任务挂死，`buildDiscarder` 控制日志与产物留存，`disableConcurrentBuilds` 避免同一任务并发打架。
5. **合理使用 `agent none` + 阶段级容器**：减少不必要的调度开销，动态容器在阶段内按需拉起。
6. **明确 `post` 的收尾职责**：通知、清理、归档等放在对应条件块，避免用 `always` 做过重的副作用。

**常见坑：**

- **凭据硬编码**：明文写入 Jenkinsfile 会随版本库泄露，且难以轮换，务必走凭据绑定。
- **声明式体量超限**：声明式存在代码体量上限，超限时应拆分为共享库，而不是继续堆砌。
- **脚本式不可序列化**：脚本式流水线需可序列化，部分 Groovy 闭包写法受限，控制器重启后可能报错，复杂逻辑应下沉到库。
- **阶段级超时未预留供给时间**：动态拉起 Pod / 容器的供给耗时**计入** stage 超时，否则会出现「还没开始跑就超时」。
- **构建卡在排队**：检查执行器数量、全局并发上限与 Agent 标签是否匹配，避免资源被打满。
- **升级后插件缺失**：2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件，从旧版本升级后如流水线报错，先检查插件是否需手动安装。
- **Java 版本过旧**：使用 Java 17 将直接无法运行 2.555.1 及以上版本，示例与部署命令需对齐 JDK 21 / 25。

## 六、核心要点速查

1. CI/CD 以**流水线（Pipeline）**为核心，把「提交 → 构建 → 测试 → 发布 → 部署」自动化。
2. 三层递进：**CI** 自动构建测试 → **持续交付**维持可发布 → **持续部署**自动上线。
3. Jenkins 定位为**自动化服务器**，通过 Pipeline 插件套件把流程描述为流水线。
4. **Pipeline as Code**：用 Jenkinsfile 描述流程并纳入版本控制，实现可评审、可版本化、可复用、可审计。
5. 抽象骨架：`pipeline` → `stages` → `stage` → `steps`。
6. 常用指令：`agent`、`environment`、`options`、`parameters`、`triggers`、`when`、`post`、`parallel`、`matrix`。
7. 两种语法：**声明式**（规范、官方主推）与**脚本式**（灵活、适合复杂逻辑），共用同一 Pipeline 子系统。
8. 执行模型：**Controller 调度 + Agent 执行**，`agent` 指令把阶段绑定到具体执行环境。
9. 截至 2026-11，最新 LTS 为 **2.580.2**（2026-10-28），Weekly 为 **2.591**（2026-11-16，默认启用 CSP）。
10. **2.555.1 起要求 Java 21 / Java 25**，Java 17 已弃用。
11. 凭据以 ID 引用、日志掩码，切勿在 Jenkinsfile 中硬编码明文。
12. 2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件，升级后需手动补齐。

## 七、学习资源

以下均为 Jenkins 官方来源：

1. [Pipeline（Jenkins 官方用户手册·流水线概览）](https://www.jenkins.io/doc/book/pipeline/)
2. [Pipeline Syntax（Jenkins 官方用户手册·流水线语法）](https://www.jenkins.io/doc/book/pipeline/syntax/)
3. [Using a Jenkinsfile（Jenkins 官方用户手册·Jenkinsfile）](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
4. [Extending with Shared Libraries（Jenkins 官方用户手册·共享库）](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
5. [Jenkins 用户手册（官方手册首页）](https://www.jenkins.io/doc/book/)
6. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
7. [Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)
8. [Jenkins Docker 安装文档](https://www.jenkins.io/doc/book/installing/docker/)
9. [Using credentials（官方用户手册·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]（本主题总览，体系导航）
- [[DevOps]]
- [[DevOps与Kubernetes-从入门到精通]]
- [[CI-CD现代实践与趋势]]
- [[Jenkins流水线配置]]

## 九、变更记录

- 2026-11-19：首次创建。
