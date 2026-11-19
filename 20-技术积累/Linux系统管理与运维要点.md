---
title: Linux系统管理与运维要点
date: 2026-11-18
tags:
  - 技术积累
  - Linux
  - 运维
  - SRE
  - 系统管理
---

# Linux系统管理与运维要点

## 一、概述

本笔记聚焦**生产环境的系统管理与运维实战**：systemd 服务与定时任务、日志治理、磁盘与 LVM、性能排查方法论（USE 法则）、运维 Shell 脚本模板、安全加固清单，以及容器时代与自动化工具（Ansible）的衔接。学习路线见 [[Linux-从入门到精通]]，命令速查见 [[Linux常用命令集]]。

> [!info] 运维第一性原则
> 一切变更要"可回滚、可追溯、可复现"：改配置前备份，改内核参数前记录原值，一切手工操作最终沉淀为脚本或 Ansible 代码，避免"只在某台机器上成立"的隐式知识。

## 二、systemd 深入

### 2.1 服务单元编写示例

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/java -Xms512m -Xmx1024m -jar /opt/myapp/app.jar
Restart=on-failure
RestartSec=5
MemoryMax=1500M                 # cgroup v2 内存上限，超限触发 OOM 杀进程
LimitNOFILE=65536               # 文件句柄上限

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload          # 改过 unit 文件必须先 reload
sudo systemctl enable --now myapp
systemctl show myapp -p MemoryMax,Restart   # 查看实际生效属性
systemd-analyze blame                 # 启动耗时排名，优化开机速度
```

要点：`Type=simple`（前台常驻，最常用）、`Type=oneshot`（一次性任务）、`Type=notify`（程序主动就绪通知）；`Restart=on-failure` 配合 `RestartSec` 避免风暴式重启。

### 2.2 systemd timer 替代 cron

timer 优势（依据 [systemd.timer(5) 手册](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)）：日志自动进 journald、`Persistent=true` 可补跑停机期间错过的任务、`RandomizedDelaySec` 摊开多机同时触发的负载、`OnBootSec` 等单调定时器不受时钟跳变影响。

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=30min

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup job

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

```bash
sudo systemctl enable --now backup.timer
systemctl list-timers --all          # 看下次/上次触发时间
journalctl -u backup.service -n 50   # 看任务执行日志
```

## 三、日志体系

### 3.1 journald

```bash
journalctl -u nginx --since "1 hour ago"   # 按 unit + 时间过滤
journalctl -p err -b                       # 本次启动的 err 及以上
journalctl -k | grep -i "out of memory"    # 内核日志查 OOM
journalctl --disk-usage                    # 日志占用
sudo journalctl --vacuum-size=500M         # 手动收缩到 500M
```

持久化：默认 journald 只存内存/易失目录，创建 `/var/log/journal` 并 `systemctl restart systemd-journald` 后落盘；大小策略在 `/etc/systemd/journald.conf`（`SystemMaxUse=`、`MaxRetentionSec=`）。

### 3.2 rsyslog 与 logrotate

rsyslog 负责 `/var/log/messages`、`/var/log/secure`（RHEL 系）等传统文件日志与远程转发（`@logserver:514`），配置主文件为 `/etc/rsyslog.conf` 与 `/etc/rsyslog.d/*.conf`。

```conf
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    copytruncate        # 应用不支持重开日志文件时使用
}
```

> [!warning] 双重切割冲突
> 应用自带按天切割（如 Logback）时不要再让 logrotate 处理同一批文件，会出现 `.log.1.gz` 套娃或丢日志；二者选其一。上线前用 `logrotate -d /etc/logrotate.d/myapp` 做 dry-run 验证。

## 四、磁盘与 LVM

```bash
lsblk -f                        # 块设备树 + 文件系统/UUID
df -h                           # 空间水位；df -i 查 inode 是否耗尽
du -xh / | sort -rh | head      # 定位大目录（-x 不跨文件系统）
sudo mkfs.xfs /dev/vdb1         # 格式化（XFS 适合大文件；ext4 通用）
echo 'UUID=xxxx /data xfs defaults 0 2' | sudo tee -a /etc/fstab
sudo mount -a                   # fstab 写完先挂载验证，别直接重启
```

LVM 标准流程与在线扩容：

```bash
sudo pvcreate /dev/vdb /dev/vdc
sudo vgcreate datavg /dev/vdb /dev/vdc
sudo lvcreate -n datalv -l 100%FREE datavg
sudo mkfs.xfs /dev/datavg/datalv && sudo mount /dev/datavg/datalv /data

# 空间不足时在线扩容（XFS 与 ext4 的放大命令不同）
sudo lvextend -l +50%FREE /dev/datavg/datalv
sudo xfs_growfs /data           # XFS 挂载点扩容
# sudo resize2fs /dev/datavg/datalv   # ext4 用这个
```

## 五、性能排查方法论（USE 法则）

[USE 方法](https://www.brendangregg.com/USEmethod/use-linux.html)（Brendan Gregg）：对每种资源检查 **U**tilization（使用率）、**S**aturation（饱和度）、**E**rrors（错误）。落地时先跑"前 60 秒"快查清单，再按资源下钻。

```bash
uptime              # load average，对照 CPU 核数
dmesg -T | tail     # 有无 OOM / 硬件报错
vmstat 1 5          # r/b 列：等 CPU 与阻塞进程；si/so：swap 换入换出
mpstat -P ALL 1     # 各核利用率，看 usr/sys/iowait 分布
pidstat 1           # 进程级 CPU；pidstat -r/-d 看内存/IO
iostat -xz 1        # %util 接近 100% 即磁盘饱和；await 是单次 IO 延迟
free -h             # available 才是真实可用内存
ss -s               # 连接总数与状态分布
```

| 资源 | 工具 | 关键指标与判断 |
|---|---|---|
| CPU | `top`/`htop`/`mpstat`/`pidstat` | load 持续 > 核数；`sys` 高查内核路径；`iowait` 高转查磁盘 |
| 内存 | `free -h`/`vmstat`/`ps aux --sort=-rss` | available 低于 5% 危险；`si/so` 持续非零说明真缺内存；RSS 排名找泄漏者 |
| 磁盘 IO | `iostat -xz 1`/`iotop`/`pidstat -d` | `%util` 饱和、`await` 飙升；结合 `lsof \| grep deleted` 找已删未释放文件 |
| 网络 | `ss -ti`/`sar -n DEV`/`tcpdump` | 重传率、队列溢出（`netstat -s` 对应 `ss -s` 统计）、带宽水位 |

**load average 含义**：Linux 中为"可运行 + 不可中断睡眠（D 状态）"进程数的指数平均，因此 IO 卡死也会推高 load，不能只归因 CPU；三个值对应 1/5/15 分钟趋势。

### OOM 排查

```bash
sudo dmesg -T | grep -iE "out of memory|killed process"   # 找到被杀进程与当时内存快照
journalctl -k --since "1 day ago"                          # 重启过后用 journald 翻内核日志
grep oom_kill /proc/vmstat                                 # 累计 OOM 次数
```

预防：给服务加 `MemoryMax=`/`MemoryHigh=` 限制爆炸半径；确认 systemd-oomd（用户态 OOM 守护）是否参与；参考 [Linuxize 的 OOM 诊断指南](https://linuxize.com/post/how-to-diagnose-oom-killer-events-in-linux/)。

## 六、Shell 脚本运维实战

统一规范：`#!/usr/bin/env bash` 开头 + `set -euo pipefail` 严格模式 + 用 [ShellCheck](https://www.shellcheck.net/) 过一遍（参考 [2025 年 Bash 最佳实践](https://nochlin.com/blog/6-techniques-hacker-news-uses-to-create-great-shell-scripts)）。

```bash
#!/usr/bin/env bash
# backup.sh —— 数据库目录备份：本地压缩 + 异地 rsync + 失败告警
set -euo pipefail

SRC="/var/lib/mysql"
DST="/backup"
KEEP_DAYS=7
REMOTE="ops@10.0.0.8:/backup/db/"

STAMP=$(date +%Y%m%d-%H%M%S)
OUT="${DST}/db-${STAMP}.tar.gz"

cleanup() { rm -f "${OUT}.tmp"; }
trap cleanup EXIT                        # 无论成败都清理临时文件

tar -czf "${OUT}.tmp" -C "$(dirname "$SRC")" "$(basename "$SRC")"
mv "${OUT}.tmp" "$OUT"
rsync -a --delete "$DST/" "$REMOTE"      # 增量同步到备份机
find "$DST" -name 'db-*.tar.gz' -mtime +${KEEP_DAYS} -delete   # 本地保留 7 天
logger -t backup "backup ok: $OUT"       # 写入系统日志便于审计
```

```bash
#!/usr/bin/env bash
# check.sh —— 最小巡检：磁盘/内存/load 超阈值则输出告警行（可接监控）
set -euo pipefail
DISK_PCT=$(df --output=pcent / | tail -1 | tr -dc '0-9')
MEM_AVAIL=$(free -m | awk '/^Mem/{print $7}')
LOAD=$(awk '{printf "%.2f", $1}' /proc/loadavg)
CORES=$(nproc)

(( DISK_PCT > 85 )) && echo "[WARN] disk / usage ${DISK_PCT}%"
(( MEM_AVAIL < 512 )) && echo "[WARN] memory available ${MEM_AVAIL}MB"
awk -v l="$LOAD" -v c="$CORES" 'BEGIN{exit !(l > c*1.5)}' && \
    echo "[WARN] load ${LOAD} > cores*1.5 (${CORES})"
```

部署脚本骨架：`rsync -a --delete new/ /opt/app/` → `systemctl restart myapp` → `curl -fsS --max-time 5 http://127.0.0.1:8080/health` 健康检查失败即 `systemctl restart` 回滚版本目录。生产建议直接交给 [[Jenkins流水线配置]] 编排。

## 七、安全加固清单

```bash
# /etc/ssh/sshd_config 关键项（改完务必 sshd -t 校验再重启）
Port 22                          # 对公网可改高位端口减少扫描噪音
PermitRootLogin no
PasswordAuthentication no        # 仅密钥登录
AllowGroups ssh-users
MaxAuthTries 3
```

```bash
sudo sshd -t && sudo systemctl restart sshd      # 语法校验（失败不会白屏断连）
sudo ufw allow from 10.0.0.0/24 to any port 22   # Ubuntu 防火墙限源放行
sudo firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=10.0.0.0/24 service name=ssh accept'   # RHEL firewalld
sudo nft list ruleset                            # 底层 nftables 实际生效规则
```

| 加固项 | 做法 |
|---|---|
| SSH | Ed25519 密钥、禁 root、禁密码、限源 IP，详见 [Linuxize SSH 加固指南](https://linuxize.com/post/ssh-hardening-best-practices/) |
| fail2ban | `/etc/fail2ban/jail.local` 中对 `sshd` 设 `maxretry 5`、`bantime 1h`，自动封禁爆破 IP |
| 最小权限 | 服务用专用低权用户跑（`User=`）、sudoers 命令白名单、`umask 027`、敏感文件 600 |
| 防火墙 | 默认拒绝（default deny），按端口/来源白名单放行；规则先持久化再 reload |
| 纵深 | SELinux（RHEL 系）或 AppArmor（Debian 系）强制访问控制；auditd 审计关键文件变更 |

> [!danger] 改 SSH 配置的自我保护
> 修改 sshd 前先开一个**已登录的备用会话**再重启服务，并 `sshd -t` 预检；一旦 `PasswordAuthentication no` 生效而密钥未配置，将无法再登录。fail2ban 首次配置时把自己的管理 IP 加入 ignoreip，防止自封。

## 八、容器时代要点

- **容器 = namespace + cgroup + capabilities**。cgroup v2 采用统一层级（`/sys/fs/cgroup`），GKE 1.33+、Amazon Linux 2023、Kubernetes 1.25+ 均默认启用；systemd 259 起移除 cgroup v1，宿主机排查资源问题统一到 v2 路径。
- 服务用 `MemoryMax=`/`CPUQuota=` 限资源，与容器镜像里的 limit 同源同效——理解了 systemd 资源控制，就理解了 [[Kubernetes部署实践]] 的 requests/limits。
- 宿主机关键内核参数：`net.ipv4.ip_forward=1`（容器跨节点转发）、`fs.inotify.max_user_instances`（挂载多的节点要调）、`net.core.somaxconn`。
- 构建镜像遵循 [[Dockerfile编写指南]] 的多阶段与最小化原则；journald 在宿主机上仍能看到所有容器 stdout（经 dockerd/containerd 转发的场景除外），排障顺序：容器日志 → `journalctl -u containerd` → 内核日志。
- 可观测：node_exporter 暴露主机指标给 [[Prometheus监控入门]]，容器指标交给 cAdvisor/kube-state-metrics。

## 九、运维自动化概览（Ansible）

Ansible 用 YAML 声明期望状态，SSH 直连免 agent，幂等性由模块保证，适合把本笔记所有手工操作代码化。

```yaml
# inventory.ini
[web]
web1 ansible_host=10.0.0.11
web2 ansible_host=10.0.0.12

[web:vars]
ansible_user=ops
```

```yaml
# playbook.yml
- hosts: web
  become: true
  tasks:
    - name: 确保时间同步与时区
      community.general.timezone:
        name: Asia/Shanghai
    - name: 安装基础包
      ansible.builtin.package:
        name: [htop, iotop, fail2ban]
        state: present
    - name: 部署 backup.timer
      ansible.builtin.copy:
        src: backup.timer
        dest: /etc/systemd/system/backup.timer
      notify: enable backup timer
  handlers:
    - name: enable backup timer
      ansible.builtin.systemd:
        name: backup.timer
        enabled: true
        state: started
```

常用命令：`ansible all -m ping`、`ansible-playbook -i inventory.ini playbook.yml --check`（干跑）、`--limit web1`。规模化后可被 CI（[[Jenkins流水线配置]]）触发，形成"提交即变更"的 GitOps 流程。

## 十、核心要点速查

| 场景 | 首选命令/位置 |
|---|---|
| 服务起不来 | `systemctl status` → `journalctl -u x -n 100` → `systemd-analyze blame` |
| 定时任务 | `systemctl list-timers` 优先于 crontab；cron 用 `/etc/cron.d/` 统一管理 |
| 磁盘满 | `df -h` → `df -i` → `du -xh / \| sort -rh \| head` → `lsof \| grep deleted` |
| 内存告急 | `free -h`（看 available）→ `ps aux --sort=-rss` → `dmesg -T \| grep -i oom` |
| 端口冲突 | `ss -tlnp \| grep <port>` → `kill <pid>`（先 TERM 后 KILL） |
| 改配置 | 备份 → `systemctl daemon-reload`/`ssh -t` 校验 → 验证 → 沉淀到 Ansible |
| 日志膨胀 | `journalctl --vacuum-size=` + journald.conf 上限 + logrotate 轮转 |

## 十一、常见坑与最佳实践

> [!warning] fstab 写错 = 无法开机
> `/etc/fstab` 里写错 UUID 或文件系统类型，重启会掉进 emergency shell。守则：只追加 `defaults,nofail` 类选项，改完 `mount -a` 验证后再重启；云主机为数据盘加 `nofail`，避免盘未就绪卡住启动。

> [!tip] 排查顺序纪律
> 性能问题先跑"前 60 秒"快查（uptime/dmesg/vmstat/iostat/free/ss），建立"哪类资源饱和"的假设后再深挖（strace/perf），不要一上来就 tcpdump 全量抓包。复盘中把每一步命令与结论记进工单，形成团队排障知识库。

> [!danger] 别在生产机器上"顺手"改内核参数
> `sysctl -w` 立即生效但重启即失效，散落的临时调整会让两台"同配置"机器行为不同。所有调优写入 `/etc/sysctl.d/99-*.conf` 并纳入版本管理；调整前记录原值，便于回滚。

## 十二、2025-2026 最新动态

| 时间点 | 变化 | 运维影响 |
|---|---|---|
| 2024-06 | systemd 256 引入 soft-reboot（仅重启用户态，内核不动） | 应用栈升级可在数秒内完成，配合 `$SYSTEMD_SOFT_REBOOTS_COUNT` 判断重启次数（[systemd 手册](https://www.freedesktop.org/software/systemd/man/256/systemd-soft-reboot.service.html)） |
| 2024-12 | systemd 257 扩大 Varlink IPC 使用，提供 `varlinkctl`（[LWN](https://lwn.net/Articles/1001657/)） | 脚本可经 Varlink 调 systemd API，SSH 隧道亦可透传 |
| 2025-2026 | systemd 259 起移除 cgroup v1、SysV 启动脚本支持逐步移除（259/260） | 遗留 init 脚本与 cgroup v1 工具链必须迁移为原生 unit + cgroup v2 |
| 2025-08 | Debian 13 trixie 发布（内核 6.12 LTS、systemd 257、OpenSSH 10.0p1） | OpenSSH 10 移除 DSA；升级 Debian 时注意 sshd 配置兼容性 |
| 2025 | RHEL 10 / Rocky 10（内核 6.12），Rocky 10.1（2025-11）支持后量子密码 | 企业侧基线更新；RHEL 10 重建版支持至 2035-05 |
| 2026-04 | 内核 7.0 发布（2026-04-12，改号决策 2026-02-08）；Ubuntu 26.04 LTS (2026-04-23) 搭载 7.0 | 当前 kernel.org 稳定版 7.3.5（2026-11-17），生产仍建议 LTS 系（6.18/6.12）；容器 rootfs 加速、fserror 等新特性逐步下沉 |
| 2025-2026 | cgroup v2 全面默认（K8s 1.25+、GKE 1.33+、AL2023） | 统一用 `/sys/fs/cgroup` 排查容器资源问题 |

## 十三、参考资料

1. [systemd.timer(5) 官方手册](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) —— OnCalendar/Persistent/RandomizedDelaySec 语义与示例
2. [systemd-soft-reboot.service (v256)](https://www.freedesktop.org/software/systemd/man/256/systemd-soft-reboot.service.html) 与 [LWN: systemd 257 released](https://lwn.net/Articles/1001657/)
3. [Brendan Gregg: USE Method Linux Checklist](https://www.brendangregg.com/USEmethod/use-linux.html) 与 [Linux Performance](https://www.brendangregg.com/linuxperf.html) —— USE 法则与工具全景
4. [Linuxize: How to Diagnose OOM Killer Events in Linux](https://linuxize.com/post/how-to-diagnose-oom-killer-events-in-linux/)
5. [Linuxize: SSH Hardening Best Practices](https://linuxize.com/post/ssh-hardening-best-practices/)
6. [ShellCheck Wiki](https://www.shellcheck.net/wiki/) 与 [6 Techniques to Create Great Shell Scripts](https://nochlin.com/blog/6-techniques-hacker-news-uses-to-create-great-shell-scripts)（2025-03）
7. [kernel.org](https://www.kernel.org/)（2026-11-17 版本快照）、[DebianWiki: DebianTrixie](https://wiki.debian.org/DebianTrixie)、[Ubuntu 26.04 发行说明](https://documentation.ubuntu.com/release-notes/26.04/)

## 十四、关联笔记

- [[Linux-从入门到精通]] —— 学习路线主线
- [[Linux常用命令集]] —— 日常命令速查
- [[Kubernetes部署实践]] / [[Dockerfile编写指南]] —— 容器化延伸
- [[Jenkins流水线配置]] —— 自动化发布集成
- [[Prometheus监控入门]] —— 指标采集与告警
- [[Web安全最佳实践]] / [[HTTP协议详解]] —— 安全与网络协议上位知识
