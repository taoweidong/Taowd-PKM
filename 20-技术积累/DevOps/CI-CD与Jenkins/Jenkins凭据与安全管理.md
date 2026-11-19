---
title: Jenkins 凭据与安全管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - 凭据
  - 安全管理
  - CI/CD
aliases:
  - Jenkins 凭据管理
  - Jenkins 安全管理
source: 网络资料整理
---

# Jenkins 凭据与安全管理

> [!摘要] 摘要
> 本文聚焦 Jenkins 的凭据体系与安全加固：讲解 Credentials Plugin 的凭据类型、加密存储与掩码机制，`credentials()` / `withCredentials()` 的 Pipeline 用法，API Token 与权限（RBAC / Matrix）的落地配置，以及 CSP、CSRF、反序列化等安全能力的版本演进。适合需要在 Jenkins 中管理镜像仓库、SSH、云平台与部署凭证，并控制访问范围的运维与研发工程师。

## 一、最新动态（截至 2026-11）

- **版本基线**：生产推荐以 **LTS 2.580.x** 为基线，截至 2026-11 最新为 **2.580.2（2026-10-28 发布，安全修复版）**；**2.580.3** 的 RC 已于 2026-11-10/11 发布，正式版计划 2026-11-25 发布。**Weekly 最新为 2.591（2026-11-16 发布）**，主打变更为**默认启用内容安全策略（CSP）**（该能力自 2.539 引入）。
- **Java 硬约束**：**2.555.1（2026-04-15）起要求 Java 21 或 Java 25**，Java 17 不再支持。
- **API Token 支持过期日期**：自 **2.555.x** 起可用，便于对长期 Token 强制定期轮换。
- **安全能力持续收紧**：2.555.1 起**默认启用 `Overall/Manage` 权限**，CSRF crumb 不再包含客户端 IP；2.580.x 起默认**禁止 Object 字段反序列化**、引入密码复杂度规则。
- **安全公告**：2026 年全年共发布 **10 次**安全公告。其中 **CVE-2026-84651（2026-09-02）**：更新代理配置的 REST API 与 CLI 端点存在授权绕过，可跨代理覆盖配置并获取入站代理密钥，影响 2.579 及更早 / LTS 2.568.2 及更早，修复于 LTS 2.568.3 / Weekly 2.580，**需尽快升级**。
- 权威来源：[Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/)、[Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)。

## 二、基础概念

- **凭据（Credential）**：由 **Credentials Plugin** 提供的一类「命名 + 加密存储」的敏感数据，用于在流水线中向镜像仓库、云平台、服务器、SCM 等提供认证信息，避免明文散落在脚本里。
- **凭据类型**：用户名/密码、Secret text（纯文本密钥）、SSH 私钥、证书（PKCS#12）、Secret file、Token、Docker Host 证书认证等。

| 类型 | 典型用途 |
| --- | --- |
| 用户名/密码 | 私有镜像仓库、云平台控制台登录 |
| Secret text | API Key、访问令牌等纯文本密钥 |
| SSH 私钥 | 拉取私有仓库、登录远程主机执行部署 |
| Secret file | 需要以整文件形式挂载的密钥 |
| 证书（PKCS#12 等） | 客户端证书、Docker Host 证书认证 |
- **存储与掩码**：凭据以**控制器 ID 加密**存放在控制器上，流水线中**只按凭据 ID 引用**。敏感值在控制台日志中显示为 `****`，凭据 ID 中的敏感部分同样被掩码。
- **关键边界**：掩码机制**仅降低意外泄露风险，无法阻止恶意用户通过其他途径获取凭据值**。因此官方明确：**不要允许不受信任的流水线使用受信任凭据**。
- **权限模型**：Jenkins 采用基于权限（permission）的授权策略，凭据相关的常用权限为 `Credentials/View`、`Credentials/Use`、`Credentials/Create`、`Credentials/Update`、`Credentials/Delete`，另有控制脚本执行的 `Overall/RunScripts` 与控制全局配置的 `Overall/Manage`。

## 三、核心机制

**1. 凭据的创建与作用域。** 凭据可在 `Manage Jenkins > Credentials` 或文件夹级页面创建，作用域分为 **Global / System / User / 文件夹**，用于限制哪些任务与流水线可访问，降低跨项目泄露与在控制器间复制的风险。

**2. 两种使用方式。**

- `credentials('id')`：绑定为环境变量，适合「整个阶段都需要」的场景。
- `withCredentials([...]) { ... }`：在作用域内注入，作用域结束后不可再引用，适合「仅在某一步使用」的场景。

**3. 核心安全能力。**

- **CSRF 防护**：通过 crumb 防止跨站请求伪造；2.555.1 起 crumb 不再包含客户端 IP。
- **CSP**：内容安全策略自 2.541.1 引入、**2.591 起默认启用**，约束页面可加载的资源来源。
- **反序列化加固**：2.555.x 起默认禁止 Object 字段反序列化，降低插件注入风险。
- **API Token**：为 CLI / 脚本提供独立于用户密码的访问凭证，支持**过期日期**。
- **脚本安全**：不受信任的构建脚本受 Script Security Plugin 的 Groovy 沙箱约束。

## 四、实践步骤（含代码/命令示例）

**1. 通过 Configuration as Code 声明凭据（推荐，可版本化、可审计）。**

