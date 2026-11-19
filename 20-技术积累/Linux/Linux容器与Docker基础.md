---
title: Linux容器与Docker基础
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 容器
  - Docker
  - 运维
aliases:
  - Docker入门
  - Linux容器基础
source: 网络资料整理
---

# Linux容器与Docker基础

> [!摘要]
> 本篇是 [[Linux-从入门到精通]] 体系「阶段四：精通」中容器底层机制的落地篇，聚焦**容器到底是什么、Docker 如何工作、日常怎么用、生产怎么避坑**。核心结论：容器不是"轻量级虚拟机"，而是**内核 namespace（隔离）+ cgroup v2（限额）+ 联合文件系统（镜像分层）**三项能力的工程封装；Docker 是这套能力的用户侧入口，底层由 containerd/runc 协作完成。版本基准（截至 2026-11-19 调研）：Docker Engine **29.9.2**、containerd **2.4.2**、Podman **6.0.1**、systemd **262**。

## 一、最新动态（截至 2026-11）

以下版本号均来自 2026-11-19 调研文件，正式引用前请回查官方发布说明。

- **Docker Engine 29.x 推进至 29.9.2**（2026-10-20）：29.x 最新补丁版，含 Go 运行时安全修复与 containerd 升级。官方发布说明见 [Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)。
- **containerd 2.4.2**（2026-10-13）：CRI 日志不再跟随符号链接、修复镜像拉取内存占用问题、默认 seccomp 白名单加固。见 [containerd v2.4.2 Release](https://github.com/containerd/containerd/releases/tag/v2.4.2)。
- **Podman 6.0.1**（2026-07-08）：**移除 CNI**，Netavark 成为唯一网络后端；新增基于 nftables 的防火墙规则（不再支持 iptables）；配置默认迁移至 `/usr/share/containers`。见 [Debian 1143118 变更记录](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1143118)。
- **内核支撑面**：容器依赖 namespaces 与 cgroup。**cgroup v2 已成为默认**，Ubuntu 26.04 LTS 已移除 cgroup v1；systemd **262** 可构建单一静态链接的 PID 1，便于极小容器直接以 systemd 作为 init，配合 `systemd-nspawn`、`systemd-container` 使用。见 [systemd Releases](https://github.com/systemd/systemd/releases)。

> [!warning] 时效性提示
> 以上为 2026-11 快照。内核小版本、Docker/Podman 补丁号迭代极快，生产选型前务必按官方仓库复核最新版本号；查不到的一律写「以官方仓库为准」。

## 二、基础概念

### 2.1 容器的本质

容器是**共享宿主内核的进程隔离环境**，不是虚拟机：没有独立的内核，不经过 Hypervisor，因此启动快、开销低。它的"隔离"来自内核的三样能力：

| 能力 | 内核机制 | 解决什么问题 |
|---|---|---|
| 隔离 | **namespaces** | 让每个容器看到独立的 PID、网络、挂载、用户、IPC 视图 |
| 限额 | **cgroups v2** | 限制 CPU、内存、IO、PID 等资源上限，防止单个容器耗尽宿主 |
| 打包 | 联合文件系统（**overlay2** 等） | 把只读镜像层 + 可写容器层叠加，实现镜像分层与可写层 |

加上 **capabilities**（能力集裁剪）与 **seccomp**（系统调用白名单），共同构成容器的安全边界。

### 2.2 容器 vs 虚拟机

| 维度 | 容器 | 虚拟机 |
|---|---|---|
| 内核 | 共享宿主内核 | 每个 VM 独立内核 |
| 启动速度 | 秒级 | 分钟级 |
| 隔离强度 | 进程级（相对弱） | 硬件级（强） |
| 资源占用 | MB 级 | GB 级 |
| 典型用途 | 应用打包与交付 | 强隔离、多操作系统 |

### 2.3 Docker 是什么

Docker 是**容器运行时的用户侧工具集**，提供镜像构建、拉取、运行、编排的统一命令。它本身不是内核功能，而是对 namespace/cgroup/overlay 等能力的封装。完整分层：

```text
用户命令（docker CLI）
      ↓
Docker Engine（守护进程 dockerd：镜像管理、容器编排、网络）
      ↓
containerd（镜像/容器生命周期管理）
      ↓
runc（基于 Linux 系统调用，真正创建/运行容器）
      ↓
内核：namespaces + cgroups v2 + overlay2
```

### 2.4 关键名词

- **镜像（Image）**：只读、分层、可复用的模板，一个镜像由多个只读层叠加而成。
- **容器（Container）**：镜像之上加一层可写层后运行的实例。
- **仓库（Registry）**：存放和分发镜像的服务，如 [Docker Hub](https://hub.docker.com/)、[Quay.io](https://quay.io/)。
- **OCI**：开放容器倡议，规定镜像格式与运行时标准，Docker、Podman、containerd 均遵循。

## 三、核心机制

### 3.1 namespaces：隔离的基石

`unshare` 或容器启动时，内核为容器创建一组 namespace，每个 namespace 隔离一类全局资源视图：

```bash
# 列出当前进程所属的各类 namespace（数字即 namespace ID）
ls -l /proc/self/ns/

# 查看所有 namespace 类型
# 容器内 /proc/self/ns 与宿主的对应项不同，即"隔离"
ls -l /proc/1/ns/          # 容器内 PID 1 的视角
```

常用 namespace 类型：`PID`（进程）、`NET`（网络）、`MNT`（挂载）、`UTS`（主机名/域名）、`IPC`（进程间通信）、`USER`（用户与 UID 映射）。

### 3.2 cgroups v2：资源限额

cgroup v2 统一挂载在 `/sys/fs/cgroup`，通过**子树控制**限制资源：

```bash
# 查看当前 cgroup 层级与控制器
cat /sys/fs/cgroup/cgroup.controllers
cat /proc/self/cgroup

# 限制某进程内存上限（示例：写入内存子系统的 max）
echo "$MAX_MEM" > /sys/fs/cgroup/<group>/memory.max
```

> [!info] 版本提示
> Ubuntu 26.04 LTS 已移除 cgroup v1，容器运行时与监控工具需按 cgroup v2 编写；cgroup v1 的 `/sys/fs/cgroup/memory/` 等路径已不适用。

### 3.3 镜像分层与 overlay2

镜像分层让镜像可复用、可增量拉取。overlay2 将多层只读目录与一层可写目录叠加为统一视图：

```bash
# 查看镜像的层结构（每行一层）
docker history nginx:latest

# 查看容器可写层与挂载信息
docker inspect <container> --format '{{.GraphDriver.Data}}'
```

### 3.4 systemd 与容器

systemd **262** 支持构建单一静态 PID 1，可在极小容器内以 systemd 为 init，接管服务生命周期；`systemd-nspawn` 可直接把一个目录"装进"容器运行：

```bash
# 用 systemd-nspawn 启动一个容器
systemd-nspawn -D /var/lib/machines/demo --bind=/tmp/data:/data /bin/bash

# 查看 systemd 对容器的支持能力
systemd-nspawn --help | head -40
```

## 四、实践步骤（含代码/命令示例）

### 4.1 安装与版本确认

```bash
# 确认 Docker Engine 版本（应为 29.x）
docker version
docker info | grep -Ei 'server version|storage driver|cgroup'

# 查看 containerd / runc 版本
ctr version
runc --version

# 无 Docker 时使用 Podman（命令兼容子集）
podman --version        # 应为 6.0.x
```

### 4.2 拉取、运行、交互

```bash
# 拉取镜像
docker pull nginx:latest

# 后台运行并映射端口、挂载目录
docker run -d --name web \
  -p 8080:80 \
  -v /opt/html:/usr/share/nginx/html:ro \
  nginx:latest

# 进入容器执行命令
docker exec -it web /bin/bash

# 查看容器状态与日志
docker ps -a
docker logs --tail 100 web
```

### 4.3 构建镜像（Dockerfile）

```dockerfile
# Dockerfile：基于官方镜像，安装工具并启动
FROM nginx:1.27-alpine

RUN apk add --no-cache curl
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# 构建并打标签
docker build -t myapp:1.0 .

# 运行并验证
docker run -d --name app -p 8080:80 myapp:1.0
curl http://127.0.0.1:8080
```

### 4.4 使用 Docker Compose 编排多容器

```yaml
# docker-compose.yml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    depends_on:
      - api

  api:
    image: myapp:1.0
    environment:
      - DB_HOST=db
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
```

```bash
docker compose up -d
docker compose ps
docker compose logs -f api
docker compose down        # 停止并清理
```

### 4.5 不使用 Docker 时的容器命令

```bash
# Podman 兼容替代（Docker 系命令大多可直接替换为 podman）
podman run -d --name web -p 8080:80 nginx:latest
podman exec -it web /bin/bash
podman compose up -d

# 直接操作 containerd（容器运行时层）
ctr images ls
ctr run --rm --env KEY=val docker.io/library/nginx:latest nginx-ctr

# Kubernetes 场景下排查 Pod 的运行时
crictl ps
crictl inspect <container-id>
```

## 五、最佳实践与常见坑

> [!tip] 镜像与容器
> - **镜像要小**：优先用 `alpine`/`slim` 基础镜像，多阶段构建，避免把调试工具留在生产镜像。
> - **标签要固定**：生产用明确版本或摘要（`nginx:1.27-alpine`），不用 `latest`，避免不可复现。
> - **用 `:ro` 只读挂载配置目录**，防止容器内进程误改宿主文件。
> - **镜像分层顺序按变动频率从低到高排列**，最大化利用构建缓存。

> [!warning] 网络与安全
> - **Podman 6 已移除 CNI、仅用 Netavark + nftables**，Docker 的 iptables 示例不能直接套用到 Podman，网络排查命令要分清后端。
> - **不要用 `--privileged` 跑生产容器**：它等于给了容器接近宿主 root 的能力，应改用最小 `capabilities` 与 seccomp profile。
> - **容器内默认不是 root 更安全**：镜像里创建非特权用户，用 `USER` 指令切换。
> - **端口映射是 NAT，不是真正的公网暴露**，暴露服务需结合防火墙（nftables/ufw/firewalld）与反向代理。

> [!danger] 常见坑
> - **`docker run` 后容器退出**：先看 `docker logs`，多半是前台进程结束或配置错误；用 `docker run --rm -it <img> /bin/bash` 进去排查。
> - **端口冲突**：宿主端口被占用时 `docker run` 会报错，用 `ss -tulpn` 查占用进程后再换端口。
> - **数据丢失**：容器文件系统是临时的，`docker rm` 即删除；持久数据必须用 `-v`/`--mount` 挂载到宿主。
> - **cgroup 版本差异**：在 Ubuntu 26.04 等已移除 cgroup v1 的系统上，旧脚本读取 `/sys/fs/cgroup/memory/` 会失败，统一走 cgroup v2 的 `/sys/fs/cgroup/<group>/memory.max`。
> - **时区与 DNS**：容器内常缺时区与 DNS，`docker run -e TZ=Asia/Shanghai -e DNS=8.8.8.8` 或在镜像里配置 `/etc/resolv.conf`。

## 六、核心要点速查

| 主题 | 关键命令 / 事实 |
|---|---|
| 隔离 | namespaces（`PID/NET/MNT/UTS/IPC/USER`），看 `/proc/self/ns/` |
| 限额 | cgroup v2，路径 `/sys/fs/cgroup`，Ubuntu 26.04 已移除 v1 |
| 镜像 | `docker history` 看层；`docker build -t` 构建 |
| 运行 | `docker run -d -p -v`；`docker exec -it` 进入 |
| 编排 | `docker compose up -d / down` |
| 运行时层 | `ctr`（containerd）、`crictl`（CRI）、`runc` |
| 替代方案 | Podman 6：`podman run`，Netavark + nftables，无 CNI |
| systemd | `systemd-nspawn -D <dir>`，systemd 262 静态 PID 1 |
| 版本基准 | Docker 29.9.2、containerd 2.4.2、Podman 6.0.1、systemd 262 |

## 七、学习资源

1. [Docker Engine Release Notes 29](https://docs.docker.com/engine/release-notes/29/) —— Docker 版本与变更官方记录
2. [containerd v2.4.2 Release](https://github.com/containerd/containerd/releases/tag/v2.4.2) —— containerd 变更
3. [Docker 官方文档](https://docs.docker.com/) —— 命令、Dockerfile、Compose 权威手册
4. [systemd 官方文档（systemd-nspawn）](https://www.freedesktop.org/software/systemd/man/latest/systemd-nspawn.html) —— systemd 容器化能力
5. [kernel.org 内核文档](https://www.kernel.org/doc/) —— namespaces、cgroup、overlay 底层机制
6. [man7.org Linux Man Pages](https://man7.org/) —— `unshare`、`mount` 等系统调用手册
7. [Podman 官方文档](https://podman.io/docs/) —— Podman 6 的 Netavark/nftables 网络模型

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本篇所属的 Linux 学习主线地图
- [[Dockerfile编写指南]] —— 镜像编写与构建进阶
- [[Kubernetes部署实践]] —— 容器编排与集群运维
- [[Linux系统管理与运维要点]] —— 容器宿主机的日常运维基础

## 九、变更记录

- 2026-11-19：首次创建。
