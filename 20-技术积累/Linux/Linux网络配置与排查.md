---
title: Linux网络配置与排查
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 网络
  - 运维
  - 故障排查
aliases:
  - Linux网络
  - Linux 网络配置
source: 网络资料整理
---

# Linux网络配置与排查

> [!摘要] 内容与定位
> 本文聚焦 Linux 主机的网络**配置**与**排查**两条主线：从网卡、IP、路由、端口到 DNS、防火墙，给出可直接落地的命令与配置示例。网络问题遵循"链路层 → 网络层 → 传输/端口 → 应用"的分层定位逻辑，本文按此组织，配合 `iproute2`、`nftables`、`systemd-resolved` 等当前主流工具讲解。网络配置是系统管理的高频技能，也是容器、云服务器与运维自动化（见 [[Linux-从入门到精通]]）的必备基础。版本与动态均以 2026-11 调研快照为准，正式使用前请按来源 URL 复核。

## 一、最新动态（截至 2026-11）

- **网络配置工具集 iproute2 更新至 7.3.0**（Debian unstable，2026-10-25）：`ip/ss/tc/bridge/vlan` 等工具集为当前主流版本，`ss` 已全面取代传统 `netstat`。
- **包过滤框架 nftables 更新至 1.1.7**（2026-09，Debian unstable）：作为新一代防火墙框架，Podman 6.0 已改为 nftables 后端，不再支持 iptables。
- **Podman 6.0.1（2026-07-08）移除 CNI**：Netavark 成为唯一网络后端，并新增基于 nftables 的防火墙规则。Docker 的 iptables 示例不能直接套用到 Podman，容器网络需区分。
- **Docker Engine 29.9.2（2026-10-20）**、**containerd 2.4.2（2026-10-13）**：容器运行时持续升级，容器网络与镜像拉取的稳定性持续改善。
- **systemd 262（2026-09-22）**：对 `systemd-resolved` 的 **DNS-SD 注册行为有破坏性变更**——客户端断开后自动注销，常驻服务需用 `*.dnssd` 文件注册。这是 DNS 排障与 mDNS 场景必须注意的更新点。
- **发行版差异**：Ubuntu 26.04 LTS 搭载内核 7.0、systemd 259；Debian 13 使用 6.12 LTS 内核；Fedora 45 搭载内核 7.2、systemd 262。写网络配置示例时需按目标发行版区分 systemd 版本行为。

## 二、基础概念

**分层模型**：理解网络先建立分层心智——物理/链路层（网卡、MAC、VLAN）、网络层（IP、路由、网关）、传输层（TCP/UDP、端口）、应用层（DNS、HTTP 等）。排查时**自下而上**逐层排除，避免跳层乱猜。

**核心对象**：
- **网络接口（interface）**：如 `eth0`、`ens33`、`enp0s3`，是 IP 的载体；`ip link` 管理链路层，`ip addr` 管理网络层。
- **IP / 子网掩码 / 网关**：IP 标识主机，掩码决定网段，默认网关是跨网段通信的出口。
- **路由表（routing table）**：决定数据包"往哪走、怎么走"，是网络层核心。
- **端口与套接字（socket）**：传输层用端口区分服务，`ss` 可查看监听与连接。
- **DNS**：把域名解析为 IP，配置错误常表现为"能连通但打不开网页"。
- **防火墙**：包过滤层，决定哪些流量放行或丢弃。

**工具分层**：`iproute2` 管接口与路由，`ss` 看连接，`nftables`/`iptables` 做包过滤，`ufw`/`firewalld` 是上层封装，`systemd-resolved`/`resolvectl` 管 DNS，`tcpdump` 抓包。掌握工具归属，命令才不会用混。

## 三、核心机制

**内核协议栈与 Netlink**：网卡数据经驱动进入内核协议栈，`ip` 命令通过 **RTNL（Netlink 路由接口）** 与内核通信，实时修改接口、路由和策略，无需重启服务。这也是临时配置重启后丢失的原因——临时配置只存在于内存中。

**路由选择**：路由表按"最长前缀匹配"选路。默认路由（`default via ...`）处理所有未命中网段的流量；`ip rule` 可定义基于源地址、TOS 的策略路由，实现多出口分流。

