---
source: "http://www.cnblogs.com/qyhblog/p/6086877.html"
title: "基于easyui 写的后台管理系统（用户角色，角色功能）的实现 - 你猜呀㊣ - 博客园"
fetched_at: "2026-10-05 15:31:29"
---

学了后台管理系统后，自己尝试写了个一些零碎的功能块，以便加强自己对Easyui的理解和具体运用。

那后台管理信息系统里最重要的一块应该是用户与角色，角色与功能，之间的关系了，整理了下这两个模块的代码发上来。

1.用户角色模块是用了两个表格来实现，可以对不同用户所对应的角色进行简单的编辑删除和增加。

++++++++++++++++++++++++++++++++++++++++

页面就是用了easyui组件，比如表格的样式还有分页条等内容，组件里一些属性和方法也可以更加方便的实现功能的实现。具体可参照easyui的API。后台传过来的值也只需跟表格字段里的键值一一对应就可以了，代码中对于增加用户、删除用户等方法的实现用的是ajax方法。


    <html>
      <head>
        <base href="<%=basePath%>">

        <title>用户角色设置</title>

        <meta http-equiv="pragma" content="no-cache">
        <meta http-equiv="cache-control" content="no-cache">
        <meta http-equiv="expires" content="0">
        <meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
        <meta http-equiv="description" content="This is my page">

        <link rel="stylesheet" type="text/css" href="Common/jquery-easyui-1.5/themes/icon.css">
        <link rel="stylesheet" type="text/css" href="Common/jquery-easyui-1.5/themes/default/easyui.css">




      </head>


        <body class="easyui-layout">

              <a href="Web/Jsp/Main2.jsp">转到角色功能</a>



           <table id="dg2" class="easyui-datagrid" title="用户信息" style="width:700px;height:336px"
      data-options="url:'servlet/roleServlet',fitColumns:true,pagination:true,pageList:[10]">

            <thead>
                <tr>
                    <th data-options="field:'RoleId',checkbox:'true',width:40"></th>
                    <th data-options="field:'Title',width:60">角色名称</th>
                    <th data-options="field:'Memo',width:120">说明</th>
                </tr>
            </thead>
            </table>

                <a href="javascript:void(0);" class="easyui-linkbutton" iconCls="icon-save" plain="true" onclick="save()">保存设置</a>



          <table id="dg1" class="easyui-datagrid" title="用户信息" style="width:700px;height:336px"
              data-options="url:'servlet/userServlet',fitColumns:true,singleSelect:true,pagination:true,pageList:[10]">

            <thead>
                <tr>
                    <th data-options="field:'UserId',width:40"> </th>
                    <th data-options="field:'UserName',width:60">用户名</th>
                    <th data-options="field:'UserPwd',width:120">用户密码</th>
                    <th data-options="field:'Name',width:60,align:'right'">姓名</th>
                    <th data-options="field:'Phone',width:300,">用户联系电话</th>
                    <th data-options="field:'Memo',width:80,align:'right'">备注</th>
                    <th data-options="field:'_operate',width:120,align:'center',formatter:formatOper">操作</th>
                </tr>
            </thead>
        </table>

        <a href="javascript:void(0);" class="easyui-linkbutton" iconCls="icon-add" plain="true" onclick="add()">增加用户</a>


        <!-- ++++++++++++++++++++弹出的增加用户框++++++++++++++++++++++++++++++++++++++++ -->


             <table>
                <tr><td>用户名:<td><input name="UserName" type="text" id="username"></td></td></tr>
                <tr><td>用户密码：<td><input name="UserPwd" type="text" id="userpwd"></td></td></tr>
                <tr><td>姓名：<td><input name="Name" type="text" id="name"></td></td></tr>
                <tr><td>用户联系电话：<td><input name="Phone" type="text" id="phone"></td></td></tr>
                <tr><td>备注：<td><input name="Memo" type="text" id="memo"></td></td></tr>
                </table>


      </body>


        function formatOper(value,row,index){

                  return '<a href="javascript:void(0);" onclick="bianjiUser('+index+')">编辑</a> <a href="javascript:void(0);" onclick="shanchuUser('+index+')">删除</a>';
            };
        //++++++++++增加用户按钮++++++++
        $("#dg1").datagrid({
            toolbar:'#tb1'
        });
        //+++++增加用户+++++
           function add(){
             $('#add').dialog('open').dialog({
                    title:增加用户,
                    modal: true
             });
           };

           function queding(){

             var message={
                            "username":$("#username").val(),
                            "userpwd":$("#userpwd").val(),
                            "name":$("#name").val(),
                            "phone":$("#phone").val(),
                            "memo":$("#memo").val(),
                        };
                 if($("#username").val()!=""&&$("#userpwd").val()!=""&&$("#name").val()!=""&&$("#phone").val()!=""&&$("#memo").val()!="")
                  {
                      $.ajax({
                          type:"post",
                          url:"servlet/adduserServlet",
                          data:{"Message":JSON.stringify(message)},
                          success:function(){
                             $('#dg1').datagrid('reload');
                             alert("添加成功！");
                            $("#username").val("");
                            $("#userpwd").val("");
                            $("#name").val("");
                            $("#phone").val("");
                            $("#memo").val("");
                          }
                        })

                    }
                    else{alert("请填写完整！");
                           $("#username").val("");
                            $("#userpwd").val("");
                            $("#name").val("");
                            $("#phone").val("");
                            $("#memo").val("");
                        }

           }
         //++++++++++用户编辑+++++++++++++
           function  bianjiUser(index){

                 alert(index);
            }

         //++++++++++++用户删除++++++++++++++++
            function shanchuUser(index){
               $.ajax({
                   type:"post",
                   url:"servlet/shanchuServlet",
                   data:{"index":index},
                   success:function(){
                      $("#dg1").datagrid('reload');
                   }
               });

            }
        //++++++++保存设置按钮+++++++++
        $("#dg2").datagrid({
            toolbar:'#tb2'
         });
         //=====保存设置=====
          function save(){
             var userow=$('#dg1').datagrid("getSelected");
             var rows1=$('#dg2').datagrid("getChecked");
             $.ajax({                           //先删除用户所对应的角色
                 type:"post",
                 url:"servlet/deleteServlet",
                 data:{"userid":userow.UserId},
             });

                $.ajax({                        //再将勾选的角色保存
                      type:"post",
                      url:"servlet/saveServlet",
                      data:{"rows":JSON.stringify(rows1),"userid":userow.UserId}
                })


           };

             $("#dg1").datagrid({
                    //================点击用户选中角色============
                  onClickRow:function(Index,rowData){
                  var rows = $('#dg2').datagrid("getRows");
                  $("#dg2").datagrid('uncheckAll');
                      $.ajax({
                           type:"post",
                           url:"servlet/ru2Servlet",
                           data:{"Userid":rowData.UserId},
                           success:function(array1){
                              for(var i=0;i<array1.length;i++){
                                  for(var j=0;j<rows.length;j++){
                                   if(array1[i]==rows[j].RoleId){
                                        $("#dg2").datagrid('checkRow',j);
                                   }
                                }
                              }
                           }
                      });
                   }
             });


           $("#dg2").datagrid({
           //============勾选角色保存设置=====
                onCheck:function(Index,rowData){
                   $.ajax({
                         type:"post",
                         url:"servlet/ru1Servlet",
                         data:{"roleid":rowData.RoleId},
                         dataType:"json",

                   });

                }
           });
         //  var rows = $('#dg2').datagrid('getSelected');
         //   alert(rows.Title);




    </html>

2.角色与功能模块的用的是一个表格和树状图。

树状图对于表格的不同最大的就是数据库表格上的一些处理，另外的也无很大差异，值得注意的是每行的索引，行等easyui属性的理解。

因为是新手，代码也仅供参考，如果前辈们有什么好的建议，希望大家能给予我一些指点。谢谢大家！
