---
title: Jenkins-共享库实战
date: 2026-11-19
tags:
  - 技术积累
  - DevOps
  - Jenkins
  - SharedLibrary
  - Groovy
---

# Jenkins-共享库实战

> [!abstract] 摘要
> 共享库（Shared Library）把多个 Jenkinsfile 里重复的构建/通知/部署逻辑抽成可复用代码库，实现 DRY：业务流水线退化为 20 行以内的编排层。本文覆盖库的类型与权限、`vars/src/resources` 目录逐个讲解、@Library 版本化与动态加载、@NonCPS 等 CPS 陷阱，并提供"通知+构建+部署"三步封装的完整案例。

## 一、概念与原理

没有共享库时，几十个项目的 Jenkinsfile 各自复制粘贴同一段 `mvn build + docker push + 企微通知`，改一处要发 N 个 PR。共享库把这些公共逻辑放进独立 Git 仓库，由 Jenkins 在编译流水线时注入 classpath：

```mermaid
graph LR
    A[业务仓库 A Jenkinsfile] -->|@Library| L[(共享库 Git 仓库<br>vars/src/resources)]
    B[业务仓库 B Jenkinsfile] -->|@Library| L
    C[业务仓库 C Jenkinsfile] -->|@Library@v2.3| L
    L --> J[Jenkins Controller<br>编译期注入 classpath]
    J --> R[构建运行<br>全局变量=新步骤]
```

### 全局共享库 vs 文件夹级

| 维度 | Global Trusted Library | Folder-level Library |
| --- | --- | --- |
| 配置位置 | Manage Jenkins → System → Global Trusted Pipeline Libraries | 文件夹配置页 |
| 作用范围 | 所有流水线 | 该文件夹及其子项 |
| 权限 | trusted：可调任意 Jenkins/Java API（配置需管理员） | 一律 untrusted：跑在 Groovy 沙箱内 |
| 风险 | **能 push 该库仓库 = 拥有 Jenkins 管理员权限**，提交权限必须锁紧 | 沙箱限制，风险较低 |

> [!warning]
> Trusted 库的提交权限等同于 Jenkins 管理员。给共享库仓库的写权限评审级别，要按管理员标准执行（受保护分支 + 至少一人 approve）。

## 二、目录结构与编写详解

```
jenkins-shared-library/          # 独立 Git 仓库
├── src/                         # Java 风格包结构的 Groovy 类（进 classpath，可单测）
│   └── org/demo/NotifyClient.groovy
├── vars/                        # 每个文件 = 一个全局变量（步骤），必须 camelCase
│   ├── buildJava.groovy         # → buildJava(...)
│   ├── notifyWecom.groovy       # → notifyWecom(...)
│   ├── deployK8s.groovy
│   └── buildJava.txt            # 同名 .txt 为全局变量文档页（Global Variable Reference）
└── resources/                   # libraryResource() 读取的静态资源（模板/JSON）
    └── templates/deploy.yaml
```

### 2.1 vars 全局变量：三种签名

```groovy
// vars/sayHello.groovy —— ① 最简：call 方法即步骤入口
def call(String name = 'human') {
    echo "Hello, ${name}."
}
// 调用：sayHello('Joe') 或 sayHello 'Joe'
```

```groovy
// vars/buildJava.groovy —— ② Map 参数 + 默认值（推荐对外 API 形式）
def call(Map cfg = [:]) {
    def jdkImage  = cfg.get('jdkImage', 'maven:3.9-eclipse-temurin-21')
    def skipTests = cfg.get('skipTests', false)
    def app       = cfg.get('app', error('必须传 app 参数'))

    pipeline {
        agent { docker { image jdkImage; args '-v /var/cache/m2:/root/.m2' } }
        options { timestamps(); buildDiscarder(logRotator(numToKeepStr: '15')) }
        stages {
            stage('单测') {
                when { not { expression { skipTests } } }
                steps { sh 'mvn -B verify' }
            }
            stage('打包') { steps { sh 'mvn -B clean package -DskipTests' } }
        }
        post {
            always { junit allowEmptyResults: true, testResults: '**/surefire-reports/*.xml' }
        }
    }
}
```

```groovy
// vars/dockerLogin.groovy —— ③ 闭包调用：withCredentials 风格包裹
def call(String credentialsId, Closure body) {
    withCredentials([usernamePassword(
            credentialsId: credentialsId,
            usernameVariable: 'USR', passwordVariable: 'PSW')]) {
        body()          // 调用方：dockerLogin('regcred') { sh 'docker push ...' }
    }
}
```

> [!tip]
> 声明式流水线里调用共享库的**非步骤型**全局变量方法（如 `log.info`）要放进 `script { }` 块；直接实现为 `call` 的步骤可以裸调用。vars 脚本应保持无状态，需要字段时用 `@groovy.transform.Field`（建议只读常量）。

### 2.2 src Groovy 类与 @NonCPS

