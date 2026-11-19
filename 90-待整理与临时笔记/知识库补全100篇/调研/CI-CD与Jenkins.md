---
title: CI/CD 与 Jenkins 调研
date: 2026-11-19
updated: 2026-11-19
tags:
  - 调研
  - CI/CD
  - Jenkins
  - DevOps
  - 自动化
---

# CI/CD 与 Jenkins 调研

> 调研范围：14 个「CI/CD 与 Jenkins」知识点的最新官方支持与关键事实，截至 2026-11。
> 用途：供后续写作 14 篇详细文档引用。
> 数据来源：Jenkins 官方文档（jenkins.io）、Jenkins 官方安全公告、Jenkins GitHub 仓库、Jenkins 插件仓库（plugins.jenkins.io）、官方 Docker 镜像等。

---

## 一、主题最新动态（截至 2026-11）

- **Jenkins 采用双发布线**：Weekly（每周）与 LTS（长期支持）。LTS 基线每 12 周从 Weekly 流中选取一次，随后每 4 周发布一个补丁（bug / 安全 / 小功能回移）。
- **当前版本状态**：
  - **Weekly 最新：2.591（2026-11-16 发布）**，主打变更为**默认启用内容安全策略（CSP）**（该能力自 2.539 引入，2.591 起默认生效）。
  - **LTS 最新：2.580.2（2026-10-28 发布）**，为安全修复版本；**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25 发布**。
  - **下一个 LTS 基线定于 2027-01-06**（新 Manage Jenkins UI 将随该基线正式进入 LTS）。
- **2.580.x LTS 系列的重大变更**：
  - **移除一批默认捆绑插件**（bouncycastle API、JUnit、Mailer、Matrix Authorization、Matrix Project、OWASP Markup Formatter、JavaMail、SSH server 等），`jenkins.war` 体积缩减 **40 MB+**；从 2.356 之前升级或检测到面向旧版本的插件时，需通过插件管理器手动安装这些插件。
  - **Winstone / Eclipse Jetty 持续升级至 Jetty 12.1.x**。
  - **API Token 支持过期日期**（2.555.x 起）。
- **Java 支持政策收紧**：**Jenkins 2.555.1 及以后要求 Java 21 或 Java 25，Java 17 不再支持**（2.555.1 起移除 Java 17 容器镜像）；此前测试配置为 JDK 21 / 25。
- **安全公告（2026 年）**：全年共发布 **10 次**安全公告，其中影响 Core 的包括：2026-10-28、2026-09-16、2026-09-02、2026-08-05、2026-06-24、2026-06-10、2026-05-27、2026-04-29、2026-03-18、2026-02-18。**CVE-2026-84651（2026-09-02）**：更新代理配置的 REST API 与 CLI 端点存在授权绕过，可跨代理覆盖配置并获取入站代理密钥，影响 2.579 及更早 / LTS 2.568.2 及更早，修复于 LTS 2.568.3 / Weekly 2.580。
- **Kubernetes 集成**：**Kubernetes 插件最新 1.35（活跃，EOL 2027-02-28）**，1.34 已 EOL。2026 年 10 月 Jenkins 官方「Plugin of the Month」专题即 Kubernetes 插件。**JKO（Jenkins Kubernetes Operator）v0.10.0-beta1（2026-11）**新增 Istio/Linkerd 服务网格支持、云身份（AWS IRSA、EKS Pod Identity、Azure Workload Identity、Google ADC）注入保护等。
- **官方 Docker 镜像**：LTS 线为 `jenkins/jenkins:2.580.2-lts`（jdk21 / jdk25），官方文档示例使用 `FROM jenkins/jenkins:2.580.2-jdk21`。

---

## 二、版本与关键事实表

