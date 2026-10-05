---
source: "http://blog.csdn.net/chaoyangzhixue/article/details/50686771"
title: "简单的EasyUI登录界面_easyui登录界面模板-CSDN博客"
fetched_at: "2026-10-05 15:31:02"
---

使用easyui自带的样式等，做的一个简单的登录界面，效果如下：
![这里写图片描述](https://img-blog.csdn.net/20160218160031826)


    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width" />
        <title>用户登录</title>


        <link href="~/Plugins/easyui-1.4.4/themes/gray/easyui.css" rel="stylesheet" />
        <link href="~/Plugins/easyui-1.4.4/themes/icon.css" rel="stylesheet" />

            document.onkeydown = function (e) {
                var event = e || window.event;
                var code = event.keyCode || event.which || event.charCode;
                if (code == 13) {
                    login();
                }
            }
            $(function () {
                $("input[name='login']").focus();
            });
            function cleardata() {
                $('#loginForm').form('clear');
            }
            function login() {
                if ($("input[name='login']").val() == "" || $("input[name='password']").val() == "") {
                    $("#showMsg").html("用户名或密码为空，请输入");
                    $("input[name='login']").focus();
                } else {
                    //ajax异步提交
                    $.ajax({
                        type: "POST",   //post提交方式默认是get
                        url: "login.action",
                        data: $("#loginForm").serialize(),   //序列化
                        error: function (request) {      // 设置表单提交出错
                            $("#showMsg").html(request);  //登录错误提示信息
                        },
                        success: function (data) {
                            document.location = "index.action";
                        }
                    });
                }
            }

    </head>
    <body>



                    <form id="loginForm" method="post">

                            <label for="login">帐号:</label>
                            <input type="text" name="login" style="width:260px;" />


                            <label for="password">密码:</label>
                            <input type="password" name="password" style="width:260px;" />


                    </form>


                    <a class="easyui-linkbutton" iconcls="icon-ok" href="javascript:void(0)" onclick="login()">登录</a>



    </body>
    </html>
