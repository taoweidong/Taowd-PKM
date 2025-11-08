import os
import sys
from datetime import datetime, timedelta

# 文件内容模板 - 移到模块级别，确保所有函数都能访问
file_contents = {
    "主页.md": """# 个人知识库主页

欢迎来到我的知识管理系统！这里是所有知识的起点。

## 🧭 快速导航

### 核心知识领域
- [[20-技术积累]] - 编程语言、框架、工具等技术知识
- [[30-软件设计]] - 设计模式、架构、原则等
- [[40-AI技术]] - 机器学习、深度学习等AI相关技术

### 知识管理
- [[10-个人知识管理]] - 学习方法论和工具使用
- [[50-项目记录]] - 项目实践和经验总结
- [[70-代码片段]] - 可复用的代码库
- [[80-代码片段]] - 日常记录和思考

### 实用工具
- [[00-索引与导航]] - 搜索和导航工具
- [[60-参考资料]] - 外部资料和读书笔记
- [[90-待整理与临时笔记]] - 临时笔记存放区

## 🔖 常用标签
#技术积累 #软件设计 #AI技术 #项目实践 #日记

## 📅 最近更新
- {最近更新}

---
*本知识库使用 Obsidian 管理，持续更新中...*
""",

    "标签索引.md": """# 标签索引

这里是知识库的标签导航系统，通过标签快速找到相关内容。

## 🏷️ 技术标签
### 技术领域
- #前端开发 - HTML、CSS、JavaScript、React、Vue等
- #后端开发 - Spring、Node.js、API设计等
- #DevOps - Docker、Kubernetes、Jenkins、Linux等
- #数据库 - MySQL、MongoDB、Redis等
- #编程语言 - Java、Python、JavaScript等

### 专业方向
- #软件设计 - 设计模式、架构、原则
- #AI技术 - 机器学习、深度学习、自然语言处理
- #全栈开发 - 前后端综合技术

## 📚 学习标签
- #学习笔记 - 学习过程中的记录
- #项目实践 - 项目相关经验
- #读书笔记 - 书籍阅读总结
- #问题解决 - 技术问题排查记录

## 📓 日记标签
- #日记 - 日常记录
- #周总结 - 每周总结
- #月总结 - 每月总结
- #灵感 - 突发灵感

## 🗂️ 状态标签
- #待完善 - 需要进一步补充的内容
- #重要 - 核心知识点
- #常用 - 高频使用内容

---
*使用 `#标签` 格式为笔记添加标签，便于分类检索*
""",

    "最近更新.md": """# 最近更新

记录知识库的最新变化和更新内容。

## 📝 更新记录

### 本周更新
- 初始化知识库目录结构
- 创建日记系统
- 完善目录索引文件

### 按月份归档
#### 2024年
- **1月**: 知识库建立

---
*保持定期更新，维护知识的新鲜度*
""",

    "学习路线图.md": """# 技术学习路线图

我的技术成长路径和学习计划。

## 🎯 核心目标
1. 提升软件设计能力
2. 掌握AI相关技术
3. 深化全栈开发技能

## 📚 学习路径

### 软件设计能力提升
- [ ] 深入学习设计模式 [[设计模式-工厂模式]]
- [ ] 掌握软件架构原理 [[软件架构-微服务架构]]
- [ ] 实践领域驱动设计 [[领域驱动设计-DDD]]
- [ ] 学习重构技巧 [[重构案例研究]]

### AI技术学习
- [ ] 机器学习基础 [[机器学习-线性回归]]
- [ ] 深度学习框架 [[深度学习-TensorFlow使用笔记]]
- [ ] 自然语言处理 [[自然语言处理-BERT模型详解]]
- [ ] AI工具应用 [[AI工具-LangChain实战]]

### 全栈技术深化
- [ ] 前端框架进阶 [[前端开发]]
- [ ] 后端架构优化 [[后端开发]]
- [ ] DevOps实践 [[DevOps]]
- [ ] 数据库性能 [[数据库]]

## 🗓️ 时间规划
- **Q1**: 完成设计模式学习
- **Q2**: 掌握机器学习基础
- **Q3**: 实践微服务架构
- **Q4**: AI项目实战

---
*路线图会根据实际情况动态调整*
""",

    "快速开始.md": """# 快速开始指南

## 🚀 第一天使用指南

### 1. 配置环境
- 安装 Obsidian
- 配置核心插件
- 学习基本快捷键

### 2. 开始记录
- 写第一篇日记 [[日记模板]]
- 创建学习计划 [[2024技术提升计划]]
- 记录代码片段 [[常用工具函数]]

### 3. 建立习惯
- 每日写日记
- 每周做总结
- 定期整理笔记

## 📖 核心功能

### 笔记管理
- 使用链接连接相关概念
- 为笔记添加合适的标签
- 定期回顾和更新

### 知识网络
- 通过图谱视图发现连接
- 建立知识间的关联
- 形成个人知识体系

---
*更多帮助请查看 [[笔记组织原则]]*
""",

    "笔记组织原则.md": """# 笔记组织原则

本知识库的组织方法论和基本原则。

## 🏗️ 结构原则
1. **分层分类**: 按照领域-主题-细目分层组织
2. **链接优先**: 使用双向链接建立知识网络
3. **渐进完善**: 从简单笔记开始，逐步丰富内容

## 📝 笔记规范
- 每个笔记聚焦一个主题
- 使用清晰的标题结构
- 及时添加相关链接
- 合理使用标签分类

## 🔗 链接策略
- 链接到相关概念 [[软件设计]]
- 链接到具体技术 [[Dockerfile编写指南]]
- 链接到项目实践 [[项目记录]]

相关链接：[[知识复用的技巧]] [[核心插件配置]]
""",

    "日记模板.md": """# {date} 日记

## 📅 今日概览
**日期**: {date}
**星期**: {weekday}
**天气**: 
**心情**: 

## 🎯 今日计划
- [ ] 
- [ ] 
- [ ] 

## 📝 工作记录
### 技术工作
- 

### 项目进展
- 

### 遇到的问题
- 

## 📚 学习收获
### 新知识
- 

### 技术洞察
- 

## 💡 灵感与思考
- 

## 🔗 相关链接
- [[{prev_date}]] ← 前一天
- [[{next_date}]] → 后一天

---
*标签: #日记*
""",

    "周总结模板.md": """# {year}年第{week}周总结

## 📊 本周概览
**时间范围**: {start_date} ~ {end_date}
**主要成就**: 
**待改进**: 

## 🎯 目标完成情况
### 已完成
- 

### 未完成
- 

## 📚 学习进展
### 技术学习
- 

### 项目实践
- 

## 💡 重要思考
### 技术洞察
- 

### 个人成长
- 

## 🎯 下周计划
### 主要目标
- 

### 学习重点
- 

---
*标签: #周总结 #日记*
""",

    "月总结模板.md": """# {year}年{month}月总结

## 📈 月度概览
**月份**: {year}年{month}月
**关键成果**: 
**主要挑战**: 

## 🎯 目标回顾
### 完成情况
- 

### 未完成原因
- 

## 📚 学习成长
### 技术能力
- 

### 软技能
- 

## 💼 工作项目
### 项目进展
- 

### 技术实践
- 

## 🔮 下月计划
### 核心目标
- 

### 学习方向
- 

---
*标签: #月总结 #日记*
""",

    "2024年1月.md": """# 2024年1月日记索引

## 📅 本月概览
**月份**: 2024年1月
**主题**: 新年开始，知识库建立

## 🗓️ 日记索引
- [[2024-01-01]] - 知识库初始化
- 

## 🎯 月度目标
- [ ] 完善知识库结构
- [ ] 制定技术学习计划
- [ ] 开始软件设计学习

## 📝 月度总结
*月底填写*

---
*标签: #月索引 #日记*
"""
}

