---
title: Linux基础与命令入门
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 命令行
  - 入门
aliases:
  - Linux命令入门
  - Linux 基础与命令
source: 网络资料整理
---

# Linux基础与命令入门

> [!摘要] 内容与定位
> 本文是 [[Linux-从入门到精通]] 学习路线中**阶段一（入门）**的核心文档，目标是让读者在终端里独立完成日常操作：认识 Linux 的内核与发行版关系、理解 shell 与命令执行机制，掌握路径导航、文件操作、文本查看、帮助系统与管道重定向等基础命令。所有版本号均来自 2026-11-19 的调研快照，正式选型请回查官方源。读完本文可进入 [[Linux常用命令集]] 做命令速查，再向 [[Linux系统管理与运维要点]] 的进阶内容推进。

## 一、最新动态（截至 2026-11）

Linux 迭代极快，入门阶段虽以基础命令为主，但需要对「版本」有正确认知，避免把主线版本当成发行版默认版本。

- **内核进入 7.x 时代**：主线 **7.0.0** 于 2026-04-12 发布；**7.3** 于 2026-10-18 发布；截至调研时稳定版为 **7.3.5**（2026-11-16 由 Greg Kroah-Hartman 发布，同批发布 LTS 6.18.64、6.12.118）。
- **LTS 长期维护内核三支并行**：**6.18**（2025-11-30 首发，维护至 2028-12）、**6.12**（2024-11-17 首发，维护至 2028-12）、**6.6**（维护至 2027-12）。入门教学建议**统一以 LTS 内核为例**，避免与 7.x 新特性混淆。
- **发行版自带内核差异明显**：Ubuntu 26.04 LTS 搭载内核 **7.0**；Debian 13（trixie）与 RHEL 10 系列采用 **6.12 LTS**。同一条命令的可用行为在不同发行版上可能不同。
- **命令行工具版本基准**：常用命令（`ls/cp/mv/rm/find/cat/echo` 等）来自 **GNU coreutils 9.12**（2026-09-14）；默认 shell 多为 **bash 5.3**（2025-07-04 发布，新增 `read -E`、`source -p PATH`，源码已 C23 合规、不再兼容 K&R 编译器）。`cut/nl/unexpand` 已支持多字节字符，`cat/yes` 在 Linux 上使用零拷贝 I/O。
- **系统服务栈**：systemd 已进入 **262** 代（2026-09-22 发布，systemd-stable 已到 262.2）；但 Ubuntu 26.04 LTS 仍使用 **systemd 259**，跨发行版套用 systemd 示例时需先确认版本。