| 版本号 | 类型 | 发布日期 | 关键变化 | 官方来源 URL |
| --- | --- | --- | --- | --- |
| 2.591 | Weekly | 2026-11-16 | 默认启用 CSP（#27727）；实验性任务 UI 改进；Ranged API 请求；修复多处 UI/队列/锁问题 | https://www.jenkins.io/changelog/2.591/ |
| 2.590 | Weekly | 2026-11-10 | 每周例行发布，bug 修复与 UI 改进 | https://github.com/jenkinsci/jenkins/releases/tag/jenkins-2.591 |
| 2.589 | Weekly | 2026-11-03 | 每周例行发布 | https://endoflife.date/jenkins |
| 2.588 | Weekly | 2026-10-28 | **安全修复**，对应 2026-10-28 安全公告 | https://github.com/jenkinsci/jenkins/releases |
| 2.580.2 | **LTS（当前最新）** | 2026-10-28 | **重要安全修复**；handlebars 4.7.10；Winstone/Jetty 12.1.14 | https://www.jenkins.io/changelog-stable/ |
| 2.580.1 | LTS | 2026-09-30 | 捆绑 Commons Lang 兼容；Winstone 8.1050.x / Jetty 12.1.13；slf4j 2.0.19 | https://www.jenkins.io/changelog-stable/ |
| 2.568.3 | LTS | 2026-09-02 | **重要安全修复**（含 CVE-2026-84651 代理配置授权绕过修复）；Winstone 8.1047.x / Jetty 12.1.12 | https://www.jenkins.io/changelog-stable/ |
| 2.568.2 | LTS | 2026-08-05 | **重要安全修复** | https://www.jenkins.io/changelog-stable/ |
| 2.568.1 | LTS | 2026-07-08 | Spring Security 7.1.0 / Spring Framework 7.0.8；移除 Windows 2019 控制器镜像；新增 Windows Server 2025 容器镜像 | https://www.jenkins.io/changelog-stable/ |
| 2.555.2 | LTS | 2026-05-13 | MSI 安装器改用「LF Open Source, LLC」签名（SmartScreen 提示）；Winstone / Jetty 12.1.8 | https://www.jenkins.io/changelog-stable/ |
| 2.555.1 | LTS | 2026-04-15 | **要求 Java 21 或 25，弃用 Java 17**；**API Token 支持过期日期**；默认启用 Overall/Manage 权限；CSRF crumb 不再包含客户端 IP | https://www.jenkins.io/changelog-stable/ |
| 2.541.3 | LTS | 2026-03-18 | **重要安全修复** | https://www.jenkins.io/changelog-stable/ |
| 2.541.2 | LTS | 2026-02-18 | **重要安全修复**；表单提交偶发错误修复 | https://www.jenkins.io/changelog-stable/ |
| 2.541.1 | LTS | 2026-01-21 | 更换 Linux RPM/DEB 仓库 GPG 签名密钥（需安装新密钥）；新增 Windows Server 2022 与 Java 25 容器镜像 | https://www.jenkins.io/changelog-stable/ |
| 2.580.3 | LTS | **预计 2026-11-25**（RC 2026-11-10） | 待发布正式版；2.580.x 线延续 | https://community.jenkins.io/t/platform-sig-november-17-2026/37690 |

> 补充：LTS 历史归档见 `https://www.jenkins.io/changelog-stable/` 页底部的 LTS changelog archive。

---

## 三、分知识点关键事实

### 1. CI/CD 理念与流水线模型

- **核心理念**：CI（持续集成）聚焦代码合入后自动构建与测试；CD（持续交付/持续部署）在此基础上自动完成发布。Jenkins 官方文档将自身定位为「自动化服务器」，覆盖构建、测试与部署环节。
- **流水线模型**：Jenkins Pipeline 是一套插件套件，将构建流程描述为「流水线」（Pipeline），并支持将其定义**代码化（Pipeline as Code）**，即用 Jenkinsfile 描述过程，纳入版本控制。
- **关键抽象**：`pipeline` → `stages` → `stage` → `steps`；支持 `agent`、`environment`、`options`、`parameters`、`triggers`、`post` 等指令。
- **权威来源**：
  - https://www.jenkins.io/doc/book/pipeline/
  - https://www.jenkins.io/doc/book/

### 2. Jenkins 架构与安装配置

