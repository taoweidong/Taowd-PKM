---
date: 2025-08-09
tags:
  - Python
  - 常用库
aliases:
  - Pandas
---

Pandas 是一个强大的 Python 库，专注于**数据处理和分析**。它提供了高性能、易用的数据结构和数据分析工具，尤其擅长处理表格数据（如 CSV、Excel）、时间序列等结构化数据。核心数据结构是 `DataFrame`（二维表格）和 `Series`（一维数组）。

---

### 核心功能
1. **数据读写**：支持 CSV、Excel、SQL、JSON 等格式
2. **数据清洗**：处理缺失值、重复值、异常值
3. **数据转换**：合并/连接数据集、重塑数据、分组聚合
4. **数据分析**：统计描述、时间序列分析、数据可视化集成

---

### 基础代码示例

#### 1. 安装 Pandas
```bash
pip install pandas
```

#### 2. 创建 DataFrame
```python
import pandas as pd

# 从字典创建
data = {
    "姓名": ["张三", "李四", "王五"],
    "年龄": [25, 30, 28],
    "城市": ["北京", "上海", "广州"]
}
df = pd.DataFrame(data)
print(df)
```
输出：
```
   姓名  年龄  城市
0  张三  25  北京
1  李四  30  上海
2  王五  28  广州
```

#### 3. 数据选择
```python
# 选择列
print(df["姓名"])  # 输出姓名列

# 选择行
print(df.iloc[1])  # 第二行（索引从0开始）

# 条件筛选
print(df[df["年龄"] > 26])  # 年龄大于26的所有行
```

#### 4. 数据清洗
```python
# 添加缺失值
df.loc[2, "年龄"] = None

# 填充缺失值
df_filled = df.fillna({"年龄": df["年龄"].mean()})  # 用平均值填充
print(df_filled)

# 删除重复行
df_no_dup = df.drop_duplicates()
```

#### 5. 数据分组聚合
```python
# 添加部门列
df["部门"] = ["技术部", "销售部", "技术部"]

# 按部门分组并计算平均年龄
grouped = df.groupby("部门")["年龄"].mean()
print(grouped)
```
输出：
```
部门
技术部    26.5
销售部    30.0
```

#### 6. 数据可视化
```python
import matplotlib.pyplot as plt

# 绘制年龄分布直方图
df["年龄"].plot(kind="hist", bins=10, title="年龄分布")
plt.show()
```

#### 7. 读写文件
```python
# 保存到 CSV
df.to_csv("data.csv", index=False)

# 从 CSV 读取
new_df = pd.read_csv("data.csv")
print(new_df.head())
```

---

### 进阶示例：时间序列分析
```python
# 创建日期范围
dates = pd.date_range("2023-01-01", periods=5, freq="D")

# 创建带时间索引的 DataFrame
ts_df = pd.DataFrame({
    "销售额": [100, 150, 200, 180, 220],
    "日期": dates
}).set_index("日期")

# 计算7天移动平均
ts_df["移动平均"] = ts_df["销售额"].rolling(window=2).mean()
print(ts_df)
```
输出：
```
            销售额  移动平均
日期                     
2023-01-01  100    NaN
2023-01-02  150  125.0
2023-01-03  200  175.0
2023-01-04  180  190.0
2023-01-05  220  200.0
```

---

### 应用场景
- 数据清洗与预处理
- 探索性数据分析（EDA）
- 金融数据分析（股票、交易）
- 科学实验数据处理
- 机器学习特征工程

Pandas 通常与 NumPy（数值计算）、Matplotlib/Seaborn（可视化）、Scikit-learn（机器学习）等库配合使用，构成 Python 数据科学生态的核心。