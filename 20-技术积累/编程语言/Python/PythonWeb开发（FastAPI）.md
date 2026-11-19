---
title: Python Web 开发（FastAPI）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - Python
  - Web开发
  - FastAPI
  - ASGI
aliases:
  - FastAPI 开发指南
  - FastAPI 实战
source: 网络资料整理
---

# Python Web 开发（FastAPI）

> [!摘要] 摘要
> 本文系统讲解用 Python 构建现代 Web API 的主流方案——**FastAPI**：从 ASGI 运行模型、Pydantic 类型校验、路径/查询/请求体参数，到依赖注入、异步路由、项目结构、测试与部署，形成一条可直接落地的实战路径。截至 2026-11，FastAPI 最新版 **0.162.3** 已正式支持 **Python 3.15**，底层为 **Starlette 1.9.0**（ASGI）+ **Pydantic 2.14**。适合已掌握 Python 基础、准备用 FastAPI 做接口开发，或从 Flask / Django 迁移的开发者。

## 一、最新动态（截至 2026-11）

- **FastAPI 最新 0.162.3（2026-11）**：新增对 **Python 3.15** 的支持（PR #16727）；锁定依赖 **Pydantic 2.14.3**（PR #16728）；0.162.0 于 2026-11 前后发布。
- **底层依赖**：**Starlette 1.9.0**（2026-10/11，ASGI 框架）与 **Pydantic v2**，二者是 FastAPI 运行与校验的两块基石。
- **Pydantic 2.14（2026-10-07）**：支持 Python 3.15、**放弃 Python 3.9**；`MISSING` 哨兵稳定化（字段未提供时序列化排除）；支持 PEP 810 延迟导入（跨模块模型引用更省启动时间）、`TypeForm`、`frozendict`（PEP 814）；`create_model()` 新增 `__namespace__` 参数。
- **Pydantic 版本线**：v2.13.0（2026-04-13）、v2.13.5；`pydantic.v1` 命名空间匹配 1.10.26（支持 Python 3.14）；**v2.14.3 为 FastAPI 当前锁定版本**。
- **配套工具链**：Python 3.15.2（2026-10-25）、pip 26.3（2026-11-02）、uv 0.13.7（2026-11-03，0.13.0 起将 Python 3.15 设为默认稳定版）、pytest 9.1.1（2026-11-07）、mypy 2.4、pyright 1.1.413。
- **选型判据**：FastAPI 0.162.3、Pydantic 2.14、Starlette 1.9.0 均已支持 Python 3.15，可作为「已可上生产」的版本组合依据；版本号更新频繁，实际以当日 PyPI 与官方发布页为准。

## 二、基础概念

- **ASGI（Asynchronous Server Gateway Interface）**：异步服务网关接口，是 FastAPI 的运行底座。与传统 WSGI（Flask 使用）相比，ASGI 原生支持 `async/await`，可在同一进程内并发处理大量长连接请求。
- **Starlette**：FastAPI 底层使用的轻量 ASGI 框架，负责请求分发、中间件与响应组装；FastAPI 在其之上叠加了类型驱动的校验与依赖注入。
- **Pydantic**：基于 Python 类型注解的数据校验与序列化库。FastAPI 用它把函数签名直接翻译成校验规则与 OpenAPI 文档，是「类型即校验」的核心。
- **路由与端点**：用装饰器（`@app.get`、`@app.post` 等）把「HTTP 方法 + 路径」绑定到处理函数。
- **依赖注入（Dependency Injection）**：用 `Depends()` 声明接口所需的资源（数据库连接、当前用户、配置等），FastAPI 自动解析、缓存并在请求结束后执行清理。
- **自动文档**：FastAPI 依据类型注解自动生成 OpenAPI（`/openapi.json`）与 Swagger UI（`/docs`），无需手写接口文档。

## 三、核心机制

**1. 类型注解驱动校验。** 处理函数的参数类型就是校验规则：路径参数、查询参数、请求体、请求头分别用不同方式声明，校验失败自动返回结构化的 422 错误响应。

