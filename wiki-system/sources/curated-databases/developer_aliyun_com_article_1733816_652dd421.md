---
source: "https://developer.aliyun.com/article/1733816"
title: "【MySQL】索引核心：Explain执行计划解读、慢SQL优化全流程-阿里云开发者社区"
fetched_at: "2026-10-06 12:24"
---

# 【MySQL】索引核心：Explain执行计划解读、慢SQL优化全流程

2026-05-11 531

**简介：** 本文系统讲解MySQL索引与慢SQL优化全链路：从B+树原理、聚簇/联合索引设计，到EXPLAIN执行计划深度解读（重点解析type、key、rows、Extra等核心字段），再到慢查询定位、9类索引失效场景及实战优化策略，助力高效根治慢SQL。

# 索引核心：Explain执行计划解读、慢SQL优化全流程 系统性知识体系

## 一、索引基础理论：性能优化的基石

### 1.1 索引本质与底层原理

  * **索引定义** ：帮助MySQL高效获取数据的**排好序的数据结构** ，类似书籍目录
  * **底层数据结构** ：InnoDB默认使用**B+树**
    * 所有数据都在**叶子节点** ，非叶子节点只存索引键+指针
    * 叶子节点通过**双向链表** 相连，天然支持范围查询、排序和分组
    * 树高通常为3-4层，可存储千万级数据，查询只需3-4次磁盘IO
  * **为什么不用其他结构** ： 
    * 二叉树/AVL树：层高太高，磁盘IO次数多
    * 哈希索引：仅支持等值查询，不支持范围、排序、模糊匹配
    * B树：非叶子节点也存数据，节点容量小，树高更高



### 1.2 索引分类体系

#### 按物理存储划分

  * **聚簇索引（主键索引）** ⭐ 
    * InnoDB独有，每张表**有且只有一个**
    * 叶子节点直接存储**整行完整数据**
    * 数据物理存储顺序与索引逻辑顺序一致
    * 选取规则：显式主键 → 第一个唯一非空索引 → 自动生成隐藏自增列
  * **非聚簇索引（二级索引/辅助索引）**
    * 叶子节点只存储**主键值**
    * 查询需要**回表** ：先查二级索引拿到主键，再查聚簇索引获取完整数据



#### 按业务用途划分

  * **主键索引** ：非空、唯一，建议使用自增BIGINT
  * **唯一索引** ：列值唯一，允许一个NULL值
  * **普通索引** ：最常用，仅用于加速查询
  * **联合索引** ：多个字段组合而成，遵循**最左前缀原则**
  * **覆盖索引** ：查询的所有字段都在索引中，无需回表，性能极高
  * **全文索引** ：用于全文搜索，底层是倒排索引
  * **空间索引** ：用于地理空间数据查询（MySQL 5.7+支持）



### 1.3 索引设计核心原则

  1. **最左前缀原则** ：联合索引从左到右匹配，遇到范围查询（>、<、BETWEEN）就停止匹配
  2. **等值列在前，范围列在后** ：联合索引设计的黄金法则
  3. **覆盖索引优先** ：尽量让查询只需要访问索引就能完成
  4. **避免冗余索引** ：如已有索引(a,b)，则索引(a)是冗余的
  5. **控制索引数量** ：单表索引建议不超过5个，过多索引会降低写入性能
  6. **索引字段尽量小** ：优先选择整型、短字符串作为索引字段



## 二、Explain执行计划详解：SQL优化的"透视镜"

### 2.1 Explain基础

  * **作用** ：查看MySQL优化器生成的查询执行计划，揭示数据访问路径、索引使用、连接顺序等关键信息
  * **基本语法** ：
        
        EXPLAIN SELECT * FROM users WHERE age > 30;
        
        EXPLAIN FORMAT=JSON SELECT * FROM orders;
        

  * **输出字段** ：共12个核心字段，其中**id、select_type、type、key、key_len、rows、Extra** 是重点关注对象



### 2.2 核心字段深度解析