**连接跟踪与 NAT**：`conntrack` 维护连接状态（NEW/ESTABLISHED/RELATED），有状态防火墙据此放行回程流量。NAT（`SNAT`/`DNAT`）实现内网共享出口与端口映射（`iptables -t nat` 或 `nft` 等价规则），是端口转发、容器出网的基础。

**防火墙与状态**：现代防火墙默认**有状态**，只需放行入站服务端口，回程流量自动放行。规则应尽量精确到端口与源地址，避免 `0.0.0.0/0` 全开。

**容器网络命名空间**：容器通过独立的 `net` namespace 隔离网络，通过 `veth` 对与网桥相连，出网经 NAT。理解命名空间是解释"容器内能通、宿主机不通"这类问题的关键。

## 四、实践步骤（含代码/命令示例）

### 4.1 查看接口、IP 与路由

```bash
# 查看所有接口及 IP（iproute2 7.3.0）
ip addr show
ip -br addr

# 查看链路状态与统计
ip link show

# 查看路由表与默认网关
ip route
ip route show default

# 查看连接与监听端口（ss 已取代 netstat）
ss -tulpn          # -t TCP -u UDP -l 监听 -p 进程 -n 不解析
ss -s              # 连接统计概览
```

### 4.2 配置静态 IP 与 DHCP

临时配置（重启失效，适合快速验证）：

```bash
# 临时配置 IP 与默认路由
sudo ip addr add 192.168.1.10/24 dev eth0
sudo ip route add default via 192.168.1.1
```

持久化配置按发行版不同。Ubuntu 使用 **netplan**（YAML）：

```yaml
# /etc/netplan/01-netcfg.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses: [192.168.1.10/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [114.114.114.114, 8.8.8.8]
```

```bash
sudo netplan apply          # 应用配置
netplan try                 # 校验并尝试应用，出错自动回滚
```

RHEL/Fedora 使用 **NetworkManager**：

```bash
sudo nmcli con add type ethernet ifname eth0 con-name my-static \
  ipv4.method manual ipv4.addresses 192.168.1.10/24 \
  ipv4.gateway 192.168.1.1 ipv4.dns "114.114.114.114"
sudo nmcli con up my-static
nmcli con show              # 查看连接
```

### 4.3 连通性与路由排查

```bash
ping -c 4 8.8.8.8           # 网络层连通性
ping -c 4 example.com       # 顺带验证 DNS
traceroute 8.8.8.8          # 逐跳路径
mtr -n -c 20 8.8.8.8        # 结合 ping 与 traceroute，看丢包在哪一跳
ip route get 8.8.8.8        # 查看到目标实际命中的路由规则
```

### 4.4 端口与服务排查

```bash
ss -tulpn | grep :80        # 看 80 端口是否有进程监听
ss -tnp state established   # 看已建立连接及对应进程
sudo ss -tulpn              # 需 root 才能看到完整进程名
```

### 4.5 DNS 排查

```bash
resolvectl status           # 查看 systemd-resolved 状态（systemd 262 可用）
resolvectl dns               # 只看当前生效的 DNS 服务器
dig example.com @114.114.114.114   # 指定 DNS 查询
dig +short example.com      # 精简输出
cat /etc/resolv.conf        # 查看解析器配置（可能由 resolved 生成）
```

> [!warning] systemd-resolved 接管 `/etc/resolv.conf`
> 启用 resolved 后，`/etc/resolv.conf` 通常是指向 `127.0.0.53` 的**桩文件**，直接改写会被覆盖。应通过 `resolvectl` 或 netplan/NetworkManager 的 DNS 配置修改，否则容易"改了没生效"。

### 4.6 防火墙配置

nftables 直接查看规则集：

```bash
sudo nft list ruleset                 # 查看当前全部规则
sudo nft add rule inet filter input type filter hook input priority 0 \
  tcp dport 22 ct state established,related accept
sudo nft list table inet filter       # 查看表与链
```

firewalld（RHEL 系封装）：

```bash
sudo firewall-cmd --list-all          # 查看当前区域规则
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload
```

ufw（Debian/Ubuntu 封装）：

```bash
sudo ufw status verbose
sudo ufw allow 22/tcp
sudo ufw enable
```

### 4.7 抓包定位

