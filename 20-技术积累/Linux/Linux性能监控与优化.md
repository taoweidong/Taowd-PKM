---
title: Linux性能监控与优化
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 性能监控
  - 性能优化
  - 运维
aliases:
  - Linux性能调优
source: 网络资料整理
---

# Linux性能监控与优化

> [!摘要]
> 本篇聚焦「Linux 性能监控与优化」这一高级阶段知识点：讲解性能数据的**采集工具栈**（sysstat 12.7.9、procps-ng 4.0.6、iproute2 7.3.0）、**核心机制**（/proc 与 /sys 数据源、cgroup v2 限额、eBPF 无插桩追踪、systemd 资源控制），并给出一套「先定位 → 再调参 → 后验证」的可落地排查流程与命令示例。阅读前建议先建立 [[Linux-从入门到精通]] 的体系框架，配合 [[Linux常用命令集]] 查阅命令细节。

## 一、最新动态（截至 2026-11）

- **性能监控工具集更新**：**sysstat 12.7.9**（2026 年发布，Fedora 45 于 2026-09 打包），`sar/iostat/mpstat/pidstat/sadf/sa` 为性能数据采集核心。
- **进程/内存概览工具更新**：**procps-ng 4.0.6**（2026-01-30，Fedora 44 打包），提供 `top/free/vmstat/ps/pgrep/kill`。
- **网络统计工具更新**：**iproute2 7.3.0**（2026-10-25，Debian unstable），`ss` 与 `ip -s` 用于网络侧性能统计。
- **内核侧改进**：主线内核 **7.3**（2026-10-18 发布）在 **存储 I/O 与内存管理**方向有性能改进；截至调研时最新稳定版为 **7.3.5**（2026-11-16）。LTS 内核 **6.12 / 6.18 / 6.6** 并行维护，教学与生产建议以 LTS 为例。
- **systemd 262**（2026-09-22 发布，systemd-stable 已到 **262.2**）：新增 **`ActivatingConcurrencyMax=`**，可限制 slice 内同时激活的单元数，为服务并发控制提供新手段；`RestartRandomizedDelaySec=` 可随机化重启间隔，防止重启惊群。
- **cgroup v2 已成基线**：统一层级位于 `/sys/fs/cgroup`；Ubuntu 26.04 LTS 已移除 cgroup v1，资源限额必须基于 cgroup v2。

> [!note] 版本时效
> 内核小版本迭代频繁，本文为 2026-11-19 快照。正式使用前请按来源 URL 复核最新版本号（如内核稳定版号、sysstat/procps-ng 打包版本）。

## 二、基础概念

**性能监控的三个层次**

| 层次 | 关注对象 | 代表工具 |
|---|---|---|
| 系统级 | CPU、内存、磁盘、网络的整体利用率 | `top`、`vmstat`、`free`、`sar` |
| 进程级 | 单进程的 CPU/内存/IO/上下文切换 | `pidstat`、`ps`、`htop` |
| 内核级 | 系统调用、调度、块设备、网络栈行为 | `bpftrace`、`bpftool`、`/proc`、`/sys` |

**关键概念**

- **负载均值（load average）**：`/proc/loadavg` 中 1/5/15 分钟的运行队列长度，是"可运行进程数"的累计指标，**不等于 CPU 利用率**，要结合 CPU 核数看才有意义。
- **USE 方法**：从 **利用率（Utilization）、饱和（Saturation）、错误（Errors）** 三个维度逐层排查 CPU、内存、磁盘、网络，是性能定位的方法论框架。
- **采样与历史数据**：`sar` 按固定间隔落盘采样，可回看历史；`iostat/mpstat/pidstat` 适合现场短时采样。两者配合使用：`sar` 找"曾经的瓶颈"，实时工具找"此刻的瓶颈"。
- **工具来源约定**：性能命令并非内核自带，而由 **sysstat**（性能统计）、**procps-ng**（进程/内存）、**iproute2**（网络）三套工具集提供，安装前需确认发行版已装。

## 三、核心机制

