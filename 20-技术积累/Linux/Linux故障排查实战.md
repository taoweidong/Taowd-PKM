---
title: Linux故障排查实战
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 故障排查
  - 运维
  - 排障
aliases:
  - Linux排障实战
  - Linux 故障诊断
source: 网络资料整理
---

# Linux故障排查实战

> [!摘要] 内容与定位
> 本文聚焦 Linux 生产环境的**故障排查方法论与可落地命令**，不罗列所有工具，而是给出"从现象到根因"的分层定位路径：内核/驱动 → 系统资源 → 服务 → 网络 → 存储。覆盖 systemd 日志、性能瓶颈、服务异常、网络连通、磁盘故障、内核与 OOM 等高频场景，配套可直接运行的命令示例。它是 [[Linux-从入门到精通]] 中"高级/精通"阶段"故障演练"的实战展开，与 [[Linux常用命令集]] 的命令速查、[[Linux系统管理与运维要点]] 的运维体系互为补充。

## 一、最新动态（截至 2026-11）

- **内核主线进入 7.x 时代**：7.0.0 于 2026-04-12 发布，7.3 于 2026-10-18 发布；截至调研时最新稳定版为 **7.3.5**（2026-11-16 由 Greg Kroah-Hartman 发布，同批发布 LTS 6.18.64、6.12.118）。
- **LTS 内核三支并行**：**6.18**（首发 2025-11-30，维护至 2028-12）、**6.12**（首发 2024-11-17，维护至 2028-12）、**6.6**（维护至 2027-12）。主流发行版（Debian 13、RHEL 10 系列）多搭载 6.12 LTS，Ubuntu 26.04 LTS 搭载内核 7.0——排查时务必区分"主线版本"与"发行版实际版本"。
- **systemd 262 的 journal 损坏恢复**：systemd 262 于 2026-09-22 发布，systemd-stable 已推进到 v262.2。其新增**损坏 journal 条目恢复**能力，在断电、内核崩溃、强制重启导致活动日志文件被截断时，可尝试救回有效条目——这是非正常关机后排查的关键更新。
- **排查工具版本基线**：进程/内存工具 **procps-ng 4.0.6**、性能监控 **sysstat 12.7.9**、网络配置 **iproute2 7.3.0**、块设备与挂载 **util-linux 2.42.4**。排查命令的行为以这些版本为基准。
- **发行版现状**：Debian 13.7（2026-09-12）、Ubuntu 26.04.1 LTS（2026-08-27）、Fedora 45（2026-11-03，搭载 systemd 262.1）。注意 Ubuntu 26.04 LTS 使用 **systemd 259**，与 Fedora 45 的 262 行为不同，命令示例不可跨发行版直接套用。

> [!note] 时效性
> 以上版本为 2026-11-19 调研快照，内核/发行版迭代极快，写作与实操前请按文末来源 URL 复核，查不到的以官方仓库为准。

## 二、基础概念

**1. 排查的本质是"分层收敛"。** Linux 是分层系统，故障信号从内核层逐层向上传导。排查不是逐个试命令，而是先判断故障落在哪一层，再在该层内定位。标准层次为：

- **内核/驱动层**：`dmesg`、`/sys`、`/proc`，对应硬件、驱动、内核参数异常。
- **系统资源层**：`procps-ng`（`ps/top/free/vmstat`）、`sysstat`（`sar/iostat/mpstat/pidstat`），对应 CPU、内存、负载、磁盘 I/O。
- **服务层**：`systemctl status`、`journalctl -u <unit>`，对应 unit 启动失败、依赖断裂、崩溃重启。
- **网络层**：`iproute2`（`ip/ss/tc`）、`nftables`，对应连通性、路由、端口、防火墙。
- **存储层**：`util-linux`（`lsblk/mount/blkid`）、`smartctl`，对应分区、文件系统、硬件损坏。

**2. 统一的证据入口。** 现代发行版排障有四个"第一入口"：`journalctl`（systemd 统一日志）、`dmesg`（内核环形缓冲）、`/var/log`（传统文本日志）、`/proc` 与 `/sys`（内核虚拟文件系统，实时反映系统状态）。先从这四个入口各取一段信息，通常能快速缩小范围。

**3. 排查方法论四原则。** 先复现（确认现象与触发条件）→ 再分层（按上述五层定位）→ 最小变更（一次只改一个变量并留备份）→ 保留证据（导出日志、截图、命令输出，便于复盘与上报）。

## 三、核心机制

**1. journal 的存储与恢复。** systemd journal 默认写入 `/var/log/journal`（启用持久化后），同时使用内存映射加速。日志文件头/尾部记录了写入边界，非正常关机时活动日志可能被截断。systemd 262 的恢复能力可尝试解析并导出有效条目，因此**非正常关机后第一件事就是查 journal，而不是急着重启服务**。

