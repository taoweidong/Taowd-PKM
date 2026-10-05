---
source: "https://cuiqingcai.com/"
title: "静觅丨崔庆才的个人站点 - Python爬虫教程"
fetched_at: "2026-10-05 15:43:34"
---

##  技术教程 __ [OpenCode 对接 Google 搜索 MCP](/3045801.html)

> 📘 **Overview** ：[OpenCode MCP Overview →](https://platform.acedata.cloud/documents/opencode-mcp-all)

你在远程服务器上用 OpenCode 排查一个 OOM 问题，看到一条不太熟悉的内核日志。以前只能复制错误信息、断开终端、切到本地浏览器搜索，再切回来。接上 Serp MCP Server 后，OpenCode 可以直接在终端里搜 Google，不需要离开命令行就能完成“看日志 → 搜资料 → 改代码”整条链路。

Google 搜索 MCP 适合在 OpenCode 里调试生产问题、做技术选型调研、查官方文档、找 GitHub issue，以及任何需要“搜索网页才能继续工作”的场景。

## 获取 API Token

使用 Google 搜索 MCP Server 之前，需要先准备一个 Ace Data Cloud API Token。OpenCode 和 Claude Code 共用一套 Token，获取流程一样：

  1. 打开 [Ace Data Cloud 控制台 - 应用列表](https://platform.acedata.cloud/console/applications)，获取您的 API Token，留作备用。
  2. 如果你尚未登录或注册，会自动跳转到登录页面；登录注册之后会自动返回当前页面。
  3. 首次申请时会有免费额度赠送，可以先免费体验 Google 搜索 MCP 服务。

![获取 Ace Data Cloud API Key](https://cdn.acedata.cloud/dvc3cg.jpg)

一个 Token 可以使用 Ace Data Cloud 提供的全部 MCP Server，无需为 Google 搜索 单独申请。文档和截图里建议只展示脱敏形式，例如 `YOUR_ACEDATACLOUD_API_KEY`，不要把完整 Token 贴到公开仓库、Issue、截图或聊天记录里。

> 想用 Claude Desktop / Claude.ai 网页版直接 OAuth 一键授权？请看 [Google 搜索 MCP 的 Claude.ai / Desktop 教程](https://platform.acedata.cloud/documents/claude-mcp-serp)。

## 配置 OpenCode

OpenCode 用一份 `opencode.json` 描述所有 MCP Server，文件可以放在两处，按下面”作用范围”选一种即可。两种位置的字段结构完全相同，区别只是优先级。

强烈推荐先把 Token 写到环境变量里：


    1


|


    export ACEDATACLOUD_API_KEY="替换为你的真实 Token"


---|---

然后在 `opencode.json` 里用 `{env:ACEDATACLOUD_API_KEY}` 占位符引用，避免真实 Token 写进文件。

### 全局：所有项目共用

文件位置：`~/.config/opencode/opencode.json`，适合”我自己的机器，一次配好，所有项目都能用”。


    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12


|


    {
      "$schema": "https://opencode.ai/config.json",
      "mcp": {
        "serp": {
          "type": "remote",
          "url": "https://serp.mcp.acedata.cloud/mcp",
          "enabled": true,
          "oauth": false,
          "headers": { "Authorization": "Bearer {env:ACEDATACLOUD_API_KEY}" }
        }
      }
    }


---|---

> ⚠️ `"oauth": false` 不可省略。AceData 的 MCP Server 使用 Bearer Token 鉴权，不走 OAuth 流程；OpenCode 默认会把 401 当成 OAuth 挑战自动重定向，导致 `opencode mcp list` 出现 `SSE error: Non-200 status code (401)`。显式声明 `"oauth": false` 让 OpenCode 直接以 `Authorization: Bearer ...` 调用，`opencode mcp debug serp` 也会回显 `OAuth explicitly disabled`，代表生效。

### 项目级：仅当前项目生效

文件位置：当前项目根目录下的 `opencode.json`，会**覆盖** 全局配置。适合团队共享、单仓库定制，或者只在某个项目里临时启用某个 MCP。


    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12


|


    {
      "$schema": "https://opencode.ai/config.json",
      "mcp": {
        "serp": {
          "type": "remote",
          "url": "https://serp.mcp.acedata.cloud/mcp",
          "enabled": true,
          "oauth": false,
          "headers": { "Authorization": "Bearer {env:ACEDATACLOUD_API_KEY}" }
        }
      }
    }


---|---

如果项目级 `opencode.json` 会被提交到 Git，请确保用 `{env:ACEDATACLOUD_API_KEY}` 占位符而不是真实 Token，避免泄露。

> 💡 如果 Shell 里的 `.env` 没有显式 `export`，需要用 `set -a && source .env && set +a` 才能把变量传给 OpenCode 进程，否则 `opencode debug config` 会显示 `"Authorization": "Bearer "`（占位符没解析）。

## 验证连接

配置后运行：


    1
    2


|


    opencode mcp list
    opencode mcp debug serp


---|---

看到 `serp connected` 即表示握手成功。失败时检查 `ACEDATACLOUD_API_KEY` 是否已导出、`oauth` 是否为 `false`，以及 `Authorization` 是否包含 `Bearer` 前缀。模型和工具 Schema 会持续变化，请从当前目录选择支持原生工具调用的模型。

## 典型场景

配置完成后，直接在 OpenCode 会话里用自然语言即可调用，无需先切到 `/mcp`：

**调试生产问题**


    1


|


    搜索 nginx 502 bad gateway response header too large 怎么解决


---|---

**技术选型调研**


    1


|


    搜索一下 2025 年 Python 异步 ORM 的性能对比，SQLAlchemy 2.0 async vs Tortoise ORM


---|---

**查官方文档**


    1


|


    搜索 Kubernetes CronJob concurrencyPolicy 的官方文档，Forbid 和 Replace 的区别


---|---

## 工具列表

下表列出主要工具；可通过 `curl -X POST https://serp.mcp.acedata.cloud/mcp -H 'Authorization: Bearer <token>' -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'` 获取当前完整清单：

工具 | 说明
---|---
serp_google_search | Google 网页搜索，支持指定国家、语言、时间范围
serp_google_images | Google 图片搜索
serp_google_news | Google 新闻搜索
serp_google_videos | Google 视频搜索
serp_google_maps / serp_google_places | 地图 / 本地商户搜索

## 相关链接

  * [Google 搜索 MCP Server（GitHub）](https://github.com/AceDataCloud/SerpMCP)
  * [Claude + Google 搜索 MCP 图文教程（claude.ai / Desktop）](https://platform.acedata.cloud/documents/claude-mcp-serp)
  * [OpenCode MCP Overview](https://platform.acedata.cloud/documents/opencode-mcp-all)
  * [OpenCode 终端配置教程](https://platform.acedata.cloud/documents/mcp-tutorials-opencode)
  * [MCP 协议官网](https://modelcontextprotocol.io)

__ 作者 [崔庆才](/authors/崔庆才) __ 发表于 2026-09-10 __ 阅读次数： __ 本文字数： 3.1k __ 阅读时长 ≈ 3 分钟