> [!note] 时效性提示
> 以上为 2026-11-19 快照。内核小版本、发行版补丁号变化频繁，正式使用前请按来源 URL 复核：内核见 [kernel.org](https://www.kernel.org/)，命令行工具见 [GNU Coreutils](https://www.gnu.org/software/coreutils/)。

## 二、基础概念

### 2.1 Linux 是内核，不是完整系统

严格说 **Linux 只是内核**（Kernel），负责进程调度、内存管理、文件系统与设备驱动。普通人用的「Linux 系统」其实是**内核 + GNU 工具链 + 包管理器 + 桌面/服务**打包成的**发行版**（Distribution），如 Debian、Ubuntu、Fedora、RHEL、Alpine、openSUSE 等。内核与发行版解耦：同一份 6.12 LTS 内核可以出现在 Debian 13、RHEL 10 等不同发行版中。

### 2.2 Shell 与终端

Shell 是用户与内核之间的命令解释器，负责读取输入、解析语法、创建子进程执行命令。主流 shell：

| Shell | 特点 | 典型场景 |
|---|---|---|
| bash | GNU 项目默认 shell，语法丰富 | 各主流发行版默认（bash 5.3） |
| sh (dash) | POSIX 精简，兼容优先 | `/bin/sh`，Debian 系默认 |
| zsh | 交互体验好、补全强 | 桌面/开发机常用 |
| fish | 语法直观、免配置 | 个人开发机 |

终端（Terminal/TTY）只是 shell 的输入输出界面，真正的逻辑在 shell 里。

### 2.3 几个绕不开的核心概念

- **一切皆文件**：普通文件、目录、设备、管道、套接字在 Linux 里都以文件形式暴露，统一用同一套读写接口处理。
- **绝对路径与相对路径**：绝对路径从 `/` 开始（如 `/etc/passwd`），相对路径相对当前目录（`.` 当前、`..` 上一级）。命令里优先使用绝对路径，避免 `cd` 后路径漂移。
- **权限三要素**：每个文件有属主（user）、属组（group）、其他人（other）三类身份，每类有读 `r`、写 `w`、执行 `x` 三种权限。这是后续所有文件操作的前提。
- **命令执行模型**：shell 解析命令后，通过 `fork` 创建子进程、`exec` 替换为目标程序，父进程等待或异步回收。理解这一点，才能明白「管道」「重定向」为何存在。

## 三、核心机制

### 3.1 一条命令的执行链路

```bash
$ ls -l /etc/hostname
```

1. Shell 读取输入，按空格拆分词法，识别 `ls` 为命令、`-l` 为选项、`/etc/hostname` 为参数；
2. 通过 `PATH` 环境变量按顺序查找 `ls`（通常在 `/usr/bin/ls`）；
3. `fork` 出子进程，`exec` 加载 GNU coreutils 的 `ls`；
4. `ls` 通过系统调用读取目录项并格式化输出，退出后 shell 回收子进程并显示返回码。

`echo $PATH` 可查看搜索路径，它同时决定了「为什么在任意目录都能执行 `ls`」。

### 3.2 管道与重定向

Linux 命令的强项在于**把单一小功能串成流水线**。其基础是标准流：每个进程默认有三个文件描述符——`0` 标准输入、`1` 标准输出、`2` 标准错误。

- **管道 `|`**：把前一个命令的 stdout 接到后一个命令的 stdin，实现流式处理。
- **重定向 `>` / `>>`**：把输出写入文件，`>` 覆盖、`>>` 追加。
- **`2>&1`**：把错误流合并进输出流，常用于日志收集。

```bash
# 查看磁盘占用最大的前 10 个目录（管道 + 排序 + 截取）
du -sh /var/* 2>/dev/null | sort -h | tail -n 10

# 同时记录正常输出与错误
systemctl status ssh.service > ssh.log 2>&1
```

### 3.3 帮助系统：先看手册，再查语法

Linux 命令极多，记住「**现场查手册**」比死记参数更重要：

- `man 命令`：完整手册，按 `q` 退出、`/关键词` 搜索、`h` 看快捷键。例如 `man ls`、`man tar`。
- `命令 --help`：快速查看用法摘要，适合记不全时快速回忆。
- `apropos 关键词`：按关键词反查「哪个命令支持这个功能」。

```bash
man ls              # 完整手册
tar --help          # 快速摘要
apropos compress   # 找与压缩相关的命令
```

### 3.4 路径展开与通配

Shell 在执行前会展开 `*`、`?`、`[]` 等通配符，并支持 `~`、`.`、`..`：

```bash
ls /var/log/*.log      # 匹配所有 .log 文件
ls /etc/[sv]sh*        # 匹配 sshd、ssh 相关配置
```

注意展开是 shell 完成的，若把通配符放进脚本或期望程序自行处理，往往得到意外结果。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境准备

推荐用虚拟机、WSL2 或容器做隔离练习，不要在生产机上试手。先确认当前环境：

```bash
uname -a        # 内核版本、架构、发行信息
cat /etc/os-release   # 发行版名称与版本
whoami          # 当前用户
hostname        # 主机名
echo $SHELL     # 当前 shell
```

### 4.2 路径导航与文件操作

```bash
# 导航
pwd                 # 显示当前目录绝对路径
ls -l               # 长格式列出，看清权限、属主、大小、时间
ls -la              # 含隐藏文件（以 . 开头）
cd /etc && ls       # 切换目录并列出
cd -                # 回到上一个目录

# 创建与删除
mkdir -p ~/demo/sub   # -p 递归创建多级目录
touch ~/demo/note.txt # 创建空文件或刷新时间戳
cp -i ~/demo/note.txt ~/demo/backup.txt   # -i 覆盖前询问
mv ~/demo/backup.txt ~/demo/backup.old    # 移动或重命名
rm -i ~/demo/backup.old                   # -i 交互删除，避免误删
```

### 4.3 查看文本与统计

```bash
cat  /etc/hostname          # 全文输出（文件大时不要用）
less /etc/ssh/sshd_config   # 分页查看，q 退出
head -n 20 /var/log/syslog  # 前 20 行
tail -n 50 /var/log/syslog  # 后 50 行
tail -f /var/log/syslog     # 实时跟踪新增内容（排障利器）
wc -l /var/log/syslog       # 统计行数

# 查找文件
find /var/log -name '*.log' -type f -mtime -7   # 最近 7 天的日志文件
```

### 4.4 权限的入门操作

```bash
id                      # 查看当前用户 UID 与所属组
chmod 644 note.txt      # 属主读写，其他人只读
chmod 755 script.sh     # 属主全权，其他人可读可执行
chmod +x script.sh      # 追加执行位
chown user:group file   # 修改属主与属组（通常需 sudo）
```

### 4.5 管道重定向综合练习

```bash
# 找出当前登录用户
whoami | tr 'A-Z' 'a-z'

# 统计当前目录下文件总数
find . -type f | wc -l

# 在日志中筛出错误行，去重后计数
grep -i error /var/log/syslog | sort | uniq -c | sort -rn
```

## 五、最佳实践与常见坑

> [!danger] `rm -rf` 是第一大坑
> 变量为空或路径少空格时会造成毁灭性删除：`rm -rf "$DIR/"*` 在 `DIR` 未定义时可能退化为删除根目录。守则：删除一律用**绝对路径**、先 `echo` 预演、脚本里给变量兜底 `: "${DIR:?未设置}"`。GNU rm 对 `/` 有内置保护，但拼接路径没有。

- **不要日常用 root**：root 下一条误操作无法挽回，普通操作用普通用户，需要权限时用 `sudo`，并且按命令白名单最小授权。
- **避免 `chmod -R 777`**：人人可写既不安全，也掩盖了属主设计问题。正确做法是先 `id`、`ps aux` 查清运行身份，再用 `chown` + 属组或 ACL 精确授权。
- **慎用 `kill -9`**：SIGKILL 不可捕获，会跳过进程的清理逻辑，数据库类服务强杀恢复成本极高。先 `kill PID`（SIGTERM 留清理机会），超时再 `kill -9`。
- **路径含空格要加引号**：`cp my file.txt /tmp/` 会被拆成三个参数。统一写成 `cp "my file.txt" /tmp/`。
- **命令替换与引号**：变量赋值和条件判断不加引号，遇到空格、通配符就会出错；`"$var"` 是安全默认。
- **`sed -i` 改配置必带备份后缀**：如 `sed -i.bak 's/old/new/g' file.conf`，改完先验证再推生产。
- **养成看手册与返回码的习惯**：`echo $?` 查看上一条命令返回码，`0` 为成功。排障时先查返回码，再查输出。

## 六、核心要点速查

| 分类 | 高频命令 |
|---|---|
| 环境信息 | `uname -a`、`cat /etc/os-release`、`whoami`、`hostname`、`echo $PATH` |
| 路径导航 | `pwd`、`ls -la`、`cd`、`cd -`、`cd ~` |
| 文件操作 | `mkdir -p`、`touch`、`cp -i`、`mv`、`rm -i`、`ln` |
| 文本查看 | `cat`、`less`、`head`、`tail -f`、`wc`、`find` |
| 权限 | `id`、`chmod`、`chown`、`ls -l` |
| 帮助 | `man`、`--help`、`apropos` |
| 流控制 | `\|`、`>`、`>>`、`2>&1`、`2>/dev/null` |
| 过滤组合 | `grep`、`sort`、`uniq`、`xargs`、`tr` |

**权限数字对照**：`7`=rwx、`6`=rw-、`5`=r-x、`4`=r--、`0`=---。常用组合：`755`（目录/脚本）、`644`（普通文件）、`700`（`~/.ssh` 等私有目录）。默认权限由 umask 决定，常见 umask `022` → 新文件 644、新目录 755。

## 七、学习资源

1. [The Linux Command Line（William Shotts，官方免费在线书）](https://www.linuxcommand.org/) —— 入门首选，覆盖命令与脚本
2. [man7.org: Linux Man Pages](https://man7.org/) —— 命令手册权威入口
3. [GNU Coreutils 官方文档](https://www.gnu.org/software/coreutils/) —— `ls/cp/mv/rm/find` 等命令的权威来源
4. [GNU Bash 官方文档](https://www.gnu.org/software/bash/) —— shell 语法与 5.3 新特性
5. [kernel.org 内核文档](https://www.kernel.org/doc/) —— 内核机制查证入口
6. [Linux Journey](https://linuxjourney.com/) —— 交互式闯关式练习
7. [ShellCheck 官网](https://www.shellcheck.net/) —— 脚本静态检查，入门后期必备

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在体系中的位置与完整学习路线
- [[Linux常用命令集]] —— 各阶段高频命令速查

## 九、变更记录

- 2026-11-19：首次创建。
