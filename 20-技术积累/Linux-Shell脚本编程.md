---
title: Linux-Shell脚本编程
date: 2026-11-19
tags:
  - 技术积累
  - Linux
  - Shell
  - Bash
  - 脚本编程
aliases:
  - Shell 脚本
  - Bash 编程
---

# Linux-Shell脚本编程

> [!abstract] 摘要
> Shell 脚本是把命令组合成可复用自动化流程的手段：备份、巡检、部署、日志清理都靠它。本篇覆盖变量与引号、条件与循环、函数、数组、getopts 参数处理、`set -euo pipefail` 严格模式与调试方法，最后给出两个生产可用的完整脚本，是 [[Linux-从入门到精通]] 阶段二"脚本"知识点的展开，配合 [[Linux-文本三剑客实战]] 的文本处理能力使用。

## 一、概念与原理

Shell 脚本的执行模型：逐行解析 → 展开（变量替换、通配符、命令替换）→ 分词 → 执行。理解"展开发生在执行之前"是理解引号规则的关键。本篇以 Bash 为准（Ubuntu 默认 shell）。

```mermaid
graph LR
    A[脚本文件] --> B[逐行读取解析]
    B --> C["展开阶段<br/>变量替换 / 命令替换 $(...)"]
    C --> D["分词与通配符匹配<br/>未加引号才会分词"] --> E[执行命令]
```

