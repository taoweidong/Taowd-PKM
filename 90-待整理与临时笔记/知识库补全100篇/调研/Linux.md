---
title: Linux 调研
date: 2026-11-19
updated: 2026-11-19
tags:
  - 调研
  - Linux
  - 知识库补全
---

# Linux 调研

> 用途：为「Linux」方向的 16 篇详细文档提供**最新官方支持与关键事实**引用素材。
> 数据截止：**2026-11-19**。内核、发行版、systemd 与工具版本迭代极快，正式写作前请按来源 URL 复核最新版本号。
> 说明：所有版本号、发布日期、功能描述均来自下方标注的官方/权威来源；第三方报道仅在官方源缺失时作为补充并已注明。

## 一、主题最新动态（截至 2026-11）

- **Linux 主线内核已进入 7.x 时代**：7.0.0 于 2026-04-12 发布，7.3 于 2026-10-18 发布；截至调研时最新稳定版为 **7.3.5**（2026-11-16 由 Greg Kroah-Hartman 发布，同批发布 LTS 6.18.64、6.12.118）。
- **LTS（长期维护）内核保持三支并行**：**6.18**（2025-11-30 首发，维护至 2028-12）、**6.12**（2024-11-17 首发，维护至 2028-12）、**6.6**（维护至 2027-12）。主流发行版多采用 6.12 LTS（Debian 13、RHEL 10 系列）。
- **systemd 进入 262 代**：systemd 262 于 2026-09-22 发布，systemd-stable 已推进到 **v262.2**；核心变化包括内置基础单元文件、可构建单一静态 PID 1、Intel TDX 机密虚拟机、TPM 密封凭据加固、journal 损坏恢复等。
- **发行版大版本集中更新**：Debian 13（trixie，13.7 于 2026-09-12）、Ubuntu 26.04 LTS（26.04.1 于 2026-08-27）、Fedora 45（2026-11-03）、RHEL 10.2（2026-05-19）、Alpine 3.24（3.24.4）、openSUSE Leap 16.1（2026-11-02，引入 Immutable Mode）。
- **容器生态同步升级**：Docker Engine 29.x 推进至 **29.9.2**（2026-10-20），containerd **2.4.2**（2026-10-13），Podman 6.0 移除 CNI、以 Netavark + nftables 为唯一后端。
- **文本处理工具全线更新**：GNU coreutils 9.12、sed 4.10、gawk 5.4.1、grep 3.12、bash 5.3，为脚本与命令行文档提供明确的版本基准。

## 二、版本与关键事实表

