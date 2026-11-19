---
title: Python数据处理与分析（Pandas）
date: 2026-11-19
updated: 2026-11-19
tags:
  - 技术积累/Python
  - 编程语言
  - 数据处理
  - Pandas
aliases:
  - Pandas 数据处理与分析
  - pandas 学习笔记
source: 网络资料整理
---

# Python数据处理与分析（Pandas）

> [!summary] 摘要
> 本文面向已具备 Python 基础、需要用 pandas 完成数据清洗、转换、聚合与分析的开发者，系统覆盖 pandas 的核心数据结构（DataFrame / Series）、索引与选择、向量化运算、分组聚合、缺失值与类型处理，以及数据读写与可视化。内容以 **pandas 3.0**（截至 2026-11 的 3.0.6）为基准，重点说明 3.0 大版本带来的**专用字符串 dtype、统一 Copy-on-Write、日期时间解析默认值调整**三大变化，以及从 2.x 升级的迁移要点。定位为「能照着写、能照着排查」的实战笔记，与 [[Python-从入门到精通]] 共同构成 Python 数据处理的学习闭环。

## 一、最新动态（截至 2026-11）

- **pandas 3.0.0（2026-01-22 发布公告）**：进入 3.x 大版本，四项关键变化：默认使用**专用字符串数据类型（dedicated string dtype）**；**统一 Copy-on-Write（CoW）拷贝/视图语义**，**取消 `SettingWithCopyWarning`**；**日期时间类数据采用新的默认解析规则**；**初始支持 `pd.col` 语法**（表达式式列操作）。
- **pandas 3.0.6（2026-10）**：3.0.x 补丁版，**首个支持 Python 3.15** 的版本；**pandas 3.0 支持 Python 3.11 及以上**。
- **版本节奏**：3.0.2（2026-03-30，含 `Series.case_when()` 对 `pd.col()` 的支持）、3.0.3（2026-05）、3.0.4（2026-06）、3.0.6（2026-10）。
- **升级风险**：3.0 含**可能的破坏性变更**（字符串 dtype、CoW、日期时间解析默认值），从 2.x 升级需重点回归校验。安装建议 `python -m pip install --upgrade pandas==3.0.*`，或使用 conda-forge 渠道。
- **配套生态**：NumPy 当前为 **2.5.4（2026-10-10，2.5.0 于 2026-06-21）**，与 pandas 3.0 构成当前数据处理栈基础；`pyarrow`、`polars`、`duckdb` 是常用的替代与加速方案（自由线程构建下 `pyarrow`/`pandas` 已发布 cp314t/cp315t wheel）。

