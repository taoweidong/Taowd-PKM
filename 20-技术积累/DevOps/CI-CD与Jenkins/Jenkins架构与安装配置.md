---
title: Jenkins 架构与安装配置
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 安装配置
  - 架构
aliases:
  - Jenkins 安装与配置
source:
  - 网络资料整理
---

# Jenkins 架构与安装配置

> [!摘要] 摘要
> 本文聚焦 Jenkins 的**架构模型**与**安装配置**两个落地基础：先厘清 Controller + Agent 的分布式架构、端口与目录等关键事实，再给出 Linux、Windows、WAR、Docker、离线与 Kubernetes 六种安装路径的完整命令与配置示例，并附升级、安全与常见坑的排查清单。适合准备搭建或迁移 Jenkins 环境的运维与研发工程师。版本口径统一锚定 **LTS 2.580.x（当前 2.580.2）**，最新特性参考 **Weekly 2.591**。

## 一、最新动态（截至 2026-11）

以下版本与日期均来自 Jenkins 官方渠道，未查到的细节一律以官方仓库为准。

- **双发布线**：Jenkins 采用 **Weekly（每周）+ LTS（长期支持）** 双轨。LTS 基线每 **12 周**从 Weekly 流中选取一次，之后每 **4 周**发布一个补丁（bug / 安全 / 小功能回移）。
- **Weekly 最新：2.591（2026-11-16 发布）**。最重要的变更是**默认启用内容安全策略（CSP）**——该能力自 2.539 引入，自 2.591 起默认生效。
- **LTS 最新：2.580.2（2026-10-28 发布）**，为安全修复版本；**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25 发布**。
- **下一个 LTS 基线定于 2027-01-06**，新的 Manage Jenkins UI 将随该基线正式进入 LTS。
- **2.580.x 的重大变更**：
  - **移除一批默认捆绑插件**（bouncycastle API、JUnit、Mailer、Matrix Authorization、Matrix Project、OWASP Markup Formatter、JavaMail、SSH server 等），`jenkins.war` 体积缩减 **40 MB+**；从 **2.356 之前**升级，或检测到面向旧版本的插件时，需通过插件管理器**手动安装**这些插件。
  - Winstone / Eclipse Jetty 持续升级至 **Jetty 12.1.x**。
  - **API Token 支持过期日期**（2.555.x 起）。
- **Java 政策收紧**：**2.555.1 及以后要求 Java 21 或 Java 25，Java 17 不再支持**；自 2.555.1 起已移除 Java 17 容器镜像。这是安装与升级的**硬约束**。
- **安全公告**：2026 年全年共发布 **10 次**安全公告。其中 **CVE-2026-84651（2026-09-02）**——更新代理配置的 REST API 与 CLI 端点存在**授权绕过**，可跨代理覆盖配置并获取**入站代理密钥**，影响 Weekly 2.579 及更早、LTS 2.568.2 及更早，修复于 LTS 2.568.3 / Weekly 2.580。**尚未升级的实例应尽快处理**。
- **Kubernetes 集成**：**Kubernetes 插件最新 1.35（活跃，EOL 2027-02-28）**，1.34 已 EOL；**JKO（Jenkins Kubernetes Operator）v0.10.0-beta1（2026-11）**新增 Istio/Linkerd 服务网格支持与云身份注入保护（AWS IRSA、EKS Pod Identity、Azure Workload Identity、Google ADC）。JKO 该版本为 **beta 测试性质**，生产使用需谨慎。
- **官方 Docker 镜像**：LTS 线为 `jenkins/jenkins:2.580.2-lts`（jdk21 / jdk25），官方文档示例使用 `FROM jenkins/jenkins:2.580.2-jdk21`。

## 二、基础概念

**1. Jenkins 的定位。** Jenkins 是一套**开源自动化服务器**，承担「构建 → 测试 → 部署」环节的自动化，是 CI/CD 流水线的运行时载体。其核心理念是**流水线即代码（Pipeline as Code）**：用 Groovy 编写的 Jenkinsfile 描述构建过程，纳入版本控制，从而可评审、可复用、可审计。

**2. Controller（控制器）与 Agent（代理）。** Jenkins 采用经典的**分布式架构**：

- **Controller（控制器）**：系统的「大脑」。承担 Web 服务、配置管理、认证授权、任务调度、队列与构建状态展示。
- **Agent（代理 / 节点）**：真正**执行构建任务**的工作节点，通过执行器（Executor）运行任务，实现**分布式构建**。
- **通信方式**：二者通过 **Remoting** 通信。构建产物默认写入控制器文件系统，也可外包给 Nexus / Artifactory 等制品库。

**3. Agent 的两种接入方向。**

| 方向 | 机制 | 说明 |
| --- | --- | --- |
| **Inbound（入站）** | 传统 JNLP / WebSocket，Agent 主动连 Controller | 需要控制器侧可达，使用**入站代理密钥（inbound agent secret）** |
| **Outbound（出站）** | Agent 通过 Remoting 反向连接 | **2.492 起为默认方式**，对网络边界更友好 |

