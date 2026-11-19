---
title: Linux进程管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 进程管理
  - systemd
  - 运维
aliases:
  - Linux 进程管理
  - Linux 进程控制
source: 网络资料整理
---

# Linux进程管理

> [!摘要]
> 本笔记系统讲解 Linux 中**进程的查看、控制、优先级调节与资源限制**，并覆盖 systemd 作为 PID 1 对服务进程的生命周期管理。内容从进程概念与状态出发，深入到信号机制、调度器、cgroup v2 等核心原理，再落到可直接运行的命令与单元文件配置，最后给出生产环境的避坑清单。适合作为 [[Linux-从入门到精通]] 阶段三「服务管理与性能调优」的专项展开。文中版本号为 2026-11 调研快照，实际使用请以官方仓库为准。

## 一、最新动态（截至 2026-11）

- **procps-ng 4.0.6**（2026-01-30，Fedora 44 打包）：`ps/top/free/vmstat/pgrep/kill` 等进程与内存工具集的当前基准版本，本文命令示例均以此为准。
- **systemd 262**（2026-09-22 发布，`systemd-stable` 已推进到 **262.2**）：新增两个与服务进程管理直接相关的参数——`ActivatingConcurrencyMax=`（限制 slice 内同时激活的单元数，防并发爆炸）与 `RestartRandomizedDelaySec=`（随机化重启间隔，避免惊群式重启）。
- **内核进入 7.x 时代**：7.0.0 于 2026-04-12 发布，7.3 于 2026-10-18 发布，最新稳定版 **7.3.5**（2026-11-16，与 LTS 6.18.64、6.12.118 同批发布）。内核 7.3 在 CPU 与内存管理方向有效率改进，可作为调度与内存章节的背景。
- **LTS 内核三支并行**：6.18（维护至 2028-12）、6.12（维护至 2028-12）、6.6（维护至 2027-12），主流发行版多采用 6.12 LTS。
- **发行版 systemd 版本不一**：Ubuntu 26.04 LTS 仍使用 **systemd 259** 并已移除 cgroup v1，Fedora 45 使用 **systemd 262.1**，跨发行版套用 systemd 示例时需注意差异。

## 二、基础概念

- **进程（Process）**：程序在数据集合上的一次执行过程，是操作系统进行**资源分配和调度的基本单位**。Linux 中每个进程都有唯一的 **PID**（进程号，通常从 1 开始递增）和 **PPID**（父进程号）。
- **PID 1 与 init**：内核启动后拉起的第一个进程即 PID 1，负责初始化系统与回收僵尸进程。现代发行版统一由 **systemd** 担任 PID 1；容器内则常以 `tini`、`dumb-init` 或 systemd 自身承担该职责。
- **线程（Thread）**：进程内的执行单元，共享进程地址空间。线程的创建与调度开销远小于进程，是多线程服务提升并发的基础。
- **进程状态**：`ps` 的 `STAT` 列常用取值：

  | 状态 | 含义 | 说明 |
  |---|---|---|
  | R | 运行/可运行 | 在运行队列或就绪 |
  | S | 可中断睡眠 | 等待事件，可被信号唤醒，最常见 |
  | D | 不可中断睡眠 | 通常在等 I/O，信号无法打断，需等 I/O 完成 |
  | T/t | 停止 | 被作业控制或调试器暂停 |
  | Z | 僵尸 | 已退出但父进程尚未回收，仍占用 PID 表项 |
  | I | 空闲内核线程 | 内核态空闲线程，`ps` 中常见于内核线程 |

- **僵尸进程与孤儿进程**：子进程退出后若父进程未调用 `wait`/`waitpid` 回收，子进程变为**僵尸进程**，长期堆积会耗尽 PID；父进程先于子进程退出时，子进程被 init（PID 1）收养，成为**孤儿进程**，通常会被重新挂到 PID 1 下并得到回收。

## 三、核心机制

