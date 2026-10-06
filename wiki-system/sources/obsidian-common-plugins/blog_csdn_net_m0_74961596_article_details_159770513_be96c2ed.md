---
source: "https://blog.csdn.net/m0_74961596/article/details/159770513"
title: "Obsidian最强绘图插件Excalidraw完全指南：从零基础到高手进阶_obsidian excalidraw-CSDN博客"
fetched_at: "2026-10-06 12:48"
---

> 作者：吃一根烤肠
> 
> 日期：2026年4月2日

### 一、为什么你需要Excalidraw？

在知识管理领域，纯文字笔记已经无法满足复杂思维的表达需求。根据认知心理学研究，人脑处理视觉信息的速度是文字的60,000倍。这意味着，当你用图形化方式组织知识时，理解效率将呈指数级提升。

**Excalidraw** 正是为此而生——它将专业级绘图工具Excalidraw深度整合进Obsidian，让你的笔记库从“文字仓库”进化为“视觉思维工作台”。

#### 1.1 Excalidraw的核心优势

优势 |  说明  
---|---  
**零学习成本** ​ |  手绘风格设计，不追求像素级精准，降低心理门槛  
**深度集成** ​ |  与Obsidian双向链接无缝结合，不是简单的插件嵌入  
**无限扩展** ​ |  内置ExcalidrawAutomate脚本引擎，支持JavaScript自动化  
**文件一体化** ​ |  画板数据可嵌入.md文件，文字和图形共存于同一文件  
**跨平台协作** ​ |  支持实时协作，适合远程团队头脑风暴  
  
#### 1.2 与Obsidian白板(Canvas)的区别

很多用户会混淆Excalidraw和Obsidian自带的Canvas功能，两者有本质区别：

特性 |  Excalidraw |  Canvas  
---|---|---  
**文件格式** ​ |  `.excalidraw`或嵌入`.md` |  `.canvas`(独立JSON文件)  
**与笔记集成** ​ |  可嵌入.md文件，同一文件包含文字和图形 |  独立文件，需单独管理  
**打开方式** ​ |  可设置默认以Markdown模式打开 |  总是以画板模式打开  
**手绘功能** ​ |  专门的手绘笔迹工具(快捷键7) |  无专门手绘工具  
**AI支持** ​ |  支持AI生成图表 |  基础绘图功能  
  
### 二、安装与配置：3分钟快速上手

#### 2.1 安装方法

##### 方法一：社区插件商店安装（推荐）

  1. 打开Obsidian，进入 **设置** ​ → **第三方插件**

  2. 关闭“安全模式”（首次安装需要）

  3. 点击“浏览”，搜索 **Excalidraw**

  4. 找到由Zsolt Viczian开发的插件，点击“安装”

  5. 安装完成后，**启用插件**




##### 方法二：手动安装（适用于网络受限环境）
    
    
    # 克隆中文版插件仓库
    git clone https://github.com/korbinzhao/obsidian-excalidraw-cn-plugin.git
    cd obsidian-excalidraw-cn-plugin
    npm install
    npm run build

将生成的`main.js`、`manifest.json`、`styles.css`文件复制到Obsidian插件目录：`.obsidian/plugins/obsidian-excalidraw-plugin/`

#### 2.2 关键配置项

安装后建议立即调整以下设置（**设置** ​ → **Excalidraw** ）：

设置项 |  推荐值 |  说明  
---|---|---  
**Excalidraw文件夹** ​ |  `Drawing/`或 `Visual/` |  集中管理所有绘图文件  
**模板文件夹** ​ |  `Templates/Excalidraw/` |  存放常用绘图模板  
**默认模式** ​ |  查看模式 |  打开文件时默认显示模式  
**自动导出** ​ |  开启PNG/SVG |  保存时自动生成图片文件  
**新文件自动加日期** ​ |  关闭 |  避免文件名冗长  
  
#### 2.3 创建第一个绘图文件

**方式一：命令面板**

  * 按下 `Ctrl+P`（Windows）或 `Cmd+P`（Mac）

  * 输入"Excalidraw"

  * 选择"新建Excalidraw图纸"




**方式二：工具栏**

  * 插件启用后，左侧工具栏会多出Excalidraw图标

  * 点击图标直接新建




