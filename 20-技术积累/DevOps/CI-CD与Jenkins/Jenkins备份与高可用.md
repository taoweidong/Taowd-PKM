---
title: Jenkins 备份与高可用
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Jenkins
  - CI/CD
  - 备份
  - 高可用
  - 运维
aliases:
  - Jenkins 备份与高可用
  - Jenkins 容灾
source:
  - 网络资料整理
---

# Jenkins 备份与高可用

> [!摘要] 摘要
> 本文聚焦 Jenkins 的两件「保命」工程：**备份与高可用**。Jenkins 的核心数据全部落在 `JENKINS_HOME` 目录中，备份的本质是保护这一目录的完整性与可恢复性，用于灾难恢复、回退旧配置以及抢救损坏或误删的文件。高可用方面必须明确：**Jenkins 核心是单 Controller 架构，官方并未提供原生的多 Controller 多活方案**，生产高可用需借助外部编排（Kubernetes + Jenkins Operator / 持久化存储 / 外部数据库与凭据）以及负载均衡的只读或故障转移来实现。适合负责 Jenkins 运维、需要制定备份策略或规划生产架构的工程师。

## 一、最新动态（截至 2026-11）

- **版本基线**：截至 2026-11，最新 Jenkins **LTS 为 2.580.2**（2026-10-28 发布，含重要安全修复）；**Weekly 最新为 2.591**（2026-11-16 发布，默认启用内容安全策略 CSP）。**2.580.3** 的 RC 已于 2026-11-10/11 发布，**正式版计划 2026-11-25 发布**，下一个 LTS 基线定于 **2027-01-06**。
- **Java 硬约束**：**2.555.1 及以后要求 Java 21 或 Java 25，Java 17 已弃用**，备份与恢复演练的环境需同步满足该要求。
- **高可用工具**：**JKO（Jenkins Kubernetes Operator）v0.10.0-beta1（2026-11）**新增 Istio/Linkerd 服务网格支持与云身份注入保护（AWS IRSA、EKS Pod Identity、Azure Workload Identity、Google ADC）。注意该版本为 **beta 测试性质**，生产使用需谨慎。
- **安全关联**：**CVE-2026-84651（2026-09-02）**揭示更新代理配置的 REST API/CLI 存在授权绕过，可跨代理接管配置并获取入站代理密钥，修复于 LTS 2.568.3 / Weekly 2.580。Agent 配置属高可用链路的关键配置，务必及时升级。
- 官方未发布「原生多 Controller 高可用」方案，相关表述以官方文档为准。

## 二、基础概念

**备份要解决什么**。Jenkins 的运行状态几乎全部集中在 `JENKINS_HOME` 目录，备份的三个明确目标来自官方文档：**灾难恢复**（整机损坏后重建）、**恢复旧配置**（改坏配置后回滚）、**恢复损坏或误删文件**（如误删某个 Job 目录）。

**`JENKINS_HOME` 必须覆盖的关键内容**：

- `config.xml`：全局主配置。
- `jobs/`：所有任务（含自由风格与 Pipeline）的定义与构建记录。
- `users/`：用户与授权数据。
- `credentials.xml`：凭据（加密存储，但需随目录一并备份）。
- `plugins/`：已安装插件。
- `secrets/`：密钥、初始密码等敏感信息。
- `scripts/`、`nodes/`、`updated.txt` 等运行期文件。

**高可用的边界**。Jenkins 的 Controller 既是 Web 服务，又是调度、配置与认证授权中枢，**没有内置的多活/主备切换**。实践中的高可用是「**外部编排 + 数据持久化 + 负载均衡**」的组合，而非 Jenkins 自身能力，规划时切勿假设双活自动切换。

## 三、核心机制

**备份的三种主流机制**：

1. **文件系统快照**：一致性最高、速度最快，依赖底层文件系统能力，支持 **LVM、btrfs、Solaris ZFS、OpenZFS** 等。适合数据量大、要求低停机的宿主环境。
2. **备份插件**：开源插件生态中**仅 thinBackup Plugin 仍在维护**，其余备份类插件可能失修，选型时需评估维护状态。
3. **Shell 脚本 + cron**：复制关键文件与目录，最灵活、零依赖，适合小中规模与定制策略。