- **架构**：经典 **Controller（控制器）+ Agent（代理）** 架构。Controller 负责调度、队列与 UI；Agent 负责实际执行构建。
- **安装方式**：Linux（apt/yum 仓库，`pkg.jenkins.io`）、Windows（MSI）、macOS、Docker、WAR（`java -jar jenkins.war`）、Servlet 容器、离线安装。
- **硬件/软件要求**：最低 256 MB RAM、1 GB 磁盘（Docker 建议 ≥10 GB）；**软件要求 Java 21 或更高**（见 Java Requirements）；推荐小型团队 4 GB+ RAM、50 GB+ 磁盘。
- **官方 Docker 镜像**：`jenkins/jenkins`，LTS 线 `jenkins/jenkins:2.580.2-lts`，可自定义镜像（`FROM jenkins/jenkins:2.580.2-jdk21`）。
- **关键参数/端口**：UI 默认 8080，Agent 入站 50000；`JENKINS_HOME` 为配置与数据目录。
- **权威来源**：
  - https://www.jenkins.io/doc/book/installing/
  - https://www.jenkins.io/doc/book/installing/docker/
  - https://www.jenkins.io/doc/book/installing/offline/
  - https://www.jenkins.io/download/

### 3. Jenkins 用户与权限管理

- **用户体系**：内置用户数据库；支持 LDAP、SAML、OpenID Connect 等外部认证（由相关插件提供），以及 GitHub/GitLab 等集成。
- **授权模型**：Jenkins 采用**基于权限（permission）的授权策略**，权限按角色/用户授予。常用授权策略包括 Role-Based Authorization Strategy（RBAC，需插件）与 Matrix-based。
- **关键权限**：`Overall/Read`、`Overall/Configure`、`Overall/Manage`（2.555.x 起默认启用）、`Job/Build`、`Job/Configure`、`Credentials/View`、`Credentials/Use`、`RunScripts` 等。
- **安全强化**：2.555.1 起**默认启用 `Overall/Manage` 权限**；密码复杂度规则与可配置密码校验扩展点；CSRF crumb 计算不再包含客户端 IP。
- **权威来源**：
  - https://www.jenkins.io/doc/book/security/
  - https://www.jenkins.io/changelog-stable/

### 4. Jenkins 插件管理

- **更新中心（Update Center）**：由 Jenkins 项目运营，提供开源插件清单；控制器默认**每 24 小时**检查一次更新，可在 `Manage Jenkins > Manage Plugins > Updates` 手动「Check now」。
- **插件格式**：`.hpi` 文件，含运行所需代码与资源。
- **安装方式**：Web UI（`Manage Jenkins > Manage Plugins > Available`，可勾选「Install without restart」）、Jenkins CLI `install-plugin` 命令、离线安装、JCasC（Configuration as Code）批量安装。
- **关键能力**：插件健康评分（Plugin Health Score，2.516.1 起在插件管理器展示）、禁用/启用插件、插件版本查看（Script Console：`Jenkins.instance.pluginManager.plugins.each { println("${it.getShortName()}: ${it.getVersion()}") }`）。
- **2.580.x 注意点**：**移除默认捆绑插件**，升级后如检测到面向旧版本的插件或从 2.356 之前升级，需通过插件管理器手动补齐（如 JUnit、Mailer、Matrix 等）。
- **权威来源**：
  - https://www.jenkins.io/doc/book/managing/plugins/
  - https://plugins.jenkins.io/

### 5. Jenkins 自由风格任务（Freestyle Job）

- **定位**：传统、配置驱动的构建任务类型，通过 Web UI 或 XML 配置，适合单任务、步骤简单、无需 Pipeline 的场景。
- **关键配置项**：源码管理（Git/SVN/Mercurial）、触发器（定时、SCM 轮询、上游构建）、构建环境、构建步骤（Shell、Ant、Maven、MSBuild 等）、后构建操作（归档、邮件、测试报告发布）、参数化构建（Parameters）。
- **与 Pipeline 对比**：自由风格为图形化/配置式；Pipeline 为代码化，适合复杂、多阶段、需要版本化与复用的工作流。官方推荐复杂场景使用 Pipeline。
- **安全提示**：自由风格的构建步骤若包含不受信任脚本，应配合 Script Security Plugin 的沙箱策略。
- **权威来源**：
  - https://www.jenkins.io/doc/book/pipeline/
  - https://www.jenkins.io/doc/book/managing/plugins/

### 6. Jenkins Pipeline 语法详解

