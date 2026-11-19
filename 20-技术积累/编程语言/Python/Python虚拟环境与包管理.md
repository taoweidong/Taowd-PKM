---
title: Python虚拟环境与包管理
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 虚拟环境
  - 包管理
aliases:
  - Python venv 与 pip/uv/Poetry 包管理
source: 网络资料整理
---

# Python虚拟环境与包管理

> [!摘要] 摘要
> 本文系统讲解 Python 的**环境隔离**与**依赖管理**体系：从内置 `venv` 的隔离原理，到 `pip`、`uv`、Poetry 三类工具的分工，再到 `pyproject.toml`、PEP 735 依赖组、PEP 751 标准锁文件 `pylock.toml`、PEP 723 内联脚本元数据等现代标准。目标是让读者能独立完成「建环境 → 装依赖 → 锁定版本 → 跨机器复现」的完整闭环，并避开版本与工具混用带来的常见坑。适合刚入门 Python、需要做项目环境标准化，或在 `venv`/`uv`/Poetry 之间做选型的开发者。

## 一、最新动态（截至 2026-11）

以下版本与 PEP 状态均来自调研文件，第三方补丁版本更新频繁，**具体以写作当日的官方发布页为准**。

- **Python 3.15 是当前最新稳定主线**：3.15.0 首发于 2026-10-09，最新补丁 **3.15.2** 于 2026-10-25 发布（紧急安全发布）。与本主题直接相关的语言级变化是 **PEP 686：UTF-8 成为默认编码**，文件与文本 I/O 不再依赖系统 locale，建议始终显式传 `encoding` 保证跨版本兼容。
- **PEP 829（Python 3.15）引入包启动配置文件**：`.pth` 中以 `import ` 开头的行被**静默弃用**，改为新增的 `.start` 文件（`pkg.mod:callable` 形式在启动时调用）。依赖旧式 `.pth` 注入的打包方案需要关注。
- **PEP 810（Python 3.15）显式延迟导入**（`lazy` 软关键字），可缩短包导入启动时间，Pydantic 2.14 等库已跟进。
- **pip 最新为 26.3**（2026-11-02），26.0 于 2026-01-31 发布。
- **uv 最新为 0.13.7**（2026-11-03）；**0.13.0（2026-10-09）起将 Python 3.15 设为默认稳定 Python 版本**。
- **Poetry 最新为 2.3.4**：2.3.0（2026-01-18）起 `installer.re-resolve` 默认由 `true` 改为 `false`；2.1.0（2025-02）支持 PEP 621 的替代构建后端（`poetry build` 遵循 `[build-system]`）；2.0（2025-01）起 `poetry lock` 默认 `--no-update`，并移除 `poetry shell`（改用 `poetry-plugin-shell`）。
- **标准层面**：PEP 735（`pyproject.toml` 依赖组）、PEP 751（**Python 标准锁文件 `pylock.toml`**，2025-03 被接受）、PEP 723（内联脚本元数据）构成当前依赖管理的事实标准。

## 二、基础概念

- **解释器与环境隔离**：Python 解释器可同时存在多个版本，每个项目需要一份**独立的依赖目录**，避免不同项目的包互相污染。虚拟环境就是一份「独立的 `site-packages` + 指向某个解释器的轻量副本」。
- **`sys.prefix` 与 `sys.base_prefix`**：两者用于区分「当前激活的虚拟环境」与「解释器本体」。在虚拟环境中，`sys.prefix` 指向 `.venv`，`sys.base_prefix` 指向基础解释器；未激活时二者相同。**Python 3.15 的 C API 也已改用 `PyConfig_Get()` 读取相关配置（PEP 741 后续）**。
- **包管理工具的四个层次**：环境创建（`venv` / `virtualenv` / `uv venv`）、依赖解析与安装（`pip` / `uv pip` / Poetry）、构建与元数据（PEP 517 / 518 / 621 / 660）、版本锁定（`requirements.txt` / `poetry.lock` / `uv.lock` / PEP 751 `pylock.toml`）。
- **`pyproject.toml` 是事实来源**：`[project]` 声明项目元数据与依赖，`[build-system]` 声明构建后端，`[tool.*]` 存放各工具配置。**环境隔离是现代 Python 工程的第一步**。