**备份的语义要点**：备份不是「复制文件」这么简单，必须保证**快照的一致性**——避免在构建、写配置过程中拷贝出半写状态的文件。文件系统快照天然具备一致性；脚本方案则应配合锁、停止或原子拷贝（如 `cp -a` 配合软链接切换）来收敛一致性风险。

**高可用的实现层次**：

- **数据层**：`JENKINS_HOME` 挂载到持久卷，控制器可随时在节点间迁移或重建。
- **编排层**：Kubernetes 上用 **JKO（Jenkins Kubernetes Operator）**声明式管理 Jenkins 实例，配合 **JCasC（Configuration as Code）**将配置、凭据、插件、Job 全部代码化，实现可恢复的「种子 Job」。
- **访问层**：控制器前部署负载均衡（HAProxy / Nginx）做健康检查与故障摘除，承担**只读访问或故障转移**，而非多活写。

## 四、实践步骤（含代码/命令示例）

**1. Docker 方式部署并持久化（数据层前提）**

```bash
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-home:/var/jenkins_home \
  jenkins/jenkins:2.580.2-jdk21
```

`JENKINS_HOME` 必须落在命名卷或持久卷上，容器重建才能复用数据。

**2. Shell 脚本 + cron 全量备份**

```bash
#!/usr/bin/env bash
# 备份 Jenkins 主目录，保留最近 7 份
set -euo pipefail
JENKINS_HOME="/var/jenkins_home"
BACKUP_ROOT="/backup/jenkins"            # 独立文件系统，勿用 /tmp
TS=$(date +%Y%m%d-%H%M%S)
DEST="$BACKUP_ROOT/jenkins-$TS"

mkdir -p "$DEST"
# 使用 cp -a 保留权限与软链接，配合 rsync 做增量校验
cp -a "$JENKINS_HOME" "$DEST/JENKINS_HOME"
tar -czf "$DEST/JENKINS_HOME.tar.gz" -C "$BACKUP_ROOT" "jenkins-$TS/JENKINS_HOME"

# 清理过期备份，仅保留最近 7 份
ls -1t "$BACKUP_ROOT"/jenkins-* | tail -n +8 | xargs -r rm -rf
echo "备份完成：$DEST"
```

```bash
# 写入 crontab：每天凌晨 2 点执行
0 2 * * * /usr/local/bin/jenkins-backup.sh >> /var/log/jenkins-backup.log 2>&1
```

**3. 文件系统快照（以 LVM 为例，一致性最高）**

```bash
# 创建快照卷（大小需覆盖增量写入量），随后挂载只读备份
lvcreate -s -n jenkins-snap -L 10G /dev/vg_jenkins/lv_jenkins
mkfs.xfs /dev/vg_jenkins/jenkins-snap
mount -o ro /dev/vg_jenkins/jenkins-snap /mnt/jenkins-snap
tar -czf /mnt/jenkins-snap/jenkins-$(date +%F).tar.gz -C /var/jenkins_home .
umount /mnt/jenkins-snap
lvremove /dev/vg_jenkins/jenkins-snap
```

**4. 使用 thinBackup 插件**

在 `Manage Jenkins > Manage Plugins` 安装 **thinBackup**，于 `Manage Jenkins > ThinBackup` 中配置备份目录与计划，可执行「备份 / 还原 / 校验」。适合不想写脚本、又希望有 UI 操作入口的场景。

**5. 恢复演练**

```bash
# 停止 Jenkins，将备份目录替换回 JENKINS_HOME，再启动
systemctl stop jenkins
mv /var/jenkins_home /var/jenkins_home.bak
cp -a /backup/jenkins/jenkins-XXXX/JENKINS_HOME /var/jenkins_home
chown -R jenkins:jenkins /var/jenkins_home
systemctl start jenkins
```

**6. 高可用落地：Kubernetes + JKO（声明式）**

```yaml
# Jenkins CR 片段：依赖持久卷、JCasC 配置与种子 Job
apiVersion: jenkins.io/v1alpha2
kind: Jenkins
metadata:
  name: jenkins
spec:
  controller:
    serviceAccount: jenkins
    image: jenkins/jenkins:2.580.2-jdk21
    volumeMounts:
      - name: jenkins-home
        mountPath: /var/jenkins_home
    ingress:
      className: nginx
  seedJob:
    enabled: true
    configurationAsCode:
      jobConfig: |
        jenkins:
          systemMessage: "由 JKO 声明式管理"
```

