---
title: Python 单元测试
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - Python
  - 测试
  - pytest
aliases:
  - Python 测试与 pytest 实战
source: 网络资料整理
---

# Python 单元测试

> [!摘要] 摘要
> 本文聚焦 Python 的单元测试体系，以 **pytest（当前 9.1.1，2026-11-07）** 为主线，兼顾标准库 **unittest**，讲清测试发现、fixture 依赖注入、参数化、断言重写等核心机制，并给出可直接运行的工程化实践步骤与常见坑。定位为「[[Python-从入门到精通]]」体系下的测试专题，适合从零建立 Python 测试习惯、或从 unittest 迁移到 pytest 的开发者。

## 一、最新动态（截至 2026-11）

- **pytest 最新为 9.1.1（2026-11-07）**，9.1.0 于 2026-06-13 发布；8.4.x 仍是常用的稳定线（8.4.2，2025-09-03）。pytest 9 对部分 8.x 行为做了生效性移除，升级需对照官方 Deprecations and Removals 章节更新代码。
- **pytest 9 起 pygments 成为必需依赖**，输出默认对源码做高亮；若不想要高亮，可用 `--code-highlight=no` 关闭。
- **标准库 `unittest` 在 3.15 有两处行为变化**：`IsolatedAsyncioTestCase`（3.8+）中「测试方法返回非 `None` 值」的行为被**弃用**；`assertWarns()` / `assertWarnsRegex()` **不再吞掉不匹配的警告**，测试可能开始泄漏此前被屏蔽的警告，需配合 warning filters 或额外的 `assertWarns*()` 捕获。
- **Python 当前稳定主线为 3.15**（3.15.0 于 2026-10-09，最新补丁 3.15.2 于 2026-10-25，属紧急安全发布）；3.14.10 同日发布。测试依赖可通过 `pyproject.toml` 的标准依赖组（PEP 735）管理。

## 二、基础概念

- **单元测试**：针对一个最小可测单元（通常是函数或类方法）编写断言，验证其输入输出与副作用是否符合预期。它追求**快、独立、可重复**。
- **断言（assert）**：测试的核心，判断实际结果与期望结果是否一致；失败即让测试「变红」。
- **测试用例与测试函数**：pytest 约定以 `test_` 开头的函数为用例；unittest 约定 `TestCase` 子类中以 `test_` 开头的方法。
- **fixture**：pytest 的依赖注入机制，用于在测试前后准备/清理资源（临时目录、数据库、mock、客户端等）。
- **参数化（parametrize）**：把同一逻辑用多组输入批量跑，避免重复代码。
- **pytest vs unittest**：`unittest` 是标准库自带、无需安装、可与 `pytest` 共存；`pytest` 语法更简洁、fixture 更灵活、生态更丰富，是新项目的主流选择。二者可混用，pytest 可直接运行 unittest 风格的用例。

## 三、核心机制

**1. 测试发现**
pytest 按命名规则自动发现用例：文件名 `test_*.py` 或 `*_test.py`，函数/方法名 `test_*`，类名 `Test*`。发现范围由 `testpaths`、命令行参数或 `conftest.py` 决定。

**2. fixture 与作用域**
fixture 由 `@pytest.fixture` 定义，可指定 `scope`（`function` / `class` / `module` / `session`）控制复用范围，并用 `yield` 做清理。测试函数通过参数名请求 fixture，实现依赖注入。

```python
import pytest


@pytest.fixture(scope="module")
def db_conn():
    conn = create_connection()  # 前置准备
    yield conn
    conn.close()                 # 后置清理


def test_query(db_conn):
    assert db_conn.query("SELECT 1") == 1
```

**3. 参数化**
`@pytest.mark.parametrize` 将一组数据注入单个测试函数，失败时能精确定位到具体参数组合。

```python
@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (0.5, 0.5, 1.0), (-1, 1, 0)])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

**4. 断言重写与标记**
pytest 会在导入测试模块时**重写断言**，使 `assert x == y` 失败时输出 `x`、`y` 的具体值，而非仅一行 AssertionError。`@pytest.mark.*` 用于分类、跳过、标记慢测试等。

**5. unittest 兼容性**
pytest 可运行 `unittest.TestCase`；`unittest` 的 `setUp/tearDown`、`setUpClass/tearDownClass` 仍可用，但 fixture 体验更直观，迁移成本很低。

## 四、实践步骤（含代码/命令示例）

**1. 项目结构与依赖声明**

```text
myproj/
├── pyproject.toml
├── src/myproj/calc.py
└── tests/
    ├── conftest.py
    └── test_calc.py
```

```toml
[project]
name = "myproj"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"

