


```dataview
TABLE 
  file.link AS "文件",
  dateformat(file.mtime, "yyyy-MM-dd HH:mm") AS "修改时间",
  file.ctime AS "创建时间",
  file.folder AS "目录"
FROM "Obsidian"
WHERE file.name != this.file.name  // 排除自身
SORT file.mtime DESC
LIMIT 20
```