负载均衡层对控制器做 `/login`、`/api/json` 等健康检查，故障时摘除并重新调度。

## 五、最佳实践与常见坑

**最佳实践**：

- **备份目录放独立文件系统**，**绝不要备份到 `/tmp`**——重启或临时清理会直接抹掉备份。
- **先锁再拷**：脚本备份时配合锁文件或维护窗口，保证快照一致性；大目录优先用文件系统快照或 `rsync --hard-links`。
- **定期做恢复演练**：备份「存在」不等于「可用」，必须实际还原并跑通一次流水线，才能验证可用性。
- **区分全量与增量**：全量周备 + 增量日备，保留策略与磁盘容量匹配，避免保留过短无法满足回溯需求。
- **高可用不要追求「多活写」**：接受单 Controller 写、负载均衡只读/故障转移的现实，把精力放在快速重建与数据持久化上。
- **配置即代码（JCasC）**：把全局配置、凭据、插件、Job 都纳入版本控制，让「重建」变成可复现的部署而非手工恢复。
- **升级前先备份并核对插件**：2.580.x 移除了 JUnit、Mailer、Matrix 等默认捆绑插件，升级可能缺插件，恢复后需补齐。

**常见坑**：

- **备份了 `/var/jenkins_home` 却漏了挂载的卷或软链接**，恢复后插件/配置丢失。
- **备份与恢复环境的 Java 版本不一致**，2.555.1 起 Java 17 不可用，恢复后可能启动失败。
- **把凭据安全等同于绝对安全**：凭据以掩码与加密降低意外泄露风险，但无法阻止恶意用户，不能因此放松权限控制。
- **误信「双活」**：Jenkins 无原生多 Controller 高可用，若方案承诺主备自动切换，需确认是编排层实现而非 Jenkins 自身能力。
- **JKO 用 beta 版上生产**：v0.10.0-beta1 为测试性质，关键生产需评估并做好回退。

## 六、核心要点速查

1. 备份目标是**灾难恢复、回退旧配置、抢救损坏/误删文件**，核心目录为 `JENKINS_HOME`。
2. 必须备份的关键内容：`config.xml`、`jobs/`、`users/`、`credentials.xml`、`plugins/`、`secrets/`。
3. 三种备份机制：**文件系统快照**（LVM/btrfs/ZFS，一致性最高）、**thinBackup 插件**（开源中仅其仍在维护）、**Shell + cron**。
4. **备份目录放独立文件系统，不要放 `/tmp`**。
5. 快照一致性是备份成败关键，脚本方案需配合锁或原子拷贝。
6. **必须定期做恢复演练**，否则备份不保证可用。
7. Jenkins **核心为单 Controller，无原生多活高可用**，官方未提供多 Controller 方案。
8. 高可用 = **持久化存储 + 外部编排（JKO / JCasC）+ 负载均衡只读/故障转移**。
9. 截至 2026-11，生产基线用 **LTS 2.580.2**；**2.555.1 起要求 Java 21 / 25**。
10. JKO v0.10.0-beta1 为 **beta**，生产使用需谨慎。

## 七、学习资源

1. [Backing-up/Restoring Jenkins（Jenkins 官方手册·备份与恢复）](https://www.jenkins.io/doc/book/system-administration/backing-up/)
2. [Jenkins LTS Changelog（官方 LTS 变更日志）](https://www.jenkins.io/changelog-stable/)
3. [Jenkins 安全公告索引（Agent 配置等安全修复）](https://www.jenkins.io/security/advisories/)
4. [Jenkins Kubernetes Operator（JKO 官方仓库）](https://github.com/jenkinsci/kubernetes-operator)
5. [Kubernetes Plugin for Jenkins（插件站）](https://plugins.jenkins.io/kubernetes/)
6. [Configuration as Code（配置即代码）](https://www.jenkins.io/doc/book/managing/configuration-as-code-plugin/)
7. [Jenkins Docker 安装文档](https://www.jenkins.io/doc/book/installing/docker/)

## 八、关联笔记

- [[CI-CD与Jenkins-从入门到精通]]
- [[DevOps]]

## 九、变更记录

- 2026-11-19：首次创建。