**2. Pydantic v2 数据模型。** 用 `BaseModel` 定义数据契约，`Field` 描述约束，`response_model` 约束返回结构并做输出裁剪，避免把内部字段泄露给前端。

**3. 异步运行模型。** FastAPI 的路由函数可以是 `async def`（在事件循环内执行）或普通 `def`（FastAPI 自动放入线程池执行）。这一机制决定了阻塞 I/O 的处理方式。

**4. 依赖注入与生命周期。** 依赖可以是普通函数或带 `yield` 的生成器：生成器依赖在响应返回**之后**才执行 `yield` 之后的清理逻辑，是管理连接关闭的标准方式。

**5. 文档自动生成。** 校验规则、参数描述、响应模型都会被写入 OpenAPI，Swagger UI 与 ReDoc 开箱即用。

## 四、实践步骤（含代码/命令示例）

**1. 环境准备（uv 创建项目）**

```bash
uv init fastapi-demo
cd fastapi-demo
uv add "fastapi>=0.162.3" "uvicorn[standard]>=0.35"
uv add --dev "pytest>=9" "httpx>=0.28"
```

**2. 项目结构**

```text
fastapi-demo/
├── pyproject.toml
├── main.py           # 应用入口与路由
└── tests/
    └── test_main.py
```

**3. 最小可运行应用**

```python
from fastapi import FastAPI

app = FastAPI(title="我的第一个 FastAPI 服务")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, FastAPI"}
```

**4. 数据模型与请求校验**

```python
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=64, description="商品名称")
    price: float = Field(gt=0, description="必须为正数")
    count: int = Field(default=1, ge=0, description="库存，默认 1")
```

**5. 路径、查询参数与请求体**

```python
@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None, limit: int = 10) -> dict:
    # item_id 为路径参数，q 与 limit 为查询参数
    return {"item_id": item_id, "q": q, "limit": limit}


@app.post("/items/", status_code=201, response_model=Item)
def create_item(item: Item) -> Item:
    # item 为 JSON 请求体，类型即校验规则
    return item
```

**6. 依赖注入（含认证与清理）**

```python
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


def get_token(x_token: str = Header(default="")) -> str:
    if not x_token:
        raise HTTPException(status_code=401, detail="未提供令牌")
    return x_token


@app.get("/me")
def me(token: str = Depends(get_token)) -> dict:
    return {"token": token}
```

**7. 异步与同步路由的取舍**

```python
import asyncio


@app.get("/async")
async def async_route() -> dict:
    await asyncio.sleep(0.1)  # 非阻塞等待，不卡事件循环
    return {"ok": True}


@app.get("/blocking")
def blocking_route() -> dict:
    # 同步函数：FastAPI 自动放入线程池执行，避免阻塞事件循环
    return {"ok": True}
```

**8. 启动与文档**

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动后访问 Swagger UI：`http://127.0.0.1:8000/docs` ，OpenAPI 描述：`http://127.0.0.1:8000/openapi.json` 。

**9. 测试（TestClient）**

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Hello, FastAPI"


def test_create_item():
    resp = client.post("/items/", json={"name": "书", "price": 9.9})
    assert resp.status_code == 201
    assert resp.json()["name"] == "书"


def test_create_item_invalid():
    resp = client.post("/items/", json={"name": "", "price": -1})
    assert resp.status_code == 422  # 校验失败
