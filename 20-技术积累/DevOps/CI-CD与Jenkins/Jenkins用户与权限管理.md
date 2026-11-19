---
title: Jenkins 用户与权限管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - Jenkins
  - 权限管理
  - RBAC
  - 认证授权
  - 安全
  - DevOps
  - CI/CD
aliases:
  - Jenkins 用户管理
  - Jenkins 权限管理
  - Jenkins RBAC
source: 网络资料整理
---

# Jenkins 用户与权限管理

> [!摘要]
> 本文围绕 Jenkins 的「用户体系」与「授权模型」展开：先厘清认证与授权的区别、内置用户数据库与 LDAP / SAML / OpenID Connect 等外部认证方式；再讲清基于权限（permission）的授权机制、Matrix 与 Role-Based（RBAC）两类授权策略、常用权限项的语义与作用域；最后给出创建用户、配置 Matrix / RBAC、接入 LDAP、控制凭据与共享库权限等可直接落地的步骤与命令、Groovy、YAML 示例。适合需要为 Jenkins 设计最小权限体系、落地 RBAC，或排查越权与登录问题的运维与研发工程师。

## 一、最新动态（截至 2026-11）

- Jenkins 采用 **Weekly（每周）+ LTS（长期支持）** 双发布线。当前 **LTS 最新为 2.580.2（2026-10-28 发布，安全修复版本）**，**Weekly 最新为 2.591（2026-11-16 发布）**，后者的主打变更为默认启用内容安全策略（CSP）。
- **2.555.1（LTS，2026-04-15）起默认启用 `Overall/Manage` 权限**，同时正式要求 Java 21 或 Java 25（弃用 Java 17）；该版本起 **API Token 支持过期日期**，CSRF crumb 计算不再包含客户端 IP。
- **2.580.x LTS 系列新增密码复杂度规则**，并提供可配置的密码校验扩展点；**2.580.3 计划于 2026-11-25 发布**（RC 已于 2026-11-10 发布），下一个 LTS 基线定于 **2027-01-06**。
- **安全公告**：2026 年已发布 10 次安全公告。其中 **CVE-2026-84651（2026-09-02）** 是更新代理配置的 REST API/CLI 端点**授权绕过**，可跨代理覆盖配置并获取入站代理密钥，修复于 LTS 2.568.3 / Weekly 2.580，与授权语义直接相关，需尽快升级。
- 版本口径统一以 [Jenkins LTS Changelog](https://www.jenkins.io/changelog-stable/) 为准。

## 二、基础概念

**用户（User）**：Jenkins 通过用户数据库记录身份，每个用户拥有唯一 ID、显示名、密码或外部身份映射，以及一组全局权限。用户可由管理员在 `Manage Jenkins > Manage Users` 手动创建，也可由外部认证插件自动同步。

**认证（Authentication）**：回答「你是谁」。除内置用户数据库外，Jenkins 通过插件接入外部认证源：

- **LDAP**：对接 Active Directory / OpenLDAP 等企业目录，由 LDAP 插件提供。
- **SAML**：基于联合身份的单点登录（SSO）。
- **OpenID Connect（OIDC）**：OAuth2 体系的 SSO。
- **GitHub / GitLab 等集成**：直接复用代码平台身份登录。

**授权（Authorization）**：回答「你能做什么」。Jenkins 采用**基于权限（permission）的授权策略**，权限按角色或用户授予，与认证解耦——同一身份在不同授权策略下可以映射出完全不同的权限集合。

**两类授权策略**：

- **Matrix-based Authorization**：Jenkins 内置，在全局安全配置中以「用户/组 × 权限项」的矩阵逐项勾选，支持按项目细化，适合节点少、权限简单的场景。
- **Role-Based Authorization Strategy（RBAC）**：需插件，把权限绑定到**角色（Role）**，用户被赋予角色，适合多项目、多团队、需要按文件夹/节点/凭据细粒度授权的场景。

**权限（Permission）**：Jenkins 的权限项按命名空间组织，形如 `对象/动作`（如 `Job/Build`）。权限自上而下按层级叠加与收敛，是理解授权行为的关键。

## 三、核心机制

**1. 权限命名与层级收敛。** 权限采用层级命名：`Overall/*` 为全局权限，`Job/*` 针对任务，`Credentials/*` 针对凭据，`RunScripts` 针对脚本控制台等。用户最终权限是其所属用户/组权限的并集；**父对象未授予的权限，子对象无法单独授予**，因此只给任务级权限而漏给全局基础权限时，用户可能连任务列表都看不到。

**2. 常用权限项语义**

| 权限项 | 语义 | 典型使用对象 |
| --- | --- | --- |
| `Overall/Read` | 查看 Jenkins 与任务列表 | 所有用户至少应具备 |
| `Overall/Configure` | 修改全局配置 | 管理员 |
| `Overall/Manage` | 管理用户、插件、节点、安全配置 | 管理员（2.555.x 起默认启用） |
| `Overall/RunScripts` | 使用脚本控制台 | 仅可信运维，与共享库信任配置相关 |
| `Job/Build` | 触发构建 | 开发 / 测试 |
| `Job/Configure` | 修改任务配置 | 流水线负责人 |
| `Credentials/View` | 查看凭据 ID 与作用域 | 需要绑定凭据的用户 |
| `Credentials/Use` | 在流水线中使用凭据 | 需要拉取镜像、推送制品的用户 |
| `Credentials/Create` / `Delete` / `Update` | 增删改凭据 | 管理员 |

**3. 两类授权策略的落地机制。**

- **Matrix**：在 `Manage Jenkins > Configure Global Security` 中选择 Matrix-based 策略，为 `anonymous`、`authenticated` 及具体用户/组逐项勾选权限；开启「按项目授权」可细化到单个任务。
- **RBAC**：安装插件后，在 `Manage Jenkins > Configure Global Security` 切换为 Role-Based 策略，然后在 `Manage Jenkins > Manage Roles` 创建角色并勾选权限，再在 `Assign Roles` 分配给用户/组。角色作用域分三类：**Global roles**（全局，优先级最高）、**Item roles**（按作业/文件夹 Pattern 匹配）、**Agent roles**（按节点标签匹配）。Pattern 区分大小写，可用 `(?i)` 做大小写不敏感匹配，例如 `(?i)folder($|/.*)` 可匹配文件夹及其内部作业。

**4. 用户与凭据作用域。** 凭据由 Credentials 插件提供，以控制器 ID 加密存储在控制器上，可设置 **Global / System / 用户级**作用域，限制凭据与流水线的访问范围，降低跨控制器复制与越权使用风险。流水线中**只按凭据 ID 引用**，敏感值在日志中显示为 `****`。掩码**仅降低意外泄露风险，无法阻止恶意用户通过其他途径获取凭据值**，因此不要允许不受信任的流水线使用受信任凭据。

**5. Shared Library 的信任模型与权限绑定。** 共享库是权限管控的高危面：**trusted** 库可调用 Java / Groovy / Jenkins 内部 API，不受 Groovy 沙箱限制，其配置者需具备 `Overall/RunScripts` 权限；**untrusted** 库在沙箱内运行，仅 `Overall/Manage` 权限可配置。应把「谁能配置库」与「谁能执行库」分开管理。

**6. 安全强化机制（与权限直接相关）。** 2.555.1 起默认启用 `Overall/Manage` 权限，CSRF crumb 不再包含客户端 IP；2.580.x 起默认禁止 Object 字段反序列化、新增密码复杂度规则与可配置密码校验扩展点；API Token 支持过期日期，便于按期限收回自动化凭据。

## 四、实践步骤（含代码/命令示例）

**步骤 1：创建用户。** 在 `Manage Jenkins > Manage Users > 新建用户` 中填写 ID、全名与邮箱，设置密码并保存；也可由 LDAP/OIDC 等插件按外部身份自动同步。

**步骤 2：使用 Matrix 授权策略（内置，无需插件）。**

在 `Manage Jenkins > Configure Global Security` 中：

- 勾选 `Matrix-based security`。
- 为 `anonymous`、`authenticated` 及具体用户/组逐项勾选权限。
- 勾选 `Enable project-based security`，可为单个任务再单独配置矩阵。

**步骤 3：安装 RBAC 插件并切换授权策略（多团队推荐）。**

```bash
# 通过 Jenkins CLI 安装 Role-based Authorization Strategy（需管理员权限）
java -jar jenkins-cli.jar -s http://jenkins:8080 install-plugin role-strategy
```

安装后进入 `Manage Jenkins > Configure Global Security`，将授权策略切换为 `Role-Based Authorization Strategy`。**不切换则角色配置不会生效**，这是最常见的踩坑点。

**步骤 4：创建角色并绑定权限。** 在 `Manage Jenkins > Manage Roles` 中创建角色，例如 Item Role `dev-build`，Pattern 填 `dev-.*`，勾选 `Job/Build`、`Job/Read`、`Credentials/View`、`Credentials/Use`。也可在脚本控制台用官方方式创建角色（需 `Overall/RunScripts`）：

```groovy
import com.michelin.cio.hudson.plugins.rolestrategy.AuthorizationType
import com.michelin.cio.hudson.plugins.rolestrategy.PermissionEntry
import com.michelin.cio.hudson.plugins.rolestrategy.RoleBasedAuthorizationStrategy
import com.michelin.cio.hudson.plugins.rolestrategy.Role
import com.synopsys.arc.jenkins.plugins.rolestrategy.RoleType
import hudson.security.Permission
import jenkins.model.Jenkins

Jenkins jenkins = Jenkins.get()
def rbas = new RoleBasedAuthorizationStrategy()

// 创建全局管理员角色，权限对象可按需替换为具体权限
Set<Permission> permissions = new HashSet<>()
permissions.add(Jenkins.ADMINISTER)
Role adminRole = new Role("admin", permissions)

globalRoleMap = rbas.getRoleMap(RoleType.Global)
globalRoleMap.addRole(adminRole)
globalRoleMap.assignRole(adminRole, new PermissionEntry(AuthorizationType.USER, 'admin'))
globalRoleMap.assignRole(adminRole, new PermissionEntry(AuthorizationType.GROUP, 'administrators'))
jenkins.setAuthorizationStrategy(rbas)

jenkins.save()
```

**步骤 5：分配角色。** 在 `Manage Jenkins > Manage Roles > Assign Roles` 中，把 `dev-build` 角色分配给开发组。用户组由认证源（如 LDAP）提供，另有内置组 `authenticated`（已登录用户）与 `anonymous`（未登录用户）。

**步骤 6：接入 LDAP 外部认证。** 可用 JCasC（Configuration as Code）声明，官方 schema 如下：

```yaml
jenkins:
  securityRealm:
    ldap:
      configurations:
        - server: ldap.acme.com
          rootDN: dc=acme,dc=fr
          managerDN: "manager"
          managerPasswordSecret: ${LDAP_MANAGER_PASSWORD}
          userSearch: "(&(objectCategory=User)(sAMAccountName={0}))"
          groupSearchFilter: "(&(cn={0})(objectclass=group))"
          groupMembershipStrategy:
            fromGroupSearch:
              filter: "(&(objectClass=group)(|(cn=GROUP_1)(cn=GROUP_2)))"
      cache:
        size: 100
        ttl: 10
      userIdStrategy: CaseInsensitive
      groupIdStrategy: CaseSensitive
```

> [!warning] LDAP 配置注意
> `managerPasswordSecret` 使用 Secret 引用，**不要写入明文密码**；`java.naming.referral` 默认 `ignore` 是出于安全考虑，设为 `follow` 会暴露凭据外泄与 SSRF 风险，仅在完全信任 LDAP 基础设施时才开启。保存前务必用「Test LDAP Settings」验证，避免把自己锁在系统外。

**步骤 7：用角色控制凭据与流水线访问。** 项目角色不授予 `Credentials/Use`，则该角色下的流水线无法绑定凭据，实现「无凭据权限即无法拉取私有镜像/推送制品」。再配合用户级凭据作用域进一步收紧：

```groovy
// 通过 Script Console 查看凭据存储位置（需管理员权限）
import jenkins.model.Jenkins
println "凭据存储根: ${System.getenv('JENKINS_HOME')}/credentials.xml"
```

实际凭据作用域建议在 `Manage Jenkins > Manage Credentials` 界面按「作用域」字段设置。

**步骤 8：在流水线中查询当前用户角色。** RBAC 提供两个内置步骤，可用于按角色做条件分支或审计：

```groovy
// 返回当前触发构建用户拥有的全局角色；定时/SCM 触发时回退为 SYSTEM 用户
def roles = currentUserGlobalRoles()
println "当前全局角色: ${roles}"

// 返回当前流水线匹配的 Item 角色（showAllRoles: true 可返回全部）
def itemRoles = currentUserItemRoles(showAllRoles: true)
println "当前 Item 角色: ${itemRoles}"
```

**步骤 9：校验权限生效。**

```bash
# 以普通用户身份访问 API，验证权限是否收敛
curl -u dev-user:<api-token> -s http://jenkins:8080/api/json | jq '.jobs[].name'
# 无 Job/Read 权限时返回 403，据此确认授权策略已生效
```

## 五、最佳实践与常见坑

**最佳实践**

1. **最小权限**：只授予完成工作必需的权限，开发角色不授予 `Overall/Configure`、`Credentials/Create`、`Overall/RunScripts`。
2. **用 RBAC 取代全局 Matrix**：项目多、团队多时 Matrix 难以维护，用「角色 + Pattern」统一治理，人员变动只改角色分配。
3. **认证与授权分离**：LDAP/OIDC 只负责「是谁」，权限一律由授权策略决定，避免在认证插件中隐含权限。
4. **凭据作用域最小化**：优先用户级作用域，避免用 Global 作用域承载高敏凭据。
5. **API Token 设过期**：自动化凭据到期即回收，降低长期有效凭据外泄风险。
6. **共享库权限分离**：配置库的人需要 `Overall/RunScripts`（trusted）或 `Overall/Manage`（untrusted），业务流水线用户只给执行权限。
7. **升级前核对安全公告**：涉及授权绕过的 CVE（如 CVE-2026-84651）应优先升级到修复版本。

**常见坑**

- **权限不生效，多因父级没给**：只给 `Job/Build` 而漏给 `Overall/Read`，用户可能连任务列表都看不到，应先保证基础权限完整。
- **RBAC 插件未切换授权策略**：安装 Role-based Authorization Strategy 后必须手动在 Configure Global Security 切换，否则仍走内置策略，角色配置不生效。
- **凭据绑定失败**：多是作用域或缺少 `Credentials/View` / `Credentials/Use`，需确认调用方具备凭据的读取与使用权限。
- **外部认证登录后仍无权限**：认证成功但授权策略中没有该用户的任何条目，需显式添加用户/组。
- **从外部目录切回内置数据库**：用户与权限配置不会自动迁移，需提前规划。
- **过度授予 `Overall/RunScripts`**：脚本控制台能力极强，随意授予等同下放管理员权限，应仅给可信运维。

## 六、核心要点速查

1. Jenkins **认证（你是谁）与授权（你能做什么）解耦**：内置用户数据库，外部认证由 LDAP / SAML / OIDC 等插件提供。
2. 授权采用**基于权限的模型**，权限按用户/角色授予，命名形如 `对象/动作`。
3. 两类授权策略：**Matrix-based**（内置、简单）与 **Role-based（RBAC，需插件、多团队推荐）**。
4. 常用权限：`Overall/Read`、`Overall/Configure`、`Overall/Manage`（2.555.x 起默认启用）、`Job/Build`、`Job/Configure`、`Credentials/View`、`Credentials/Use`、`RunScripts`。
5. RBAC 角色作用域：**Global roles**、**Item roles**（按作业/文件夹 Pattern）、**Agent roles**（按节点标签），全局角色优先级最高。
6. 权限按层级叠加与收敛，**父对象未授予的权限，子对象无法单独授予**。
7. 凭据以控制器 ID 加密存储，可设 **Global / System / 用户级**作用域，流水线只按 ID 引用，日志掩码为 `****`。
8. 掩码只防意外泄露，**不能阻止恶意用户**，不可让不受信任的流水线使用受信任凭据。
9. Shared Library：**trusted** 需 `Overall/RunScripts`，**untrusted** 仅 `Overall/Manage`。
10. 2.555.1 起要求 Java 21/25、API Token 支持过期、CSRF crumb 不含客户端 IP；2.580.x 新增密码复杂度规则、默认禁止 Object 反序列化；2.591 默认启用 CSP。
11. CVE-2026-84651 为代理配置授权绕过，修复于 LTS 2.568.3 / Weekly 2.580，应尽快升级。

## 七、学习资源

1. [Jenkins Security（官方用户手册·安全）](https://www.jenkins.io/doc/book/security/)
2. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
3. [Jenkins Security Advisories（官方安全公告）](https://www.jenkins.io/security/advisories/)
4. [Using credentials（官方用户手册·凭据使用）](https://www.jenkins.io/doc/book/using/using-credentials/)
5. [Role-based Authorization Strategy（插件站）](https://plugins.jenkins.io/role-strategy/)
6. [LDAP Plugin（插件站）](https://plugins.jenkins.io/ldap/)
7. [SAML Plugin（插件站）](https://plugins.jenkins.io/saml/)
8. [Credentials Plugin（插件站）](https://plugins.jenkins.io/credentials/)
9. [Extending with Shared Libraries（官方用户手册·共享库）](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
10. [Jenkins 官方手册](https://www.jenkins.io/doc/book/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]
- [[Kubernetes安全（RBAC-网络策略）]]

## 九、变更记录

- 2026-11-19：首次创建。
