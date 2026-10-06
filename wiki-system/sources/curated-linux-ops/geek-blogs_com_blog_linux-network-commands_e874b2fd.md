---
source: "https://geek-blogs.com/blog/linux-network-commands"
title: "Linux 网络命令详解：从基础到高级应用指南 — geek-blogs.com"
fetched_at: "2026-10-06 12:36"
---

## 目录#

  1. 基础网络接口管理：ifconfig 与 ip
  2. 网络连通性测试：ping
  3. 路径追踪：traceroute 与 tracepath
  4. 端口与连接监控：netstat 与 ss
  5. DNS 查询工具：nslookup 与 dig
  6. HTTP/HTTPS 工具：curl 与 wget
  7. 防火墙管理：iptables
  8. 数据包捕获：tcpdump
  9. 路由表管理：route 与 ip route
  10. 主机名管理：hostname 与 hostnamectl
  11. ARP 缓存管理：arp
  12. 综合网络诊断：mtr
  13. 最佳实践总结
  14. 参考资料



## 1\. 基础网络接口管理：ifconfig 与 ip#

### 1.1 背景与对比#

`ifconfig` 是传统的网络接口配置命令，但已逐渐被 `ip` 命令（来自 `iproute2` 工具包）取代。`ip` 命令功能更强大，支持 IPv6、VLAN、隧道等高级特性，且输出更规范。建议优先使用 `ip`。

### 1.2 `ip` 命令核心用法#

#### 查看所有网络接口信息#
    
    
    ip addr show  # 缩写：ip a

输出示例：
    
    
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 00:16:3e:xx:xx:xx brd ff:ff:ff:ff:ff:ff
        inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
           valid_lft forever preferred_lft forever
    

#### 启用/禁用接口#
    
    
    ip link set eth0 up   # 启用接口 eth0
    ip link set eth0 down # 禁用接口 eth0

#### 配置 IP 地址#

临时分配 IPv4 地址（重启后失效）：
    
    
    ip addr add 192.168.1.200/24 dev eth0  # 添加 IP
    ip addr del 192.168.1.200/24 dev eth0  # 删除 IP

永久配置需修改网络配置文件（因发行版而异）：

  * **Debian/Ubuntu** ：`/etc/netplan/*.yaml`
  * **CentOS/RHEL** ：`/etc/sysconfig/network-scripts/ifcfg-eth0`



### 1.3 `ifconfig` 命令（兼容性说明）#

若需兼容旧系统，`ifconfig` 仍可使用：
    
    
    ifconfig eth0          # 查看接口 eth0 信息
    ifconfig eth0 192.168.1.200 netmask 255.255.255.0  # 配置 IP

## 2\. 网络连通性测试：ping#

### 2.1 功能与原理#

`ping` 通过发送 ICMP 回显请求（Echo Request）测试目标主机的可达性，基于 ICMP 协议（需目标主机允许 ICMP 入站）。

### 2.2 常用选项与示例#
    
    
    ping -c 4 google.com  # 发送 4 个数据包后停止（-c：count）
    ping -i 2 -c 5 192.168.1.1  # 每 2 秒发送 1 个包，共 5 个（-i：interval）
    ping -s 1024 baidu.com  # 发送 1024 字节的数据包（-s：packet size）
    ping -n 114.114.114.114  # 禁用域名解析，直接显示 IP（-n：numeric）

**输出解析** ：关注 `time`（往返延迟，单位 ms）和 `packet loss`（丢包率），丢包率高通常表示网络不稳定。

### 2.3 注意事项#

  * 部分服务器/网络会禁用 ICMP（如阿里云 ECS 默认禁 ping），此时 `ping` 会返回超时。
  * IPv6 测试需使用 `ping6` 或 `ping -6`。



## 3\. 路径追踪：traceroute 与 tracepath#

### 3.1 功能对比#

  * `traceroute`：显示数据包从本地到目标主机经过的路由节点（跳数），支持 TCP/UDP/ICMP 协议。
  * `tracepath`：轻量级替代工具，无需 root 权限，默认使用 UDP，但功能较少。