def create_directory(path):
    """创建目录"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"创建目录: {path}")

def create_file(file_path, content=None):
    """创建文件并写入内容"""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            if content:
                # 处理动态内容
                processed_content = process_dynamic_content(content)
                f.write(processed_content)
            else:
                # 默认内容：文件名的标题
                file_name = os.path.basename(file_path).replace('.md', '')
                f.write(f"# {file_name}\n\n*本页面内容待完善...*")
        print(f"创建文件: {file_path}")

def process_dynamic_content(content):
    """处理动态内容模板"""
    now = datetime.now()
    
    replacements = {
        '{date}': now.strftime('%Y-%m-%d'),
        '{year}': now.strftime('%Y'),
        '{month}': now.strftime('%m'),
        '{week}': now.strftime('%U'),
        '{weekday}': ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][now.weekday()],
        '{start_date}': (now - timedelta(days=now.weekday())).strftime('%Y-%m-%d'),
        '{end_date}': (now + timedelta(days=6-now.weekday())).strftime('%Y-%m-%d'),
        '{prev_date}': (now - timedelta(days=1)).strftime('%Y-%m-%d'),
        '{next_date}': (now + timedelta(days=1)).strftime('%Y-%m-%d'),
        '{最近更新}': f"知识库初始化 - {now.strftime('%Y-%m-%d')}"
    }
    
    for key, value in replacements.items():
        content = content.replace(key, value)
    
    return content

def create_directory_index(dir_path, level):
    """为目录创建索引文件，列出目录下所有文件链接"""
    dir_name = os.path.basename(dir_path)
    index_file_path = os.path.join(dir_path, f"{dir_name}.md")
    
    if os.path.exists(index_file_path):
        return  # 索引文件已存在，不覆盖
    
    # 获取目录下的所有文件和子目录
    items = []
    subdirs = []
    for item in os.listdir(dir_path):
        if item == f"{dir_name}.md":
            continue  # 跳过索引文件自身
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            subdirs.append(item)
        elif item.endswith('.md'):
            items.append(item.replace('.md', ''))
    
    # 生成索引文件内容
    if level == 1:
        # 一级目录（主分类）
        index_content = f"""# {dir_name}

