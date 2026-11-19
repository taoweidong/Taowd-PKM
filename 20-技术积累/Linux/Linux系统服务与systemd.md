---
title: Linux系统服务与systemd
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - systemd
  - 服务管理
  - 运维
aliases:
  - systemd服务管理
  - Linux服务管理
source: 网络资料整理
---

# Linux系统服务与systemd

> [!摘要]
> 本文是「Linux 系统服务与 systemd」知识点的完整学习文档：先梳理截至 2026-11 的版本动态（**systemd 262 / systemd-stable 262.2**，262 于 2026-09-22 发布），再讲清 systemd 的架构与单元（unit）机制，给出**单元文件编写、服务启停与依赖、定时器、日志查询、临时服务运行**等可直接复用的操作步骤，最后总结生产环境最佳实践与常见坑。它是 [[Linux-从入门到精通]] 阶段三「服务管理」的核心落地篇，建议与 [[Linux常用命令集]]、[[Linux系统管理与运维要点]] 配合阅读。

## 一、最新动态（截至 2026-11）

- **systemd 已进入 262 代**：**systemd 262** 于 **2026-09-22** 发布，**systemd-stable** 已推进到 **v262.2**，这是本主题最重要的版本基准（来源：[systemd GitHub Releases](https://github.com/systemd/systemd/releases)）。
- **systemd 262 的关键变化**：
  - **基础单元文件内置**：基础 target/service 单元文件被编译进管理器，磁盘单元文件缺失时仍能兜底启动，容器场景更稳健。
  - **可构建单一静态 PID 1**：可静态链接出单一可执行文件作为 init/executor，适配极小的容器镜像。
  - **Intel TDX 机密虚拟机**：新增 `systemd-vmspawn` 支持机密虚拟机。
  - **TPM 密封凭据加固**：凭据绑定存储根密钥（SRK），密钥派生改用 Argon2id。
  - **损坏 journal 条目恢复**：断电、内核崩溃、强制重启等导致日志文件头尾截断时，可尝试救回有效条目。
  - **D-Bus 事务式多单元操作**，并新增 `RestartRandomizedDelaySec=`、`ActivatingConcurrencyMax=` 两条指令。
- **发行版差异（必须区分，示例不可跨发行版直接套用）**：
  - **Ubuntu 26.04 LTS 使用 systemd 259**（26.04.1 于 2026-08-27），已移除 **cgroup v1**、`/tmp` 默认挂载为 **tmpfs**，System V 脚本被弃用（26.04 是最后一个支持 SysV 脚本的版本）。
  - **Fedora 45**（2026-11-03 发布）使用 **systemd 262.1**。
  - **Debian 13**（trixie，13.7 于 2026-09-12）搭载内核 6.12 LTS。
- 版本迭代极快，正式使用前请按上方官方来源 URL 复核最新稳定版号。

## 二、基础概念

**systemd** 是现代 Linux 发行版的 **init 系统与服务管理器**，在内核启动后作为 **PID 1** 运行，是所有用户态进程的"总调度"。它统一接管了传统 SysV init、System V 启动脚本、`init.d`、`rc.local`、`cron` 的部分职责，负责：引导时拉起服务、按依赖关系排序、进程崩溃后自动拉起、资源限额、日志收集、定时任务与设备/挂载管理。

**单元（unit）** 是 systemd 管理一切对象的基本单位，是一份描述"如何管理某资源"的配置文件。常见类型：

| 单元类型 | 作用 | 典型文件 |
|---|---|---|
| `service` | 守护进程（启动/停止/重启） | `nginx.service` |
| `socket` | 网络/Unix 套接字，可做按需拉起 | `ssh.socket` |
| `target` | 一组服务的集合（等价于"运行级别"） | `multi-user.target` |
| `timer` | 定时任务，替代 cron | `backup.timer` |
| `mount` / `automount` | 文件系统挂载 | `local-fs.mount` |
| `path` | 监听路径变化触发服务 | `fs-clean.path` |
| `slice` / `scope` | 资源分组的容器（不直接运行进程） | `system.slice` |

**单元文件查找路径**（同名时优先级由高到低）：`/etc/systemd/system/`（管理员自定义，优先级最高）→ `/run/systemd/system/`（运行时临时单元）→ `/usr/lib/systemd/system/`（软件包自带）。

相比传统的 SysV init 与 `rc.local`，systemd 的优势在于**并行启动**（依赖明确的服务同时拉起，而非串行等待）、**状态可观测**（每个单元都有明确的 active/failed 状态与日志）、**能力整合**（日志、定时、挂载、网络、凭据都由同一套工具管理），因此新部署应优先使用 systemd，遗留脚本逐步迁移。

## 三、核心机制

1. **依赖关系**：`After=`/`Before=` 控制**启动顺序**（不强制存在），`Wants=`/`Requires=` 控制**是否要一起启动**（单元不存在时 `Wants` 忽略、`Requires` 导致启动失败），`Conflicts=` 声明互斥，`Requisite=` 要求依赖必须先就绪。
2. **状态机**：单元处于 `inactive (dead)`、`activating`、`active (running)`、`reloading`、`failed` 等状态。`systemctl` 的操作本质都是状态迁移。
3. **拉起与重启**：`Restart=` 取值 `no` / `always` / `on-failure` / `on-success` / `on-watchdog` 等，配合 systemd 262 新增的 `RestartRandomizedDelaySec=` 可随机化重启间隔、避免多个服务同时崩溃后"惊群"式重启。
4. **并发与资源控制**：通过 **cgroup v2**（挂载于 `/sys/fs/cgroup`）做 CPU、内存、IO 限额；`ActivatingConcurrencyMax=`（262 新增）可限制一个 slice 内同时激活的单元数量，防止批量服务同时启动打满资源。
5. **日志**：所有单元的标准输出/错误默认进入 **systemd journal**（二进制索引日志），存放于 `/var/log/journal/`，可按单元、时间、优先级检索，无需逐文件 `grep`。
6. **按需拉起（socket 激活）**：`socket` 单元先监听端口，收到连接时才触发对应的 `service`，可让监听守护进程在无连接时完全休眠，节省资源、加速启动。
7. **配置继承**：`/etc/systemd/system/xxx.service.d/` 下的 `*.conf` 片段可对软件包自带的单元做增量覆盖，升级软件包时自定义配置不会被覆盖，适合做生产定制。

## 四、实践步骤（含代码/命令示例）

### 4.1 常用 systemctl 操作

```bash
# 查看服务状态、最近日志、是否开机自启
systemctl status nginx.service
systemctl is-active nginx.service      # active / inactive / failed
systemctl is-enabled nginx.service     # enabled / disabled / static

# 启动、重启、停止、重载配置、开机自启（一条命令完成 enable + start）
systemctl start nginx.service
systemctl restart nginx.service
systemctl reload nginx.service         # 优雅重载，不中断连接
systemctl stop nginx.service
systemctl enable --now nginx.service
systemctl disable nginx.service

# 查看所有失败单元并重试
systemctl --failed
systemctl reset-failed nginx.service
```

### 4.2 编写自定义 service 单元

以"每日备份脚本"为例，编写 `/etc/systemd/system/backup.service`：

```yaml
[Unit]
Description=每日数据备份任务
Documentation=file:///opt/backup/README.md
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=backup
Group=backup
WorkingDirectory=/opt/backup
Environment=BACKUP_DIR=/data/backup
ExecStart=/opt/backup/backup.sh --full
# 失败时自动重启（有重试上限），并在重启间加入随机延迟
Restart=on-failure
RestartRandomizedDelaySec=10s
# 资源上限：内存 512M，最多 2 个并发实例
MemoryMax=512M
TasksMax=2

[Install]
WantedBy=multi-user.target
```

启用并验证：

```bash
systemctl daemon-reload                # 修改单元文件后必须执行
systemctl enable --now backup.service
systemctl status backup.service
journalctl -u backup.service -n 50 --no-pager
```

> [!warning] `daemon-reload` 不可省
> 修改任何 `/etc/systemd/system/` 下的单元文件后，systemd 不会自动重读，必须先 `systemctl daemon-reload`，否则新配置不生效且排查时极易误判。

### 4.3 分析启动耗时

```bash
systemd-analyze                       # 查看各单元启动耗时排名
systemd-analyze blame                 # 找出拖慢开机的单元
systemd-analyze dot --verify=no > /tmp/boot.dot   # 导出依赖图
systemd-analyze critical-chain       # 关键启动链
```

### 4.4 临时运行与日志查询

```bash
# 不写单元文件，临时以服务身份运行（适合调试）
systemd-run --unit=myapp --collect --service /opt/app/run.sh

# journalctl 常用过滤
journalctl -b                          # 本次启动以来的全部日志
journalctl -u nginx.service --since today
journalctl -b -p err                   # 本次启动的错误及以上
journalctl -f -u nginx.service         # 实时跟踪
journalctl _SYSTEMD_UNIT=nginx.service # 按字段精确过滤
```

### 4.5 用 timer 替代 cron

`/etc/systemd/system/backup.timer`：

```yaml
[Unit]
Description=每天凌晨 2 点执行备份

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true            # 停机错过后开机补跑一次
RandomizedDelaySec=60s

[Install]
WantedBy=timers.target
```

```bash
systemctl enable --now backup.timer
systemctl list-timers --all             # 核对定时任务
systemd-run --on-calendar 'echo hi'    # 临时验证日历表达式
```

## 五、最佳实践与常见坑

- **迁移遗留脚本**：System V 脚本在 Ubuntu 26.04 已被弃用（26.04 是最后一个支持的版本），应尽早把 `/etc/init.d` 脚本迁移为原生 unit，避免升级后服务不自启。
- **不要在 `ExecStart` 里跑前台常驻脚本时漏掉 `Type=`**：脚本自行 fork 后台化时用默认的 `simple`，脚本前台运行且退出即算完成用 `oneshot`，监听套接字的服务可考虑 `notify`（需脚本调用 `sd_notify`）。
- **区分 `restart` 与 `reload`**：改配置优先 `reload`；无 `reload` 支持时用 `restart`，注意会短暂中断连接。
- **`kill -9` 同理要慎用**：优先 `systemctl stop`（先发 SIGTERM 给清理机会），`systemctl stop` 卡住再考虑强制。
- **失败自愈要设边界**：`Restart=on-failure` 配合 `StartLimitIntervalSec=` / `StartLimitBurst=` 限制重试次数，避免"死循环重启"掩盖配置错误。
- **日志别只盯 `/var/log`**：systemd 服务默认写 journal，`journalctl` 才是第一入口；传统 `rsyslog` 的 `/var/log/syslog` 需要配置才落盘。
- **cgroup 版本差异**：Ubuntu 26.04 已移除 **cgroup v1**，老脚本里基于 v1 路径的写法需改为 `/sys/fs/cgroup` 下的 v2 路径。
- **生产操作纪律**：改单元文件前 `cp /etc/systemd/system/x.service /tmp/x.service.bak`，改完先 `daemon-reload` 再在测试实例验证，最后再推生产。
- **用覆盖片段而非直接改软件包单元**：需要定制第三方服务时，优先在 `/etc/systemd/system/<unit>.service.d/` 建 `override.conf`，避免升级时被覆盖。
- **路径与退出码要明确**：`ExecStart` 用绝对路径，脚本内显式 `exit` 返回非零值表示失败，systemd 才能正确触发 `Restart=` 与 `failed` 状态。

## 六、核心要点速查

| 主题 | 关键命令 / 指令 |
|---|---|
| 生命周期 | `systemctl start/stop/restart/reload/status/enable --now/disable` |
| 依赖指令 | `After=` `Before=` `Wants=` `Requires=` `Conflicts=` `Requisite=` |
| 拉起策略 | `Restart=`、`RestartRandomizedDelaySec=`、`StartLimitBurst=` |
| 资源控制 | `MemoryMax=`、`CPUQuota=`、`TasksMax=`、`ActivatingConcurrencyMax=`（262） |
| 定时任务 | `OnCalendar=`、`Persistent=true`、`RandomizedDelaySec=` |
| 日志 | `journalctl -u/-b/-p/--since/-f` |
| 启动分析 | `systemd-analyze blame/dot/critical-chain` |
| 临时运行 | `systemd-run --unit=xxx --collect` |
| 重读配置 | `systemctl daemon-reload` |

## 七、学习资源

- [systemd 官方手册（freedesktop.org）](https://www.freedesktop.org/software/systemd/man/latest/) —— unit 指令权威定义
- [systemd GitHub Releases](https://github.com/systemd/systemd/releases) —— 版本发布与 262 新特性
- [Linux Journal: systemd 262 released](https://www.linuxjournal.com/content/systemd-262-released-static-pid-1-intel-tdx-tpm-improvements-and-new-container-features) —— 262 静态 PID 1 / TDX / TPM 解读
- [systemd.timer(5) 手册](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) —— 定时任务
- [journalctl(1) 手册](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) —— 日志查询
- [Ubuntu 26.04 特性说明（ComputingForGeeks）](https://computingforgeeks.com/ubuntu-2604-lts-features/) —— 发行版 systemd 版本差异

## 八、关联笔记

- [[Linux-从入门到精通]] —— Linux 学习主线地图，本篇对应其「阶段三：高级」的服务管理模块
- [[Linux-systemd服务管理]] —— systemd 服务管理的另一展开视角
- [[Linux常用命令集]] —— `systemctl`/`journalctl` 等命令速查
- [[Linux系统管理与运维要点]] —— 生产环境运维与排障实战
- [[Linux-性能排查实战]] —— 服务性能问题的定位方法

## 九、变更记录

- 2026-11-19：首次创建。