**方式三：快捷键**

  * 可在快捷键设置中自定义新建绘图快捷键




### 三、基础绘图功能详解

#### 3.1 工具栏与快捷键

Excalidraw的工具栏每个工具都标有数字，按数字键可直接切换工具：

工具 |  快捷键 |  功能  
---|---|---  
**选择工具** ​ |  1 |  选中、移动、调整元素大小  
**矩形** ​ |  2 |  绘制长方形/正方形  
**菱形** ​ |  3 |  绘制菱形  
**椭圆** ​ |  4 |  绘制椭圆/圆形  
**箭头** ​ |  5 |  绘制带箭头的连接线  
**直线** ​ |  6 |  绘制直线  
**手绘笔迹** ​ |  7 |  自由绘制路径  
**文本** ​ |  8 |  添加文字标注  
**橡皮擦** ​ |  0 |  删除选中元素  
  
#### 3.2 实用操作技巧

操作 |  方法 |  说明  
---|---|---  
**选中多个元素** ​ |  按住`Shift`点击多个元素，或框选 |  批量操作  
**复制元素** ​ |  选中后按住`Alt`键拖动 |  快速复制  
**自动对齐** ​ |  默认开启，按住`Shift`临时禁用 |  精确控制位置  
**全选** ​ |  按`A`键 |  选择画布所有元素  
**缩放画布** ​ |  `Ctrl/Cmd`\+ 鼠标滚轮 |  调整视图大小  
**平移画布** ​ |  `Space`\+ 拖拽，或鼠标中键拖拽 |  移动画布  
  
#### 3.3 元素样式设置

##### 3.3.1 颜色与填充
    
    
    // 样式属性示例
    {
      strokeColor: "red",        // 边框颜色
      backgroundColor: "#FF0000", // 填充颜色  
      fillStyle: "hachure"       // 填充样式：阴影线/交叉线/实心
    }

##### 3.3.2 线条样式

  * **strokeWidth** : 线条粗细（数字，值越大越粗）

  * **strokeStyle** : 线条风格（solid实线/dashed虚线/dotted点线）

  * **strokeSharpness** : 线角锐度（round圆角/sharp尖角）

  * **roughness** : 粗糙度/手绘感（0建筑风/1艺术风/2漫画风）




##### 3.3.3 文字样式

  * **fontFamily** : 字体（1-Virgil/2-Helvetica/3-Cascadia）

  * **fontSize** : 字号（默认20px）

  * **textAlign** : 水平对齐（left/center/right）

  * **verticalAlign** : 垂直对齐（top/middle）




### 四、与Obsidian深度集成

#### 4.1 双向链接与嵌入

Excalidraw最强大的功能之一是与Obsidian的双向链接系统深度集成：

