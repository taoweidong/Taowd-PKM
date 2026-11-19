---
title: Linux用户与权限管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 权限管理
  - 用户管理
  - 运维
aliases:
  - Linux权限与用户管理
  - Linux 用户权限
source: 网络资料整理
---

# Linux用户与权限管理

> [!摘要] 内容与定位
> 本篇系统讲解 Linux 的**用户、组与权限**体系：从 UID/GID、`/etc/passwd` 与 `/etc/shadow` 的底层结构，到 rwx 权限位、umask、ACL、SUID 等授权机制，再到 `useradd`/`chmod`/`setfacl`/`sudo` 的落地操作与安全纪律。它是 [[Linux-从入门到精通]] 阶段二的核心知识点，也是后续 systemd 服务管理、容器能力（capabilities）与安全加固的**前置基础**。示例以 Debian/Ubuntu 与 RHEL 系通用命令为准，版本事实以 2026-11 调研快照为依据。

## 一、最新动态（截至 2026-11）

用户与权限管理的核心命令集（`useradd`/`usermod`/`groupadd`/`passwd`/`chsh` 等）由 **shadow-utils** 提供，命令与配置文件结构多年保持稳定，权威手册见 man7.org。本知识点的"最新"主要体现在**配套工具与发行版策略**的演进：

