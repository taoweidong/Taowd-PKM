---
title: Linux定时任务与计划任务
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 定时任务
  - cron
  - systemd
  - 运维
aliases:
  - Linux定时任务
  - cron与systemd timer
  - 计划任务
source: 网络资料整理
---

# Linux定时任务与计划任务

> [!摘要] 内容与定位
> 本文系统讲解 Linux 上实现「定时、周期性、一次性」自动执行任务的两条主线：**传统 cron**（crond 守护进程 + crontab/cron.d）与 **systemd timer**（现代发行版首选，与 systemd 深度集成，另含 `at`、`anacron` 辅助工具）。内容覆盖基础概念、执行机制、可直接运行的实战步骤、常见坑与排查方法，并附命令速查表。本知识点位于 Linux 学习路线的「进阶 → 高级」阶段，是自动化运维与定时备份、巡检、清理等任务的必备基础。版本基准以 [Linux 调研](../90-待整理与临时笔记/知识库补全100篇/调研/Linux.md) 2026-11-19 快照为准。

## 一、最新动态（截至 2026-11）

- **传统 cron 仍在维护**：Debian 13 系打包 **cron 3.0pl1-213**（2026-11-03），`crontab`、`/etc/crontab`、`/etc/cron.d` 等机制与既往版本保持一致，未发生破坏性变更（[Debian cron 打包跟踪](https://tracker.debian.org/pkg/cron/)）。
- **systemd timer 随 systemd 持续演进**：**systemd 262** 于 **2026-09-22** 发布，systemd-stable 已推进到 **v262.2**。timer 相关能力在 262 中进一步成熟，尤其是 `RandomizedDelaySec=` 的广泛使用（该参数同样可用于服务重启的随机化延迟），为定时任务提供了更精细的调度与防惊群手段（[systemd Releases](https://github.com/systemd/systemd/releases)）。
- **发行版搭载版本存在差异**：**Ubuntu 26.04 LTS 搭载 systemd 259**，**Fedora 45 搭载 systemd 262.1**。两者在 timer 行为与部分指令支持上不完全相同，跨发行版套用同一套 unit 示例前需确认版本（[Ubuntu 26.04 发行说明](https://documentation.ubuntu.com/release-notes/26.04/)）。
- **辅助工具格局**：`anacron` 负责补跑停机期间错过的任务，`at` 负责一次性任务，两者与 cron/systemd 共同构成完整的计划任务生态，在主流发行版中均持续可用。

> [!note] 时效性提示
> 以上版本号均来自调研文件记录的官方/权威来源。内核、发行版与 systemd 迭代极快，正式使用前请按上文来源 URL 复核最新版本号；若查不到，以官方仓库为准。

## 二、基础概念

**定时任务**指让系统在指定时间、按指定周期自动执行命令或脚本的能力。Linux 上主要有四类实现，理解其定位有助于选型：

| 工具 | 类型 | 定位与特点 |
|---|---|---|
| **cron / crond** | 周期性任务 | 传统守护进程，配置简单、历史悠久，是绝大多数定时脚本的首选；依赖系统时间，停机期间的任务不会补跑 |
| **systemd timer** | 周期性/事件触发 | 现代发行版首选，与 service unit 天然绑定，支持精确日历、依赖、持久化与随机延迟，无需额外守护进程 |
| **at** | 一次性任务 | 在指定时刻执行一次，适合「稍后运行」，不适合重复周期 |
| **anacron** | 补跑任务 | 通常配合 cron 使用，在系统重新开机后补执行停机期间错过的任务 |

几个核心术语：

- **crontab**：每个用户（以及系统）的定时任务清单，存放于 `/var/spool/cron/crontabs/`（用户级）或 `/etc/crontab`（系统级）。
- **cron.d**：`/etc/cron.d/` 下的独立任务文件，需 root 权限，适合集中管理多应用的定时任务。
- **timer unit**：systemd 的定时器单元，与同名 service 单元配对，`systemctl enable --now xxx.timer` 即可同时启用调度与服务。
- **时间字段**：cron 的 5 个时间字段（分、时、日、月、周）与 systemd 的日历表达式是两种不同语法，不可混用。

## 三、核心机制

### 3.1 cron 的执行流程

1. **守护进程扫描**：`crond` 按分钟粒度扫描所有任务文件（用户 crontab、`/etc/crontab`、`/etc/cron.d/*`、`/etc/cron.hourly` 等目录）。
2. **匹配时间**：当当前时间与任务的时间字段匹配时，取出命令交给 **sh** 执行。
3. **环境与日志**：cron 运行任务时使用**极简环境**（`PATH` 通常仅 `/usr/bin:/bin`，无用户 shell 的 `~/.bashrc`），执行结果默认通过邮件通知（未配置 MTA 时需改用日志）。
4. **无补跑**：如果任务执行时系统处于关机状态，该次执行被直接跳过，这正是 `anacron` 存在的理由。

### 3.2 cron 时间字段语法

`/etc/crontab` 与 `/etc/cron.d/` 中的每行格式为（用户级 crontab 无用户名字段）：

```text
*  *  *  *  *  用户名  命令
│  │  │  │  └── 星期（0-6，0=周日）
│  │  │  └───── 月份（1-12）
│  │  └──────── 日期（1-31）
└────────────── 小时（0-23）
```

- `*` 表示任意值，用 `,` 列举、用 `-` 表示区间、用 `/n` 表示步长。
- 特殊别名：`@reboot`（启动时）、`@yearly`/`@annually`、`@monthly`、`@weekly`、`@daily`/`@midnight`、`@hourly`。
- 示例：`*/5 * * * * root /usr/local/bin/health-check.sh` 表示每 5 分钟由 root 执行一次健康检查。

### 3.3 systemd timer 机制

systemd 的定时器是 **unit 对**：一个 `xxx.service`（要执行的任务）与一个 `xxx.timer`（调度器）。timer 本身不直接跑命令，而是**在触发时刻拉起同名 service**。

关键指令：

| 指令 | 作用 |
|---|---|
| `OnCalendar=` | 日历表达式，等价于 cron 的时间字段，精度到秒 |
| `OnBootSec=` / `OnUnitActiveSec=` | 开机后多久 / 单元上次激活后多久触发 |
| `Persistent=true` | 开机时补上关机期间错过的触发（类似 anacron） |
| `RandomizedDelaySec=` | 触发时附加随机延迟，避免多节点同时执行形成惊群（systemd 262 推荐用于服务重启） |
| `AccuracySec=` | 触发精度窗口，默认 1min，可放宽以降低唤醒开销 |
| `After=` / `Wants=` | 与其它 unit 的依赖关系，保证执行顺序 |

### 3.4 at 与 anacron 的定位

- **at**：`at now + 30 min`、`at 02:00 tomorrow` 提交一次性任务，用 `atq` 查看、`atrm <id>` 删除。任务存入队列，由 `atd` 守护进程执行。
- **anacron**：以「天/周/月」为周期检查任务是否因停机错过，补跑后再记录。现代发行版中常以 `anacron` + `cron` 或 `systemd timer + Persistent=true` 两种方式实现补跑。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境确认

先确认系统时间、时区与 systemd 版本，避免后续排查方向跑偏：

```bash
# 查看当前时间与时区
date
timedatectl status

# 查看 cron 守护进程是否在运行
systemctl status cron.service        # Debian/Ubuntu
systemctl status crond.service       # RHEL/CentOS/Fedora

# 查看 systemd 版本与已加载的 timer
systemd --version
systemctl list-timers --all
```

### 4.2 用 crontab 配置用户级任务

```bash
# 查看当前用户已有任务
crontab -l

# 编辑（会进入编辑器）
crontab -e
```

写入如下内容（示例：每天 02:30 备份、每小时整点巡检）：

```bash
# 分 时 日 月 周   命令
30  2  * * *   /opt/backup/daily-backup.sh >> /var/log/daily-backup.log 2>&1
0   *  * * *   /opt/ops/health-check.sh >> /var/log/health-check.log 2>&1
```

保存后 `crontab -l` 复核即可，`crond` 会自动感知变更，无需重启。

### 4.3 用 /etc/cron.d 集中管理系统级任务

```bash
sudo tee /etc/cron.d/backup-jobs <<'EOF'
# 格式：分 时 日 月 周 用户名 命令
0  3  * * *  root  /opt/backup/daily-backup.sh >> /var/log/daily-backup.log 2>&1
EOF
sudo chmod 644 /etc/cron.d/backup-jobs
```

> [!warning] cron.d 文件规范
> `/etc/cron.d/` 中文件**必须指定用户名**，且**必须设置严格权限**（建议 `644`、属主 `root:root`）。该目录文件由 `crond` 直接读取，若被非授权用户可写，可能造成任意命令以任意用户身份执行。

### 4.4 用 systemd timer 配置（现代首选）

创建任务脚本：

```bash
sudo mkdir -p /opt/ops
sudo tee /opt/ops/daily-report.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "[$(date '+%F %T')] 生成日报" >> /var/log/daily-report.log
EOF
sudo chmod 755 /opt/ops/daily-report.sh
```

创建 service 与 timer 两个 unit 文件：

```ini
# /etc/systemd/system/daily-report.service
[Unit]
Description=每日生成运维日报
After=network-online.target

[Service]
Type=oneshot
ExecStart=/opt/ops/daily-report.sh
```

```ini
# /etc/systemd/system/daily-report.timer
[Unit]
Description=每日 02:00 触发日报任务

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
RandomizedDelaySec=60

[Install]
WantedBy=timers.target
```

启用并验证：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now daily-report.timer

# 查看 timer 状态与下次触发时间
systemctl list-timers daily-report.timer
systemctl status daily-report.timer

# 手动触发一次（不改变调度）
sudo systemctl start daily-report.service

# 查看执行日志
journalctl -u daily-report.service --since today
```

也可以不落地 unit 文件，用 `systemd-run` 临时运行：

```bash
sudo systemd-run --on-calendar='*-*-* 02:00:00' -- /opt/ops/daily-report.sh
systemctl list-timers
```

### 4.5 用 at 提交一次性任务

```bash
# 30 分钟后执行一次
echo '/opt/ops/clean-temp.sh' | at now + 30 min

# 明天凌晨 3 点执行
at 03:00 tomorrow

# 查看与删除
atq
atrm <任务ID>
```

## 五、最佳实践与常见坑

> [!warning] 时区问题
> cron 按**系统本地时间**判断，systemd timer 的 `OnCalendar=` 也遵循系统时区。改时区后需确认 `/etc/localtime` 与 `timedatectl` 结果一致，否则任务会在错误时刻执行。跨时区服务器建议统一使用 UTC，并在脚本内用 `date -u` 记录。

> [!warning] 环境变量缺失
> cron 使用极简环境，脚本里依赖的 `PATH`、`JAVA_HOME`、`NODE_ENV`、Shell 函数等都不会自动加载，常出现「手动执行正常、cron 执行报 command not found」。**最佳实践：命令一律写绝对路径，脚本开头显式 `export PATH=/usr/local/bin:/usr/bin:/bin` 或 `source` 所需环境文件。**

> [!danger] 任务重叠
> 若任务执行时间超过调度间隔（如每分钟任务跑了 90 秒），会出现任务堆积甚至并发冲突。**在脚本内加锁**是最简单可靠的手段：

```bash
#!/usr/bin/env bash
set -euo pipefail

exec 9>/var/lock/my-job.lock
if ! flock -n 9; then
  echo "上一次任务尚未结束，本次跳过" >&2
  exit 0
fi
# ... 真正任务逻辑
```

其他高频坑：

- **权限差异**：用户 crontab 只能管自己，系统级任务需放 `/etc/crontab`、`/etc/cron.d/` 或指定 `root` 用户；`systemd timer` 需 root 创建并 `enable`。
- **日志去向**：cron 输出默认走邮件（未装 MTA 时会静默丢失），应显式重定向到日志文件；systemd 任务则用 `journalctl -u <unit>` 查看，注意 journal 轮转。
- **Persistent 的误区**：`Persistent=true` 只在**关机期间错过**的触发点补一次，不会因为服务长时间未运行就连续补多轮；且要求 timer 处于 `enabled` 状态。
- **发行版差异**：Ubuntu 26.04 为 systemd 259，Fedora 45 为 systemd 262.1，涉及 `RandomizedDelaySec=` 等指令时先确认本机支持，避免 unit 加载报错。
- **不要在 cron 里跑交互式命令**：需要交互的程序应改造成非交互脚本，或通过 `expect`/参数化处理。

**选型建议**：新项目优先用 **systemd timer**（可依赖、可持久化、日志统一、免装守护进程）；传统脚本迁移、或需支持多用户场景时用 **cron**；一次性提醒用 **at**；停机补跑用 **anacron 或 `Persistent=true`**。

## 六、核心要点速查

| 任务 | 命令 / 配置 |
|---|---|
| 查看/编辑用户任务 | `crontab -l`、`crontab -e` |
| 系统级任务目录 | `/etc/crontab`、`/etc/cron.d/`、`/etc/cron.hourly/` 等 |
| 查看 cron 服务 | `systemctl status cron.service`（或 `crond.service`） |
| 查看/创建 timer | `systemctl list-timers --all`、`systemctl enable --now xxx.timer` |
| 临时触发定时任务 | `systemd-run --on-calendar='*-*-* 02:00:00' -- <cmd>` |
| 查看 timer 执行日志 | `journalctl -u xxx.service --since today` |
| 一次性任务 | `at now + 30 min`、`atq`、`atrm <id>` |
| 时区确认 | `timedatectl status`、`cat /etc/localtime` |
| 常用 calendar 表达式 | `OnCalendar=*-*-* 02:00:00`、`OnCalendar=Mon *-*-* 09:00:00` |

## 七、学习资源

1. [man7.org: crontab(5)](https://www.man7.org/linux/man-pages/man5/crontab.5.html) —— cron 时间字段与文件格式权威手册
2. [systemd 官方文档：systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) —— 定时器单元指令完整说明
3. [Debian cron 打包跟踪](https://tracker.debian.org/pkg/cron/) —— cron 3.0pl1-213 版本来源
4. [systemd Releases（GitHub）](https://github.com/systemd/systemd/releases) —— systemd 262 / 262.2 版本与特性
5. [Ubuntu 26.04 LTS 发行说明](https://documentation.ubuntu.com/release-notes/26.04/) —— 发行版 systemd 版本差异

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习路线中的位置与前置基础

## 九、变更记录

- 2026-11-19：首次创建。