### 3.2 `traceroute` 常用选项#
    
    
    traceroute google.com  # 默认使用 UDP 端口 33434
    traceroute -T -p 80 baidu.com  # 使用 TCP 协议，目标端口 80（-T：TCP）
    traceroute -I 192.168.1.1  # 使用 ICMP 协议（模拟 ping 的路径追踪）
    traceroute -n github.com  # 禁用域名解析，仅显示 IP

**输出解析** ：每行代表一个路由节点，包含跳数、节点 IP（或域名）、三次往返延迟（若超时显示 `*`）。

### 3.3 `tracepath` 示例#
    
    
    tracepath www.taobao.com  # 无需 root，适合普通用户使用

## 4\. 端口与连接监控：netstat 与 ss#

### 4.1 功能对比#

  * `netstat`：传统工具，功能全面但性能较差（尤其在高连接数场景）。
  * `ss`（Socket Statistics）：`iproute2` 套件工具，基于内核哈希表，速度快、资源占用低，推荐优先使用。



### 4.2 `ss` 核心用法#
    
    
    ss -tuln  # 列出所有监听的 TCP/UDP 端口（-t：TCP，-u：UDP，-l：listening，-n：numeric）
    ss -tulnp  # 显示监听端口对应的进程（需 root，-p：process）
    ss -an | grep ESTAB  # 查看所有已建立的连接（-a：all）
    ss -o state TIME-WAIT  # 查看 TIME-WAIT 状态的 TCP 连接（-o：显示定时器）

**示例输出** ：
    
    
    State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
    LISTEN     0      128          0.0.0.0:22                      0.0.0.0:*                   users:(("sshd",pid=1234,fd=3))
    ESTAB      0      52       192.168.1.100:22                103.xx.xx.xx:54321            timer:(keepalive,10min,0)
    

### 4.3 `netstat` 兼容性示例#
    
    
    netstat -tuln  # 等价于 ss -tuln
    netstat -anp | grep 8080  # 查找端口 8080 对应的进程

## 5\. DNS 查询工具：nslookup 与 dig#

### 5.1 功能对比#

  * `nslookup`：传统 DNS 查询工具，语法简单，适合快速查询。
  * `dig`（Domain Information Groper）：功能更强大，支持 DNS 记录类型（A、AAAA、CNAME、MX 等）、高级查询选项，输出更详细。



### 5.2 `dig` 常用示例#
    
    
    dig google.com  # 查询 A 记录（默认），输出完整 DNS 响应
    dig +short baidu.com  # 仅显示简化结果（IP 地址）
    dig google.com MX  # 查询 MX 记录（邮件服务器）
    dig @8.8.8.8 github.com  # 指定 DNS 服务器（8.8.8.8 为 Google DNS）
    dig +trace www.qq.com  # 追踪 DNS 解析过程（从根域到权威服务器）

### 5.3 `nslookup` 示例#
    
    
    nslookup google.com  # 基础查询
    nslookup -type=MX qq.com  # 查询 MX 记录
    nslookup github.com 114.114.114.114  # 使用 114 DNS 服务器查询

## 6\. HTTP/HTTPS 工具：curl 与 wget#

### 6.1 功能对比#

  * `curl`：支持 HTTP/HTTPS/FTP 等协议，可发送请求、获取响应头、提交数据，更适合接口调试。
  * `wget`：专注于文件下载，支持断点续传、后台下载，适合批量下载场景。



### 6.2 `curl` 实用示例#
    
    
    curl http://example.com  # 获取网页内容并打印到终端
    curl -I https://www.baidu.com  # 仅获取响应头（-I：head）
    curl -X POST -d "username=test&pass=123" http://api.example.com/login  # POST 表单数据
    curl -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com  # POST JSON 数据
    curl -O https://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso  # 下载文件（-O：保留原文件名）

### 6.3 `wget` 实用示例#
    
    
    wget https://example.com/file.zip  # 下载文件
    wget -c http://largefile.iso  # 断点续传（-c：continue）
    wget -b ftp://ftp.example.com/bigdata.tar.gz  # 后台下载（-b：background）
    wget -r -np -k https://docs.docker.com  # 递归下载整个网站（-r：recursive，-np：不跳转父目录，-k：修复链接）

