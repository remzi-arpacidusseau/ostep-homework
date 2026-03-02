# 概述

这个名为 process-run.py 的程序，可以让你观察进程状态在 CPU 上运行时如何变化。如章节所述，进程可以处于几种不同的状态：

```
运行 (RUNNING) - 进程当前正在使用 CPU
就绪 (READY)   - 进程本可以立即使用 CPU
                  但（唉）其他进程正在使用
阻塞 (BLOCKED) - 进程正在等待 I/O
                  (例如，它向磁盘发出了一个请求)
完成 (DONE)    - 进程已执行完毕
```

在这次作业中，我们将看到进程状态如何随程序运行而变化，从而更好地理解其工作原理。

要运行程序并查看其选项，请执行：

```
提示符> ./process-run.py -h
```

如果上述命令无效，请在命令前输入 `python`，如下所示：

```
提示符> python process-run.py -h
```

你将看到如下内容：

```
用法: process-run.py [选项]

选项:
  -h, --help            显示此帮助信息并退出
  -s SEED, --seed=SEED  随机种子
  -l PROCESS_LIST, --processlist=PROCESS_LIST
                        要运行的进程列表，以逗号分隔，格式为 X1:Y1,X2:Y2,...
                        其中 X 是该进程应运行的指令数量，Y 是指令使用 CPU
                        或发出 I/O 的几率（从 0 到 100）
  -L IO_LENGTH, --iolength=IO_LENGTH
                        I/O 操作所需时长
  -S PROCESS_SWITCH_BEHAVIOR, --switch=PROCESS_SWITCH_BEHAVIOR
                        何时在进程间切换: SWITCH_ON_IO, SWITCH_ON_END
  -I IO_DONE_BEHAVIOR, --iodone=IO_DONE_BEHAVIOR
                        I/O 结束时的行为类型: IO_RUN_LATER, IO_RUN_IMMEDIATE
  -c                    为我计算答案
  -p, --printstats     结束时打印统计数据；仅与 -c 标志一起使用
                        （否则不会打印统计信息）
```

最重要的需要理解的选项是 PROCESS_LIST（由 -l 或 --processlist 标志指定），它精确指定了每个运行的程序（或"进程"）将执行的操作。一个进程由一系列指令组成，每条指令只能执行以下两种操作之一：

- 使用 CPU
- 发出 I/O 操作（并等待其完成）

当进程使用 CPU 时（完全不进行 I/O），它应简单地在 CPU 上 RUNNING 和处于可运行的 READY 状态之间交替。例如，下面是一个简单的运行示例，其中只有一个程序在运行，并且该程序仅使用 CPU（不进行任何 I/O）。

```
提示符> ./process-run.py -l 5:100
生成运行这些进程时将发生的跟踪信息：
进程 0
  cpu
  cpu
  cpu
  cpu
  cpu

重要行为：
  当当前进程完成或发出 I/O 时，系统将切换
  I/O 之后，发出 I/O 的进程将在稍后（轮到时）运行

提示符>
```

这里，我们指定的进程是 "5:100"，意味着它应由 5 条指令组成，并且每条指令是 CPU 指令的几率是 100%。

你可以通过使用 -c 标志查看进程发生的情况，该标志会为你计算结果：

```
提示符> ./process-run.py -l 5:100 -c
时间     PID: 0         CPU        IOs
  1     RUN:cpu          1
  2     RUN:cpu          1
  3     RUN:cpu          1
  4     RUN:cpu          1
  5     RUN:cpu          1
```

这个结果并不太有趣：进程简单地从运行状态开始然后结束，一直使用 CPU，从而使 CPU 在整个运行期间保持繁忙，并且不执行任何 I/O 操作。

让我们运行两个进程，使其稍微复杂一些：

```
提示符> ./process-run.py -l 5:100,5:100
生成运行这些进程时将发生的跟踪信息：
进程 0
  cpu
  cpu
  cpu
  cpu
  cpu

进程 1
  cpu
  cpu
  cpu
  cpu
  cpu

重要行为：
  当当前进程完成或发出 I/O 时，调度器将切换
  I/O 之后，发出 I/O 的进程将在稍后（轮到时）运行
```

在这个例子中，两个不同的进程在运行，每个都只使用 CPU。当操作系统运行它们时会发生什么？让我们看看：

