---
title: Linux文本处理三剑客
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 文本处理
  - 命令行
  - 运维
aliases:
  - 三剑客
  - grep sed awk
  - Linux文本处理
source: 网络资料整理
---

# Linux文本处理三剑客

> [!摘要] 内容与定位
> **grep、sed、awk** 是 Linux 命令行中处理文本的三件套：`grep` 负责**筛选**，`sed` 负责**变换**，`awk` 负责**聚合统计**。三者都基于流式处理，可像积木一样通过管道 `|` 自由组合，是 Shell 脚本、日志分析、配置批处理与数据清洗的底层能力。
> 本文从基础概念、核心机制、实践步骤、常见坑与速查五个维度展开，版本基准以调研文件为准（`grep 3.12`、`sed 4.10`、`gawk 5.4.1`），定位在 [[Linux-从入门到精通]] 的「阶段二：进阶」文本处理模块。

## 一、最新动态（截至 2026-11）

- **GNU sed 4.10**（2026-04-21 发布）：时隔约 3.5 年的大版本，主要修复大量缺陷，是当前主流发行版采用的版本基准。
- **GNU awk (gawk) 5.4.1**（2026-07-29 发布）：文本处理主版本更新，在 CSV、多字节字符处理与系统调用等方向持续完善。
- **GNU grep 3.12**（2025-09 上游发布，各发行版 2026 年陆续打包）：Debian 13、Fedora 44/45 等主流发行版统一采用的正则匹配工具版本。
- **配套工具同步升级**：GNU coreutils **9.12**（2026-09-14，`cut/nl/unexpand` 已支持多字节、`cat/yes` 零拷贝加速）、bash **5.3**，为三剑客的脚本与命令行环境提供明确的版本基准。
- **组合形态**：三者搭配的成熟范式仍是 `grep` 筛选 → `sed` 变换 → `awk` 聚合统计；处理大文件优先使用流式管道，避免一次性载入内存。

> [!info] 版本时效说明
> 以上版本号来自 2026-11-19 调研快照。正式引用前请按下方来源 URL 复核最新版本号，若官方源已更新则以官方仓库为准。

## 二、基础概念

三剑客并非三个平级工具，而是按职责划分的三种文本处理范式：

| 工具 | 定位 | 核心能力 | 典型场景 |
|---|---|---|---|
| `grep` | 文本**检索/过滤** | 按正则在文本中找匹配行 | 在日志中找错误、从配置中筛条目 |
| `sed` | 文本**流编辑** | 逐行替换、插入、删除、多行处理 | 批量改配置、替换占位符、格式化输出 |
| `awk` | 文本**分析/聚合** | 按字段切分、条件处理、统计输出 | 求和、计数、报表、日志字段分析 |

三个关键共性：

1. **面向行处理**：默认把输入按换行符拆成行，逐行处理后再输出，天然适合日志、配置文件这类行结构化文本。
2. **流式处理**：从标准输入读取、向标准输出写出，不把整个文件读进内存，因此可以处理 GB 级大文件，也能直接嵌入管道。
3. **可组合**：通过 `|` 串联，`grep` 的输出就是 `sed` 的输入，`sed` 的输出又是 `awk` 的输入，无需落地临时文件。

## 三、核心机制

### 3.1 grep：正则匹配引擎

`grep` 在输入行上执行正则匹配，命中的整行（或匹配片段）被输出，不命中的被丢弃。它本质上是一个**模式匹配过滤器**。

- **三种正则语法**：基础正则（BRE，默认）、扩展正则（ERE，用 `-E`）、Perl 兼容正则（PCRE，用 `-P`，非所有发行版默认启用）。
- **关键选项**：`-n` 显示行号、`-c` 只输出匹配计数、`-o` 只输出匹配片段、`-i` 忽略大小写、`-w` 整词匹配、`-r/-R` 递归目录、`-E` 扩展正则、`-P` Perl 正则、`-A/-B/-C` 输出上下文。

```bash
# 在日志中检索 ERROR，忽略大小写并显示行号与后 2 行上下文
grep -in -A2 'error' /var/log/syslog

# 递归查找所有 Python 文件中 import os 的行
grep -rnE '^\s*import os' --include='*.py' ./src

# 只提取 IP 地址片段并统计去重后的个数
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log | sort -u | wc -l
```

### 3.2 sed：流编辑器

`sed` 按"模式空间"逐行处理文本，按脚本指令对每行做替换、删除、插入等变换，输出变换后的行。它本质上是一个**批处理的行级文本变换器**。