#### 1\. id：查询执行顺序

  * **id相同** ：同一级别的查询，执行顺序**从上到下**
  * **id不同** ：存在子查询或嵌套查询，**id值越大优先级越高** ，越先执行
  * **id为NULL** ：表示该行是UNION操作的结果合并，最后执行



#### 2\. select_type：查询类型

类型 | 含义  
---|---  
SIMPLE | 简单查询，不包含子查询或UNION  
PRIMARY | 复杂查询中的最外层主查询  
SUBQUERY | SELECT或WHERE子句中的子查询  
DERIVED | FROM子句中的派生表（临时表）  
UNION | UNION操作中的第二个及以后的SELECT  
UNION RESULT | UNION结果的合并操作  
  
#### 3\. type：访问类型（性能核心指标）⭐

**性能从优到劣排序** ：`system > const > eq_ref > ref > range > index > ALL`

类型 | 含义 | 场景 | 优化目标  
---|---|---|---  
system | 系统表，表中只有一行数据 | 查询mysql系统表 | 可遇不可求  
const | 常量级查询，通过主键或唯一索引定位到一行 | `WHERE id = 1` | 理想状态  
eq_ref | 联表查询时，使用主键或唯一索引匹配 | `WHERE a.id = b.user_id` | 联表查询的最佳状态  
ref | 使用普通非唯一索引进行等值匹配 | `WHERE name = 'Tom'` | 日常查询的合格线  
range | 索引范围扫描 | `BETWEEN`、`>`、`<`、`IN`等 | 必须达到的最低标准  
index | 全索引扫描，扫描整个索引树 | `SELECT id FROM user`（无WHERE条件） | 较差，需优化  
ALL | 全表扫描，扫描整个数据表 | 无索引或索引失效 | 必须优化  
  
**优化铁律** ：至少要达到`range`级别，最好能达到`ref`级别

#### 4\. possible_keys与key

  * **possible_keys** ：MySQL认为**可能** 使用的索引（优化器备选方案）
  * **key** ：MySQL**实际** 使用的索引（优化器最终决策）
  * **关键判断** ： 
    * possible_keys有值但key为NULL → 索引失效
    * key的值不在possible_keys中 → 优化器选择了其他索引



#### 5\. key_len：索引使用长度

  * **含义** ：MySQL使用的索引字节数
  * **作用** ：判断联合索引实际使用了多少列
  * **计算规则** ： 
    * 整型：TINYINT(1)、SMALLINT(2)、INT(4)、BIGINT(8)
    * 字符串：CHAR(n)=n字节，VARCHAR(n)=n+2字节（变长）
    * 允许NULL：额外+1字节
  * **示例** ：联合索引`idx_name_age(name VARCHAR(20), age INT)`
    * key_len=22 → 只使用了name列
    * key_len=26 → 使用了name和age两列



#### 6\. rows：预估扫描行数

  * **含义** ：MySQL认为执行查询需要扫描的行数
  * **重要性** ：这是一个**估算值** ，但非常关键，数值越小越好
  * **优化目标** ：尽量让rows接近实际返回的行数



#### 7\. Extra：额外信息（关键补充）

信息 | 含义 | 评价  
---|---|---  
Using index | 使用了覆盖索引，无需回表 | ✅ 非常好  
Using where | 使用WHERE条件过滤数据 | 正常  
Using temporary | 使用临时表存储中间结果 | ❌ 需优化  
Using filesort | 使用文件排序，无法利用索引排序 | ❌ 需优化  
Using join buffer | 使用连接缓冲区 | 一般，可优化  
Impossible WHERE | WHERE条件永远为false | 无意义  
Select tables optimized away | 聚合函数查询索引列，无需扫描表 | ✅ 非常好  
  
## 三、慢SQL优化全流程：从发现到解决的完整闭环

### 3.1 第一步：慢SQL发现与定位

#### 1\. 开启慢查询日志（MySQL 8.0+生产级配置）
    
    
    SET GLOBAL slow_query_log = 'ON';
    SET GLOBAL long_query_time = 1; 
    SET GLOBAL log_output = 'FILE';
    SET GLOBAL log_queries_not_using_indexes = 'OFF'; 
    SET GLOBAL min_examined_row_limit = 1000; 
    
    
    [mysqld]
    slow_query_log = ON
    slow_query_log_file = /var/log/mysql/slow.log
    long_query_time = 1
    log_output = FILE
    min_examined_row_limit = 1000
    

