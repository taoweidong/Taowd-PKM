---
title: Linux-文本三剑客实战
date: 2026-11-19
tags:
  - 技术积累
  - Linux
  - 文本处理
  - grep
  - sed
  - awk
aliases:
  - 文本三剑客
  - grep sed awk
---

# Linux-文本三剑客实战

> [!abstract] 摘要
> grep、sed、awk 是 Linux 文本处理的"三剑客"：grep 负责**筛出行**，sed 负责**改文本**，awk 负责**按字段算数据**。三者组合可以完成 90% 的日志分析、配置批量修改与数据统计任务，是 [[Linux-从入门到精通]] 阶段二的核心技能，也是 [[Linux常用命令集]] 中文本处理部分的深入展开。

## 一、概念与原理

三剑客同属 Unix 流式文本处理工具，共享管道哲学：只处理文本流、逐行消费、不落地中间文件。分工如下：

| 工具 | 定位 | 处理单位 | 典型场景 |
|---|---|---|---|
| grep | 过滤（匹配就输出） | 行 | 找错误日志、搜代码、递归搜目录 |
| sed | 编辑（替换/删除/插入） | 行（模式空间） | 批量改配置、清洗文本、按行号取内容 |
| awk | 分析（分字段 + 计算） | 记录 / 字段 | 列求和、分组统计、格式化报表 |

```mermaid
graph LR
    A[文本流<br/>日志 / 命令输出] --> B["grep 过滤<br/>选出有用的行"]
    B --> C["sed 编辑<br/>替换 / 删除 / 重排"]
    C --> D["awk 分析<br/>按字段统计计算"]
    D --> E[报表 / 结论]
```

**正则方言对照**（三剑客通用，但默认方言不同）：

| 方言 | 启用方式 | 语法差异 |
|---|---|---|
| BRE（基本） | grep / sed 默认 | `+ ? \| ( ) {m,n}` 都需加反斜杠转义 |
| ERE（扩展） | `grep -E`、`sed -E`、awk 默认 | `+ ? \| ( ) {m,n}` 直接写 |
| PCRE | `grep -P`（GNU 扩展） | 支持 `\d` `\s` 等 Perl 语法 |

通用元字符：`.` 任意单字符、`^` 行首、`$` 行尾、`[abc]` 字符集、`[^abc]` 反集、`*` 前一元素重复 0 次以上。

> [!info] 环境说明
> 本文命令均在 Ubuntu/Debian（GNU grep 3.x / GNU sed 4.x / gawk 5.x）下验证；macOS/BSD 的 sed 与 awk 行为有差异（如 BSD `sed -i` 必须带备份后缀参数），跨平台使用前先查对应手册。

## 二、核心语法 / 命令详解

### 2.1 grep — 过滤行