**4. 关键参数与目录。**

| 项目 | 值 / 说明 |
| --- | --- |
| Web UI 端口 | 默认 **8080** |
| Agent 入站端口 | 默认 **50000** |
| 配置与数据目录 | **`JENKINS_HOME`**（含 config.xml、jobs、users、credentials.xml、plugins、secrets 等） |
| 节点标签 | `label`，用于任务与 Agent 匹配 |
| 并发数 | `executors`，控制单节点并行构建数 |
| Agent 端 | `remoting.jar`（2.555.x 起最低支持 `3176.v207ec082a_8c0`） |

## 三、核心机制

**1. 调度与执行分离。** Controller 负责接收构建请求、匹配节点、排队与状态维护；Agent 负责实际执行。构建在 Agent 上运行，因此**扩容能力 = 增加 Agent**，而控制器本身可保持轻量稳定。这种解耦是 Jenkins 能支撑大规模构建的架构基础。

**2. 动态 Agent 供给。** Agent 不一定是常驻物理机或虚拟机，可由云**按需动态创建**：Docker、Kubernetes、SSH 等。Docker 插件提供 `docker` / `dockerfile` agent；Kubernetes 插件通过 `podTemplate` / `yamlFile` 动态创建**一次性 Agent Pod**，构建完成即销毁，实现弹性伸缩。

**3. 安全机制（安装后必须理解）。**

- **入站代理密钥**：入站 Agent 的接入凭证。CVE-2026-84651 正是利用更新代理配置的授权绕过获取该密钥，务必升级到 **2.568.3 / 2.580 及以上**。
- **CSRF crumb**：防跨站请求伪造；2.555.1 起 crumb 计算**不再包含客户端 IP**。
- **内容安全策略（CSP）**：2.541.1 起为 UI 引入，**2.591 起默认启用**。
- **Object 字段反序列化**：2.580.x 起**默认禁止**，可能影响依赖反序列化的旧插件。
- **`Overall/Manage` 权限**：2.555.x 起**默认启用**。
- **API Token 过期日期**：2.555.x 起支持，便于凭据生命周期治理。

**4. 配置的载体。** 全局配置、节点、凭据、插件、Job 最终都落在 `JENKINS_HOME` 的文件结构中，因此**备份与迁移本质上都是对 `JENKINS_HOME` 的操作**。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境要求

- **软件**：**Java 21 或更高**（2.555.1 起不再支持 Java 17）。若计划使用 Java 25，需 2.541.1 及以上。
- **硬件**：最低 **256 MB RAM、1 GB 磁盘**（Docker 场景建议 **≥10 GB**）；小团队推荐 **4 GB+ RAM、50 GB+ 磁盘**。

### 4.2 Linux 安装（apt / yum）

```bash
# Debian / Ubuntu：添加官方仓库
wget -q -O - https://pkg.jenkins.io/debian/jenkins-io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

# RHEL / CentOS / Fedora
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins-io.key
sudo dnf install jenkins
```

### 4.3 WAR 方式（最轻量，适合快速试用）

```bash
# 需要 Java 21+
java -jar jenkins.war --httpPort=8080
```

### 4.4 Windows 安装

下载官方 MSI 安装包，通过图形化向导安装并注册为 Windows 服务。注意 2.555.2 起 MSI 安装器改用「LF Open Source, LLC」签名，安装时可能触发 SmartScreen 提示，属正常现象。

### 4.5 Docker 安装（推荐起步方式）

```bash
# 映射 Web 与入站 Agent 端口，挂载卷持久化 JENKINS_HOME
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  jenkins/jenkins:2.580.2-jdk21
```

官方镜像**不含 Docker CLI**，若流水线需调用 Docker，应使用自定义镜像：

```dockerfile
FROM jenkins/jenkins:2.580.2-jdk21
USER root
RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*
USER jenkins
```

### 4.6 首次初始化

访问 `http://<host>:8080`，初始管理员密码位于 `JENKINS_HOME/secrets/initialAdminPassword`：

```bash
# Docker 中读取初始密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

随后按向导**安装建议插件**、创建第一个管理员用户。若后续从 2.356 之前升级或遇到插件缺失，需在 `Manage Jenkins > Manage Plugins` 手动补装 JUnit、Mailer、Matrix 等。

### 4.7 添加一个 Agent（入站 WebSocket）

```bash
# 1. 在 Controller 上：Manage Jenkins > Nodes > New Node
#    选择 "Launch agent via WebSocket"，生成并复制启动命令
# 2. 在 Agent 主机上执行（Java 21+）
java -jar remoting.jar -url http://<controller>:8080 \
  -workDir /opt/agent-home -labels builder