- **地址匹配**：`sed '2s/.../.../'` 只处理第 2 行；`sed '/error/s/.../.../'` 只处理匹配 `error` 的行。
- **`s` 命令**：核心的替换命令，格式 `s/匹配/替换/标志`，标志常用 `g`（全局）、`i`（忽略大小写）。
- **就地编辑**：`-i` 直接改写文件，务必配合备份后缀（`-i.bak`）。
- **多行处理**：`N` 读入下一行、`P` 打印模式空间前半部分、`D` 删除并重新处理，可做段落级操作。

```bash
# 就地替换（带 .bak 备份）
sed -i.bak 's/localhost/127.0.0.1/g' /etc/hosts

# 仅替换每行第一个逗号前的内容
echo 'a,b,c' | sed 's/,.*//'

# 删除所有空行与以 # 开头的注释行
sed '/^$/d; /^#/d' config.conf

# 用扩展正则做多分隔符替换
echo 'hello world' | sed -E 's/ +/_/g'
```

### 3.3 awk：模式-动作语言

`awk` 是三者中表达能力最强的：它按"模式 { 动作 }"的结构，对每一行做**字段切分 + 条件执行 + 聚合输出**。它本质上是**轻量级的行式数据处理语言**。

- **字段**：默认以空白分隔字段，`$1`、`$2`... 表示各字段，`$0` 表示整行；可用 `-F` 或 `FS` 自定义分隔符（如逗号、冒号）。
- **内置变量**：`FS/OFS`（输入/输出分隔符）、`NF`（字段数）、`NR`（累计行号）、`NR==FNR`（多文件区分）。
- **生命周期**：`BEGIN` 在处理前执行一次，`END` 在处理完后执行一次，适合做累计统计。
- **函数与系统调用**：`length/substr/split/printf/sprintf`，还可调用 `system()`。

```bash
# 以逗号分隔，求第一列的和
awk -F, '{sum += $1} END {print sum}' data.csv

# 统计文件行数与字段数（自定义输入/输出分隔符）
awk -F: 'BEGIN{OFS="\t"} {print NR, NF}' /etc/passwd

# 输出每行的第 1 和第 3 个字段
awk '{print $1, $3}' data.txt

# 打印字段数大于 5 的行，并统计命中行数
awk 'NF > 5 {print; cnt++} END {print "matched:", cnt}' log.txt
```

### 3.4 三者协作机制

`grep`、`sed`、`awk` 都是 Unix 管道模型下的"标准输入 → 标准输出"程序，串联后形成**流式处理流水线**：

```bash
# 完整流水线：先筛出 404，再统一替换路径前缀，最后统计状态码出现次数
cat access.log \
  | grep ' 404 ' \
  | sed -E 's#^([^ ]*) .*#\1#' \
  | awk '{count[$1]++} END {for (k in count) print k, count[k]}'
```

## 四、实践步骤（含代码/命令示例）

### 4.1 环境验证

```bash
# 确认当前工具版本（应分别为 grep 3.12、sed 4.10、gawk 5.4.1 级别）
grep --version | head -1
sed --version | head -1
awk --version | head -1
```

### 4.2 实战一：日志错误分析

需求：统计某日志中各错误关键字的出现次数，并保留前后上下文。

```bash
# 1. 找出包含 error/fail 的行（忽略大小写，显示行号）
grep -inE 'error|fail' app.log

# 2. 统计各错误关键字出现次数
grep -oEi 'error|fail' app.log | sort | uniq -c | sort -rn

# 3. 查看最后一个 error 的前后 3 行上下文
grep -n 'error' app.log | tail -1 | cut -d: -f1 \
  | xargs -I{} sh -c 'sed -n "$(({}-3)),$(({}+3))p" app.log'
```

### 4.3 实战二：批量修改配置

需求：把一批配置文件里的旧域名替换为新域名，保留备份并输出改动行。

```bash
# 就地替换，生成 .bak 备份，并在标准输出显示被修改的行（-i 无后缀时不写文件需小心）
sed -i.bak 's/old.example.com/new.example.com/g' conf/*.conf

# 验证：对比备份与现文件，只显示有差异的行
diff -u conf/app.conf.bak conf/app.conf

# 若只想要替换结果预览、不修改文件，去掉 -i
sed 's/old.example.com/new.example.com/g' conf/app.conf
```

### 4.4 实战三：CSV 数据聚合

需求：按第二列分组，统计第三列数值的平均值。

