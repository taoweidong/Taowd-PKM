---
title: Linux安全加固
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 安全加固
  - 运维
  - 操作系统
aliases:
  - Linux 安全加固
  - Linux安全加固实战
source: 网络资料整理
---

# Linux安全加固

> [!摘要] Linux 安全加固是「用最小可运行代价，把系统从默认可被利用状态收敛到可审计、可控制、可恢复状态」的工程过程。本文档按**概念 → 机制 → 落地步骤 → 避坑 → 速查**组织，覆盖强制访问控制（SELinux / AppArmor）、最小权限与 SSH 加固、内核与传输加固、防火墙与审计、供应链校验等主线，并给出可直接运行的命令与配置。本文是 [[Linux-从入门到精通]] 中「阶段四：精通」安全模块的实战展开，所有关键版本号以 2026-11 调研快照为准，生产落地前请回查官方发布说明。

## 一、最新动态（截至 2026-11）

以下版本与日期均来自本次调研，未经核实的信息不纳入：

- **内核进入 7.x 时代，加固特性持续下沉**：主线最新稳定版为 **7.3.5**（2026-11-16 由 Greg Kroah-Hartman 发布，同批发布 LTS **6.18.64**、**6.12.118**）；LTS 三支并行：**6.18**（首发 2025-11-30，维护至 2028-12）、**6.12**（首发 2024-11-17，维护至 2028-12）、**6.6**（维护至 2027-12）。内核层面的 ROP/COP/JOP 缓解（Intel CET、ARM PAC/BTI）在 Debian 13 的 amd64/arm64 上已被强化，是硬件辅助加固的主线。
- **systemd 262 强化凭据与容器**：systemd 262 于 2026-09-22 发布，systemd-stable 已推进到 **v262.2**；对安全而言最重要的是 **TPM 密封凭据绑定 SRK、Argon2id 密钥派生**的加固，以及可构建单一静态 PID 1、Intel TDX 机密虚拟机。`systemd-creds` 成为密码/密钥存储的事实工具。
- **强制访问控制（MAC）两线并进**：**SELinux policy 38.1.75**（RHEL 系，9.8 于 2026-10 打包）与 **AppArmor 5.0.2**（Debian/Ubuntu 系）按发行版分治，二者不可混用。
- **网络与传输层更新**：**nftables 1.1.7**（Debian unstable，2026-09）为新一代包过滤框架，Podman 6 已改用 nftables 后端；**Fedora 45**（2026-11-03）已升级到 **OpenSSL 4.0**；容器侧 **containerd 2.4.2**（2026-10-13）默认 seccomp 白名单加固。
- **发行版差异需特别留意**：Debian 13（trixie，13.7 于 2026-09-12）、Ubuntu 26.04 LTS（26.04.1 于 2026-08-27，搭载内核 7.0、systemd 259）、RHEL 10.2（2026-05-19）、Fedora 45。**Ubuntu 26.04 使用 systemd 259**，与 Fedora 45 的 systemd 262 行为不同，示例不可直接跨发行版套用。

> [!note] 时效性
> 内核小版本与发行版补丁迭代极快，以上为 2026-11-19 快照。正式编写脚本或变更基线前，请按各官方发布页复核版本号与维护截止日；查不到的一律以官方仓库为准。

## 二、基础概念

**1. 安全加固的四层模型**：从外到内依次是**边界层**（防火墙、SSH、端口暴露）、**权限层**（用户、组、sudo、ACL、capabilities）、**强制控制层**（SELinux/AppArmor、审计）、**内核与传输层**（内核缓解特性、TLS、凭据存储）。加固的优先级是「先收敛暴露面，再收紧权限，再上强制控制，最后加固内核与供应链」。

**2. 最小权限原则（Least Privilege）**：任何主体只持有完成其职责所需的最小权限。典型落地是「不用 root 日常登录，用 `sudo` 命令白名单替代 `NOPASSWD` 全量提权」。