**2. `/proc` 与 `/sys` 是内核的"只读仪表盘"。** `/proc` 下每个 PID 目录对应一个进程，`/proc/meminfo`、`/proc/vmstat`、`/proc/loadavg`、`/proc/mounts` 是排障数据源；`/sys` 暴露设备与内核对象，cgroup v2 挂在 `/sys/fs/cgroup`。很多"工具看不见"的状态，直接读这两个虚拟文件系统即可确认。

**3. systemd 单元的生命周期。** 一个 service 的运行状态由 unit 文件（`After/Requires/ExecStart/Restart` 等指令）决定。启动失败通常不是"命令错了"，而是依赖未满足、`ExecStart` 路径错误、或重启策略陷入 `Restart=` 死循环（可结合 systemd 262 新增的 `RestartRandomizedDelaySec=`、`ActivatingConcurrencyMax=` 控制重启与并发）。

**4. 资源限额的底层是 cgroup v2。** 内存不足、CPU 争抢、进程被限制，根源都在 cgroup。排查 OOM 需看内核记录与 `/sys/fs/cgroup` 的限额配置，而非只看 `free` 的表象数字。

## 四、实践步骤（含代码/命令示例）

### 步骤 0：建立排查入口，先记录现场

```bash
# 当前系统版本与内核
uname -a
cat /etc/os-release

# 系统启动时间、运行时长（判断是否刚重启过）
uptime
last -x | head -20

# 一次性采集现场证据，保存到工作目录
mkdir -p /tmp/diag && cd /tmp/diag
dmesg -T -l err,warn > dmesg.txt
journalctl -b -p err > journal_err.txt
df -hT > df.txt; free -h > free.txt; ps -eo pid,stat,cmd > ps.txt
```

### 步骤 1：分层定位主流程

```bash
# ① 内核/驱动层
dmesg -T -l err,warn,crit,alert,emerg
ls /sys/class/net/        # 网卡是否被内核识别

# ② 系统资源层
uptime                    # load average 是否超标
free -h                   # 内存/缓存
vmstat 1 5                # 整体上下文切换、IO 等待

# ③ 服务层
systemctl --failed --no-legend        # 所有启动失败的单元
systemctl status <unit>.service       # 单个服务状态与最近日志

# ④ 网络层
ss -tulpn                 # 监听端口与进程归属
ip route                  # 默认路由与网段

# ⑤ 存储层
lsblk -f                 # 块设备、文件系统类型、挂载点
df -hT; df -i             # 空间与 inode
```

### 步骤 2：性能类故障——先定位，再调参

```bash
# 用 sar 看历史与当前：CPU/内存/磁盘
sar -q 1 5        # 队列与负载
sar -u 1 5        # CPU 使用
sar -r 1 5        # 内存
sar -d 1 5        # 磁盘

# 进程级定位
pidstat -urd 1 5      # 每进程的 CPU/内存/IO
mpstat -P ALL 1 3     # 每核 CPU
iostat -xz 1 5        # 每设备磁盘 I/O
```

> [!tip] USE 方法
> 按"利用率（Utilization）→ 饱和度（Saturation）→ 错误（Error）"检查每类资源：CPU 看 `mpstat`，内存看 `pidstat -r`，磁盘看 `iostat -x`，网络看 `ip -s`。先确认是哪类资源饱和，再往下钻取进程，避免盲目调参。

### 步骤 3：服务类故障——查状态与日志

```bash
# 查看失败单元及其依赖
systemctl --failed --no-legend
systemctl status nginx.service

# 过滤该服务的日志
journalctl -u nginx.service --since today
journalctl -u nginx.service -p warning -f     # 实时跟随

# 查看服务启动耗时与依赖树
systemd-analyze blame
systemd-analyze dot nginx.service | dot -Tsvg > deps.svg
```

### 步骤 4：网络类故障——自底向上逐层验证

```bash
# 物理/链路层：接口是否 up、是否有收发
ip -s link show eth0
ip addr show eth0

# IP/路由层
ip route get 8.8.8.8          # 出网路径是否合理
ping -c 4 8.8.8.8

# 端口/防火墙层
ss -tulpn                     # 端口是否监听
nft list ruleset | grep -i drop
firewall-cmd --list-all       # firewalld 场景

# DNS 层
resolvectl status             # systemd-resolved 状态
dig example.com @8.8.8.8
```

### 步骤 5：存储类故障

```bash
lsblk -f                      # 设备与文件系统
df -hT; df -i                 # 空间/inode
findmnt -T /var/log           # 确认挂载点

# 挂载异常时尝试只读重挂，避免数据进一步损坏
mount -o remount,ro /data

# 硬件与坏块
smartctl -a /dev/sda          # 磁盘健康状态
badblocks -n /dev/sdb1        # 只读坏块检测（注意停机执行）
```

