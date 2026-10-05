---
source: "http://www.cnblogs.com/adolfmc/archive/2012/10/07/2713711.html"
title: "Oracle the network adapter could not establish the connection - adolfmc - 博客园"
fetched_at: "2026-10-05 15:27:49"
---

这个问题折腾我时间比较长，网上很多资料都不太适合我的情况。不过最后还是被找到了 花了很多时间在其他方面没有锁定问题根源.

1 开始以为是防火墙 server client端都排除

2 oracle client端问题 （ubuntu 安装的client端）

3 最后用程序测试发现还是报Network adapter问题 最终锁定肯定是数据库server端问题 继续搜索发现问题.

找了ubuntu oracle clinet端工具用的时间比较长.

h2.jar 都用上了 我汗.

\-------------------------------------------------------------------------------------------------------------

最近自己学oracle发现了这个异常去google搜索了一下，这个问题一大堆啊，可是解决的方法寥寥无几(也许本人搜索水平太差)。这问题整整困惑我3个小时啦。刚刚解决，在这里把自已解决问题的方法帖出来，帮助那些碰见相同问题的初学者。不废话了直入主题。  
  
  
1.确定oracle Listener 监听服务已经启动。  
2.如果你的oracle数据库不是安装在本机那么请把oracle所在主机防火墙给关掉(哪怕你的防火墙开放1521端口,因为当有一个连接请求 1521端口时oracle会随机分配另一个端口给它.这是个人见解!望高手指点)  
3.确定你连接的IP地址正确。  
  
如果以上问题你都核实过那么请继续往下看。  
  
  
开始我是用eclipse database development 配置时发现了此问题.  
  
![oracle1](http://m2pk2q.blu.livefilestore.com/y1pG97d04U2bx2M2cRnKfHgcmNQLeSNVzHsuvT3rlnjhZGVnWLSikR6vZEOFUJBJRDXjbtT-sn62aWNjuFKgBWrW9PKkwLi9Ktq/Oracle1.jpg?psid=1)  
  
后来用 Oracle SQL Developer同样也无法连接.后来试了试sqlplus却可以连接.  
  
![oracle2](http://m2pk2q.blu.livefilestore.com/y1p1S5Nw63knJ3LpDNrqnJOMxbIL7U6Ms7YXMH33hYDZ6gi7KG422APagLapB74Xg8PXr01HtP23hBfAL74CnSrVrj5xVhJb1dI/Oracle2.jpg?psid=1)  
  
  
于是我再sqlplus试了一下192.168.1.2这个地址(同样是本机)却给出了这样的答案。  
第一次无监听程序，提示再输入用户名 却又连接上了。(看来第二次是跟你输入sqlplus一样的)  
  
![images3](http://m2pk2q.blu.livefilestore.com/y1p9ZPA4swje1BtT8VBPn6CBXMsguqkmQs7jjahrJ_aq_-lQfCsoz5H7PUWvSftCEdC1N_MjkpFwE3MrbYg7LzVopicNRd8x9Uc/Oracle3.jpg?psid=1)  
  
这个答案很明确了当你直接输入sqlplus可以登录，但是你把本机的IP给加上却不能登录。  
  
纳闷了几小时忽然想起以前在玩oracle的时候(没学之前^_^)在哪看见可以配置监听的,就是忘记哪在了。于是又花了半个小时终于找到了  
  
原来是Net Manager，(看来没事玩玩软件比玩玩游戏受益多啊)  
  
![images](http://m2pk2q.blu.livefilestore.com/y1pHT9NNWVZRfpqO7lu7if7jIenegDRZzu14mr5VdZ7Msnsrc_qSQLnnkyRwG8sc-TLFXzNcW_E6WSI-z5SF0IKqy3RJ2xD8EOU/imaegs.jpg?psid=1)  
  
启动Net Manager 选择LISTENER 现在可以看见监听的地址1原来是localhost不是192.168.1.2(本机)奇怪喽localhost不就是192.168.1.2(我的本机IP)吗?  
  
![](http://m2pk2q.blu.livefilestore.com/y1p9ZPA4swje1BRVciQEc6qw579xQBq3Y006UCxfxtL8RN5SyeONI54pfKqpxNsTdZzzNeLEGpLRFqycad6lqRhzftSr39ofpq6/Oracle4.jpg?psid=1)  
  
于是尝试了一下192.168.1.2  
用添加地址的按钮增加了一个192.168.1.2  
保存退出重启oracle Listener 监听服务稍等片刻。  
  
![images6](http://m2pk2q.blu.livefilestore.com/y1p-1Vdk5RYW8mXUgBefLX_F18RTa5kA-9xFs1SGfrh0xa25ijYMyzNT67UnvOj64mhoRdgmvahWxe8b0BnY6AgnDExL-e0YiJT/Oracle5.jpg?psid=1)  
  
  
![](http://m2pk2q.blu.livefilestore.com/y1pDx1TBeq_YLj72Wo8_i6cHysxGBGX-5MZ478-UZfx71ZiZ1VZTeFxYch_wA4dR1zphBTdSpwPLf8QFRbJJyVe_y27-JI2wbsf/Oracle6.jpg?psid=1)  
  
哈哈居然连接上。看来localhost 不等于192.168.1.2 (localhost是没有经过网卡的监听，嘿嘿个人意见，我不懂网络，纯属联想。)  
  
再试试 Oracle SQL Developer 同样也OK。  
  
![](http://m2pk2q.blu.livefilestore.com/y1pbMHIkoNibOiYuGHVXAjMXmqwGsE9ASoccu1PfmwqIKw24Gnb6whRzJTeByhE6NqPfMW34oPzaHD205-J9uPinDP8bvImxJiL/Oracle7.jpg?psid=1)  
  
  
无意间看着dos命令发现了这个  
  
![images7](http://m2pk2q.blu.livefilestore.com/y1pFiVVB0R2SyE1drzlC0jaHdSzZZFMgzLIaeNeEcm9W5-vQJ5IwK87dba6qnp4Jpmk0FWqjaWALkTkwyga2kPFAKjhqjy4X1nv/Oracle8.jpg?psid=1)  
  
以上有3个监听端点(这是增加了192.168.1.2IP)第一个是127.0.0.1第二是IPC协议xxxx(不懂)第三个就是增加的192.168.1.2。  
  
以下图片是增加192.168.1.2之前的  
  
![](http://m2pk2q.blu.livefilestore.com/y1puWnKsJ26urCdROK7TQueP17Kkiu6o9WJ58ZKx7rYc1fvZ2HFY9Ay9XknEY8jzR2MTDciDaxsUl0rnQQNN-Eb_bRu79NmyGAo/Oracle9.jpg?psid=1)  
  
只有两个监听端点  
  
提示：重启服务可以用命令也可以用windows的服务管理。  
  
命令如下  
  
监听启动: lsnrctl start  
监听停止: lsnrctl stop  
或者就输入：lsnrctl 再输入start 或者 stop  
  
启动Oracle: net start OracleServiceORACLE(ORACLE 我的SID)  
停止Oracle: net stop OracleServiceORACLE
