---
title: 容器与Docker基础
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Kubernetes
  - 容器
  - Docker
  - 云原生
aliases:
  - Docker与容器基础
  - 容器技术基础
source:
  - 网络资料整理
---

# 容器与 Docker 基础

> [!摘要] 内容与定位
> 本文是 [[DevOps与Kubernetes-从入门到精通]] 体系下的「入门第一课」，聚焦容器与 Docker 的基础原理与实操：容器与镜像的本质（namespace 隔离 + cgroups 限制 + 联合文件系统分层）、Docker 核心组件与常用命令、Dockerfile 编写与镜像构建、镜像仓库管理，以及 2026 年必须关注的运行时与内核基线变化。读完后应能独立完成本地容器的构建、运行与排障，并为后续 Kubernetes（以 containerd/CRI 为运行时）的学习打下基础。

## 一、最新动态（截至 2026-11）

- **Docker Engine**：最新稳定版 **29.9.2（2026-10-20）**，内嵌 containerd **v2.4.2**（修复 CVE-2026-95839 等安全漏洞），默认启用 containerd 镜像存储与 BuildKit **v0.32.2**。来源 [Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
- **Docker Desktop**：最新 **4.98.0（2026-11）**，内置 Docker Compose v5.0.2、Docker Buildx v0.31.1、Docker Sandbox；Windows 新安装默认 `--user` 模式。来源 [Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)
- **v29 运行细节**：`gvisor-tap-vsock` 成为默认 rootless 网络驱动，`slirp4netns` 不再随 Docker 打包；受支持内核可默认启用私有 time namespace；local 日志驱动支持自定义属性；`docker ps --format` 支持 `.HealthStatus` 占位符。来源 [Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
- **内核基线**：Kubernetes v1.35 已移除 cgroup v1 支持，节点必须启用 **cgroup v2**。来源 [K8s v1.35 Sneak Peek（cgroup v1 移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
- **运行时口径**：Kubernetes 已移除 dockershim，集群内真正运行容器的是满足 CRI 的运行时（containerd 等）；`docker` 命令更多是本地开发与构建工具。
- **版本口径提醒**：官方 Docker Engine（29.x）与发行版包（如 Debian `docker.io 28.x`）版本体系不同，不可直接对比。来源 [Debian docker.io 新闻](https://tracker.debian.org/pkg/docker.io/news/)

## 二、基础概念

### 2.1 容器是什么

容器是共享宿主内核、以进程级隔离运行的轻量单元。与传统虚拟机相比，它不虚拟硬件、不包含完整操作系统，启动快、占用小，因此成为云原生的交付标准。

容器本质由三项内核机制叠加而成：

- **namespace（隔离）**：PID、Network、Mount、UTS、IPC、User 等命名空间，让容器看到独立的进程、网络、文件系统与主机名视图。
- **cgroups（资源限制）**：限制 CPU、内存、IO、PID 等资源上限，防止单个容器抢占宿主资源；现代环境要求 **cgroup v2**。
- **联合文件系统（镜像分层）**：镜像由多层只读层叠加而成，容器启动时在最上层加一个可写层，实现「一次构建、到处运行」。

### 2.2 镜像与容器

- **镜像（Image）**：不可变的只读模板，包含应用及其运行环境，遵循 [OCI（Open Container Initiative）](https://opencontainers.org/) 规范。
- **容器（Container）**：镜像运行后的实例，是可读写、有生命周期的进程集合。
- **仓库（Registry）**：存放与分发镜像，公有如 Docker Hub，私有如 Harbor。

### 2.3 Docker 核心组件

| 组件 | 作用 |
| --- | --- |
| Docker Engine（daemon） | 后台守护进程，负责容器生命周期管理 |
| containerd | 镜像与容器运行时，Docker Engine 29.x 内嵌 v2.4.2 |
| BuildKit | 默认构建引擎，负责镜像构建与缓存 |
| Docker CLI | `docker` 命令，面向开发者的交互入口 |
| 镜像仓库 | 镜像的存储、分发与拉取 |

> [!warning] 关键区分
> 集群（Kubernetes）里真正跑容器的是 **containerd 等 CRI 运行时**，不是 Docker Engine。不要把「本机装了 docker」等同于「集群能使用 Docker 运行时」。

## 三、核心机制

### 3.1 镜像分层与构建缓存

镜像由基础镜像层 + 应用层逐层叠加，每条 Dockerfile 指令生成一层。修改某一层，其后所有层缓存都会失效。理解这一点是写好 Dockerfile、提升构建速度的前提。

### 3.2 容器生命周期

容器遵循 `创建 → 启动 → 运行 → 暂停/停止 → 删除` 的生命周期。容器的可写层在删除时丢失，持久数据必须通过卷（Volume）挂载，不能依赖容器内文件系统。

### 3.3 与 Kubernetes 运行时的关系

Kubernetes 通过 CRI（Container Runtime Interface）对接运行时，kubelet 调用 containerd 完成 Pod 内容器的创建与管理。因此容器隔离与资源限制的稳定性，直接决定 K8s 节点上 Pod 的可靠性，容器基础是理解 Pod 调度与资源治理的前置知识。

## 四、实践步骤（含代码/命令示例）

### 4.1 环境验证

```bash
# 查看版本，确认引擎与运行时
docker --version
docker info | grep -E "Server Version|Storage Driver|Cgroup"

# 确认 cgroup v2（现代内核要求）
stat -fc %T /sys/fs/cgroup   # 应输出 cgroup2fs
```

### 4.2 拉取、运行与排查

```bash
# 拉取镜像（生产建议固定版本，避免 latest）
docker pull nginx:1.27-alpine

# 后台运行并映射端口
docker run -d --name web -p 8080:80 nginx:1.27-alpine

# 查看与排查
docker ps                       # 查看运行中的容器
docker logs --tail 100 web      # 查看日志
docker exec -it web sh          # 进入容器
docker inspect web              # 查看配置与状态

# 停止与清理
docker stop web && docker rm web
```

### 4.3 镜像构建（Dockerfile）

```dockerfile
# 多阶段构建：构建环境与运行环境分离，产物更小
FROM golang:1.23-alpine AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server .

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

构建与分发：

```bash
# Docker Engine 29 默认启用 BuildKit 构建
docker build -t my-app:1.0.0 .

# 使用缓存挂载加速依赖下载
docker build -t my-app:1.0.0 \
  --mount=type=cache,target=/root/.cache/go-build .

docker images
docker push my-app:1.0.0
```

### 4.4 数据持久化

```bash
# 使用卷挂载，避免容器删除后数据丢失
docker run -d --name web \
  -p 8080:80 \
  -v web-data:/usr/share/nginx/html \
  nginx:1.27-alpine

docker volume ls
```

### 4.5 容器网络与资源限制

```bash
docker network create app-net

docker run -d --name web --network app-net \
  --memory 256m --cpus 0.5 \
  nginx:1.27-alpine

docker network connect app-net web
```

## 五、最佳实践与常见坑

**最佳实践**

1. **多阶段构建**：只把最终产物复制进运行镜像，显著减小体积与攻击面。
2. **最小基础镜像**：优先 `distroless`、`alpine`，避免引入完整系统与包管理器。
3. **固定基础镜像 tag**，生产镜像用 **digest**，避免 `latest` 被覆盖导致「改了代码却没换镜像」。
4. **非 root 运行**：使用 `nonroot` 镜像或 `USER` 指令，降低容器逃逸风险。
5. **善用 `.dockerignore`**：排除 `.git`、构建产物与密钥文件，缩短构建上下文、避免泄露。
6. **按层合并指令**：把频繁变化的命令（如 `COPY`）放在靠后位置，最大化缓存命中。
7. **供应链安全**：镜像签名（cosign）、SBOM 与漏洞扫描（Trivy），私有仓库可用 [Harbor 2.16.0](https://github.com/goharbor/harbor/releases/tag/v2.16.0) 提供 OCI、扫描、复制与签名。

**常见坑**

- **`CrashLoopBackOff`**：多为入口命令或配置错误。`docker logs --tail 100 web` 查看日志，检查启动命令与依赖。
- **`ImagePullBackOff`**：镜像名/tag 写错，或私有仓库未登录。执行 `docker login` 后重试，并核对镜像名。
- **容器删除后数据消失**：可写层随容器销毁，持久数据必须使用卷。
- **资源占用失控**：未设置 `--memory`/`--cpus` 等 cgroup 限制，单容器拖垮宿主；生产应同时设置 requests 与 limits。
- **cgroup v1 环境**：K8s v1.35 起不再支持 cgroup v1，节点需启用 cgroup v2，否则升级后节点无法就绪。
- **版本口径混淆**：官方 Docker Engine（29.x）与发行版包（Debian `docker.io 28.x`）不同，排查时先确认 `docker info` 的真实版本。

## 六、核心要点速查

1. 容器 = namespace 隔离 + cgroups 限制 + 联合文件系统分层；镜像是不可变交付单元，容器是运行实例。
2. Docker 核心组件：Engine（daemon）、containerd、BuildKit、CLI、镜像仓库。
3. 镜像分层决定构建缓存，Dockerfile 指令顺序直接影响构建速度。
4. 容器可写层随删除消失，持久化必须使用 Volume。
5. 生产镜像用固定 tag 或 digest，基础镜像选最小化版本，非 root 运行。
6. K8s 自 v1.24 移除 dockershim，集群运行时是 containerd 等 CRI 实现，`docker` 主要是本地开发工具。
7. K8s v1.35 起要求 cgroup v2，cgroup v1 已退出支持。
8. Docker Engine 最新 29.9.2（2026-10-20），内嵌 containerd v2.4.2、BuildKit v0.32.2。
9. 排障顺序：看状态 → 看日志 → 看事件 → 查资源与网络。

## 七、学习资源

1. [Docker 官方文档：Engine v29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
2. [Docker 官方文档：Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
3. [Docker 官方文档：Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)
4. [Debian 软件包追踪：docker.io 新闻](https://tracker.debian.org/pkg/docker.io/news/)
5. [Kubernetes 官方博客：Kubernetes v1.35 Sneak Peek（cgroup v1 移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
6. [OCI 官方规范（Open Container Initiative）](https://opencontainers.org/)
7. [Harbor v2.16.0 发布说明](https://github.com/goharbor/harbor/releases/tag/v2.16.0)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
