---
source: "http://www.cnblogs.com/ToFlying/p/3511605.html"
title: "关于easyui-accordion的添加以及显示隐藏菜单的使用 - Follow-your-heart - 博客园"
fetched_at: "2026-10-05 15:31:28"
---

       $(function()
       {
             leftMenus();
       });

       function leftMenus()
       {
           var _menus=<%=jsonStr %>;
             //$(".easyui-accordion").empty();
             $.each(_menus.menus, function(i, n) {
                  $(".easyui-accordion").accordion('add',
                    {
                       title: n.text,
                       content:moduleIndex(n.menus)
                 });
            });
            $(".easyui-accordion").accordion();
                    $('.easyui-accordion li a').click(function()
                    {
                        var tabTitle = $(this).text();
                        var url = $(this).attr("href");
                        //alert(url);
                        addTab(tabTitle,url);
                        $('.easyui-accordion li div').removeClass("selected");
                        $(this).parent().addClass("selected");
                   }).hover(function()
                   {
                        $(this).parent().addClass("hover");
                   },function()
                   {
                        $(this).parent().removeClass("hover");
                   });
       }

       function addTab(subtitle,url){
        if(!$('#tabs').tabs('exists',subtitle)){
            $('#tabs').tabs('add',{
                title:subtitle,
                content:createFrame(url),
                closable:true,
                width:$('#mainPanle').width()-10,
                height:$('#mainPanle').height()-26
            });
        }else{
            $('#tabs').tabs('select',subtitle);
        }
        //tabClose();
    }

        function createFrame(url)
        {
            var s = '  ';
            return s;
        }

       function moduleIndex(menusData)
       {
          var text="";
          text += '<ul>';
          $.each(menusData,function(j,o)
          {
              text += '<li> <a target="mainFrame" href="'+o.attributes+'" >' + o.text + '</a> </li> ';
          });
          text += '</ul>';
          return text;
       }



    <body id="cc" class="easyui-layout">









                <h1>欢迎您使用，报表在线查询系统</h1>




    </body>

展示效果图片：
