---
title: Jenkins Shared Library
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 流水线
  - 共享库
aliases:
  - Jenkins 共享库
  - Jenkins 共享流水线库
  - Shared Library
source:
  - 网络资料整理
---

# Jenkins Shared Library

> [!摘要] 摘要
> 本文聚焦 Jenkins 的 **Shared Library（共享库）**：如何用 `src/`、`vars/`、`resources/` 三个目录组织可复用的 Pipeline 代码，如何用 `@Library` 注解与 `library` 步骤在 Jenkinsfile 中加载，以及 trusted / untrusted 信任模型、全局变量状态管理、自定义步骤与版本治理等落地要点。它是「Pipeline as Code」从「能跑」走向「可复用、可维护、可标准化」的核心一环，适合已掌握 Jenkinsfile 语法、希望在团队内沉淀流水线公共能力的工程师。

## 一、最新动态（截至 2026-11）

- **版本锚点**：截至 2026-11，Jenkins **LTS 最新为 2.580.2**（2026-10-28 发布，含重要安全修复）；**Weekly 最新为 2.591**（2026-11-16 发布，默认启用内容安全策略 CSP）。生产建议以 **2.580.x LTS** 为基线。
- **Java 硬约束**：**2.555.1（2026-04-15）起要求 Java 21 或 Java 25，Java 17 不再支持**。构建共享库的 Agent 与运行控制器均需满足该要求，示例中不要沿用过时 JDK。
- **共享库实现插件**：共享库由 `Pipeline: Shared Groovy Libraries` 插件（仓库 `workflow-cps-global-lib-plugin`）提供。调研文件未给出该插件的独立版本号与更新节奏，**具体版本以官方插件仓库为准**。
- **2.580.x 重要变更**：移除一批默认捆绑插件（bouncycastle API、JUnit、Mailer、Matrix Authorization、Matrix Project、OWASP Markup Formatter、JavaMail、SSH server 等），`jenkins.war` 体积缩减 **40 MB+**；从 2.356 之前升级或检测到面向旧版本的插件时，需通过插件管理器手动补齐。
- **信任与权限**：全局共享库的 **trusted** 配置需要 `Overall/RunScripts` 权限，**untrusted** 仅需 `Overall/Manage`；2.555.1 起默认启用 `Overall/Manage` 权限。
- **官方镜像**：LTS 线为 `jenkins/jenkins:2.580.2-lts`（jdk21 / jdk25），官方文档示例使用 `FROM jenkins/jenkins:2.580.2-jdk21`。

## 二、基础概念

**Shared Library（共享库）** 是 Jenkins 为 Pipeline 提供的代码复用机制：把多个项目里反复出现的构建、测试、部署逻辑从 Jenkinsfile 中抽离出来，放进一个独立的源码仓库，由所有流水线按需加载，从而实现 **DRY（不要重复自己）**、统一规范、集中维护。

理解它需要抓住三个概念：

- **库的载体是仓库**：共享库本身就是一个普通源码仓库，通常与业务代码分开管理，通过 SCM（Git、Subversion 等）拉取。
- **库的代码分两类**：`src/` 里的是 **Groovy 类**（进 classpath，可被 import）；`vars/` 里的是 **全局变量脚本**（文件名即变量名，直接当步骤调用）。
- **加载方式有两种**：**编译期静态加载**（`@Library` 注解）与 **运行期动态加载**（`library` 步骤），前者类型检查友好，后者更灵活。

> [!note] 内部库与外部库
> **内部库（Internal Library）** 直接配置在控制器上，加载时不受 Groovy 沙箱约束，可调用 Java / Groovy / Jenkins 内部 API；**外部库（External Library）** 从 SCM 仓库拉取，默认在 Groovy 沙箱内运行，行为与普通 Pipeline 脚本一致。选型时先明确库的信任等级。

## 三、核心机制

### 3.1 目录结构（官方约定）

