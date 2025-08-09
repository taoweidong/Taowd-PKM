以下是一份详细的 **Obsidian Dataview 插件操作指南**，涵盖核心功能、操作步骤及实用示例，助你高效管理知识库：

---

### **一、Dataview 插件核心功能**
1. **动态数据聚合**  
   - 自动扫描库中所有笔记，按条件筛选内容（如标签、日期、自定义字段）。
2. **多视图展示**  
   - 表格（TABLE）、列表（LIST）、任务列表（TASK）、日历（CALENDAR）四种展示模式。
3. **查询自定义字段**  
   - 解析笔记中的 YAML 元数据（Frontmatter）或行内字段（如 `key:: value`）。
4. **执行计算与排序**  
   - 对数字、日期等字段进行排序、过滤、分组运算。

---

### **二、前置准备**
1. **安装插件**  
   - Obsidian 设置 → 社区插件 → 搜索 "Dataview" → 安装并启用。
2. **启用查询功能**  
   - 新建笔记或编辑现有笔记，用代码块包裹查询语句：
     ````markdown
     ```dataview
     // 查询语句写在这里
     ```
     ````

---

### **三、基础操作指南**
#### **场景1：列出所有带特定标签的笔记**
```dataview
LIST
FROM #标签名
```

#### **场景2：表格展示读书笔记（带评分和日期）**
1. **在笔记中添加元数据**：  
   在笔记顶部添加 YAML Frontmatter：
   ```yaml
   ---
   book: true
   rating: 8
   finish-date: 2023-10-01
   ---
   ```

2. **执行查询**：
   ```dataview
   TABLE rating, finish-date
   FROM "文件夹路径"  // 如 "10-读书笔记"
   WHERE book
   SORT rating DESC
   ```

#### **场景3：聚合未完成的待办任务**
```dataview
TASK
FROM "目标文件夹"
WHERE !completed  // 筛选未完成
GROUP BY file.folder  // 按文件夹分组
```

---

### **四、高级技巧**
#### **1. 行内字段（无需Frontmatter）**
在笔记任意位置添加字段（支持动态更新）：
```markdown
阅读进度:: 45%
```
查询语句：
```dataview
TABLE 阅读进度
WHERE 阅读进度 < 100
```

#### **2. 日期计算**
```dataview
LIST
WHERE file.ctime >= date(today) - dur(7 days)  // 筛选最近7天创建的笔记
```

#### **3. 复杂条件组合**
```dataview
TABLE author AS "作者", length(file.name) AS "文件名长度"
FROM #article 
WHERE rating > 7 AND !contains(tags, "#暂存")
SORT length(file.name) DESC
```

---

### **五、常用查询参数速查**
| 语法         | 作用           | 示例                     |
| ---------- | ------------ | ---------------------- |
| `FROM`     | 指定来源路径/标签    | `FROM "Projects"`      |
| `WHERE`    | 过滤条件         | `WHERE status = "进行中"` |
| `SORT`     | 排序字段（+升序-降序） | `SORT -priority`       |
| `GROUP BY` | 按字段分组        | `GROUP BY type`        |
| `FLATTEN`  | 展开数组字段       | `FLATTEN tags AS tag`  |
|            |              |                        |

---

### **六、实战示例：创建动态项目看板**
```dataview
TABLE WITHOUT ID
  status AS "状态",
  rows.file.link AS "任务"
FROM "01-项目"
WHERE !completed
GROUP BY status
SORT status
```
**效果**：自动按状态（进行中/待处理/已完成）分组展示任务列表。

---

### **七、避坑指南**
1. **字段命名**：避免使用中文或特殊符号（如 `日期::` 比 `Date::` 更易出错）。
2. **日期格式**：必须用 `YYYY-MM-DD`（如 `2023-10-01`）。
3. **实时更新**：修改数据后需**切换笔记标签页**或**重新打开文件**触发刷新。

---

### **进阶学习资源**
- 官方文档：[Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- 查询生成器：[Dataview Query Generator](https://s-blu.github.io/obsidian-dataview-query-generator/)

掌握 Dataview 后，你的 Obsidian 将从静态笔记升级为**动态知识数据库**。如需特定场景的查询方案（如学术文献管理/周报生成），可告知具体需求，我会为你定制查询语句！