```

```bash
uv run pytest -q
```

## 五、最佳实践与常见坑

- **版本基线**：新项目从 Python 3.13+ 起步。截至 2026-11，推荐组合为 **FastAPI 0.162.3 + Pydantic 2.14 + Starlette 1.9.0**；Pydantic 2.14 已放弃 Python 3.9，不要沿用旧环境。
- **`async def` 与 `def` 的选择**：性能关键路径用 `async` + 异步驱动库（如 `asyncpg`、`aiomysql`）；涉及阻塞调用（`time.sleep`、`requests`、同步 ORM）时改用普通 `def`，让 FastAPI 走线程池。**不要在协程里直接调用阻塞代码**，否则会卡住整个事件循环。
- **校验要写在模型里**：用 `Field(min_length/max_length/gt/ge)` 表达约束，错误信息与文档自动生成，避免在业务函数里手写一堆 `if`。
- **输出裁剪**：用 `response_model` 声明返回结构，防止内部字段被意外返回；敏感字段用 `Field(exclude=True)`。
- **依赖注入的清理时机**：用 `yield` 依赖管理连接，注意其作用域（请求级 vs 应用级），避免在请求级依赖中缓存本应隔离的状态。
- **文件上传**：用 `UploadFile` 接收，限制上传大小、校验文件类型与存储路径，防止路径穿越与超大请求体。
- **安全基线**：认证用 `fastapi.security`（API Key / OAuth2），密码使用 bcrypt / argon2 加盐哈希，CORS 使用白名单，SQL 一律参数化。
- **性能与稳定性**：限流、超时、请求体大小限制放在反向代理或网关层；生产部署用多 worker（如 `gunicorn -k uvicorn.workers.UvicornWorker`，Windows 可直接用 Uvicorn），前置 Nginx 处理静态资源与 TLS。
- **版本时效**：第三方库补丁版本更新频繁，文中版本号以 2026-11 调研为准，实际使用请以当日 PyPI 与官方发布页为准。

## 六、核心要点速查

1. FastAPI 最新版 **0.162.3**（2026-11），已支持 **Python 3.15**；底层为 **Starlette 1.9.0** + **Pydantic v2**。
2. Pydantic **2.14**（2026-10-07）支持 Python 3.15、放弃 3.9；`MISSING` 稳定化、支持 PEP 810 延迟导入与 `frozendict`；FastAPI 锁定 **Pydantic 2.14.3**。
3. FastAPI 的核心能力：**类型注解自动校验、自动 OpenAPI/Swagger 文档、原生 `async/await`、依赖注入**。
4. 参数来源：路径参数直接声明在路径中，查询参数用普通带默认值的参数，请求体用 Pydantic 模型，请求头用 `Header`。
5. 校验失败返回 **422**，错误结构由 Pydantic 自动生成。
6. **`async def`** 用于异步 I/O；**`def`** 由 FastAPI 放入线程池，用于阻塞操作，二者不可混用阻塞代码。
7. `Depends()` 支持 `yield` 依赖，响应返回后执行清理，是连接生命周期管理的标准方式。
8. 测试用 `fastapi.testclient.TestClient`，可直接驱动应用并断言状态码与响应体。
9. 部署：`uvicorn main:app --reload` 开发；生产多 worker + 反向代理。
10. 版本与 PEP 事实均以官方仓库为准，写文档时不要臆造版本号。

## 七、学习资源

- [FastAPI 官方文档（含教程与示例）](https://fastapi.tiangolo.com/)
- [FastAPI Release Notes](https://fastapi.tiangolo.com/release-notes/)
- [FastAPI GitHub Releases](https://github.com/fastapi/fastapi/releases)
- [Pydantic v2.14: Python 3.15 Support, Lazy Imports, TypeForm & More](https://pydantic.dev/articles/pydantic-v2-14-release)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
- [Starlette GitHub Releases（ASGI 框架）](https://github.com/encode/starlette/releases)
- [Uvicorn 官方文档（ASGI 服务器）](https://www.uvicorn.org/)
- [ASGI 规范](https://asgi.readthedocs.io/en/latest/)
- [Python 3.15 What's new（官方）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [PEP 810 – Explicit lazy imports](https://peps.python.org/pep-0810/)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 语言与工程化全景，本知识点在体系中的位置
- [[Python-asyncio异步编程]] — FastAPI 异步路由背后的事件循环与协程基础
- [[Python-类型注解实战]] — Pydantic 校验所依赖的类型注解体系
- [[Python-高级特性]] — 装饰器、元编程等支撑框架使用的进阶语法
- [[RESTful-API规范]] — 接口设计规范，与 FastAPI 路由实践配合
- [[NodeJS-Express框架笔记]] — 与 FastAPI 对比的 Node.js Web 方案

## 九、变更记录

- 2026-11-19：首次创建。