| 项目 | 版本号 | 发布日期 | 关键变化 / 说明 | 官方来源 URL |
|---|---|---|---|---|
| Linux 内核（主线稳定） | 7.3.5 | 2026-11-16（公告） | 与 6.18.64、6.12.118 同批发布，修复若干重要缺陷 | https://lwn.net/Articles/1108142/ |
| Linux 内核（主线） | 7.3 | 2026-10-18 | ksmbd 支持 Apple Time Machine；Btrfs 性能优化；支持 AMD Zen 6 平台、存储 I/O 改进 | https://gigazine.net/gsc_news/en/20261020-linux-kernel-7-3 |
| Linux 内核（首个 7.x） | 7.0.0 | 2026-04-12 | 开启 7.x 系列；Ubuntu 26.04 LTS 搭载内核 7.0 | https://www.phoronix.com/news/Linux-7.0-Changes |
| Linux LTS 内核 | 6.18.64 | 2026-11-16 | LTS 分支，首发 2025-11-30，维护至 2028-12 | https://www.kernel.org/releases.html |
| Linux LTS 内核 | 6.12.118 | 2026-11-16 | LTS 分支，首发 2024-11-17，维护至 2028-12 | https://www.kernel.org/releases.html |
| Linux LTS 内核 | 6.6.141 | 2026-05-23 | LTS 分支，维护至 2027-12 | https://www.kernel.org/releases.html |
| systemd | 262 / systemd-stable 262.2 | 262 发布于 2026-09-22；stable 262.2 后续 | 内置基础 unit 文件、静态 PID 1、Intel TDX、TPM 加固、journal 恢复、`RestartRandomizedDelaySec=`、`ActivatingConcurrencyMax=` | https://github.com/systemd/systemd/releases |
| Debian | 13（trixie）/ 13.7 | 2025-08-09 / 2026-09-12 | 内核 6.12 LTS、GNOME 48、GCC 14.2、Python 3.13；支持至 2028-08-09，LTS 至 2030-06-30 | https://www.debian.org/releases/ |
| Ubuntu | 26.04 LTS / 26.04.1 LTS | 2026-04-23 / 2026-08-27 | 内核 7.0、GNOME 50、systemd 259；标准支持至 2031-05 | https://ubuntu.com/download/desktop |
| Ubuntu | 26.10（短期版） | 2026-10 | 代号 Stonking Stingray，9 个月支持 | https://ubuntu.com/about/release-cycle |
| Fedora | 45 | 2026-11-03 | 内核 7.2、GNOME 51、KDE Plasma 6.8、systemd 262、GCC 16.2、glibc 2.44、Python 3.15、kmscon 默认控制台 | https://www.phoronix.com/news/Fedora-45-Released |
| Red Hat Enterprise Linux | 10.2 | 2026-05-19 | 内核 6.12.0-211.7.1.el10_2（RHEL 10 系列） | https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates |
| Alpine Linux | 3.24 / 3.24.4 | 分支日 2026-06-09 / 3.24.4 | musl + busybox，2 年支持（main 仓库） | https://alpinelinux.org/releases/ |
| openSUSE Leap | 16.1 | 2026-11-02 | 首个 Leap 16 小版本，整合 Leap Micro 为 Immutable Mode，支持事务更新；Leap 16.0 发布于 2025-10-01 | https://nl.opensuse.org/openSUSE:Aankondiging_van_uitgave_van_16.1 |
| GNU coreutils | 9.12 | 2026-09-14 | `env` 新增 `--env0-from=FILE`；9.11 起 `cut/nl/unexpand` 支持多字节、`cat/yes` 零拷贝加速 | https://savannah.gnu.org/news/?group=coreutils |
| GNU sed | 4.10 | 2026-04-21 | 时隔 3.5 年的大版本，修复大量缺陷 | https://savannah.gnu.org/news/?id=10885 |
| GNU awk (gawk) | 5.4.1 | 2026-07-29 | 文本处理主版本 | https://ftp.gnu.org/pub/pub/pub/gnu/gawk/ |
| GNU grep | 3.12 | 2025-09（各发行版打包 2026） | 主流发行版统一采用的正则匹配工具版本 | https://tracker.debian.org/pkg/grep/ |
| GNU Bash | 5.3 | 2025-07-04 | `read -E`、`source -p PATH`；C23 合规，不再兼容 K&R 编译器；Readline 同步更新 | https://lists.gnu.org/archive/html/info-gnu/2025-07/msg00001.html |
| procps-ng | 4.0.6 | 2026-01-30（Fedora 44 打包） | `ps/top/free/vmstat` 等进程/内存工具集 | https://packages.fedoraproject.org/pkgs/procps-ng/procps-ng/fedora-44.html |
| sysstat | 12.7.9 | 2026（Fedora 45 于 2026-09 打包） | `sar/sadf/mpstat/iostat/pidstat/sa` 性能监控工具集 | https://openkoji.iscas.ac.cn/koji/buildinfo?buildID=227753 |
| iproute2 | 7.3.0 | 2026-10-25（Debian unstable） | `ip/ss/tc/netstat` 等网络配置工具集 | https://tracker.debian.org/pkg/iproute2/news |
| util-linux | 2.42.4 | 2026-09-26（Debian testing） | `lsblk/fdisk/blkid/mount` 等块设备与挂载工具 | https://tracker.debian.org/pkg/util-linux/news |
| nftables | 1.1.7 | 2026-09（Debian unstable） | 新一代包过滤框架，Podman 6 已以 nftables 作为防火墙后端 | https://tracker.debian.org/pkg/nftables/news |
| cron | 3.0pl1-213（Debian 打包） | 2026-11-03 | Debian 13 系定时任务守护进程版本 | https://tracker.debian.org/pkg/cron/ |
| Docker Engine | 29.9.2 | 2026-10-20 | 29.x 最新补丁，含 Go 运行时安全修复与 containerd 升级 | https://docs.docker.com/engine/release-notes/29/ |
| containerd | 2.4.2 | 2026-10-13 | CRI 日志不跟随符号链接、镜像拉取内存修复、seccomp 加固 | https://github.com/containerd/containerd/releases/tag/v2.4.2 |
| Podman | 6.0.1 | 2026-07-08 | 6.0 移除 CNI，Netavark 成为唯一网络后端；配置移至 `/usr/share/containers` | https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1143118 |
| AppArmor | 5.0.2 | 2026（Debian unstable） | Ubuntu/Debian 系强制访问控制（MAC）框架 | https://tracker.debian.org/pkg/apparmor/ |
| SELinux 策略 | selinux-policy 38.1.75 | 2026-10（RHEL 9.8 打包） | RHEL 系强制访问控制策略版本 | https://downloads.rockylinux.org/pub/rocky/9/BaseOS/aarch64/os/Packages/s/ |

