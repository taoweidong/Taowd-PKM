---
source: "http://jingyan.baidu.com/article/0eb457e523cbb803f1a9058d.html"
title: "java中map集合类用法（hashmap用法）-百度经验"
fetched_at: "2026-10-05 15:32:59"
---

# java中map集合类用法（hashmap用法）

  * 原创
  * |
  * 浏览：7164
  * |
  * 更新：2015-01-15 10:53
  * |
  * 标签：[java](/tag?tagName=java)

map键值对，值一般存储的是对象。hashmap中常用的方法，put(object key,object value);

get(object key);//根据key值找出对应的value值。

判断键是否存在：containsKey(object key)

判断值是否存在：containsValue(object value)

## [](javascript:;)方法/步骤

  1. 1

1.Map的特性即「键-值」（Key-Value）匹配

java.util.HashMap实作了Map界面，

HashMap在内部实作使用哈希（Hash），很快的时间内可以寻得「键-值」匹配.

2\. Map<String, String> map =

new HashMap<String, String>();

String key1 = "caterpillar";

String key2 = "justin";

map.put(key1, "caterpillar的讯息");

map.put(key2, "justin的讯息");

System.out.println(map.get(key1));

System.out.println(map.get(key2));

  2. 2

3.可以使用values()方法返回一个实作Collection的对象，当中包括所有的「值」对象

.

Map<String, String> map =

new HashMap<String, String>();

map.put("justin", "justin的讯息");

map.put("momor", "momor的讯息");

map.put("caterpillar", "caterpillar的讯息");

Collection collection = map.values();

Iterator iterator = collection.iterator();

while(iterator.hasNext()) {

System.out.println(iterator.next());

}

System.out.println();

  3. 3

4\. Map<String, String> map =

new LinkedHashMap<String, String>();

map.put("justin", "justin的讯息");

map.put("momor", "momor的讯息");

map.put("caterpillar", "caterpillar的讯息");

for(String value : map.values()) {

System.out.println(value);

}

END

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

 _作者声明：_ 本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

展开阅读全部 __
