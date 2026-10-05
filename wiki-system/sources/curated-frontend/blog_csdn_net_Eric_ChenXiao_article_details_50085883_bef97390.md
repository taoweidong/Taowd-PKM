---
source: "http://blog.csdn.net/Eric_ChenXiao/article/details/50085883"
title: "ztree+java后台取数据(包括异步)生成树状图_ztree java后台-CSDN博客"
fetched_at: "2026-10-05 15:31:24"
---

java小白初用ztree：
ztree的官网上demo已经很详细，最近项目有用到树桩结构，自己就选择了ztree,下面从后台取数据生成树状结构的源码，官网上用到的php.
1.项目jar包：
![这里写图片描述](https://img-blog.csdn.net/20151128173500862)
2.实体类ZtreeNode.java，生成demo中的zNodes:
![这里写图片描述](https://img-blog.csdn.net/20151128174251466)
示例代码：


    package com.demo.ztree.entity;

    public class ZtreeNode {
        private String id;
        private Integer state;
        private String pid;
        private String icon;
        private String iconClose;
        private String iconOpen;
        private String name;
        private boolean open;
        private boolean isParent;

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("{id:\"");
            sb.append(id);
            sb.append("\",pId:\"");
            sb.append(pid);
            sb.append("\",name:\"");
            sb.append(name);
            sb.append("\",state:");
            sb.append(state);
            sb.append(",icon:\"");
            sb.append(icon);
            sb.append("\",iconClose:\"");
            sb.append(iconClose);
            sb.append("\",iconOpen:\"");
            sb.append(iconOpen);
            sb.append("\",open:\"");
            sb.append(open);
            sb.append("\",isParent:\"");
            sb.append(isParent);
            sb.append("\"}");
            return sb.toString();
        }

        public String getIcon() {
            return icon;
        }

        public void setIcon(String icon) {
            this.icon = icon;
        }

        public String getIconClose() {
            return iconClose;
        }

        public void setIconClose(String iconClose) {
            this.iconClose = iconClose;
        }

        public String getIconOpen() {
            return iconOpen;
        }

        public void setIconOpen(String iconOpen) {
            this.iconOpen = iconOpen;
        }

        public boolean isOpen() {
            return open;
        }

        public void setOpen(boolean open) {
            this.open = open;
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public String getPid() {
            return pid;
        }

        public void setPid(String pid) {
            this.pid = pid;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public boolean isIsParent() {
            return isParent;
        }

        public void setIsParent(boolean isParent) {
            this.isParent = isParent;
        }


        public Integer getState() {
            return state;
        }

        public void setState(Integer state) {
            this.state = state;
        }

        public static void main(String[] args) {
            ZtreeNode ztree1 = new ZtreeNode();
            ztree1.setId("1");
            ztree1.setPid("0");
            ztree1.setName("顶层节点");
            System.out.println(ztree1);
        }
    }



其中，id、pid、isparent必须，其他的根据需求添加
3.在action中给ZtreeNode属性取值，根据业务，在数据库中取相应值，这里我就直接生成一些值：
这里根据取值过程，分为2中方式：
(1).一次性取值，传到页面：
示例代码：


    public String showTree() {
            for(int i=-1;i<100000;i++){
                if(i<0){
                    ZtreeNode ztree = new ZtreeNode();
                    ztree.setId("0");
                    ztree.setName("顶层节点 ");
                    ztree.setIsParent(true);
                    ztree.setIcon(icon);
                    ztree.setIconClose(iconClose);
                    ztree.setIconOpen(iconOpen);
                    listTree.add(ztree);
                }else{
                    ZtreeNode ztree = new ZtreeNode();
                    ztree.setId(""+(i+1));
                    ztree.setName("级节点");
                    ztree.setPid(""+i/10);
                    ztree.setIcon(icon);
                    ztree.setIconClose(iconClose);
                    ztree.setIconOpen(iconOpen);
                    listTree.add(ztree);
                }
            }
            return SUCCESS;
        }

(2).异步取值返回页面：
示例代码：


    public String getTree() {
            return SUCCESS;
        }
        public String asyncTree() {

            String pid = getRequest().getParameter("id");
            if(pid==null ||pid.equals("")){
                pid="0";
                ZtreeNode ztree = new ZtreeNode();
                ztree.setId("1");
                ztree.setName("顶级节点");
                ztree.setIsParent(true);
                ztree.setState(1);
                ztree.setIcon(icon);
                ztree.setIconClose(iconClose);
                ztree.setIconOpen(iconOpen);
                listTree.add(ztree);

            }else{
                for(int i=0;i<40;i++){
                    ZtreeNode ztree = new ZtreeNode();
                    ztree.setId(pid+i);
                    ztree.setName(""+pid.length()+"级节点");
                    ztree.setState(1);
                    ztree.setIcon(icon);
                    ztree.setIconClose(iconClose);
                    ztree.setIconOpen(iconOpen);
                    if(pid.length()<4){
                        ztree.setIsParent(true);
                    }
                    listTree.add(ztree);
                }
            }
            json = JSONArray.fromObject(listTree);
            return SUCCESS;
        }

4.页面
(1).一次性取值，传到页面：
示例代码：


    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>ztree</title>
    <link href="${request.contextPath}/css/zTreeStyle/zTreeStyle.css" rel="stylesheet" type="text/css">



         var zNodes = ${listTree};
        var setting = {
                check: {
                    enable: true,
                    chkboxType: {"Y":"s", "N":"ps"}
                },
                data: {
                    simpleData: {
                        enable: true
                    }
                }
            };
        $(document).ready(function(){
            $.fn.zTree.init($("#treeDemo"), setting, zNodes);
        });


    </head>
    <body>

            <ul id="treeDemo" class="ztree"></ul>


    <body >
    </html>

(2).异步取值返回页面：
示例代码：


    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>ztree</title>
    <link href="${request.contextPath}/css/zTreeStyle/zTreeStyle.css" rel="stylesheet" type="text/css">



    var setting = {
                view: {
                    showLine: false,
                    addDiyDom: addDiyDom
                },
                async: {
                    enable: true,
                    autoParam: ["id"],
                    url: "${request.contextPath}/asyncTree.action",
                    dataFilter: filter
                },
                check: {
                    enable: true,
                    chkboxType: {"Y":"s", "N":"ps"}
                },
                callback: {
                    onAsyncSuccess: zTreeOnAsyncSuccess
                },
                data: {
                    simpleData: {
                        enable: true
                    }
                }
            };
        $(document).ready(function(){
            $.fn.zTree.init($("#treeDemo"), setting);
        });

        var zTree = $.fn.zTree.getZTreeObj("treeDemo");

    function zTreeOnAsyncSuccess(event, treeId, treeNode, msg) {
        if(treeNode==null){
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            nodes = zTree.getNodes();
            for (var i=0, l=nodes.length; i<l; i++) {
                zTree.expandNode(nodes[i], true, false, false);
            }
            asyncNodes(zTree.getNodes());
             if (!goAsync) {
                curStatus = "";
             }
        }
    };

    function asyncNodes(nodes) {
            if (!nodes) return;
            curStatus = "async";
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            for (var i=0, l=nodes.length; i<l; i++) {
                if (nodes[i].isParent && nodes[i].zAsync) {
                    asyncNodes(nodes[i].children);
                } else {
                    goAsync = true;
                    zTree.reAsyncChildNodes(nodes[i], "refresh", true);
                }
            }
        }

    function filter(treeId, parentNode, childNodes) {
                if (!childNodes) return null;
                for (var i=0, l=childNodes.length; i<l; i++) {
                    childNodes[i].name = childNodes[i].name.replace(/\.n/g, '.');
                }
                return childNodes;
            }

    function addDiyDom(treeId, treeNode) {
        var aObj = $("#" + treeNode.tId + "_a");
        if ($("#diyBtn_"+treeNode.id).length>0) return;
        switch (treeNode.state) {
            case 0:
                var editStr = " 未审核 ";
                break;
            case 1:
                var editStr = " 正常 ";
                break;
            case 2:
                var editStr = " 锁定 ";
                break;
            default:
                var editStr = " 未知状态 ";
                break;
            }
        aObj.append(editStr);
    }


    </head>
    <body>

            <ul id="treeDemo" class="ztree"></ul>


    <body >
    </html>

5.struts.xml配置：


    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE struts PUBLIC
        "-//Apache Software Foundation//DTD Struts Configuration 2.3//EN"
        "http://struts.apache.org/dtds/struts-2.3.dtd">

    <struts>

        <constant name="struts.devMode" value="true" />

            <result-types>
                <result-type name="json" class="org.apache.struts2.json.JSONResult"/>
            </result-types>
            <interceptors>
                <interceptor name="json" class="org.apache.struts2.json.JSONInterceptor"/>
            </interceptors>


            <action name="showTree" class="com.demo.ztree.action.HelloAction"
                method="showTree">
                <result name="success" type="freemarker">/hello.ftl</result>
            </action>
            <action name="getTree" class="com.demo.ztree.action.HelloAction"
                method="getTree">
                <result name="success" type="freemarker">asyncZtree.ftl</result>
            </action>
            <action name="asyncTree" class="com.demo.ztree.action.HelloAction"
                method="asyncTree">
                 <result name="success" type="json">
                          json
                 </result>
            </action>


    </struts>

6.效果图：
![这里写图片描述](https://img-blog.csdn.net/20151128181028454)
7.可以根据自己的业务要求自己选用和改进，这里包含了：
(1)checked框的提交;
(2)异步加载，显示1级节点后，后台自动加载下级节点。