**3. 纵深防御（Defense in Depth）**：单层被绕过仍有下一层兜底。例如：防火墙挡住攻击只是第一道；即使攻击者拿到一个低权账号，SELinux/AppArmor 还会阻止其访问未授权资源，auditd 还会留下可追溯记录。

**4. 可审计与可恢复**：加固不只是「堵」，还要保证**出了事能查**（auditd、journald）、**改坏了能回滚**（配置备份、不可变基线）。systemd 262 新增**损坏 journal 条目恢复**，可在非正常关机（断电、内核崩溃）导致日志头尾截断时尝试救回有效条目。

**5. MAC 与 DAC 的区别**：Linux 默认是 **DAC**（以属主/属组/其他用户的 rwx 判定），容易被提权绕过；**MAC**（SELinux/AppArmor）由独立策略决定主体能否访问客体，即使文件权限为 777 也可能被拒绝，是权限体系之外的强制约束。

## 三、核心机制

**1. 强制访问控制（MAC）**
- **SELinux**（RHEL/Fedora 系，policy 38.1.75）：以「主体—类型—域」为模型，通过类型强制（Type Enforcement）+ 角色访问控制（RBAC）限制进程可访问的文件、端口、能力。三种状态：`Enforcing` / `Permissive` / `Disabled`。
- **AppArmor**（Debian/Ubuntu 系，5.0.2）：以「profile」用路径 + 权限方式约束程序，语法更贴近「哪个程序能读/写/执行哪些路径」，`aa-status` 查看生效 profile。

**2. 内核级缓解与加固**
- Intel **CET**（影子栈，防 ROP）与 ARM **PAC/BTI**（指针认证、分支目标识别，防 JOP/COP）由内核在 amd64/arm64 上启用，是无需改代码即可获得的硬件辅助加固。
- 内核 6.12/6.18/7.x 持续修复安全缺陷，生产应锁定 LTS 并及时打补丁。

**3. 传输与凭据安全**
- **SSH** 是服务器最常被攻击的入口，加固重点在禁用密码登录、限制登录用户、限制算法与端口。
- **systemd 262 的 TPM 密封凭据**（SRK 绑定 + Argon2id 派生）用于把密钥与机器绑定，`systemd-creds` 负责加密存储；Fedora 45 的 **OpenSSL 4.0** 是 TLS 栈的更新基线。

**4. 网络过滤**
- **nftables 1.1.7** 是新一代包过滤框架（`nft` 命令族），`firewalld`、`ufw` 是其上层封装；Podman 6 已把后端统一到 nftables，不再支持 iptables。

**5. 供应链与审计**
- 包签名与来源校验（Debian 签名、RPM GPG、apk 签名）防止安装被篡改的软件。
- **auditd** 记录文件访问、系统调用与认证事件，是事后追溯的依据；**journald** 负责运行期日志。

## 四、实践步骤（含代码/命令示例）

> [!warning] 执行顺序
> 先备份配置、先在测试实例验证、逐项变更并验证服务正常，再进入生产。防火墙与 SSH 规则一旦写错可能把自己锁在门外——务必保留一个已登录的备用会话。

### 1. 记录基线，做好回滚

```bash
# 记录当前内核参数与防火墙规则，便于回滚
sysctl -a > /tmp/sysctl.before.conf
nft list ruleset > /tmp/ruleset.before.nft 2>/dev/null || iptables-save > /tmp/ruleset.before.ipt
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%F)
```

### 2. 用户与权限：最小授权

```bash
# 创建无登录权限的服务账号（用于跑服务，不交互登录）
sudo useradd --system --no-create-home --shell /usr/sbin/nologin --comment "app service" appuser

# sudo 命令白名单：用 visudo 编辑（语法错误会当场拦截，避免锁死）
sudo visudo
# 在 /etc/sudoers.d/appuser 中写入（按需替换）
appuser ALL=(root) NOPASSWD: /usr/bin/systemctl restart app.service, /usr/bin/journalctl -u app.service
sudo chmod 440 /etc/sudoers.d/appuser   # sudoers 文件必须为 440
```

