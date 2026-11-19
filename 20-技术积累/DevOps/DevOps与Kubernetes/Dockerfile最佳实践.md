---
title: Dockerfile 最佳实践
date: 2026-11-19
updated: 2026-11-19
tags:
  - DevOps
  - Docker
  - Dockerfile
  - 容器
  - 镜像构建
  - 云原生
aliases:
  - Dockerfile 最佳实践
  - Dockerfile Best Practices
source:
  - 网络资料整理
---

# Dockerfile 最佳实践

> [!摘要] 摘要
> 本文系统梳理 Dockerfile 的编写规范与工程实践，是 [[DevOps与Kubernetes-从入门到精通]] 体系中「容器与镜像构建」这一环的落地文档。内容覆盖：截至 2026-11 的构建工具链版本动态、镜像分层与 BuildKit 缓存等核心机制、多阶段构建等完整可运行示例、最佳实践清单与高频坑，最后给出速查表与权威学习资源。适合需要把镜像做小、做快、做安全的后端、运维与平台工程师直接对照落地。

Dockerfile 是把源码与依赖固化为可移植容器镜像的「构建配方」。它决定了镜像体积、构建速度、可复现性与运行安全，是容器化交付的第一道关口。截至 2026-11，构建链路已全面转向 **BuildKit + containerd 镜像存储**，实践时应以这一代工具链为准。

## 一、最新动态（截至 2026-11）

以下版本号均来自 2026-11-19 调研核实的官方发布说明，写作/落地前建议回源核对。

