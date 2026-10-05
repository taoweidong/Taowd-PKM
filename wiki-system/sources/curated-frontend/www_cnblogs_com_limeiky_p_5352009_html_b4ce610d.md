---
source: "http://www.cnblogs.com/limeiky/p/5352009.html"
title: "jQuery+zTree加载树形结构菜单 - limeiky - 博客园"
fetched_at: "2026-10-05 15:31:39"
---

# jQuery+zTree加载树形结构菜单

由于项目中需要设计树形菜单功能，经过一番捣腾之后，终于给弄出来了，所以便记下来，也算是学习zTree的一个总结吧。

zTree的介绍：

1、zTree 是利用 JQuery 的核心代码，实现一套能完成大部分常用功能的 Tree 插件

2、zTree v3.0 将核心代码按照功能进行了分割，不需要的代码可以不用加载

3、采用了 延迟加载 技术，上万节点轻松加载，即使在 IE6 下也能基本做到秒杀

4、兼容 IE、FireFox、Chrome、Opera、Safari 等浏览器

5、支持 JSON 数据

6、支持静态 和 Ajax 异步加载节点数据

7、支持任意更换皮肤 / 自定义图标（依靠css）

8、支持极其灵活的 checkbox 或 radio 选择功能

9、提供多种事件响应回调

10、灵活的编辑（增/删/改/查）功能，可随意拖拽节点，还可以多节点拖拽哟

11、在一个页面内可同时生成多个 Tree 实例

核心的函数和属性介绍：

核心：zTree(setting, [zTreeNodes])

这个函数接受一个JSON格式的数据对象setting和一个JSON格式的数据对象zTreeNodes，从而建立 Tree。

核心参数：setting

zTree 的参数配置都在这里完成，简单的说：树的样式、事件、访问路径等都在这里配置


    var setting = {
        showLine: true,
        checkable: true
      };

因为参数太多，具体参数详见zTreeAPI

核心参数：zTreeNodes

zTree 的全部节点数据集合，采用由JSON对象组成的数据结构，简单的说：这里使用Json格式保存了树的所有信息

1、zTree官方网站： <http://www.ztree.me/v3/main.php#_zTreeInfo>

在官网能够下载到zTree的源码、实例和API，其中作者pdf的API写得非常详细

关于zTree的节点数据的获取方式分为静态（直接定义）的和动态（后台数据库加载）的

具体的配置步骤：

**第一步 —— 引入相关文件**


    <link rel="stylesheet" href="ztree/css/zTreeStyle/zTreeStyle.css" type="text/css">




备注：

1、第一个（zTreeStyle.css）是zTree的样式css文件，引入了这个，才能呈现出树形的结构样式，

2、第二个（jquery-1.9.1.min.js）是jQuery文件，因为要用到，

3、第三个（jquery.ztree.core-3.5.min.js）则是zTree的核心js文件，这个是必须的，

4、最后一个（js/jquery.ztree.excheck-3.5.min.js）则是拓展文件，主要用于单选框和复选框的功能，因为用到了复选框，所以也要要引进来。

**第二步 —— 相关配置（具体的详细配置，请到官网参考详细API文档）**


    var zTree;
    var setting = {
      view: {
        dblClickExpand: false,//双击节点时，是否自动展开父节点的标识
        showLine: true,//是否显示节点之间的连线
        fontCss:{'color':'black','font-weight':'bold'},//字体样式函数
        selectedMulti: false //设置是否允许同时选中多个节点
      },
      check:{
        //chkboxType: { "Y": "ps", "N": "ps" },
        chkStyle: "checkbox",//复选框类型
        enable: true //每个节点上是否显示 CheckBox
      },
      data: {
        simpleData: {//简单数据模式
          enable:true,
          idKey: "id",
          pIdKey: "pId",
          rootPId: ""
        }
      },
      callback: {
        beforeClick: function(treeId, treeNode) {
          zTree = $.fn.zTree.getZTreeObj("user_tree");
          if (treeNode.isParent) {
            zTree.expandNode(treeNode);//如果是父节点，则展开该节点
          }else{
            zTree.checkNode(treeNode, !treeNode.checked, true, true);//单击勾选，再次单击取消勾选
          }
        }
      }
    };

