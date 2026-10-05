---
source: "http://www.cnblogs.com/wuhuacong/p/3317223.html"
title: "基于MVC4+EasyUI的Web开发框架形成之旅--界面控件的使用 - 伍华聪 - 博客园"
fetched_at: "2026-10-05 15:31:29"
---

在前面介绍了两篇关于我的基于MVC4+EasyUI技术的Web开发框架的随笔，本篇继续介绍其中界面部分的一些使用知识，包括控件的赋值、取值、清空，以及相关的使用。

我们知道，一般Web界面包括的界面控件有：单行文本框、多行文本框、密码文本框、下拉列表Combobox、日期输入控件、数值输入控件、单项选择、复选框、表格控件DataGrid、树形控件、布局控件、弹出式对话框、提示信息、列表控件等，这些界面控件的操作都有哪些不同，下面我们来逐一进行介绍。

![](https://images0.cnblogs.com/blog/8867/201309/22154622-0076dcd508ba4355840ff1905c1442f5.png)

### 1、单行文本框

使用easyui的控件，单行文本可以使用easyui-validatebox样式即可，类型为text的控件。

![](https://images0.cnblogs.com/blog/8867/201309/22154825-2bf2d6b2ed5e4e1ebd29dbe05c991918.png)

界面代码如下所示：


    <input class="easyui-validatebox" type="text" id="Name" name="Name" />
    或者
    <input type="text" ID="txtLoginName" name="txtLoginName" style="width:100px"  />

赋值给界面控件代码如下：


    $("#Name").val(info.Name);

获取界面控件的值代码如下：


    var name = $("#Name").val();

如果是标签Lable控件，这需要把val 使用text替代即可，如下代码所示：


    $("#Name").text(info.Name);

对于easyui-validatebox样式的控件，一般来说，有几个常见属性可以设置他们的。


    //必输项：
     <input class="easyui-validatebox" type="text" name="name" data-options="required:true"></input>

    //格式的验证：
     <input class="easyui-validatebox" type="text" name="email" data-options="validType:'email'"></input>
     <input class="easyui-validatebox" type="text" name="email" data-options="required:true,validType:'url'"></input>

    //长度范围的验证：
     <input class="easyui-validatebox" data-options="validType:'length[1,3]'">

### 2、多行文本框

easyui的界面样式，可以使用easyui-validatebox，或者默认的textarea即可。

![](https://images0.cnblogs.com/blog/8867/201309/22154931-3f09390a17fa4558b76586efb1f1ed21.png)

界面代码如下所示：


    <textarea id="type_Remark" class="easyui-validatebox" required="true" style="height:100px;"></textarea>

或者


    <textarea style="height:60px;width:200px" id="type_Remark" name="Remark"></textarea>

赋值给界面控件代码如下：


    $("#type_Remark").val(json.Remark);

获取界面控件的值代码如下：


     var text = $("#type_Remark").val();

### 3、密码文本框

密码文本框和常规的文本框一样，只是输入字符的时候，系统做了屏蔽显示而已，把它作为一个来独立说明，也是因为它也是常见输入的一种。

![](https://images0.cnblogs.com/blog/8867/201309/22155215-4aecd8e74673446abf03941484516320.png)

界面代码如下所示：


     <input type="password" name="password" style="width:260px;"></input>

赋值给界面控件代码如下：


    var password = '123';
    $("#Password").val(password)

获取界面控件的值代码如下：


                $("#btnLogin").click(function () {
                    var postData = {
                        UserName: $("#UserName").val(),
                        Password: $("#Password").val(),
                        Code: $("#Code").val()
                    };

### 4、下拉列表Combobox

常见的EasyUI的ComboBox是可以输入，也可以从列表选择的内容的输入控件。

![](https://images0.cnblogs.com/blog/8867/201309/22155816-e75b872b4b1e435da5f3fc59dc14772c.png)

界面代码如下所示：


    <input class="easyui-combobox" type="text" id="type_PID1" name="PID" />

绑定下拉列表的数据源代码如下：


                $('#type_PID1').combobox({
                    url: '/DictType/GetDictJson',
                    valueField: 'Value',
                    textField: 'Text'
                });

设置控件的选择的内容代码如下：


    $("#type_PID1").combobox('setValue', json.PID);

获取界面控件的值代码如下：


    var systemType=  $("#txtSystemType_ID").combobox('getValue');

而利用标准的Select控件虽然可以实现从列表选择，不过不够ComboBox控件那么灵活方便，Select控件的界面代码如下：

![](https://images0.cnblogs.com/blog/8867/201309/22160046-d867a9aa1a2c45be82adc38d5df8bb84.png)


    <select id="txtPID" style="width: 100%" > </select>

### 5、日期输入控件

easyui使用class=‘easyui-datebox’来标识日期控件，从弹出的层中选择正确的日期，是一种非常常见的界面输入控件，可以替代My97DatePicker日期输入控件。

![](https://images0.cnblogs.com/blog/8867/201309/22160431-1ac11199b022497eb42699ad857befbc.png)

弹出窗体界面效果如下。

![](https://images0.cnblogs.com/blog/8867/201309/22160441-f6320ef46ca64400910532018bba5392.png)

它的界面代码如下所示：


    <input class="easyui-datebox" type="text" ID="txtLastUpdated" name="txtLastUpdated" style="width:100px"  />

赋值给界面控件代码如下：


    $("#LastUpdated").datebox('setValue', info.LastUpdated);

获取界面控件的值代码如下：


    var lastupate = $("#txtLastUpdated").datebox('getValue');

### 6、数值输入控件

easyui使用样式easyui-numberbox标识为数值类型，其表现为文本框，但只能输入数值。

![](https://images0.cnblogs.com/blog/8867/201309/22161155-4859195ed83d4096adcc74f1db52653c.png)

界面代码如下所示：


    <input class="easyui-numberbox" data-options="min:10,max:90,precision:2,required:true">

或者使用‘easyui-numberspinner’样式来标识，可以上下调节数值。

![](https://images0.cnblogs.com/blog/8867/201309/22161246-d241e97c9815425f9474ffa496a5685b.png)


    <input class="easyui-numberspinner" data-options="min:10,max:100,required:true" style="width:80px;"></input>

赋值给界面控件代码如下：


    $('#nn').numberbox('setValue', 206.12);

或者


    $('#ss').numberspinner('setValue', 8234725);

获取界面控件的值代码如下：


    var v = $('#nn').numberbox('getValue');

或者


    var v = $('#ss').numberspinner('getValue');

### 7、单项选择Radio控件

单项选择Radio控件，是在多项内容里面选择一个选项进行保存或者显示。

![](https://images0.cnblogs.com/blog/8867/201309/22161547-eabd4c0fe9cf4cd29319a787483e65d1.png)

界面代码如下所示：


                        <tr>
                            <th>
                                <label>数据分开方式：</label>
                            </th>
                            <td>
                                <input name="SplitType" type="radio" class="easyui-validatebox" checked="checked" required="true" value="Split">分隔符方式，多个数据中英文逗号，分号，斜杠或顿号[, ， ; ； / 、]分开，或一行一个

                                <input name="SplitType" type="radio" class="easyui-validatebox" required="true" value="Line">一行一个记录模式，忽略所有分隔符号
                            </td>
                        </tr>

赋值给界面控件代码如下：


    $('input:radio[name="SplitType"][value="Split"]').prop('checked', true);

获取界面控件的值代码如下：


    $("input[name='SplitType']:checked").val()

或者使用Comobo控件作为单项选择的控件也是可以的，界面效果如下所示。

![](https://images0.cnblogs.com/blog/8867/201309/18150941-fcdea5f7b40d436a93b0d1485437efcf.png)

其界面代码如下所示：


        <select id="cc" style="width:150px"></select>

             Select a language
            <input type="radio" name="lang" value="01"> Java
            <input type="radio" name="lang" value="02"> C#
            <input type="radio" name="lang" value="03"> Ruby
            <input type="radio" name="lang" value="04"> Basic
            <input type="radio" name="lang" value="05"> Fortran


            $(function(){
                $('#cc').combo({
                    required:true,
                    editable:false
                });
                $('#sp').appendTo($('#cc').combo('panel'));
                $('#sp input').click(function(){
                    var v = $(this).val();
                    var s = $(this).next('span').text();
                    $('#cc').combo('setValue', v).combo('setText', s).combo('hidePanel');
                });
            });


### 8、复选框

复选框是在一项或多项内容中，选择零项或者多项的一个输入界面控件。

![](https://images0.cnblogs.com/blog/8867/201309/22161826-3d0a0f4e910b40b286d1455ef2650a64.png)

界面代码如下所示：


    <input id="chkIsExpire" type="checkbox" >帐号过期

由于复选框的一些特殊性质，在表单提交的时候，如果没有勾选的选型，使用serializeArray()方法构造的数据，复选框的值则不会被提交。

基于这个原因，我们可以使用Select控件进行替代，实现复选项的功能，而不影响


    var postData = $("#ffEdit").serializeArray();

以上代码的使用。

![](https://images0.cnblogs.com/blog/8867/201309/22162010-b6f901dcd14a49a4ba379dd01d698ec6.png)

使用Select控件的代码如下所示。


    <select  id="Visible1" name="Visible">
              <option value="true" selected>正常</option>
              <option value="false">不可见</option>
     </select>

赋值给界面控件代码如下：


    $("#Visible1").prop('checked', info.Visible);

获取界面控件的值代码如下：


    var visible = $("#txtVisible").val();

### 9、表格控件DataGrid

easyui的列表控件，可以通过指定table的class属性为easyui-datagrid即可实现表格的定义，界面代码如下所示：


    <table class="easyui-datagrid" title="Basic DataGrid" style="width:700px;height:250px"
                data-options="singleSelect:true,collapsible:true,url:'../datagrid/datagrid_data1.json'">
            <thead>
                <tr>
                    <th data-options="field:'itemid',width:80">Item ID</th>
                    <th data-options="field:'productid',width:100">Product</th>
                    <th data-options="field:'listprice',width:80,align:'right'">List Price</th>
                    <th data-options="field:'unitcost',width:80,align:'right'">Unit Cost</th>
                    <th data-options="field:'attr1',width:250">Attribute</th>
                    <th data-options="field:'status',width:60,align:'center'">Status</th>
                </tr>
            </thead>
        </table>

不过为了避免使用脚本定义datagrid导致多次初始化的问题，我们一般只需要指定一个table代码即可，界面如下所示



                <table id="grid" style="width: 1024px" title="用户操作" iconcls="icon-view">
                </table>

而表格控件的数据加载，我们使用javascript进行初始化，初始化后的表格界面显示效果如下所示。

![](https://images0.cnblogs.com/blog/8867/201309/22162745-bb551bedf44a40ceb9f5810a8cf5b4ce.png)

Javascript代码如下所示，其中的width: function () { return document.body.clientWidth * 0.9 }是用来实现宽度自适应的一个操作。


            //实现对DataGird控件的绑定操作
            function InitGrid(queryData) {
                $('#grid').datagrid({   //定位到Table标签，Table标签的ID是grid
                    url: '/Menu/FindWithPager',   //指向后台的Action来获取当前菜单的信息的Json格式的数据
                    title: '功能菜单',
                    iconCls: 'icon-view',
                    height: 650,
                    width: function () { return document.body.clientWidth * 0.9 },
                    nowrap: true,
                    autoRowHeight: false,
                    striped: true,
                    collapsible: true,
                    pagination: true,
                    pageSize: 100,
                    pageList: [50,100,200],
                    rownumbers: true,
                    //sortName: 'ID',    //根据某个字段给easyUI排序
                    sortOrder: 'asc',
                    remoteSort: false,
                    idField: 'ID',
                    queryParams: queryData,  //异步查询的参数
                    columns: [[
                        { field: 'ck', checkbox: true },   //选择
                         { title: '显示名称', field: 'Name', width: 200},
                         { title: '图标', field: 'Icon', width: 150 },
                         { title: '排序', field: 'Seq', width: 80 },
                         { title: '功能ID', field: 'FunctionId', width: 80 },
                         { title: '菜单可见', field: 'Visible', width: 80 },
                         { title: 'Winform窗体类型', field: 'WinformType', width: 400 },
                         { title: 'Web界面Url地址', field: 'Url', width: 200 },
                         { title: 'Web界面的菜单图标', field: 'WebIcon', width: 120 },
                         { title: '系统编号', field: 'SystemType_ID', width: 80 }
                    ]],
                    toolbar: [{
                        id: 'btnAdd',
                        text: '添加',
                        iconCls: 'icon-add',
                        handler: function () {
                            ShowAddDialog();//实现添加记录的页面
                        }
                    }, '-', {
                        id: 'btnEdit',
                        text: '修改',
                        iconCls: 'icon-edit',
                        handler: function () {
                            ShowEditOrViewDialog();//实现修改记录的方法
                        }
                    }, '-', {
                        id: 'btnDelete',
                        text: '删除',
                        iconCls: 'icon-remove',
                        handler: function () {
                            Delete();//实现直接删除数据的方法
                        }
                    }, '-', {
                        id: 'btnView',
                        text: '查看',
                        iconCls: 'icon-table',
                        handler: function () {
                            ShowEditOrViewDialog("view");//实现查看记录详细信息的方法
                        }
                    }, '-', {
                        id: 'btnReload',
                        text: '刷新',
                        iconCls: 'icon-reload',
                        handler: function () {
                            //实现刷新栏目中的数据
                            $("#grid").datagrid("reload");
                        }
                    }],
                    onDblClickRow: function (rowIndex, rowData) {
                        $('#grid').datagrid('uncheckAll');
                        $('#grid').datagrid('checkRow', rowIndex);
                        ShowEditOrViewDialog();
                    }
                })
            };

对于查询按钮触发的数据后台查询及数据绑定操作，javascript代码如下所示：


            //绑定查询按钮的的点击事件
            function BindSearchEvent() {
                //按条件进行查询数据，首先我们得到数据的值
                $("#btnSearch").click(function () {
                    //得到用户输入的参数，取值有几种方式：$("#id").combobox('getValue'), $("#id").datebox('getValue'), $("#id").val()
                    //字段增加WHC_前缀字符，避免传递如URL这样的Request关键字冲突
                    var queryData = {
                        WHC_ID: $("#txtID").val(),
                        WHC_Name: $("#txtName").val(),
                        WHC_Icon: $("#txtIcon").val(),
                        WHC_Seq: $("#txtSeq").val(),
                        WHC_FunctionId: $("#txtFunctionId").val(),
                        WHC_Visible: $("#txtVisible").val(),
                        WHC_WinformType: $("#txtWinformType").val(),
                        WHC_Url: $("#txtUrl").val(),
                        WHC_WebIcon: $("#txtWebIcon").val(),
                        WHC_SystemType_ID: $("#txtSystemType_ID").val()
                    }
                    //将值传递给
                    InitGrid(queryData);
                    return false;
                });
            }

通过构造一些查询参数并传递相应的值，后台根据这些参数，从对应控制器的分页方法 **FindWithPager** 获取相应的分页数据，并绑定到grid控件中。

**另外，如果需要在grid里面增加一些图片或者链接什么的，应该如何操作呢？**

如下界面所示的效果：

![](https://images0.cnblogs.com/blog/8867/201309/23102342-e51fe469baa44e00bafa66d86a863614.png)

首先需要在初始化代码里面增加列的formatter回调函数，如下所示。


                    columns: [[
                        { field: 'ck', checkbox: true },   //选择
                         { title: '显示名称', field: 'Name', width: 200},
                         { title: '图标', field: 'Icon', width: 150 },
                         { title: '排序', field: 'Seq', width: 80 },
                         { title: '功能ID', field: 'FunctionId', width: 80 },
                         {
                             title: '菜单可见', field: 'Visible', width: 80, **formatter** : function (val, rowdata, index) {
                                 if (val) {
                                     return '<a class="grid_visible" href="javascript:void(0)" >' + val + '</a>';
                                 } else {
                                     return '<a class="grid_unvisible" href="javascript:void(0)" >' + val + '</a>';
                                 }
                             }
                         },
                         { title: 'Winform窗体类型', field: 'WinformType', width: 400 },
                         { title: 'Web界面Url地址', field: 'Url', width: 200 },
                         { title: 'Web界面的菜单图标', field: 'WebIcon', width: 120 },
                         { title: '系统编号', field: 'SystemType_ID', width: 80 }
                    ]],

在formatter回调函数里面添加逻辑代码，判断是否可见，其实就是增加两个图片按钮，但是图片按钮的样式设置，必须在加载数据完毕后才能操作，因此需要在函数里面处理。


                    onLoadSuccess: function () {
                        $(".grid_visible").linkbutton({ text: '可见', plain: true, iconCls: 'icon-ok' });
                        $(".grid_unvisible").linkbutton({ text: '不可见', plain: true, iconCls: 'icon-stop' });
                    },

如果显示的图片不完整，设置行的自动调整高度属性为true即可。

**autoRowHeight: true**

### 10、树形控件

虽然easyui也有Tree控件，不过我较喜欢使用zTree这个树形控件，这个是一个免费的Jquery树控件。

![](https://images0.cnblogs.com/blog/8867/201309/22163041-1f9ff9ff2d7e40818d0e3cdbc1e67d97.png)

引用代码如下所示：


        <link href="~/Content/JQueryTools/JQueryTree/css/zTreeStyle/zTreeStyle.css" rel="stylesheet" type="text/css" />


初始化在Tree树控件的界面代码如下所示：



         <!--
            var setting = {
                data: {
                    simpleData: {
                        enable: true
                    }
                },
                callback: {
                    onClick: onClick,
                    onDblClick: onDblClick
                }
            }

            //重新加载树形结构（异步）
            function reloadTree() {
                $("#loading").show();

                $.getJSON("/DictType/GetTreeJson?r=" + Math.random(), function (json) {
                    $.fn.zTree.init($("#treeDemo"), setting, json);
                    $.fn.zTree.getZTreeObj("treeDemo").expandAll(true);

                    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                    var treeNodes = treeObj.getNodes();
                    if (treeNodes != null) {
                        loadTypeData(treeNodes[0].id);
                    }
                });
                $("#loading").fadeOut(500);
            }

            //树单击节点操作
            function onClick(event, treeId, treeNode, clickFlag) {
                var id = treeNode.id;
                loadTypeData(id);
            }
            //树双击节点操作
            function onDblClick(event, treeId, treeNode) {
                var id = treeNode.id;
                loadTypeData(id);
                ShowDictType('edit');
            }

### 11、布局控件

EasyUI通过DIV层来控制布局的显示，DIV里面增加一个Region的属性用来区分属于哪个区域，如下图是我Web开发框架的界面布局效果图。

![](https://images0.cnblogs.com/blog/8867/201309/22164311-9f0f0c57b81441cd9bc34e4763031d91.png)

界面代码如下所示：

![](https://images0.cnblogs.com/blog/8867/201309/22164357-f370041737594c1e9dce471a2b53eeb8.png)

我们详细查看主工作区的代码，如下所示。


        <!--主工作区-->





其中字典管理里面还有子布局的展示，我们查看字典管理里面界面代码，如下所示。





                    .......................

                    <ul id="treeDemo" class="ztree">
                    </ul>



                <!-------------------------------详细信息展示表格----------------------------------->
                <table id="grid" style="width: 940px" title="用户操作" iconcls="icon-view"></table>



### 12、弹出式对话框

EasyUI弹出式对话框用的很多，对话框的界面代码放在DIV层里面，一般在界面整个界面加载后中已经初始化了，只是我们根据条件相似适当的层即可，这样就形成了弹出式对话框，弹出式对话框有一个遮罩的效果。

![](https://images0.cnblogs.com/blog/8867/201309/22165231-2cca658e91e143159d94e14d3bc850d9.png)

界面代码如下所示：

![](https://images0.cnblogs.com/blog/8867/201309/22165501-982742dbe6dc4eba95420938f5d6267b.png)

### 13、提示信息

在常规的Web界面提示里面，我们一般用纯粹的javascript的alert函数来进行信息的提示，如果在基于EasyUI的界面布局和演示里面，使用这个提示显然会和界面演示不够匹配，因此我们使用messager类来进行相应的提示信息处理，简单的脚本提示代码如下。


    $.messager.alert("提示", "修改成功");

![](https://images0.cnblogs.com/blog/8867/201309/22170108-321c27d9d62d4870bee10a8741272490.png)

提示信息也可以更加丰富，添加图标等信息，界面代码如下所示。



            function alert1(){
                $.messager.alert('My Title','Here is a message!');
            }
            function alert2(){
                $.messager.alert('My Title','Here is a error message!','error');
            }
            function alert3(){
                $.messager.alert('My Title','Here is a info message!','info');
            }
            function alert4(){
                $.messager.alert('My Title','Here is a question message!','question');
            }
            function alert5(){
                $.messager.alert('My Title','Here is a warning message!','warning');
            }


对于一般的删除操作，一般有一个提示确认的消息框，这个messager类也进行了封装处理，效果也不错。

![](https://images0.cnblogs.com/blog/8867/201309/22170710-24e3b1ef797c4e2d9ffd9ebae26182b2.png)

界面代码如下所示。


                    $.messager.confirm("删除确认", "您确认删除选定的记录吗？", function (deleteAction) {
                        if (deleteAction) {
                            $.get("/DictData/DeletebyIds", postData, function (data) {
                                if (data == "true") {
                                    $.messager.alert("提示", "删除选定的记录成功");
                                    $("#grid").datagrid("reload");

                                    //当删除完成之后，第二次删除的时候还记得上次的信息，这样是不可以的，所以我们需要清除第一次的信息
                                    rows.length = "";//第一种方法
                                    $("#grid").datagrid("clearSelections");//第二种方法
                                }
                                else {
                                    $.messager.alert("提示", data);
                                }
                            });
                        }
                    });

以上就是我Web开发框架里面常用到的一些界面控件展示以及相关的代码介绍，有一些不太常用的控件可能还没有在本文中介绍，欢迎大家进行补充和讨论，以后有时间继续完善这个文章，作为基于MVC+EasyUI的框架界面的一个很好的参考。希望大家喜欢，多多提意见。

### 基于MVC4+EasyUI的Web开发框架的系列文章：

[基于MVC4+EasyUI的Web开发框架形成之旅--总体介绍](http://www.cnblogs.com/wuhuacong/p/3281103.html)

[](http://www.cnblogs.com/wuhuacong/p/3281103.html)[基于MVC4+EasyUI的Web开发框架形成之旅--MVC控制器的设计](http://www.cnblogs.com/wuhuacong/p/3284628.html)

[基于MVC4+EasyUI的Web开发框架形成之旅--界面控件的使用](http://www.cnblogs.com/wuhuacong/p/3317223.html)

[基于MVC4+EasyUI的Web开发框架形成之旅--附件上传组件uploadify的使用](http://www.cnblogs.com/wuhuacong/p/3343967.html)

[基于MVC4+EasyUI的Web开发框架形成之旅--框架总体界面介绍](http://www.cnblogs.com/wuhuacong/p/3344096.html)

[基于MVC4+EasyUI的Web开发框架形成之旅--基类控制器CRUD的操作](http://www.cnblogs.com/wuhuacong/p/3352016.html)

[基于MVC4+EasyUI的Web开发框架形成之旅--权限控制](http://www.cnblogs.com/wuhuacong/p/3361351.html)

[基于MVC4+EasyUI的Web开发框架经验总结（1）-利用jQuery Tags Input 插件显示选择记录](http://www.cnblogs.com/wuhuacong/p/3667703.html)

[基于MVC4+EasyUI的Web开发框架经验总结（2）- 使用EasyUI的树控件构建Web界面](http://www.cnblogs.com/wuhuacong/p/3669575.html)

[基于MVC4+EasyUI的Web开发框架经验总结（3）- 使用Json实体类构建菜单数据](http://www.cnblogs.com/wuhuacong/p/3669708.html)

[基于MVC4+EasyUI的Web开发框架经验总结（4）--使用图表控件Highcharts](http://www.cnblogs.com/wuhuacong/p/3736564.html)

[基于MVC4+EasyUI的Web开发框架经验总结（5）--使用HTML编辑控件CKEditor和CKFinder](http://www.cnblogs.com/wuhuacong/p/3780356.html)

[基于MVC4+EasyUI的Web开发框架经验总结（6）--在页面中应用下拉列表的处理](http://www.cnblogs.com/wuhuacong/p/3840321.html)

[基于MVC4+EasyUI的Web开发框架经验总结（7）--实现省份、城市、行政区三者联动](http://www.cnblogs.com/wuhuacong/p/3841338.html)

[基于MVC4+EasyUI的Web开发框架经验总结（8）--实现Office文档的预览](http://www.cnblogs.com/wuhuacong/p/3871991.html)

[基于MVC4+EasyUI的Web开发框架经验总结（9）--在Datagrid里面实现外键字段的转义操作](http://www.cnblogs.com/wuhuacong/p/3872890.html)

[基于MVC4+EasyUI的Web开发框架经验总结（10）--在Web界面上实现数据的导入和导出](http://www.cnblogs.com/wuhuacong/p/3873498.html)

[基于MVC4+EasyUI的Web开发框架经验总结（11）--使用Bundles处理简化页面代码](http://www.cnblogs.com/wuhuacong/p/4073203.html)

[基于MVC4+EasyUI的Web开发框架经验总结（12）--利用Jquery处理数据交互的几种方式](http://www.cnblogs.com/wuhuacong/p/4085682.html)

[基于MVC4+EasyUI的Web开发框架经验总结（13）--DataGrid控件实现自动适应宽带高度](http://www.cnblogs.com/wuhuacong/p/4085725.html)

[基于MVC4+EasyUI的Web开发框架经验总结（14）--自动生成图标样式文件和图标的选择操作](http://www.cnblogs.com/wuhuacong/p/4093778.html)