1. **数据来源是虚拟文件系统**：`/proc`（进程与内核统计，如 `/proc/meminfo`、`/proc/vmstat`、`/proc/loadavg`）与 `/sys`（设备、cgroup、内核对象）是大多数性能工具的底层数据源，工具本质是这些文件的**格式化读取器**。
2. **sysstat 采集机制**：`sar` 由后台守护进程按 `/etc/sysconfig/sysstat`（RHEL 系）或 `/etc/default/sysstat`（Debian 系）配置的间隔采集，数据写入 `/var/log/sa/` 下的 `saNN` 报表，`sa` 命令负责汇总，`sadf` 可输出 JSON 供程序消费。
3. **cgroup v2 限额机制**：通过 `/sys/fs/cgroup` 下的控制文件施加资源上限——`cpu.max` 限制 CPU 带宽、`memory.max` 限制内存、`io.max` 限制块设备 IO，是容器与服务级资源隔离的核心。
4. **eBPF 无插桩追踪**：内核提供的动态插桩框架，可在不改动源码、不重启进程的前提下挂载探针观测系统调用、调度、块设备与网络事件，`bpftrace` 是其常用前端。
5. **systemd 资源控制**：systemd 262 的单元指令（`CPUQuota=`、`MemoryMax=`）直接映射到 cgroup；新增的 `ActivatingConcurrencyMax=` 控制同一 slice 内同时激活的单元数量，`RestartRandomizedDelaySec=` 随机化重启延迟。
6. **内核 7.3 的底层改进**：7.3 强调存储 I/O 与内存管理的效率改进，为监控与优化提供了更好的底层基础，但具体收益需结合实测数据验证。

## 四、实践步骤（含代码/命令示例）

**第 0 步：环境准备**

```bash
# Debian/Ubuntu 系安装并开启历史数据采集
sudo apt update && sudo apt install -y sysstat procps iproute2
sudo sed -i 's/^ENABLED=false/ENABLED=true/' /etc/default/sysstat
sudo systemctl enable --now sysstat

# RHEL/Fedora 系
sudo dnf install -y sysstat procps-ng iproute
sudo sed -i 's/^ENABLED=false/ENABLED=true/' /etc/sysconfig/sysstat
sudo systemctl enable --now sysstat
```

**第 1 步：系统级总览**

```bash
uptime                      # 负载均值
free -h                     # 内存/Swap 使用
vmstat 1 5                  # CPU、内存、IO、上下文切换综合视图
ss -s                       # 网络连接与套接字统计
```

**第 2 步：分维度定位瓶颈**

```bash
# CPU：全部核 + 汇总
mpstat -P ALL 1 5
sar -u 1 5

# 内存
sar -r 1 5
vmstat 1 5                  # 关注 si/so（换入换出）非零

# 磁盘：%util、await、r/s
iostat -xz 1 5
sar -d 1 5

# 网络
sar -n DEV 1 5
ip -s link                  # 接口收发错误、丢包
```

**第 3 步：进程级定位**

```bash
pidstat -urd 1 5            # 进程级 CPU/内存/IO 混合统计
pidstat -p <PID> 1 5        # 针对可疑进程
top -o %CPU                 # 按 CPU 排序
```

**第 4 步：历史数据复盘**

```bash
sa                          # 最近一次采集的报表
sadf /var/log/sa/sa15       # 输出结构化 JSON，便于二次处理
sar -f /var/log/sa/sa15 -u -r -d
```

**第 5 步：高级手段（eBPF 无插桩追踪）**

```bash
# 统计被打开最多的文件路径
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { @files[str(args->filename)] = count(); }'

# 按进程统计 10 秒内的 CPU 占用
sudo bpftrace -e -d 10 'profile:hz:99 { @[comm] = count(); }'
```

**第 6 步：资源限额（cgroup v2）**

```bash
sudo mkdir -p /sys/fs/cgroup/mygroup
sudo bash -c 'echo "500000 100000" > /sys/fs/cgroup/mygroup/cpu.max'     # 限 50% CPU
sudo bash -c 'echo 536870912 > /sys/fs/cgroup/mygroup/memory.max'       # 限 512MiB
sudo bash -c 'echo $$ > /sys/fs/cgroup/mygroup/cgroup.procs'            # 将当前 shell 加入
```

**第 7 步：systemd 单元级限制**

```ini
[Unit]
Description=Demo Service

[Service]
ExecStart=/usr/bin/myapp
CPUQuota=50%
MemoryMax=512M
Restart=on-failure
RestartRandomizedDelaySec=5s

[Install]
WantedBy=multi-user.target
```