- **Docker Engine 29.9.2（2026-10-20 发布）**：29.x 最新补丁版，内嵌 containerd **v2.4.2**（修复 CVE-2026-95839 等安全漏洞）、BuildKit **v0.32.2**，构建产物默认使用 BuildKit。来源：[Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
- **Docker Desktop 4.98.0（2026-11 最新）**：内置 Docker Compose **v5.0.2**、Docker Buildx **v0.31.1** 与 Docker Sandbox；Windows 新安装默认采用 `--user` 模式。来源：[Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)
- **运行时基线收紧**：Kubernetes 已移除 dockershim，集群内真正运行容器的是符合 CRI 的运行时（containerd 等）；K8s **v1.35 已移除 cgroup v1 支持**，节点必须启用 cgroup v2。这意味着镜像必须适配 cgroup v2 环境。来源：[K8s v1.35 Sneak Peek（cgroup v1 移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)
- **构建最佳实践**：官方核心仍为多阶段构建、`.dockerignore`、最小基础镜像、按层合并、固定基础镜像 tag、非 root 运行、BuildKit 缓存挂载。来源：[Dockerfile 最佳实践（docs.docker.com）](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- **供应链安全升温**：镜像供应链安全（签名、SBOM、Trivy 扫描、私有仓库）已成为标配，可结合 Harbor 2.16、Trivy 等工具落地。

## 二、基础概念

- **镜像是交付单元**：镜像由多层只读文件系统叠加而成，容器在镜像之上加一层可写层运行；镜像即制品，应可版本化、可追溯、可复现。
- **Dockerfile 与构建上下文（build context）**：`docker build` 会把当前目录（或 `-f` 指定的上下文）打包传给构建器，Dockerfile 中的 `COPY`/`ADD` 只能从该上下文取文件。上下文越大，构建越慢、传输越贵。
- **BuildKit**：新一代构建引擎，支持并行构建、缓存挂载、secret/ssh 挂载、内联缓存等，Docker Engine 29.x 默认启用。相比传统 builder，它能显著降低重复构建的耗时。
- **containerd 镜像存储（containerd image store）**：Docker Engine 29.x 默认启用，镜像由 containerd 统一管理，层去重与拉取效率更高。
- **OCI 规范**：镜像与制品遵循 Open Container Initiative 标准，同一镜像可被 containerd、CRI-O、Kubernetes 等共同消费，是「一次构建、多处运行」的基础。
- **构建四要素**：基础镜像（`FROM`）、工作目录与环境（`WORKDIR`/`ENV`）、安装与拷贝指令（`RUN`/`COPY`）、运行时元数据（`EXPOSE`/`USER`/`ENTRYPOINT`/`CMD`）。

## 三、核心机制

**1. 镜像分层与缓存。** 每条指令生成一个只读层，构建器按指令顺序逐层比对缓存：某层缓存命中后，其后未变更的层直接复用。因此**指令顺序决定构建速度**——把不常变化的依赖安装放在前面，把频繁变化的业务代码放在后面，可最大化缓存命中。

**2. 层数与体积。** 每条指令都会新增一层，`RUN` 中的安装、编译会产生临时文件。通过「一条 `RUN` 合并多条命令 + 清理临时文件」可减少层数、压缩体积，但更推荐用多阶段构建直接丢弃中间产物。

**3. 构建上下文过滤。** `.dockerignore` 在打包上下文前排除 `.git`、`node_modules`、日志、本地配置等，既加速传输，又避免把无关文件打进镜像。

**4. BuildKit 缓存挂载。** 用 `--mount=type=cache` 把包管理器缓存（如 `pip`/`npm`/`apt`）挂载到构建外部，避免缓存被固化进镜像层，同时跨构建复用。

**5. 多阶段构建。** 用多个 `FROM` 分阶段编译与运行，只把最终需要的可执行文件、依赖从构建阶段 `COPY --from` 到运行阶段，从而用「编译期完整环境 + 运行期最小镜像」兼顾构建与交付。

**6. 运行身份与镜像供应链。** 镜像内置用户（`USER`）决定容器进程权限；镜像还可附 SBOM、签名与漏洞扫描结果，配合准入策略形成供应链闭环。

## 四、实践步骤（含代码/命令示例）

**1. 环境准备**，确认构建工具链版本：

```bash
docker version
docker buildx version
docker info | grep -i -E "storage|containerd"
```

**2. 编写多阶段 Dockerfile**（以 Python 服务为例）：

```dockerfile
# syntax=docker/dockerfile:1.7

# ---- 构建阶段 ----
FROM python:3.12-slim AS builder
WORKDIR /app

# 先拷依赖清单，最大化利用层缓存
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# 再拷源码并编译（示例：编译消息目录）
COPY . .
RUN python -m compileall /app

# ---- 运行阶段：最小镜像、非 root ----
FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app

# 只拷需要的产物
COPY --from=builder --chown=nonroot:nonroot /install /install
COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/install/bin/python", "/app/app.py"]
```

**3. 编写 `.dockerignore`**，避免把无关内容送进上下文：

```text
.git
.gitignore
**/__pycache__
**/*.pyc
.venv
venv
node_modules
*.log
*.md
Dockerfile
.dockerignore
.env
```

**4. 构建镜像**，开启 BuildKit 并显式指定 tag：

```bash
# DOCKER_BUILDKIT=1 在新版 Engine 中默认开启，保留以兼容旧环境
DOCKER_BUILDKIT=1 docker buildx build \
  --platform linux/amd64 \
  --cache-from type=local,src=/tmp/.buildx-cache \
  --cache-to type=local,dest=/tmp/.buildx-cache,mode=max \
  -t registry.example.com/demo/app:1.0.0 \
  -f Dockerfile .
```

**5. 本地运行与验证**：

```bash
docker run --rm -p 8080:8080 registry.example.com/demo/app:1.0.0
docker image inspect registry.example.com/demo/app:1.0.0 --format '{{.Size}}'
```

**6. 镜像安全扫描**（供应链安全）：

```bash
trivy image --severity HIGH,CRITICAL registry.example.com/demo/app:1.0.0
```

**7. 镜像签名与推送**（可选，配合 cosign）：

```bash
cosign sign --key cosign.key registry.example.com/demo/app@<digest>
docker push registry.example.com/demo/app:1.0.0
```

## 五、最佳实践与常见坑

**推荐做法**

- **多阶段构建**：把编译依赖与运行时彻底分离，最终镜像只保留运行必需文件，兼顾体积与安全。
- **固定基础镜像 tag**：用 `python:3.12-slim` 这类确定版本，**避免使用 `latest`**，防止同 tag 被覆盖导致「改了代码却没换镜像」。
- **最小基础镜像**：优先 `alpine`、`slim` 或 `distroless`，减少漏洞面与体积。
- **按层合并、控制层数**：把相关 `RUN` 合并为一条，并在同层清理临时文件。
- **依赖清单先拷**：先 `COPY requirements.txt` 再安装依赖，代码变动不会让依赖层缓存失效。
- **非 root 运行**：用 `USER` 指定低权限用户，配合 `--chown` 处理文件属主。
- **用 BuildKit 缓存**：`--mount=type=cache` 挂载包管理器缓存，兼顾速度与镜像纯净。
- **显式声明时区与编码**：需要时设置 `TZ` 与 `LANG`，避免容器内时区/字符集异常。

**常见坑**

- **`COPY . .` 拷贝整个上下文**：未配 `.dockerignore` 时会把 `.git`、`node_modules`、密钥等打进镜像，既慢又不安全。
- **依赖与代码顺序颠倒**：先拷源码再装依赖，导致每次改代码都触发全量依赖重装。
- **构建阶段跑测试或下载**：把测试、调试工具留在镜像里，增大体积与攻击面；测试应放在 CI，而非镜像构建。
- **以 root 运行**：容器逃逸时 root 危害更大，生产镜像务必降权。
- **`latest` tag**：不可复现、易被覆盖，生产环境建议用**摘要（digest）**或精确版本号。
- **缺少进程信号处理**：直接以应用为 PID 1 可能吞掉 `SIGTERM`，导致滚动更新时不能优雅退出，可引入 `tini`/`dumb-init` 或改用 `exec` 形式启动。
- **缓存与可复现性冲突**：缓存挂载能加速，但跨机器复现时需保证依赖版本锁定（锁文件），否则构建结果可能不一致。

## 六、核心要点速查

1. 镜像是交付单元，Dockerfile 决定镜像的体积、速度、可复现性与安全。
2. 截至 2026-11：Docker Engine **29.9.2（2026-10-20）**，内嵌 containerd **v2.4.2**、BuildKit **v0.32.2**；Docker Desktop **4.98.0**。
3. 构建默认走 **BuildKit + containerd 镜像存储**，善用 `--mount=type=cache` 加速。
4. 镜像分层与缓存由指令顺序决定，**依赖清单先拷、代码后拷**是缓存命中的关键。
5. **多阶段构建**是压缩镜像体积的头号手段，只把运行必需产物带进最终镜像。
6. 基础镜像用固定版本，**拒绝 `latest`**，生产建议用镜像摘要。
7. 必备 `.dockerignore`，排除 `.git`、`node_modules`、日志与本地密钥。
8. 运行阶段用 `USER` 降权，避免以 root 运行。
9. 基础镜像优先 `alpine`/`slim`/`distroless`，最小化漏洞面。
10. 供应链安全：Trivy 扫描 + cosign 签名 + 私有仓库（如 Harbor），与构建流程集成。
11. 运行时基线：K8s 自 v1.24 移除 dockershim；**v1.35 起需 cgroup v2 与 containerd 2.0+**。
12. 常用命令：`docker buildx build`、`docker image inspect`、`trivy image`、`cosign sign`。

## 七、学习资源

1. [Docker 官方文档：Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
2. [Docker Engine 29 Release Notes](https://docs.docker.com/engine/release-notes/29/)
3. [Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)
4. [Docker 官方文档：多阶段构建（Multi-stage builds）](https://docs.docker.com/build/building/multi-stage/)
5. [Docker 官方文档：使用 BuildKit 缓存挂载（cache mounts）](https://docs.docker.com/build/builders/guide/)
6. [Trivy：开源漏洞扫描器](https://github.com/aquasecurity/trivy)
7. [cosign：镜像签名与验证](https://github.com/sigstore/cosign)
8. [Kubernetes 官方博客：v1.35 Sneak Peek（cgroup v1 移除）](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)

## 八、关联笔记

- [[DevOps与Kubernetes-从入门到精通]]
- [[DevOps]]
- [[Dockerfile编写指南]]
- [[Docker-compose示例]]
- [[Kubernetes部署实践]]

## 九、变更记录

- 2026-11-19：首次创建。