> [!info] 时效说明
> 以上版本号来自调研文件，第三方补丁版本更新频繁；写作当日的具体版本请以 [pandas 官方 What's new](https://pandas.pydata.org/docs/whatsnew/) 与 [PyPI pandas 页面](https://pypi.org/project/pandas/) 为准。

## 二、基础概念

- **DataFrame 与 Series**：DataFrame 是二维、标签化的表格结构（行索引 + 列索引），Series 是一维、带标签的数组。二者是 pandas 最核心的抽象，绝大多数操作都在这两种结构上进行。
- **轴（axis）语义**：`axis=0` 表示沿行方向操作（跨列取值），`axis=1` 表示沿列方向操作。例如 `dropna(axis=0)` 删除含缺失值的行，`dropna(axis=1)` 删除含缺失值的列。
- **索引（Index）**：行索引默认是 0 开始的整数位置，也可自定义为唯一标签。索引是快速定位、对齐与合并的基础，建议主键类字段设为唯一索引。
- **dtype**：pandas 在 NumPy 类型之上提供扩展 dtype，如可空整数 `Int64`、字符串 `string`、`category`、`datetime64[ns]` 等。**3.0 起字符串列默认使用专用字符串 dtype**，不再是 NumPy 的 `object`。
- **向量化**：以整列 / 整行的运算替代逐行 Python 循环，是 pandas 性能优势的主要来源，也是编写 pandas 代码时的第一原则。
- **索引对齐**：两个 DataFrame / Series 按各自索引自动对齐后再运算，这是分组、合并等操作成立的隐含前提，也意味着索引不一致时会出现大量 `NaN`。

## 三、核心机制

**1. Copy-on-Write（3.0 统一启用）**
3.0 起 CoW 成为全局统一语义，视图与拷贝的边界不再需要人工判断；链式赋值不再触发 `SettingWithCopyWarning`，该告警已被**取消**。实际效果是：`df2 = df1` 之后修改 `df2` 不会意外改动 `df1`，从机制上杜绝了「改了原表却没发现」的隐蔽 bug。

**2. 索引与选择机制**
按标签选择用 `.loc`，按整数位置选择用 `.iloc`。二者是 pandas 中唯一推荐的显式选择方式，避免依赖 `df[]` 在列名与布尔序列之间的歧义。

**3. 分组聚合机制**
`groupby` 将数据按指定键分组，再对每组应用聚合函数（`mean`、`sum`、`count`、`agg` 等），本质是「拆分—应用—合并」（split-apply-combine）。

**4. 缺失值处理机制**
pandas 用 `NaN`/`NaT` 表示缺失，缺失值在算术运算中具有传染性（参与运算得 `NaN`），因此必须先显式处理再计算，或用 `skipna` 控制跳过。

**5. 类型解析机制（3.0 变化）**
日期时间类数据在 3.0 采用**新的默认解析规则**，字符串到时间的推断行为有调整，读取 CSV/Excel 时建议显式指定 `parse_dates` 或 `dtype`，避免依赖隐式推断。

## 四、实践步骤（含代码/命令示例）

**第 1 步：环境准备**

```bash
# 使用 uv（推荐）或标准库 venv 创建隔离环境
uv init && uv add pandas
# 或
python -m venv .venv
python -m pip install --upgrade "pandas==3.0.*"
```

**第 2 步：构造与读取数据**

```python
import pandas as pd

# 从内嵌字典构造 DataFrame
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "部门": ["研发", "研发", "市场", "市场"],
    "薪资": [18000, 22000, 15000, 16000],
    "入职日期": ["2021-03-01", "2020-07-15", "2022-11-20", "2023-05-09"],
})

# 从文件读取（显式指定日期列，规避 3.0 新的默认解析行为）
df = pd.read_csv("data.csv", parse_dates=["入职日期"])
```

**第 3 步：查看与选择**

```python
df.head(3)          # 查看前 3 行
df.info()           # 查看列数、非空数量、dtype
df.describe()       # 数值列的统计摘要

df.loc[:, ["姓名", "薪资"]]        # 按标签选列
df.iloc[0:2]                       # 按位置选前两行
df[df["薪资"] > 16000]             # 布尔掩码过滤行
```

**第 4 步：清洗（缺失值、类型、去重）**

```python
df = df.drop_duplicates(subset="姓名")          # 去重
df["薪资"] = df["薪资"].astype("Int64")         # 转为可空整数
df = df.fillna({"部门": "未分配"})              # 分类列填充
df = df.dropna(subset=["薪资"])                 # 关键列缺失则删行
```

**第 5 步：分组聚合**

```python
# 单聚合
salary_by_dept = df.groupby("部门")["薪资"].mean().round(2)

# 多聚合：一次得到多个统计量
stats = df.groupby("部门")["薪资"].agg(["mean", "min", "max", "count"])

# 自定义聚合
stats2 = df.groupby("部门").agg(
    平均薪资=("薪资", "mean"),
    人数=("姓名", "count"),
)
```

**第 6 步：透视与合并**

```python
# 透视表
pivot = df.pivot_table(index="部门", values="薪资", aggfunc="mean")

# 合并：按共同键横向拼接
df_right = df[["姓名", "绩效"]].copy()
merged = df[["姓名", "薪资"]].merge(df_right, on="姓名", how="left")
```

**第 7 步：导出结果**

```python
stats2.to_csv("部门薪资统计.csv", encoding="utf-8-sig")
stats2.to_excel("部门薪资统计.xlsx", index=False)
```

**可视化（依赖 matplotlib）**

```python
import matplotlib.pyplot as plt

stats2["平均薪资"].plot(kind="bar", title="各部门平均薪资")
plt.ylabel("薪资")
plt.tight_layout()
plt.savefig("平均薪资.png", dpi=150)
```

## 五、最佳实践与常见坑

**最佳实践**

- **优先向量化**：用整列运算和内置方法替代 `for + append`，必要时用 `.map()`、`.apply()` 仅作用于需要自定义逻辑的少数列。
- **用 `.loc`/`.iloc` 显式选择**：不要依赖链式索引 `df['a']['b']`，可读性和正确性都更差。
- **尽早确定 dtype**：在读取阶段用 `dtype`、`parse_dates` 明确类型，避免后续类型推断带来的性能与正确性问题。
- **按唯一键做 `merge`**：关联前先确认连接键唯一，或用 `validate` 参数检查合并结果类型。
- **大文件用分块读取**：`pd.read_csv(path, chunksize=100000)` 逐块处理，避免一次性载入内存。
- **升级到 3.0 时回归日期时间逻辑**：解析默认值有调整，务必用样本数据验证时间相关字段。

**常见坑**

- **3.0 的字符串 dtype 变化**：字符串列不再是 `object`，做 `.str` 访问器之外的操作、或与 `object` 类型数据拼接时，行为可能与 2.x 不同。
- **误判「改了副本」**：3.0 已统一 CoW，但若仍残留 2.x 的链式赋值写法，容易在旧认知下写出错误预期；迁移时按新语义重新审视。
- **缺失值传染**：`NaN` 参与运算会污染结果，先 `dropna`/`fillna`，或对聚合函数使用 `skipna`。
- **索引未对齐产生 `NaN`**：合并或对齐前检查两侧索引，必要时 `reset_index(drop=True)`。
- **`SettingWithCopyWarning` 消失不等于安全**：该告警在 3.0 被取消，但错误的选择方式仍可能导致修改未生效，建议始终用显式赋值或 `.loc`。
- **内存放大**：`category` 对低基数字符串列能显著省内存，但对高基数或持续变化的数据反而更慢，需实测。

## 六、核心要点速查

1. pandas 两大核心结构：**DataFrame（二维标签表格）**、**Series（一维标签数组）**。
2. **`axis=0` 按行方向、`axis=1` 按列方向**；`dropna`、`sum`、`mean` 等均遵循该约定。
3. 选择数据：**按标签用 `.loc`，按位置用 `.iloc`**。
4. 分组聚合：`groupby(...)[col].agg([...])`，本质是拆分—应用—合并。
5. 透视用 `pivot_table(index=, values=, aggfunc=)`；关联用 `merge(on=, how=)`。
6. **pandas 3.0（2026-01-22）三大变化**：专用字符串 dtype、统一 Copy-on-Write（取消 `SettingWithCopyWarning`）、日期时间新默认解析。
7. **pandas 3.0.6（2026-10）是首个支持 Python 3.15 的版本**；pandas 3.0 要求 **Python 3.11+**。
8. 缺失值用 `NaN`/`NaT` 表示，算术运算中会传染，先处理再计算。
9. 向量化是性能第一原则，逐行循环是 pandas 中最需要避免的写法。
10. 升级 3.0 前优先回归校验：字符串 dtype、CoW、日期时间解析三类逻辑。

## 七、学习资源

- [pandas 3.0.0 What's new（pandas 官方）](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html)
- [pandas 官方文档（What's new 汇总）](https://pandas.pydata.org/docs/whatsnew/)
- [pandas 用户指南（User Guide）](https://pandas.pydata.org/docs/user_guide/index.html)
- [PyPI pandas 版本页](https://pypi.org/project/pandas/)
- [NumPy Releases（NumPy 官方）](https://numpy.org/news/)
- [Python 3.15 What's new（Python 官方文档）](https://docs.python.org/3.15/whatsnew/3.15.html)

## 八、关联笔记

- [[Python-从入门到精通]] — Python 语言与生态全景，本知识点的上级主题
- [[Python学习]] — Python 入门与基础学习路径
- [[Python-高级特性]] — 迭代器、类型等与数据处理配合的进阶主题
- [[Python-并发编程实战]] — 大数据量并行处理的延伸参考
- [[编程语言]] — 跨语言视角下的数据处理选型

## 九、变更记录

- 2026-11-19：首次创建。