- **两种语法**：**Scripted Pipeline**（脚本式，自由度/复杂度高）与 **Declarative Pipeline**（声明式，结构更规范、更易读，官方推荐大多数场景）。
- **Declarative 核心指令**：
  - `agent`：指定执行环境，可为 `any` / `none` / `label` / `docker` / `dockerfile` / `kubernetes`。
  - `stages` / `stage` / `steps`：阶段与步骤结构。
  - `options`：`timeout`、`retry`、`buildDiscarder`、`disableConcurrentBuilds`、`skipDefaultCheckout`、`timestamps`、`skipStage`、`waitForQueuedTask` 等。
  - `parameters`：`string`、`booleanParam`、`choice`、`password`、`file` 等，通过 `params` 对象访问。
  - `environment`：环境变量与凭据绑定。
  - `triggers`：`cron`、`pollSCM`、`upstream` 等。
  - `matrix`：矩阵构建（axes / excludes），配合 `parallel` 实现多维并行。
  - `parallel`：并行阶段，支持 `failFast true`（任一失败则中止全部）。
  - `post`：`always`、`success`、`failure`、`unstable`、`changed`、`cleanup` 等条件动作。
- **关键参数示例**：`timeout(time: 30, unit: 'MINUTES')`、`retry(2)`、`disableConcurrentBuilds()`。
- **权威来源**：
  - https://www.jenkins.io/doc/book/pipeline/syntax/
  - https://www.jenkins.io/doc/book/pipeline/

### 7. Jenkinsfile 编写实践

- **定义**：Jenkinsfile 是用 Groovy 语言编写的 Pipeline 源码文件，纳入 SCM 即实现「Pipeline as Code」。支持 **Declarative** 与 **Scripted** 两种语法。
- **加载方式**：SCM 中的 `Jenkinsfile` 或通过 `build` / `checkout` 参数指定路径；Multibranch Pipeline 自动按分支发现。
- **关键实践**：
  - 使用 Declarative 为主，脚本式用于复杂逻辑。
  - 合理使用 `agent none` + 阶段级 `container` 减少调度开销。
  - 用 `options { timeout(...) }`、`buildDiscarder(logRotator(...))` 控制资源与日志留存。
  - 用 `environment` 绑定凭据，避免明文暴露（敏感值在日志中显示为 `****`）。
  - 可调用 Pipeline 步骤参考（Pipeline Steps reference）校验可用步骤。
- **安全提示**：不要在 Jenkinsfile 中硬编码凭据；凭据应通过 `credentials` 绑定或 `withCredentials` 使用。
- **权威来源**：
  - https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
  - https://www.jenkins.io/doc/book/pipeline/syntax/

### 8. Jenkins Shared Library

- **作用**：将可复用的 Pipeline 代码抽取为共享库，供多个 Jenkinsfile 引用，避免重复，统一规范。
- **目录结构（官方要求）**：
  ```
  (root)
  +- src      # Groovy 源码，标准 Java 源目录结构，如 org/foo/Bar.groovy
  +- vars     # 全局变量脚本，如 foo.groovy、foo.txt（文档）
  +- resources # 外部库资源文件，通过 libraryResource 步骤加载（内部库不支持）
  ```
- **加载/引用**：在 Jenkinsfile 使用 `@Library('my-shared-library') _`；支持版本指定 `@Library('my-shared-library@1.0') _`；支持一次导入多个 `@Library(['lib1', 'lib2@tag']) _`。
- **配置位置**：可在 `Manage Jenkins > Configure System > Pipeline Libraries` 配置，或在 Multibranch 项目级别配置。
- **运行模型**：`vars/` 中的脚本按需以**单例**方式实例化；内部库受信任（无 Groovy 沙箱），外部库（SCM 加载）受沙箱约束。
- **权威来源**：
  - https://www.jenkins.io/doc/book/pipeline/shared-libraries/
  - https://github.com/jenkinsci/workflow-cps-global-lib-plugin

### 9. Jenkins Agent 与分布式构建