```bash
# 精确授权：优先用 ACL 而非 chmod 777
sudo setfacl -m u:appuser:rx /srv/app
sudo getfacl /srv/app          # 查看 ACL 生效结果
```

### 3. SSH 加固（sshd_config）

编辑 `/etc/ssh/sshd_config`，关键项如下（改完 `systemctl reload ssh` 或 `sshd` 生效）：

```bash
PermitRootLogin no            # 禁止 root 直接登录
PasswordAuthentication no     # 禁用密码登录，仅用密钥
PermitEmptyPasswords no
MaxAuthTries 4               # 限制最大尝试次数
LoginGraceTime 30            # 限制认证等待时间
AllowUsers deploy             # 白名单，只允许指定用户
# 限制算法，剔除弱算法
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes256-ctr
```

```bash
# 部署公钥（仅追加，勿覆盖）
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
# 校验配置语法，避免重启后失联
sudo sshd -t
```

### 4. 防火墙：nftables / ufw

```bash
# ufw（Debian/Ubuntu 系，默认后端已切换到 nftables）
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp          # 仅放行 SSH，按实际服务增补
sudo ufw enable
sudo ufw status verbose
```

```bash
# nftables 原生方式（适用于未用 ufw/firewalld 的环境）
sudo nft add table inet filter
sudo nft 'add chain inet filter { type filter hook input priority 0; }'
sudo nft add rule inet filter ct state established,related accept
sudo nft add rule inet filter tcp dport 22 ct state new accept
sudo nft list ruleset
```

### 5. 强制访问控制：按发行版启用

```bash
# RHEL/Fedora 系：SELinux
sudo getenforce                       # 查看状态
sudo sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
sudo systemctl enable --now selinux    # 或重启后生效
sudo setsebool -P httpd_can_network_connect 1   # 按需为服务放行，避免直接 setenforce 0
```

```bash
# Debian/Ubuntu 系：AppArmor
sudo apt install apparmor             # Debian 13 / Ubuntu 26.04
sudo systemctl enable --now apparmor
sudo aa-status                        # 查看已加载 profile
# 用 aa-logprof 分析审计日志，为自研程序生成 profile
```

### 6. 内核参数加固（sysctl）

写入 `/etc/sysctl.d/99-hardening.conf` 后 `sudo sysctl --system` 生效：

```bash
# 禁止 ICMP 重定向，减少路由欺骗
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
# 禁止源路由，防止伪造源地址
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
# 开启 TCP SYN Cookie，缓解 SYN Flood
net.ipv4.tcp_syncookies = 1
# 限制核心转储，避免内存内容被读取
fs.suid_dumpable = 0
kernel.kptr_restrict = 2
```

### 7. 审计与日志

```bash
sudo apt install auditd            # Debian/Ubuntu；RHEL 系用 dnf install audit
sudo systemctl enable --now auditd
# 记录所有对 /etc 的修改（含 sudo 使用）
sudo auditctl -w /etc -p wa -k config_change
# 查看审计日志
sudo ausearch -k config_change
sudo aureport -i                    # 汇总报告
```

```bash
# journald 常用排查/审计命令
journalctl -b -p warning            # 本次启动的告警以上日志
journalctl -u ssh.service --since today
journalctl _SYSTEMD_UNIT=app.service -f
```

### 8. 供应链与凭据

```bash
# 校验软件包签名（Debian/Ubuntu 示例）
sudo apt-key list
sudo apt-get update --allow-insecure-repositories   # 仅调试用，勿长期开启

# 用 systemd-creds 加密存储密钥（systemd 262 TPM 加固）
sudo systemd-creds encrypt --type=tpm2 secret.key secret.cred
# 生成高强度密钥
sudo dd if=/dev/urandom of=/root/.ssh/id_ed25519 bs=32 count=1
```

## 五、最佳实践与常见坑

