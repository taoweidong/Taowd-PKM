---
title: Linux-从入门到精通
date: 2026-11-18
updated: 2026-11-18
tags:
  - 技术积累
  - Linux
  - 学习路线
  - 运维
  - 操作系统
aliases:
  - Linux学习路线
  - Linux 技术体系
---

# Linux-从入门到精通

## 一、概述

Linux 是开源类 Unix 操作系统内核，1991 年由 Linus Torvalds 发布，如今是服务器、云基础设施与容器的绝对主流。本笔记是 Linux 学习的**主线地图**：按"入门 → 进阶 → 高级 → 精通"四个阶段组织学习目标、核心知识点、实践项目与推荐资源；高频命令的速查在 [[Linux常用命令集]]，运维实战细节在 [[Linux系统管理与运维要点]]。

> [!info] 学习心法
> Linux 的知识点是"分层"的：命令层（用什么）、机制层（为什么）、内核层（怎么实现的）。每学一个命令都追问它操作的是哪一层抽象（文件描述符、进程、cgroup、namespace），比死记参数有效得多。环境上推荐用虚拟机或 WSL2 练习，配合容器（见 [[Dockerfile编写指南]]）做隔离实验。

## 二、分阶段学习路线

```mermaid
graph LR
    A[阶段一 入门<br/>基础命令/文件系统/编辑器] --> B[阶段二 进阶<br/>权限/用户/软件包/Shell脚本]
    B --> C[阶段三 高级<br/>服务管理/网络/性能调优]
    C --> D[阶段四 精通<br/>内核机制/安全加固/自动化运维]
```

### 阶段一：入门（1-2 个月）