- **架构**：Controller 负责调度，Agent 负责执行；构建任务在 Agent 上运行，实现**分布式构建**。
- **Agent 连接方式**：**Inbound（入站，传统 JNLP / WebSocket，Agent 主动连 Controller）** 与 **Outbound（出站，Agent 通过 Remoting 反向连接，2.492 起默认）**。
- **动态 Agent**：可由云（Docker、Kubernetes、SSH、SSH 等）按需动态创建。
- **安全关键项**：入站 Agent 使用**入站代理密钥（inbound agent secret）**；**CVE-2026-84651（2026-09-02）**揭示更新代理配置的 REST API/CLI 存在授权绕过，可跨代理接管配置并获取入站密钥，修复于 2.568.3 / 2.580，需尽快升级。
- **关键参数**：`label`（节点标签，用于任务与 Agent 匹配）、`executors`（并发数）、`remoting.jar`（Agent 端，2.555.x 起最低支持 3176.v207ec082a_8c0）、离线/在线状态与原因。
- **权威来源**：
  - https://www.jenkins.io/doc/book/using/
  - https://www.jenkins.io/doc/pipeline/steps/kubernetes/
  - https://www.jenkins.io/security/advisories/

### 10. Jenkins 凭据与安全管理

- **凭据体系**：由 **Credentials Plugin** 提供，支持用户名/密码、Secret text、SSH 密钥、证书、Secret file、Token 等多种类型，凭据存储在 Jenkins 中并以**加密 + 掩码**方式使用。
- **使用方式**：Pipeline 中通过 `environment { AWS_ACCESS_KEY_ID = credentials('cred-id') }` 绑定；通过 `withCredentials([usernamePassword(...)]){ ... }` 在作用域内使用。
- **安全行为**：敏感值在控制台日志中显示为 `****`；凭据 ID 本身的敏感部分同样被掩码。**该机制仅降低意外泄露风险，无法阻止恶意用户通过其他途径获取凭据值**，因此**不要允许不受信任的流水线使用受信任凭据**。
- **关键安全能力**：API Token（支持过期日期）、CSRF 防护、内容安全策略（CSP，2.591 起默认启用）、禁用反序列化 Object 字段（2.555.x 起默认）、`Overall/Manage` 默认启用、密码复杂度规则。
- **权威来源**：
  - https://www.jenkins.io/doc/book/using/using-credentials/
  - https://www.jenkins.io/doc/book/security/
  - https://www.jenkins.io/security/advisories/

### 11. Jenkins 与 Kubernetes 集成（JKO）

- **Kubernetes 插件**：连接 Controller 与 Kubernetes 集群，用 **pod template** 按需动态创建 Agent Pod，构建完成后销毁。**当前版本 1.35（活跃，EOL 2027-02-28）**；1.34 已 EOL。
- **核心步骤**：`kubernetes { ... }` 与 `podTemplate { ... }`，支持 `label`、`namespace`、`nodeSelector`、`nodeUsageMode`、`containerTemplate`、`defaultContainer`、`yamlFile`、`imagePullSecrets`、`idleMinutes`、`podRetention`、`instanceCap` 等参数。
- **重要变更**：`containerTemplate` 已**弃用**，官方推荐改用 **YAML 格式**（`yamlFile`）定义 Pod 模板。
- **扩展插件**：Kubernetes Ephemeral Container 插件，可在 Agent Pod 内运行临时容器执行步骤（类似 `withDockerContainer`），适用于无 Docker 守护进程的集群。
- **JKO（Jenkins Kubernetes Operator）**：Kubernetes 原生 Operator，声明式管理 Jenkins 实例，支持 JCasC 配置、开箱安全加固。**v0.10.0-beta1（2026-11）**新增 Istio/Linkerd 服务网格支持、云身份注入（AWS IRSA / EKS Pod Identity / Azure Workload Identity / Google ADC）保护。
- **权威来源**：
  - https://plugins.jenkins.io/kubernetes/
  - https://www.jenkins.io/doc/pipeline/steps/kubernetes/
  - https://github.com/jenkinsci/kubernetes-operator
  - https://www.jenkins.io/blog/2026/10/18/plugin_month_october/

### 12. Jenkins 测试集成与质量门禁

