---
title: Jenkins 自由风格任务
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 自由风格任务
  - 持续集成
aliases:
  - Jenkins Freestyle Job
  - 自由风格构建
source:
  - 网络资料整理
---

# Jenkins 自由风格任务

> [!摘要] 摘要
> 自由风格任务（Freestyle Job）是 Jenkins 最经典、最基础的任务类型：它以 Web UI 或 XML 配置驱动，把「拉取源码 → 构建 → 测试 → 归档 → 通知」的步骤串成一条任务，无需编写 Groovy 脚本。本文从概念与定位出发，梳理自由风格任务的配置模型、触发与构建机制，给出参数化构建、定时/轮询触发、归档与测试报告、CLI 批量建 Job 等可落地的操作示例，并对比它与 Pipeline 的取舍、列出升级与安全方面的常见坑。适合刚接触 Jenkins、想快速落地单个构建任务的运维与研发工程师；若已进入多阶段、多分支的复杂交付流程，建议在本篇基础上转向 [[CI-CD与Jenkins-从入门到精通]] 中的 Pipeline 体系。

## 一、最新动态（截至 2026-11）

- **Jenkins 采用双发布线**：**Weekly**（每周）与 **LTS**（长期支持）。LTS 基线每 12 周从 Weekly 流中选取一次，随后每 4 周发布一个补丁（bug / 安全 / 小功能回移）。
- **当前版本状态**：**Weekly 最新 2.591**（2026-11-16 发布），主打变更为默认启用内容安全策略（CSP）；**LTS 最新 2.580.2**（2026-10-28 发布，含重要安全修复），**2.580.3** 正式版计划 2026-11-25 发布，**下一个 LTS 基线定于 2027-01-06**。
- **2.580.x 的重大变更**：**移除一批默认捆绑插件**（bouncycastle API、JUnit、Mailer、Matrix Authorization、Matrix Project、OWASP Markup Formatter、JavaMail、SSH server 等），`jenkins.war` 体积缩减 40 MB+。**从 2.356 之前升级**或检测到面向旧版本的插件时，需通过插件管理器**手动补装**这些插件——自由风格任务常用的 **JUnit（测试报告发布）**、**Mailer（邮件通知）**、**Matrix Project（矩阵构建）** 都在其中。
- **Java 硬约束**：**2.555.1 及以后要求 Java 21 或 Java 25，Java 17 不再支持**（2.555.1 起同时移除 Java 17 容器镜像）。
- **安全公告**：2026 年共发布 10 次安全公告。**CVE-2026-84651（2026-09-02）**：更新代理配置的 REST API 与 CLI 端点存在授权绕过，可跨代理覆盖配置并获取入站代理密钥，影响 Weekly 2.579 及更早 / LTS 2.568.2 及更早，**修复于 LTS 2.568.3 / Weekly 2.580**。
- **与自由风格直接相关**：自由风格任务本身没有独立的版本演进，其能力随核心版本与配套插件更新。在 2.580.x 上新建自由风格任务时，注意按插件管理器提示补齐 JUnit、Mailer、Parameterized Build、Script Security 等插件。

