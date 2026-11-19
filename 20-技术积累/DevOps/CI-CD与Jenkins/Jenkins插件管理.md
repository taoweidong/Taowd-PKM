---
title: Jenkins 插件管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 插件管理
  - 运维
aliases:
  - Jenkins 插件管理
source:
  - 网络资料整理
---

# Jenkins 插件管理

> [!摘要] 摘要
> 插件是 Jenkins 扩展能力的核心方式，覆盖源码管理、构建、测试、部署、通知、安全等几乎全部工具链。本文以 Jenkins **LTS 2.580.x** 为基线，讲清插件管理的关键概念、更新中心机制、四种安装方式（Web UI / CLI / 离线 / JCasC）、插件健康评分与版本查看、以及 2.580.x 移除默认捆绑插件后的补齐要点，并给出可直接落地的命令与脚本示例，适合需要稳定管理 Jenkins 插件环境的运维与研发工程师。

## 一、最新动态（截至 2026-11）

以下版本与变更均来自 Jenkins 官方渠道，截至 2026-11。

- **双发布线**：Jenkins 分 **Weekly（每周）** 与 **LTS（长期支持）** 两条线。LTS 基线每 12 周从 Weekly 流中选取一次，随后每 4 周发布补丁（bug / 安全 / 小功能回移）。
- **当前版本状态**：
  - **Weekly 最新：2.591（2026-11-16 发布）**，主打变更为**默认启用内容安全策略（CSP）**（该能力自 2.539 引入，2.591 起默认生效）。
  - **LTS 最新：2.580.2（2026-10-28 发布）**，为安全修复版本；**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25 发布**；**下一个 LTS 基线定于 2027-01-06**。
  - 生产环境建议以 **2.580.x LTS** 为插件管理的基线，避免频繁跟随 Weekly 引入不兼容变更。