- **测试报告集成**：**JUnit 插件**提供发布器，消费构建生成的 **JUnit/TestNG XML 报告**，提供历史趋势、测试报告 Web UI、失败追踪等能力。JUnit 插件自 Jenkins 1.577 起从核心拆出。
- **关键参数**：`testResults`（Ant glob 路径，如 `**/build/test-reports/*.xml`）、`allowEmptyResults`、`checksName`、`healthScaleFactor`（健康评分放大因子，默认 1.0）。
- **质量门禁**：通过 `junit` 步骤发布测试结果，结合 `post { failure { ... } }` 或 `unstable` 状态实现门禁；可与 Checkstyle、PMD、SpotBugs、SonarQube Scanner 等质量插件集成形成门禁。
- **Pipeline 用法**：`junit '**/build/test-reports/*.xml'`。
- **权威来源**：
  - https://plugins.jenkins.io/junit/
  - https://www.jenkins.io/doc/pipeline/steps/junit/
  - https://www.jenkins.io/doc/book/pipeline/syntax/

### 13. Jenkins 部署自动化（蓝绿/滚动）

- **实现思路**：Jenkins 本身不内置特定部署策略，通过 Pipeline 调用部署工具/脚本实现**蓝绿部署**（同时维护两套环境，通过负载均衡/路由切换流量）与**滚动部署**（逐批替换实例）。
- **典型实践**：
  - 使用 `sh` / `ssh` 步骤调用 kubectl、Helm、Ansible 等执行发布。
  - 用 `environment` 或 `params` 区分环境与策略；用 `input` 步骤实现部署审批门禁（`submitter` 可指定审批人）。
  - 关注部署的原子性与回滚：镜像使用**不可变 digest**，避免生产使用可变标签。
  - 结合 Kubernetes 插件，可用滚动更新（RollingUpdate）或蓝绿（如配合 Istio/Flagger）实现。
- **官方参考**：Jenkins 官方 Handbook 与 Pipeline 文档提供步骤与语法基础，部署策略需结合云/编排平台工具实现。
- **权威来源**：
  - https://www.jenkins.io/doc/book/pipeline/syntax/
  - https://plugins.jenkins.io/kubernetes/
  - https://www.jenkins.io/doc/book/pipeline/

### 14. Jenkins 备份与高可用

- **备份**：官方文档「Backing-up/Restoring Jenkins」指出备份用于**灾难恢复、恢复旧配置、恢复损坏/误删文件**。
  - **文件系统快照**：一致性最高、速度快，支持 LVM、btrfs、Solaris ZFS、OpenZFS 等。
  - **备份插件**：开源插件中仅 **thinBackup Plugin** 仍在维护；其他插件可能失修。
  - **Shell 脚本 + cron**：复制关键文件与目录；**不要备份到 `/tmp`**（重启可能被清理）；建议独立文件系统。
- **需备份的关键内容**：`JENKINS_HOME`（含 config.xml、jobs、users、credentials.xml、plugins、secrets 等）。
- **高可用**：Jenkins 核心为单 Controller（无原生多活）；高可用通常通过**外部编排**实现，如 Kubernetes 上用 **JKO（Jenkins Kubernetes Operator）**管理、配合持久化存储与外部数据库/凭据，或通过负载均衡做只读/故障转移。**官方文档未提供「Jenkins 原生多 Controller 高可用」的直接方案**，写作时需明确说明这一限制。
- **权威来源**：
  - https://www.jenkins.io/doc/book/system-administration/backing-up/
  - https://github.com/jenkinsci/kubernetes-operator

---

## 四、写作要点与风险提示

### 写作要点

1. **版本锚点统一**：14 篇文档统一以 **LTS 2.580.x（2.580.2 为当前）** 为生产推荐基线，以 **Weekly 2.591** 为最新特性参考，避免各文档版本口径不一致。
2. **Java 版本是硬约束**：明确 **Java 21 或 25**，Java 17 已弃用（2.555.1 起），避免示例使用过时 JDK 导致运行失败。
3. **区分语法**：Scripted 与 Declarative Pipeline 需分篇或明确区分，Declarative 为官方主推，示例优先使用 Declarative。
4. **强调 Pipeline as Code 与共享库复用**：这是 Jenkins 现代化的核心，写作中应突出 Jenkinsfile 版本管理与 Shared Library 目录规范（`src` / `vars` / `resources`）。
5. **安全贯穿始终**：凭据不硬编码、日志掩码、Agent 密钥保护、CSP 默认启用等，需在每篇相关文档中给出安全提示。
6. **Kubernetes 集成用最新事实**：插件版本 1.35；`containerTemplate` 已弃用，示例改用 `yamlFile`/YAML 模板。
7. **测试与部署结合 Pipeline 语法**：质量门禁用 `junit` + `post` 条件；部署用 `input` 审批 + `sh`/`ssh`/`kubectl`。