#### 2\. 慢查询日志分析工具

  * **mysqldumpslow** ：MySQL自带工具
        
        mysqldumpslow -s r -t 10 /var/log/mysql/slow.log
        
        mysqldumpslow -s c -t 10 /var/log/mysql/slow.log
        

  * **pt-query-digest** ：Percona工具集，功能更强大
        
        pt-query-digest /var/log/mysql/slow.log > slow_report.txt
        




#### 3\. 实时监控工具

  * **SHOW PROCESSLIST** ：查看当前正在执行的SQL
  * **Performance Schema** ：MySQL内置性能监控工具
  * **第三方工具** ：PMM、Prometheus+Grafana、Zabbix等



### 3.2 第二步：执行计划分析

  1. **看type** ：是否达到range级别以上
  2. **看key** ：是否使用了预期的索引
  3. **看key_len** ：联合索引是否充分利用
  4. **看rows** ：预估扫描行数是否过多
  5. **看Extra** ：是否有Using filesort、Using temporary等不良信息



### 3.3 第三步：问题诊断与优化策略

#### 1\. 索引优化（性价比最高的优化手段）

  * **添加合适的索引** ：为WHERE、ORDER BY、GROUP BY涉及的字段添加索引
  * **创建联合索引** ：遵循"等值列在前，范围列在后"原则
  * **使用覆盖索引** ：将查询需要的所有字段都包含在索引中
  * **删除冗余和无效索引** ：减少写入开销



#### 2\. SQL语句重构

  * **避免SELECT *** ：只查询需要的列，减少IO和网络传输
  * **避免索引失效** ：见下文"索引失效常见场景"
  * **优化子查询** ：多数场景下JOIN比IN(子查询)更高效
  * **优化深分页** ：使用"游标分页"或"覆盖索引+延迟关联"
  * **优化排序** ：让索引顺序与排序顺序一致，避免Using filesort
  * **优化分组** ：让索引顺序与分组顺序一致，避免临时表



#### 3\. 表结构优化

  * **选择合适的数据类型** ：尽量使用小的数据类型
  * **避免NULL值** ：NULL值会占用额外空间，且影响索引效率
  * **拆分大表** ：将大字段（如TEXT、BLOB）拆分到单独的表中
  * **适当反范式** ：减少JOIN操作，提高查询效率



#### 4\. 系统级优化

  * **调整MySQL配置参数** ：如innodb_buffer_pool_size、innodb_log_file_size等
  * **硬件升级** ：增加内存、使用SSD硬盘
  * **架构升级** ：读写分离、分库分表、引入缓存（Redis）等



### 3.4 第四步：验证与监控

  1. **验证优化效果** ：再次执行EXPLAIN，对比优化前后的执行计划
  2. **性能测试** ：在测试环境进行压力测试，确保优化不会引入新问题
  3. **上线监控** ：上线后持续监控SQL性能，观察慢查询日志
  4. **建立长效机制** ：定期审查慢查询日志，及时发现和解决新的慢SQL



## 四、索引失效常见场景与解决方案

