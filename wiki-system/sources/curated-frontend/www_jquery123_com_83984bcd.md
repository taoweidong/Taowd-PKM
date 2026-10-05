---
source: "https://www.jquery123.com/"
title: "jQuery API 中文文档 | jQuery中文网"
fetched_at: "2026-10-05 15:31:38"
---

## ![jQuery logo](/assets/images/jquery-logo-md.png)[jQuery API 中文文档 | jQuery 中文网](/ "jQuery API 中文文档 | jQuery 中文网")

# jQuery API 中文文档

jQuery 是一个高效、精简并且功能丰富的 JavaScript 工具库。它提供的 API 易于使用且兼容众多浏览器，这让诸如 HTML 文档遍历和操作、事件处理、动画和 Ajax 操作更加简单。如果你是一个 jQuery 新手，我们建议你先到[jQuery 学习中心](http://learn.jquery.com/)历练历练。

如果你是在升级新版本的 jQuery ，务必阅读[我们博客](http://blog.jquery.com/)上列出的版本发布说明。如果你以前使用的是 1.9 版本之前的 jQuery ，建议你再看一看 [1.9 版本升级指南](http://jquery.com/upgrade-guide/1.9/)。

注意，这份 API 中文文档是关于 jQuery 的，其他兄弟项目的 API 文档地址如下：

  * [jQuery UI API 文档](http://api.jqueryui.com/)
  * [jQuery Mobile API 文档](http://api.jquerymobile.com)
  * [QUnit API 文档](http://api.qunitjs.com)

* * *

添加元素到匹配的元素集合。

添加堆栈中元素集合到当前集合，一个选择性的过滤选择器。

为每个匹配的元素添加指定的样式类名

在匹配元素集合中的每个元素后面插入参数所指定的内容，作为其兄弟节点。

Register a handler to be called when Ajax requests complete. This is an AjaxEvent.

当Ajax请求完成后注册一个回调函数。这是一个 AjaxEvent。

Register a handler to be called when Ajax requests complete with an error. This is an Ajax Event.

Ajax请求出错时注册一个回调处理函数，这是一个 Ajax Event。

Attach a function to be executed before an Ajax request is sent. This is an Ajax Event.

在Ajax请求发送之前绑定一个要执行的函数，这是一个 Ajax Event.

Register a handler to be called when the first Ajax request begins. This is an Ajax Event.

在AJAX 请求刚开始时执行一个处理函数。 这是一个 Ajax Event.

Register a handler to be called when all Ajax requests have completed. This is an Ajax Event.

在AJAX 请求完成时执行一个处理函数。 这是一个 Ajax Event。

Attach a function to be executed whenever an Ajax request completes successfully. This is an Ajax Event.

绑定一个函数当 Ajax 请求成功完成时执行。 这是一个Ajax Event.

选择所有元素.

添加先前的堆栈元素集合到当前组合。

根据一组 CSS 属性，执行自定义动画。

选择所有正在执行动画效果的元素.

在每个匹配元素里面的末尾处插入参数内容。

将匹配的元素插入到目标元素的最后面（译者注：内部插入）。

获取匹配的元素集合中的第一个元素的属性的值。设置每一个匹配元素的一个或多个属性。

选择指定属性值等于给定字符串或以该字符串为前缀（该字符串后跟一个连字符“-” ）的元素。

选择指定属性具有包含一个给定的子字符串的元素。（选择给定的属性是以包含某些值的元素）

选择指定属性用空格分隔的值中包含一个给定值的元素。

选择指定属性是以给定值结尾的元素。这个比较是区分大小写的。

选择指定属性是给定值的元素。

选择不存在指定属性，或者指定的属性值不等于给定值的元素。

选择指定属性是以给定字符串开始的元素

根据参数设定，在匹配元素的前面插入内容（译者注：外部插入）

为一个元素绑定一个事件处理程序。

Bind an event handler to the "blur" event, or trigger that event on an element.

为 "blur" 事件绑定一个处理函数，或者触发元素上的 "blur" 事件（注：此事件不支持冒泡）。

选择所有按钮元素和类型为按钮的元素。

回调列表中添加一个回调或回调的集合。

禁用回调列表中的回调

确定回调列表是否已被禁用。

从列表中删除所有的回调.

传入指定的参数调用所有的回调

访问给定的上下文和参数列表中的所有回调。

确定回调是否至少已经调用一次。

确定列表中是否提供一个回调

锁定回调列表的当前状态。

确定回调列表是否已被锁定。

从回调列表中的删除一个回调或回调集合。

为JavaScript 的 "change" 事件绑定一个处理函数，或者触发元素上的 "change" 事件。

Bind an event handler to the "change" event, or trigger that event on an element.

选择所有类型为复选框的元素。

匹配所有勾选的元素。

选择所有指定“parent”元素中指定的"child"的直接子元素。

获得匹配元素集合中每个元素的子元素，选择器选择性筛选。

选择给定样式类名的所有元素。

从列队中移除所有未执行的项。

Bind an event handler to the "click" event, or trigger that event on an element.

为 JavaScript 的"click" 事件绑定一个处理器，或者触发元素上的 "click" 事件。

从元素本身开始，在DOM 树上逐级向上级元素匹配，并返回最先匹配的祖先元素。以数组的形式返回与选择器相匹配的所有元素，从当前元素开始，在 DOM 树中向上遍历。

创建一个匹配的元素集合的深度拷贝副本。

选择所有包含指定文本的元素。

获得匹配元素集合中每个元素的子元素，包括文字和注释节点。

原始的DOM节点的内容传给jQuery()；如果没有东西被传递，那么上下文将可能是该文档（document）。

Bind an event handler to the "contextmenu" event, or trigger that event on an element.

Bind an event handler to the "contextmenu" event, or trigger that event on an element.

获取匹配元素集合中的第一个元素的样式属性的值设置每个匹配元素的一个或多个CSS属性。

在匹配元素上存储任意相关数据. 返回匹配的元素集合中的第一个元素的给定名称的数据存储的值。 通过.data(name, value)或HTML5 data-* 属性设置

Bind an event handler to the "dblclick" event, or trigger that event on an element.

为JavaScript 的 "dblclick" 事件绑定一个处理函数，或者触发元素上的 "dblclick" 事件。

当Deferred（延迟）对象解决或拒绝时，调用添加处理程序。

Add handlers to be called when the Deferred object is rejected.

当Deferred（延迟）对象解决时，调用添加处理程序。

当Deferred（延迟）对象拒绝时，调用添加的处理程序。

确定一个Deferred（延迟）对象是否已被拒绝。

确定一个Deferred（延迟）对象是否已被解决。

根据给定的 args参数 调用Deferred（延迟）对象上进行中的回调 （progressCallbacks）。

根据给定的上下文（context）和args递延调用Deferred（延迟）对象上进行中的回调（progressCallbacks ）。

用用于过滤 and/or 链式延迟对象的工具方法。

当Deferred（延迟）对象生成进度通知时，调用添加处理程序。

返回Deferred(延迟)的Promise（承诺）对象。

拒绝Deferred（延迟）对象，并根据给定的args参数调用任何失败回调函数（failCallbacks）。

拒绝Deferred（延迟）对象，并根据给定的 context和args参数调用任何失败回调函数（failCallbacks）。

解决Deferred（延迟）对象，并根据给定的args参数调用任何完成回调函数（doneCallbacks）。

解决Deferred（延迟）对象，并根据给定的 context和args参数调用任何完成回调函数（doneCallbacks）。

当Deferred（延迟）对象解决，拒绝或仍在进行中时，调用添加处理程序。

确定一个Deferred（延迟）对象的当前状态。

设置一个延时来推迟执行队列中后续的项。

为所有匹配选择器（selector参数）的元素绑定一个或多个事件处理函数，基于一个指定的根元素的子集，匹配的元素包括那些目前已经匹配到的元素，也包括那些今后可能匹配到的元素。

执行匹配元素队列的下一个函数。

选择给定的祖先元素的所有后代元素。

从DOM中去掉所有匹配的元素。

从元素中删除先前用.live()绑定的所有事件。

选择所有被禁用的元素。

遍历一个jQuery对象，为每个匹配元素执行一个函数。

根据给定（html）标记名称选择所有的元素。

选择所有没有子元素的元素（包括文本节点）。

从DOM中移除集合中匹配元素的所有子节点。

选择所有可用的（注：未被禁用的元素）元素。

终止在当前链的最新过滤操作，并返回匹配的元素的以前状态。

在匹配的集合中选择索引值为index的元素。

减少匹配元素的集合为指定的索引的哪一个元素。

Bind an event handler to the "error" event, or trigger that event on an element.

为 JavaScript 的 "error" 事件绑定一个处理函数。

选择所引值为偶数的元素，从 0 开始计数。 也可以查看 odd.

Reduce the set of matched elements to the even ones in the set, numbered from zero.

在事件冒泡过程中的当前DOM元素。

绑定了当前正在调用jQuery 事件处理器的元素。

当当前正在执行的处理程序绑定时，一个可选的数据对象传递给一个事件方法。

根据事件对象中是否调用过 event.preventDefault() 方法,来返回一个布尔值。

根据事件对象中是否调用过 event.stopImmediatePropagation() 方法,来返回一个布尔值。

根据事件对象中是否调用过 event.stopPropagation() 方法,来返回一个布尔值。

表示事件触发时哪个Meta键被按下。

当事件被触发时此属性包含指定的命名空间。

鼠标相对于文档的左边缘的位置（左边）。

鼠标相对于文档的顶部边缘的位置（坐标）。

如果调用这个方法，默认事件行为将不再触发。

在事件中涉及的其它任何DOM元素。

事件被触发的一个事件处理程序的最后返回值，除非值是 undefined。

阻止剩余的事件处理函数执行并且防止事件冒泡到DOM树上。

防止事件冒泡到DOM树上，也就是不触发的任何前辈元素上的事件处理函数。

触发事件的DOM元素。

这个属性返回事件触发时距离1970年1月1日的毫秒数。

描述事件的性质。

针对键盘和鼠标事件，这个属性能确定你到底按的是哪个键。

通过淡入的方式显示匹配元素。

通过淡出的方式隐藏匹配元素。

调整匹配元素的透明度。

通过匹配的元素的不透明度动画，来显示或隐藏它们。

选择所有类型为文件（file）的元素。

筛选元素集合中匹配表达式 或 通过传递函数测试的 那些元素集合。

通过一个选择器，jQuery对象，或元素过滤，得到当前匹配的元素集合中每个元素的后代。

停止当前正在运行的动画，删除所有排队的动画，并完成匹配元素所有的动画。

选择所有父级元素下的第一个子元素。

选择所有相同的元素名称的第一个兄弟元素。

选择第一个匹配的元素。

获取匹配元素集合中第一个元素。

选择当前获取焦点的元素。

Bind an event handler to the "focus" event, or trigger that event on an element.

为 JavaScript 的 "focus" 事件绑定一个处理函数，或者触发元素上的 "focus" 事件。

Bind an event handler to the "focusin" event, or trigger that event on an element.

将一个事件函数绑定到"focusin" 事件。

Bind an event handler to the "focusout" event, or trigger that event on an element.

将一个事件函数绑定到"focusout" 事件。

通过jQuery对象获取一个对应的DOM元素。

选择匹配集合中所有大于给定index（索引值）的元素。

选择所有具有指定属性的元素，该属性可以是任何值。

选择元素其中至少包含指定选择器匹配的一个种元素。

筛选匹配元素集合中的那些有相匹配的选择器或DOM元素的后代元素。

确定任何一个匹配元素是否有被分配给定的（样式）类。

选择所有标题元素，像h1, h2, h3 等.

获取匹配元素集合中的第一个元素的当前计算高度值。设置每一个匹配元素的高度值。

选择所有隐藏的元素。

隐藏匹配的元素。

将二个事件函数绑定到匹配元素上，分别当鼠标指针进入和离开元素时被执行。将一个单独事件函数绑定到匹配元素上，分别当鼠标指针进入和离开元素时被执行。

获取集合中第一个匹配元素的HTML内容 设置每一个匹配元素的html内容。

选择一个具有给定id属性的单个元素。

选择所有图像类型的元素。

从匹配的元素中搜索给定元素的索引值，从0开始计数。

为匹配的元素集合中获取第一个元素的当前计算高度值,包括padding，但是不包括border。

为匹配的元素集合中获取第一个元素的当前计算宽度值,包括padding，但是不包括border。

选择所有 input, textarea, select 和 button 元素.

在目标元素后面插入集合中每个匹配的元素(注：插入的元素作为目标元素的兄弟元素)。

在目标元素前面插入集合中每个匹配的元素(注：插入的元素作为目标元素的兄弟元素)。

判断当前匹配的元素集合中的元素，是否为一个选择器，DOM元素，或者jQuery对象，如果这些元素至少一个匹配给定的参数，那么返回true。

一个多用途的回调列表对象，提供了强大的的方式来管理回调函数列表。

Handle errors produced by Deferreds.

Return an Error instance with a defined stack.

Return an Error instance with a defined stack.

一个构造函数，返回一个链式实用对象方法来注册多个回调，回调队列， 调用回调队列，并转达任何同步或异步函数的成功或失败状态。

执行一个异步的HTTP（Ajax）的请求。

在每个请求之前被发送和$.ajax()处理它们前处理，设置自定义Ajax选项或修改现有选项。

为以后要用到的Ajax请求设置默认的值

创建一个对象，用于处理Ajax数据的实际传输。

在jQuery 1.3中不建议使用（查看jQuery.support)。当前页面中浏览器是否使用标准盒模型渲染页面。 建议使用 jQuery.support.boxModel 代替。W3C CSS Box Model。

用来获取useragent的包含标志，读取自 navigator.userAgent。这个属性在jQuery 1.9已经被删除并且只能通过的jQuery.migrate插件使用。请尝试使用特征检测代替。 用户的浏览器渲染引擎的版本号。

检查一个DOM元素是另一个DOM元素的后代。

直接向 jQuery 中添加钩子，用于覆盖设置或获取特定 CSS 属性时的方法，目的是为了标准化 CSS 属性名或创建自定义属性。

An object containing all CSS properties that may be used without a unit. Prior to jQuery 4.0, the .css() method uses this object to see if it may append px to unitless values.

存储任意数据到指定的元素,返回设置的值。 返回用jQuery.data(element, name, value)储存在元素上的相应名字的数据，或者元素上完整的数据存储

在匹配的元素上执行队列中的下一个函数。

一个通用的迭代函数，它可以用来无缝迭代对象和数组。数组和类似数组的对象通过一个长度属性（如一个函数的参数对象）来迭代数字索引，从0到length - 1。其他对象通过其属性名进行迭代。

接受一个字符串，并抛出包含这个字符串的异常。

Escapes any character that has a special meaning in a CSS selector.

将两个或更多对象的内容合并到第一个对象。

The jQuery selector engine, formerly known as Sizzle, is exposed under jQuery.find. This page describes all the APIs under jQuery.find.

一个对象的内容合并到jQuery的原型，以提供新的jQuery实例方法。

该动画的频率（以毫秒为单位）。

全局的禁用所有动画。

使用一个HTTP GET请求从服务器加载数据。

使用一个HTTP GET请求从服务器加载JSON编码的数据。

使用一个HTTP GET请求从服务器加载并执行一个 JavaScript 文件

在全局上下文下执行一些JavaScript代码。

查找满足过滤函数的数组元素。原始数组不受影响。

确定任何一个元素是否有与之相关的jQuery数据。

暂停或恢复.ready() 事件的执行。

接受一个包含一个CSS选择器的字符串，用于匹配的一组元素。根据提供的原始 HTML 标记字符串，动态创建由 jQuery 对象包装的 DOM 元素。当DOM完成加载的时候绑定一个要执行的函数。

Modify and filter HTML strings passed through jQuery manipulation methods.

在数组中查找指定值并返回它的索引（如果没有找到，则返回-1）。

确定的参数是一个数组。

检查对象是否为空（不包含任何属性）。

确定参数是否为一个Javascript 函数。

确定它的参数是否是一个数字。

测试对象是否是纯粹的对象（通过 "{}" 或者 "new Object" 创建的）

确定参数是否为一个window对象。

检查一个DOM节点是否在XML文档中（或者是一个XML文档）。

转换一个类似数组的对象成为真正的JavaScript数组。

将一个数组中的所有元素转换到另一个数组中。

合并两个数组内容到第一个数组。

放弃jQuery控制$ 变量。

一个空函数

返回一个数字，表示当前时间。

创建一个数组或对象序列化的的字符串，适用于一个URL 地址查询字符串或Ajax请求。

将字符串解析到一个DOM节点的数组中。

接受一个标准格式的 JSON 字符串，并返回解析后的 JavaScript 对象。

使用一个HTTP POST 请求从服务器加载数据。

解析一个字符串到一个XML文档。

接受一个函数，然后返回一个新函数，并且这个新函数始终保持了特定的上下文语境。

显示在匹配的元素上的已经执行的函数列队。操作匹配元素上将要执行的函数队列。

A Promise-like object (or "thenable") that resolves when the document is ready.

Handles errors thrown synchronously in functions wrapped in jQuery().

删除一个先前存储的数据片段。

Creates an object containing a set of properties ready to be used in the definition of custom animations.

可创建一个新的jQuery副本，其属性和方法可以修改，而不会影响原来的jQuery对象。

它们代表了不同的浏览器功能或错误存在的属性集合。当他们不再需要在内部以提高页面的启动性能时，这些特定属性可能会被删除。 对于你自己的项目功能检测的需求， 我们强烈建议使用外部库，比如Modernizr的，而不是依赖于jQuery.support上的属性。

去掉字符串起始和结尾的空格。

确定JavaScript 对象的类型[[Class]] 。

删除数组中重复元素。只处理删除DOM元素数组，而不能处理字符串或者数字数组。

Sorts an array or an array-like object of DOM elements, in place, with the duplicates removed. Note that this only works on arrays/array-likes of DOM elements, not strings or numbers.

提供一种方法来执行一个或多个对象的回调函数， Deferred(延迟)对象通常表示异步事件。

一个包含了jQuery版本号的字符串。

Bind an event handler to the "keydown" event, or trigger that event on an element.

为 "keydown" 事件绑定一个处理函数，或者触发元素上的 "keydown" 事件。

为 "keypress" 事件绑定一个处理函数，或者触发元素上的 "keypress" 事件。

Bind an event handler to the "keypress" event, or trigger that event on an element.

Bind an event handler to the "keyup" event, or trigger that event on an element.

为 "keyup" 事件绑定一个处理函数，或者触发元素上的 "keyup" 事件。

选择指定语言的所有元素。

选择所有父级元素下的最后一个子元素。

选择的所有元素之间具有相同元素名称的最后一个兄弟元素。

选择最后一个匹配的元素。

获取匹配元素集合中最后一个元素。

在jQuery对象中元素的数量。

附加一个事件处理器到匹配目前选择器的所有元素，现在和未来。

为 JavaScript 的 "load" 事件绑定一个处理函数。

Bind an event handler to the "load" event, or trigger that event on an element.

从服务器载入数据并且将返回的 HTML 代码并插入至 匹配的元素 中。

选择匹配集合中所有索引值小于给定index参数的元素。

通过一个函数匹配当前集合中的每个元素,产生一个包含新的jQuery对象。

Bind an event handler to the "mousedown" event, or trigger that event on an element.

为 JavaScript 的 "mousedown" 事件绑定一个处理函数，或者触发元素上的该事件。

Bind an event handler to the "mouseenter" event, or trigger that event on an element.

为 mouse enters（鼠标进入） 事件绑定一个处理函数，或者触发元素上的 mouse enters（鼠标进入） 事件。

Bind an event handler to the "mouseleave" event, or trigger that event on an element.

为 mouse leaves（鼠标离开） 事件绑定一个处理函数，或者触发元素上的 mouse leaves（鼠标离开） 事件。

Bind an event handler to the "mousemove" event, or trigger that event on an element.

为 JavaScript 的 "mousemove" 事件绑定一个处理函数，或者触发元素上的该事件。

Bind an event handler to the "mouseout" event, or trigger that event on an element.

为 JavaScript 的 "mouseout" 事件绑定一个处理函数，或者触发元素上的该事件。（注：支持事件冒泡）

Bind an event handler to the "mouseover" event, or trigger that event on an element.

为 JavaScript 的 "mouseover" 事件绑定一个处理函数，或者触发元素上的该事件。（注：支持事件冒泡）

Bind an event handler to the "mouseup" event, or trigger that event on an element.

为 JavaScript 的 "mouseup" 事件绑定一个处理函数，或者触发元素上的该事件。

选择匹配所有指定的属性筛选器的元素

将每一个选择器匹配到的元素合并后一起返回。

Selects all next elements matching "next" that are immediately preceded by a sibling "prev".

匹配 “prev” 元素之后的所有 兄弟元素。具有相同的父元素，并匹配过滤“siblings”选择器。

取得匹配的元素集合中每一个元素紧邻的后面同辈元素的元素集合。如果提供一个选择器，那么只有紧跟着的兄弟元素满足选择器时，才会返回此元素。

获得每个匹配元素集合中所有下面的同辈元素，选择性筛选的选择器。

通过选择器，DOM节点，或jQuery对象得到每个元素之后的所有兄弟元素，但不包括匹配的元素。

选择所有元素去除不匹配给定的选择器的元素。

从匹配的元素集合中移除指定的元素。

选择的他们所有父元素的第n个子元素。

选择所有他们父元素的第n个子元素。计数从最后一个元素开始到第一个。

选择的所有他们的父级元素的第n个子元素，计数从最后一个元素到第一个。

选择同属于一个父元素之下，并且标签名相同的子元素中的第n个。（感谢@caikan提供的翻译）

选择索引值为奇数元素，从 0 开始计数。同样查看偶数 even.

Reduce the set of matched elements to the odd ones in the set, numbered from zero.

在匹配的元素集合中，获取的第一个元素的当前坐标，坐标相对于文档。 设置匹配的元素集合中每一个元素的坐标， 坐标相对于文档。

移除一个事件处理函数。

取得离指定元素最近的含有定位信息的祖先元素。含有定位信息的元素指的是，CSS 的 position 属性是 relative, absolute, 或 fixed 的元素。

在选定的元素上绑定一个或多个事件处理函数。

为元素的事件添加处理函数。处理函数在每个元素上每种事件类型最多执行一次。

如果某个元素是其父元素的唯一子元素，那么它就会被选中。

获取元素集合中第一个元素的当前计算高度值,包括padding，border和选择性的margin。返回一个整数（不包含“px”）表示的值 ，或如果在一个空集合上调用该方法，则会返回 null。

选择所有没有兄弟元素，且具有相同的元素名称的元素。

获取元素集合中第一个元素的当前计算宽度值,包括padding，border和选择性的margin。（注：返回一个整数（不包含“px”）表示的值，或如果在一个空集合上调用该方法，则会返回 null。）

选择所有含有子元素或者文本的父级元素。

取得匹配元素集合中，每个元素的父元素，可以提供一个可选的选择器。

获得集合中每个匹配元素的祖先元素，可以提供一个可选的选择器作为参数。

查找当前元素的所有的前辈元素，直到遇到选择器， DOM 节点或 jQuery 对象匹配的元素为止，但不包括这些元素。

选择所有类型为密码的元素。

获取匹配元素中第一个元素的当前坐标，相对于offset parent的坐标。( 译者注：offset parent指离该元素最近的而且被定位过的祖先元素 )

将参数内容插入到每个匹配元素的前面（元素内部）。

将所有元素插入到目标前面（元素内）。

取得一个包含匹配的元素集合中每一个元素紧邻的前一个同辈元素的元素集合。选择性筛选的选择器。

获得集合中每个匹配元素的所有前面的兄弟元素，选择性筛选的选择器。

获取每个元素但不包括选择器，DOM节点，或者jQuery对象匹配的元素的所有前面的兄弟元素。

返回一个 Promise 对象，用来观察当某种类型的所有行动绑定到集合，排队与否还是已经完成。

获取匹配的元素集中第一个元素的属性（property）值为匹配的元素设置一个或多个属性（properties）。

将一个DOM元素集合加入到jQuery栈。

显示在匹配的元素上的已经执行的函数列队。在匹配元素上操作已经附加函数的列表。

选择所有类型为单选框的元素。

当DOM准备就绪时，指定一个函数来执行。

将匹配元素集合从DOM中删除。（注：同时移除元素上的事件及 jQuery 数据。）

为匹配的元素集合中的每个元素中移除一个属性（attribute）。

移除集合中每个匹配元素上一个，多个或全部样式。

为集合中匹配的元素删除一个属性（property）。

在元素上移除绑定的数据

用集合的匹配元素替换每个目标元素。

用提供的内容替换集合中所有匹配的元素并且返回被删除元素的集合。

选择所有类型为重置的元素。

Bind an event handler to the "resize" event, or trigger that event on an element.

为 JavaScript 的 "resize" 事件绑定一个处理函数，或者触发元素上的该事件。

Bind an event handler to the "scroll" event, or trigger that event on an element.

选择该文档的根元素。

为 JavaScript 的 "scroll" 事件绑定一个处理函数，或者触发元素上的该事件。

获取匹配的元素集合中第一个元素的当前水平滚动条的位置。设置每个匹配元素的水平滚动条位置。

获取匹配的元素集合中第一个元素的当前垂直滚动条的位置或设置每个匹配元素的垂直滚动条位置。设置每个匹配元素的垂直滚动条位置

Bind an event handler to the "select" event, or trigger that event on an element.

为 JavaScript 的 "select" 事件绑定一个处理函数，或者触发元素上的该事件。

获取 select 元素中所有被选中的元素。

返回传给jQuery()的原始选择器。

将用作提交的表单元素的值编译成字符串。

显示匹配的元素

将用作提交的表单元素的值编译成拥有name和value对象组成的数组。例如[ { name: a value: 1 }, { name: b value: 2 },...]

获得匹配元素集合中每个元素的兄弟元素,可以提供一个可选的选择器。。

返回的jQuery对象匹配的DOM元素的数量。

根据指定的下标范围，过滤匹配的元素集合，并生成一个新的 jQuery 对象。

用滑动动画显示或隐藏一个匹配元素。

用滑动动画显示一个匹配元素。

用滑动动画隐藏一个匹配元素。

停止匹配元素当前正在运行的动画。

选择所有类型为提交的元素。

Bind an event handler to the "submit" event, or trigger that event on an element.

为 JavaScript 的 "submit" 事件绑定一个处理函数，或者触发元素上的该事件。

选择由文档URI的格式化识别码表示的目标元素。

选择所有类型为文本的元素。

得到匹配元素集合中每个元素的合并文本，包括他们的后代设置匹配元素集合中每个元素的文本内容为指定的文本内容。

返回一个包含jQuery对象集合中的所有DOM元素的数组。

绑定两个或多个处理程序绑定到匹配的元素，用来执行在交替的点击。

显示或隐藏匹配元素。

在匹配的元素集合中的每个元素上添加或删除一个或多个样式类,取决于这个样式类是否存在或值切换属性。即：如果存在（不存在）就删除（添加）一个类。

根据绑定到匹配元素的给定的事件类型执行所有的处理程序和行为。

为一个事件执行附加到元素的所有处理程序。

从元素上删除一个以前附加事件处理程序。

删除当前选择器匹配的所有元素的事件处理程序，根据一组特定根元素的集合。

Sorts a jQuery object of DOM elements, in place, with the duplicates removed. Note that this only works on jQuery objects consisting of DOM elements, not strings or numbers.

Bind an event handler to the "unload" event, or trigger that event on an element.

为 JavaScript 的 "unload" 事件绑定一个处理函数。

将匹配元素集合的父级元素删除，保留自身（和兄弟元素，如果存在）在原来的位置。

获取匹配的元素集合中第一个元素的当前值。设置匹配的元素集合中每个元素的值。

选择所有可见的元素。

为匹配的元素集合中获取第一个元素的当前计算宽度值。给每个匹配的元素设置CSS宽度。

在每个匹配的元素外层包上一个html元素。

在所有匹配元素外面包一层HTML结构。

在匹配元素里的内容外包一层结构。