**最佳实践**
- **先备份、后变更、逐项验证**：每次只改一个维度，改完确认服务正常再加下一项，便于定位回滚点。
- **权限用白名单而非黑名单**：`AllowUsers` 优于 `DenyUsers`，sudo 命令白名单优于全量提权。
- **SELinux/AppArmor 用 `Permissive` 试跑，再转 `Enforcing`**：先用日志确认无误拦，再上强制，避免上线即服务不可用。
- **加固要可观测**：开启 auditd 与日志告警，否则「加固成功但被入侵时无迹可查」。

**常见坑**
- **改 SSH 配置后把自己锁死**：`sshd -t` 先校验语法，且保持一个已登录的备用会话，改完用 `reload` 而非重启。
- **直接 `setenforce 0` 或关闭 MAC 绕过问题**：这会撤销全部强制保护。应通过 `audit2allow` 分析拒绝日志，为服务补策略。
- **用 `chmod 777` 图省事**：人人可写且掩盖属主设计错误。正确做法是查清运行身份（`id`、`ps aux`）后用 `chown`+组或 ACL 精确授权。
- **`PermitRootLogin yes` + 密码登录并存**：这是最常见的高危组合，务必两者一起收紧。
- **发行版混用示例**：SELinux 属于 RHEL 系、AppArmor 属于 Debian/Ubuntu 系；Ubuntu 26.04 用 systemd 259、Fedora 45 用 systemd 262，systemd 相关示例不能跨发行版照抄。
- **只加固不更新**：内核与发行版补丁是加固的底层基础，锁 LTS 但不更新会留下已知漏洞。
- **忽略备份**：防火墙、sshd、sysctl 改动前先导出快照，否则故障时只能凭记忆重建。

## 六、核心要点速查

| 维度 | 关键命令 / 配置 | 说明 |
|---|---|---|
| MAC | `getenforce` / `setenforce` / `aa-status` | SELinux（RHEL 系）/ AppArmor（Debian 系）状态查看 |
| 权限 | `visudo` / `setfacl` / `getfacl` | sudo 白名单与 ACL 精确授权 |
| SSH | `PermitRootLogin no` / `PasswordAuthentication no` | 禁用 root 与密码登录，最高性价比的一步 |
| 防火墙 | `nft list ruleset` / `ufw status` | nftables 1.1.7 为新一代后端 |
| 内核参数 | `sysctl -a` / `sysctl --system` | 关闭重定向、源路由，开启 SYN Cookie |
| 审计 | `auditctl -w` / `ausearch -k` / `journalctl -p err` | 文件访问与运行期日志追溯 |
| 凭据 | `systemd-creds encrypt` | systemd 262 TPM 密封凭据 |
| 回滚 | `sysctl -a > backup` / `nft list ruleset > backup` | 变更前快照，随时可还原 |

## 七、学习资源

1. [kernel.org 内核发布与稳定版列表](https://www.kernel.org/) —— 内核版本与 LTS 维护截止日权威来源
2. [systemd 官方手册（systemd.exec / systemd.creds）](https://www.freedesktop.org/software/systemd/man/latest/) —— 单元加固、TPM 凭据等机制说明
3. [Red Hat: Security Hardening 官方文档](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/) —— SELinux 与系统加固的权威参考
4. [Debian AppArmor 打包跟踪页](https://tracker.debian.org/pkg/apparmor/) —— AppArmor 版本与发行版落地情况
5. [man7.org 手册](https://www.man7.org/linux/man-pages/) —— `sshd_config`、`auditctl`、`sysctl`、`nft` 等命令的权威手册
6. [nftables 官方文档](https://wiki.nftables.org/) —— 新一代包过滤框架用法
7. [Linuxize: SSH Hardening Best Practices](https://linuxize.com/post/ssh-hardening-best-practices/) —— SSH 加固操作清单（实践参考）

## 八、关联笔记

- [[Linux-从入门到精通]] —— Linux 学习主线地图，本知识点位于「阶段四：精通」的安全模块
- [[Web安全最佳实践]] —— 安全加固的上层视角（应用层风险）

## 九、变更记录

- 2026-11-19：首次创建。