1. **进程创建**：经典流程为 `fork()` 复制父进程（写时复制）→ `execve()` 装载新程序映像，新进程获得全新执行流。Shell 中每条命令基本都走这一套。
2. **信号（Signal）机制**：进程间异步通知的轻量方式，内核在目标进程的待处理信号集中置位，进程在合适的时机处理。`SIGTERM`（15）可被捕获用于优雅退出，`SIGKILL`（9）不可捕获、不可忽略，是最终手段。
3. **调度器**：进程在 CPU 上的时间分配由调度器负责。早期 CFS（完全公平调度）在 6.6 起被 **EEVDF**（最早截止时间优先）接替；6.12 起 **PREEMPT_RT** 实时补丁合入主线。`sched_ext` 还允许用 BPF 编写可热加载的调度器，为自定义调度策略提供入口。
4. **systemd 服务管理**：systemd 以 **unit（单元）** 描述进程/服务，通过依赖关系（`After=`、`Requires=`、`Wants=`）编排启动顺序，用 `Restart=` 定义异常退出后的恢复策略，并通过 **cgroup** 施加资源限制，是现代 Linux 管理进程的事实标准。
5. **cgroup v2 资源限制**：统一层级位于 `/sys/fs/cgroup`，可对 CPU、内存、IO、PID 数等做分组限制。Ubuntu 26.04 已移除 cgroup v1，新项目应以 v2 为准。

## 四、实践步骤（含代码/命令示例）

### 4.1 查看进程

```bash
# 查看全部进程：PID、父 PID、状态、优先级、CPU/内存占比、运行时长、命令
ps -eo pid,ppid,stat,ni,%cpu,%mem,etime,cmd

# 只看当前用户，按内存降序取前 20
ps -u "$USER" -o pid,ppid,%mem,%cpu,cmd --sort=-%mem | head -20

# 交互式动态查看，-o 指定排序字段
top -o %CPU
top -o %MEM
top -p 1234,5678      # 仅监控指定 PID
htop                 # 功能更强的交互式版本（通常需单独安装）
```

```bash
# 按名称/用户查找 PID
pgrep -f "nginx: master"
pgrep -u www-data
pidof nginx
```

### 4.2 用信号控制进程

```bash
kill -l                      # 列出全部信号编号与名称
kill 1234                  # 发送 SIGTERM(15)，优先使用
kill -USR1 1234           # 发送自定义信号，如让守护进程重载配置
kill -9 1234               # SIGKILL，强制终止，最后手段

pkill -f "java -jar app.jar"
killall nginx
```

> [!tip] 终止顺序
> 先 `kill PID`（TERM，给进程清理与落盘的机会）→ 等待数秒 → 仍不退出再 `kill -9`。util-linux 的 `kill` 还支持 `PID:inode` 形式精确定位同名进程，并可用 `--timeout` 组合信号，降低 PID 复用导致的误杀风险。

### 4.3 调整优先级与资源限制

```bash
# nice 值范围 -20（最高）~ 19（最低），默认 0
nice -n -10 ./heavy-job.sh      # 以高优先级启动
nice -n 10 ./low-prio.sh        # 以低优先级启动
renice -n 5 -p 1234             # 调整已运行进程的优先级

ulimit -a                          # 查看当前资源限制
ulimit -n 65535                   # 临时提高打开文件数上限
ulimit -c unlimited               # 打开 core dump
# 永久生效需写入 /etc/security/limits.conf
```

```bash
# 用 cgroup v2 限制内存上限（以 systemd 临时作用域为例）
systemd-run --scope -p MemoryMax=1G -p CPUQuota=80% ./myapp
cat /sys/fs/cgroup/<组路径>/cgroup.procs   # 查看组内进程
```

### 4.4 systemd 服务管理

```bash
systemctl status nginx.service               # 查看状态、最近日志与资源
systemctl start nginx.service
systemctl restart nginx.service
systemctl reload nginx.service               # 仅重载配置，不中断进程
systemctl enable --now nginx.service         # 开机自启并立即启动
systemctl list-units --type=service --state=running
systemd-analyze dot nginx.service | dot -Tsvg > graph.svg   # 输出依赖图
```

```ini
# /etc/systemd/system/myapp.service —— 带资源限制与新版重启参数
[Unit]
Description=My Application
After=network.target

[Service]
ExecStart=/usr/local/bin/myapp
Restart=on-failure
RestartRandomizedDelaySec=5s   # systemd 262：随机化重启间隔，防惊群
CPUQuota=80%
MemoryMax=1G

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload && systemctl enable --now myapp.service
```

