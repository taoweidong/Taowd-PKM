---
title: Linux文件系统与目录结构
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 文件系统
  - 目录结构
  - 运维
aliases:
  - FHS
  - Linux目录结构
  - Linux文件系统
source: 网络资料整理
---

# Linux文件系统与目录结构

> [!摘要] 本文系统讲解 Linux 的文件系统与目录结构：以 **FHS（Filesystem Hierarchy Standard）** 为骨架，梳理 `/`、`/etc`、`/var`、`/home`、`/usr`、`/proc`、`/sys`、`/dev` 等核心目录的职责与运维关注点；说明 inode、挂载、虚拟文件系统等核心机制，对比 ext4 / XFS / Btrfs / ZFS 的选型差异；并给出磁盘查看、挂载、查找、空间排查等可直接运行的命令示例。定位为 [[Linux-从入门到精通]] 中「阶段一：入门」的核心基础篇，是后续权限、进程、磁盘与容器学习的前提。

## 一、最新动态（截至 2026-11）

以下事实均来自调研快照（数据截止 2026-11-19），版本号请以官方仓库为准：

- **内核进入 7.x 时代**：首个 7.0.0 于 2026-04-12 发布，**7.3 于 2026-10-18 发布**，最新稳定版为 **7.3.5**（2026-11-16 发布）。7.3 对存储 I/O 与 **Btrfs** 做了性能优化，并支持 AMD Zen 6 平台。
- **LTS 内核三支并行**：**6.18**（2025-11-30 首发，维护至 2028-12）、**6.12**（2024-11-17 首发，维护至 2028-12，Debian 13、RHEL 10 系列采用）、**6.6**（维护至 2027-12）。教学与生产建议以 LTS 为例，避免与 7.x 新特性混淆。
- **工具链版本**：磁盘/挂载工具来自 **util-linux 2.42.4**（2026-09-26），文件操作命令来自 **GNU coreutils 9.12**（2026-09-14）。
- **systemd 262**（2026-09-22 发布）：基础单元文件已内置进二进制，磁盘上的 unit 文件缺失时仍可用内置兜底，容器场景下更稳健。
- **发行版差异**：Ubuntu 26.04 LTS 默认将 **`/tmp` 挂载为 tmpfs**（重启即清空、不落盘），Debian 13 / RHEL 10 采用 6.12 LTS 内核。
- **ReiserFS 已在主线内核移除**（6.12 周期）；bcachefs 的移除情况写作前需到 kernel.org 的 `Documentation/filesystems` 官方目录核实。

## 二、基础概念

**1. 一切皆文件。** Linux 把设备、管道、套接字、普通文件都抽象成文件，由虚拟文件系统（VFS）统一调度，因此 `ls`、`cat`、`mount` 等命令在形式上一致，差别只在底层实现。

**2. inode（索引节点）。** 每个文件对应一个 inode，存放权限、属主、大小、时间戳以及指向数据块的指针。`ls -i` 可查看 inode 号。理解 inode 是理解"磁盘还有空间却报 No space left"的关键。

**3. 挂载（mount）。** 一个文件系统挂到某个目录（挂载点）后才可通过路径访问。挂载关系可由 `/etc/fstab` 持久化，开机自动挂载。

**4. FHS 目录结构。** FHS 规定了各目录的用途，是 Linux 目录结构的"法律"。核心目录如下：

| 目录 | 内容 | 运维关注点 |
|---|---|---|
| `/` | 根，所有路径的起点 | 不要随意放业务文件 |
| `/etc` | 系统与应用配置 | 改前备份；`/etc/fstab` 写错可能无法开机 |
| `/var` | 可变数据（`log`/`lib`/`spool`） | 日志常撑爆磁盘，是排查高发区 |
| `/home` | 普通用户家目录 | 重装可保留；配额管理对象 |
| `/usr` | 系统软件资源（bin/lib/share） | 常态只读；`/usr/local` 放手动编译软件 |
| `/opt` | 第三方大型软件 | 自研/闭源软件常用 |
| `/tmp` | 临时文件 | 重启清空；Ubuntu 26.04 起默认 tmpfs |
| `/proc` | 内核与进程虚拟文件 | `/proc/meminfo`、`/proc/mounts` 排障数据源 |
| `/sys` | 设备与内核对象 | cgroup v2 位于 `/sys/fs/cgroup` |
| `/dev` | 设备文件 | 块设备如 `/dev/sda`、`/dev/nvme0n1` |
| `/boot` | 内核与引导文件 | 多内核共存，升级排查重点 |

## 三、核心机制

**虚拟文件系统（VFS）。** 上层通过路径访问，VFS 负责解析路径、查找 inode、把操作分派到具体文件系统驱动（ext4、XFS、Btrfs 等），从而让同一套命令兼容不同文件系统。

**inode 与硬链接、软链接。** 硬链接与源文件共享同一 inode，删除源文件数据不丢；软链接（符号链接）只存目标路径，源文件删除后成为"悬空链接"。`ln` 不加参数创建硬链接，`ln -s` 创建软链接。

**挂载与命名空间。** 挂载点是一个普通目录，文件系统"叠"在之上。容器依赖 mount namespace 实现隔离，因此同一份根文件系统在不同容器里看到的挂载视图可以不同。

**主流文件系统对比。**

| 文件系统 | 特点 | 适用场景 |
|---|---|---|
| ext4 | 通用、成熟、稳定，默认选择多 | 常规服务器、小到中等卷 |
| XFS | 大卷与大文件友好，支持在线扩容，**不可收缩** | 数据库、大文件存储 |
| Btrfs | 支持快照、子卷、校验、在线扩缩容；**内核 7.3 已做性能优化** | 需要快照/子卷的灵活场景 |
| ZFS | 功能强，但**不在主线内核**，需第三方模块 | 需自行安装模块的环境 |