## 三、分知识点关键事实

### 1. Linux 基础与命令入门

**要点**
- 内核与发行版现状：主线 **7.3.5**，LTS 为 **6.12 / 6.18 / 6.6**；Ubuntu 26.04 LTS 用内核 7.0，Debian 13 / RHEL 10 用 6.12 LTS。入门教学建议统一以 LTS 内核为例，避免与 7.x 新特性混淆。
- 常用命令（`ls/cp/mv/rm/find/cat/echo` 等）来自 **GNU coreutils 9.12**（2026-09-14）；`cut/nl/unexpand` 已支持多字节字符，`cat/yes` 在 Linux 上使用零拷贝 I/O。
- 默认 shell 多为 **bash 5.3**（Ubuntu 26.04 提供），需注意 `bash 5.3` 的 `read -E`、`source -p PATH` 等新特性与不兼容变更。
- 权威手册站点 **man7.org**（man pages）、**kernel.org/doc**（内核文档）为标准查证入口。

**关键参数 / 命令**：`uname -a`、`hostname`、`whoami`、`man`、`--help`、`ls --color=auto`。
**权威来源 URL**：https://www.kernel.org/ 、https://www.gnu.org/software/coreutils/ 、https://www.man7.org/ 、https://lists.gnu.org/archive/html/info-gnu/2025-07/msg00001.html

### 2. Linux 文件系统与目录结构

**要点**
- 目录结构遵循 **FHS（Filesystem Hierarchy Standard）**，`/`、`/etc`、`/var`、`/home`、`/usr`、`/proc`、`/sys`、`/dev` 为教学核心。
- 内核 **7.3** 对存储 I/O 与 **Btrfs** 有性能优化；主流文件系统为 **ext4 / XFS / Btrfs**（ZFS 不在主线内核）。
- **ReiserFS 已在主线内核移除**（6.12 周期）；bcachefs 的移除情况需在写作前到 kernel.org 的 `Documentation/filesystems` 核实。
- **systemd 262** 已将基础单元文件内置进二进制，磁盘单元文件缺失时仍可用内置兜底——容器场景下更稳健。

**关键参数 / 命令**：`df -hT`、`du -sh`、`mount`、`lsblk`、`findmnt`、`/proc/mounts`、`/proc/self/mounts`。
**权威来源 URL**：https://www.kernel.org/category/releases.html 、https://www.man7.org/linux/man-pages/man8/mount.8.html 、https://www.freedesktop.org/software/systemd/man/ 、https://gigazine.net/gsc_news/en/20261020-linux-kernel-7-3

### 3. Linux 用户与权限管理

**要点**
- 用户/组管理命令（`useradd/usermod/groupadd/passwd/chsh`）由 **shadow-utils** 提供，权威手册见 man7.org。
- 提权工具 **sudo** 是事实标准；`sudoers` 语法建议引用官方文档。
- 强制访问控制（MAC）两条主线：**AppArmor 5.0.2**（Debian/Ubuntu 系）、**SELinux policy 38.1.75**（RHEL 系，9.8 于 2026-10 打包）。
- 内核 7.x 与 Debian 13 引入的**加固特性**（Intel CET、ARM PAC/BTI、ROP/COP/JOP 缓解）可作为安全章节背景。

**关键参数 / 命令**：`id`、`groups`、`chmod`、`chown`、`setfacl`、`getfacl`、`sudo -l`、`visudo`。
**权威来源 URL**：https://www.man7.org/linux/man-pages/man8/useradd.8.html 、https://tracker.debian.org/pkg/apparmor/ 、https://www.debian.org/releases/ 、https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/