### 4.5 查看服务日志与进程级性能

```bash
journalctl -u nginx.service --since "1 hour ago"
journalctl -u nginx.service -f            # 实时跟踪
journalctl -b -p err                     # 本次启动的错误级日志

pidstat -urd 1 5       # 进程级 CPU/内存/IO 采样
mpstat -P ALL 1 5      # 每个 CPU 核的利用率
```

## 五、最佳实践与常见坑

- **先 TERM 后 KILL**：数据库、消息队列等服务强杀会跳过清理逻辑，可能损坏数据或延长恢复时间。仅在 TERM 超时、进程无响应时再用 KILL。
- **警惕僵尸进程堆积**：`ps -eo pid,ppid,stat,cmd | awk '$3 ~ /Z/'` 可快速定位；根因通常在父进程代码未处理 `SIGCHLD`，优先修父进程而非反复重启。
- **不要随意 `kill -9` PID 1 / systemd**：会导致系统失去 init，进程无人回收、服务无法重启，严重时需要救援。
- **systemd 依赖要写全**：`After=` 只控制顺序，服务真正依赖另一个服务时应配合 `Requires=`/`Wants=`，否则会出现启动竞态。修改单元文件后务必 `systemctl daemon-reload` 再重启。
- **区分 cgroup v1 / v2**：Ubuntu 26.04 已移除 cgroup v1，老教程中的 v1 路径与指令在较新系统上会失效，按 `/sys/fs/cgroup` 实际挂载确认。
- **PID 复用与精确终止**：`kill` 仅凭 PID 可能误杀已被复用的进程，可用 `ps -o pid,inode` 或 `kill PID:inode` 交叉验证。
- **生产操作纪律**：批量终止前先 `ps` 核对目标，关键操作保留现场与日志（`journalctl`、`dmesg -T`），避免直接重启掩盖根因。

## 六、核心要点速查

| 需求 | 命令 |
|---|---|
| 全量进程视图 | `ps -eo pid,ppid,stat,%cpu,%mem,cmd` |
| 交互监控 | `top -o %CPU` / `htop` |
| 按名查 PID | `pgrep -f <pattern>` / `pidof` |
| 优雅终止 | `kill PID`（SIGTERM 15） |
| 强制终止 | `kill -9 PID`（SIGKILL 9） |
| 调整优先级 | `nice -n N` / `renice -n N -p PID` |
| 查看限制 | `ulimit -a` |
| 服务状态与控制 | `systemctl status/restart/enable --now <unit>` |
| 服务日志 | `journalctl -u <unit> --since ...` |
| 进程级性能 | `pidstat -urd 1` |

**常用信号速查**：`1 SIGHUP` 重读配置、`2 SIGINT` 中断、`9 SIGKILL` 强制终止、`15 SIGTERM` 默认终止、`17 SIGCHLD` 子进程结束、`18 SIGCONT` 继续、`19 SIGSTOP` 暂停。

## 七、学习资源

1. [man7.org: ps(1)](https://man7.org/linux/man-pages/man1/ps.1.html)、[kill(1)](https://man7.org/linux/man-pages/man1/kill.1.html) —— 进程查看与信号语义的权威手册。
2. [systemd 官方文档](https://www.freedesktop.org/software/systemd/man/latest/) —— unit 文件指令与服务管理细节。
3. [procps-ng（Fedora 打包页）](https://packages.fedoraproject.org/pkgs/procps-ng/procps-ng/fedora-44.html) —— `ps/top/kill` 等工具集的版本基准。
4. [kernel.org 内核文档](https://www.kernel.org/doc/html/latest/) —— 调度、cgroup、进程子系统的一手资料。
5. [Brendan Gregg: USE Method](https://www.brendangregg.com/USEmethod/use-linux.html) —— 性能排查方法论。
6. [KernelNewbies](https://kernelnewbies.org/) —— 内核版本特性追踪（EEVDF、sched_ext、PREEMPT_RT）。

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习体系中的位置与整体路线
- [[Linux常用命令集]] —— 进程相关高频命令的速查
- [[Linux系统管理与运维要点]] —— 服务管理、性能与运维的实战展开

## 九、变更记录

- 2026-11-19：首次创建。