### 步骤 6：内核相关与 OOM 排查

```bash
# OOM 记录：内核会直接写进 dmesg/journal
dmesg -T | grep -i -E "oom|out of memory"
journalctl -k -b | grep -i oom

# 查看当前内存与 cgroup 限额
cat /proc/meminfo | head
cat /sys/fs/cgroup/<group>/memory.max
```

## 五、最佳实践与常见坑

> [!danger] 不要用重启掩盖根因
> 重启后服务"看起来好了"往往只是现象消失，根因（磁盘满、句柄泄漏、依赖错误、内核 panic 前的软错误）仍在，下次会以更严重的形式复现。规范做法是先保留现场证据，再按最小变更修复。

> [!warning] 避免在生产环境做不可逆操作
> - 删文件一律用绝对路径，脚本中给变量兜底 `: "${DIR:?未设置}"`，先 `echo` 预演再执行。
> - 改内核参数前记录原值：`sysctl -a > /tmp/before.conf`；改防火墙前备份：`nft list ruleset > backup.nft`。
> - `sed -i` 批量改配置必带备份后缀（如 `sed -i.bak`），改动先在测试实例验证。

**常见坑清单：**

1. **`systemctl restart` 掩盖启动失败**：`restart` 对已失败或依赖异常的服务可能"假成功"。排查时用 `systemctl status` 看退出码与状态，再单独 `start`，必要时 `systemctl fail` 重置失败标记。
2. **`journalctl` 查不到旧日志**：journal 可能未持久化或已轮转。先确认 `/var/log/journal` 是否存在，必要时用 `--directory` 指定日志目录；历史日志回 `/var/log/syslog`、`/var/log/messages`。
3. **`free` 显示内存不足但实际充裕**：Linux 会用空闲内存做页缓存，`free` 中的 `cached` 大部分可回收。判断是否真缺内存要看 `available` 列与 OOM 日志，而非 `free`。
4. **`kill -9` 依赖症**：优先 `kill PID`（SIGTERM，给进程清理机会），仍不退出再 `kill -9`。数据库类服务强杀可能导致恢复成本极高。
5. **发行版差异套用**：Ubuntu 26.04 用 systemd 259、已移除 cgroup v1，Fedora 45 用 systemd 262.1，Podman 6 已移除 CNI、仅用 Netavark + nftables。命令与配置不可跨发行版直接照搬。
6. **忽略内核 ABI/头文件**：涉及驱动编译或内核模块时，注意发行版内核版本与头文件版本匹配（如 Debian 13.7 的内核 ABI），版本不匹配会直接导致编译或加载失败。

## 六、核心要点速查

| 场景 | 首选命令 |
|---|---|
| 系统整体异常 | `journalctl -b -p err`、`dmesg -T -l err,warn`、`uptime` |
| 服务启动失败 | `systemctl --failed`、`systemctl status <unit>`、`journalctl -u <unit>` |
| CPU 瓶颈 | `mpstat -P ALL 1`、`pidstat -urd 1` |
| 内存/OOM | `free -h`、`pidstat -r 1`、`dmesg \| grep -i oom` |
| 磁盘 I/O | `iostat -xz 1`、`sar -d 1 5` |
| 磁盘空间/inode | `df -hT`、`df -i`、`lsblk -f` |
| 网络不通 | `ip route`、`ss -tulpn`、`ping`、`nft list ruleset` |
| DNS 异常 | `resolvectl status`、`dig @8.8.8.8` |
| 硬件/坏块 | `smartctl -a /dev/sdX`、`badblocks -n` |
| 启动耗时 | `systemd-analyze blame` |

## 七、学习资源

1. [systemd 官方手册（systemd.service / journalctl）](https://www.freedesktop.org/software/systemd/man/latest/) —— unit 指令与日志查询权威文档
2. [The Linux Kernel Archives（kernel.org）](https://www.kernel.org/) —— 稳定版/LTS 版本与内核变更
3. [man7.org: Linux man pages](https://www.man7.org/linux/man-pages/) —— `ps/top/iostat/ss` 等命令的权威手册
4. [Brendan Gregg: USE Method (Linux)](https://www.brendangregg.com/USEmethod/use-linux.html) —— 性能排查的分层清单
5. [Linuxize: How to Diagnose OOM Killer Events in Linux](https://linuxize.com/post/how-to-diagnose-oom-killer-events-in-linux/) —— OOM 排查实操
6. [systemd 262 发布说明（GitHub Releases）](https://github.com/systemd/systemd/releases) —— journal 恢复等新特性

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点的体系位置与学习路线
- [[Linux常用命令集]] —— 排障命令的速查补充
- [[Linux系统管理与运维要点]] —— 服务管理、监控、加固的运维体系

## 九、变更记录

- 2026-11-19：首次创建。