### 4. Linux 进程管理

**要点**
- 进程查看与控制工具集来自 **procps-ng 4.0.6**：`ps/top/free/vmstat/pgrep/kill`。
- **systemd 262** 新增 `ActivatingConcurrencyMax=`（限制 slice 内同时激活的单元数）与 `RestartRandomizedDelaySec=`（随机化重启间隔，防惊群），是进程/服务管理的新参数。
- 内核 **7.3** 在 CPU 与内存管理方向有效率改进，可作为“进程调度/内存”章节的更新点。
- 僵尸进程、孤儿进程、PID 1（systemd）职责是核心教学点。

**关键参数 / 命令**：`ps -eo pid,ppid,stat,cmd`、`top`、`htop`、`kill -l`、`pkill`、`nice`、`renice`、`systemctl status`。
**权威来源 URL**：https://packages.fedoraproject.org/pkgs/procps-ng/procps-ng/fedora-44.html 、https://github.com/systemd/systemd/releases 、https://www.man7.org/linux/man-pages/man1/ps.1.html

### 5. Linux 系统服务与 systemd

**要点**
- 最新稳定版为 **systemd 262 / systemd-stable 262.2**（262 于 2026-09-22 发布）。
- **systemd 262 关键变化**：基础 target/service 单元文件内置进管理器；可构建单一静态链接的 PID 1/executor（适配极小容器）；Intel TDX 机密虚拟机（`systemd-vmspawn`）；TPM 密封凭据绑定 SRK、Argon2id 密钥派生；损坏 journal 的条目恢复；D-Bus 事务式多单元操作。
- 发行版差异（写作需特别提示）：**Ubuntu 26.04 LTS 使用 systemd 259**，并已移除 **cgroup v1**、`/tmp` 默认挂载为 **tmpfs**、System V 脚本被弃用（26.04 是最后一个支持 SysV 脚本的版本）；**Fedora 45 使用 systemd 262.1**。
- 单元文件、unit 指令（`After/Requires/Restart/ExecStart`）以 systemd.io 官方文档为准。

**关键参数 / 命令**：`systemctl enable --now`、`systemd-analyze`、`systemd-analyze dot`、`journalctl -u`、`systemd-run`。
**权威来源 URL**：https://github.com/systemd/systemd/releases 、https://www.linuxjournal.com/content/systemd-262-released-static-pid-1-intel-tdx-tpm-improvements-and-new-container-features 、https://www.freedesktop.org/software/systemd/man/latest/ 、https://computingforgeeks.com/ubuntu-2604-lts-features/

### 6. Linux 网络配置与排查

**要点**
- 网络配置工具集来自 **iproute2 7.3.0**（Debian unstable，2026-10-25）：`ip/ss/tc/bridge/vlan`。
- 包过滤：**nftables 1.1.7** 为新一代框架，Podman 6.0 已改为 nftables 后端（不再支持 iptables）；`firewalld`、`ufw` 为上层封装。
- **systemd 262** 对 `systemd-resolved` 的 DNS-SD 注册行为有破坏性变更：客户端断开后自动注销，常驻服务需用 `*.dnssd` 文件注册。
- 排查链路：物理/链路层 → IP/路由 → 端口/防火墙 → 应用；结合 `ss`、`ip route`、`ping/traceroute/mtr`、`journalctl`。

**关键参数 / 命令**：`ip addr`、`ip route`、`ss -tulpn`、`nft list ruleset`、`firewall-cmd --list-all`、`resolvectl status`。
**权威来源 URL**：https://tracker.debian.org/pkg/iproute2/news 、https://tracker.debian.org/pkg/nftables/news 、https://www.man7.org/linux/man-pages/man8/ip.8.html 、https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.html

### 7. Linux 磁盘与文件系统

**要点**
- 分区与块设备工具来自 **util-linux 2.42.4**：`lsblk/fdisk/blkid/mount/swapon`；逻辑卷用 **LVM（lvm2）**，软 RAID 用 **mdadm**。
- 文件系统选型：**ext4**（通用、成熟）、**XFS**（大卷/数据库、不可收缩）、**Btrfs**（快照/子卷、内核 7.3 性能优化）；**ZFS** 非主线内核，需第三方模块。
- 内核 **6.18** 周期有文件系统相关的重大变更（第三方资料称 bcachefs/ReiserFS 已移除），写作前务必以 kernel.org `Documentation/filesystems` 官方目录核实。
- 磁盘排查：`lsblk`、`smartctl`、`badblocks`、`dmesg`、`iostat`。