### 风险提示

- **版本时效性**：Jenkins 每周发布，版本号随时变化；本调研截至 **2026-11**，写作时如已晚于该时间，需重新核对版本。**2.580.3（计划 2026-11-25）与下一个 LTS 基线（2027-01-06）**是两个临近节点。
- **捆绑插件移除**：2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件，从旧版本升级可能遇到插件缺失，需在升级/配置文档中明确提示手动安装。
- **安全漏洞**：**CVE-2026-84651**（代理配置授权绕过）影响面较广，涉及 Agent 安全管理，相关文档需提示升级到 2.568.3 / 2.580 及以上。
- **JKO 版本状态**：`v0.10.0-beta1` 为**测试性质**，生产使用需谨慎，写作中应标注「beta」。
- **凭据安全边界**：官方明确掩码仅降低意外泄露风险，无法阻止恶意用户；不可在文档中暗示凭据绝对安全。
- **高可用表述谨慎**：Jenkins 无原生多 Controller 高可用，写作时应避免夸大，准确表述为「通过外部编排/JKO + 持久化存储实现」。
- **来源可靠性**：优先引用 jenkins.io、plugins.jenkins.io、github.com/jenkinsci 等官方来源；非官方聚合站（如 endoflife.date、stack.watch）仅作交叉印证，不作为唯一依据。

---

## 附：主要来源清单

1. Jenkins LTS 变更日志：https://www.jenkins.io/changelog-stable/
2. Jenkins Weekly 2.591 变更日志：https://www.jenkins.io/changelog/2.591/
3. Jenkins 安全公告索引：https://www.jenkins.io/security/advisories/
4. Jenkins 官方手册：https://www.jenkins.io/doc/book/
5. 安装 Jenkins：https://www.jenkins.io/doc/book/installing/
6. Jenkins Docker 安装：https://www.jenkins.io/doc/book/installing/docker/
7. 离线安装：https://www.jenkins.io/doc/book/installing/offline/
8. Jenkins 安全：https://www.jenkins.io/doc/book/security/
9. 使用凭据：https://www.jenkins.io/doc/book/using/using-credentials/
10. 管理插件：https://www.jenkins.io/doc/book/managing/plugins/
11. Pipeline 概览：https://www.jenkins.io/doc/book/pipeline/
12. Pipeline 语法：https://www.jenkins.io/doc/book/pipeline/syntax/
13. 使用 Jenkinsfile：https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
14. 共享库：https://www.jenkins.io/doc/book/pipeline/shared-libraries/
15. 备份/恢复 Jenkins：https://www.jenkins.io/doc/book/system-administration/backing-up/
16. Kubernetes 插件：https://plugins.jenkins.io/kubernetes/
17. Kubernetes 流水线步骤：https://www.jenkins.io/doc/pipeline/steps/kubernetes/
18. JKO（Jenkins Kubernetes Operator）：https://github.com/jenkinsci/kubernetes-operator
19. JUnit 插件：https://plugins.jenkins.io/junit/
20. JUnit 流水线步骤：https://www.jenkins.io/doc/pipeline/steps/junit/
21. Jenkins 下载页：https://www.jenkins.io/download/
22. Jenkins GitHub Releases：https://github.com/jenkinsci/jenkins/releases
23. Jenkins Docker 镜像仓库：https://github.com/jenkinsci/docker
24. 版本生命周期参考（交叉印证）：https://endoflife.date/jenkins
25. Plugin of the Month – Kubernetes Plugin（2026-10）：https://www.jenkins.io/blog/2026/10/18/plugin_month_october/