## 📋 目录概览

本目录包含以下内容：

"""
    else:
        # 二级及以下目录
        index_content = f"""# {dir_name}

## 📁 内容索引

"""

    # 添加子目录链接
    if subdirs:
        index_content += "### 📂 子目录\n\n"
        for subdir in sorted(subdirs):
            index_content += f"- [[{subdir}/{subdir}]]\n"
        index_content += "\n"

    # 添加文件链接
    if items:
        index_content += "### 📄 文件列表\n\n"
        for item in sorted(items):
            index_content += f"- [[{item}]]\n"
        index_content += "\n"

    # 添加导航链接
    parent_dir = os.path.basename(os.path.dirname(dir_path))
    if level > 1:
        index_content += f"## 🔗 导航\n\n"
        index_content += f"- [[../{parent_dir}]] ← 返回上级目录\n"
    
    if level == 1:
        index_content += f"- [[知识库总览]] ← 返回知识库总览\n"

    index_content += f"""
---
*本文件为自动生成的目录索引，最后更新于 {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"创建目录索引: {index_file_path}")

def create_daily_note(base_path):
    """创建今天的日记文件"""
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    year = today.strftime('%Y')
    
    # 日记文件路径 - 确保不超过4层
    diary_path = os.path.join(base_path, "80-代码片段", year)
    create_directory(diary_path)
    
    # 日记文件
    diary_file = os.path.join(diary_path, f"{date_str}.md")
    
    if not os.path.exists(diary_file):
        # 创建今天的日记
        diary_content = """# {date} 日记

## 📅 今日概览
**日期**: {date}
**星期**: {weekday}
**天气**: 
**心情**: 

## 🎯 今日计划
- [ ] 
- [ ] 
- [ ] 

## 📝 工作记录
### 技术工作
- 

### 项目进展
- 

### 遇到的问题
- 

## 📚 学习收获
### 新知识
- 

### 技术洞察
- 

## 💡 灵感与思考
- 

## 🔗 相关链接
- [[{prev_date}]] ← 前一天
- [[{next_date}]] → 后一天

---
*标签: #日记*
"""
        # 处理动态内容
        now = datetime.now()
        replacements = {
            '{date}': now.strftime('%Y-%m-%d'),
            '{weekday}': ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][now.weekday()],
            '{prev_date}': (now - timedelta(days=1)).strftime('%Y-%m-%d'),
            '{next_date}': (now + timedelta(days=1)).strftime('%Y-%m-%d')
        }
        
        for key, value in replacements.items():
            diary_content = diary_content.replace(key, value)
        
        with open(diary_file, 'w', encoding='utf-8') as f:
            f.write(diary_content)
        print(f"创建今日日记: {diary_file}")