**工程化基线**（与 [[Linux系统管理与运维要点]] 的脚本规范一致）：`#!/usr/bin/env bash` 开头、`set -euo pipefail` 严格模式、所有变量展开加双引号、上线前用 [ShellCheck](https://www.shellcheck.net/) 静态检查过一遍。

> [!info] 环境
> 本文脚本均在 Ubuntu/Debian 的 bash 5.x 下验证。`#!/bin/sh` 走的是 dash（Ubuntu 的 sh 链接指向 dash），不支持数组与 `[[ ]]`，切勿混用。

## 二、核心语法 / 命令详解

### 2.1 变量与引号规则

```bash
name="world"              # 赋值时 = 两边不能有空格
echo "hello, $name"       # 双引号：变量展开 → hello, world
echo 'hello, $name'       # 单引号：原样输出 → hello, $name
echo "hello, ${name}ly"   # 变量名与后文字符粘连时用 {} 定界
files="a b c"; echo $files; echo "$files"   # 不加引号分 3 词（危险）；加引号是 1 个参数
d=$(date +%F)             # 命令替换：把命令输出赋给变量
LOG="${LOG_FILE:-/var/log/app.log}"   # 默认值：未设置则用后备
: "${SRC_DIR:?未设置 SRC_DIR}"        # 兜底：未设置时报错退出（严格模式救星）
```

> [!tip] 引号判定口诀
> 双引号内：`$` 仍生效（展开变量/命令）；单引号内：一切原样；**不加引号**：展开后还要经历分词和通配符匹配。脚本里默认"所有 `$var` 都写 `"$var"`"，确定要分词时才去掉引号。

### 2.2 条件判断：test、[ ] 与 [[ ]]

```bash
if [ "$a" = "$b" ]; then echo "相等"; fi          # 经典 test（POSIX，注意空格）
if [ "$n" -gt 10 ] || [ ! -x app.sh ]; then echo "数值条件/文件测试"; fi
# 数值比较：-eq -ne -gt -ge -lt -le；文件测试 -f -d -e -x -r -w -s；! 取反

if [[ $file == *.log ]]; then echo "通配匹配"; fi     # Bash 扩展：无需引号包变量
if [[ $num =~ ^[0-9]+$ ]]; then echo "正则匹配：纯数字"; fi   # =~ 正则
if [[ -f "$f" && -r "$f" ]]; then echo "与逻辑"; fi   # && || 可直接用
if (( count > 3 )); then echo "count>3"; fi       # 算术判断
```

### 2.3 循环与 case

```bash
for f in /var/log/*.log; do echo "处理 $f"; done          # 列表循环
for i in {1..5}; do echo "第 $i 次"; done                  # 序列循环

while IFS= read -r line; do echo "行内容: $line"; done < /etc/hostname
# IFS= 保留行首空格；-r 防止反斜杠转义（读文件的标准姿势）

while ! curl -fsS --max-time 2 http://127.0.0.1:8080/health; do sleep 2; done
# 无限循环 + break 的等价形态：不健康就一直等

case "$1" in                                              # 服务控制脚本标配
  start)   echo "启动";;
  stop)    echo "停止";;
  status)  echo "查询状态";;
  *)       echo "用法: $0 {start|stop|status}"; exit 1;;
esac
```

### 2.4 函数与返回值

```bash
log() {
  local level="$1"; shift                                 # local 声明局部变量
  echo "[$(date '+%F %T')] [$level] $*" | tee -a /var/log/myscript.log
}
log INFO "开始备份"                                        # 调用时不加括号

is_running() { systemctl is-active --quiet "$1"; }        # return 即退出码 0-255
if is_running nginx; then echo "nginx 在跑"; fi           # if 直接消费返回码

get_top_ip() { awk '{print $1}' "$1" | sort | uniq -c | sort -rn | head -1 | awk '{print $2}'; }
top="$(get_top_ip access.log)"                            # "返回字符串"走 stdout 捕获
```

### 2.5 数组

```bash
servers=(web1 web2 db1)                 # 定义
echo "${servers[0]}"                    # 第一个元素；${#servers[@]} 元素个数
servers+=("cache1")                     # 追加
for s in "${servers[@]}"; do ping -c1 "$s"; done   # 遍历（引号包住防分词）
mapfile -t files < <(find /var/log -name "*.log" -mtime -1)   # 逐行读入数组，${#files[@]} 计数
```

### 2.6 参数处理：getopts 与位置参数

```bash
# getopts：解析 -n 带值等短选项；OPTARG=选项参数值，OPTIND=处理进度
while getopts "n:h" opt; do
  case "$opt" in
    n) NAME="$OPTARG";;
    h) echo "用法: $0 [-n 名称] [-h]"; exit 0;;
    *) echo "用法: $0 [-n 名称] [-h]"; exit 1;;   # 未知选项，getopts 自己会报错
  esac
done
shift $((OPTIND - 1))            # 剩下的 $1 $2 ... 是位置参数（如目标文件）
# 兜底：NAME="${NAME:-默认值}"，配合 set -u 必须给默认或强制传参
```

### 2.7 set -euo pipefail 严格模式

```bash
set -e          # 任何命令非零退出码 → 立即退出脚本
set -u          # 使用未定义变量 → 报错退出
set -o pipefail # 管道中任何一段失败 → 整条管道算失败（默认只看最后一段）
# 惯用一行写法：set -euo pipefail
```

依据 [GNU Bash 手册 set 内建](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)，`-e` 有这些**不退出**的例外：条件在 `if`/`while` 的测试里、在 `&&`/`||` 链中非最后位置、取反 `!` 的命令。所以"可能失败但无所谓"的命令要显式处理：

```bash
grep -q "ERROR" app.log || true            # 明确容忍失败；或放进 if（-e 不生效）
```

### 2.8 调试手段

```bash
bash -x script.sh        # 打印每条展开后的命令，定位变量值
bash -n script.sh        # 只做语法检查不执行
set -x                   # 脚本内开启跟踪，set +x 关闭
shellcheck script.sh     # 静态分析（sudo apt install shellcheck）
```

ShellCheck 常见报警：`SC2086` 变量要加引号防分词、`SC2034` 定义了未使用的变量、`SC2046` 命令替换结果要加引号。每个编号在 [ShellCheck Wiki](https://www.shellcheck.net/wiki/) 有详解与修复示例。

## 三、实战案例

### 3.1 案例 A：自动化备份脚本（压缩 + 日志 + 清理，Ubuntu 22.04/24.04）

```bash
#!/usr/bin/env bash
# backup.sh —— 目录备份：tar 压缩 → 记日志 → 清理过期备份
set -euo pipefail

SRC="/opt/app/data"                       # 要备份的目录（配置区集中在顶部）
DST="/backup"                             # 备份存放目录
KEEP_DAYS=7                               # 本地保留天数
LOG_FILE="/var/log/backup.log"
STAMP=$(date +%F_%H%M%S)
OUT="${DST}/data-${STAMP}.tar.gz"
LOCK="/var/run/backup.lock"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG_FILE"; }

exec 9>"$LOCK" && flock -n 9 || { log ERROR "已有备份在运行"; exit 1; }   # flock 防并发

[[ -d "$SRC" ]] || { log ERROR "源目录不存在: $SRC"; exit 1; }   # 严格模式下显式校验
[[ -d "$DST" ]] || mkdir -p "$DST"

TMP="${OUT}.tmp"
cleanup() { rm -f "$TMP"; }               # trap：无论成败都清临时文件
trap cleanup EXIT

log INFO "开始备份 $SRC"
tar -czf "$TMP" -C "$(dirname "$SRC")" "$(basename "$SRC")"
mv "$TMP" "$OUT"                          # 原子改名，避免读到半截包
log INFO "完成: $OUT ($(du -h "$OUT" | cut -f1))"

# 清理过期备份（find -mtime 语法见 [[Linux常用命令集]]）
find "$DST" -name 'data-*.tar.gz' -mtime "+$KEEP_DAYS" -print -delete | while read -r f; do
  log INFO "清理过期: $f"
done
log INFO "备份流程结束"
```

配套 systemd timer 挂载方式见 [[Linux-systemd服务管理]] 第三节；`flock` 防并发与 `trap` 清理是 [[Linux系统管理与运维要点]] 中备份模板的核心手法。

### 3.2 案例 B：日志巡检脚本

```bash
#!/usr/bin/env bash
# inspect_log.sh —— 巡检应用日志：错误计数 + Top 错误类型 + 超阈值告警退出
set -euo pipefail

LOG="/var/log/app/app.log"
THRESH=${1:-100}                          # 第1个参数：错误数阈值，默认100
[[ -f "$LOG" ]] || { echo "日志不存在: $LOG"; exit 1; }

# 今日 0 点之后的错误行计数（日期匹配依赖日志格式，按需调整）
TODAY=$(date +%F)
ERR_COUNT=$(awk -v d="$TODAY" '$0 ~ d && /ERROR/' "$LOG" | wc -l)

echo "===== 巡检报告 $(date '+%F %T') ====="
echo "日志文件: $LOG（$(du -h "$LOG" | cut -f1)）"
echo "今日 ERROR: $ERR_COUNT 条（阈值 $THRESH）"

# Top5 错误类型：取 ERROR 行的第 4 列分组计数（字段按实际日志调整）
awk '/ERROR/ {print $4}' "$LOG" | sort | uniq -c | sort -rn | head -5 | \
  while read -r n msg; do echo "  $n  $msg"; done

if (( ERR_COUNT > THRESH )); then
  echo "状态: 异常（超过阈值）"
  exit 2                                  # 约定退出码 2 = 告警，方便接入监控
fi
echo "状态: 正常"
```

## 四、动手练习

### 练习 1（热身）：引号与变量

写一行命令：把变量 `BIN_DIR` 设为 `/usr/local/bin`，输出字符串 `当前目录: /usr/local/bin`，要求变量展开而非硬编码路径。
提示：双引号展开变量；再故意把变量命名成 `PATH` 观察 `echo "$PATH"`，体会与内置变量撞名的问题。

### 练习 2（进阶）：函数、数组与 getopts

写一个脚本，支持 `./avg.sh -n 3 88 92 79`（`-n` 指定个数）计算平均值（保留 1 位小数）；数字参数用数组接收，计算逻辑封装成 `avg()` 函数。
提示：`getopts` 取 `-n`，`shift $((OPTIND-1))` 后用 `"$@"` 填数组；`printf "%.1f"` 格式化。

### 练习 3（实战）：写一个服务健康检查脚本

要求：① 接收服务名（如 `nginx`）作为参数，缺失时打印用法并以非零退出；② 用 `systemctl is-active` 判断状态，不活跃则尝试 `restart`；③ 重启后再 `curl -fsS --max-time 5` 探测 `http://127.0.0.1:8080/health`，失败输出告警并以退出码 2 结束；④ 全程 `set -euo pipefail`，日志统一走 `log()` 函数；⑤ `shellcheck` 检查通过后实际跑一次。

> [!success]- 练习 3 参考答案要点
> ```bash
> #!/usr/bin/env bash
> # health_check.sh —— 服务健康检查：不活跃则重启，再探测 HTTP 健康端点
> set -euo pipefail
> SVC="${1:-}"; URL="http://127.0.0.1:8080/health"
> log() { echo "[$(date '+%F %T')] $*"; }
> if [[ -z "$SVC" ]]; then echo "用法: $0 <服务名>"; exit 1; fi
> if ! systemctl is-active --quiet "$SVC"; then
>   log "服务 $SVC 未运行，尝试重启"; sudo systemctl restart "$SVC"
> fi
> if curl -fsS --max-time 5 "$URL" >/dev/null; then
>   log "健康检查通过"; exit 0
> else
>   log "健康检查失败: $URL 无响应" >&2; exit 2
> fi
> ```
> 关键点：`[[ -z "$SVC" ]]` 校验参数；`systemctl is-active --quiet` 静默输出只用退出码；`curl -f` 把 HTTP 4xx/5xx 变成非零退出码（否则 500 也算"成功"）；错误信息 `>&2` 重定向到 stderr；退出码 0/1/2 语义分明，可被监控系统消费。

## 五、常见坑与 FAQ

> [!danger] 未加引号的变量展开 + rm 是脚本事故之王
> `rm -rf "$DIR/"*` 在 `DIR` 为空时的行为已在 [[Linux-从入门到精通]] 中复盘；脚本侧的根治手段是 `set -u`（未定义变量直接报错）+ 删除前校验 `[[ -d "$DIR" ]]` + 兜底语法 `: "${DIR:?未设置}"`。三层防御成本极低，建议成为写脚本的本能。

> [!warning] set -e 不是万能保险
> 依据 Bash 手册，`-e` 在 `if`/`&&`/`||` 上下文中失效（设计行为），所以必须配合 `pipefail`：`curl url | grep ok` 中 curl 失败时，没有 pipefail 脚本会照常往下走。另一个高频坑：`(( ))` 算出结果为 0 时返回非零码，在 `-e` 下会让脚本意外退出，改用 `if (( x > 0 ))` 形式。

> [!warning] [[ 与 [ 混用、sh 与 bash 混用
> `[[` 是 Bash 关键字（支持 `=~` 正则与通配匹配），`[` 是普通命令（POSIX）；把 `[[` 写进 `#!/bin/sh` 脚本，Ubuntu 下会因 dash 报 `Syntax error`。同理 `(( ))`、数组、`local`、getopts 循环里的 Bash 语法都是 Bash 特性。要么 shebang 用 bash 并只写 Bash 语法，要么全文写 POSIX——不要混。

> [!tip] 让脚本可被别人放心复用
> 三个低成本高回报的习惯：① 配置项集中在脚本顶部或支持环境变量覆盖；② 退出码有约定（0 成功 / 非 0 失败类别）；③ 用 getopts 提供 `-h` 帮助分支。再加上 ShellCheck 与 `bash -x` 两个工具，脚本质量即可达到可入库水平。

## 六、自检清单

- [ ] 能说清单引号/双引号/不加引号三种展开行为差异
- [ ] 习惯性写 `set -euo pipefail`，并能解释 `-e` 在 `if`/`&&` 中失效的例外
- [ ] 会用 `[[ =~ ]]` 正则判断与 `case` 多分支
- [ ] 会写函数：`local` 变量、return 状态码、stdout 返回字符串两种返回语义
- [ ] 会定义/遍历数组，知道 `"$arr[@]"` 加引号的必要性
- [ ] 会用 getopts 解析短选项（OPTARG/OPTIND/shift 三件套）
- [ ] 会用 `bash -x` 与 ShellCheck 定位脚本问题（知道 SC2086 是什么）
- [ ] 独立写过含 trap 清理、日志函数、退出码约定的完整脚本

## 七、关联笔记与参考

**库内笔记：**

- [[Linux-从入门到精通]] —— Shell 脚本在阶段二的学习目标与推荐书单
- [[Linux-文本三剑客实战]] —— 脚本内文本处理的三件套
- [[Linux系统管理与运维要点]] —— 运维脚本模板（备份/巡检）与 ShellCheck 规范
- [[Linux-systemd服务管理]] —— 脚本注册成 systemd 服务/timer 的后续步骤
- [[Linux-权限与用户管理]] —— 脚本文件的执行权限与属主管理

**外部参考（均来自本次官方文档调研）：**

1. [GNU Bash 手册 — The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) —— `-e/-u/-o pipefail` 的精确语义与例外
2. [ShellCheck 官网与 Wiki](https://www.shellcheck.net/wiki/) —— SC2086/SC2034/SC2046 等规则详解
3. [GNU Bash 手册 — Shell 参数展开](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html) —— `${var:-}`、`${var:?}` 等兜底语法