[dependency-groups]
test = ["pytest>=9", "pytest-cov>=6"]
```

**2. 被测代码与测试代码**

```python
# src/myproj/calc.py
def divide(a: int | float, b: int | float) -> float:
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b
```

```python
# tests/test_calc.py
import pytest

from myproj.calc import divide


@pytest.mark.parametrize("a, b, expected", [(6, 3, 2.0), (1, 4, 0.25)])
def test_divide_ok(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(ValueError, match="除数"):
        divide(1, 0)


@pytest.mark.skip(reason="待补充负数场景")
def test_divide_negative():
    pass
```

**3. 常用运行命令**

```bash
pytest                          # 运行全部用例
pytest -q                       # 简洁输出
pytest tests/test_calc.py -k divide_ok   # 按名称筛选
pytest -x                       # 首次失败即停止
pytest --maxfail=2              # 最多失败 2 条后停止
pytest -m "not slow"            # 按标记过滤（需注册 marker）
pytest --code-highlight=no      # 关闭源码高亮（pytest 9）
```

**4. 覆盖率**

```bash
uv run pytest --cov=myproj --cov-report=term-missing
```

## 五、最佳实践与常见坑

**最佳实践**
- **一个用例只验证一个行为**，失败信息即定位信息；用例名写成「断言 + 场景」。
- **用 fixture 管理状态与依赖**：文件用 `tmp_path`、时间用 `freezegun`、网络/外部调用用 `monkeypatch` 或 mock。
- **参数化优先**，避免把多组输入复制成多个近似用例。
- **分层测试**：单元测试保持毫秒级，慢测试（集成、真实 I/O）用标记单独跑。
- **显式注册 marker**（`--strict-markers`），防止拼写错误的标记被静默忽略。

**常见坑**
- **断言过于笼统**：只写 `assert result` 而丢失细节，失败时无法定位，应给出明确期望值。
- **用例相互依赖**：依赖执行顺序或共享可变状态，一旦随机化或隔离运行就失败。每个用例必须自包含。
- **在测试中做真实网络/文件调用**：结果不可控、速度慢、易受环境影响，应 mock 或使用临时目录。
- **忽略 fixture 清理**：用 `yield` 而非在 `tearDown` 里漏掉释放，避免资源泄漏与状态污染。
- **升级 pytest 9 未读弃用清单**：部分 8.x 行为已生效性移除，升级后旧写法可能直接报错。
- **Python 3.15 的 `assertWarns*()` 行为变化**：原先被屏蔽的警告可能外泄，需要显式处理 warning filters，否则会干扰其他用例。
- **`unittest.IsolatedAsyncioTestCase` 返回值**：3.15 起测试方法返回非 `None` 被弃用，异步用例应显式返回 `None`。

## 六、核心要点速查

1. 测试双轨：**pytest**（主流）+ **unittest**（标准库），可混用，pytest 可运行 unittest 用例。
2. pytest 核心三件套：**fixture（依赖注入）**、**`@pytest.mark.parametrize`（参数化）**、**断言重写（失败即见差异）**。
3. 用例命名：文件 `test_*.py`，函数 `test_*`，类 `Test*`；发现范围由 `testpaths` 控制。
4. fixture 用 `yield` 做前置/后置，`scope` 控制 `function`/`class`/`module`/`session` 复用。
5. 常见命令：`pytest -q`、`-x`、`-k`、`-m`、`--maxfail`、`--code-highlight=no`。
6. 覆盖率：`pytest --cov=包名 --cov-report=term-missing`（需 `pytest-cov`）。
7. 版本：pytest 当前 **9.1.1（2026-11-07）**，pygments 为必需依赖；稳定线 8.4.2。
8. Python 3.15 注意：`assertWarns*()` 不再吞警告；`IsolatedAsyncioTestCase` 返回非 `None` 弃用。

## 七、学习资源

- [pytest 官方文档（含 changelog）](https://docs.pytest.org/en/stable/changelog.html)
- [pytest 9.1.0 发布说明](https://docs.pytest.org/en/stable/announce/release-9.1.0.html)
- [About fixtures（pytest 官方文档）](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [unittest —— Unit testing framework（Python 官方文档）](https://docs.python.org/3/library/unittest.html)
- [Python 3.15 What's new（含 3.15 测试相关变更）](https://docs.python.org/3.15/whatsnew/3.15.html)
- [PEP 735 – Dependency groups in pyproject.toml](https://peps.python.org/pep-0735/)
- [pytest-cov（覆盖率插件）](https://pytest-cov.readthedocs.io/)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 技术全景总览，测试是工程化的重要一环
- [[Python-工程化与现代工具链]] — 环境、依赖与工具链配套实践
- [[Python学习]] — Python 入门与基础学习路径

## 九、变更记录

- 2026-11-19：首次创建。
