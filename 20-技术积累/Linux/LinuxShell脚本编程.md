---
title: Linux Shell 脚本编程
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累
  - Linux
  - Shell脚本
  - 运维
  - 自动化
aliases:
  - Shell脚本
  - Bash脚本
source: 网络资料整理
---

# Linux Shell 脚本编程

> [!摘要]
> 本篇聚焦 Linux 下的 Shell 脚本编程：以 **bash 5.3** 为基准解释器，从 shebang、变量、位置参数、条件与循环、函数、数组讲起，重点讲 `set -euo pipefail` 严格模式、`getopts` 参数解析、`trap` 清理，以及 `bash -n` / ShellCheck 的校验流程，并给出可直接落地的脚本模板与常见坑。定位是 [[Linux-从入门到精通]] 中「阶段二：进阶」的脚本专项，向上承接命令与文本处理，向下延伸自动化运维与定时任务（cron / systemd timer）。

## 一、最新动态（截至 2026-11）

- **bash 5.3（2025-07-04）为当前脚本基准解释器**：新增 `read -E`（行编辑时保留历史与编辑能力）、`source -p PATH`（打印并导出变量，便于检查运行环境）；命令替换语义有调整；源码已升级为 **C23** 合规，不再兼容 K&R 老式编译器，Readline 同步更新。本篇示例以 bash 5.3 为准，默认 shell 因发行版而异（Ubuntu 26.04 提供 bash 5.3）。
- **GNU coreutils 9.12（2026-09-14）**：脚本中调用的文本/文件命令版本基准。`env` 新增 `--env0-from=FILE`；`cut/nl/unexpand` 支持多字节字符；`cat/yes` 在 Linux 上使用零拷贝 I/O，处理大文件更快。
- **静态检查 ShellCheck 是脚本文档的标配工具**：虽非本次调研重点，但写脚本建议配合它做静态检查；`bash -n` 负责语法校验，二者分工不同。
- **可移植性提示**：脚本需区分 `sh`（POSIX）、`bash`、`zsh`，不要把 bash 专有语法（数组、`[[ ]]`、`function`）跑在 `/bin/sh` 上。
- 具体版本号与日期以 [GNU Bash 发布公告](https://lists.gnu.org/archive/html/info-gnu/2025-07/msg00001.html) 与 [GNU Coreutils 新闻](https://savannah.gnu.org/news/?group=coreutils) 为准，写作发布前建议按链接复核最新版本。

## 二、基础概念

Shell 脚本的本质：把一系列命令写入文本文件，由 shell 解释器逐行读取并执行。核心概念如下。

- **Shell 与解释器**：shell 是用户与内核之间的命令解释器。脚本首行用 shebang 声明解释器：`#!/bin/bash` 使用 bash，`#!/bin/sh` 使用 POSIX shell，跨环境时两者能力差异明显。
- **变量与引号**：变量以 `$VAR` 或 `${VAR}` 展开；单引号不展开、双引号展开但保留单词边界；反引号与 `$(...)` 是命令替换。引号使用是脚本正确性的第一道关。
- **位置参数与特殊变量**：`$0` 为脚本名、`$1`~`$9` 为位置参数、`$#` 为参数个数、`$@`/`$*` 为全部参数、`$?` 为上条命令退出码、`$$` 为当前进程 PID、`$!` 为后台任务 PID。
- **退出码**：0 表示成功，非 0 表示失败。脚本健壮性依赖退出码判断，而非只看输出内容。
- **管道与重定向**：`|`、`>`、`>>`、`2>&1`、`<`，配合文本处理命令完成数据流加工，是脚本处理日志与报表的基础。

## 三、核心机制

- **严格模式 `set -euo pipefail`**：`-e` 遇错即停、`-u` 对未定义变量报错、`-o pipefail` 让管道任一环节失败即整体失败，是生产脚本的默认起点。
- **参数解析 `getopts`**：配合 `shift` 循环处理 `-h`、`-f` 等短选项，是命令行脚本的标准做法。
- **函数与作用域**：`local` 声明局部变量，避免污染全局；函数内变量作用域不清是常见错误源。
- **数组**：bash 专有语法，`arr=(a b c)`、`${arr[i]}`、`"${arr[@]}"`，遍历必须加引号以保留元素边界。
- **信号与清理 `trap`**：捕获 `EXIT/INT/TERM` 等信号，执行临时文件清理与资源释放，保证脚本被中断时不留残渣。
- **子 shell 与命令替换**：`$(...)`、管道、`( ... )` 都会创建子 shell，其中的变量修改不会回传到父 shell，这是循环里 `cd` 失效、变量累加不生效的常见根因。

## 四、实践步骤（含代码/命令示例）

### 4.1 脚本骨架与严格模式

```bash
#!/usr/bin/env bash
# 示例：带严格模式、日志与帮助信息的脚本骨架
set -euo pipefail

log() { printf '[%s] %s\n' "$(date '+%F %T')" "$*" >&2; }
die() { log "错误: $*"; exit 1; }

main() {
    local opt
    while getopts ":h" opt; do
        case "$opt" in
            h) echo "用法: $0 -h"; exit 0 ;;
            \?) die "未知选项 -$OPTARG" ;;
            :) die "选项 -$OPTARG 需要参数" ;;
        esac
    done
    shift $((OPTIND - 1))
    log "开始执行，剩余参数: $*"
}

main "$@"
```

### 4.2 参数、函数、数组与 trap

```bash
#!/usr/bin/env bash
set -euo pipefail

tmpdir="$(mktemp -d)"
cleanup() { rm -rf -- "$tmpdir"; }
trap cleanup EXIT INT TERM

files=("$@")
for f in "${files[@]}"; do
    [[ -f "$f" ]] || { echo "跳过不存在的文件: $f" >&2; continue; }
    size=$(stat -c %s "$f")
    echo "$f -> $size 字节"
done
```

### 4.3 语法检查与静态检查

```bash
bash -n ./deploy.sh    # 仅做语法检查，不执行
shellcheck ./deploy.sh # 静态检查：未加引号、可疑用法、拼写问题等
bash -x ./deploy.sh    # 调试执行：打印每条命令及其展开结果
```

### 4.4 与文本处理、定时任务配合

```bash
# 用脚本统计 Nginx 日志，再挂到 cron / systemd timer
grep -c ' 404 ' /var/log/nginx/access.log
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# crontab -e：每天 02:00 执行备份脚本
# 0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

## 五、最佳实践与常见坑

- **首行用 `#!/usr/bin/env bash`**：避免依赖固定解释器路径，跨发行版更稳。
- **变量一律加双引号**：写 `"$var"`，防止空格与通配符被拆分；删除、复制等破坏性操作前先 `echo` 预演，删除路径务必带 `--` 并使用绝对路径。
- **不要依赖未定义变量**：`set -u` 会把 `$UNDEFINED` 变成致命错误，需要兜底时用 `${VAR:-默认值}` 或 `${VAR:?未设置}`。
- **数组与 `for` 展开加引号**：`"${arr[@]}"`，否则元素会被按单词拆分。
- **注意子 shell 陷阱**：在 `$(...)`、管道、`( )` 内修改的变量不会回传；需要保留结果时避免放进子 shell。
- **退出码与日志分离**：关键分支显式 `exit`，日志写向 `>&2` 与正常输出分离；调用外部命令后检查 `$?`，或直接依赖 `set -e`。
- **避免 bash 专有语法跑 `/bin/sh`**：`sh` 不支持数组与 `[[ ]]`，跨环境脚本尽量保持 POSIX 兼容。
- **改动前备份、先测后推**：批量改配置用 `sed -i.bak` 保留备份后缀，先在测试实例验证再推生产。

## 六、核心要点速查

| 主题 | 命令 / 语法 | 说明 |
|---|---|---|
| 严格模式 | `set -euo pipefail` | 遇错停、未定义变量报错、管道失败即失败 |
| 参数解析 | `getopts ":hf:" opt`、`shift $((OPTIND-1))` | 解析短选项并清空已处理参数 |
| 局部变量 | `local x=...` | 限定函数内作用域 |
| 信号清理 | `trap cleanup EXIT INT TERM` | 退出/中断时执行清理 |
| 语法检查 | `bash -n script.sh` | 不执行，仅校验语法 |
| 静态检查 | `shellcheck script.sh` | 脚本工程必备检查工具 |
| 调试执行 | `bash -x script.sh` | 打印命令与展开过程 |
| 特殊变量 | `$0 $# $? $$ $! $@` | 脚本名/参数数/退出码/PID |
| 数组遍历 | `for x in "${arr[@]}"` | 保留空白与元素边界 |
| 命令替换 | `$(cmd)` | 推荐替代反引号 |

## 七、学习资源

- [GNU Bash 官方主页](https://www.gnu.org/software/bash/) —— bash 官方发布与文档入口
- [GNU Bash 5.3 发布公告](https://lists.gnu.org/archive/html/info-gnu/2025-07/msg00001.html) —— `read -E`、`source -p PATH` 等变更说明
- [GNU Coreutils 新闻](https://savannah.gnu.org/news/?group=coreutils) —— `env --env0-from=FILE` 等工具版本记录
- [ShellCheck 官网](https://www.shellcheck.net/) —— 脚本静态检查工具与 Wiki
- [man7.org](https://www.man7.org/) —— bash(1)、getopts、trap 等权威手册
- [The Linux Command Line（免费在线书）](https://www.linuxcommand.org/) —— 命令与脚本的系统化讲解

## 八、关联笔记

- [[Linux-从入门到精通]] —— 本知识点在 Linux 学习路线中的位置与阶段划分
- [[Linux常用命令集]] —— 脚本中高频命令的速查参考
- [[Linux系统管理与运维要点]] —— 脚本落地的自动化运维场景

## 九、变更记录

- 2026-11-19：首次创建。
