---
title: Python 文件与 IO 操作
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 文件与IO
  - 文件系统
aliases:
  - Python 文件读写与 IO 操作
  - Python 文件系统与压缩
source: 网络资料整理
---

# Python 文件与 IO 操作

> [!摘要] 摘要
> 本文梳理 Python 的文件读写、路径操作、目录管理、流式处理与压缩归档能力，并以 **PEP 686（UTF-8 默认编码）** 与 **PEP 784（`compression` 包 / zstd）** 两条 3.14–3.15 关键变化为主线，说明其对既有代码的影响与迁移方式。适合处理日志、数据落盘、归档打包与跨平台文件操作的开发者，是 [[Python-从入门到精通]] 体系中「文件与系统交互」一环。

## 一、最新动态（截至 2026-11）

- **Python 3.15（3.15.0 于 2026-10-09 首发，3.15.2 于 2026-10-25 发布）落实 PEP 686：UTF-8 成为默认编码**。`open()` 等未显式指定 `encoding` 的 I/O 一律按 UTF-8 处理，**独立于系统环境**；`PYTHONUTF8=0` 或 `-X utf8=0` 可保留旧行为，`encoding='locale'` 可取当前 locale 编码（3.10+）。
- **Python 3.14（2025-10-07 首发）新增 `compression` 包（PEP 784）**：`compression.lzma/bz2/gzip/zlib` 为旧模块再导出，另新增绑定 Meta zstd 库的 **`compression.zstd`**。**旧模块名暂未弃用**，最早在 3.14 发布 5 年后弃用。
- **归档与目录工具同步支持 zstd**：`tarfile`、`zipfile`、`shutil` 已支持读写 Zstandard 压缩归档。
- **Python 3.15 的 PEP 829**：`.pth` 中以 `import ` 开头的行被**静默弃用**，改用 `.start` 启动配置文件（`pkg.mod:callable` 形式）。
- **`shutil.rmtree()` 的 `onerror` 参数自 3.12 起弃用**，改用 `onexc`。
- 来源：[Python 3.15 What's new](https://docs.python.org/3.15/whatsnew/3.15.html)、[Python 3.14 What's new](https://docs.python.org/3.14/whatsnew/3.14.html)

## 二、基础概念

- **文件即流**：`open()` 返回文本流或二进制流，统一支持上下文管理（`with`）、迭代读取与定位；文本模式按字符解码，二进制模式按字节透传，二者不可混用。
- **编码与缓冲**：文本 I/O 需要 `encoding`/`newline` 参数；默认编码在 3.15 前取决于系统 locale，3.15 起统一为 UTF-8。
- **路径对象**：`pathlib.Path` 提供面向对象的路径操作，`os.path` 提供函数式等价能力；新代码优先用 `pathlib`。
- **目录与归档**：`os`/`shutil` 负责目录树复制、移动、删除；`zipfile`/`tarfile` 负责打包，`gzip`/`bz2`/`lzma`/`zstd` 负责单文件压缩。
- **流式处理**：大文件应逐行迭代或分块读取，避免一次性载入内存。

## 三、核心机制

**1. 打开模式与关键参数**

| 模式 | 含义 |
| --- | --- |
| `r` / `rb` | 只读（文本/二进制） |
| `w` / `wb` | 覆盖写，文件不存在则创建 |
| `a` / `ab` | 追加写 |
| `x` / `xb` | 排他创建，已存在则报错 |
| `r+` / `rb+` | 读写，不截断 |

核心参数：`encoding`、`errors`（`strict`/`ignore`/`replace`）、`newline`、`buffering`。3.15 起编码默认 UTF-8，但官方仍建议**始终显式传 `encoding`**。

**2. 压缩模块的新旧关系（PEP 784）**

`compression` 包是旧模块的**再导出 + 新增 zstd**，两种写法在 3.14 均可用：

```python
import gzip              # 旧写法，仍有效
import compression.gzip  # 3.14 起新写法，指向同一实现
```

**3. 归档格式差异**：`zipfile` 跨平台通用、支持随机访问；`tarfile` 为 Unix 常用、保留权限与符号链接元数据、支持流式读写；`shutil.make_archive()` 按格式创建归档，底层复用上述模块。

## 四、实践步骤（含代码/命令示例）

**1. 基础读写与逐行处理**

```python
# 写入（显式 UTF-8，兼容旧版本）
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n第二行\n")

# 读取：逐行迭代，适合大文件
with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip("\n"))
```

**2. 二进制分块与 pathlib**

```python
from pathlib import Path

with open("logo.png", "rb") as f:
    chunk = f.read(4096)          # 分块读取二进制

p = Path("data") / "input.txt"
p.write_text("hello", encoding="utf-8")
print(p.read_text(encoding="utf-8"))
for child in Path("data").iterdir():
    print(child.name, child.stat().st_size)
```

**3. 目录操作与删除（注意 `onexc`）**

```python
import shutil
from pathlib import Path

shutil.copy2(Path("a.txt"), Path("backup/a.txt"))   # 复制，保留元数据
shutil.move("old_dir", "new_dir")                   # 移动/重命名

# Python 3.12+：用 onexc 代替已弃用的 onerror
shutil.rmtree("temp_dir", onexc=lambda func, path, exc: print(f"跳过: {path}"))
```

**4. 压缩与归档（含 3.14 zstd）**

```python
import gzip, tarfile
from pathlib import Path

with open("log.txt", "rb") as src, gzip.open("log.txt.gz", "wb") as dst:
    dst.write(src.read())
with gzip.open("log.txt.gz", "rt", encoding="utf-8") as f:
    print(f.readline())

# Python 3.14+：标准库 zstd
from compression import zstd
with zstd.open("report.zst", "wt", encoding="utf-8") as f:
    print(f.read())

with tarfile.open("archive.tar.gz", "w:gz") as tar:
    tar.add(Path("data"))
```

**5. 命令行校验**

```bash
# 统计文件行数
python -c "print(sum(1 for _ in open('log.txt', encoding='utf-8')))"

# 3.15 起找出依赖默认编码的代码
python -X warn_default_encoding script.py
```

## 五、最佳实践与常见坑

- **始终显式指定 `encoding`**：3.15 前默认编码随系统 locale 变化，跨平台行为不一致；用 `-X warn_default_encoding` 排查受影响代码。
- **永远用 `with` 管理句柄**：避免依赖垃圾回收关闭文件，防止句柄泄漏或写入未刷新。
- **大文件不要 `read()` 全量加载**：改用逐行迭代或分块读取。
- **文本/二进制勿混用**：文本模式下不要直接写入字节，反之亦然。
- **跨平台路径用 `pathlib`**：避免硬编码分隔符，`Path` 会自动按平台处理。
- **删除前确认目标**：`shutil.rmtree` 不可逆，使用前确认绝对路径；新代码用 `onexc`，不要用已弃用的 `onerror`。
- **压缩模块选择**：需 zstd 用 3.14 的 `compression.zstd`；仅用 gzip/bz2/lzma 时旧模块写法仍有效，但新代码建议新包名以规避 5 年后的弃用。
- **归档解压安全**：`tarfile.extractall()` 可能受路径穿越影响，对来源不可信的归档应校验成员路径。

## 六、核心要点速查

1. **PEP 686（3.15）**：UTF-8 成为默认编码，与系统环境无关；`PYTHONUTF8=0` / `-X utf8=0` 保留旧行为。
2. **官方建议**：始终显式传 `encoding`，用 `-X warn_default_encoding` 排查默认编码依赖。
3. **PEP 784（3.14）**：新增 `compression` 包（`gzip`/`bz2`/`lzma`/`zlib`/`zstd`），旧模块名暂不弃用，计划 5 年后弃用。
4. **归档支持**：`tarfile`、`zipfile`、`shutil` 已支持 Zstandard 压缩归档。
5. **`shutil.rmtree`**：3.12 起 `onerror` 弃用，改用 `onexc`。
6. **PEP 829（3.15）**：`.pth` 中 `import ` 行静默弃用，改用 `.start` 启动配置文件。
7. **`pathlib.Path`** 为现代路径操作首选，读写方法均需显式编码。
8. **大文件**：逐行迭代或分块读取，避免一次性载入内存。

## 七、学习资源

- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Python 3.14 What's new（Python 官方文档）](https://docs.python.org/3.14/whatsnew/3.14.html)
- [PEP 686 – Make UTF-8 mode default](https://peps.python.org/pep-0686/)
- [PEP 784 – Add zstd to the standard library](https://peps.python.org/pep-0784/)
- [pathlib — Manipulate paths (Python 官方文档)](https://docs.python.org/3/library/pathlib.html)
- [shutil — High-level file operations (Python 官方文档)](https://docs.python.org/3/library/shutil.html)
- [io — Core tools for working with streams (Python 官方文档)](https://docs.python.org/3/library/io.html)
- [tarfile / zipfile / compression（Python 官方文档）](https://docs.python.org/3/library/tarfile.html)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 语言演进与工程化全景总览，本篇为其「文件与系统交互」子主题
- [[Python-高级特性]] — 装饰器、元编程等进阶主题，配合理解函数式 IO 封装

## 九、变更记录

- 2026-11-19：首次创建。
