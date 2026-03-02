# 概述

在本作业中，你将使用 Linux 上的一个真实工具来查找多线程代码中的问题。这个工具叫做 `helgrind`（可作为 valgrind 调试工具套件的一部分使用）。

关于该工具的详细信息，包括如何下载和安装（如果你的 Linux 系统上还没有的话），请参阅 `http://valgrind.org/docs/manual/hg-manual.htm`。

然后，你将查看一些多线程 C 程序，了解如何使用该工具来调试有问题的线程代码。

首先：下载并安装 `valgrind`和相关的 `helgrind`工具。

然后，输入 `make`来构建所有不同的程序。查看 `Makefile`以了解更多关于其工作原理的详细信息。

之后，你有一些不同的 C 程序需要查看：

- `main-race.c`: 一个简单的竞态条件
- `main-deadlock.c`: 一个简单的死锁
- `main-deadlock-global.c`: 死锁问题的一个解决方案
- `main-signal.c`: 一个简单的子/父线程信号示例
- `main-signal-cv.c`: 通过条件变量实现的更高效信号传递
- `common_threads.h`: 包含包装函数的头文件，使代码能检查错误并更具可读性

通过这些程序，你现在可以回答教科书中的问题。