| 维度 | 内容 |
|---|---|
| 学习目标 | 能在终端里独立完成日常文件操作，理解"一切皆文件"，会用 vim 编辑配置，读懂 `ls -l` 输出 |
| 核心知识点 | ① 基础命令：`ls/cd/pwd/cp/mv/rm/mkdir/touch/find/ln`；② 文件系统：FHS 目录结构、inode 概念、挂载与 `/etc/fstab`；③ 文本查看：`cat/less/head/tail/wc`；④ 编辑器：vim 基本模式（normal/insert/命令行）、保存退出、查找替换；⑤ 管道与重定向：`\|`、`>`、`>>`、`2>&1`；⑥ 帮助系统：`man`、`--help`、`apropos` |
| 实践项目建议 | 在虚拟机里手动分区装一遍系统；用纯命令行整理一个目录树；把 `/etc` 下某个服务的配置用 vim 改一遍并验证生效 |
| 推荐资源 | 《The Linux Command Line》（William Shotts，官方免费 PDF）；[Linux Journey](https://linuxjourney.com/)；发行版官方文档（Ubuntu Server Guide / RHEL Docs） |

### 阶段二：进阶（2-3 个月）

| 维度 | 内容 |
|---|---|
| 学习目标 | 独立完成用户与权限管理、软件安装，能写出健壮的 Shell 脚本 |
| 核心知识点 | ① 权限体系：rwx 与数字法、`chmod/chown/chgrp`、umask、ACL（`setfacl/getfacl`）、SUID/SGID；② 用户与组：`useradd/usermod/passwd/sudo`、`/etc/passwd` 与 `/etc/shadow`；③ 软件包管理：`apt`（Debian/Ubuntu）与 `dnf/rpm`（RHEL 系）的安装、搜索、仓库配置、版本锁定；④ 文本三剑客：`grep/sed/awk` 与 `sort/uniq/xargs` 组合；⑤ Shell 脚本：shebang、变量与引号、条件与循环、函数、`set -euo pipefail` 严格模式、`trap` 清理；⑥ 定时任务：cron 与 systemd timer |
| 实践项目建议 | 写一个带参数校验和日志的备份脚本并挂 cron/timer；用 `awk` 做一次 Nginx 日志分析报告；为团队新建账号并按最小权限配置 sudo 规则 |
| 推荐资源 | [ShellCheck 官网](https://www.shellcheck.net/)（脚本静态检查必配）；《Linux Command Line and Shell Scripting Bible》；GNU Coreutils 与 sed/awk 官方手册 |

### 阶段三：高级（3-6 个月）

| 维度 | 内容 |
|---|---|
| 学习目标 | 管理一台生产级服务器：服务编排、网络排障、性能定位、日志治理 |
| 核心知识点 | ① systemd：unit 类型、依赖关系（`After/Wants`）、`systemctl` 生命周期、journalctl 查询、timer 替代 cron；② 网络：`ip/ss` 替代 netstat、路由与 NAT、DNS 排障（`dig`）、防火墙（nftables/ufw/firewalld）、抓包（tcpdump）；③ 性能：load average 含义、`vmstat/iostat/mpstat/pidstat`、USE 方法、`strace/perf`、OOM 排查；④ 磁盘：LVM 创建与扩容、`df -i` inode 耗尽问题、日志轮转 logrotate；⑤ 进程信号与资源限制：`kill` 信号语义、ulimit、cgroup |
| 实践项目建议 | 自建一台 VPS：SSH 加固 + 防火墙 + fail2ban + 自动备份 + 监控告警；模拟一次"磁盘满/内存泄漏/端口冲突"故障演练并写排障报告；用 `perf` 对一个程序做火焰图分析 |
| 推荐资源 | [Brendan Gregg 的 USE 方法清单](https://www.brendangregg.com/USEmethod/use-linux.html)与《Systems Performance》；[systemd 官方文档](https://www.freedesktop.org/wiki/Software/systemd/)；Arch Wiki（工具页质量极高，发行版差异注意甄别） |

### 阶段四：精通（持续）

| 维度 | 内容 |
|---|---|
| 学习目标 | 理解内核机制并用于生产决策，能做安全加固与规模化自动化运维 |
| 核心知识点 | ① 内核机制：进程调度（6.6+ 的 EEVDF）、内存管理与页缓存、VFS、eBPF 可观测与安全；② 容器底层：namespace + cgroup v2 + capabilities，镜像分层与 overlay2；③ 安全：SELinux/AppArmor、auditd、最小权限与补丁策略、[SSH 加固](https://linuxize.com/post/ssh-hardening-best-practices/)；④ 自动化：Ansible 声明式配置管理、与 [[Jenkins流水线配置]] 集成做发布；⑤ 可观测：node_exporter 指标接入 [[Prometheus监控入门]] 体系 |
| 实践项目建议 | 用 eBPF/bpftrace 写一个观测脚本；把一台手工维护的服务器改造成 Ansible Playbook 管理；给内核提一个文档或简单 patch（体会社区流程） |
| 推荐资源 | 《Linux 内核设计与实现》；[KernelNewbies](https://kernelnewbies.org/)（内核版本特性追踪）；LWN.net（内核与社区深度报道） |

## 三、核心要点速查

### 3.1 FHS 目录结构（常用部分）

| 目录 | 内容 | 运维关注点 |
|---|---|---|
| `/etc` | 系统与应用配置 | 改前备份；`/etc/fstab` 写错会无法开机 |
| `/var` | 可变数据 | `/var/log` 日志、`/var/lib` 状态数据，最常被日志撑爆 |
| `/home` | 普通用户家目录 | 重装可保留；配额管理对象 |
| `/usr` | 系统软件资源（bin/lib/share） | 常态只读；`/usr/local` 放手动编译软件 |
| `/opt` | 第三方大型软件 | 自研/闭源软件常用 |
| `/tmp` | 临时文件 | 重启清空；Ubuntu 26.04 起默认 tmpfs |
| `/proc` | 内核与进程虚拟文件 | `/proc/meminfo`、`/proc/vmstat` 排障数据源 |
| `/sys` | 设备与内核对象 | cgroup v2 挂在 `/sys/fs/cgroup` |
| `/dev` | 设备文件 | 块设备如 `/dev/sda`、`/dev/nvme0n1` |
| `/boot` | 内核与引导文件 | 多内核共存，升级失败排查重点 |

### 3.2 权限数字对照

| 数字 | 权限 | 说明 |
|---|---|---|
| 7 | rwx | 读+写+执行 |
| 6 | rw- | 读+写 |
| 5 | r-x | 读+执行 |
| 4 | r-- | 只读 |
| 0 | --- | 无权限 |

常用组合：`755`（脚本/目录，属主全权、他人只读执行）、`644`（普通配置/数据文件）、`700`（私有目录如 `~/.ssh`）、`640`（服务配置文件，配合属组授权）。特殊位：`4xxx` 为 SUID、`2xxx` 为 SGID（如 `/usr/bin/passwd` 的 4755）；新文件默认权限由 umask 决定，常见 umask `022` → 新文件 644、新目录 755。

### 3.3 常用信号表（依据 man7.org kill(1) 手册）

| 编号 | 名称 | 默认动作 | 典型用途 |
|---|---|---|---|
| 1 | SIGHUP | 终止 | 通知守护进程重读配置 |
| 2 | SIGINT | 终止 | Ctrl+C 中断前台进程 |
| 3 | SIGQUIT | 终止+core | Ctrl+\ 退出并转储 |
| 9 | SIGKILL | 强制终止 | ==不可捕获/忽略==，最后手段 |
| 13 | SIGPIPE | 终止 | 写入已关闭的管道 |
| 15 | SIGTERM | 终止 | **kill 默认信号**，可被捕获做清理 |
| 17 | SIGCHLD | 忽略 | 子进程结束通知 |
| 18 | SIGCONT | 继续 | 恢复被暂停的进程 |
| 19 | SIGSTOP | 暂停 | 不可捕获的挂起（对应 Ctrl+Z 的 20 SIGTSTP 可捕获） |

> [!tip] 信号使用顺序
> 先 `kill PID`（TERM，留清理机会）→ 等待数秒 → 仍不退出再 `kill -9`（KILL）。util-linux 的 kill 自内核 6.9 起还支持 `PID:inode` 定位与 `--timeout` 组合信号，避免 PID 复用导致的误杀。

## 四、常见坑与最佳实践

> [!danger] rm -rf 典型事故
> 变量为空或含空格时的递归删除是最经典的事故源：`rm -rf "$DIR/"*` 在 `DIR` 未定义时可能退化为删除根；`rm -rf /tmp /tmp2` 少写一个空格删错目标。守则：删除命令一律用**绝对路径**、先 `echo` 预演、脚本里给变量兜底 `: "${DIR:?未设置}"`。GNU rm 对 `/` 有内置保护，但拼接路径没有。

> [!warning] chmod 777 与 kill -9 依赖症
> `chmod -R 777` 是"用炸药开锁"：人人可写、安全审计不过关、还掩盖了进程属主设计错误。正确路径是查清运行身份（`id`、`ps aux`）后用 `chown`+组或 ACL 精确授权。同理，习惯性 `kill -9` 会跳过进程的信号处理器，数据库类服务强杀可能导致恢复成本极高；kill(1) 手册明确建议优先 TERM。

> [!warning] 生产环境操作纪律
> - 不用 root 日常登录，sudo 按"命令白名单"最小授权（`visudo` 校验后再生效）。
> - 改内核参数前记录原值（`sysctl -a > /tmp/before.conf`），改防火墙前 `nft list ruleset > backup.nft`。
> - `sed -i` 批量改配置必带备份后缀；改动后先在测试实例验证再推生产。

> [!tip] 把命令变成肌肉记忆
> 每天用 `history | awk '{print $2}' | sort | uniq -c | sort -rn | head` 看自己最常用的命令，针对 Top10 精读 man 页；新命令当场记入个人速查（可参考 [[Linux常用命令集]] 的分类结构）。

## 五、2025-2026 最新动态

| 时间点 | 版本/事件 | 要点 |
|---|---|---|
| 2024-11 | Linux 6.12 | **PREEMPT_RT 实时补丁合入主线**；EEVDF 调度器（6.6 引入，接替 CFS）在此版本达到完整支持；新增 sched_ext：可用 BPF 编写可热加载的调度器（来源：[KernelNewbies](https://kernelnewbies.org/Linux_6.12)、[TuxCare](https://tuxcare.com/blog/linux-kernel-6-12)） |
| 2025-01 | Linux 6.13 | 引入 lazy preemption（惰性抢占）模式；用户态 shadow stack（硬件辅助控制流保护）；该版本 2025-04 EOL |
| 2025-08-09 | Debian 13 "trixie" | 内核 6.12 LTS、systemd 257；首次官方支持 riscv64（共 7 架构）（来源：[DebianWiki](https://wiki.debian.org/DebianTrixie)） |
| 2025-05 起 | RHEL 10 / Rocky Linux 10.x | RHEL 10 基于内核 6.12；Rocky 10.1（2025-11）带来后量子密码支持，RHEL 10 重建版支持至 2035-05 |
| 2025-12 | Rust 转正 | Rust 在内核中不再是实验特性（LWN 报道）；首枚 Rust GPU 驱动 Tyr（Arm Mali）2025-11 合入 6.18；当前内核约 473 个 Rust 源文件、约 11.4 万行 |
| 2026-02-08 | 内核改号 | Torvalds 宣布跳过 6.20，下一版直接命名 7.0（纯编号决策，无技术断层，见 [Wikipedia 版本史](https://en.wikipedia.org/wiki/Linux_kernel_version_history)） |
| 2026-04-12 | Linux 7.0 发布 | 主线进入 7.x 时代；截至 2026-11-17 稳定版为 7.3.5，LTS 为 6.18 / 6.12 / 6.6 / 6.1 / 5.15 / 5.10（来源：[kernel.org](https://www.kernel.org/)） |
| 2026-04-23 | Ubuntu 26.04 LTS | 搭载内核 7.0；标准支持至 2031-04，Ubuntu Pro 可再延长 10 年 ESM（来源：[Ubuntu 26.04 发行说明](https://documentation.ubuntu.com/release-notes/26.04/)） |
| 2024-06 / 2024-12 | systemd 256 / 257 | 256 引入 soft-reboot（仅重启用户态）；257 扩大 Varlink IPC 使用并新增 `varlinkctl`（来源：[LWN](https://lwn.net/Articles/1001657/)、[systemd 手册](https://www.freedesktop.org/software/systemd/man/256/systemd-soft-reboot.service.html)） |
| 2025-2026 | systemd 259-260 | 259 起移除 cgroup v1、不再支持 SysV 启动脚本的方向已明确，运维需将遗留 init 脚本迁移为原生 unit（以 systemd 官方发布日志为准） |
| 2025-2026 | 容器时代基线 | cgroup v2 成为默认（GKE 1.33+、Amazon Linux 2023、Kubernetes 1.25+），统一层级位于 `/sys/fs/cgroup`；容器本质即 namespace + cgroup + capabilities，与 [[Kubernetes部署实践]] 的节点运维直接相关 |

> [!note] 时效性提示
> 以上为 2026-11 调研快照。生产选型（尤其内核版本与发行版升级）务必回查各官方发布说明与安全公告。

## 六、参考资料

1. [The Linux Kernel Archives（kernel.org）](https://www.kernel.org/) —— 稳定版/LTS 版本列表与源码
2. [KernelNewbies: Linux 6.12](https://kernelnewbies.org/Linux_6.12) 与 [TuxCare: Linux Kernel 6.12](https://tuxcare.com/blog/linux-kernel-6-12) —— PREEMPT_RT、EEVDF、sched_ext 特性
3. [Wikipedia: Linux kernel version history](https://en.wikipedia.org/wiki/Linux_kernel_version_history) —— 7.0 改号决策（2026-02-08）与发布时间线
4. [man7.org: kill(1)](https://man7.org/linux/man-pages/man1/kill.1.html) —— 信号语义权威手册
5. [systemd 官方文档：systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) 与 [systemd-soft-reboot.service](https://www.freedesktop.org/software/systemd/man/256/systemd-soft-reboot.service.html)
6. [LWN: systemd 257 released](https://lwn.net/Articles/1001657/) —— Varlink 与 257 版变化
7. [Brendan Gregg: USE Method (Linux)](https://www.brendangregg.com/USEmethod/use-linux.html) —— 性能排查方法清单
8. [ShellCheck Wiki](https://www.shellcheck.net/wiki/) 与 [6 Techniques to Create Great Shell Scripts](https://nochlin.com/blog/6-techniques-hacker-news-uses-to-create-great-shell-scripts)（2025-03）—— 脚本工程规范
9. [Linuxize: How to Diagnose OOM Killer Events](https://linuxize.com/post/how-to-diagnose-oom-killer-events-in-linux/) 与 [Linuxize: SSH Hardening Best Practices](https://linuxize.com/post/ssh-hardening-best-practices/)
10. [DebianWiki: DebianTrixie](https://wiki.debian.org/DebianTrixie)、[Ubuntu 26.04 发行说明](https://documentation.ubuntu.com/release-notes/26.04/)、[ComputingForGeeks: Debian 13 vs Ubuntu 24.04 vs Rocky Linux 10](https://computingforgeeks.com/debian-ubuntu-rocky-comparison) —— 发行版现状
11. [SegmentFault: Linux 从入门到精通系统化学习路线](https://segmentfault.com/a/1190000047073205)（2025）—— 中文学习路线参照

## 七、关联笔记

- [[Linux常用命令集]] —— 各阶段高频命令速查
- [[Linux系统管理与运维要点]] —— 高级/精通阶段实战展开
- [[网络基础概念]] —— 阶段三网络知识的前置
- [[Web安全最佳实践]] —— 安全加固的上层视角
- [[Dockerfile编写指南]] / [[Kubernetes部署实践]] —— 容器时代应用
- [[Prometheus监控入门]] —— 可观测体系落地

## 八、变更记录

- 2026-11-18 首次创建
- [[HTTP协议详解]] —— `curl` 调试 HTTP 服务的原理支撑