```bash
# 监听 eth0 上 80 端口的 TCP 包，输出可读时间戳
sudo tcpdump -i eth0 -nn 'tcp port 80' -c 20

# 查看内核网络统计，定位丢包/错包
ip -s link show eth0
```

### 4.8 端口转发（NAT）

```bash
# 将本机 8080 转发到内网 192.168.1.20 的 80 端口
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 \
  -j DNAT --to-destination 192.168.1.20:80
sudo iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j MASQUERADE
```

## 五、最佳实践与常见坑

- **分层排查，自下而上**：先确认链路（`ip link`、网卡灯/VLAN）→ 再 IP 与路由（`ip addr`、`ip route`、`ping`）→ 再端口与防火墙（`ss`、`nft`）→ 最后应用。跳层排查最耗时。
- **改防火墙前先备份**：`sudo nft list ruleset > /tmp/nft-backup.nft`，误锁后可快速还原；远程操作时务必保留一条已放行的 SSH 规则，防止把自己锁在门外。
- **区分临时配置与持久配置**：`ip addr add` 等只改内存，重启失效。生产环境务必用 netplan / NetworkManager / systemd-networkd 持久化，避免"重启后网络不通"。
- **`/etc/resolv.conf` 被托管**：启用 `systemd-resolved` 或 NetworkManager 后，直接编辑该文件可能无效或被覆盖，改 DNS 要走正确的配置入口。
- **容器网络不能套用 Docker 规则**：Podman 6.0 已移除 CNI、仅支持 Netavark + nftables，Docker 的 iptables 示例在 Podman 上不成立。
- **MTU 与 VLAN 不匹配**：MTU 不一致会导致"能 ping 通但大包/HTTP 不通"，用 `ping -M do -s` 探测；VLAN 配置错误会让接口直接掉链路。
- **先验证再放行**：排查端口问题时，可临时用 `iptables -I INPUT -j ACCEPT` 放行验证，确认后再替换为精确规则，避免长期全开。
- **SSH 加固与端口暴露**：对外服务只开放必要端口，SSH 建议禁用密码登录、改用密钥，并配合 fail2ban 防暴力破解。

## 六、核心要点速查

| 场景 | 命令 |
|---|---|
| 查看接口与 IP | `ip -br addr` |
| 查看路由 | `ip route` / `ip route show default` |
| 查看监听端口 | `ss -tulpn` |
| 连接统计 | `ss -s` |
| 连通性 | `ping` / `traceroute` / `mtr -n -c 20 <ip>` |
| 查看 DNS 状态 | `resolvectl status` |
| DNS 查询 | `dig example.com` |
| 防火墙规则 | `nft list ruleset` / `firewall-cmd --list-all` / `ufw status` |
| 抓包 | `sudo tcpdump -i eth0 -nn 'tcp port 80'` |
| 内核网络统计 | `ip -s link show eth0` |
| 应用配置 | `netplan apply` / `nmcli con up <name>` |

## 七、学习资源

1. [iproute2 在 Debian 的发布动态（iproute2 7.3.0）](https://tracker.debian.org/pkg/iproute2/news) —— 网络工具集版本来源
2. [nftables 在 Debian 的发布动态（nftables 1.1.7）](https://tracker.debian.org/pkg/nftables/news) —— 新一代包过滤框架
3. [man7.org: ip(8) 手册](https://www.man7.org/linux/man-pages/man8/ip.8.html) —— `ip` 命令权威手册
4. [systemd-resolved 官方手册](https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.html) —— DNS 管理与 systemd 262 变更
5. [kernel.org 官方内核与版本发布页](https://www.kernel.org/category/releases.html) —— 内核版本与网络相关变更
6. [Docker Engine 29.x 发布说明](https://docs.docker.com/engine/release-notes/29/) —— 容器网络运行时版本
7. [containerd v2.4.2 发布页](https://github.com/containerd/containerd/releases/tag/v2.4.2) —— 容器运行时更新

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习体系中的位置与路线
- [[Linux常用命令集]] —— 高频网络与系统命令速查
- [[Linux系统管理与运维要点]] —— 网络配置在生产运维中的综合展开
- [[网络基础概念]] —— 分层模型与协议的前置理论

## 九、变更记录

- 2026-11-19：首次创建。