| 目录 | 内容 | 说明 |
| --- | --- | --- |
| `src/` | Groovy 源码，标准 Java 源目录结构 | 如 `src/org/foo/Bar.groovy` 对应类 `org.foo.Bar`，编译时加入 classpath |
| `vars/` | 全局变量脚本 | 如 `vars/foo.groovy` 对应全局变量 `foo`；同名 `vars/foo.txt` 作为该变量的文档 |
| `resources/` | 外部资源文件 | **仅外部库支持**，通过 `libraryResource` 步骤加载；内部库不支持 |

根目录下的其他目录为官方保留，供未来扩展使用，不要自行占用。

### 3.2 加载模型：注解与步骤

**编译期加载（`@Library` 注解）**：库在脚本编译前解析，因此其中的类可用于类型声明、静态导入。

```groovy
// 基本加载
@Library('my-shared-library') _

// 指定版本（分支、标签、commit 均可）
@Library('my-shared-library@1.0') _

// 一次加载多个库
@Library(['lib-a', 'lib-b@abc1234']) _

// 引入类库时，注解习惯放在 import 上
@Library('somelib')
import com.mycorp.pipeline.somelib.UsefulClass
```

**运行期动态加载（`library` 步骤）**：自 `Pipeline: Shared Groovy Libraries` 插件 **2.7** 起提供，可在构建任意时刻加载。因为脚本已编译完成，此时**不能 import 或静态引用**库中的类，只能通过全限定名动态访问。

```groovy
// 仅使用 vars 中的全局变量，语法简单
library 'my-shared-library'

// 动态指定版本，版本可以是变量
library "my-shared-library@${params.LIB_VERSION}"

// 动态指定检索方式，库无需预先在 Jenkins 中配置
library identifier: 'custom-lib@master', retriever: modernSCM(
    [$class: 'GitSCMSource',
     remote: 'git@git.mycorp.com:my-jenkins-utils.git',
     credentialsId: 'my-private-key'])

// 通过返回值按全限定名访问类
library('my-shared-library').com.mycorp.pipeline.Utils.someStaticMethod()
```

### 3.3 vars 的单例与调用模型

`vars/` 下的脚本**按需实例化为单例**，一个文件可定义多个方法。要让它像内置步骤一样被调用，需实现 `call` 方法，且全局变量名须为全小写或 camelCase。

```groovy
// vars/sayHello.groovy
def call(String name = 'human') {
    echo "Hello, ${name}."
}
```

```groovy
// 使用
@Library('utils') _
sayHello 'Joe'
sayHello()          // 使用默认参数
```

接收闭包的步骤则把闭包作为参数，适合封装「切换到某类节点执行」的逻辑：

```groovy
// vars/windows.groovy
def call(Closure body) {
    node('windows') {
        body()
    }
}
```

### 3.4 信任模型与权限

- **trusted（受信任）**：可调用任意 Java / Groovy / Jenkins 内部 API、插件与第三方库，**不受 Groovy 沙箱限制**。配置需要 `Overall/RunScripts` 权限（通常授予 Jenkins 管理员）。官方警告：**任何能向该 SCM 仓库提交代码的人都将获得 Jenkins 的无限访问权限**，因此受信任库的仓库必须严格管控写权限。
- **untrusted（不受信任）**：在 Groovy 沙箱内运行，与普通 Pipeline 脚本一致，仅需 `Overall/Manage` 权限即可配置。
- 可在 `Manage Jenkins > Configure System`（新版 UI 为 `Manage Jenkins > System > Global Trusted Pipeline Libraries`）配置全局库，也可在 **Multibranch / 文件夹级别**配置，后者作用域更小。

### 3.5 状态、序列化与资源

- 类中保存状态时**必须实现 `Serializable`**，否则 Pipeline 无法正确挂起与恢复。
- **全局变量应保持无状态**，只作为函数集合；状态会因控制器重启而丢失，需要状态时改用静态类或局部变量。仅作只读常量字段时，须加 `@groovy.transform.Field` 注解。
- 外部库可用 `libraryResource` 读取 `resources/` 下的文件，返回字符串，常配合 `writeFile` 落盘。

```groovy
def request = libraryResource 'com/mycorp/pipeline/somelib/request.json'
```

### 3.6 库内定义声明式流水线