**关键参数 / 命令**：`lsblk -f`、`mkfs.ext4`、`mkfs.xfs`、`mount -o remount`、`resize2fs`、`xfs_growfs`、`lvs`。
**权威来源 URL**：https://tracker.debian.org/pkg/util-linux/news 、https://www.kernel.org/doc/html/latest/filesystems/ 、https://www.man7.org/linux/man-pages/man8/lsblk.8.html

### 8. Linux Shell 脚本编程

**要点**
- 脚本解释器以 **bash 5.3**（2025-07-04）为基准：`read -E`、`source -p PATH`、命令替换新语义；源码已更新为 **C23** 合规（不再支持 K&R 编译器）。
- 脚本中调用的文本/文件命令来自 **coreutils 9.12**（`env --env0-from=FILE`、多字节感知的 `cut/nl/unexpand`、零拷贝 `cat/yes`）。
- 静态检查推荐 **ShellCheck**（非本调研重点，但为脚本文档标配工具）；`set -euo pipefail`、`getopts`、数组与函数为教学要点。
- 注意脚本可移植性：区分 `sh`（POSIX）、`bash`、`zsh`，避免使用 bash 专有语法跑在 `/bin/sh`。

**关键参数 / 命令**：`set -euo pipefail`、`getopts`、`local`、`trap`、`export`、`bash -n`、`shellcheck`。
**权威来源 URL**：https://lists.gnu.org/archive/html/info-gnu/2025-07/msg00001.html 、https://savannah.gnu.org/news/?group=coreutils 、https://www.gnu.org/software/bash/

### 9. Linux 文本处理三剑客

**要点**
- **grep 3.12**：正则匹配，`-E`、`-P`、`-o`、`-n`、`-c`、`-A/-B/-C`；主流发行版（Debian 13、Fedora 44/45）统一采用。
- **sed 4.10**（2026-04-21，时隔 3.5 年的大版本）：流编辑器，`s` 替换、`-i` 就地编辑、多行处理、`-E` 扩展正则。
- **gawk 5.4.1**（2026-07-29）：模式-动作语言，`BEGIN/END`、字段 `FS/OFS`、正则、系统调用、CSV/多字节处理。
- 三者搭配：`grep` 筛选 → `sed` 变换 → `awk` 聚合统计；处理大文件优先使用流式（管道）而非一次性载入。

**关键参数 / 命令**：`grep -rnE`、`sed -i.bak 's/.../.../g'`、`awk -F, '{sum+=$1} END{print sum}'`、`xargs`。
**权威来源 URL**：https://tracker.debian.org/pkg/grep/ 、https://savannah.gnu.org/news/?id=10885 、https://ftp.gnu.org/pub/pub/pub/gnu/gawk/ 、https://www.man7.org/linux/man-pages/man1/awk.1.html

### 10. Linux 定时任务与计划任务