- **2.580.x 重大变更（与插件直接相关）**：**移除一批默认捆绑插件**（bouncycastle API、JUnit、Mailer、Matrix Authorization、Matrix Project、OWASP Markup Formatter、JavaMail、SSH server 等），`jenkins.war` 体积缩减 **40 MB+**。从 **2.356 之前**升级、或检测到面向旧版本的插件时，需通过插件管理器**手动补齐**这些插件。
- **插件健康评分**：**Plugin Health Score 自 2.516.1 起**在插件管理器中展示，用于直观判断插件的活跃维护与质量水平。
- **Java 硬约束**：**Jenkins 2.555.1 及以后要求 Java 21 或 Java 25，Java 17 不再支持**（2.555.1 起移除 Java 17 容器镜像）。
- **官方插件站点**：插件清单与版本以 [Jenkins 插件站](https://plugins.jenkins.io/) 为准，插件官方说明以 [Jenkins 官方手册·管理插件](https://www.jenkins.io/doc/book/managing/plugins/) 为准。

## 二、基础概念

- **插件（Plugin）**：Jenkins 的核心扩展单元，用于接入各类工具链与平台；源码管理、凭据、构建、通知等能力也由插件提供。
- **插件格式**：插件以 **`.hpi`** 文件分发，内含运行所需的代码与资源。更新中心提供的插件即为此格式。
- **更新中心（Update Center）**：由 Jenkins 项目运营，维护开源插件的清单与版本。控制器默认**每 24 小时**检查一次更新，也可在 `Manage Jenkins > Manage Plugins > Updates` 中手动点击 **「Check now」** 立即检查。
- **插件管理器（Manage Plugins）**：`Manage Jenkins > Manage Plugins` 入口，含 **Installed / Available / Updates / Advanced** 等标签页，是插件管理的中枢。
- **插件健康评分**：综合评估插件维护状态与质量，自 2.516.1 起在插件管理器展示，作为插件准入与淘汰的参考。

## 三、核心机制

**1. 更新中心与依赖解析。** 更新中心在控制器启动时加载插件清单，控制器定期拉取元数据，对比得出可更新项。安装插件时 Jenkins 会**自动解析并下载依赖插件**，无需手工逐个处理；更新中心不可达（内网 / 离线）时改用离线安装或 JCasC。

**2. 安装与生效时机。** 通过 Web UI 安装时可勾选 **「Install without restart」**，插件在下一个空闲时机加载而无需立即重启；但**首次启用**或涉及核心依赖变更时，通常仍需重启控制器才能完全生效。

**3. 禁用与启用。** 插件可在插件管理器 **Disable / Enable**，禁用后功能立即不可用，插件文件仍保留在 `$JENKINS_HOME/plugins`，避免重复下载。

**4. 版本查看与健康诊断。** 插件版本可经插件管理器或 **Script Console** 查看，用于核对升级结果。

**5. 2.580.x 的捆绑插件移除。** 该系列不再默认捆绑 JUnit、Mailer、Matrix 等插件；**升级到 2.580.x 后**若流水线依赖这些能力，需在插件管理器手动补装，否则会出现构建步骤缺失、测试报告无法发布等问题。

> [!note] 插件与 Java 版本
> 插件依赖的 Java API 受控制器 JDK 约束。Jenkins 2.555.1 起要求 **Java 21 或 25**，安装或升级插件前应先确认控制器 JDK 版本，避免插件加载失败。

## 四、实践步骤（含代码/命令示例）

**方式一：Web UI 安装（最常用）**

进入 `Manage Jenkins > Manage Plugins > Available`，搜索插件名（如 `git`），勾选后点击 **Install**，可勾选 **Install without restart**。安装完成后在 **Installed** 标签页确认版本。

**方式二：Jenkins CLI 安装（适合自动化）**

```bash
# 在能访问 Controller 的机器上，用 jenkins-cli.jar 安装插件
# -s 指定 Controller 地址，-auth 使用用户 + API Token 认证
java -jar jenkins-cli.jar -s http://jenkins:8080 -auth admin:11xxxxxxxxxxxxxxxxxxxx install-plugin git

# 如需指定版本，可先查看更新中心可用版本
java -jar jenkins-cli.jar -s http://jenkins:8080 -auth admin:11xxxxxxxxxxxxxxxxxxxx install-plugin \
  --version 5.13.0 git
```

> [!warning] API Token
> 推荐使用 **API Token**（支持过期日期）替代明文密码；Token 可在 `用户 > Configure > API Token` 生成。避免在脚本中硬编码长期有效凭据。

**方式三：离线安装（内网 / 无外网环境）**

```bash
# 1. 在可联网机器上从更新中心下载插件及其依赖 .hpi
#    注意：需一并下载依赖插件，可用 Jenkins 插件依赖工具或更新中心页面整理清单
# 2. 将 .hpi 复制到 Controller 的插件目录
docker cp git.hpi jenkins:/var/jenkins_home/plugins/
docker cp ssh-agent.hpi jenkins:/var/jenkins_home/plugins/

# 3. 重启控制器加载插件
docker restart jenkins
```

**方式四：JCasC 批量安装（配置即代码）**

使用 Configuration as Code 插件，把插件清单写进 CasC 配置文件，随控制器启动自动安装：

```yaml
# jenkins.yaml (JCasC 配置)
plugins:
  - id: "git"
  - id: "docker-workflow"
  - id: "junit"
    version: "1.16"
```

```bash
# 以 CasC 启动控制器
java -Djenkins.model.ConfigurationAsCode.config=/var/jenkins_home/jenkins.yaml \
  -jar jenkins.war
```

**查看插件版本与健康状态**

```groovy
// Script Console：打印所有已安装插件的名称与版本
Jenkins.instance.pluginManager.plugins.each { p ->
    println("${p.getShortName()}: ${p.getVersion()}")
}
```

```groovy
// Script Console：禁用 / 启用插件（无需进入 UI）
def pm = Jenkins.instance.pluginManager
pm.getPlugin('github').disable()   // 禁用
pm.getPlugin('github').enable()     // 启用
```

## 五、最佳实践与常见坑

**最佳实践**

- **最小化安装**：只保留必要插件，减少安全面与升级复杂度；定期清理长期未使用、健康评分低或已 EOL 的插件。
- **版本锁定与节奏控制**：插件升级常引发兼容性问题。生产环境**固定 LTS 基线（2.580.x）**，先在测试控制器验证后再升级，避免频繁跟随 Weekly。
- **统一安装入口**：小团队用 Web UI 即可；规模化环境优先 **JCasC 批量安装**，保证配置可版本化、可审计、可复现。
- **保留依赖清单**：离线安装时务必一并下载依赖插件，否则插件加载会因缺少依赖失败。
- **升级后核对清单**：升级到 2.580.x 后，逐项确认 JUnit、Mailer、Matrix 等被移除的默认插件是否需要手动补装。

**常见坑**

- **升级后插件缺失**：从 2.356 之前升级到 2.580.x，检测到面向旧版本的插件时会提示，需按提示手动安装被移除的默认插件。
- **装完没生效**：仅 `Install without restart` 时，部分插件需重启控制器才完全加载；先看插件是否处于 **Enabled** 状态，再决定是否重启。
- **离线安装缺依赖**：只拷贝目标插件、漏掉依赖插件，导致插件一直无法加载，报错通常指向缺失的依赖插件。
- **插件与 JDK 不匹配**：在 Java 17 环境运行 2.555.1 及以上控制器，或插件依赖更高版本 API，会直接启动 / 加载失败，应先升级到 **Java 21 或 25**。
- **CLI 认证失败**：使用明文密码或过期 Token 导致 `install-plugin` 失败，改用有效 API Token，并避免把凭据写进脚本。
- **盲目升级触发流水线异常**：插件升级后流水线报错时，先**回滚插件版本**，对照插件健康评分与安全公告定位兼容性问题，建立版本锁定机制。

## 六、核心要点速查

1. 插件以 **`.hpi`** 文件分发；更新中心默认**每 24 小时**检查一次，可手动 **Check now**。
2. 四种安装方式：**Web UI**、**Jenkins CLI `install-plugin`**、**离线安装**、**JCasC 批量安装**。
3. Web UI 安装可勾选 **Install without restart**，首次启用或依赖变更通常仍需重启控制器。
4. **Plugin Health Score** 自 **2.516.1** 起在插件管理器展示，用于判断插件维护质量。
5. 插件版本可用 Script Console 查看：`Jenkins.instance.pluginManager.plugins.each { ... }`。
6. 插件可在插件管理器中 **Disable / Enable**，文件保留在 `$JENKINS_HOME/plugins`。
7. **2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件**，从旧版本升级需手动补齐。
8. **Java 21 或 25** 为硬约束（2.555.1 起），Java 17 不再支持。
9. 生产建议锁定 **LTS 2.580.x**，插件升级先在测试环境验证，建立版本锁定机制。

## 七、学习资源

1. [Managing plugins（Jenkins 官方手册·管理插件）](https://www.jenkins.io/doc/book/managing/plugins/)
2. [Jenkins 插件站（插件清单与版本）](https://plugins.jenkins.io/)
3. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
4. [Jenkins Weekly 2.591 Changelog](https://www.jenkins.io/changelog/2.591/)
5. [Jenkins 安全公告索引](https://www.jenkins.io/security/advisories/)
6. [Jenkins 官方手册首页](https://www.jenkins.io/doc/book/)
7. [Jenkins GitHub Releases](https://github.com/jenkinsci/jenkins/releases)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
