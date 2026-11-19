---
title: Linux日志管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 日志
  - systemd
  - 运维
aliases:
  - Linux日志
  - Linux 日志管理
source: 网络资料整理
---

# Linux日志管理

> [!摘要]
> 本篇是 [[Linux-从入门到精通]] 中「阶段三：高级」的落地专题，聚焦 Linux 日志的**采集、存储、查询、轮转与排障**。内容以现代发行版默认的 **systemd journal** 为主线，兼顾传统 **rsyslog/syslog-ng** 与 **logrotate** 轮转，覆盖从「一条日志从哪来、落在哪、怎么查」到「生产环境如何配容量、留证据、避坑」的完整闭环。文中版本号与新特性来自 2026-11 调研快照，使用前请按官方文档复核。

## 一、最新动态（截至 2026-11）

- **systemd 进入 262 代**：systemd 262 于 **2026-09-22** 发布，systemd-stable 已推进到 **v262.2**。其中与日志直接相关的是**损坏 journal 的条目恢复**能力：在非正常关机（断电、内核崩溃、强制重启）导致活动日志文件头/尾部被截断时，可尝试救回仍有效的条目，这是排障场景的重要更新点（来源：[systemd releases](https://github.com/systemd/systemd/releases)）。
- **发行版自带版本有差异**：Ubuntu 26.04 LTS 使用 **systemd 259**，Fedora 45 使用 **systemd 262.1**，Debian 13（trixie）搭载 6.12 LTS 内核。同一命令在不同发行版上的默认行为并不相同，配置前先用 `systemctl --version` 确认。
- **内核进入 7.x 时代**：主线稳定版已到 **7.3.5**（2026-11-16 发布），LTS 分支保持 **6.18 / 6.12 / 6.6** 并行。内核环形缓冲区（`dmesg`）仍是排查硬件与驱动问题的首要入口。
- **容器日志更强调「不跟随符号链接」**：containerd **2.4.2**（2026-10-13）起 CRI 日志不再跟随符号链接，容器运行时日志的采集与轮转行为随之变化，容器场景需单独配置日志驱动与上限（来源：[containerd releases](https://github.com/containerd/containerd/releases/tag/v2.4.2)）。

## 二、基础概念

日志是系统运行的「黑匣子」，核心用途有四类：**故障定位、性能分析、安全审计、合规留痕**。Linux 上的日志可以从三个维度理解。

**1. 按来源分三层**

| 层 | 典型内容 | 存储位置 |
|---|---|---|
| 内核/系统 | 驱动、硬件、OOM、调度异常 | `dmesg` 环形缓冲区、`/var/log/kern.log`、`journalctl -k` |
| 服务/守护进程 | systemd 单元、SSH、Nginx、数据库 | journal、`/var/log/syslog`、`/var/log/messages` |
| 应用 | 业务自身的运行日志 | 由应用决定，常见 `/var/log/<app>/` |

**2. 按存储形态分两类**

- **文本日志**：传统 syslog 派生体系（rsyslog、syslog-ng）直接写入文本文件，可直接 `grep/tail`，人可读性好。
- **带索引的二进制日志**：systemd journal 将结构化字段（时间、优先级、PID、单元名、字段）序列化并建立索引，查询能力远强于文本，代价是不可直接编辑。

**3. 关键术语**

- **优先级（PRI）**：syslog 用 0（emerg）到 7（debug）共 8 级，数字越小越严重；`journalctl -p` 就是按此过滤。
- **采集器（logger/daemon）**：负责接收并落盘日志，如 `systemd-journald`、`rsyslogd`。
- **轮转（rotation）**：日志按时间或大小切分、压缩、删除旧文件，防止磁盘被撑爆，由 **logrotate** 统一完成。
- **集中式日志**：多机场景把日志转发到统一服务（如 Loki、ELK），本地只做短期留存。

## 三、核心机制

**1. journald 采集与存储**：PID 1（systemd）启动 `systemd-journald`，各进程通过 `write()` 或 `journal_log()` 写入 `/run/log/journal`（易失）与 `/var/log/journal`（持久化）。每个 boot 一个日志文件，journald 按 `SystemMaxUse`、`MaxFileSec`、`MaxFileSize` 等参数自动轮转并压缩旧日志。

**2. rsyslog 转发与过滤**：rsyslog 作为传统 syslog 守护进程，按规则文件（`/etc/rsyslog.conf`、`/etc/rsyslog.d/*.conf`）匹配字段（`programname`、`facility`、优先级）后写入不同文件或转发给远端。常见规则语言基于 `if ... then` 的过滤表达式。

**3. logrotate 轮转**：由 cron/systemd timer 周期触发，依据配置文件判断是否达到轮转条件，执行切分、压缩、删除，并可运行 `postrotate` 脚本通知服务重新打开日志文件——**这一步最容易被忽略，导致日志文件被删后服务仍写旧句柄、日志"消失"**。

**4. 内核日志双通道**：内核日志同时存在于内存环形缓冲区（`/dev/kmsg`，`dmesg` 读取）与 journal（`journalctl -k`）。二者并不等价，排查驱动问题优先看 `dmesg -T`。

**5. 应用日志的落地方式**：systemd 托管的服务可通过单元文件的 `StandardOutput=journal`/`StandardError=journal` 把标准输出收进 journal；自行写文件的应用则需自行做轮转，或交给 rsyslog 转发。

## 四、实践步骤（含代码/命令示例）

**1. 查看与过滤 journal**

```bash
# 本次启动的所有日志，只看错误及以上
journalctl -b -p err

# 指定单元，只看今天
journalctl -u ssh.service --since today

# 按时间区间与字段精确过滤
journalctl --since "2026-11-19 08:00" --until "2026-11-19 10:00"
journalctl _SYSTEMD_UNIT=nginx.service _PID=1234

# 实时跟踪某个服务的日志
journalctl -f -u nginx.service

# 内核日志、只取最近 100 条、不使用分页器
journalctl -k -n 100 --no-pager

# 查看所有启动记录与日志文件状态
journalctl --list-boots
journalctl --header
journalctl --verify
```

**2. 传统文本日志与内核日志**

```bash
dmesg -T -l err,warn          # 内核日志，人类可读时间，仅错误与警告
tail -f /var/log/syslog        # 跟踪系统日志（Debian/Ubuntu）
tail -f /var/log/messages      # 跟踪系统日志（RHEL/CentOS 系）
grep -n "ERROR" /var/log/nginx/error.log
```

**3. 开启 journal 持久化并限制容量**

```ini
# /etc/systemd/journald.conf
[Journal]
Storage=persistent          # 持久化到 /var/log/journal，重启不丢
SystemMaxUse=2G            # 日志总用量上限，超出自动轮转
MaxFileSize=200M           # 单个日志文件上限
MaxRetentionSec=30d        # 日志最长保留时间
```

```bash
systemctl restart systemd-journald
mkdir -p /var/log/journal && chmod 2755 /var/log/journal
```

**4. 用 rsyslog 按程序分流日志**

```rsyslog
# /etc/rsyslog.d/10-myapp.conf
if $programname == 'myapp' then {
    action(type="omfile" file="/var/log/myapp/app.log"
           create="yes" rotatePerSize="100" rotateTimes="5")
    stop
}
```

```bash
systemctl restart rsyslog
```

**5. 配置 logrotate 轮转**

```yaml
# /etc/logrotate.d/myapp
/var/log/myapp/app.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 app adm
    postrotate
        /usr/bin/systemctl reload rsyslog >/dev/null 2>&1 || true
    endscript
}
```

```bash
logrotate -d /etc/logrotate.conf   # 演练模式：只打印将执行的动作，不真正执行
logrotate -f /etc/logrotate.d/myapp  # 强制立即轮转一次，用于验证配置
```

**6. 容器日志处理**

```json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "100m", "max-file": "5" }
}
```

```bash
docker logs -f --tail 200 <container>   # 查看容器日志
```

## 五、最佳实践与常见坑

> [!tip] 生产建议
> - **持久化 + 容量上限**双管齐下：`Storage=persistent` 保证重启可查，`SystemMaxUse` 防止磁盘被日志写满拖垮系统。
> - **日志要可追溯**：关键服务统一打到 journal 或集中式平台，避免散落在各自定义的路径里。
> - **改动先演练**：`logrotate -d`、`journalctl --verify` 都是只读检查，正式变更前先跑一遍。

> [!warning] 常见坑
> - **rsyslog 与 journald 重复采集**：两者同时运行时，同一条消息可能同时落进文本文件与 journal，排查时注意不要重复计数。
> - **`postrotate` 缺失导致日志"消失"**：服务仍持有旧文件句柄，轮转后新日志写进新文件、旧文件被删，排查时找不到日志——务必在 `postrotate` 中通知服务重开文件。
> - **权限不足读不到 journal**：`/var/log/journal` 应为 `2755 root:systemd-journal`，否则普通用户 `journalctl` 可能无输出。
> - **时间不同步**：日志时间取决于系统时钟，未配置 `chrony`/`timedatectl` 的主机日志时间会漂移，跨机对比无从下手。
> - **容器里 journald 常常不可用**：精简容器镜像通常没有 journal，`journalctl` 会返回空；容器日志应依赖运行时驱动（json-file/journald）或 stdout 采集。
> - **不要把敏感信息写进日志**：应用日志需做脱敏，避免密码、令牌等落入 `/var/log` 或集中式平台。

## 六、核心要点速查

| 任务 | 命令 |
|---|---|
| 看本次启动错误日志 | `journalctl -b -p err` |
| 跟踪某服务日志 | `journalctl -f -u <unit>` |
| 按时间过滤 | `journalctl --since today --until tomorrow` |
| 按字段精确过滤 | `journalctl _SYSTEMD_UNIT=<unit> _PID=<pid>` |
| 内核日志 | `dmesg -T -l err,warn` / `journalctl -k` |
| 持久化与容量 | 改 `/etc/systemd/journald.conf` 后重启 journald |
| 配置轮转 | 编辑 `/etc/logrotate.d/<name>`，用 `logrotate -d` 演练 |
| 验证日志完整性 | `journalctl --verify` |
| 容器日志 | `docker logs -f --tail 200 <container>` |

## 七、学习资源

1. [journalctl(1) 官方手册（systemd）](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) —— 过滤、字段、boot 相关选项权威说明
2. [systemd/journald.conf(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.conf.html) —— 持久化与轮转参数
3. [rsyslogd(8) 手册（man7.org）](https://www.man7.org/linux/man-pages/man8/rsyslogd.8.html) —— 传统 syslog 配置
4. [logrotate 配置说明（Linux Journey）](https://linuxjourney.com/note/log-rotation) —— 轮转语法与实战
5. [systemd 官方发布记录](https://github.com/systemd/systemd/releases) —— 262 版 journal 恢复等新特性
6. [kernel.org 内核文档](https://www.kernel.org/) 与 [man7.org](https://www.man7.org/) —— 内核与命令的一手手册

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习体系中的位置与阶段划分
- [[Linux系统管理与运维要点]] —— 日志排障与运维实战的上层展开

## 九、变更记录

- 2026-11-19：首次创建。
