---
title: Jenkins 部署自动化（蓝绿/滚动）
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 部署自动化
  - 蓝绿部署
  - 滚动部署
aliases:
  - Jenkins 蓝绿部署
  - Jenkins 滚动部署
source:
  - 网络资料整理
---

# Jenkins 部署自动化（蓝绿/滚动）

> [!summary] 摘要
> 本文聚焦「在 Jenkins 中落地应用发布」这一关键环节：说明 Jenkins 本身**不内置任何部署策略**，而是通过 Pipeline 调用 kubectl、Helm、Ansible 等工具，把**蓝绿部署**（同时维护两套环境、一键切换流量）与**滚动部署**（逐批替换实例）编排进发布流水线。内容涵盖基础概念、核心机制、可直接复用的 Jenkinsfile 示例、回滚与审批门禁，以及镜像不可变、凭据安全等生产级最佳实践。适合已掌握 Jenkins Pipeline 基础、需要把 CI/CD 推进到生产发布阶段的工程师；概念体系的全局定位见 [[CI-CD与Jenkins-从入门到精通]]。

## 一、最新动态（截至 2026-11）

- **Jenkins 双发布线**：Weekly（每周）与 LTS（长期支持）。LTS 基线每 12 周从 Weekly 选取一次，随后每 4 周发布补丁。生产建议以 **LTS** 为基线。
- **当前版本状态**：**LTS 最新 2.580.2（2026-10-28 发布，安全修复版）**；**Weekly 最新 2.591（2026-11-16 发布）**，该版起默认启用内容安全策略（CSP）。2.580.3 已出 RC，**正式版计划 2026-11-25 发布**；下一个 LTS 基线定于 2027-01-06。
- **Java 硬约束**：**2.555.1 及以后要求 Java 21 或 Java 25，Java 17 已弃用**。部署类 Agent 同样需满足该要求，示例镜像使用 `jenkins/jenkins:2.580.2-jdk21`。
- **Kubernetes 集成**：**Kubernetes 插件最新 1.35（活跃，EOL 2027-02-28）**；**JKO（Jenkins Kubernetes Operator）v0.10.0-beta1（2026-11）** 为测试性质，新增 Istio/Linkerd 服务网格与云身份注入保护。**`containerTemplate` 已弃用，官方推荐改用 `yamlFile`/YAML 定义 Pod 模板**。
- **安全提示**：**CVE-2026-84651（2026-09-02）** 涉及更新代理配置的 REST API/CLI 授权绕过，可跨代理接管配置并获取入站代理密钥，修复于 **2.568.3 / 2.580**，涉及 Agent 编排的部署流水线应尽快升级。

