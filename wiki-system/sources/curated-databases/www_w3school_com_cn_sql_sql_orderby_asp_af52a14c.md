---
source: "http://www.w3school.com.cn/sql/sql_orderby.asp"
title: "SQL ORDER BY 关键字"
fetched_at: "2026-10-05 15:29:34"
---

# SQL ORDER BY 关键字

* [SQL WHERE](/sql/sql_where.asp "SQL WHERE 子句")
* [SQL AND](/sql/sql_and.asp "SQL AND 操作符")

## SQL ORDER BY

`ORDER BY` 关键字用于对结果集进行升序或降序排序。

`ORDER BY` 关键字默认对结果集进行升序 (`ASC`) 排序。

要按降序对记录进行排序，请使用 `DESC` 关键字。

### 实例

按价格对产品进行排序：
    
    
    SELECT * FROM Products
    ORDER BY Price;
    

[亲自试一试](/sql/t.php?f=sql_select_orderby_price)

## ORDER BY 语法
    
    
    SELECT _column1_ , _column2_ , ...
    FROM _table_name_
    ORDER BY _column1_ , _column2_ , ... ASC|DESC;
    

## 演示数据库

以下是在实例中使用的 [Products](/sql/t.php?f=sql_products) 表的片段：

ProductID | ProductName | SupplierID | CategoryID | Unit | Price  
---|---|---|---|---|---  
1 | Chais | 1 | 1 | 10 boxes x 20 bags | 18  
2 | Chang | 1 | 1 | 24 - 12 oz bottles | 19  
3 | Aniseed Syrup | 1 | 2 | 12 - 550 ml bottles | 10  
4 | Chef Anton's Cajun Seasoning | 2 | 2 | 48 - 6 oz jars | 22  
5 | Chef Anton's Gumbo Mix | 2 | 2 | 36 boxes | 21.35  
  
## DESC

要按降序对记录进行排序，请使用 `DESC` 关键字。

### 实例

按价格从高到低对产品进行排序：
    
    
    SELECT * FROM Products
    ORDER BY Price DESC;
    

[亲自试一试](/sql/t.php?f=sql_select_orderby_price_desc)

## 按字母顺序排序

对于字符串值，`ORDER BY` 关键字将按字母顺序排序：

### 实例

按产品名称的字母顺序对产品进行排序：
    
    
    SELECT * FROM Products
    ORDER BY ProductName;
    

[亲自试一试](/sql/t.php?f=sql_select_orderby_name)

## 按字母降序排序

要按字母逆序对表进行排序，请使用 `DESC` 关键字：

### 实例

按产品名称的逆序对产品进行排序：
    
    
    SELECT * FROM Products
    ORDER BY ProductName DESC;
    

[亲自试一试](/sql/t.php?f=sql_select_orderby_name_desc)

## 按多列排序

以下 SQL 语句从 "Customers" 表中选择所有客户，并按 "Country" 和 "CustomerName" 列进行排序。

这意味着它按国家排序，但如果某些行具有相同的国家，则按 CustomerName 对它们进行排序：

### 实例
    
    
    SELECT * FROM Customers
    ORDER BY Country, CustomerName;
    

[亲自试一试](/sql/t.php?f=sql_select_orderby_1)

## 同时使用 ASC 和 DESC

以下 SQL 语句从 "Customers" 表中选择所有客户，并按 "Country" 列升序和 "CustomerName" 列降序进行排序：

### 实例
    
    
    SELECT * FROM Customers
    ORDER BY Country ASC, CustomerName DESC;
    

[亲自试一试](/sql/t.php?f=sql_select_orderby_2)

* [SQL WHERE](/sql/sql_where.asp "SQL WHERE 子句")
* [SQL AND](/sql/sql_and.asp "SQL AND 操作符")