类中不能直接调 `sh` 等步骤，必须显式传入 steps 对象；需要跨挂起/恢复保存状态的类要实现 `Serializable`：

```groovy
// src/org/demo/Utilities.groovy
package org.demo
import com.cloudbees.groovy.cps.NonCPS

class Utilities implements Serializable {
    def steps
    Utilities(steps) { this.steps = steps }

    // 步骤类逻辑经由传入的 steps 调用
    def mvn(String args) {
        steps.sh "${steps.tool 'Maven'}/bin/mvn -B ${args}"
    }

    // 纯计算逻辑（JSON 解析/集合排序/正则）标 @NonCPS，绕过 CPS 转换
    @NonCPS
    def parseJson(String text) {
        new groovy.json.JsonSlurper().parseText(text)
    }
}
```

> [!warning] @NonCPS 的边界
> `@NonCPS`（`com.cloudbees.groovy.cps.NonCPS`）让方法以"普通 Groovy"运行，用于修复 CPS 方法不匹配（如 Jenkins API 返回的 Map 做 `entrySet`、`.sort{}`、JsonSlurper 解析）。但它**不能调用 `sh`/`echo` 等 CPS 步骤**，且方法中途 Jenkins 重启不会从断点恢复而是重头再跑——只放纯计算短逻辑。

### 2.3 引用、版本化与动态加载

```groovy
// 编译期注解引用（最常用）—— 版本 = Git 分支/tag/commit hash
@Library('my-shared-library') _            // 用 Default version
@Library('my-shared-library@v2.3') _       // 显式锁定版本（推荐）
@Library(['lib-a', 'lib-b@main']) _        // 多库一次引入
```

```groovy
// 运行时动态加载（共享库插件 2.7+），版本可用变量
library "my-shared-library@${BRANCH_NAME}"
// 完全动态检索（SCM 都运行时给）
library identifier: 'custom-lib@main', retriever: modernSCM(
    [$class: 'GitSCMSource', remote: 'git@git.example.com:ops/jenkins-libs.git',
     credentialsId: 'jenkins-lib-key'])
```

### 2.4 Global Pipeline Libraries 配置项

| 配置项 | 说明 |
| --- | --- |
| Load implicitly | 勾选后无需 `@Library` 全局可用（用 Default version） |
| Default version | 未指定 `@版本` 时的默认版本（建议指向稳定 tag） |
| Allow default version to be overridden | 允许 `@Library('lib@x')` 覆盖默认版本 |
| Retrieval method | Modern SCM（Git/SVN，首选）或 Legacy SCM（URL 中嵌 `${library.库名.version}`） |
| 缓存 | Versions to exclude/include 控制哪些版本绕过缓存 |

> [!tip]
> 用 library 步骤动态加载的 src 类**不能静态 import**，要全限定名调用（`lib().org.demo.Utils.someStaticMethod()`），且同一库不能加载两次。测试库的 PR 可直接 `@Library('lib@pull/<PR号>/head') _` 验证，不影响主干用户。

## 三、实战案例：通知 + 构建 + 部署三步封装（Jenkins LTS 2.580.2）

```groovy
// vars/notifyWecom.groovy —— 封装企业微信机器人通知
def call(String result) {
    def color = (result == 'SUCCESS') ? 'info' : 'warning'
    def msg = "【${result}】${env.JOB_NAME} #${env.BUILD_NUMBER} ${env.BUILD_URL}"
    sh """curl -s -X POST 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${WECOM_KEY}' \
          -H 'Content-Type: application/json' \
          -d '{"msgtype":"text","text":{"content":"${msg}"}}'"""
}
```

```groovy
// vars/buildDockerImage.groovy —— 标准镜像构建推送（凭据见 [[Jenkins-凭据与安全]]）
def call(Map cfg = [:]) {
    def registry = cfg.get('registry')
    def image    = cfg.get('image', "${registry}/${env.JOB_BASE_NAME}:${env.BUILD_NUMBER}")
    def credId   = cfg.get('credId', 'docker-registry-cred')
    docker.withRegistry("https://${registry}", credId) {
        def app = docker.build(image, '.')
        app.push()
        app.push('latest')
    }
}
```

```groovy
// vars/deployK8s.groovy —— resources 模板渲染 + kubectl 应用
def call(Map cfg = [:]) {
    def manifest = libraryResource('templates/deploy.yaml')
    writeFile file: "deploy-${cfg.env}.yaml", text: manifest
    sh "kubectl -n ${cfg.namespace} set image deploy/${cfg.app} " +
       "${cfg.app}=${cfg.image} && kubectl -n ${cfg.namespace} rollout status deploy/${cfg.app}"
}
```

业务 Jenkinsfile 退化为编排层：