## 三、核心机制

**1. `venv` 的隔离机制**：`python -m venv .venv` 会生成 `pyvenv.cfg`、独立的 `site-packages` 目录，并在其中放置指向基础解释器的可执行文件副本。激活的本质不是「运行什么程序」，而是**修改 `PATH`（把 `.venv/bin` 或 `.venv\Scripts` 前置）并设置 `VIRTUAL_ENV` 环境变量**，使 `python`、`pip` 与脚本默认命中虚拟环境。

**2. `pip` 的解析与安装**：pip 从索引（默认 PyPI）下载并解析依赖树，把包安装到当前环境的 `site-packages`，同时生成 `.dist-info` 记录版本与依赖。它只做安装，**不提供锁定语义**，长期项目应配合 `requirements.txt` 或锁文件。

**3. `uv` 的缓存与项目模型**：uv 由 Astral 用 Rust 实现，以**全局内容寻址缓存** + **硬链接**复用已下载的包，因此创建环境与安装速度显著快于 `venv`/`virtualenv`。它把项目环境（`uv add`/`uv sync` + `uv.lock`）与全局工具环境（`uvx`）分离，避免工具污染项目。

**4. Poetry 的依赖解析**：Poetry 以 `pyproject.toml` + `poetry.lock` 为核心，负责解析、锁定与构建；2.3.0 起 `installer.re-resolve` 默认关闭，意味着**安装时不再默认重新解析依赖**，直接以锁文件为准。

**5. 锁文件与标准**：PEP 751 定义的 **`pylock.toml`** 是**人可读、机器生成**的可复现锁文件，安装器消费它时**无需在安装期再做依赖解析**。PEP 735 把「依赖组」（如 `dev`、`test`）标准化进 `pyproject.toml`。PEP 723 允许在脚本头部用注释声明依赖，配合 `uv run` 可自动创建临时环境。

## 四、实践步骤（含代码/命令示例）

**1. 标准库 `venv`（最基础、零第三方依赖）**

```bash
# 创建环境
python -m venv .venv

# 激活（Windows PowerShell）
.venv\Scripts\Activate.ps1
# 激活（macOS / Linux）
source .venv/bin/activate

# 确认命中的是虚拟环境
python -c "import sys; print(sys.prefix, sys.base_prefix)"

# 安装与使用
python -m pip install --upgrade pip
python -m pip install requests
python app.py

# 退出
deactivate
```

**2. 项目清单 `pyproject.toml`**

```toml
[project]
name = "myproj"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["pydantic>=2.14", "requests>=2.32"]

[project.optional-dependencies]
dev = ["pytest>=9", "mypy>=2.4"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**3. uv（推荐，新项目主流）**

```bash
uv init                     # 生成 pyproject.toml、.python-version、.venv
uv add requests             # 写入依赖并更新 uv.lock
uv add --dev pytest         # 写入开发依赖组
uv sync                     # 严格按 uv.lock 同步环境
uv run python main.py       # 在同步后的环境里执行
uv pip list                 # 查看环境包
uvx ruff check .            # 用隔离的临时环境运行工具，不污染项目
```

**4. Poetry**

```bash
poetry init                 # 交互式生成 pyproject.toml
poetry add requests         # 添加依赖并写入 poetry.lock
poetry install              # 按锁文件安装
poetry run python main.py   # 在项目环境中运行
poetry shell                # 需安装 poetry-plugin-shell（2.0 起内置已移除）
```

**5. 依赖组与内联脚本**

```bash
# 安装标准依赖组（PEP 735 / uv 语法）
uv sync --group dev
```

```python
# /// script
# dependencies = ["rich>=13"]
# ///
import rich