自 **Declarative 1.2（2017 年 9 月）**起，可在共享库中定义完整的声明式流水线，但**只能在 `vars/*.groovy` 的 `call` 方法中**，且**单次构建只能执行一条流水线**，尝试执行第二条会导致构建失败。

## 四、实践步骤

**步骤 1：创建库仓库并组织目录**

```bash
# 初始化共享库仓库（示例）
mkdir -p my-shared-library/{src/com/mycorp/pipeline,vars,resources/com/mycorp/pipeline}
cd my-shared-library
git init && git add -A && git commit -m "init shared library"
```

**步骤 2：编写 `vars/` 全局步骤**

```groovy
// vars/buildApp.groovy
def call(Map config) {
    node {
        git url: config.repo, branch: config.branch
        sh "./mvnw -B clean package -DskipTests=false"
        junit '**/target/surefire-reports/*.xml'
    }
}
```

**步骤 3：编写 `src/` 中的可复用类**

```groovy
// src/com/mycorp/pipeline/Utilities.groovy
package com.mycorp.pipeline

class Utilities implements Serializable {
    def steps
    Utilities(steps) { this.steps = steps }

    def mvn(String args) {
        steps.sh "${steps.tool 'Maven'}/bin/mvn -o ${args}"
    }
}
```

**步骤 4：在 Jenkins 中配置库**

在 `Manage Jenkins > Configure System`（或文件夹级别）新增共享库：填写 **Name**、**Retrieval method**（推荐 Modern SCM，Git / Subversion 插件已支持）、可选的 **Default version**；勾选 **Load implicitly** 则所有流水线可直接使用，无需写 `@Library`。若勾选了 **Allow default version to be overridden**，`@Library` 中可覆盖默认版本。

**步骤 5：在 Jenkinsfile 中引用**

```groovy
pipeline {
    agent any

    // 静态加载：带版本号，推荐生产使用固定版本（标签/commit）
    @Library('my-shared-library@1.0') _

    stages {
        stage('Build') {
            steps {
                // 直接调用库中的全局步骤
                buildApp repo: 'git@git.mycorp.com:app/demo.git', branch: 'main'
            }
        }
    }

    post {
        failure {
            echo "构建失败：${currentBuild.result}"
        }
    }
}
```

> [!tip] 声明式中的全局变量调用
> 声明式 Pipeline 不允许在 `script` 块之外直接对对象调用方法。若 `vars/` 脚本的方法需要在声明式中调用，请把调用放进 `script { }` 指令内，否则会报错。

```groovy
stage('Example') {
    steps {
        script {
            log.info 'Starting'
            log.warning 'Nothing to do!'
        }
    }
}
```

**步骤 6：用 Replay 与 PR 测试库变更**

- 对 **untrusted** 库，构建失败时点击构建页的 **Replay** 链接即可在构建内直接编辑源码试跑（**trusted 库不支持 Replay**，修改资源文件也不支持）。
- 库托管在 GitHub 时，可在消费者 Jenkinsfile 顶部写 `@Library('my-shared-library@pull/123/head') _`，在构建中实测某个 PR 的改动。

## 五、最佳实践与常见坑

**最佳实践**

- **全局变量保持无状态**：只做函数集合，状态放入静态类或局部变量，这是生产级库治理的强制要求。
- **版本策略统一**：生产用**标签或固定 commit** 固定库版本，测试用分支，避免「同一名称、版本漂移」导致结果不可复现。
- **优先 Modern SCM**：配置库时选择 Modern SCM 检索方式，旧版 SCM 插件需使用 Legacy SCM 并配置 `${library.<名称>.version}` 变量。
- **能力分层**：把「怎么做」封装进库（如 `buildPlugin`、`buildApp`），让业务 Jenkinsfile 只描述「做什么」，形成高层 DSL。
- **不要在库中用 `@Grab` 拉取第三方依赖**：官方不推荐，第三方库默认缓存在控制器的 `~/.groovy/grapes/`。更稳妥的做法是把可执行程序安装到 Agent 上，再用 `sh` / `bat` 调用。
- **文档同步**：为 `vars/` 中的每个变量提供同名 `.txt` 文档，成功构建后会出现在 Global Variable Reference 页面。