```
提示符> ./process-run.py -l 5:100,5:100 -c
时间     PID: 0     PID: 1        CPU        IOs
  1     RUN:cpu      READY          1
  2     RUN:cpu      READY          1
  3     RUN:cpu      READY          1
  4     RUN:cpu      READY          1
  5     RUN:cpu      READY          1
  6        DONE    RUN:cpu          1
  7        DONE    RUN:cpu          1
  8        DONE    RUN:cpu          1
  9        DONE    RUN:cpu          1
 10        DONE    RUN:cpu          1
```

如上所示，首先是"进程 ID"（或"PID"）为 0 的进程运行，而进程 1 处于就绪状态，等待 0 完成。当 0 完成时，它进入完成状态，而 1 开始运行。当 1 完成后，跟踪结束。

在开始回答问题之前，让我们再看一个例子。在这个例子中，进程只发出 I/O 请求。我们通过 -L 标志指定 I/O 操作需要 5 个时间单位来完成。

```
提示符> ./process-run.py -l 3:0 -L 5
生成运行这些进程时将发生的跟踪信息：
进程 0
  io
  io_done
  io
  io_done
  io
  io_done

重要行为：
  当当前进程完成或发出 I/O 时，系统将切换
  I/O 之后，发出 I/O 的进程将在稍后（轮到时）运行
```

你认为执行跟踪会是什么样子？让我们看看：

```
提示符> ./process-run.py -l 3:0 -L 5 -c
时间    PID: 0       CPU       IOs
  1         RUN:io             1
  2        BLOCKED             1
  3        BLOCKED             1
  4        BLOCKED             1
  5        BLOCKED             1
  6        BLOCKED             1
  7*   RUN:io_done             1
  8         RUN:io             1
  9        BLOCKED             1
 10        BLOCKED             1
 11        BLOCKED             1
 12        BLOCKED             1
 13        BLOCKED             1
 14*   RUN:io_done             1
 15         RUN:io             1
 16        BLOCKED             1
 17        BLOCKED             1
 18        BLOCKED             1
 19        BLOCKED             1
 20        BLOCKED             1
 21*   RUN:io_done             1
```

如你所见，程序只发出了三个 I/O 操作。每当发出一个 I/O 时，进程就进入阻塞状态，而在设备忙于处理 I/O 时，CPU 处于空闲状态。

为了处理 I/O 的完成，会再发生一次 CPU 操作。请注意，用一条指令来处理 I/O 的发起和完成并不是特别现实，但这里仅为了简单而使用。

让我们打印一些统计数据（运行与上面相同的命令，但加上 -p 标志）以查看总体行为：

```
统计: 总时间 21
统计: CPU 繁忙 6 (28.57%)
统计: IO 繁忙 15 (71.43%)
```

如你所见，跟踪运行了 21 个时钟滴答，但 CPU 繁忙时间少于 30%。另一方面，I/O 设备相当繁忙。一般来说，我们希望保持所有设备繁忙，因为这样才能更好地利用资源。

还有一些其他重要标志：

```
-s SEED, --seed=SEED  随机种子
    这为你提供了一种随机创建多个不同作业的方法

  -L IO_LENGTH, --iolength=IO_LENGTH
    这决定了 I/O 操作完成所需的时间（默认为 5 个滴答）

  -S PROCESS_SWITCH_BEHAVIOR, --switch=PROCESS_SWITCH_BEHAVIOR
                        何时在进程间切换: SWITCH_ON_IO, SWITCH_ON_END
    这决定了我们何时切换到另一个进程:
    - SWITCH_ON_IO, 系统会在进程发出 I/O 时切换
    - SWITCH_ON_END, 系统只在当前进程完成时才切换

  -I IO_DONE_BEHAVIOR, --iodone=IO_DONE_BEHAVIOR
                        I/O 结束时的行为类型: IO_RUN_LATER, IO_RUN_IMMEDIATE
    这决定了进程发出 I/O 后何时运行:
    - IO_RUN_IMMEDIATE: 立即切换到此进程
    - IO_RUN_LATER: 在自然情况下切换到此进程
      （例如，取决于进程切换行为）
```

现在请去回答章节后面的问题以了解更多。