```

在 Jenkinsfile 中按标签匹配：

```groovy
pipeline {
    agent { label 'builder' }
    stages {
        stage('Build') { steps { sh 'mvn -q clean package' } }
    }
}
```

### 4.8 备份配置（配置数据即 JENKINS_HOME）

```bash
# 使用文件系统快照（LVM / btrfs / ZFS），一致性最高、速度最快
# 若用脚本+cron，切勿备份到 /tmp（重启可能被清理），建议放独立文件系统
0 3 * * * tar -czf /backup/jenkins-$(date +\%F).tar.gz -C /var/jenkins_home .
```

## 五、最佳实践与常见坑

**最佳实践**

1. **版本口径统一**：生产以 **LTS 2.580.x** 为基线，新特性参考 Weekly。
2. **先确认 JDK 再装**：Java 17 环境须先迁移到 **Java 21/25**，否则启动失败。
3. **`JENKINS_HOME` 必须持久化**：容器场景务必挂载卷，避免重建后配置全丢。
4. **控制器与 Agent 分工清晰**：Controller 保持轻量稳定，构建压力交给 Agent，用 `label` 分类（编译 / 测试 / 部署）。
5. **安全配置前置**：开启 CSP、CSRF crumb，规范 API Token 过期策略，限制凭据与流水线作用域。
6. **升级前排查插件兼容性**：核对插件清单，留意捆绑插件移除与反序列化默认禁用的影响。

**常见坑**

- **Java 版本不符**：提示 `UnsupportedClassVersionError` 或启动即退出，多为 JDK 版本低于 21，需升级 JDK。
- **端口未映射 / 被占用**：UI 的 8080 与 Agent 入站的 50000 都要映射；Agent 连不上先排查端口与网络边界，必要时改用 **WebSocket**（无需映射 50000）。
- **升级后插件缺失**：从 2.356 之前升级，JUnit、Mailer、Matrix 等需手动补装，否则流水线步骤失效。
- **凭据绑定失败**：确认凭据类型与作用域，确认调用方对凭据具备读取权限。
- **构建卡在排队**：检查执行器数量、全局并发上限与节点标签是否匹配，避免 CPU / 内存 / IO 被打满。
- **Agent 密钥泄露风险**：CVE-2026-84651 说明代理配置接口存在授权绕过，未升级的实例应优先处理。
- **高可用误区**：**Jenkins 核心为单 Controller，无原生多活**。高可用需借助外部编排（如 Kubernetes 上用 JKO + 持久化存储），不要假设「双活自动切换」。

## 六、核心要点速查

1. 架构为 **Controller（调度 / 配置 / 安全）+ Agent（执行构建）**，通过 Remoting 通信，构成**分布式构建**。
2. Agent 接入分 **Inbound（JNLP / WebSocket）** 与 **Outbound（2.492 起默认）**；入站需**入站代理密钥**。
3. 关键端口：Web UI **8080**、Agent 入站 **50000**；数据目录为 **`JENKINS_HOME`**。
4. **2.555.1 起要求 Java 21 或 Java 25，Java 17 不再支持**。
5. 截至 2026-11，最新 LTS 为 **2.580.2**（2026-10-28），Weekly 为 **2.591**（2026-11-16，默认启用 CSP）。
6. **2.580.x 移除默认捆绑插件**、`jenkins.war` 缩减 40 MB+；从 2.356 之前升级需手动补装插件。
7. **CVE-2026-84651**（2026-09-02）为代理配置授权绕过，修复于 LTS 2.568.3 / Weekly 2.580。
8. 安装方式：Linux apt/yum、Windows MSI、macOS、Docker、WAR、Servlet 容器、离线。
9. 官方 Docker 镜像 LTS 标签 `jenkins/jenkins:2.580.2-lts`，**镜像不含 Docker CLI**。
10. **Jenkins 无原生多 Controller 高可用**，需外部编排 + 持久化存储实现。

## 七、学习资源

1. [Jenkins 安装总览（官方手册）](https://www.jenkins.io/doc/book/installing/)
2. [Jenkins Docker 安装（官方手册）](https://www.jenkins.io/doc/book/installing/docker/)
3. [Jenkins 离线安装（官方手册）](https://www.jenkins.io/doc/book/installing/offline/)
4. [Jenkins 下载页（官方）](https://www.jenkins.io/download/)
5. [Jenkins LTS 变更日志](https://www.jenkins.io/changelog-stable/)
6. [Jenkins Weekly 2.591 变更日志](https://www.jenkins.io/changelog/2.591/)
7. [Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)
8. [Jenkins 官方用户手册](https://www.jenkins.io/doc/book/)
9. [Managing Nodes（官方·节点管理）](https://www.jenkins.io/doc/book/managing/nodes/)
10. [Kubernetes Plugin for Jenkins（插件站）](https://plugins.jenkins.io/kubernetes/)
11. [JKO（Jenkins Kubernetes Operator）](https://github.com/jenkinsci/kubernetes-operator)
12. [Jenkins Docker 镜像仓库](https://github.com/jenkinsci/docker)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