> [!info] 版本口径
> 本篇统一以 **LTS 2.580.x（当前 2.580.2）** 为生产推荐基线，以 **Weekly 2.591** 为最新特性参考；若写作时间晚于 2026-11，请以 [Jenkins 官方变更日志](https://www.jenkins.io/changelog-stable/) 重新核对。

## 二、基础概念

**定义**：自由风格任务是 Jenkins 传统的、**配置驱动**的构建任务类型。它不要求编写 Jenkinsfile，而是通过 **Web UI 表单**或 **`config.xml`** 声明任务的各个部分，Jenkins 据此生成任务并在触发时执行。

**典型适用场景**：

- 单仓库、单任务，构建步骤简单、顺序固定；
- 快速验证想法、跑一次性脚本、简单定时任务；
- 已有大量历史自由风格任务、暂时不打算迁移的存量系统。

**不适用场景**：多阶段、多分支、需要并行与回滚、需要版本化与复用、需要与团队代码评审流程结合的复杂交付流程——这类场景官方推荐使用 **Pipeline（Jenkinsfile）**。

**核心概念模型**：一个自由风格任务由若干可插拔的「部分（section）」组成，每类部分由对应插件提供，彼此独立组合：

| 部分（Section） | 作用 | 常见实现 |
| --- | --- | --- |
| 源码管理（Source Code Management） | 拉取或更新代码 | Git、SVN、Mercurial |
| 触发器（Triggers） | 决定何时启动构建 | 定时（cron）、SCM 轮询、上游构建触发 |
| 构建环境（Build Environment） | 准备执行环境 | 设置环境变量、凭据、容器等 |
| 构建步骤（Build Steps） | 实际执行的工作 | Shell、Ant、Maven、MSBuild、Gradle 等 |
| 后构建操作（Post-build Actions） | 构建后的收尾 | 归档产物、发布测试报告、邮件通知 |
| 参数化构建（Parameters） | 运行时传入参数 | 字符串、布尔、选项、文件等 |

## 三、核心机制

**1. 配置即 XML。** 每个自由风格任务在 `JENKINS_HOME/jobs/<任务名>/config.xml` 中保存一份配置。Web UI 的每次保存，本质都是重写这份 XML；因此可以通过 Git 管理配置、用 CLI 批量导入，实现一定程度的「配置可版本化」。

**2. 触发模型。** 触发器决定任务何时运行，与构建逻辑解耦：

- **定时触发（Build Trigger）**：按 cron 表达式轮询调度；
- **SCM 轮询（Poll SCM）**：定期检查代码仓库是否有新提交，有则触发（依赖仓库可被轮询，不依赖 Webhook）；
- **上游构建触发（Build after other projects are built）**：当依赖任务完成（成功/失败/不稳定）后触发，用于串起任务链。

**3. 构建步骤在 Agent 上执行。** 任务实际运行时由 Controller 调度，构建步骤在匹配的 **Agent（Node）** 上由执行器（Executor）运行。通过任务的「限制构建节点（Restrict where this project can run）」填写标签，可把任务绑定到特定 Agent。

**4. 后构建操作按条件执行。** 后构建部分可在构建完成后执行归档、测试报告发布、邮件等，通常通过 `buildResult`（成功 / 失败 / 不稳定）等条件控制，达到类似质量门禁的效果。

**5. 与 Pipeline 的本质差异。** 自由风格是**配置式、图形化**；Pipeline 是**代码化（Pipeline as Code）**，定义在 Jenkinsfile 中，纳入版本控制。二者底层共享 Pipeline 子系统与 Agent 体系，但自由风格不具备 Declarative 的 `stage` / `parallel` / `matrix` 等结构化编排能力。

## 四、实践步骤（含代码/命令示例）

**步骤 1：创建任务并配置源码与构建步骤**

在 Jenkins 首页点击「新建 Item」→ 选择「Freestyle project」→ 填写名称进入配置页。核心两块：

- **源码管理**：选择 Git，填写仓库地址与分支，并配置凭据；
- **构建步骤**：选择「Execute shell」，填入命令。

```bash
# 构建步骤中的 Shell 示例（构建并运行测试）
echo "当前分支: ${GIT_BRANCH}"
set -e
./gradlew clean build -x test
./gradlew test
```

**步骤 2：启用参数化构建**

安装 **Parameterized Build 插件**后，在「Parameters」部分新增参数，构建步骤中通过 `$参数名` 引用：

```bash
# 参数 APP_VERSION（默认 1.0.0）、ENV（选项 dev/test/prod）
echo "构建版本 ${APP_VERSION} 到环境 ${ENV}"
```

**步骤 3：配置触发器**

```text
# 定时触发：每小时第 15 分钟执行一次（cron 表达式）
15 * * * *

# SCM 轮询：每 5 分钟检查一次仓库是否有新提交
H/5 * * * *
```

**步骤 4：配置后构建操作**

- **Archive the artifacts**：填写产物路径，如 `build/libs/*.jar`；
- **Publish JUnit test result report**：填写 `**/build/test-results/*.xml`；
- **E-mail Notification**：配置收件人，在构建失败时通知。

> [!warning] 插件缺失提醒
> **2.580.x 起 JUnit、Mailer 等插件不再默认捆绑**。若升级后「后构建操作」里找不到 Publish JUnit 或邮件相关选项，需先到 `Manage Jenkins > Manage Plugins > Available` 手动安装对应插件。

**步骤 5：用 Jenkins CLI 批量建 Job（配置即 XML）**

自由风格任务的 `config.xml` 结构固定，可用于批量创建或模板化管理：

```xml
<?xml version='1.1' encoding='UTF-8'?>
<project>
  <description>示例自由风格任务</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>APP_VERSION</name>
          <defaultValue>1.0.0</defaultValue>
          <description>部署的应用版本号</description>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <builders>
    <hudson.tasks.Shell>
      <command>echo "build ${APP_VERSION}"</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
```

```bash
# 通过 CLI 导入配置创建任务（config.xml 为上文文件）
java -jar jenkins-cli.jar -s http://jenkins:8080 -auth user:API_TOKEN \
  create-job my-freestyle-job config.xml

# 校验任务是否创建成功
java -jar jenkins-cli.jar -s http://jenkins:8080 -auth user:API_TOKEN \
  list-jobs
```

**步骤 6：首次运行与验证**

进入任务页点击「Build Now」，若配置了参数则在弹窗中填写；随后在「Build History」中查看控制台输出，确认源码拉取、构建、测试报告、归档均按预期执行。

## 五、最佳实践与常见坑

**最佳实践**：

1. **小任务用自由风格，复杂流程用 Pipeline。** 单步或两三步的简单构建，自由风格的配置成本最低；一旦出现多阶段、多分支、需要复用与审计，应迁移到 Declarative Pipeline（见 [[CI-CD与Jenkins-从入门到精通]]）。
2. **用标签做资源隔离。** 通过「限制构建节点」把编译型、测试型、部署型任务分别绑定到不同标签的 Agent，避免资源争抢与相互污染。
3. **配置纳入版本管理。** 将 `config.xml` 或其生成脚本放入 Git，配合 CLI 导入，实现任务配置可追溯、可回滚。
4. **敏感信息走凭据，不写明文。** 仓库密码、部署密钥等一律使用 Jenkins 凭据，自由风格任务中通过凭据绑定引用，避免明文出现在构建日志或配置里。
5. **及时清理历史构建。** 配置构建丢弃策略（保留最近 N 次），控制磁盘占用，避免 `JENKINS_HOME` 无限增长。
6. **触发器避免过密轮询。** SCM 轮询间隔过短会给仓库与控制器带来额外压力，优先使用 Webhook 或合理 cron。

**常见坑**：

- **插件缺失导致配置项消失**：2.580.x 移除默认捆绑插件后，升级可能丢失 JUnit、Mailer、Matrix 等能力，需在插件管理器手动补装，并排查旧插件兼容性。
- **构建步骤报 `Script Security` 拒绝**：自由风格的 Shell / Groovy 步骤若包含不受信任脚本，会被 **Script Security Plugin** 的沙箱拦截。对可信脚本可在步骤上启用沙箱策略或为脚本添加签名；对完全不受信任的脚本，不要授予其运行权限。
- **参数不生效**：未安装 Parameterized Build 插件，或在触发时（定时/轮询）没有填写参数而使用了默认值——确认参数定义与构建时实际传入值。
- **源码没更新就构建**：SCM 轮询检查间隔或分支填写有误，或 Webhook 未配置导致控制器感知不到新提交。
- **构建卡在排队**：检查执行器数量、节点标签是否匹配、并发上限，避免任务长期等待而误判为失败。
- **安全升级风险**：**CVE-2026-84651** 影响入站代理密钥安全，请尽快升级到 **LTS 2.568.3 / Weekly 2.580 及以上**；同时确认运行环境满足 **Java 21 或 25**。

## 六、核心要点速查

1. 自由风格任务是 **配置驱动**的传统任务类型，通过 Web UI 或 `config.xml` 定义，无需编写 Jenkinsfile。
2. 标准组成：**源码管理 → 触发器 → 构建环境 → 构建步骤 → 后构建操作**，另有可选的**参数化构建**。
3. 触发器三类：**定时（cron）、SCM 轮询、上游构建触发**。
4. 构建步骤在匹配标签的 **Agent** 上执行，通过「限制构建节点」绑定。
5. **参数化构建**需 **Parameterized Build 插件**，构建步骤中以 `$参数名` 引用。
6. 后构建常用：**归档产物、发布 JUnit 测试报告、邮件通知**。
7. 可用 **CLI `create-job config.xml`** 批量建任务，实现配置可版本化。
8. **与 Pipeline 的取舍**：简单单任务用自由风格，复杂多阶段/多分支/需复用审计用 **Declarative Pipeline**。
9. 版本基线：**LTS 2.580.2（2026-10-28）**，Weekly **2.591**；**2.555.1 起要求 Java 21 / 25**。
10. **2.580.x 移除默认捆绑插件**，升级后需手动补装 JUnit、Mailer 等。
11. 安全：**CVE-2026-84651** 需升级至 2.568.3 / 2.580 及以上；不受信任脚本受 **Script Security Plugin** 沙箱约束。

## 七、学习资源

1. [Pipeline（Jenkins 官方用户手册·流水线概览）](https://www.jenkins.io/doc/book/pipeline/)
2. [Managing Plugins（Jenkins 官方用户手册·插件管理）](https://www.jenkins.io/doc/book/managing/plugins/)
3. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
4. [Jenkins Security Advisories（官方安全公告）](https://www.jenkins.io/security/advisories/)
5. [Jenkins 官方用户手册（总览）](https://www.jenkins.io/doc/book/)
6. [Jenkins 插件站（plugins.jenkins.io）](https://plugins.jenkins.io/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