以上版本号均来自 Jenkins 官方变更日志与安全公告，后续可能变化，**以官方仓库为准**：[Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/)、[Jenkins 安全公告](https://www.jenkins.io/security/advisories/)。

## 二、基础概念

- **CI/CD 的分层**：CI 负责代码合入后的自动构建与测试；CD 之**持续交付**把制品维持在「随时可发布」状态；CD 之**持续部署**进一步自动发布到生产。部署自动化属于最后一环，对流水线的可靠性、可观测与回滚能力要求最高。
- **Jenkins 的定位**：Jenkins 是自动化服务器，用 **Pipeline as Code**（Jenkinsfile）描述流程。**部署策略不由 Jenkins 实现**，Jenkins 负责「编排」——在流水线的 Deploy 阶段调用部署工具，并完成审批、校验、通知与回滚。
- **蓝绿部署**：同时维护**绿色（新）**与**蓝色（旧）**两套完整环境，构建并验证新环境通过后，把流量（负载均衡 / 网关 / Service Endpoint）**一次性切换**到绿色；发现问题可瞬间切回蓝色。优点是回滚快、对用户几乎无感，代价是**资源翻倍**。
- **滚动部署**：按批次（`maxSurge` / `maxUnavailable`）逐批替换旧实例，无需两套全量环境，资源占用低；但发布期间新旧版本**同时存在**，需要应用兼容（如接口版本、数据库变更向前兼容）。
- **共同前提**：**原子发布**与**快速回滚**。镜像应使用**不可变 digest**，避免生产引用可变标签导致「回滚后又被覆盖」。

## 三、核心机制

**1. 调度与执行**：Controller 负责调度与队列，Deploy 阶段在带部署能力的 **Agent**（或 `kubernetes`/`docker` Agent）上执行 `sh`/`ssh`，调用 `kubectl`、`Helm`、`Ansible` 等工具完成发布。

**2. 用 `environment` 与 `params` 区分环境/策略**：把目标环境、版本、部署方式建模为参数，避免流水线里散落魔法值。

**3. 审批门禁**：生产发布前用 **`input`** 步骤等待人工确认，可用 `submitter` 指定审批人，实现持续交付（人工放行）而非纯持续部署。

**4. 条件与分支**：用 `when` 控制只在特定环境/分支执行部署；用 `options { disableConcurrentBuilds() }` 防止同一任务并发发布造成状态错乱。

**5. 回滚机制**：发布失败或健康检查不通过时，在 `post { failure { ... } }` 中执行回滚（切回旧标签或镜像 digest），保证「发布-回滚」闭环。

**6. 凭据安全**：镜像仓库、集群凭证等一律通过 `credentials('id')` 引用，禁止硬编码；敏感值在日志中显示为 `****`。

## 四、实践步骤（含代码/命令示例）

**步骤 1：准备部署 Agent 与凭据**。在控制器配置带 `kubectl`/`helm` 的 Agent 标签（如 `deploy`），并在凭据中保存集群访问凭证（`kubeconfig` 用 Secret file 类型，仓库凭证用用户名密码）。

**步骤 2：滚动部署流水线**。以下为生产环境滚动发布示例：

```groovy
pipeline {
    agent { label 'deploy' }

    parameters {
        string(name: 'APP_VERSION', defaultValue: '1.2.0', description: '发布版本')
        choice(name: 'DEPLOY_STRATEGY', choices: ['rolling', 'blue-green'], description: '部署策略')
    }

    environment {
        // 只按 ID 引用凭据，避免明文
        KUBE_CONFIG = credentials('k8s-kubeconfig-id')
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }

    stages {
        stage('Build & Test') {
            steps {
                sh "./build.sh && ./test.sh"
                junit '**/build/test-reports/*.xml'
            }
        }
        stage('Deploy') {
            when { expression { params.DEPLOY_STRATEGY == 'rolling' } }
            steps {
                withEnv(['KUBECONFIG=/tmp/kubeconfig']) {
                    sh """
                        kubectl --kubeconfig "${KUBE_CONFIG}" set image \
                          deployment/app app=registry.example.com/app:${params.APP_VERSION} \
                          -n production --record
                        kubectl --kubeconfig "${KUBE_CONFIG}" rollout status \
                          deployment/app -n production --timeout=300s
                    """
                }
            }
        }
    }

    post {
        failure {
            sh "kubectl rollout undo deployment/app -n production"
            emailext to: 'team@example.com', subject: '发布失败已回滚', body: "${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
```

**步骤 3：蓝绿部署流水线**。维护 `app-blue` 与 `app-green` 两套 Deployment，发布时部署到非活跃环境，验证通过后切换 Service 的 Selector 或 Endpoint：

```bash
# 切换流量的核心动作：把 Service 的 selector 指向新环境（label 切换）
kubectl patch service app -n production --type='json' \
  -p '[{"op":"replace","path":"/spec/selector/env","value":"green"}]'
```

```groovy
    stage('Blue-Green Deploy') {
        when { expression { params.DEPLOY_STRATEGY == 'blue-green' } }
        steps {
            // 判定当前活跃环境，部署到非活跃环境
            sh """
                CURRENT=$(kubectl get service app -n production -o jsonpath='{.spec.selector.env}')
                TARGET=\$( [ "\$CURRENT" = "blue" ] && echo green || echo blue )
                kubectl --kubeconfig "${KUBE_CONFIG}" set image deployment/app-${TARGET} \
                  app=registry.example.com/app:${params.APP_VERSION} -n production
                kubectl --kubeconfig "${KUBE_CONFIG}" rollout status \
                  deployment/app-${TARGET} -n production --timeout=300s
            """
            // 人工审批门禁后再切换流量
            input message: "确认将生产流量切换到新环境？", submitter: 'release-approver'
            sh "./switch-traffic.sh ${params.APP_VERSION}"
        }
    }
```

**步骤 4：回滚**。滚动发布回滚用 `kubectl rollout undo`；蓝绿发布回滚只需再次切换 selector，**无需重新部署**，这是蓝绿的核心优势。

## 五、最佳实践与常见坑

- **镜像用 digest，不用可变标签**：生产镜像固定 `sha256:...`，否则 `rollout undo` 或切回旧版本时可能被同一标签的新版本覆盖，导致「回滚无效」。
- **发布必须有健康检查与超时**：`rollout status` 前确保 Deployment 配置了 `readinessProbe`；设置合理 `--timeout`，避免流水线长时间挂起。
- **防并发**：同一应用/环境务必 `disableConcurrentBuilds()`，否则两次发布互相覆盖，状态不可预期。
- **审批门禁分层**：测试环境自动发布，生产环境用 `input` + `submitter` 人工放行；不要把生产发布完全放开给所有人。
- **回滚前置设计**：`post { failure }` 中的回滚必须经过测试验证，否则「自动回滚」可能引入二次故障。
- **凭据作用域最小化**：部署用集群凭证按项目/文件夹作用域隔离，**不要允许不受信任的流水线使用受信任凭据**；掩码只能降低意外泄露，无法阻止恶意获取。
- **资源与超时预留**：动态 Agent（`kubernetes`/`docker`）的**供给时间计入 stage 超时**，给拉取镜像与调度留出余量。
- **蓝绿资源成本**：蓝绿需要两套环境，注意容量规划与成本；可结合 Istio/Flagger 做更精细的流量切换与自动分析（参见 [[Kubernetes部署策略（滚动-蓝绿-金丝雀）]]）。
- **避免版本时效陷阱**：Jenkins 每周发布，示例中的插件与镜像标签会过期，使用前以官方仓库为准。

## 六、核心要点速查

1. Jenkins **不内置部署策略**，通过 Pipeline 调用 `kubectl`/`Helm`/`Ansible` 编排发布。
2. **蓝绿部署**：两套环境 + 流量切换，回滚最快；**滚动部署**：逐批替换，资源占用低。
3. 发布前用 `environment`/`params` 建模环境与策略，生产用 `input` 做审批门禁。
4. 用 `when` 控制执行条件，用 `disableConcurrentBuilds()` 防止并发发布。
5. 镜像使用**不可变 digest**，生产禁用可变标签。
6. 回滚：滚动用 `kubectl rollout undo`，蓝绿切换流量即可。
7. 凭据按 ID 引用、作用域最小化，禁止在 Jenkinsfile 硬编码。
8. 截至 2026-11，推荐 **LTS 2.580.x** 为生产基线，要求 **Java 21/25**；Kubernetes 插件 **1.35**，Pod 模板用 **`yamlFile`** 而非已弃用的 `containerTemplate`。

## 七、学习资源

1. [Pipeline Syntax（Jenkins 官方·流水线语法）](https://www.jenkins.io/doc/book/pipeline/syntax/)
2. [Pipeline Overview（Jenkins 官方·流水线概览）](https://www.jenkins.io/doc/book/pipeline/)
3. [Kubernetes Plugin for Jenkins（Jenkins 插件站）](https://plugins.jenkins.io/kubernetes/)
4. [Kubernetes Pipeline Steps（Jenkins 官方·Kubernetes 步骤）](https://www.jenkins.io/doc/pipeline/steps/kubernetes/)
5. [Using credentials（Jenkins 官方·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
6. [Jenkins Operator（JKO）官方仓库](https://github.com/jenkinsci/kubernetes-operator)
7. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
8. [Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[JenkinsPipeline语法详解]]
- [[Jenkinsfile编写实践]]
- [[Jenkins与Kubernetes集成（JKO）]]
- [[Kubernetes部署策略（滚动-蓝绿-金丝雀）]]

## 九、变更记录

- 2026-11-19：首次创建。