**第三步 —— 节点数据加载，呈现树形结构**

1、html页面，直接放一个ul就可以，数据最终会自动加载到这个ul元素里面


    <body>

        <ul id="user_tree" class="ztree" style="border: 1px solid #617775;overflow-y: scroll;height: 500px;"></ul>

    </body>

2、js中进行数据的加载

一，静态方式（直接定义）


    var zNodes =[
      { id:1, pId:0, name:"test 1", open:false},
      { id:11, pId:1, name:"test 1-1", open:true},
      { id:111, pId:11, name:"test 1-1-1"},
      { id:112, pId:11, name:"test 1-1-2"},
      { id:12, pId:1, name:"test 1-2", open:true},
             ];

    $(document).ready(function(){
      $.fn.zTree.init($("#user_tree"), setting, zNodes);
    });
    function onCheck(e,treeId,treeNode){
      var treeObj=$.fn.zTree.getZTreeObj("user_tree"),
      nodes=treeObj.getCheckedNodes(true),
      v="";
      for(var i=0;i<nodes.length;i++){
        v+=nodes[i].name + ",";
        alert(nodes[i].id); //获取选中节点的值
      }
    }

二、动态方式（从后台数据库加载）


    /**
     * 页面初始化
     */
    $(document).ready(function(){
      onLoadZTree();
    });

    /**
     * 加载树形结构数据
     */
    function onLoadZTree(){
      var treeNodes;
      $.ajax({
        async:false,//是否异步
        cache:false,//是否使用缓存
        type:'POST',//请求方式：post
        dataType:'json',//数据传输格式：json
        url:$('#ctx').val()+"SendNoticeMsgServlet?action=loadUserTree",//请求的action路径
        error:function(){
          //请求失败处理函数
          alert('亲，请求失败！');
        },
        success:function(data){
          //console.log(data);
          //请求成功后处理函数
          treeNodes = data;//把后台封装好的简单Json格式赋给treeNodes
        }
      });

      var t = $("#user_tree");
      t = $.fn.zTree.init(t, setting, treeNodes);
    }

**java后台加载数据代码** ：

#### 1、定义tree的VO类，这个也可以不用定义，由于我要用到其他操作，方便一些


    /**
     * zTree树形结构对象VO类
     *
     * @author Administrator
     *
     */
    public class TreeVO {
      private String id;//节点id
      private String pId;//父节点pId I必须大写
      private String name;//节点名称
      private String open = "false";//是否展开树节点，默认不展开

      public String getId() {
        return id;
      }

      public void setId(String id) {
        this.id = id;
      }

      public String getpId() {
        return pId;
      }

      public void setpId(String pId) {
        this.pId = pId;
      }

      public String getName() {
        return name;
      }

      public void setName(String name) {
        this.name = name;
      }

      public String getOpen() {
        return open;
      }

      public void setOpen(String open) {
        this.open = open;
      }

    }

2、查询数据库，并且sql的结构字段也要是id,pId,name,open(可选)这种格式（注意：pId中间的I必须大写），然后将结果封装到TreeVO类中。


    /**
       * 加载树形结构数据
       * @param request
       * @param response
       * @throws IOException
       */
      public void loadUserTree(HttpServletRequest request, HttpServletResponse response) throws IOException{
        WeiXinUserService weixinUserService = new WeiXinUserServiceImpl();
        List<TreeVO> user_tree_list = weixinUserService.getUserTreeList();
        String treeNodesJson = JSONArray.fromObject(user_tree_list).toString();//将list列表转换成json格式 返回

        PrintWriter out = response.getWriter();
        //利用Json插件将Array转换成Json格式
        out.print(treeNodesJson);

        //释放资源
        out.close();
      }

这里就完成了整个操作了，誒，文笔不好，组织语言自然就不怎么样了，大家见谅！共同学习，共同成长！