```yaml
# jenkins.yaml（JCasC）
credentials:
  system:
    - id: "registry-creds"
      description: "私有镜像仓库账号"
      username: "ci-robot"
      password: "${REGISTRY_PASSWORD}"
    - id: "deploy-ssh-key"
      description: "生产部署 SSH 私钥"
      privateKey: "${DEPLOY_SSH_KEY}"
```

**2. 在 Pipeline 中绑定凭据。**

```groovy
pipeline {
    agent any

    environment {
        // 仅按 ID 引用，禁止硬编码明文
        REGISTRY = credentials('registry-creds')
    }

    stages {
        stage('Build') {
            steps {
                // 拉取私有镜像时使用绑定变量
                sh "docker pull ${REGISTRY}:${env.APP_VERSION}"
            }
        }
    }
}
```

**3. 用 `withCredentials` 在作用域内使用凭据。**

```groovy
stage('Deploy') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'deploy-creds',
            usernameVariable: 'DEPLOY_USER',
            passwordVariable: 'DEPLOY_PASS'
        )]) {
            sh 'sshpass -p "$DEPLOY_PASS" ssh "$DEPLOY_USER"@host ./release.sh'
        }

        withCredentials([sshUserPrivateKey(
            credentialsId: 'deploy-ssh-key',
            keyFileVariable: 'SSH_KEY'
        )]) {
            sh 'ssh -i "$SSH_KEY" user@host ./healthcheck.sh'
        }
    }
}
```

**4. 管理 API Token（用于 CLI / 自动化脚本）。**

```bash
# 在 Manage Jenkins > Users > <user> > Configure > API Token 中生成，可设置过期日期
jenkins-cli -u ci-robot -webSocket jenkins-host -s / cli who-am-i
```

**5. 通过权限矩阵控制凭据访问（RBAC / Matrix 授权策略）。**

```text
用户/角色       Credentials/View  Credentials/Use  Overall/Manage  Overall/RunScripts
developer        ✓                 ✓(仅非生产ID)    ✗                ✗
release-bot     ✓                 ✓                ✗                ✗
admin           ✓                 ✓                ✓                ✓
```

**6. 检查凭据相关插件版本与安全状态（Script Console）。**

```groovy
// Script Console：列出凭据相关插件及版本
Jenkins.instance.pluginManager.plugins
    .findAll { it.shortName.toLowerCase().contains('credentials') }
    .each { println("${it.shortName}: ${it.version}") }
```

## 五、最佳实践与常见坑

- **绝不硬编码**：Jenkinsfile、Shell 脚本、CasC 明文里都不要写密钥；统一走凭据 ID，敏感值在日志中自动掩码。
- **最小权限**：用 RBAC / Matrix 授权策略精确分配 `Credentials/Use` 等权限，凭据作用域尽量收窄到用户或文件夹级。
- **隔离信任边界**：不受信任流水线（外部 PR、第三方分支）不得使用受信任凭据，必要时用独立控制器或受限文件夹隔离。
- **定期轮换**：利用 API Token 过期日期强制轮换；凭据变更通过 CasC 提交留痕，便于审计与回滚。
- **备份与介质保护**：凭据存放在控制器的 `credentials.xml` 等文件中，属于 `JENKINS_HOME` 备份的关键内容；备份文件同样含敏感信息，应存放到独立、受控的文件系统并加密，切勿落到 `/tmp` 或无保护的对象存储。
- **升级注意**：2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件，从旧版本升级后需手动补齐；**CVE-2026-84651** 影响 Agent 密钥安全，务必升级到 LTS 2.568.3 / Weekly 2.580 及以上。
- **常见坑**：凭据绑定失败多为作用域不匹配，或调用方缺少 `Credentials/View` / `Credentials/Use`；`withCredentials` 作用域外引用变量会为空；脚本式流水线中的闭包需可序列化，复杂逻辑应下沉到 Shared Library。

## 六、核心要点速查

1. 凭据由 **Credentials Plugin** 提供，支持用户名密码、Secret text、SSH 私钥、证书、Secret file、Token 等类型。
2. 凭据以控制器 ID 加密存储，**只按凭据 ID 引用**，敏感值日志显示 `****`。
3. 使用方式：`credentials('id')` 绑定环境变量、`withCredentials([...])` 在作用域内注入。
4. **掩码只防意外泄露，不防恶意用户**，不可让不受信任流水线使用受信任凭据。
5. 权限关键字：`Credentials/View`、`Credentials/Use`、`Overall/Manage`、`Overall/RunScripts`。
6. 截至 2026-11，LTS 最新为 **2.580.2**，Weekly 最新为 **2.591**（默认启用 CSP）。
7. **2.555.1 起要求 Java 21 / 25**；**API Token 支持过期日期**（2.555.x 起）。
8. **CVE-2026-84651**（2026-09-02）代理配置授权绕过，修复于 LTS 2.568.3 / Weekly 2.580。

## 七、学习资源

1. [Using credentials（Jenkins 官方·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
2. [Jenkins 安全（Jenkins 官方用户手册）](https://www.jenkins.io/doc/book/security/)
3. [Credentials 安全（Jenkins 官方用户手册）](https://www.jenkins.io/doc/book/security/credentials/)
4. [Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)
5. [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/)
6. [Jenkins Weekly 2.591 Changelog](https://www.jenkins.io/changelog/2.591/)
7. [Credentials 插件站](https://plugins.jenkins.io/credentials/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
