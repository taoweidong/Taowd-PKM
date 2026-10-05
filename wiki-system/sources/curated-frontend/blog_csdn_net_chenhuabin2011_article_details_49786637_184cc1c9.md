---
source: "http://blog.csdn.net/chenhuabin2011/article/details/49786637"
title: "EASYUI 树形菜单 fastjson JAVA嵌套对象转JSON_fastjson 菜单-CSDN博客"
fetched_at: "2026-10-05 15:31:19"
---

使用EASYUI 的树形导航菜单 JAVA对象转菜单

我用的是JDK1.8 使用 fastjson1.2.7版本 从github下载下来的源代码

EasyUiTree.java对象代码如下：

package org.bingley.test;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

/**
* @Title: EasyUiTree.java
* @Package org.bingley.test
* @Description: TODO(用一句话描述该文件做什么)
* @Copyright: Copyright (c) 2014 FJBL All Rights Reserved
* @author bingley
* @date 2015年11月11日 下午5:36:18
* @version V1.00.00
*/
public class EasyUiTree implements Serializable {
/**
*
*/
private static final long serialVersionUID = 3714827586565908167L;
private String id;
private String text;
private String state;
private String checked;
private Map<String,String> attributes;
private List<EasyUiTree> children;
public String getId() {
return id;
}
public void setId(String id) {
this.id = id;
}
public String getText() {
return text;
}
public void setText(String text) {
this.text = text;
}
public String getState() {
return state;
}
public void setState(String state) {
this.state = state;
}
public String getChecked() {
return checked;
}
public void setChecked(String checked) {
this.checked = checked;
}
public Map<String, String> getAttributes() {
return attributes;
}
public void setAttributes(Map<String, String> attributes) {
this.attributes = attributes;
}
public List<EasyUiTree> getChildren() {
return children;
}
public void setChildren(List<EasyUiTree> children) {
this.children = children;
}



}

测试代码如下：

package org.bingley.test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.alibaba.fastjson.JSON;


/**@ClassName: TestJsonTree
* @Description: TODO(这里用一句话描述这个类的作用)
* @Copyright: Copyright (c) 2015 FJBL All Rights Reserved
* @author bingley
* @date 2015年11月11日 下午9:16:28
* @version 1.00.00
* @history:
*/
public class TestJsonTree {

public static void main(String[] args) {

EasyUiTree tree1=new EasyUiTree();
tree1.setText("根菜单");
List<EasyUiTree> treenode=new ArrayList();
for (int i=0;i<3;i++)
{
EasyUiTree tree=new EasyUiTree();
tree.setText("一级"+i);
List<EasyUiTree> child=new ArrayList();
for (int j=0;j<4;j++)
{
EasyUiTree stree=new EasyUiTree();
stree.setText("二级菜单"+i+""+j);
Map<String,String> map=new HashMap();
map.put("url", "url"+j);
stree.setAttributes(map);
child.add(stree);
}
tree.setChildren(child);
treenode.add(tree);
}

tree1.setChildren(treenode);

String str="";
System.out.println("test 开始转化");
str= JSON.toJSONString(tree1);
System.out.println(str);
System.exit(0);


}

}

执行结果如下：

{"children":[{"children":[{"attributes":{"url":"url0"},"text":"二级菜单00"},{"attributes":{"url":"url1"},"text":"二级菜单01"},{"attributes":{"url":"url2"},"text":"二级菜单02"},{"attributes":{"url":"url3"},"text":"二级菜单03"}],"text":"一级0"},{"children":[{"attributes":{"url":"url0"},"text":"二级菜单10"},{"attributes":{"url":"url1"},"text":"二级菜单11"},{"attributes":{"url":"url2"},"text":"二级菜单12"},{"attributes":{"url":"url3"},"text":"二级菜单13"}],"text":"一级1"},{"children":[{"attributes":{"url":"url0"},"text":"二级菜单20"},{"attributes":{"url":"url1"},"text":"二级菜单21"},{"attributes":{"url":"url2"},"text":"二级菜单22"},{"attributes":{"url":"url3"},"text":"二级菜单23"}],"text":"一级2"}],"text":"根菜单"}