##### 4.1.1 在绘图中插入笔记链接
    
    
    # 在Excalidraw文本框中输入
    [[我的笔记]]           # 链接到整个笔记
    [[我的笔记#章节标题]]   # 链接到特定章节
    [[我的笔记#^块引用ID]]  # 链接到特定块

##### 4.1.2 在笔记中嵌入绘图
    
    
    # 在Markdown笔记中
    ![[我的绘图.excalidraw]]           # 嵌入完整绘图
    ![[我的绘图.excalidraw|400]]       # 指定宽度400px
    ![[我的绘图.excalidraw|400|left]]  # 指定宽度并左对齐

##### 4.1.3 拖拽嵌入

  * 直接从文件管理器拖拽Markdown文件到画布，会嵌入为笔记预览卡片

  * 拖拽图片文件到画布，直接显示图片

  * 拖拽网页链接到画布，创建可点击的链接




#### 4.2 "二合一"文件模式（重点！）

Excalidraw支持将画板数据压缩后嵌入.md文件末尾，实现**一个文件同时包含文字和图形** 。

##### 4.2.1 配置步骤

  1. **创建模板文件** ：在模板文件夹中新建`Excalidraw模板.md`

  2. **添加Frontmatter** ：



    
    
    ---
    excalidraw-plugin: parsed
    excalidraw-open-md: true
    ---

  1. **添加画板数据** ：

  2. **插件设置** ：在Excalidraw设置中指定模板文件路径




##### 4.2.2 优势

  * **统一管理** ：文字和图形在同一文件中，无需分开管理

  * **版本控制友好** ：Git等版本控制系统可以更好地跟踪变更

  * **搜索索引** ：画板中的文字内容也能被Obsidian搜索到

  * **反向链接** ：绘图中的链接会出现在目标笔记的反向链接中




### 五、高级功能与自动化

#### 5.1 ExcalidrawAutomate脚本引擎

这是Excalidraw最强大的功能之一。通过JavaScript脚本，你可以自动创建复杂的图形、连接线、思维导图等。

##### 5.1.1 快速入门
    
    
    // 在Templater、QuickAdd或DataviewJS中使用
    const ea = ExcalidrawAutomate;
    ea.reset();  // 重置所有设置为默认值

##### 5.1.2 基础脚本示例
    
    
    // 创建简单图形
    const ea = ExcalidrawAutomate;
    ea.reset();
    
    // 添加矩形
    ea.addRect(-150, -50, 450, 300);
    
    // 添加文本
    ea.addText(-100, 70, "Left to right");
    
    // 添加箭头
    ea.addArrow([[-100, 100], [100, 100]]);
    
    // 设置样式
    ea.style.strokeColor = "red";
    
    // 创建绘图
    await ea.create();

##### 5.1.3 连接两个对象
    
    
    const ea = ExcalidrawAutomate;
    ea.reset();
    
    const a = ea.addRect(-100, -100, 100, 100);
    const b = ea.addEllipse(200, 200, 100, 100);
    
    // 连接对象，2个控制点
    ea.connectObjects(a, "bottom", b, "left", {numberOfPoints: 2});
    
    ea.style.strokeColor = "red";
    // 连接对象，1个控制点
    ea.connectObjects(a, "right", b, "top", 1);
    
    await ea.create();

##### 5.1.4 使用模板创建图纸
    
    
    const ea = ExcalidrawAutomate;
    ea.reset();
    
    await ea.create({
      filename: "我的图纸",
      foldername: "我的文件夹/",
      templatePath: "Excalidraw/模板.excalidraw",
      onNewPane: true
    });

#### 5.2 AI生成图表

Excalidraw 2.4版本后支持AI生成图表功能：

  1. **生成下级文本框** ：插入矩形文本框，点击文本框，按住`Ctrl + 上下左右键`，就可以生成思维导图

  2. **AI提示生成** ：点击工具栏上的"AI"图标，输入文字描述，AI自动生成图表框架




**AI提示词技巧** ：

  * 与其说"帮我画个系统"，不如说："左侧是React前端，右侧是Node.js后端，中间用REST连接，后端下方是PostgreSQL"

  * 主谓宾清晰的指令，AI才能准确理解




#### 5.3 素材库管理

Excalidraw支持创建和使用素材库，提高绘图效率：

##### 5.3.1 保存个人素材

  1. 选中画布上的图形

  2. 点击右上角的【素材库】按钮

  3. 点击图形缩略图上方的【+】按钮，储存到个人素材库




##### 5.3.2 使用公共素材库

  1. 点击素材库底部的【浏览素材库】按钮

  2. Excalidraw会打开新标签页，里面有大量已发布的图形库

  3. 点击喜欢的素材下面的【Add to Excalidraw】按钮




**常用公共素材库** ：

  * **AWS、GCP、Kubernetes图标库** ：直接拖拽云服务图标

  * **流程图、UML图形库** ：标准化的图形，让图表更规范




##### 5.3.3 发布个人素材

  1. 把自己的作品编组（`Cmd+G`）

  2. 选中作品，添加到个人素材库

  3. 点击右上角三个点，选择【发布】

  4. 填写必要信息，提交审核




### 六、实战应用场景

#### 6.1 技术架构图绘制

**最佳实践** ：

  1. **颜色规范** ：用不同颜色区分不同的微服务（例如，用户服务用蓝色，订单服务用绿色）

  2. **填充区分** ：用斜线填充表示外部系统或第三方服务，与内部系统区分

  3. **组件复用** ：将常用组件（服务器+数据库+标签）保存为素材




**Python批量生成架构图示例** ：
    
    
    from Excalidraw_Interface import SketchBuilder
    
    sb = SketchBuilder(roughness=2)
    
    # 创建组件
    api = sb.Rectangle(x=0, y=0, label="API网关")
    user_svc = sb.Rectangle(x=0, y=180, label="用户服务", backgroundColor="#e1f5fe")
    order_svc = sb.Rectangle(x=220, y=180, label="订单服务", backgroundColor="#f3e5f5")
    db = sb.Diamond(x=110, y=380, label="数据库")
    
    # 连接箭头
    sb.create_binding_arrows(api, user_svc)
    sb.create_binding_arrows(api, order_svc)
    sb.create_binding_arrows(user_svc, db, sb.DoubleArrow)
    sb.create_binding_arrows(order_svc, db, sb.DoubleArrow)
    
    # 分组管理
    services = sb.create_bounding_element([user_svc, order_svc])
    sb.export_to_file("microservice_architecture.excalidraw")
    print("架构图已生成！")

#### 6.2 思维导图制作

**Excalidraw 2.4思维导图功能** ：

  * 插入矩形文本框

  * 点击文本框，按住`Ctrl + 上下左右键`生成下级文本框

  * 自动创建连接线，形成完整的思维导图结构




**与传统思维导图工具对比优势** ：

  * **双向链接** ：每个节点都可以链接到Obsidian笔记

  * **手绘风格** ：更自然，减少"完美主义"压力

  * **无限画布** ：不受页面限制，自由扩展




#### 6.3 会议记录与项目规划

**八爪鱼结构法** ：

  1. 中心写会议主题/项目名称

  2. 每个分支记录一个讨论点/任务

  3. 每个节点添加`[[相关笔记]]`链接

  4. 用颜色区分：已完成（绿色）、进行中（黄色）、未开始（红色）




**优势** ：比纯文字记录更直观，回头补笔记效率更高，不容易变成纯字堆砌的灾难现场

#### 6.4 幻灯片演示

配合**slideshow** 插件，Excalidraw可以制作手绘风格PPT：

  1. **安装slideshow** ：在Excalidraw右上角点击小花花🌺，找到slideshow安装

  2. **创建演示路径** ：用箭头工具对演示顺序进行描摹

  3. **演示控制** ：左上角会出现scripts按钮，点击即可开始演示




**演示技巧** ：

  * 先画一个左上角到右下角的箭头，让观众看到演示全貌

  * 再逐个元素划一下，控制显示顺序

  * 搭配录屏工具，制作高级感知识演示视频




### 七、工作流优化技巧

#### 7.1 快捷键工作流

**纯键盘操作流程** ：

操作 |  快捷键  
---|---  
切换选中下一个元素 |  Tab  
切换选中上一个元素 |  Shift+Tab  
移动选中元素 |  方向键  
进入文本编辑 |  Enter（选中文本元素时）  
退出编辑，回到选中状态 |  Esc  
复制选中元素 |  Ctrl/Cmd + D  
删除选中元素 |  Backspace 或 Delete  
全选 |  Ctrl/Cmd + A  
  
#### 7.2 导出与分享

##### 7.2.1 自动导出设置

在Excalidraw设置中开启**自动导出** 功能：

  * 保存时自动生成PNG/SVG文件

  * 可设置导出透明背景、深浅色模式

  * 适合插入博客、文档、演示文稿




##### 7.2.2 导出格式选择

  * **PNG图片** ：适合文章配图、演示文稿，可选择是否透明背景

  * **SVG矢量图** ：放大不会失真，在Web开发中尤其常用

  * **嵌入代码** ：可直接将SVG代码嵌入到HTML中




#### 7.3 团队协作规范

制定"Excalidraw设计规范"，提升图表可读性：

  * **所有微服务** ：用矩形+服务名+负责人标签

  * **数据库** ：统一使用圆柱图标

  * **异步消息** ：用波浪箭头

  * **同步调用** ：用直线箭头

  * **性能瓶颈区域** ：用红色虚线框高亮




#### 7.4 与Claude Code集成

使用**excalidraw-diagram** ​ Skill，让AI帮你画图：

  1. **下载Skill** ：从GitHub下载excalidraw-diagram Skill

  2. **放置目录** ：放进`~/.claude/skills/`目录下

  3. **使用** ：在Claude Code里输入`/excalidraw-diagram`，描述想画的内容




**扩展版Skill** ：obsidian-excalidraw，专门生成直接嵌入.md文件的画板

### 八、常见问题与解决方案

#### 8.1 安装问题

**问题1** ：插件市场无法加载

  * **解决方案** ：重启Obsidian或多次尝试打开插件市场

  * **备选方案** ：手动安装插件




**问题2** ：中文手写字体不显示

  * **解决方案** ：找到Excalidraw插件目录，将.ttf字体文件复制到该文件夹下

  * **路径查找** ：新建Excalidraw文件 → 右键 → "在系统资源管理器中显示"




#### 8.2 使用问题

**问题1** ：画布元素无法对齐

  * **解决方案** ：按住`Shift`键临时禁用自动对齐

  * **使用网格** ：开启网格显示，辅助对齐




**问题2** ：文件管理混乱

  * **解决方案** ：使用"二合一"文件模式，文字和图形在同一文件

  * **文件夹组织** ：设置专门的`Drawing/`文件夹集中管理




**问题3** ：性能问题（大型绘图卡顿）

  * **解决方案** ：

    1. 使用分组功能（`Cmd+G`）管理复杂元素

    2. 分层绘制，使用图层管理

    3. 定期清理不需要的历史版本




#### 8.3 导出问题

**问题** ：导出的图片模糊

  * **解决方案** ：

    1. 导出时选择SVG格式（矢量图，无限放大不模糊）

    2. 调整导出分辨率设置

    3. 使用"适应内容到屏幕"（`Shift+1`）确保所有内容可见




### 九、最佳实践总结

#### 9.1 新手入门路径

  1. **第一周** ：熟悉基本工具（矩形、箭头、文本），尝试绘制简单流程图

  2. **第二周** ：学习双向链接，在绘图中插入`[[笔记链接]]`

  3. **第三周** ：掌握"二合一"文件模式，统一管理文字和图形

  4. **第四周** ：探索自动化脚本，尝试用代码生成图表




#### 9.2 效率提升技巧

  1. **模板化** ：将常用图表保存为模板，如会议记录模板、流程图模板

  2. **素材库** ：建立个人素材库，保存常用组件

  3. **快捷键** ：掌握数字键切换工具，提升操作速度

  4. **颜色规范** ：制定团队颜色规范，提升图表一致性




#### 9.3 思维模式转变

Excalidraw最迷人的地方，是它模糊了"思考"与"表达"的边界。过去，我们通常是先想清楚，再动手画图；而现在，画图的过程本身就是思考的一部分。

**一位架构师的经验** ："我现在开会不带PPT了，直接开个Excalidraw房间。边讲边画，听众能实时看到我的思维路径。有时候他们一句话提醒，我就当场改图，比会后发邮件来回澄清高效太多了。"

### 十、资源推荐

#### 10.1 官方资源

  * **Excalidraw官网** ：[https://excalidraw.com](https://excalidraw.com/ "https://excalidraw.com")

  * **Obsidian插件页面** ：社区插件市场搜索"Excalidraw"

  * **GitHub仓库** ：<https://github.com/excalidraw/excalidraw>




#### 10.2 学习资源

  * **官方文档** ：插件设置中的"帮助与问题"

  * **视频教程** ：YouTube搜索"Obsidian Excalidraw tutorial"

  * **社区讨论** ：Obsidian官方论坛Excalidraw板块




#### 10.3 素材资源

  * **公共素材库** ：Excalidraw内置的"浏览素材库"

  * **图标集合** ：AWS、GCP、Kubernetes等专业图标库

  * **模板分享** ：Obsidian社区分享的Excalidraw模板




### 结语

Excalidraw在Obsidian中的存在，不是画图的附属品，更像是思维流动时的一条副通道。它不强迫你成为设计师，也不要求你精通快捷键。它只是静静地在那里，等你把脑子里的想法"画出来"。

每次画完一张图，都有一种把乱糟糟的脑袋重新整理好的爽感，像给自己的思维按了个重置键。在这个越来越依赖远程协作的世界里，我们比以往任何时候都更需要一种能够快速传递复杂思想的媒介。

Excalidraw的成功，不只是因为它的技术实现有多先进，而是因为它真正理解了用户的需求：我们要的不是另一个PowerPoint替代品，而是一支永远不会没墨的数字钢笔，一张永远擦不破的草图纸。

开始你的Excalidraw之旅吧，让视觉思维为你的知识管理注入新的活力！

**关注我，持续更行效率工具...**