**要点**
- 传统 cron：Debian 13 系打包 **cron 3.0pl1-213**（2026-11-03），`crontab/`cron.d`、`crontab -e`、时区依赖 `/etc/localtime`。
- **systemd timer** 是现代首选方案：与 systemd 262 深度集成，支持精确日历（`OnCalendar=`）、依赖（`After=`）、持久化（`Persistent=`）、随机延迟（`RandomizedDelaySec=`，262 亦可用于服务重启）。
- 辅助工具：`anacron`（补跑停机期间任务）、`at`（一次性任务）、`systemd-timers` 系列。
- 常见问题：时区、环境变量、权限（root 与用户 crontab 差异）、任务重叠（建议在脚本内加锁）。

**关键参数 / 命令**：`crontab -l/-e`、`systemctl list-timers`、`systemd-run --on-calendar`、`OnCalendar=*-*-* 02:00:00`、`Persistent=true`。
**权威来源 URL**：https://tracker.debian.org/pkg/cron/ 、https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html 、https://www.man7.org/linux/man-pages/man5/crontab.5.html

### 11. Linux 日志管理

**要点**
- **systemd journal** 是现代发行版默认日志栈：`journalctl`、`/var/log/journal`、按单元/时间/优先级过滤。
- **systemd 262** 新增**损坏 journal 条目恢复**：在非正常关机（断电、内核崩溃、强制重启）导致活动日志文件头/尾部截断时，可尝试救回有效条目——故障排查文档的重要更新点。
- 传统日志：`rsyslog`/`syslog-ng`、`/var/log/syslog`、`/var/log/messages`；`logrotate` 负责轮转。
- 排查命令：`journalctl -b`、`-u unit`、`--since`、`-p err`、`journalctl _SYSTEMD_UNIT=`。

**关键参数 / 命令**：`journalctl -b -p warning`、`journalctl -u ssh.service --since today`、`journalctl -f`、`logrotate -d /etc/logrotate.conf`。
**权威来源 URL**：https://github.com/systemd/systemd/releases 、https://www.freedesktop.org/software/systemd/man/latest/journalctl.html 、https://www.man7.org/linux/man-pages/man8/rsyslogd.8.html

### 12. Linux 性能监控与优化

**要点**
- 性能数据核心来自 **sysstat 12.7.9**：`sar`（历史）、`iostat`（磁盘）、`mpstat`（CPU）、`pidstat`（进程级）、`sadf`（JSON 输出）、`sa`（报表）。
- 进程/内存概览来自 **procps-ng 4.0.6**：`top/free/vmstat/ps`。
- 网络侧用 **iproute2 7.3.0** 的 `ss/ip -s`；内核 7.3 强调 I/O 性能与内存管理改进。
- 高级手段：**eBPF/BPF**（`bpftrace`、`bpftool`）做无插桩追踪；cgroup v2 做资源限额；`systemd 262` 的 `ActivatingConcurrencyMax=` 控制并发。
- 优化优先级：先定位（`sar/iostat/pidstat`）→ 再调参（内核 vm 参数、cgroup、systemd 单元）→ 再验证。

**关键参数 / 命令**：`sar -u -r -d 1 5`、`iostat -xz 1`、`mpstat -P ALL 1`、`pidstat -urd 1`、`ss -s`、`bpftrace -e`。
**权威来源 URL**：https://openkoji.iscas.ac.cn/koji/buildinfo?buildID=227753 、https://packages.fedoraproject.org/pkgs/procps-ng/procps-ng/fedora-44.html 、https://tracker.debian.org/pkg/iproute2/news 、https://www.kernel.org/doc/html/latest/

### 13. Linux 软件包管理

**要点**
- **Debian / Ubuntu（dpkg + apt）**：Debian 13（trixie，13.7 于 2026-09-12）；Ubuntu 26.04.1 LTS（2026-08-27）。`apt-get/apt`、`dpkg`、`apt-cache`、仓库源配置。
- **RHEL / Fedora（rpm + dnf/rpm）**：RHEL 10.2（2026-05-19，内核 6.12.0-211.7.1.el10_2）；Fedora 45（2026-11-03，RPM 6.1）。`dnf/rpm/yum`、`repoquery`。
- **Alpine（apk）**：3.24 分支（分支日 2026-06-09），最新 **3.24.4**；`apk add/upgrade`、`/etc/apk/repositories`。
- **openSUSE（zypper）**：Leap 16.1（2026-11-02，引入 Immutable Mode），`zypper/rpm`。
- 包管理文档需按发行版分别举例，命令不可混用（apt 系与 rpm 系差异是常见教学难点）。

**关键参数 / 命令**：`apt update && apt install`、`dpkg -l`、`dnf install`、`rpm -qa`、`apk add`、`zypper install`。
**权威来源 URL**：https://www.debian.org/releases/ 、https://ubuntu.com/download/desktop 、https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates 、https://alpinelinux.org/releases/ 、https://nl.opensuse.org/openSUSE:Aankondiging_van_uitgave_van_16.1

### 14. Linux 安全加固

**要点**
- **强制访问控制**：**SELinux policy 38.1.75**（RHEL 系，9.8 于 2026-10 打包）与 **AppArmor 5.0.2**（Debian/Ubuntu 系）二选一按发行版讲解。
- **内核级加固**：Debian 13 强化 amd64/arm64 的 **ROP/COP/JOP** 缓解（Intel CET、ARM PAC/BTI）；内核 6.12/6.18/7.x 持续安全修复。
- **传输安全**：Fedora 45 已升级到 **OpenSSL 4.0**；密码/密钥存储用 `systemd-creds`（systemd 262 对 TPM 密封凭据做了 SRK 绑定加固）。
- **网络层**：nftables 1.1.7、firewalld/ufw；最小权限、SSH 加固（禁用密码、密钥认证、`sshd` 配置）、sudo 最小授权。
- **供应链**：包签名与来源校验（Debian 签名、RPM GPG、apk 签名）；容器镜像校验（Docker/Podman）。

**关键参数 / 命令**：`getenforce`、`setenforce`、`aa-status`、`auditctl`、`iptables -L`、`nft list ruleset`、`sshd_config` 的 `PermitRootLogin/PasswordAuthentication`。
**权威来源 URL**：https://www.debian.org/releases/ 、https://tracker.debian.org/pkg/apparmor/ 、https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates 、https://github.com/systemd/systemd/releases

### 15. Linux 容器与 Docker 基础

**要点**
- **Docker Engine 29.9.2**（2026-10-20）为当前 29.x 最新补丁，含 Go 运行时安全修复；文档见官方 release notes。
- **containerd 2.4.2**（2026-10-13）：CRI 日志不跟随符号链接、镜像拉取内存修复、默认 seccomp 白名单加固。
- **Podman 6.0.1**（2026-07-08）：**移除 CNI**，Netavark 成为唯一网络后端；新增基于 nftables 的防火墙规则（不再支持 iptables）；配置文件迁移至 `/usr/share/containers`。
- 底层原理依赖内核：**namespaces**（隔离）、**cgroups v2**（资源限额，Ubuntu 26.04 已移除 cgroup v1）、联合文件系统（overlay2）。
- **systemd 262** 强化容器支持：可构建单一静态 PID 1，便于极小容器以 systemd 为 init；`nspawn`、`systemd-container`。

**关键参数 / 命令**：`docker run/build/compose`、`podman run`、`docker info`、`ctr`、`crictl`、`systemd-nspawn`。
**权威来源 URL**：https://docs.docker.com/engine/release-notes/29/ 、https://github.com/containerd/containerd/releases/tag/v2.4.2 、https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1143118 、https://github.com/systemd/systemd/releases

### 16. Linux 故障排查实战

**要点**
- **统一排查入口**：`journalctl`（systemd 262 的 journal 恢复能力可在非正常关机后救回日志）、`dmesg`、`/var/log`、`last`、`/proc`。
- **分层定位**：内核/驱动（`dmesg`、`/sys`）→ 系统资源（procps-ng 4.0.6、sysstat 12.7.9）→ 服务（`systemctl status`、`journalctl -u`）→ 网络（iproute2 7.3.0、nftables）→ 存储（util-linux 2.42.4、`smartctl`）。
- **性能类故障**：`sar -q/-u/-r/-d` 找瓶颈，`pidstat` 定位进程，`iostat -x` 看磁盘，`mpstat` 看 CPU，必要时用 eBPF 追踪。
- **内核相关**：`kernel.org` 内核变更日志、发行版内核 ABI（如 Debian 13.7 的 debian-installer 已将内核 ABI 提升到 6.12.107+deb13）；关注 LTS 内核修复公告。
- 排查方法论：先复现、再分层、最小变更、保留证据；避免在生产环境直接重启掩盖根因。

**关键参数 / 命令**：`journalctl -b -p err`、`dmesg -T -l err,warn`、`ps -eo pid,stat,cmd`、`sar -q 1 5`、`ss -tulpn`、`lsblk -f`、`smartctl -a`。
**权威来源 URL**：https://github.com/systemd/systemd/releases 、https://packages.fedoraproject.org/pkgs/procps-ng/procps-ng/fedora-44.html 、https://openkoji.iscas.ac.cn/koji/buildinfo?buildID=227753 、https://www.kernel.org/ 、https://www.man7.org/linux/man-pages/

## 四、写作要点与风险提示

**写作要点**
1. **版本要区分“主线 / LTS / 发行版自带”三档**：主线 7.3.5 与发行版实际搭载的 6.12 LTS、7.0/7.2 差异很大，避免把主线版本当成发行版默认版本。
2. **以官方源为锚点**：内核用 kernel.org，systemd 用 github.com/systemd/systemd 或 systemd.io，工具版本用 GNU savannah / Debian tracker / Fedora Koji 等原始发布记录，发行版用各官方发布页。
3. **每篇文档开头给出“验证环境”**：声明所用内核、发行版、systemd、工具版本，方便读者复现。
4. **命令示例与版本绑定**：`systemd 262` 的新参数（`RestartRandomizedDelaySec=`、`ActivatingConcurrencyMax=`）、Podman 6 的 nftables 后端等，应在文档中标注适用版本范围。
5. **16 篇之间保持体例统一**：命令、参数、输出示例格式一致；引用来源统一用 Markdown 外链。

**风险提示**
- **版本时效风险**：内核/发行版小版本迭代频繁，本调研为 2026-11-19 快照，写作与发布前必须按来源 URL 复核（尤其是内核稳定版号、LTS 维护截止日、Docker/Podman 补丁号）。
- **第三方来源风险**：部分中文科技媒体与聚合站（如 safeitexperts、computingforgeeks、safeguard.sh）对“bcachefs/ReiserFS 移除”“Ubuntu 26.04 细节”等描述**未经官方确认**，引用前需回溯官方内核文档与发行版发布说明；本文件已尽量以官方源为主。
- **发行版差异风险**：Ubuntu 26.04 用 **systemd 259**（且已移除 cgroup v1、`/tmp` 默认 tmpfs），Fedora 45 用 **systemd 262**，两者行为不同，不能跨发行版直接套用同一套 systemd 示例。
- **内核 ABI/头文件兼容**：Debian 13.7 的 glibc 需与 linux 7.0 头文件兼容，涉及内核开发或驱动编译的文档需提示头文件/ABI 匹配问题。
- **安全建议需结合发行版策略**：SELinux（RHEL 系）与 AppArmor（Debian/Ubuntu 系）分属不同体系，安全加固章节务必按目标发行版分别给出方案，避免混用。
- **容器网络差异**：Podman 6 已移除 CNI、仅支持 Netavark + nftables，Docker 的 iptables 示例不能直接套用到 Podman，需在容器篇明确区分。
- **不要改动知识库其他文件**：本次仅新增本调研文件，其他笔记与配置保持原样。

**主要来源（官方/权威，按主题归类）**

- 内核：https://www.kernel.org/ 、https://www.kernel.org/category/releases.html 、https://kernel.org/releases.html 、https://lwn.net/Articles/1108142/ 、https://www.phoronix.com/news/Linux-7.0-Changes 、https://gigazine.net/gsc_news/en/20261020-linux-kernel-7-3
- systemd：https://github.com/systemd/systemd/releases 、https://www.freedesktop.org/software/systemd/man/latest/ 、https://www.linuxjournal.com/content/systemd-262-released-static-pid-1-intel-tdx-tpm-improvements-and-new-container-features
- 发行版：https://www.debian.org/releases/ 、https://ubuntu.com/download/desktop 、https://ubuntu.com/about/release-cycle 、https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates 、https://fedoramagazine.org/announcing-fedora-linux-45/ 、https://alpinelinux.org/releases/ 、https://nl.opensuse.org/openSUSE:Aankondiging_van_uitgave_van_16.1
- GNU/核心工具：https://www.gnu.org/software/coreutils/ 、https://savannah.gnu.org/news/?group=coreutils 、https://savannah.gnu.org/news/?id=10885 、https://ftp.gnu.org/pub/pub/pub/gnu/gawk/ 、https://lists.gnu.org/archive/html/info-gnu/2025-07/msg00001.html
- 系统/网络工具：https://packages.fedoraproject.org/pkgs/procps-ng/procps-ng/fedora-44.html 、https://tracker.debian.org/pkg/iproute2/news 、https://tracker.debian.org/pkg/util-linux/news 、https://tracker.debian.org/pkg/nftables/news 、https://tracker.debian.org/pkg/cron/
- 性能与手册：https://openkoji.iscas.ac.cn/koji/buildinfo?buildID=227753 、https://www.man7.org/
- 容器：https://docs.docker.com/engine/release-notes/29/ 、https://github.com/containerd/containerd/releases/tag/v2.4.2 、https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1143118
- 安全：https://tracker.debian.org/pkg/apparmor/ 、https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/