## 7\. 防火墙管理：iptables#

### 7.1 功能与核心概念#

`iptables` 是 Linux 内核防火墙工具，基于规则集过滤网络流量。核心概念：

  * **链（Chain）** ：预定义规则集合，如 `INPUT`（入站流量）、`OUTPUT`（出站流量）、`FORWARD`（转发流量）。
  * **规则（Rule）** ：匹配条件（如协议、端口、IP）+ 动作（`ACCEPT` 允许、`DROP` 丢弃、`REJECT` 拒绝并返回错误）。



### 7.2 常用操作示例#
    
    
    iptables -L  # 查看所有规则（默认显示 INPUT/OUTPUT/FORWARD 链）
    iptables -L -n  # 禁用域名解析，显示 IP（更清晰）
     
    # 允许 SSH 入站连接（TCP 22 端口）
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT  # -A：追加规则到链尾
     
    # 允许 HTTP/HTTPS 入站（80/443 端口）
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT
     
    # 拒绝来自特定 IP 的入站流量
    iptables -A INPUT -s 192.168.1.10 -j DROP  # -s：源 IP
     
    # 删除规则（需先通过 iptables -L --line-numbers 查看规则序号）
    iptables -D INPUT 3  # 删除 INPUT 链中第 3 条规则
     
    # 保存规则（临时规则重启后失效，需持久化）
    iptables-save > /etc/iptables.rules  # 保存到文件
    iptables-restore < /etc/iptables.rules  # 恢复规则

### 7.3 最佳实践#

  * 生产环境建议使用 `ufw`（Uncomplicated Firewall）或 `firewalld`（CentOS 7+）简化 `iptables` 管理，例如 `ufw allow 22/tcp` 等效于上述 SSH 规则。
  * 规则变更前先备份当前规则（`iptables-save > backup.rules`），避免误操作导致断网。



## 8\. 数据包捕获：tcpdump#

### 8.1 功能与用途#

`tcpdump` 是命令行数据包捕获工具，可实时抓取网络接口上的流量，常用于网络故障排查（如丢包、延迟、异常请求）。

### 8.2 核心选项与示例#
    
    
    tcpdump -i eth0  # 抓取 eth0 接口的所有数据包（默认）
    tcpdump -i any port 80  # 抓取所有接口的 80 端口流量（-i any：所有接口）
    tcpdump -n host 192.168.1.100  # 抓取与 192.168.1.100 相关的流量（-n：禁用域名解析）
    tcpdump -c 100 -w capture.pcap  # 抓取 100 个数据包后保存到文件（-w：write）
    tcpdump -r capture.pcap  # 读取保存的数据包文件（-r：read）
    tcpdump -i eth0 'tcp and port 443 and src host 203.0.113.1'  # 复杂过滤：TCP 443 端口且源 IP 为 203.0.113.1

**输出解析** ：每行代表一个数据包，包含时间戳、源 IP:端口、目标 IP:端口、协议及数据摘要。

### 8.3 注意事项#

  * 需 root 权限（`sudo tcpdump`）。
  * 高流量场景下，`tcpdump` 可能导致服务器负载升高，建议限制抓取数量（`-c`）或过滤条件。



## 9\. 路由表管理：route 与 ip route#

### 9.1 功能对比#

  * `route`：传统路由表管理工具，仅支持 IPv4。
  * `ip route`：`iproute2` 套件工具，支持 IPv4/IPv6，功能更全面。



### 9.2 `ip route` 常用操作#
    
    
    ip route show  # 查看路由表（缩写：ip r）
    ip route add default via 192.168.1.1 dev eth0  # 添加默认网关（via：网关 IP，dev：出口接口）
    ip route add 10.0.0.0/8 via 172.16.0.1 dev eth1  # 添加静态路由：访问 10.0.0.0/8 网段走 eth1 接口
    ip route del 192.168.2.0/24  # 删除指定路由
    ip route get 8.8.8.8  # 查看访问 8.8.8.8 的路由路径（通过哪个网关/接口）