## 四、实践步骤（含代码/命令示例）

**1. 查看磁盘与文件系统。**

```bash
# 显示文件系统类型与容量（-T 显示类型，-h 人类可读）
df -hT

# 查看块设备、文件系统与挂载点
lsblk -f

# 查看当前挂载关系（等价于 cat /proc/mounts）
findmnt
cat /proc/self/mounts
```

**2. 查看目录/文件占用。**

```bash
# 目录总大小
du -sh /var/log

# 列出 /var/log 下各子目录占用并按大小排序
du -sh /var/log/* | sort -rh | head -20

# 查找大文件（如超过 100M）
find / -xdev -type f -size +100M -exec ls -lh {} \;
```

**3. 查看 inode 与文件属性。**

```bash
ls -i /etc/passwd        # 查看 inode 号
stat /etc/passwd         # 查看权限、属主、时间戳、块分配
find / -xdev -printf '%i\n' | sort | uniq -c | sort -rn | head  # 检查 inode 复用
```

**4. 创建文件系统并挂载。**

```bash
# 确认目标设备
lsblk -f

# 格式化为 ext4（-L 指定卷标）
mkfs.ext4 -L data /dev/sdb1

# 挂载到 /data
mkdir -p /data
mount /dev/sdb1 /data

# 写入 /etc/fstab 实现开机自动挂载（UUID 更稳）
blkid /dev/sdb1
echo 'UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx /data ext4 defaults 0 2' | sudo tee -a /etc/fstab

# 只读重挂或调整挂载参数
mount -o remount,rw /data
```

**5. 链接与路径解析。**

```bash
ln -s /var/log/app.log /tmp/app-link   # 软链接
ln /var/log/app.log /tmp/app-hard     # 硬链接
readlink -f /tmp/app-link              # 解析符号链接最终路径
```

## 五、最佳实践与常见坑

> [!warning] 别用 `rm -rf` 赌路径
> 递归删除前先 `echo` 预演、用绝对路径，脚本里给变量兜底 `: "${DIR:?未设置}"`。GNU rm 对 `/` 有内置保护，但拼接路径没有。

- **先看类型再看容量**：`df -h` 只显示容量，`df -hT` 才显示文件系统类型；inode 耗尽会报 "No space left on device"，需用 `df -i` 单独检查。
- **改 `/etc/fstab` 前务必备份并验证**：一行写错可能导致无法开机，建议先在测试机验证，或用 `mount -a` 校验配置能否正常挂载。
- **不要把挂载点当普通目录用**：挂载后目录原有内容会被"遮住"，卸载后才可见，容易造成数据"丢失"错觉。
- **日志治理优先于扩容**：`/var/log` 是最常撑爆的位置，用 `logrotate` 轮转，排查时先看 `du -sh /var/log/*`，不要一上来就加盘。
- **`/tmp` 行为因发行版而异**：Ubuntu 26.04 起默认 tmpfs，重启即清空、且占用内存，不要把持久数据放在 `/tmp`。
- **删除大目录先量化**：删除前用 `du -sh` 确认，避免误删在跑的日志导致服务异常。
- **容器文件系统与宿主机隔离**：容器内的挂载视图由 namespace 隔离，宿主机上的 `mount` 结果不能直接套用。

## 六、核心要点速查

- 目录结构标准：**FHS**；核心目录：`/etc`（配置）、`/var`（可变数据）、`/home`（家目录）、`/usr`（软件资源）、`/proc`、`/sys`、`/dev`、`/boot`、`/tmp`、`/opt`。
- 核心机制：**一切皆文件**、**inode**、**挂载**、**VFS**；链接分硬链接（共享 inode）与软链接（存路径）。
- 主流文件系统：**ext4**（通用）、**XFS**（大卷，不可收缩）、**Btrfs**（快照/子卷，内核 7.3 优化）、**ZFS**（非主线内核）。
- 常用命令：`df -hT`、`df -i`、`du -sh`、`lsblk -f`、`findmnt`、`mount`、`stat`、`readlink -f`。
- 版本基线：内核主线 **7.3.5**、LTS **6.12 / 6.18**；磁盘工具 util-linux **2.42.4**；文件命令 coreutils **9.12**。

## 七、学习资源

1. [FHS（Filesystem Hierarchy Standard）](https://refspecs.linuxbase.org/fhs.shtml) —— 目录结构权威标准
2. [kernel.org 内核文档：filesystems](https://www.kernel.org/doc/html/latest/filesystems/) —— 内核支持的文件系统官方目录
3. [man7.org: mount(8)](https://www.man7.org/linux/man-pages/man8/mount.8.html) —— 挂载命令权威手册
4. [man7.org: lsblk(8)](https://www.man7.org/linux/man-pages/man8/lsblk.8.html) —— 块设备查看手册
5. [GNU Coreutils 手册](https://www.gnu.org/software/coreutils/) —— `df/du/stat` 等命令来源
6. [The Linux Command Line（William Shotts，免费 PDF）](https://www.linuxcommand.org/) —— 文件系统入门系统读物

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习路线中的定位
- [[Linux常用命令集]] —— 目录操作与磁盘命令的高频速查
- [[Linux系统管理与运维要点]] —— 磁盘治理与故障排查的进阶展开

## 九、变更记录

- 2026-11-19：首次创建。