rich.print("hello")
```

```bash
uv run script.py   # 自动根据内联元数据建临时环境并运行（PEP 723）
```

## 五、最佳实践与常见坑

**最佳实践**

- **永远在虚拟环境里开发**，不要向全局解释器装项目依赖。
- **锁文件入库**（`uv.lock` / `poetry.lock` / `pylock.toml`），并以锁文件为准执行 `uv sync` / `poetry install`。
- **声明 Python 版本**：用 `requires-python = ">=3.13"` 与 `.python-version` 双重约束，uv 会据此自动选择解释器。
- **明确编码**：3.15 起 UTF-8 虽为默认，但显式传 `encoding="utf-8"` 更稳妥。

**常见坑**

- **用错解释器**：`python`、`python3`、`py -3.15` 指向不同解释器时，`python -m pip` 与 `pip` 可能装到不同环境。**统一用 `python -m pip`** 或 `uv` 的 `uv pip`，避免 PATH 歧义。
- **Windows PowerShell 激活失败**：`Activate.ps1` 可能被执行策略拦截，报错时用 `Set-ExecutionPolicy -Scope Process Bypass` 临时放行，或直接把 `.venv\Scripts` 加入 `PATH`。
- **`pip` 与 `uv` 混用**：先 `pip install` 再 `uv sync` 会因 `uv.lock` 与实际环境不一致而报错；**以 `uv sync` 为准，不要混装**。
- **Poetry 2.3 行为变化**：`installer.re-resolve` 默认改为 `false` 后，安装不再自动重解析依赖；改了 `pyproject.toml` 记得先 `poetry lock` 再 `poetry install`。
- **旧式 `.pth` 注入**：依赖 `.pth` 中 `import ` 行做启动注入的包，在 Python 3.15 下被静默弃用，需关注迁移到 `.start`。
- **可编辑安装**：`pip install -e` 依赖 PEP 660，切换构建后端（如从 setuptools 换到 hatchling）时需确认后端支持。

## 六、核心要点速查

1. 虚拟环境本质是**独立 `site-packages` + 激活时改 `PATH`/`VIRTUAL_ENV`**；用 `sys.prefix` 与 `sys.base_prefix` 区分激活态与基础解释器。
2. 截至 2026-11：Python 最新稳定版为 **3.15.2**，**pip 26.3**、**uv 0.13.7**、**Poetry 2.3.4**；uv 0.13.0 起默认 Python 3.15。
3. `pyproject.toml` 是唯一事实来源：`[project]` 依赖、`[build-system]` 后端、`[tool.*]` 工具配置。
4. uv 靠**全局缓存 + 硬链接**加速，命令以 `uv init/add/sync/run` 为核心，`uvx` 运行工具不污染项目。
5. PEP 751 定义标准锁文件 **`pylock.toml`**（人可读、机器生成、安装期无需解析）；PEP 735 标准化依赖组；PEP 723 支持内联脚本元数据。
6. Poetry 2.3.0 起 `installer.re-resolve` 默认 `false`；2.0 起移除 `poetry shell`，改用 `poetry-plugin-shell`。
7. 依赖隔离优先于全局安装，**锁文件入库**是跨机器可复现的前提。

## 七、学习资源

- [Python 官方文档：venv — Creating virtual environments](https://docs.python.org/3/library/venv.html)
- [Python 官方文档：What's new in Python 3.15](https://docs.python.org/3.15/whatsnew/3.15.html)
- [uv Releases（Astral 官方）](https://github.com/astral-sh/uv/releases)
- [uv 官方文档：项目结构与文件](https://docs.astral.sh/uv/concepts/projects/layout/)
- [Poetry Releases 官方博客](https://python-poetry.org/blog/category/releases)
- [PEP 735 — Dependency groups](https://peps.python.org/pep-0735/)
- [PEP 751 — Python lockfile format](https://peps.python.org/pep-0751/)
- [PEP 723 — Inline script metadata](https://peps.python.org/pep-0723/)
- [PEP 621 — Project metadata](https://peps.python.org/pep-0621/)
- [pip 项目页（PyPI）](https://pypi.org/project/pip/)

## 八、关联笔记

- [[Python-从入门到精通]] — 本主题在 Python 体系中的定位，环境准备与工具链总览
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 装饰器、元编程、类型等进阶主题

## 九、变更记录

- 2026-11-19：首次创建。