**常见坑**

- **声明式里直接调库方法报错**：必须在 `script { }` 块内调用全局变量方法（见上文 tip）。
- **`library` 步骤无法 import 类**：动态加载发生在编译之后，只能按全限定名动态访问，不能做静态类型声明。
- **全局变量存状态后重启丢失**：控制器重启后状态不保留，务必改用类或局部变量。
- **未设 Default version 又省略版本**：若未配置默认版本，`@Library('lib') _` 这种只写名称的写法会因缺少版本而报错，必须写成 `@Library('lib@master') _`。
- **implicitly 加载的库不能被 `library` 步骤换版本**：隐式加载在脚本启动前已完成，同名库不能二次加载。
- **受信任库仓库写权限失控**：trusted 库能调用任意 Jenkins API，仓库一旦被写入即等同泄露 Jenkins 控制权，需严格控制分支保护与推送权限。
- **插件升级或捆绑插件移除导致加载失败**：2.580.x 移除了 JUnit、Mailer 等默认插件，若库中依赖这些步骤，升级后需手动安装对应插件。

## 六、核心要点速查

1. 共享库用于**复用 Pipeline 代码**，目录约定：`src/`（Groovy 类）、`vars/`（全局变量）、`resources/`（仅外部库可用）。
2. `vars/` 下**文件名即变量名**，脚本**按需实例化为单例**；`resources/` 通过 `libraryResource` 加载。
3. 加载方式：**`@Library('lib@版本') _`**（编译期，可带版本、可多库、可 import 类）与 **`library 'lib@版本'`**（运行期动态加载，不能静态引用类）。
4. 配置位置：`Manage Jenkins > Configure System`（新版为 `System > Global Trusted Pipeline Libraries`）或**文件夹/Multibranch 级别**；勾选 **Load implicitly** 可免注解直接使用。
5. 信任模型：**trusted** 无沙箱、需 `Overall/RunScripts`，**untrusted** 受沙箱约束、需 `Overall/Manage`；trusted 库仓库须严格管控写权限。
6. 带状态的类**必须实现 `Serializable`**；**全局变量应无状态**，只读常量字段需 `@groovy.transform.Field`。
7. 自定义步骤通过 `vars/` 的 `call` 方法实现，命名须全小写或 camelCase；接收闭包可实现「切换节点执行」类封装。
8. 库内**只能定义完整声明式流水线**，且只能在 `vars/*.groovy` 的 `call` 方法中，单次构建仅能执行一条。
9. **Replay** 仅支持 untrusted 库；**PR 测试**用 `@Library('lib@pull/<PR>/head') _`。
10. 生产用**标签/commit 固定库版本**，避免版本漂移；**不要使用 `@Grab`** 拉取第三方依赖。
11. 声明式中调用库方法须放入 **`script { }`** 块。
12. 版本基线：LTS **2.580.2**、Weekly **2.591**；**2.555.1 起要求 Java 21 / 25**，Java 17 已弃用。

## 七、学习资源

1. [Extending with Shared Libraries（Jenkins 官方手册·共享库）](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
2. [Pipeline Syntax（Jenkins 官方手册·流水线语法）](https://www.jenkins.io/doc/book/pipeline/syntax/)
3. [Pipeline 概览（Jenkins 官方手册）](https://www.jenkins.io/doc/book/pipeline/)
4. [使用 Jenkinsfile（Jenkins 官方手册）](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
5. [Pipeline: Shared Groovy Libraries 插件（workflow-cps-global-lib-plugin）](https://github.com/jenkinsci/workflow-cps-global-lib-plugin)
6. [Jenkins 插件站（查找 Pipeline 相关插件）](https://plugins.jenkins.io/)
7. [Jenkins LTS Changelog（版本动态）](https://www.jenkins.io/changelog-stable/)
8. [Jenkins 官方手册总览](https://www.jenkins.io/doc/book/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]
- [[DevOps与Kubernetes-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