### 4.1 最常见的索引失效场景

  1. **违反最左前缀匹配原则**
         
         SELECT * FROM users WHERE age = 25;
         
         SELECT * FROM users WHERE name = 'Tom' AND age = 25;
         

  2. **索引列上使用函数或表达式**
         
         SELECT * FROM orders WHERE YEAR(create_time) = 2024;
         
         SELECT * FROM orders WHERE create_time BETWEEN '2024-01-01' AND '2024-12-31';
         

  3. **隐式类型转换**
         
         SELECT * FROM users WHERE phone = 13800138000;
         
         SELECT * FROM users WHERE phone = '13800138000';
         

  4. **模糊查询以%开头**
         
         SELECT * FROM users WHERE name LIKE '%Tom%';
         
         SELECT * FROM users WHERE name LIKE 'Tom%';
         
         

  5. **使用OR连接非索引列**
         
         SELECT * FROM users WHERE name = 'Tom' OR age = 25;
         
         SELECT * FROM users WHERE name = 'Tom'
         UNION ALL
         SELECT * FROM users WHERE age = 25;
         

  6. **负向查询**
         
         SELECT * FROM users WHERE age NOT IN (20, 25, 30);
         
         SELECT * FROM users WHERE age IN (18, 19, 21, 22, 23, 24, 26, 27, 28, 29);
         

  7. **优化器放弃索引**

     * 当MySQL认为全表扫描比使用索引更快时（如小表、数据分布不均）
     * 解决方案：使用FORCE INDEX强制使用索引（谨慎使用）
           
           SELECT * FROM users FORCE INDEX(idx_age) WHERE age > 20;
           




### 4.2 索引失效的底层原因

  * B+树索引存储的是**原始值** ，对列进行任何转换或计算后，都无法直接通过索引定位数据
  * 索引是**按前缀排序** 的，%开头的模糊查询无法确定起始位置
  * OR条件要求所有列都有索引，否则MySQL会选择全表扫描



## 五、高级优化技巧与最佳实践

### 5.1 高级索引技巧

  1. **函数索引** （MySQL 8.0+支持）
         
         CREATE INDEX idx_year_create_time ON orders((YEAR(create_time)));
         
         SELECT * FROM orders WHERE YEAR(create_time) = 2024;
         

  2. **降序索引** （MySQL 8.0+支持）
         
         CREATE INDEX idx_create_time_desc ON orders(create_time DESC);
         
         SELECT * FROM orders ORDER BY create_time DESC LIMIT 10;
         

  3. **索引合并优化**

     * 当查询条件涉及多个单列索引时，MySQL可能会使用索引合并
     * 但索引合并效率通常不如联合索引，建议创建联合索引覆盖所有查询条件



### 5.2 常见慢SQL优化案例

#### 案例1：深分页优化
    
    
    SELECT * FROM products ORDER BY id LIMIT 10000, 20;
    
    
    SELECT * FROM products WHERE id > 10000 ORDER BY id LIMIT 20;
    
    
    SELECT p.* FROM products p
    JOIN (SELECT id FROM products ORDER BY id LIMIT 10000, 20) t ON p.id = t.id;
    

#### 案例2：JOIN查询优化
    
    
    
    
    SELECT * FROM users u JOIN orders o ON u.id = o.user_id WHERE u.age > 20;
    
    
    ALTER TABLE orders ADD INDEX idx_user_id(user_id);
    

#### 案例3：GROUP BY优化
    
    
    SELECT category_id, COUNT(*) FROM products GROUP BY category_id;
    
    
    ALTER TABLE products ADD INDEX idx_category_id(category_id);
    

### 5.3 最佳实践总结

  1. **优化优先级** ：SQL与索引 > 表结构 > 配置参数 > 硬件与架构
  2. **四个"减少"** ：减少数据访问、减少返回数据、减少交互次数、减少服务器开销
  3. **三个"利用"** ：利用索引覆盖、利用内存缓存、利用并行/分区
  4. **一句话铁律** ：没有银弹，用数据说话（监控 + EXPLAIN验证）
  5. **预防性优化** ：在开发阶段就关注SQL性能，避免问题上线



## 六、面试高频考点总结

  1. **B+树和B树的区别**
  2. **聚簇索引和非聚簇索引的区别**
  3. **为什么InnoDB表必须有主键，并且推荐使用自增主键**
  4. **联合索引的最左前缀原则**
  5. **Explain执行计划中各个字段的含义**
  6. **type字段的各个级别及性能排序**
  7. **索引失效的常见场景及解决方案**
  8. **慢SQL优化的完整流程**
  9. **深分页问题的优化方法**
  10. **覆盖索引的概念及优势**



[ ](/profile/ypjhajr6tdfai)

[来一杯热Java](/profile/ypjhajr6tdfai)

目录

热门文章

最新文章
