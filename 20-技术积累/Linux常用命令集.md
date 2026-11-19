---
title: Linux常用命令集
date: 2026-11-18
tags:
  - 技术积累
  - Linux
  - 命令行
  - 运维
  - 速查
---

# Linux常用命令集

> [!abstract] 定位
> 高频命令速查手册，按使用场景分类组织。学习路线见 [[Linux-从入门到精通]]，运维实战见 [[Linux系统管理与运维要点]]。示例以 Bash 为准，Debian/Ubuntu 与 RHEL 系通用；带 `$` 的命令普通用户即可执行，涉及系统修改的需 `sudo`。

## 一、概述

Linux 命令行是服务器运维的基本功。日常 90% 的操作集中在几十个命令上：文件与目录操作、文本三剑客（grep/sed/awk）、权限与用户、进程与性能、网络诊断、打包压缩。本笔记只收录最常用、最不易忘的部分，组合技统一放在第十节。命令参数细节可用 `man <命令>` 或 `<命令> --help` 查询；man 页权威参考见 [man7.org](https://man7.org/linux/man-pages/)。

## 二、文件与目录

| 命令 | 常用写法 | 一句话说明 |
|---|---|---|
| `ls` | `ls -lah` | 详细列表 + 人类可读大小 + 隐藏文件 |
| `cd` | `cd -` | 返回上一次所在目录 |
| `pwd` | `pwd` | 显示当前绝对路径 |
| `cp` | `cp -av src dst` | 归档模式复制（保留属性，显示过程） |
| `mv` | `mv old new` | 移动/重命名，同盘为改名操作 |
| `rm` | `rm -rf dir` | 递归强制删除（==高危，先确认路径==） |
| `mkdir` | `mkdir -p a/b/c` | 递归创建多级目录 |
| `find` | 见下方组合技 | 按名字/大小/时间/类型递归查找 |
| `ln` | `ln -s target link` | 创建软链接 |
| `stat` | `stat file` | 查看 inode、权限、时间戳元数据 |

```bash
# find 实用示例
find /var/log -name "*.log" -mtime +7          # 7 天前的日志
find / -size +500M -type f 2>/dev/null          # 找 500MB 以上大文件
find . -name "*.tmp" -delete                    # 批量删除（先不带 -delete 预览）
find . -mtime -1 -name "*.conf"                 # 最近 1 天修改过的配置
```

## 三、文本处理

| 命令 | 常用写法 | 一句话说明 |
|---|---|---|
| `cat` | `cat -n file` | 输出全文并显示行号；大文件用 `less` |
| `less` | `less +F file` | 分页查看，`+F` 类似 `tail -f` 实时跟踪 |
| `head`/`tail` | `tail -f app.log` | 看头/尾 N 行；`-f` 实时追踪日志 |
| `grep` | `grep -rni "error" /etc` | 递归、忽略大小写、显示行号搜索 |
| `sed` | `sed -i.bak 's/old/new/g' f` | 流编辑批量替换，`-i.bak` 自动留备份 |
| `awk` | `awk '{print $1}' f` | 按列提取（默认空白分列，`$1` 为第一列） |
| `sort` | `sort -nrk3 f` | 按第 3 列数值逆序排序 |
| `uniq` | `sort f \| uniq -c` | 去重计数（必须先 sort） |
| `wc` | `wc -l f` | 统计行数 |
| `cut` | `cut -d: -f1 /etc/passwd` | 按分隔符取第 1 列 |
| `xargs` | `... \| xargs -I{} cp {} bak/` | 把管道输出变成命令参数 |

```bash
# 文本组合技
grep -r "TODO" --include="*.py" .        # 只在 .py 中递归搜索
awk -F: '$3>=1000 {print $1}' /etc/passwd   # 列出 UID>=1000 的普通用户
sort access.log | uniq -c | sort -rn | head   # 最常出现的行 Top10
echo "1 2 3" | tr ' ' '\n'               # 空格转换行
```

## 四、权限与用户

| 命令 | 常用写法 | 一句话说明 |
|---|---|---|
| `chmod` | `chmod 750 app.sh` | 数字法改权限；`chmod +x` 加执行位 |
| `chown` | `chown user:group file` | 改属主与属组（需 root） |
| `useradd` | `useradd -m -s /bin/bash tom` | 创建用户并生成家目录 |
| `usermod` | `usermod -aG docker tom` | 追加用户到附加组（`-aG` 缺 `-a` 会覆盖） |
| `passwd` | `passwd tom` | 设置/修改密码 |
| `su` | `su - tom` | 切换用户并加载其环境（带 `-`） |
| `sudo` | `sudo -l` | 提权执行；`-l` 列出当前用户可用的提权命令 |
| `id` | `id tom` | 查看 UID/GID 及所属组 |
| `umask` | `umask 022` | 设置新建文件的默认权限掩码 |
| `getfacl`/`setfacl` | `setfacl -m u:tom:rx dir` | ACL 细粒度授权，突破"属主/属组/其他"三段限制 |

```bash
# 权限数字对照：r=4, w=2, x=1
# 754 = 属主 rwx(7) + 属组 r-x(5) + 其他 r--(4)
chmod 644 /etc/nginx/conf.d/app.conf    # 配置文件常见权限
chown -R www-data:www-data /var/www     # 网站目录整体改属主
```

## 五、进程与性能

| 命令 | 常用写法 | 一句话说明 |
|---|---|---|
| `ps` | `ps aux \| grep nginx` | 快照式查看进程；`ps -ef` 看父子关系 |
| `top` | `top` 按 `P`/`M`/`1` | 动态监控；`P` 按 CPU、`M` 按内存排序，`1` 展开各核 |
| `htop` | `htop -u tom` | top 增强版，支持鼠标与树状视图 |
| `kill` | `kill 1234` | 发送信号；**默认 SIGTERM(15)**，`kill -9` 为 SIGKILL |
| `pkill` | `pkill -f "python app.py"` | 按名称/完整命令行批量杀进程 |
| `pgrep` | `pgrep -a nginx` | 按名称查 PID，`-a` 同时显示命令 |
| `nohup` | `nohup cmd &` | 挂断不退出的后台运行 |
| `free` | `free -h` | 内存概览，关注 `available` 而非 `free` |
| `df` | `df -h` / `df -i` | 磁盘空间 / inode 使用量 |
| `du` | `du -sh * \| sort -h` | 目录占用大小排序 |
| `lsof` | `lsof -i :8080` | 谁在占用端口；`lsof \| grep deleted` 找已删未释放文件 |
| `uptime` | `uptime` | 运行时长与 load average |

> [!tip] load average 怎么读
> `uptime` 三个数字是 1/5/15 分钟的平均负载（可运行+不可中断睡眠进程数）。经验法则：超过 CPU 逻辑核数即趋于饱和；持续高于核数 2 倍说明排队严重。结合 `vmstat 1` 的 `r` 列（等 CPU 的进程）与 `b` 列（阻塞进程）判断是 CPU 瓶颈还是 IO 等待。

## 六、网络

| 命令 | 常用写法 | 一句话说明 |
|---|---|---|
| `ip` | `ip -br addr` / `ip route` | 看接口地址（`-br` 紧凑模式）/ 路由表 |
| `ss` | `ss -tlnp` | 监听端口+进程；`ss -s` 连接统计；**替代 netstat** |
| `ping` | `ping -c 4 host` | ICMP 连通性，`-c` 限定次数 |
| `dig` | `dig +short example.com` | DNS 解析，`+short` 只要结果 |
| `curl` | `curl -I https://a.com` | 只看响应头；`-o` 下载、`-w` 输出耗时指标 |
| `nc` | `nc -zv host 22` | 端口连通性测试（扫描/调试 TCP/UDP） |
| `traceroute` | `traceroute host` | 路径逐跳追踪 |
| `tcpdump` | `tcpdump -i eth0 port 443 -w p.pcap` | 抓包存文件，用 Wireshark 分析 |

```bash
# 网络组合技
ss -tn state established '( dport = :443 )'   # 已建立的 443 连接
curl -o /dev/null -sw "%{http_code} %{time_total}\n" https://a.com   # 状态码+总耗时
ip -br link                                    # 网卡 up/down 一览
```

## 七、压缩与打包

| 命令 | 常用写法 | 一句话说明 |
|---|---|---|
| `tar` | `tar -czf out.tgz dir/` | 打包并 gzip 压缩（c 建/ x 解/ z gzip/ v 显示/ f 文件名） |
| `tar` | `tar -xzf out.tgz -C /target` | 解压到指定目录 |
| `gzip` | `gzip -k file` | 原地压缩，`-k` 保留原文件 |
| `zip`/`unzip` | `unzip -l a.zip` | Windows 互通场景；`-l` 只看清单 |
| `xz` | `tar -cJf out.txz dir/` | 压缩率更高、更慢，适合归档 |

```bash
# 打包时排除目录
tar --exclude="dir/node_modules" -czf code.tgz dir/
# 只解压其中一个文件
tar -xzf backup.tgz etc/nginx/nginx.conf
```

## 八、systemd 服务与日志

```bash
# systemctl：服务生命周期
sudo systemctl start|stop|restart|reload nginx   # 启停/重启/重载配置
systemctl status nginx                           # 状态 + 最近日志片段
sudo systemctl enable --now nginx                # 设为开机自启并立即启动
systemctl list-units --type=service --state=failed   # 列出失败服务
systemctl list-timers                            # 查看所有定时任务下次触发时间
systemd-analyze blame                            # 各服务启动耗时排名

# journalctl：统一日志查询
journalctl -u nginx -n 100 --no-pager            # 某 unit 最近 100 行
journalctl -u nginx -f                           # 实时跟踪某服务日志
journalctl --since "2026-11-17" --until "2026-11-18"   # 按时间窗过滤
journalctl -k -p err                             # 本次启动内核日志中的 err 及以上
journalctl --disk-usage                          # 日志占用空间
```

> [!note] timer 与 cron 的选择
> 新写的定时任务优先用 systemd timer（`OnCalendar` 表达式 + 配套 service），可从 `systemctl list-timers` 看下次触发时间、日志直接进 journald，`Persistent=true` 还能在停机期间错过后补跑。cron 适合简单的一次性行内任务。配置细节见 [[Linux系统管理与运维要点]]。

## 九、SSH 与远程

```bash
ssh user@host                        # 基本登录
ssh -p 2222 user@host                # 指定端口
ssh -J jump user@target              # 经堡垒机跳转（OpenSSH 7.3+）
ssh-keygen -t ed25519 -C "comment"   # 生成 Ed25519 密钥对（2025 年主流推荐）
ssh-copy-id user@host                # 推送公钥实现免密登录
scp file user@host:/tmp/             # 单次拷贝
rsync -avzP --delete src/ user@host:/dst/   # 增量同步（斜杠含义：src/ 同步目录内容本身）
ssh -L 8080:localhost:80 user@host   # 本地端口转发
ssh -D 1080 user@host                # 动态 SOCKS 代理
```

## 十、实用组合技速查

```bash
# 1. 统计访问日志中 Top10 来源 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 2. 找出吃掉磁盘空间的元凶（常见：日志与缓存）
du -xh / 2>/dev/null | sort -rh | head -20

# 3. 批量替换某目录下所有文件中的字符串
grep -rl "old.domain.com" /etc/nginx | xargs sed -i 's/old.domain.com/new.domain.com/g'

# 4. 杀掉占用某端口的进程
kill $(lsof -t -i :8080)

# 5. 命令结果同时输出到屏幕和文件
make 2>&1 | tee build.log

# 6. 统计代码行数
find . -name "*.go" | xargs wc -l | tail -1

# 7. 每秒观察磁盘 IO 与 CPU 等待（systra 包）
iostat -xz 1 && vmstat 1

# 8. 把当前目录打包传到远端（不落盘中间文件）
tar -czf - . | ssh user@host "tar -xzf - -C /opt/app"

# 9. 最近登录与失败尝试（安全巡检）
last -20 && sudo lastb | head -20

# 10. 找出最近 10 分钟内被修改的文件（定位异常写入）
find /etc /var -mmin -10 -type f 2>/dev/null
```

## 十一、常见坑与最佳实践

> [!danger] rm -rf 事故高发点
> 变量为空时 `rm -rf "$DIR/"*` 会退化为 `rm -rf /`（视 shell 与版本而定，GNU rm 在 `/` 上有保护，但 `"/var/$SUB"` 这类拼接路径没有）。删除前固定三步：`echo` 打出最终路径、用 `pwd`/`ls` 复核、必要时把命令限制在绝对路径并禁用通配符。生产机器建议对 `/` 下的删除操作一律先 `ls` 预览。

> [!warning] 别用 chmod -R 777 解决权限问题
> `777` 让所有用户可写，等于对world开放，还会掩盖真正的属主问题。正确做法：先 `ls -l` / `id` 弄清进程运行身份，再精确授权（`chown` + `750`/`640`），跨用户共享用组或 ACL（`setfacl`）。同理，习惯性 `kill -9` 会让进程跳过清理逻辑，应先发默认的 SIGTERM（kill(1) 手册明确建议优先 TERM，进程可注册处理器做善后），几秒无效再 `-9`。

> [!tip] 降低误操作成本的习惯
> - 危险命令前先加 `echo` 演练（`echo rm -rf "$path"`），确认无误去掉 echo 重跑。
> - `sed -i` 永远带备份后缀（`-i.bak`），改完 diff 再清理。
> - 用 `set -euo pipefail` + ShellCheck（[shellcheck.net](https://www.shellcheck.net/)）约束自己的脚本，静态检查能拦住大部分引号与变量坑。

## 十二、2025-2026 动态

| 时间点 | 变化 | 对日常命令的影响 |
|---|---|---|
| 2024-11 起（内核 6.9+） | util-linux `kill` 支持 `PID:inode` 形式与 `--timeout` 选项，基于 pidfd 避免 PID 复用竞态 | 发信号更安全，脚本杀进程可防"杀错人" |
| 2025-08 | Debian 13 (trixie) 发布，内置 OpenSSH 10.0p1 | OpenSSH 10 移除 DSA 用户密钥，推荐 Ed25519 |
| 2025-12 | 内核中 Rust 转正为非实验组件；首枚 Rust GPU 驱动 Tyr 进入 6.18 | 对命令行使用无感，但发行版开始引入 Rust 组件 |
| 2026-04 | 内核 7.0 发布（2026-02-08 宣布改号，跳过 6.20）；Ubuntu 26.04 LTS (2026-04-23) 搭载 7.0，并引入 rust-coreutils、sudo-rs | `kill`/`ls`/`cp` 等核心工具逐步出现 Rust 实现，行为保持兼容；sudo 的默认实现开始迁移 |
| 2026-11（当前） | kernel.org 最新稳定版 7.3.5（2026-11-17），LTS：6.18 / 6.12 / 6.6 / 6.1 / 5.15 / 5.10 | 服务器仍建议锁 LTS 系内核；`ss`/`ip` 全面取代 netstat/ifconfig 已是既成事实 |

## 十三、参考资料

1. [man7.org — kill(1) 手册页](https://man7.org/linux/man-pages/man1/kill.1.html)（信号语义与默认 SIGTERM 的权威来源）
2. [kernel.org — The Linux Kernel Archives](https://www.kernel.org/)（当前稳定版与 LTS 版本列表，2026-11-17 数据）
3. [Brendan Gregg — Linux Performance](https://www.brendangregg.com/linuxperf.html)（性能工具全景图与 USE 方法）
4. [systemd.timer(5) 官方手册](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)（OnCalendar、Persistent 等选项）
5. [Linuxize — SSH Hardening Best Practices](https://linuxize.com/post/ssh-hardening-best-practices/)（sshd 加固基线）
6. [ShellCheck 官网与 Wiki](https://www.shellcheck.net/wiki/)（Shell 静态检查规则）
7. [DebianWiki — DebianTrixie](https://wiki.debian.org/DebianTrixie)（Debian 13 组件版本，2025-08-09 发布）

## 十四、关联笔记

- [[Linux-从入门到精通]] —— 完整学习路线主线
- [[Linux系统管理与运维要点]] —— systemd/日志/性能排查/安全加固实战
- [[网络基础概念]] —— `ss`/`ip`/`dig` 背后的网络知识
- [[Web安全最佳实践]] —— SSH 与防火墙加固的上位视角
- [[Prometheus监控入门]] —— 把本页命令采集的指标纳入监控体系