**第 8 步：验证优化效果**

调参后重复第 2、3 步，对比优化前后 `sar/iostat/pidstat` 的关键指标（如 `%util`、`await`、`r/s`、进程 CPU 占比），确认指标改善且无副作用，形成闭环。

## 五、最佳实践与常见坑

> [!tip] 定位优先，调参在后
> 优化顺序固定为 **先定位 → 再调参 → 后验证**。用 `sar -q/-u/-r/-d` 找系统瓶颈，`pidstat` 定位到具体进程，`iostat -x` 看磁盘，`mpstat` 看 CPU，必要时再上 eBPF，避免凭感觉乱改内核参数。

- **别只盯 load average**：它不区分运行队列中的进程状态，多核机器上高负载可能只是等待 IO，需配合 `mpstat`、`iostat` 判断。
- **`sar` 采样间隔要看清**：默认间隔通常为 10 分钟，短时故障可能根本采集不到，现场排查请用 `iostat/mpstat/pidstat` 实时采样。
- **磁盘关注 `df -h` 也关注 `df -i`**：空间没满但 **inode 耗尽**同样会让写入失败，日志/海量小文件场景尤其常见。
- **改内核参数前先备份**：`sysctl -a > /tmp/sysctl.before.conf`，改动后用 `sysctl --system` 验证，避免改错导致启动异常。
- **生产环境不要直接重启**：重启会掩盖根因，先保留 `journalctl`、`dmesg`、`/var/log` 等证据，再做最小变更。
- **限额要设合理值**：`MemoryMax` 过小会触发 OOM Killer，过大会失去保护意义；`CPUQuota` 需要结合业务峰值设定，并用 `pidstat` 实测确认。
- **cgroup v2 路径不可混用**：Ubuntu 26.04 已移除 cgroup v1，不要照搬 `/sys/fs/cgroup/<group>/memory/` 这类 v1 路径。
- **systemd 参数区分版本**：`RestartRandomizedDelaySec=`、`ActivatingConcurrencyMax=` 为 systemd 262 新特性，旧版本会直接报错，应用前确认发行版 systemd 版本。

## 六、核心要点速查

| 目标 | 命令 |
|---|---|
| 系统总览 | `uptime`、`free -h`、`vmstat 1 5`、`ss -s` |
| CPU 分析 | `mpstat -P ALL 1 5`、`sar -u 1 5` |
| 内存分析 | `sar -r 1 5`、`free -h` |
| 磁盘分析 | `iostat -xz 1`、`sar -d 1 5` |
| 网络分析 | `sar -n DEV 1 5`、`ip -s link` |
| 进程级 | `pidstat -urd 1 5`、`top -o %CPU` |
| 历史数据 | `sa`、`sadf /var/log/sa/saNN` |
| 深度追踪 | `bpftrace -e`、`bpftool` |
| 资源限额 | cgroup v2 控制文件、systemd 单元指令 |

## 七、学习资源

- [Brendan Gregg: USE Method (Linux)](https://www.brendangregg.com/USEmethod/use-linux.html) —— 性能排查方法论清单
- [Brendan Gregg: Linux Performance Tools](https://www.brendangregg.com/linuxperf.html) —— 工具全景图
- [man7.org: Linux 手册页](https://man7.org/linux/man-pages/) —— `sar/iostat/mpstat/pidstat/vmstat` 等权威手册
- [sysstat 项目说明](https://github.com/sysstat/sysstat) —— 性能采集工具集源码与文档
- [systemd 官方手册](https://www.freedesktop.org/software/systemd/man/latest/) —— 单元资源控制指令
- [kernel.org 内核文档](https://www.kernel.org/doc/html/latest/) —— 内核机制与版本特性
- [KernelNewbies](https://kernelnewbies.org/) —— 内核版本特性追踪

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 体系中的位置与学习路线
- [[Linux常用命令集]] —— 监控命令的高频速查
- [[Linux系统管理与运维要点]] —— 运维实战的进阶展开
- [[Linux进程管理]] —— 进程视角的监控与信号处理
- [[Linux系统服务与systemd]] —— systemd 资源控制与服务管理
- [[Linux文件系统与目录结构]] —— 磁盘与文件系统维度的监控基础

## 九、变更记录

- 2026-11-19：首次创建。