核心选项（依据 [man7.org grep(1)](https://man7.org/linux/man-pages/man1/grep.1.html)）：`-i` 忽略大小写；`-n` 行号；`-v` 反选；`-r`/`-R` 递归（`-R` 跟随符号链接）；`-E`/`-F` ERE 正则/固定字符串（搜字面量更快）；`-c`/`-l` 只输出计数/文件名；`-w`/`-o` 整词匹配/只输出匹配片段；`-A n -B n -C n` 显示匹配行后/前/前后 n 行上下文；`--include=GLOB` 递归时只搜匹配文件名。

10 条真实命令与输出说明（示例文件 `app.log`，一行形如 `2026-11-19 10:23:01 ERROR db timeout`）：

```bash
grep -n "ERROR" app.log                     # 输出：12:2026-11-19 10:23:01 ERROR db timeout
grep -in "error" app.log                    # 忽略大小写，Error/ERROR 都命中
grep -v "DEBUG" app.log                     # 反选：排除含 DEBUG 的行
grep -C 3 "ERROR" app.log                   # 错误前后各 3 行，组间用 -- 分隔
grep -rn --include="*.py" "TODO" ~/project/ # 递归只搜 .py 文件并显示行号
grep -c "ERROR" app.log                     # 只统计匹配行数，输出：37
grep -rl "old.domain.com" /etc/nginx/       # 只列出哪些文件包含匹配
grep -F "192.168.1.1" access.log            # 固定字符串搜索：. 不当正则，搜 IP/路径必用
grep -w "cat" words.txt                     # 整词匹配，避免 cat 误命中 category
grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" access.log | head -3
# -o 只输出匹配片段：逐行打印日志中的 IP（10.0.0.5 / 10.0.0.7 / 192.168.1.100）
```

### 2.2 sed — 逐行编辑

sed 的工作模型：把一行读进**模式空间** → 执行脚本命令 → 默认打印 → 读下一行。`-n` 关闭自动打印（配合 `p`），`-i[SUFFIX]` 就地写回（依据 [GNU sed 手册](https://www.gnu.org/software/sed/manual/sed.html)）。

常用语法：`s/旧/新/标志`（标志 `g` 全部、`p` 打印、`2` 只替换第 2 处、`i` 忽略大小写）；`d` 删除；`p` 打印；`a 文本`/`i 文本` 行后追加/行前插入；`c 文本` 整行替换；`y/abc/xyz/` 逐字符转写。地址可用行号（`3`、`$`）、正则（`/ERROR/`）、范围（`3,8`、`/A/,/B/`）、步进（`1~2` 奇数行）、取反（`3!d`）。

10 条真实命令（示例文件 `conf.txt`，内容含 `port=8080`、注释行等）：

```bash
sed 's/port=8080/port=9090/g' conf.txt        # 全局替换，打印到屏幕预览，不改文件
sed -i.bak 's/port=8080/port=9090/g' conf.txt # 就地修改并留备份：conf.txt.bak 为原文件
sed 's/,/,|/2' data.csv                       # 只替换每行第 2 处匹配
sed '/^$/d' conf.txt                          # 删除空行
sed -E '/^\s*#/d' conf.txt                    # 删除以 # 开头（允许前导空格）的注释行
sed -n '3,8p' conf.txt                        # 按行号范围取第 3 到 8 行
sed -n '/BEGIN/,/END/p' conf.txt              # 从 /BEGIN/ 行打印到 /END/ 行
sed '1i # 生成于 2026-11-19' conf.txt         # 在第 1 行前插入一行
sed '/\[server\]/a log_level=info' conf.txt   # 在匹配 [server] 的行后追加一行
sed 's/;$/; # checked/' conf.txt              # 行尾追加：以 ; 结尾的行补注释
```

### 2.3 awk — 按字段分析

awk 程序结构是 `模式 { 动作 }`，对每条记录执行；缺模式=对所有行执行，缺动作=打印该行。核心内置变量（依据 [GNU gawk 手册](https://www.gnu.org/software/gawk/manual/gawk.html)）：

| 变量 | 含义 | 变量 | 含义 |
|---|---|---|---|
| `$0` | 整行 | `NF` | 当前记录字段数（`$NF` 即最后一列） |
| `$1..$NF` | 第 1 到最后字段 | `NR`/`FNR` | 累计行号 / 当前文件内行号 |
| `FS`/`-F` | 输入字段分隔符（可为正则） | `OFS`/`ORS` | 输出字段 / 记录分隔符 |
| `RS` | 记录分隔符（默认换行） | `FILENAME` | 当前文件名 |

10 条真实命令（`/etc/passwd` 以 `:` 分列：第 1 列用户名、第 3 列 UID；`access.log` 第 1 列 IP、第 7 列 URL、第 9 列状态码、第 10 列字节）：

```bash
awk '{print $1}' access.log                  # 取第 1 列（默认按空白分列）
awk -F: '{print $1}' /etc/passwd             # 指定分隔符：列出用户名
awk -F: '$3 >= 1000 {print $1, $6}' /etc/passwd   # 模式过滤：UID>=1000 的普通用户
awk '/ERROR/{n++} END{print n}' app.log      # 统计 ERROR 行数（模式计数）
awk 'BEGIN{print "user uid"} $3>=1000{print $1,$3} END{print "共", NR, "行"}' /etc/passwd
# BEGIN/END 组合：表头 + 过滤输出 + 汇总行
awk -F: 'BEGIN{OFS=" | "}{print $1, $3, $7}' /etc/passwd   # OFS 统一输出分隔符
free -m | awk '/^Mem/{printf "总:%dMB 可用:%dMB 占比%.1f%%\n", $2, $7, ($2-$7)*100/$2}'
# printf 格式化报表（对齐与精度靠它）
awk '{cnt[$1]++} END{for (ip in cnt) print ip, cnt[ip]}' access.log   # 关联数组分组计数
awk '{sum[$9]+=$10} END{for (s in sum) print s, sum[s]}' access.log   # 数组累加：按状态码求字节总量
awk '$2 > 1000 {print NR ": " $0}' data.txt  # 表达式模式：第 2 字段超 1000 的行带行号输出
```

> [!tip] NF 与 $NF 的区分
> `NF` 是"当前行有几个字段"，`$NF` 是"最后一个字段的内容"。`awk '{print NF}'` 输出数字，`awk '{print $NF}'` 输出末列值——写报表时这两个是最常用的变量。

## 三、实战案例

### 3.1 案例：Nginx 访问日志分析（Ubuntu 22.04/24.04）

样例行（combined 格式）：`10.0.0.5 - - [19/Nov/2026:10:23:01 +0800] "GET /api/users HTTP/1.1" 200 1234`，字段：`$1` 客户端 IP、`$7` URL、`$9` 状态码、`$10` 字节数。

```bash
# 1) Top10 来源 IP：awk 分组计数 + sort 计数排序
awk '{cnt[$1]++} END{for (ip in cnt) print cnt[ip], ip}' access.log | sort -rn | head
# 输出示例：4821 10.0.0.5 / 1902 192.168.1.100

# 2) 5xx 错误占比：grep 粗筛 + awk 算占比
grep -cE '" 5[0-9]{2} ' access.log
awk '{n++; if ($9 ~ /^5/) e++} END{printf "5xx: %d / %d (%.2f%%)\n", e, n, e*100/n}' access.log

# 3) 各接口请求量与平均响应字节：URL 作数组下标
awk '{cnt[$7]++; bytes[$7]+=$10}
     END{for (u in cnt) printf "%-40s 次数=%-6d 均字节=%.0f\n", u, cnt[u], bytes[u]/cnt[u]}' access.log

# 4) 14:00-15:00 的慢请求（日志末列为耗时秒）
grep "19/Nov/2026:14:" access.log | awk '$NF > 1.0 {print $7, $NF}' | sort -k2 -rn | head
```

### 3.2 组合技一：grep + awk 统计

```bash
# /var/log/auth.log 失败登录来源 IP Top5：grep 筛行、awk 倒数第 4 列分组
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -5
# 用 $(NF-3) 倒数取列，比硬编码列号抗格式变化
```

### 3.3 组合技二：find + sed 批量改名/改内容

```bash
# 1) 批量替换文件内容：先 grep -l 出清单，再 sed 批量改（-i.bak 留备份）
grep -rl "http://old.com" ./site --include="*.html" | xargs sed -i.bak 's|http://old\.com|https://new.com|g'

# 2) find + rename 批量改文件名：空格换下划线（Ubuntu 自带 file-rename）
find ./docs -name "* *.pdf" -print0 | while IFS= read -r -d '' f; do
  file-rename "s/ /_/g" "$f"
done

# 3) 只改 7 天内修改过的配置，先 dry-run 预览
find /etc/nginx -name "*.conf" -mtime -7 -exec sed -i.bak 's/worker_processes  1;/worker_processes  auto;/' {} +
```

> [!warning] 批量替换三步纪律
> 第一步 `grep -rl` 看清单，第二步加 `-i.bak` 执行，第三步 `diff` 抽查备份差异后清理。跳过第一步直接 `sed -i` 全目录替换，是改坏整站配置的最常见原因。

## 四、动手练习

练习环境：Ubuntu/Debian，先生成练习数据：

```bash
printf '%s\n' \
'10.0.0.5 - - [19/Nov/2026:10:23:01 +0800] "GET /api/users HTTP/1.1" 200 1234' \
'10.0.0.7 - - [19/Nov/2026:10:23:05 +0800] "GET /api/orders HTTP/1.1" 500 98' \
'10.0.0.5 - - [19/Nov/2026:10:23:09 +0800] "POST /api/login HTTP/1.1" 401 12' \
'192.168.1.100 - - [19/Nov/2026:10:24:12 +0800] "GET /api/users HTTP/1.1" 200 2345' \
> access.log
```

### 练习 1（热身）：grep 基础

统计 `access.log` 中 4xx/5xx 的请求行数，并显示每行的行号。
提示：`grep -nE` 一个正则同时匹配两种状态码。

### 练习 2（进阶）：awk 字段统计

用一条 awk 命令输出每个状态码出现的次数，按次数降序排列。
提示：关联数组 `cnt[$9]++` + `END` 块 + 外部 `sort -rn`。

### 练习 3（综合）：完整日志分析报表

写一条管道命令，输出：每个 IP 的请求次数、其中 5xx 次数，两列对齐显示，只列出出现过 5xx 的 IP。
提示：一个 awk 程序里用两个数组 `total[ip]++` 与 `err5[ip]++`（仅当 `$9 ~ /^5/`），`END` 里遍历 `err5` 即可。

> [!success]- 练习 3 参考答案要点
> ```bash
> awk '{t[$1]++; if ($9 ~ /^5/) e[$1]++}
>      END{for (ip in e) printf "%-16s 总=%-5d 5xx=%d\n", ip, t[ip], e[ip]}' access.log
> ```
> 要点：`$9 ~ /^5/` 状态码以 5 开头即 5xx；`e[$1]++` 条件成立才执行，未出现的不进数组；`for (ip in e)` 只遍历有 5xx 的 IP；`printf "%-16s"` 左对齐补空格，报表对齐靠它。

## 五、常见坑与 FAQ

> [!danger] sed -n 与 -i 同时用会截断文件
> `sed -ni 's/foo/bar/' file` 会把文件清空：`-n` 关闭自动打印，而 `-i` 的写回内容就是打印出来的内容。要么去掉 `-n`，要么显式 `p`（`sed -ni 's/foo/bar/p'`）。就地修改前永远先留备份 `-i.bak` 或先 `cp` 一份。

> [!warning] 正则方言不统一：BRE 里的 + 和 () 不生效
> `grep "ab+c"` 匹配不到 "abc"——BRE 里 `+` 是字面量。要么 `grep -E "ab+c"`，要么统一用 `-E`。搜 IP、路径这类含 `.` 的字面量用 `-F` 最稳：`.` 在正则里匹配任意字符，`grep "192.168.1.1"` 会误匹配 `192x168y1z1`。

> [!warning] awk 的 $NF 陷阱与 -F 空格陷阱
> `-F""`（无空格）会把**脚本原文**当成分隔符，`-F ""`（有空格）才是"每个字符一列"——gawk 手册明确提醒了这个书写差异。行尾含 `\r`（Windows 换行文件）时 `$NF` 会带 `\r`，用 `awk '{sub(/\r$/,"")}1'` 先清掉。另外修改 `OFS` 只对"重新赋值过的字段行"生效：只改 `BEGIN{OFS=","}` 而不触碰任何 `$n`，`print $1, $2` 仍用空格分隔。

> [!tip] 大文件先缩小再统计
> 处理上 GB 的日志，先 `grep` 粗筛（`-m 100` 找到即停）或按时间窗 `sed -n` 截取，再交给 awk 统计，比全量跑 awk 快一个数量级。`LC_ALL=C grep ...` 可跳过 UTF-8 解码，机械提速明显。

## 六、自检清单

- [ ] 能说出 grep/sed/awk 三者的分工与"过滤→编辑→分析"管道顺序
- [ ] 知道 BRE 与 ERE 的差异，会用 `-E` 和 `-F`
- [ ] 会用 `-r`、`--include`、`-C` 上下文、`-o` 只取匹配片段
- [ ] 会用 `sed -i.bak` 安全替换，理解 `-n` 与 `-i` 并用的截断风险
- [ ] 能解释 `NF`、`$NF`、`NR`、`FS`、`OFS` 五个内置变量
- [ ] 会用关联数组 + `END` 块做分组计数/求和（如 Top IP 统计）
- [ ] 会用 `grep -rl | xargs sed` 做批量替换，且遵循"清单→备份→diff"三步
- [ ] 能独立完成一道"状态码分布 + 错误来源 IP"的日志分析题

## 七、关联笔记与参考

**库内笔记：**

- [[Linux-从入门到精通]] —— 三剑客在阶段二学习路线中的位置
- [[Linux常用命令集]] —— 第三节文本命令速查与本篇互为详略
- [[Linux-Shell脚本编程]] —— 把三剑客组合封装进脚本
- [[Linux-性能排查实战]] —— 用 awk 快速聚合 `vmstat`/`iostat` 输出
- [[Linux-systemd服务管理]] —— `journalctl` 输出常用 grep/awk 过滤

**外部参考（均来自本次官方文档调研）：**

1. [man7.org — grep(1) 手册页](https://man7.org/linux/man-pages/man1/grep.1.html) —— 选项语义权威来源
2. [GNU sed 官方手册](https://www.gnu.org/software/sed/manual/sed.html) —— s 命令标志、地址语法、`-i` 备份规则
3. [GNU gawk 用户手册](https://www.gnu.org/software/gawk/manual/gawk.html) —— 内置变量、数组、printf 详解