- **提权工具 sudo 仍是事实标准**：`sudoers` 语法与 PAM 认证链路成熟，官方文档是配置的权威依据（[sudo 官方站点](https://www.sudo.ws/)）。
- **强制访问控制（MAC）两条主线并进**：**AppArmor 5.0.2**（Debian/Ubuntu 系打包）与 **SELinux policy 38.1.75**（RHEL 系，RHEL 9.8 于 2026-10 打包）。前者以路径为粒度，后者以类型（type）为粒度，按目标发行版二选一讲解即可。
- **内核与发行版加固特性**：内核 7.x 与 **Debian 13** 引入 **Intel CET、ARM PAC/BTI** 等控制流保护，强化 **ROP/COP/JOP** 缓解——这是权限被滥用后"提权防护"的系统级背景。
- **发行版基线**：Debian 13（trixie，13.7 于 2026-09-12）、Ubuntu 26.04 LTS（26.04.1 于 2026-08-27）、RHEL 10.2（2026-05-19）、Fedora 45（2026-11-03）。用户子系统在这些发行版上行为一致，但 MAC 默认策略随发行版不同。
- **shadow-utils 的具体版本号**在本次调研中未给出明确官方记录，写作与使用时以官方仓库为准。

> [!note] 时效性提示
> 版本与发行版信息为 2026-11 调研快照，生产操作前请回查各官方发布说明与安全公告。

## 二、基础概念

**用户（User）**：系统以数字 **UID** 标识用户。`UID=0` 为超级用户 root；`1~999` 多为系统账号（`daemon`、`nobody` 等，通常无登录 shell）；普通用户从 `1000`（或发行版约定值）起分配。`/etc/login.defs` 中的 `UID_MIN` 决定普通用户起始值。

**组（Group）**：以 **GID** 标识，用于批量授权。每个用户有且仅有一个**主组（primary group）**，可同时属于多个**附加组（supplementary group）**。`/etc/group` 记录组名、GID 与成员，`/etc/gshadow` 保存组口令哈希。

**密码存储**：`/etc/passwd` 对所有人可读，因此口令哈希单独存放于 **`/etc/shadow`**（权限 `640 root:shadow`）。哈希由算法+盐生成，现代系统默认使用 **yescrypt** 或 **SHA-512 crypt**，不可逆。

**权限模型**：每个文件/目录有 **属主（owner）、属组（group）、其他（others）** 三类主体，各含 **r（读）、w（写）、x（执行）** 三个位。目录的 `x` 表示"可进入并访问其下条目"，因此**只读目录无法列目录、无执行位无法进入**。

**特殊权限位**：
- **SUID**（4xxx）：执行时以**属主身份**运行，如 `/usr/bin/passwd`（4755）。
- **SGID**（2xxx）：执行时以**属组身份**运行，或新建文件继承目录属组。
- **SBIT / sticky bit**（1xxx）：仅目录属主与文件属主可删除，如 `/tmp`（1777）。

**umask**：决定新建文件/目录的**默认权限被屏蔽掉哪些位**。常见 `umask 022` → 新文件 `644`、新目录 `755`。

**ACL 与 capabilities**：传统 rwx 三元模型不够细，ACL 支持按用户/组单独授权；**capabilities** 把 root 的权限拆成细粒度能力（如 `CAP_NET_BIND_SERVICE`），供非 root 进程按需提权。

**sudo 与 su**：`su` 切换到指定用户（需目标口令）；`sudo` 以 root（或其他用户）身份执行**单条命令**，是生产环境"最小授权"的首选。

## 三、核心机制

**1. 认证与授权流程**：登录时 PAM（可插拔认证模块）依次完成账号校验（`/etc/shadow` 口令哈希比对）、会话建立；授权时内核按"DAC 自主访问控制"检查：先看 SUID/SGID 特殊位，再按 **属主 → 属组 → 其他** 顺序匹配第一个匹配的权限三元组，逐位判断是否放行。

**2. `/etc/passwd` 字段**：`用户名:口令占位(x):UID:GID:GECOS(备注):家目录:登录shell`。口令列恒为 `x`，真实哈希在 `/etc/shadow` 中一一对应。

**3. 登录 Shell 与账号控制**：`/sbin/nologin`、`/bin/false` 可禁止交互登录；账号锁定（`usermod -L`）在哈希前加 `!` 前缀，PAM 直接拒绝，但不删除口令。

**4. ACL 机制**：在 rwx 之外维护 `user:名称:权限`、`group:名称:权限`、`mask:权限` 条目。`mask` 是**有效权限上限**，会截断 `user:`/`group:` 中超出的部分，这是 ACL 最常见的"改了不生效"原因。目录上的**默认 ACL（d:）**可让新建文件自动继承授权。

**5. capabilities 与 root 拆分**：Linux 将 root 的权限拆为约 40 项 capability。进程的有效 capability 集合决定能否执行特权操作；容器/服务常通过 `CapabilityBoundingSet`、`--cap-add` 等按最小集合提权，避免"整包 root"。

**6. sudo 与 PAM**：`sudo` 依据 `/etc/sudoers`（及 `/etc/sudoers.d/`）判定"谁可执行什么命令、是否需要口令、以谁的身份执行"，认证同样走 PAM，因此 `/etc/security/limits.conf` 等 PAM 限制也会作用于 sudo 会话。

**7. MAC 叠加**：在 DAC 之上，SELinux（RHEL 系，基于类型强制）或 AppArmor（Debian/Ubuntu 系，基于路径）可**额外拒绝**越权访问。二者与 rwx、ACL 并存，排查"明明有权限却访问被拒"时要先排除 MAC 拦截。

## 四、实践步骤（含代码/命令示例）

### 4.1 查看与创建用户、组

```bash
# 查看当前身份与所属组
whoami
id
groups

# 查看账号与口令记录（getent 绕过 NSS 缓存，比直接 cat 更可靠）
getent passwd devops
getent group appops
sudo getent shadow devops    # 需 root，仅查看哈希状态

# 新建组与用户：-m 建家目录，-s 指定 shell，-G 指定附加组
sudo groupadd -r appops
sudo useradd -m -s /bin/bash -G appops -c "应用运维账号" devops

# 设置口令、追加附加组（-a 必须与 -G 同用，避免覆盖原有组）
sudo passwd devops
sudo usermod -aG appops devops

# 锁定 / 解锁 / 改登录 shell / 过期控制
sudo usermod -L devops          # 锁定账号
sudo usermod -U devops          # 解锁账号
sudo usermod -s /sbin/nologin backup
sudo chage -E 2027-12-31 devops   # 设置账号过期日期

# 删除用户；如需一并清家目录用 -r，谨慎操作
sudo userdel devops
```

### 4.2 权限管理

```bash
# 数字法与符号法设置权限
chmod 755 /srv/app/script.sh
chmod u+rwx,g+rx,o+rx /srv/app/script.sh
chmod -R go-w /srv/app/config     # 递归去掉组与其他人写权限

# 修改属主与属组
sudo chown -R appops:appops /srv/app
sudo chgrp appops /srv/app/config

# 查看权限详情（含 inode）
ls -l /srv/app/script.sh
stat /srv/app/script.sh
```

### 4.3 ACL 精确授权

```bash
# 为 devops 单独授予 r-x，不影响其他用户
sudo setfacl -m u:devops:rx /srv/app/config

# 默认 ACL：目录下新建的文件自动继承
sudo setfacl -m d:u:devops:rx /srv/app/config

# 查看与移除
getfacl /srv/app/config
sudo setfacl -x u:devops /srv/app/config
```

### 4.4 sudo 最小授权

```bash
# 用 visudo 编辑，写入前自动做语法校验，避免改错导致无法提权
sudo visudo
sudo visudo -c                   # 只做语法检查

# 推荐把规则放入 /etc/sudoers.d/ 下的独立文件，权限必须为 440
sudo tee /etc/sudoers.d/devops <<'EOF'
# 仅允许 devops 免密重启应用服务（命令白名单，不用通配 ALL）
devops ALL=(root) NOPASSWD: /usr/bin/systemctl restart app
EOF
sudo chmod 440 /etc/sudoers.d/devops
sudo visudo -c && sudo -l -U devops   # 校验并查看该用户实际权限
```

### 4.5 审计特殊权限

```bash
# 找出系统上的 SUID/SGID 文件，对照基线排查异常
sudo find / -xdev -perm -4000 -type f -exec ls -l {} \;
sudo find / -xdev -perm -2000 -type f -exec ls -l {} \;
```

## 五、最佳实践与常见坑

> [!warning] 不要用 chmod -R 777
> `chmod -R 777` 人人可写，过不了安全审计，还会掩盖真正的属主设计错误。正确路径：`ps aux`/`id` 弄清"谁在访问"，再 `chown` 换属主或 `setfacl` 精确授权。

- **日常不用 root 登录**：普通用户 + `sudo` 命令白名单。`sudoers` 中避免 `user ALL=(ALL) ALL` 这类全量授权，`NOPASSWD` 只在确有必要时使用。
- **SUID 只留给受控二进制**：内核会**忽略 shell 脚本的 SUID**，给自研程序加 SUID 前先评估提权面；定期用 `find ... -perm -4000` 审计基线。
- **用 `-aG` 追加组**：`usermod -G` 不加 `-a` 会**覆盖**原有附加组，属于高频事故点。
- **删除用户要清彻底**：除 `userdel` 外，还需清理 `crontab -l -u 用户名`、家目录、以及用 `find / -user 用户名` 迁移或删除遗留文件属主，否则出现"幽灵账号"。
- **保护口令文件权限**：`/etc/shadow` 保持 `640 root:shadow`，切勿放宽；不要在脚本、日志中打印明文口令或哈希。
- **ACL 改了不生效先看 mask**：`getfacl` 检查 mask 是否截断了授权，必要时用 `-m m:rwx` 调整。
- **先校验再生效**：改 `sudoers` 用 `visudo -c`，批量改配置先备份，改动后在测试实例验证再推生产。

## 六、核心要点速查

| 项目 | 关键值 / 命令 |
|---|---|
| 用户标识 | `UID=0` 为 root；系统用户 1~999；普通用户从 `UID_MIN`（常为 1000）起 |
| 核心配置文件 | `/etc/passwd`、`/etc/shadow`（640）、`/etc/group`、`/etc/gshadow`、`/etc/sudoers`、`/etc/sudoers.d/` |
| 权限数字 | `7=rwx`、`6=rw-`、`5=r-x`、`4=r--`、`0=---`；常用 `755`/`644`/`700`/`640` |
| 特殊位 | `4xxx`=SUID、`2xxx`=SGID、`1xxx`=SBIT（`/tmp` 为 1777） |
| 用户/组命令 | `useradd`、`usermod`、`userdel`、`groupadd`、`passwd`、`chsh`、`chage` |
| 权限命令 | `chmod`、`chown`、`chgrp`、`setfacl`、`getfacl`、`umask` |
| 提权命令 | `sudo`、`visudo`、`su`、`sudo -l`、`sudo -k` |
| 审计命令 | `id`、`groups`、`getent`、`find -perm -4000` |

## 七、学习资源

1. [man7.org: useradd(8)](https://www.man7.org/linux/man-pages/man8/useradd.8.html) —— 用户/组管理命令权威手册
2. [man7.org: chmod(1) 与 acl(5)](https://www.man7.org/linux/man-pages/man1/chmod.1.html) —— 权限位与 ACL 语义
3. [sudo 官方文档](https://www.sudo.ws/) —— `sudoers` 语法与 PAM 集成
4. [Debian tracker: AppArmor](https://tracker.debian.org/pkg/apparmor/) —— AppArmor 5.0.2 打包信息
5. [Red Hat: Security Hardening](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/) —— RHEL 系 SELinux 与加固实践
6. [Debian 发布页](https://www.debian.org/releases/) 与 [Ubuntu 26.04 发行说明](https://documentation.ubuntu.com/release-notes/26.04/) —— 发行版基线
7. [Kernel.org 发布页](https://www.kernel.org/releases.html) —— 内核版本与加固特性背景

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习路线中的位置（阶段二）
- [[Linux常用命令集]] —— `id`/`chmod`/`useradd` 等命令速查
- [[Linux系统管理与运维要点]] —— 生产环境的权限治理与运维实践
- [[Web安全最佳实践]] —— 最小权限与加固的上层视角

## 九、变更记录

- 2026-11-19：首次创建。