```groovy
@Library('platform-pipeline-libs@v2.3') _    // 锁定版本

pipeline {
    agent { label 'docker' }
    environment { WECOM_KEY = credentials('wecom-webhook-key') }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('构建')     { steps { buildJava(app: 'order-service') } }
        stage('镜像')     { steps { buildDockerImage(registry: 'registry.example.com') } }
        stage('部署')     { steps { deployK8s(env: 'staging', namespace: 'demo',
                                               app: 'order-service',
                                               image: "registry.example.com/order-service:${env.BUILD_NUMBER}") } }
    }
    post { always { notifyWecom(currentBuild.currentResult) } }
}
```

## 四、动手练习

1. **入门**：建一个共享库仓库，写 `vars/hi.groovy`（`def call(name)` 返回问候），业务流水线用 `@Library('…') _` 调用。提示：先配 Global Pipeline Libraries 再写 Jenkinsfile。
2. **Map 参数**：把 `hi` 改造成 `def call(Map cfg=[:])`，支持 `greeting` 与 `name` 两个可省略参数，缺 name 时 `error('name 必填')`。
3. **加文档**：为 `hi` 写同名 `hi.txt`，重跑一次构建后在 Global Variable Reference 页确认文档已生成。
4. **资源模板**：新增 `resources/templates/notice.md`，用 `libraryResource` 读取并 `writeFile` 落盘，作为通知正文。
5. **综合**：把你现有个项目 Jenkinsfile 中的"测试报告收集 + 归档 + 通知"抽成 `vars/ciReport.groovy`，并在 src 下写一个 `@NonCPS` 的 JSON 解析工具类处理报告摘要。

> [!success]- 第 5 题参考答案要点
> - `vars/ciReport.groovy` 的 call 内实现 junit 收集 → archiveArtifacts 归档 → notifyXxx 通知三段式，参数 Map 化。
> - src 工具类实现 `Serializable`，构造器接收 steps；解析方法标注 `@NonCPS` 且内部不调任何步骤。
> - Jenkinsfile 侧 `@Library('lib@tag') _` 锁版本；post 中 `always { ciReport(env: 'prod') }`。
> - 验证方式：故意让单测失败，确认报告仍被收集、通知发出（post always 生效）。

## 五、常见坑与 FAQ

> [!warning] 双引号里的 Groovy 变量在 shell 里没生效
> `sh "echo ${VAR}"` 是 Groovy 先求值 `VAR`（为 null 或空）；想要 shell 变量请用单引号 `sh 'echo $VAR'`。共享库封装 sh 时这是最高频事故，建议封装层统一约定引号规则。

> [!warning] trusted 库改动后没生效 / Replay 不生效
> Trusted 库不支持 Replay 调试（untrusted 才支持），且默认有版本缓存——改完库要等缓存刷新或换 commit 版本号引用。开发期建议把库配成 Folder 级沙箱库先跑通，再合入 trusted 主库。

> [!tip] cps method mismatch 报错速修
> 对 Jenkins 内部集合对象调 `.entrySet()`/`.containsKey()`、用闭包排序集合、JsonSlurper 解析时抛 CPS 相关异常 → 给该方法加 `@NonCPS`。但如果方法内调用了步骤（sh/echo），加注解反而报错——把步骤调用拆出去。

> [!tip] 版本管理纪律
> Default version 永远指向稳定 tag 而不是 master；库内改动遵循"先出 tag 再改引用"，杜绝所有项目 implicitly 跟踪 main 分支——共享库改坏等于全站流水线瘫痪。

## 六、自检清单

- [ ] 共享库独立 Git 仓库，受保护分支 + PR 评审
- [ ] vars 文件名全部 camelCase，对外步骤均有同名 .txt 文档
- [ ] @Library 显式锁定版本（tag/commit），未裸用默认分支
- [ ] src 类实现 Serializable 且通过构造器传入 steps
- [ ] 纯计算方法标注 @NonCPS，且不调用流水线步骤
- [ ] vars 保持"薄"，复杂逻辑下沉 src 并可单元测试
- [ ] trusted 库写权限已收紧到管理员级别
- [ ] 业务 Jenkinsfile 保持在 20 行左右的编排层

## 七、关联笔记与参考

**关联**：[[Jenkins-Jenkinsfile语法详解]]（vars 步骤的调用方）、[[Jenkins核心要点与最佳实践]]（架构与安全）、[[Jenkins-凭据与安全]]（docker.withRegistry 凭据）、[[Jenkins-分布式构建与K8s动态Agent]]（deployK8s 的落点）。

**参考资料**：

1. Jenkins 官方 - Extending with Shared Libraries：https://www.jenkins.io/doc/book/pipeline/shared-libraries/
2. Jenkins 官方 - Pipeline CPS Method Mismatches（@NonCPS 官方说明）：https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches
3. CloudBees - Pipeline Best Practices（@NonCPS 使用约束）：https://docs.cloudbees.com/docs/cloudbees-ci/latest/pipelines/pipeline-best-practices
4. OSCHINA - Jenkins共享库实战开发与最佳实践（2025）：https://my.oschina.net/emacs_7991204/blog/19216099