### 9.3 `route` 兼容性示例#
    
    
    route -n  # 查看路由表（-n：禁用域名解析）
    route add default gw 192.168.1.1  # 添加默认网关

## 10\. 主机名管理：hostname 与 hostnamectl#

### 10.1 功能对比#

  * `hostname`：查看/临时修改主机名（重启后失效）。
  * `hostnamectl`：systemd 工具，支持永久修改主机名（推荐）。



### 10.2 操作示例#
    
    
    hostname  # 查看当前主机名
    hostnamectl set-hostname web-server-01  # 永久修改主机名（立即生效，无需重启）
    hostnamectl status  # 查看主机名及系统信息

**永久生效验证** ：修改后 `/etc/hostname` 文件内容会同步更新。

## 11\. ARP 缓存管理：arp#

### 11.1 功能#

ARP（地址解析协议）用于将 IP 地址映射到 MAC 地址，`arp` 命令管理本地 ARP 缓存表。

### 11.2 常用操作#
    
    
    arp -a  # 查看 ARP 缓存（显示 IP 与 MAC 的对应关系）
    arp -n  # 禁用域名解析，仅显示 IP
    arp -d 192.168.1.1  # 删除指定 IP 的 ARP 记录
    arp -s 192.168.1.2 00:11:22:33:44:55  # 手动添加静态 ARP 记录（-s：set）

**应用场景** ：当局域网内 IP 冲突或 ARP 欺骗时，可通过 `arp -d` 清除错误记录。

## 12\. 综合网络诊断：mtr#

### 12.1 功能#

`mtr`（My Traceroute）整合了 `ping` 和 `traceroute` 的功能，实时显示每个路由节点的丢包率和延迟，更适合长时间监控网络稳定性。

### 12.2 常用示例#
    
    
    mtr google.com  # 基本模式，实时更新各节点状态
    mtr -n --report baidu.com  # 禁用域名解析，运行后生成汇总报告（--report）
    mtr -T -p 443 github.com  # 使用 TCP 协议测试 443 端口

**输出解析** ：重点关注 `Loss%`（丢包率）和 `Avg`（平均延迟），某节点丢包率突增通常表示该节点存在网络瓶颈。

## 13\. 最佳实践总结#

  1. **优先使用现代工具** ：用 `ip` 替代 `ifconfig`，`ss` 替代 `netstat`，`dig` 替代 `nslookup`。
  2. **限制`ping` 测试次数**：避免无限制发送数据包（如 `ping -c 4`）。
  3. **`tcpdump` 过滤与安全**：抓取流量时，通过端口、IP 过滤减少无关数据；敏感场景下，抓取文件需加密存储。
  4. **`iptables` 规则备份**：修改防火墙规则后，立即用 `iptables-save > /etc/iptables.rules` 备份，防止重启丢失。
  5. **DNS 缓存清理** ：若 DNS 解析异常，可尝试清理本地缓存（`systemctl restart systemd-resolved` 或 `nscd -i hosts`）。
  6. **权限控制** ：`tcpdump`、`iptables` 等命令需 root 权限，避免直接使用 `root` 用户，建议通过 `sudo` 执行。
  7. **文档化网络配置** ：记录静态 IP、路由、防火墙规则等变更，便于后续维护。



## 14\. 参考资料#

  * [Linux 手册页](https://man7.org/linux/man-pages/index.html)：`man ping`、`man ip` 等命令的权威文档。
  * [iproute2 官方文档](https://wiki.linuxfoundation.org/networking/iproute2)：深入理解 `ip` 命令。
  * [Iptables HowTo](https://www.netfilter.org/documentation/HOWTO/packet-filtering-HOWTO.html)：Netfilter/Iptables 官方指南。
  * [TCPDUMP: Detailed Examples](https://danielmiessler.com/study/tcpdump/)：`tcpdump` 高级过滤示例。



通过本文的梳理，相信你已掌握 Linux 网络命令的核心用法。实际应用中，需结合具体场景灵活选择工具，例如排查端口占用用 `ss -tulnp`，诊断域名解析用 `dig`，网络故障追踪用 `mtr`。持续实践与总结，才能真正提升网络管理能力。

[2025-11](/tag/2025-11/)
