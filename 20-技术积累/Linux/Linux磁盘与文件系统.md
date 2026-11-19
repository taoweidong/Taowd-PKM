---
title: Linux磁盘与文件系统
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 磁盘管理
  - 文件系统
  - 运维
aliases:
  - Linux 磁盘与文件系统
  - Linux 文件系统与磁盘
source: 网络资料整理
---

# Linux磁盘与文件系统

> [!摘要]
> 本文聚焦 Linux 的磁盘与文件系统：从块设备、分区、inode、挂载等基础概念讲起，深入 ext4 / XFS / Btrfs 的核心机制，以及 LVM 与 mdadm 的组织方式，并给出可直接运行的分区、格式化、挂载、扩容与故障排查命令。版本基准为 2026-11 调研快照：块设备工具集 **util-linux 2.42.4**，内核主线 **7.3.5**，LTS **6.12 / 6.18**。定位是 [[Linux-从入门到精通]] 中「文件系统与目录结构」与「磁盘/LVM」两个环节的专项展开。

## 一、最新动态（截至 2026-11）

- **内核主线已进入 7.x 时代**：最新稳定版为 **7.3.5**（2026-11-16 由 Greg Kroah-Hartman 发布，同批发布 LTS **6.18.64**、**6.12.118**）。**7.3**（2026-10-18）明确包含 **Btrfs 性能优化**、存储 I/O 改进，并为 ksmbd 增加 Apple Time Machine 支持。
- **LTS 内核三支并行**：**6.18**（2025-11-30 首发，维护至 2028-12）、**6.12**（2024-11-17 首发，维护至 2028-12，Debian 13 / RHEL 10 系默认搭载）、**6.6**（维护至 2027-12）。教学与生产选型建议以发行版实际搭载的 LTS 版本为准。
- **块设备与挂载工具集**：`lsblk / fdisk / blkid / mount / swapon` 等均出自 **util-linux 2.42.4**（2026-09-26，Debian testing）。逻辑卷用 **LVM（lvm2）**，软 RAID 用 **mdadm**。
- **文件系统生态**：主流为 **ext4 / XFS / Btrfs**；**ZFS 不在主线内核**，需第三方模块。调研提示 6.18 周期存在 bcachefs / ReiserFS 等变更，正式使用前务必以 [kernel.org 文件系统文档](https://www.kernel.org/doc/html/latest/filesystems/) 官方目录核实，如无明确公告则写「以官方仓库为准」。
- **发行版侧影响**：openSUSE Leap 16.1（2026-11-02）引入 Immutable Mode 与事务更新，改变了根文件系统的管理方式；Debian 13.7 的 debian-installer 已将内核 ABI 提升到 6.12.107+deb13，与磁盘驱动、头文件兼容性相关。

## 二、基础概念

- **块设备（block device）**：以固定大小数据块（通常 512B 或 4KB）为单位读写的设备，如 `/dev/sda`、`/dev/nvme0n1`。文件系统就建立在块设备之上，用 `lsblk` 查看。
- **分区（partition）**：把一块物理盘切成多个逻辑区域，分区表有 MBR（上限 2TB、最多 4 个主分区）与 **GPT**（支持大容量、多分区）两种。`/dev/sda1` 表示 sda 的第 1 个分区。
- **inode（索引节点）**：文件系统的元数据载体，存储文件权限、属主、大小、时间戳与**数据块位置**。inode 数量在格式化时确定，用尽后即使磁盘还有空间也无法创建新文件。
- **数据块（block）**：文件数据实际存放的单元。文件系统通过 inode 的块指针把逻辑地址映射到磁盘物理地址。
- **挂载（mount）/ 卸载（umount）**：把文件系统接入根命名空间，让它在某个目录下可见。挂载点只是「入口」，文件系统本身与目录无关。
- **`/etc/fstab`**：开机自动挂载的声明表，格式为 `设备 挂载点 文件系统类型 选项 备份标记 检查顺序`。写错可能导致无法开机。
- **swap**：交换分区/文件，内存不足时作为虚拟内存，用 `swapon --show`、`free -h` 查看。
- **LVM 三层结构**：PV（物理卷，即分区）→ VG（卷组）→ LV（逻辑卷），支持在线扩容、快照与精简供给。
- **FHS 目录结构**：磁盘最终要落到目录树上，`/`、`/etc`、`/var`、`/home`、`/usr`、`/boot` 是挂载与容量规划的关键锚点（详见 [[Linux-从入门到精通]] 的目录速查表）。

## 三、核心机制

**ext4（通用默认）**
- 基于 inode + **extent**（连续数据块区间）组织文件，减少大文件的元数据开销。
- **日志（journaling）** 保证掉电一致性：`data=ordered` 默认只保证元数据落盘，`data=journal` 连数据也入日志（更稳但更慢）。
- 成熟稳定，适合通用系统与小到中等数据量；支持在线扩容，**不支持收缩**（`resize2fs` 只能增大）。

**XFS（大卷 / 数据库）**
- 采用分配组（Allocation Groups）并行读写，适合大文件与高并发 I/O，常见于数据库与容器宿主机。
- **不支持收缩**，只能单向扩容，且扩容依赖底层空间（`xfs_growfs` 把文件系统扩到设备边界）。

**Btrfs（快照 / 子卷）**
- **写时复制（COW）**：修改不覆盖原块，天然支持 **快照、子卷（subvolume）、send/receive**、压缩与去重。
- 可在文件系统内部做软 RAID（`btrfs raid1` 等），内核 7.3 已针对其性能做优化。日常校验用 `btrfs check`，不沿用传统 `fsck`。

**LVM 与 RAID**
- LVM 把多块 PV 聚合成 VG，再切 LV，扩容时只需 `lvextend`，对上层几乎无感；精简卷（thin）还能做快照与超配。
- mdadm 以软 RAID 提供冗余与吞吐：RAID1 镜像、RAID5/6 校验、RAID10 兼顾性能与可靠性。

## 四、实践步骤（含代码/命令示例）

### 4.1 查看磁盘与分区

```bash
lsblk -f                 # 列出块设备、分区表类型、文件系统与挂载点
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT
df -hT                   # 已用空间与文件系统类型
df -i                    # 检查 inode 使用率，防 inode 耗尽
findmnt /data            # 查看单个挂载点详情
```

### 4.2 分区与格式化

```bash
# 以 /dev/sdb 为例，创建单个主分区并写入分区表
fdisk /dev/sdb
# 交互命令序列：n -> p -> 1 -> 回车(默认起始) -> +100G -> w

# 大于 2TB 或需要 GPT 时改用 gdisk
gdisk /dev/sdb           # o 建 GPT，n 新建分区，w 写入

# 格式化为 ext4 / XFS / Btrfs（-F 允许对非空设备强制，-L 打卷标）
mkfs.ext4  -F -L data-ext4  /dev/sdb1
mkfs.xfs   -f -L data-xfs   /dev/sdb1
mkfs.btrfs -f -L data-btrfs /dev/sdb1

# 创建 swap
mkswap /dev/sdb2
swapon /dev/sdb2
```

### 4.3 挂载与开机自动挂载

```bash
mkdir -p /data
mount -t ext4 -o defaults,noatime /dev/sdb1 /data
findmnt /data                       # 验证挂载成功

# 写入 /etc/fstab 实现开机自动挂载（先备份，再测试）
cp /etc/fstab /etc/fstab.bak
echo '/dev/sdb1  /data  ext4  defaults,noatime  0  2' | tee -a /etc/fstab
mount -a                            # 关键：模拟开机挂载，检查语法是否正确

# 在线调整挂载选项（无需卸载）
mount -o remount,rw /data
mount -o remount,noatime /data
```

### 4.4 LVM 创建与扩容

```bash
# 创建：分区 -> PV -> VG -> LV -> 格式化 -> 挂载
pvcreate /dev/sdb1
vgcreate vg-data /dev/sdb1
lvcreate -n lv-data -L 50G vg-data
mkfs.ext4 /dev/vg-data/lv-data
mkdir -p /data && mount /dev/vg-data/lv-data /data

# 扩容：先扩 LV，再扩文件系统
lvextend -L +20G /dev/vg-data/lv-data
resize2fs /dev/vg-data/lv-data          # ext4 在线扩容
# xfs 用 xfs_growfs /data ，且只能扩到底层 PV 边界
```

### 4.5 软 RAID 与磁盘排查

```bash
# 软 RAID1（两块盘各一个分区）
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
mkfs.ext4 /dev/md0

# 磁盘健康与 I/O 排查
dmesg -T -l err,warn            # 内核日志中的 I/O 错误
smartctl -a /dev/sda            # SMART 健康信息
badblocks -nv /dev/sdb          # 坏块检测（谨慎：会破坏数据，先做备份）
iostat -xz 1 5                  # 磁盘利用率与等待时间
du -sh /* 2>/dev/null | sort -h   # 找出占空间最大的目录
```

## 五、最佳实践与常见坑

> [!warning] 写错 `/etc/fstab` 会进不了系统
> 挂载选项或设备名写错可能触发**开机进入紧急救援模式**。改动后务必先 `mount -a` 测试，再重启。可用 `rw,noauto` 或 `x-systemd.mount-timeout=` 降低风险；紧急恢复时用 `root=` 参数从 initramfs 挂载根分区。

- **格式化前确认设备**：`lsblk -f`、`blkid` 看清设备名与卷标，避免对挂载中的盘执行 `mkfs`。误格式化后用 `wipefs -l /dev/xxx` 查看残留签名，切勿继续写入。
- **inode 耗尽不等于磁盘满**：`df -i` 显示 100% 时，即使 `df -h` 还有空间也会报 No space left，常见于海量小文件目录。
- **XFS / ext4 都不能收缩**：扩容前先规划容量，缩小文件系统通常需要备份后重建，代价极高。
- **Btrfs 用专用工具**：`btrfs subvolume`、`btrfs snapshot`、`btrfs check`，不要用传统 `fsck.ext4` 之类工具检查。
- **RAID 不等于备份**：RAID 只解决可用性与局部损坏，误删、勒索、逻辑错误同样会同步到各盘，必须另做备份。
- **`mount -o remount` 不生效**：多数情况是因为该选项必须写在 `/etc/fstab` 中或由 systemd 重新挂载，检查选项是否被强制覆盖。
- **性能调优先定位再动手**：用 `iostat -xz`、`iostat -xz 1 5` 看 `%util` 与 `await`，用 `dmesg` 看错误，避免盲目调整读预取或挂载选项。

## 六、核心要点速查

| 目标 | 命令 |
|---|---|
| 查看块设备与文件系统 | `lsblk -f` |
| 查看挂载与容量 | `df -hT`、`findmnt` |
| 检查 inode | `df -i` |
| 分区 | `fdisk` / `gdisk` |
| 格式化 | `mkfs.ext4` / `mkfs.xfs` / `mkfs.btrfs` |
| 挂载 / 在线调整 | `mount` / `mount -o remount` |
| 开机挂载表 | `/etc/fstab`，改后 `mount -a` 验证 |
| LVM 扩容 | `lvextend` + `resize2fs` / `xfs_growfs` |
| 软 RAID | `mdadm --create /dev/md0 --level=1 --raid-devices=2 ...` |
| 磁盘健康排查 | `smartctl -a`、`badblocks`、`dmesg -T`、`iostat -xz` |

**选型口诀**：通用选 ext4，大卷高并发选 XFS，要快照/子卷选 Btrfs；多盘做冗余用 mdadm，跨盘灵活扩容用 LVM。

## 七、学习资源

1. [kernel.org 文件系统文档](https://www.kernel.org/doc/html/latest/filesystems/) —— 内核官方文件系统目录，核实 ext4/XFS/Btrfs 的官方状态与变更。
2. [kernel.org 发布页](https://www.kernel.org/releases.html) —— 主线与 LTS 内核版本、维护截止日。
3. [man7.org: lsblk(8)](https://www.man7.org/linux/man-pages/man8/lsblk.8.html) —— 块设备查看权威手册。
4. [man7.org: mount(8)](https://www.man7.org/linux/man-pages/man8/mount.8.html) —— 挂载、fstab 选项与 remount 细节。
5. [Debian Tracker: util-linux](https://tracker.debian.org/pkg/util-linux/news) —— fdisk/blkid/mount 等工具集的版本动态。
6. [systemd 官方手册](https://www.freedesktop.org/software/systemd/man/latest/) —— `systemd.mount` 与自动挂载行为，与 [[Linux-从入门到精通]] 的服务管理章节呼应。

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 体系中的主线定位与学习路线。

## 九、变更记录

- 2026-11-19：首次创建。
