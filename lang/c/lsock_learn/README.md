lsock_learn
===========

[c] Learning linux C socket programming, and others.  
这是个人在学习UNIX网络编程的过程中产生的程序，  
以及一些有关安全方面的初探。  

* [fakehttpd](./fakehttpd)...一个简单http服务器  
  内有独立的README。
* [config](./config)......lserv2 的配置文件目录  
  参见lserv2.pdf或lserv2.tex
* [lserv1](./lserv1)......非常基础的socket程序  
  实现最简单的TCP聊天功能，不过根据UNP，这种程序非常不完善。
* [foo](./foo).....简易并行(OpenMP)MD5爆破程序  
  假如为lserv2添加加密功能，比如MD5，那么根据lserv2使用的4位短密码，
  foo就能进行并行爆破。foo可以很轻松地被改写为串行模式（只需注释掉预处理器），
  另外并行模式比串行模式平均节省[48%]()的时间开销。  
* []...........lserv2 研究用的主程序  
  关于该程序细节可参考lserv2.pdf这个文档。它是一个指令驱动的服务器，
  用于各种实验。

###Reference
> UNP : Unix Network Programming

###Licence
MIT
