# 概述

这个模拟器 `paging-policy.py`允许你尝试不同的页面替换策略。例如，让我们用大小为 3 的缓存来检查 LRU 策略在一系列页面引用下的表现：

```
0 1 2 0 1 3 0 3 1 2 1
```

为此，按如下方式运行模拟器：

```
提示符> ./paging-policy.py --addresses=0,1,2,0,1,3,0,3,1,2,1
                           --policy=LRU --cachesize=3 -c
```

你将看到如下输出：

```
ARG addresses 0,1,2,0,1,3,0,3,1,2,1
ARG numaddrs 10
ARG policy LRU
ARG cachesize 3
ARG maxpage 10
ARG seed 0

Solving...

Access: 0 MISS LRU->      [br 0]<-MRU Replace:- [br Hits:0 Misses:1]
Access: 1 MISS LRU->   [br 0, 1]<-MRU Replace:- [br Hits:0 Misses:2]
Access: 2 MISS LRU->[br 0, 1, 2]<-MRU Replace:- [br Hits:0 Misses:3]
Access: 0 HIT  LRU->[br 1, 2, 0]<-MRU Replace:- [br Hits:1 Misses:3]
Access: 1 HIT  LRU->[br 2, 0, 1]<-MRU Replace:- [br Hits:2 Misses:3]
Access: 3 MISS LRU->[br 0, 1, 3]<-MRU Replace:2 [br Hits:2 Misses:4]
Access: 0 HIT  LRU->[br 1, 3, 0]<-MRU Replace:2 [br Hits:3 Misses:4]
Access: 3 HIT  LRU->[br 1, 0, 3]<-MRU Replace:2 [br Hits:4 Misses:4]
Access: 1 HIT  LRU->[br 0, 3, 1]<-MRU Replace:2 [br Hits:5 Misses:4]
Access: 2 MISS LRU->[br 3, 1, 2]<-MRU Replace:0 [br Hits:5 Misses:5]
Access: 1 HIT  LRU->[br 3, 2, 1]<-MRU Replace:0 [br Hits:6 Misses:5]
```

`paging-policy.py`的完整可能参数列表在下面列出，包括许多选项，用于改变策略、指定/生成地址的方式以及其他重要参数，例如缓存的大小。

```
提示符> ./paging-policy.py --help
用法: paging-policy.py [选项]

选项:
  -h, --help            显示此帮助信息并退出
  -a ADDRESSES, --addresses=ADDRESSES
                        要访问的以逗号分隔的页面集合；-1 表示随机生成
  -f ADDRESSFILE, --addressfile=ADDRESSFILE
                        包含大量地址的文件
  -n NUMADDRS, --numaddrs=NUMADDRS
                        如果 -a (--addresses) 是 -1，则这是要生成的地址数量
  -p POLICY, --policy=POLICY
                        替换策略: FIFO, LRU, LFU, OPT, UNOPT, RAND, CLOCK
  -b CLOCKBITS, --clockbits=CLOCKBITS
                        对于 CLOCK 策略，使用多少位时钟位
  -C CACHESIZE, --cachesize=CACHESIZE
                        页面缓存的大小，以页为单位
  -m MAXPAGE, --maxpage=MAXPAGE
                        如果随机生成页面访问，这是最大的页码
  -s SEED, --seed=SEED  随机数种子
  -N, --notrace         不打印详细追踪信息
  -c, --compute         为我计算答案
```

与往常一样，"-c" 用于解决特定问题，如果没有它，则只列出访问（程序不会告诉你特定的访问是命中还是未命中）。

要生成一个随机问题，而不是使用 "-a/--addresses" 传入一些页面引用，你可以传入 "-n/--numaddrs" 作为程序应随机生成的地址数量，并使用 "-s/--seed" 来指定不同的随机种子。例如：

```
提示符> ./paging-policy.py -s 10 -n 3
...
假设替换策略为 FIFO，缓存大小为 3 页，
判断以下每个页面引用是命中还是未命中
在页面缓存中。

访问: 5  命中/未命中? 内存状态?
访问: 4  命中/未命中? 内存状态?
访问: 5  命中/未命中? 内存状态?
```

如你所见，在这个例子中，我们指定了 "-n 3"，这意味着程序应该生成 3 个随机的页面引用，它生成了：5、4 和 5。同时也指定了随机种子 (10)，这让我们得到了这些特定的数字。在你自己计算之后，可以通过传入相同的参数但加上 "-c" 来让程序为你解决问题（这里只显示相关部分）：

```
提示符> ./paging-policy.py -s 10 -n 3 -c
...
解决中...

访问: 5 未命中 队首->   [br 5] <-队尾 替换:- [br 命中:0 未命中:1]
访问: 4 未命中 队首->[br 5, 4] <-队尾 替换:- [br 命中:0 未命中:2]
访问: 5 命中  队首->[br 5, 4] <-队尾 替换:- [br 命中:1 未命中:2]
```

默认策略是 FIFO，但还有其他可用策略，包括 LRU、MRU、OPT（最佳替换策略，会窥视未来以确定最佳替换项）、UNOPT（最差替换策略）、RAND（随机替换）和 CLOCK（时钟算法）。CLOCK 算法还需要另一个参数 (-b)，指定每页应保留多少位；时钟位越多，算法在确定哪些页面应保留在内存中时就应该表现得越好。

其他选项包括："-C/--cachesize" 用于更改页面缓存的大小；"-m/--maxpage" 是如果模拟器为你生成引用时将使用的最大页码；以及 "-f/--addressfile" 允许你指定一个包含地址的文件，以防你希望从真实应用程序获取跟踪信息，或使用长跟踪信息作为输入。

最后一个有趣的问题：为什么以下这两个例子很有趣？

```
./paging-policy.py -C 3 -a 1,2,3,4,1,2,5,1,2,3,4,5
```

和

```
./paging-policy.py -C 4 -a 1,2,3,4,1,2,5,1,2,3,4,5
```
