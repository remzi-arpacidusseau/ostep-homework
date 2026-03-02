# 作业

每章末尾都附有若干问题；我们称之为“作业”，因为你应该在家中完成这些“工作”。明白吗？这是本书的一项创新之处。

作业能帮助你巩固各章节所学知识。许多作业基于运行模拟器完成，这些模拟器能复现操作系统的某些功能。例如磁盘调度模拟器可帮助理解不同磁盘调度算法的工作原理。另一些作业则是简短的编程练习，让你探索真实系统的运作机制。

模拟器的基本原理很简单：下文列出的每个模拟器都支持生成无限数量的问题并获取解法。通常可通过不同随机种子生成不同问题；使用`-c`参数可自动计算答案（当然，这需要你在尝试自行计算后使用！）。

每项作业均附有README文件说明操作步骤。此前这些内容曾直接编入章节，但导致篇幅过长。现仅保留需通过模拟器解答的问题，具体运行细节均详见README文件。

因此你的任务是：阅读章节内容，查看章末问题，并通过完成作业尝试解答。部分作业需要使用模拟器（Python编写），可通过下方链接获取；另一些则要求你编写代码，此时建议先阅读相关README文件；还有些作业需要其他操作，例如编写C代码完成特定任务。

要使用这些功能，最好的做法是克隆作业。例如：
```sh
prompt> git clone https://github.com/remzi-arpacidusseau/ostep-homework/
prompt> cd file-disks
prompt> ./disk.py -h
```

# 介绍

章节 | 你要做的 
--------|-----------
[操作系统介绍](http://www.cs.wisc.edu/~remzi/OSTEP/intro.pdf) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | 还没有作业 (目前来说) 

# 虚拟化

章节 | 你要做的 
--------|-----------
[抽象：进程](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf) | 运行 [process-运行.py](cpu-intro) 
[插叙：进程API](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-api.pdf) | 运行 [fork.py](cpu-api) 然后写点代码 
[机制：受限直接执行](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf) | 写点代码 
[进程调度：介绍](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf) | 运行 [scheduler.py](cpu-sched) 
[调度：多级反馈队列](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)	| 运行 [mlfq.py](cpu-sched-mlfq) 
[调度：比例份额](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-sched-lottery.pdf) | 运行 [lottery.py](cpu-sched-lottery) 
[多处理器调度](http://www.cs.wisc.edu/~remzi/OSTEP/cpu-sched-multi.pdf) | 运行 [multi.py](cpu-sched-multi) 
[抽象：地址空间](http://www.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf) | 写点代码 
[插叙：内存操作API](http://www.cs.wisc.edu/~remzi/OSTEP/vm-api.pdf) | 写点代码 
[机制：地址转换](http://www.cs.wisc.edu/~remzi/OSTEP/vm-mechanism.pdf) | 运行 [relocation.py](vm-mechanism) 
[分段](http://www.cs.wisc.edu/~remzi/OSTEP/vm-segmentation.pdf) | 运行 [segmentation.py](vm-segmentation) 
[空闲空间管理](http://www.cs.wisc.edu/~remzi/OSTEP/vm-freespace.pdf) | 运行 [malloc.py](vm-freespace) 
[分页：介绍](http://www.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf) | 运行 [paging-linear-translate.py](vm-paging) 
[分页：快速地址转换（TLB）](http://www.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf) | 写点代码 
[分页：较小的表](http://www.cs.wisc.edu/~remzi/OSTEP/vm-smalltables.pdf) | 运行 [paging-multilevel-translate.py](vm-smalltables) 
[超越物理内存：机制](http://www.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf) | 运行 [mem.c](vm-beyondphys) 
[超越物理内存：策略](http://www.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf) | 运行 [paging-policy.py](vm-beyondphys-policy) 
[VAX/VMS虚拟内存系统](http://www.cs.wisc.edu/~remzi/OSTEP/vm-complete.pdf) | 还没有作业 (目前来说) 

# 并发

章节 | 你要做的 
--------|-----------
[并发：介绍](http://www.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf) | 运行 [x86.py](threads-intro) 
[插叙：线程API](http://www.cs.wisc.edu/~remzi/OSTEP/threads-api.pdf)	| 运行 [some C code](threads-api) 
[锁](http://www.cs.wisc.edu/~remzi/OSTEP/threads-locks.pdf)	| 运行 [x86.py](threads-locks) 
[基于锁的并发数据结构](http://www.cs.wisc.edu/~remzi/OSTEP/threads-locks-usage.pdf) | 写点代码 
[条件变量](http://www.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf) | 运行 [some C code](threads-cv) 
[信号量](http://www.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf) | 阅读，然后写 [some code](threads-sema) 
[常见并发问题](http://www.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf) | 运行 [some C code](threads-bugs) 
[基于事件的并发](http://www.cs.wisc.edu/~remzi/OSTEP/threads-events.pdf) | 写点代码 

# 持久性

章节 | 你要做的 
--------|-----------
[I/O 设备](http://www.cs.wisc.edu/~remzi/OSTEP/file-devices.pdf) | 还没有作业 (目前来说) 
[硬盘驱动器](http://www.cs.wisc.edu/~remzi/OSTEP/file-disks.pdf) | 运行 [disk.py](file-disks) 
[廉价冗余磁盘阵列（RAID）](http://www.cs.wisc.edu/~remzi/OSTEP/file-raid.pdf) | 运行 [raid.py](file-raid) 
[插叙：文件和目录](http://www.cs.wisc.edu/~remzi/OSTEP/file-intro.pdf) | 写点代码 
[文件系统实现](http://www.cs.wisc.edu/~remzi/OSTEP/file-implementation.pdf) | 运行 [vsfs.py](file-implementation) 
[局部性和快速文件系统](http://www.cs.wisc.edu/~remzi/OSTEP/file-ffs.pdf) | 运行 [ffs.py](file-ffs) 
[崩溃一致性：FSCK和日志](http://www.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf) | 运行 [fsck.py](file-journaling) 
[日志结构文件系统](http://www.cs.wisc.edu/~remzi/OSTEP/file-lfs.pdf) | 运行 [lfs.py](file-lfs) 
[固态硬盘](http://www.cs.wisc.edu/~remzi/OSTEP/file-ssd.pdf) | 运行 [ssd.py](file-ssd) 
[数据完整性和保护](http://www.cs.wisc.edu/~remzi/OSTEP/file-integrity.pdf) | 运行 [checksum.py](file-integrity) 然后写点代码 
[分布式系统](http://www.cs.wisc.edu/~remzi/OSTEP/dist-intro.pdf) | 写点代码 
[Sun的网络文件系统（NFS）](http://www.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf) | 写点分析代码 
[Andrew文件系统（AFS）](http://www.cs.wisc.edu/~remzi/OSTEP/dist-afs.pdf) | 运行 [afs.py](dist-afs) 