def create_root_index(base_path):
    """为根目录创建索引文件"""
    root_index_path = os.path.join(base_path, "知识库总览.md")
    
    if os.path.exists(root_index_path):
        return
    
    # 获取根目录下的所有目录
    directories = []
    for item in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, item)) and not item.startswith('.'):
            directories.append(item)
    
    # 生成根目录索引内容
    index_content = """# 知识库总览

欢迎来到我的个人知识管理系统！这是一个专为程序员设计的Obsidian知识库。

## 🎯 设计理念

### 核心原则
1. **层级扁平化**: 目录结构不超过4层，提高访问效率
2. **完整索引系统**: 每个目录都有索引文件，便于导航
3. **技术全覆盖**: 涵盖全栈开发、DevOps、AI等关键技术领域
4. **实用导向**: 注重项目实践和代码复用

### 技术栈覆盖
- **前端**: React、Vue、HTML/CSS、Webpack
- **后端**: Spring Boot、Node.js、微服务
- **DevOps**: Docker、Kubernetes、Jenkins、Linux
- **数据库**: MySQL、MongoDB、Redis
- **软件设计**: 设计模式、架构原则、DDD
- **AI技术**: 机器学习、深度学习、自然语言处理

## 🗂️ 目录结构

"""
    
    # 添加目录链接和描述
    dir_descriptions = {
        "00-索引与导航": "知识库导航和全局索引系统",
        "10-个人知识管理": "学习方法论、工具使用和学习计划",
        "20-技术积累": "编程语言、框架、工具等核心技术知识", 
        "30-软件设计": "设计模式、软件架构、设计原则",
        "40-AI技术": "机器学习、深度学习、AI应用",
        "50-项目记录": "项目实践、问题解决和经验总结",
        "60-参考资料": "书籍笔记、文章收藏、技术资料",
        "70-代码片段": "可复用的代码库和工具函数",
        "80-日记记录": "日常记录、周总结、月总结",
        "90-待整理与临时笔记": "临时笔记和灵感记录区",
        "95-模板": "模板文件的存储",
        "99-附件": "存储附件图片"
    }
    
    for directory in sorted(directories):
        description = dir_descriptions.get(directory, "知识分类目录")
        index_content += f"- [[{directory}/{directory}]] - {description}\n"
    
    index_content += """
## 🚀 快速开始

### 新用户指南
1. **初次使用**: 查看 [[00-索引与导航/快速开始]]
2. **制定计划**: 参考 [[00-索引与导航/学习路线图]]
3. **日常记录**: 使用 [[80-代码片段/模板/日记模板]]
4. **项目管理**: 参考 [[50-项目记录/项目笔记模板]]

### 核心工作流
1. **每日**: 写日记记录工作和学习
2. **每周**: 做技术总结和计划
3. **每月**: 回顾学习进度和成果
4. **持续**: 积累代码片段和技术笔记

## 🔍 搜索与导航

### 快速搜索
- `Ctrl+O`: 快速打开文件
- `Ctrl+Shift+F`: 全局搜索
- `Ctrl+P`: 命令面板

### 标签系统
- 查看 [[00-索引与导航/标签索引]] 按标签浏览
- 使用 `#标签` 格式为笔记分类

### 图谱视图
- 使用图谱发现知识连接
- 通过链接建立知识网络

---
*知识库初始化于 {date}*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
    
    with open(root_index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"创建根目录索引: {root_index_path}")

def process_structure(current_path, structure, current_level=1):
    """递归处理目录结构，确保不超过四层"""
    if current_level > 3:  # 根目录为第1层，所以第4层是文件层
        print(f"警告: 目录层级过深，跳过 {current_path}")
        return
        
    for key, value in structure.items():
        item_path = os.path.join(current_path, key)
        
        if isinstance(value, list):
            # 创建目录
            create_directory(item_path)
            # 创建文件
            for file in value:
                file_path = os.path.join(item_path, file)
                content = file_contents.get(file)
                create_file(file_path, content)
            
            # 为该目录创建索引文件
            create_directory_index(item_path, current_level)
        elif isinstance(value, dict):
            # 创建子目录并递归处理
            create_directory(item_path)
            process_structure(item_path, value, current_level + 1)
            
            # 为该目录创建索引文件
            create_directory_index(item_path, current_level)

def create_obsidian_structure(base_path="Obsidian知识库"):
    """创建Obsidian知识管理目录结构，确保最深不超过四层"""
    
    # 定义目录结构 - 确保最深不超过四层
    structure = {
        "00-索引与导航": [
            "主页.md",
            "标签索引.md", 
            "最近更新.md",
            "学习路线图.md",
            "快速开始.md"
        ],
        "10-个人知识管理": [
            "笔记组织原则.md",
            "知识复用的技巧.md",
            "核心插件配置.md",
            "高级查询语法.md",
            "2024技术提升计划.md",
            "软件设计学习路径.md",
            "AI学习路径.md"
        ],
        "20-技术积累": {
            "编程语言": [
                "Java-并发编程笔记.md",
                "Python-高级特性.md", 
                "JavaScript-ES6新特性.md",
                "Go语言入门.md"
            ],
            "前端开发": [
                "HTML-CSS布局技巧.md",
                "React-Hooks详解.md",
                "Vue3-组合式API.md",
                "Webpack配置指南.md",
                "前端性能优化.md"
            ],
            "后端开发": [
                "SpringBoot最佳实践.md",
                "NodeJS-Express框架笔记.md",
                "RESTful-API规范.md",
                "微服务架构设计.md"
            ],
            "DevOps": [
                "Dockerfile编写指南.md",
                "Kubernetes部署实践.md",
                "Jenkins流水线配置.md",
                "Linux常用命令集.md",
                "Prometheus监控入门.md"
            ],
            "数据库": [
                "MySQL优化技巧.md",
                "MongoDB设计模式.md",
                "Redis缓存策略.md",
                "SQL优化指南.md"
            ],
            "网络与安全": [
                "HTTP协议详解.md",
                "Web安全最佳实践.md",
                "网络基础概念.md"
            ]
        },
        "30-软件设计": [
            "设计模式-工厂模式.md",
            "设计模式-观察者模式.md",
            "软件架构-微服务架构.md",
            "领域驱动设计-DDD.md",
            "SOLID原则详解.md",
            "重构案例研究.md",
            "UML类图指南.md",
            "设计原则总结.md"
        ],
        "40-AI技术": [
            "机器学习-线性回归.md",
            "机器学习-分类算法比较.md",
            "深度学习-TensorFlow使用笔记.md",
            "深度学习-PyTorch入门.md",
            "自然语言处理-BERT模型详解.md",
            "AI工具-LangChain实战.md",
            "AI应用场景分析.md",
            "论文阅读笔记模板.md"
        ],
        "50-项目记录": [
            "项目A-需求分析.md",
            "项目A-技术选型.md",
            "项目A-问题解决.md",
            "项目B-架构设计.md",
            "项目B-部署流程.md",
            "项目笔记模板.md",
            "项目总结模板.md"
        ],
        "60-参考资料": [
            "书籍-设计模式笔记.md",
            "书籍-机器学习笔记.md",
            "文章-前端性能优化.md",
            "会议-KubeCon2024亮点.md",
            "技术博客精选.md"
        ],
        "70-代码片段": [
            "前端-React组件片段.md",
            "后端-SpringBoot配置片段.md",
            "数据库-SQL查询片段.md",
            "Linux-脚本片段.md",
            "Docker-compose示例.md",
            "常用工具函数.md"
        ],
        "80-代码片段": {
            "2024年": [
                "2024年1月.md",
                "2024年2月.md",
                "2024年3月.md"
            ],
            "模板": [
                "日记模板.md",
                "周总结模板.md",
                "月总结模板.md"
            ]
        },
        "90-待整理与临时笔记": [
            "临时笔记模板.md",
            "待分类笔记模板.md",
            "灵感记录.md"
        ],
        "95-模板": [
            "模板.md",
        ],
        "99-附件": [
        ]
    }

    # 创建根目录
    create_directory(base_path)
    
    # 处理主结构
    process_structure(base_path, structure)
    
    # 创建今天的日记文件
    create_daily_note(base_path)
    
    # 为根目录创建索引文件
    create_root_index(base_path)
    
    print(f"\n✅ Obsidian知识库初始化完成！")
    print(f"📍 位置: {os.path.abspath(base_path)}")
    
    # 显示核心设计思路
    print(f"\n🎯 核心设计思路:")
    print(f"• 层级控制: 严格限制目录深度不超过4层")
    print(f"• 扁平化结构: 减少嵌套，提高访问效率")
    print(f"• 完整索引: 每个目录都有对应的索引文件")
    print(f"• 技术覆盖: 全栈开发 + DevOps + AI技术")
    print(f"• 实用导向: 包含项目记录和代码片段")

def count_files_and_dirs(path):
    """统计文件和目录数量"""
    file_count = 0
    dir_count = 0
    
    for root, dirs, files in os.walk(path):
        dir_count += len(dirs)
        file_count += len(files)
    
    return dir_count, file_count

if __name__ == "__main__":
    # 可以选择指定路径，默认为当前目录下的"Obsidian知识库"
    base_path = "Obsidian知识库"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    
    create_obsidian_structure(base_path)
    
    # 统计并显示创建结果
    dir_count, file_count = count_files_and_dirs(base_path)
    print(f"📊 创建统计: {dir_count} 个目录, {file_count} 个文件")
    print(f"📐 目录深度: 严格限制不超过4层")
    
    print(f"\n📝 下一步:")
    print(f"1. 用Obsidian打开 '{base_path}' 文件夹")
    print(f"2. 查看 [[主页]] 开始使用")
    print(f"3. 阅读 [[快速开始]] 了解基本操作")
    print(f"4. 编写今日日记 [[{datetime.now().strftime('%Y-%m-%d')}]]")