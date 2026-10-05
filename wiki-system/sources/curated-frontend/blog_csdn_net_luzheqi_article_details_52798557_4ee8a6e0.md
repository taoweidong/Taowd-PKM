---
source: "http://blog.csdn.net/luzheqi/article/details/52798557"
title: "NexT主题集成Algolia搜索插件_algolia search这个是收费的嘛-CSDN博客"
fetched_at: "2026-10-05 15:32:14"
---

> 欢迎移步到我的[个人博客](http://blog.jerkybible.com)
>
> 版权声明：本文为[博主](http://blog.jerkybible.com)原创文章，[转载请注明出处](http://blog.jerkybible.com)，谢谢!
>
> 很长时间不整理是很容易忘记的

### 为什么要增加Algolia搜索插件

第一个原因当然是这样可以让博客显得更加炫酷；其次就是原来常用的swiftype插件不再免费，而且Algolia不仅免费，感觉上要比Swiftype要快。

### 就没有别人有写相关博客吗

你可能会有这样的疑问。我的回答是当然有，例如[Hexo集成Algolia搜索插件](http://www.kuwoku.com/2016/05/30/Hexo%E9%9B%86%E6%88%90Algolia%E6%90%9C%E7%B4%A2%E6%8F%92%E4%BB%B6)，但是可能是[NexT主题](http://theme-next.iissnan.com)版本造成的不同，不能完全照搬。

当然，我也会写一些重复的东西，这样也不用再到别人的的博客上去翻了，万一他们博客登不上去了呢。

### 准备工作

  1. 确定你的NexT版本号，查看的方式是在NexT主题文件夹下的`_config.yml`文件中的最末端，我的是`5.0.1`。见下图。
![](https://i-blog.csdnimg.cn/blog_migrate/68f5ba19885b6c2fed0617075fb39dfe.png)
  2. 到[Algolia官网](https://www.algolia.com/)，注册一个账号，当然你可以用[Github账号](https://github.com)，重新注册的话163这种邮箱是不能用的。
![](https://i-blog.csdnimg.cn/blog_migrate/61c4ecf4420947502637ccad4a9bb925.png)
  3. 新建一个新的Index，当然用已有的也可以，再在新的Index上进行基础设置。
![](https://i-blog.csdnimg.cn/blog_migrate/fc0488e8abf96aa084d7ee3c3a22eb05.png)
![](https://i-blog.csdnimg.cn/blog_migrate/f588329630f8c6c3a6398ee16983a199.png)
  4. 打开API Keys页面，里面的信息一会儿要用到。
![](https://i-blog.csdnimg.cn/blog_migrate/91cec9b12a0cc364f3e2f92c38f0377b.png)

### 上传数据到Algolia

  1. 在Hexo工程根目录下执行下面的语句。



    npm install hexo-algolia --save

  1. 在Hexo工程根目录的_config.yml中加入如下配置，注意改成前面API Keys页面相应配置。



    algolia:
      applicationID: 'your applicationID'
      apiKey: 'your apiKey'
      adminApiKey: 'your adminApiKey'
      indexName: 'your indexName'
      chunkSize: 5000

  1. 执行下面语句，必要时先进行`hexo clean`，确保最后得到提交成功提示。



    hexo algolia

### 修改NexT主题集成Algolia

  1. 在NexT主题文件夹下（这一部分不特殊指明都在这个文件夹中操作）找到`_config.yml`，增加aloglia配置项，如下。



    algolia: true

  1. 打开`layout/_partials/head.swig`，找到下面的语句。




      ...
      var CONFIG = {
        ...
        }
      };



  1. 在`CONFIG`中增加下面的语句，相应的配置改为与API Keys页面相一致。



        root: '/',
        algolia: {
              applicationID: 'your applicationID',
              apiKey: 'your apiKey',
              indexName: ''your indexName',
              hits: {"per_page":10},
              labels: {"input_placeholder":"搜索...","hits_empty":"未发现与 「${query}」相关的内容","hits_stats":"${hits} 条相关条目，使用了 ${time} 毫秒"}
            }

  1. 打开`layout/_partials/header.swig`，找到相应代码并做以下修改。



        ...
        <!-- {% set hasSearch = theme.swiftype_key || theme.tinysou_Key || config.search %} -->
        <!-- 改为 -->
        {% set hasSearch = theme.swiftype_key || theme.tinysou_Key || config.search || theme.algolia %}
        ...
        {% if theme.menu %}
        <ul id="menu" class="menu">
            ...
            {% if hasSearch %}
                <li class="menu-item menu-item-search">
                  {% if theme.swiftype_key %}
                    <a href="javascript:;" class="st-search-show-outputs">
                  {% elseif config.search %}
                    <a href="javascript:;" class="popup-trigger">
                  <!-- 增加下面语句 -->
                  {% elseif theme.algolia %}
                    <a href="javascript:;" class="popup-trigger">
                  <!-- 增加结束 -->
                  {% endif %}
                    {% if theme.menu_icons.enable %}
                      <i class="menu-item-icon fa fa-search fa-fw"></i>
                    {% endif %}
                    {{ __('menu.search') }}
                  </a>
                </li>
            {% endif %}
        </ul>
        {% endif %}
        ...

  1. 在`layout/_partials/search`文件夹下新增`algolia.swig`文件，内容如下。






            <i class="fa fa-search"></i>









          <i class="fa fa-times-circle"></i>



  1. 打开`layout/_partials/search.swig`，做以下修改。



        {% if theme.swiftype_key %}
          {% include 'search/swiftype.swig' %}
        {% elseif theme.tinysou_Key %}
          {% include 'search/tinysou.swig' %}
        {% elseif config.search.path %}
          {% include 'search/localsearch.swig' %}
        <!-- 增加下面语句 -->
        {% elseif theme.algolia %}
          {% include 'search/algolia.swig' %}
        <!-- 增加结束 -->
    {% endif %}

  1. 在`source/js/src`下面新增文件`algolia.js`，内容如下。



    $(document).ready(function () {
      var algoliaSettings = CONFIG.algolia;
      var isAlgoliaSettingsValid = algoliaSettings.applicationID &&
        algoliaSettings.apiKey &&
        algoliaSettings.indexName;
      if (!isAlgoliaSettingsValid) {
        window.console.error('Algolia Settings are invalid.');
        return;
      }
      var search = instantsearch({
        appId: algoliaSettings.applicationID,
        apiKey: algoliaSettings.apiKey,
        indexName: algoliaSettings.indexName,
        searchFunction: function (helper) {
          var searchInput = $('#algolia-search-input').find('input');

          if (searchInput.val()) {
            helper.search();
          }
        }
      });

      // Registering Widgets
      [
        instantsearch.widgets.searchBox({
          container: '#algolia-search-input',
          placeholder: algoliaSettings.labels.input_placeholder
        }),

        instantsearch.widgets.hits({
          container: '#algolia-hits',
          hitsPerPage: algoliaSettings.hits.per_page || 10,
          templates: {
            item: function (data) {
              return (
                '<a href="' + CONFIG.root + data.path + '" class="algolia-hit-item-link">' +
                  data._highlightResult.title.value +
                '</a>'
              );
            },
            empty: function (data) {
              return (
                ' ' +
                  algoliaSettings.labels.hits_empty.replace(/\$\{query}/, data.query) +
                ' '
              );
            }
          },
          cssClasses: {
            item: 'algolia-hit-item'
          }
        }),

        instantsearch.widgets.stats({
          container: '#algolia-stats',
          templates: {
            body: function (data) {
              var stats = algoliaSettings.labels.hits_stats
                            .replace(/\$\{hits}/, data.nbHits)
                            .replace(/\$\{time}/, data.processingTimeMS);
              return (
                stats +
                ' ' +
                '  <img src="' + CONFIG.root + 'images/algolia_logo.svg" alt="Algolia" />' +
                ' ' +
                '<hr />'
              );
            }
          }
        }),

        instantsearch.widgets.pagination({
          container: '#algolia-pagination',
          scrollTo: false,
          showFirstLast: false,
          labels: {
            first: '<i class="fa fa-angle-double-left"></i>',
            last: '<i class="fa fa-angle-double-right"></i>',
            previous: '<i class="fa fa-angle-left"></i>',
            next: '<i class="fa fa-angle-right"></i>'
          },
          cssClasses: {
            root: 'pagination',
            item: 'pagination-item',
            link: 'page-number',
            active: 'current',
            disabled: 'disabled-item'
          }
        })
      ].forEach(search.addWidget, search);
      search.start();
      $('.popup-trigger').on('click', function(e) {
        e.stopPropagation();
        $('body').append(' ').css('overflow', 'hidden');
        $('.popup').toggle();
        $('#algolia-search-input').find('input').focus();
      });
      $('.popup-btn-close').click(function(){
        $('.popup').hide();
        $('.popoverlay').remove();
        $('body').css('overflow', '');
      });
    });
      $(document).ready(function () {
        if ( $('#local-search-input').size() === 0) {
          return;
        }
        // Popup Window;
        var isfetched = false;
        // Search DB path;
        var search_path = "search.xml";
        if (search_path.length == 0) {
          search_path = "search.xml";
        }
        var path = "/" + search_path;
        // monitor main search box;
        function proceedsearch() {
          $("body").append(' ').css('overflow', 'hidden');
          $('.popup').toggle();
        }
        // search function;
        var searchFunc = function(path, search_id, content_id) {
          'use strict';
          $.ajax({
            url: path,
            dataType: "xml",
            async: true,
            success: function( xmlResponse ) {
              // get the contents from search data
              isfetched = true;
              $('.popup').detach().appendTo('.header-inner');
              var datas = $( "entry", xmlResponse ).map(function() {
                return {
                  title: $( "title", this ).text(),
                  content: $("content",this).text(),
                  url: $( "url" , this).text()
                };
              }).get();
              var $input = document.getElementById(search_id);
              var $resultContent = document.getElementById(content_id);
              $input.addEventListener('input', function(){
                var matchcounts = 0;
                var str='<ul class=\"search-result-list\">';
                var keywords = this.value.trim().toLowerCase().split(/[\s\-]+/);
                $resultContent.innerHTML = "";
                if (this.value.trim().length > 1) {
                  // perform local searching
                  datas.forEach(function(data) {
                    var isMatch = true;
                    var content_index = [];
                    var data_title = data.title.trim().toLowerCase();
                    var data_content = data.content.trim().replace(/<[^>]+>/g,"").toLowerCase();
                    var data_url = data.url;
                    var index_title = -1;
                    var index_content = -1;
                    var first_occur = -1;
                    // only match artiles with not empty titles and contents
                    if(data_title != '' && data_content != '') {
                      keywords.forEach(function(keyword, i) {
                        index_title = data_title.indexOf(keyword);
                        index_content = data_content.indexOf(keyword);
                        if( index_title < 0 && index_content < 0 ){
                          isMatch = false;
                        } else {
                          if (index_content < 0) {
                            index_content = 0;
                          }
                          if (i == 0) {
                            first_occur = index_content;
                          }
                        }
                      });
                    }
                    // show search results
                    if (isMatch) {
                      matchcounts += 1;
                      str += "<li><a href='"+ data_url +"' class='search-result-title'>"+ data_title +"</a>";
                      var content = data.content.trim().replace(/<[^>]+>/g,"");
                      if (first_occur >= 0) {
                        // cut out 100 characters
                        var start = first_occur - 20;
                        var end = first_occur + 80;
                        if(start < 0){
                          start = 0;
                        }
                        if(start == 0){
                          end = 50;
                        }
                        if(end > content.length){
                          end = content.length;
                        }
                        var match_content = content.substring(start, end);
                        // highlight all keywords
                        keywords.forEach(function(keyword){
                          var regS = new RegExp(keyword, "gi");
                          match_content = match_content.replace(regS, "<b class=\"search-keyword\">"+keyword+"</b>");
                        });
                        str += " " + match_content +"... "
                      }
                      str += "</li>";
                    }
                  })};
                str += "</ul>";
                if (matchcounts == 0) { str = ' <i class="fa fa-frown-o fa-5x" /> ' }
                if (keywords == "") { str = ' <i class="fa fa-search fa-5x" /> ' }
                $resultContent.innerHTML = str;
              });
              proceedsearch();
            }
          });}
        // handle and trigger popup window;
        $('.popup-trigger').mousedown(function(e) {
          e.stopPropagation();
          if (isfetched == false) {
            searchFunc(path, 'local-search-input', 'local-search-result');
          } else {
            proceedsearch();
          };
        });
        $('.popup-btn-close').click(function(e){
          $('.popup').hide();
          $(".popoverlay").remove();
          $('body').css('overflow', '');
        });
        $('.popup').click(function(e){
          e.stopPropagation();
        });
      });


  1. 在`layout/_scripts/third_party`文件夹下增加文件`algolia.swig`，内容如下。



    {%
      set js_algolia = [
        'src/algolia.js'
      ]
    %}
    {% for common in js_algolia %}
      {# S: Include Algolia instantsearch.js library #}
      {% set algolia_instant_css = url_for(theme.vendors._internal + '/algolia-instant-search/instantsearch.min.css') %}
      {% if theme.vendors.algolia_instant_css %}
        {% set algolia_instant_css = theme.vendors.algolia_instant_css %}
      {% endif %}
      <link rel="stylesheet" href="{{ algolia_instant_css }}">

      {% set algolia_instant_js = url_for(theme.vendors._internal + '/algolia-instant-search/instantsearch.min.js') %}
      {% if theme.vendors.algolia_instant_js %}
        {% set algolia_instant_js = theme.vendors.algolia_instant_js %}
      {% endif %}

      {# E: Include Algolia instantsearch.js library #}


    {% endfor %}


  1. 在`layout/_scripts/_layout.swig`文件的`body`标签内添加下面的语句。



      {% if theme.algolia %}
        {% include '_scripts/third-party/algolia.swig' %}
      {% endif %}

  1. 在`source/css`下新建文件夹`_algolia`，新建文件`algolia.styl`，内容如下。



    ul.search-result-list {
      padding-left: 0px;
      margin: 0px 5px 0px 8px;
    }
    p.search-result {
      border-bottom: 1px dashed #ccc;
      padding: 5px 0;
    }
    a.search-result-title {
      font-weight: bold;
    }
    a.search-result {
      border-bottom: transparent;
      display: block;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .search-keyword {
      border-bottom: 1px dashed #4088b8;
      font-weight: bold;
    }
    #local-search-result {
      height: 90%;
      overflow: auto;
    }
    .popup {
      display: none;
      position: fixed;
      top: 10%;
      left: 50%;
      width: 700px;
      height: 80%;
      margin-left: -350px;
      padding: 3px 0 0 10px;
      background: #fff;
      color: #333;
      z-index: 9999;
      border-radius: 5px;
    }
    @media (max-width: 767px) {
      .popup {
        padding: 3px;
        top: 0;
        left: 0;
        margin: 0;
        width: 100%;
        height: 100%;
        border-radius: 0px;
      }
    }
    .popoverlay {
      position: fixed;
      width: 100%;
      height: 100%;
      top: 0px;
      left: 0px;
      z-index: 2080;
      background-color: rgba(0,0,0,0.3);
    }
    #local-search-input {
      margin-bottom: 10px;
      width: 50%;
    }
    .popup-btn-close {
      position: absolute;
      top: 6px;
      right: 14px;
      color: #4ebd79;
      font-size: 14px;
      font-weight: bold;
      text-transform: uppercase;
      cursor: pointer;
    }
    #no-result {
      position: absolute;
      left: 44%;
      top: 42%;
      color: #ccc;
    }
    .busuanzi-count:before {
      content: " ";
      float: left;
      width: 260px;
      min-height: 25px;
    }
    @media (min-width: 768px) and (max-width: 991px) {
      .busuanzi-count {
        width: auto;
      }
      .busuanzi-count:before {
        display: none;
      }
    }
    @media (max-width: 767px) {
      .busuanzi-count {
        width: auto;
      }
      .busuanzi-count:before {
        display: none;
      }
    }
    .site-uv,
    .site-pv,
    .page-pv {
      display: inline-block;
    }
    .site-uv .busuanzi-value,
    .site-pv .busuanzi-value,
    .page-pv .busuanzi-value {
      margin: 0 5px;
    }
    .site-uv {
      margin-right: 10px;
    }
    .site-uv::after {
      content: "|";
      padding-left: 10px;
    }
    .algolia-popup {
      overflow: hidden;
      padding: 0;
    }
    .algolia-popup .popup-btn-close {
      padding-left: 15px;
      border-left: 1px solid #eee;
      top: 10px;
    }
    .algolia-popup .popup-btn-close .fa {
      color: #999;
      font-size: 18px;
    }
    .algolia-popup .popup-btn-close:hover .fa {
      color: #222;
    }
    .algolia-search {
      padding: 10px 15px 5px;
      max-height: 50px;
      border-bottom: 1px solid #ccc;
      background: #f5f5f5;
      border-top-left-radius: 5px;
      border-top-right-radius: 5px;
    }
    .algolia-search-input-icon {
      display: inline-block;
      width: 20px;
    }
    .algolia-search-input-icon .fa {
      font-size: 18px;
    }
    .algolia-search-input {
      display: inline-block;
      width: calc(90% - 20px);
    }
    .algolia-search-input input {
      padding: 5px 0;
      width: 100%;
      outline: none;
      border: none;
      background: transparent;
    }
    .algolia-powered {
      float: right;
    }
    .algolia-powered img {
      display: inline-block;
      height: 18px;
      vertical-align: middle;
    }
    .algolia-results {
      position: relative;
      overflow: auto;
      padding: 10px 30px;
      height: calc(100% - 50px);
    }
    .algolia-results hr {
      margin: 10px 0;
    }
    .algolia-results .highlight {
      font-style: normal;
      margin: 0;
      padding: 0 2px;
      font-size: inherit;
      color: #f00;
    }
    .algolia-hits {
      margin-top: 20px;
    }
    .algolia-hit-item {
      margin: 15px 0;
    }
    .algolia-hit-item-link {
      display: block;
      border-bottom: 1px dashed #ccc;
      transition-duration: 0.2s;
      transition-timing-function: ease-in-out;
      transition-delay: 0s;
    }
    .algolia-pagination .pagination {
      margin-top: 40px;
      border-top: none;
      padding: 0;
    }
    .algolia-pagination .pagination-item {
      display: inline-block;
    }
    .algolia-pagination .page-number {
      border-top: none;
    }
    .algolia-pagination .page-number:hover {
      border-bottom: 1px solid #222;
    }
    .algolia-pagination .disabled-item {
      visibility: hidden;
    }

  1. 在`source/css/main.styl`文件的最后新增下面语句。



      @import "_algolia/algolia";

  1. 将下面的图片放置于Hexo根目录下source文件夹下的images文件夹中，命名为`algolia_logo.svg`。
![](https://i-blog.csdnimg.cn/blog_migrate/a46853ec768deb9f3e48581d3eab5c24.png)

### 效果图

经过漫长的修改终于成功了，效果图如下。
![](https://i-blog.csdnimg.cn/blog_migrate/09d9a6f3f6c276f0466831b85683e229.png)

### 写在最后

  1. 为NexT主题添加Algolia搜索是一件复杂的事情，好消息是现在已经有版本在支持，但是还在开发阶段，未来一定会像[多说](http://duoshuo.com/)等等集成在NexT主题中，但是到那个时候，旧版本升级到新版本会不会有很多不适配什么的，所以如果你想用，不如按照我的方法自己添加。

  2. 如果按照我的方式不行的话，应该是在使用的NexT主题在哪个地方和我目前的版本不太一样，需要自己进行调整了。