```bash
# 假设 CSV：name,dept,score，输出每个部门的平均分
awk -F, 'FNR > 1 {sum[$2] += $3; n[$2]++}
         END {for (d in sum) printf "%s avg=%.2f\n", d, sum[d]/n[d]}' data.csv
```

### 4.5 实战四：Shell 脚本中组合使用

```bash
#!/usr/bin/env bash
set -euo pipefail

# 从日志中提取错误行数，写进汇总文件
log_file="${1:?用法: $0 <logfile>}"
err_count=$(grep -c -i 'error' "$log_file")

# 提取错误行的 IP 并统计 Top5
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' "$log_file" \
  | sort | uniq -c | sort -rn | head -5

echo "error lines: ${err_count}"
```

## 五、最佳实践与常见坑

> [!warning] 就地修改务必留备份
> `sed -i` 是破坏性操作，批量改配置必须带备份后缀（`sed -i.bak 's/.../.../g'`），改完先用 `diff` 复核，再在测试实例验证后推生产。

> [!danger] 正则转义与特殊字符
> 用 `.`、`*`、`[`、`\` 等做字面匹配时必须转义，否则会匹配出意料之外的结果。处理含 `/` 的文本时，建议把 `s` 命令的分隔符换成 `#` 或 `,`，避免写一长串反斜杠。

> [!tip] 大文件优先流式
> 不要用 `cat big.log | grep ...`（多余的 `cat` 无意义，直接 `grep ... big.log`）；处理 GB 级文件时坚持管道流式，避免一次性载入内存。`awk` 也不要把整个文件读进数组再处理。

> [!note] 常见坑清单
> - **`-i` 与平台差异**：BSD 系（macOS）的 `sed -i` 必须带后缀（`-i.bak`），GNU sed 不带后缀也可，跨平台脚本要留意。
> - **`grep -c` 与无匹配**：`grep -c` 返回 0 时退出码为 1，`set -e` 脚本里会误判为失败，需用 `|| true` 或显式判断。
> - **字段分隔一致性**：`awk -F,` 对 CSV 中带引号、含逗号的字段会切错，复杂 CSV 建议用专用工具或先转义。
> - **多字节字符**：旧版本 `cut/nl/unexpand` 对多字节支持不佳，coreutils 9.11 起已改善，跨版本处理中文需先验证。
> - **`xargs` 空输入**：`grep ... | xargs cmd` 在无匹配时可能以空参数执行，建议加 `-r/--no-run-if-empty`。

## 六、核心要点速查

| 目标 | 命令 |
|---|---|
| 递归正则查找 | `grep -rnE 'pattern' ./dir` |
| 只显示匹配片段 | `grep -oE 'pattern' file` |
| 上下文检索 | `grep -n -A2 -B1 'pattern' file` |
| 就地替换（带备份） | `sed -i.bak 's/old/new/g' file` |
| 删除指定行 | `sed '/^#/d' file` |
| 扩展正则替换 | `sed -E 's/a+b/_/g'` |
| 字段求和 | `awk -F, '{s+=$1} END{print s}' f.csv` |
| 统计行数/字段数 | `wc -l file` / `awk '{print NF}' file` |
| 分组计数 | `awk '{c[$1]++} END{for(k in c) print k,c[k]}' f` |
| 组合流水线 | `grep | sed | awk` |

## 七、学习资源

1. [GNU sed 官方发布记录](https://savannah.gnu.org/news/?id=10885) —— sed 4.10 版本信息与更新说明
2. [GNU awk 官方发布页](https://ftp.gnu.org/pub/pub/pub/gnu/gawk/) —— gawk 5.4.1 版本与手册入口
3. [Debian grep 包跟踪页](https://tracker.debian.org/pkg/grep/) —— grep 3.12 在发行版中的打包情况
4. [man7.org: awk(1) 手册](https://www.man7.org/linux/man-pages/man1/awk.1.html) —— awk 权威手册
5. [GNU Coreutils 手册](https://www.gnu.org/software/coreutils/) —— `sort/uniq/cut/xargs` 等配套工具
6. [The Linux Command Line（免费在线书）](https://linuxcommand.org/) —— 文本处理章节系统讲解

## 八、关联笔记

- [[Linux-从入门到精通]] —— Linux 学习主线地图，本知识点位于「阶段二：进阶」文本处理模块
- [[Linux常用命令集]] —— 高频命令速查，含管道与重定向基础
- [[Linux系统管理与运维要点]] —— 日志分析与运维实战的上层应用
- [[Linux-Shell脚本编程]] —— 三剑客在脚本中的工程化使用（如 `set -euo pipefail`）

## 九、变更记录

- 2026-11-19：首次创建。
