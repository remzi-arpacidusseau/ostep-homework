
# 概述: `fork.py`

模拟器 `fork.py` 是一个简单工具，用于展示进程在创建和销毁时进程树的形态。

要运行它，只需：
```sh
prompt> ./fork.py
```

此时您将看到一系列操作列表，例如进程是否调用`fork`创建子进程，或是否调用`exit`终止运行。每个运行中的进程可拥有多个子进程（或没有子进程）。除初始进程（为简化起见，我们称之为进程）外，每个进程都拥有唯一的父进程。因此所有进程构成以初始进程为根的树状结构。我们将此树称为进程树，理解进程在创建与销毁过程中的形态变化正是本简易作业的核心要义。

# 简单示例

以下是一个简单的示例：
```sh
prompt> ./fork.py -s 4

                           Process Tree:
                               a
Action: a forks b
Process Tree?
Action: a forks c
Process Tree?
Action: b forks d
Process Tree?
Action: d EXITS
Process Tree?
Action: a forks e
Process Tree?
```

从输出中，你可以看到两点。首先，右侧显示的是系统的初始状态。如你所见，它包含一个进程 `a` 。操作系统通常会创建一个或几个初始进程来启动系统；例如在Unix系统中，初始进程名为 `init`，它会在系统运行时生成其他进程。

其次，在左侧可见一系列操作列表，其中描述了各种操作的执行过程，随后提出关于进程树在该时刻状态的问题。为求解并显示所有输出结果，请使用 `-c` 参数，如下所示：
```sh
prompt> ./fork.py -s 4 -c                                                                       +100

                           Process Tree:
                               a

Action: a forks b
                               a
                               └── b
Action: a forks c
                               a
                               ├── b
                               └── c
Action: b forks d
                               a
                               ├── b
                               │   └── d
                               └── c
Action: d EXITS
                               a
                               ├── b
                               └── c
Action: a forks e
                               a
                               ├── b
                               ├── c
                               └── e
prompt>
```

如您所见，当前显示的是特定操作产生的预期树（从左至右呈现）。首次操作后，`a` 分叉出 `b` ，此时可见一棵极为简单的树，其中 `a` 作为 `b` 的父节点。经过数次分叉后，`d` 调用 `exit` 函数，导致树结构缩减。最终生成节点e，最终状态为：`a` 作为 `b`、`c`和 `e`（视为“兄弟节点”）的父节点，构成最终树形结构。在简化模式下，你可通过 `-F` 参数尝试手动绘制最终进程树进行自测：

```sh
prompt> ./fork.py -s 4 -F
                           Process Tree:
                               a

Action: a forks b
Action: a forks c
Action: b forks d
Action: d EXITS
Action: a forks e

                        Final Process Tree?
```

再次提醒，你可以使用 `-c` 参数计算答案并验证是否正确（这次应该没错，因为这是同一道题！）

# 其他选项

分叉模拟器还提供了其他多种选项。

你可以通过 `-t` 参数反向分析问题，该参数允许你查看进程树状态，从而推测可能发生的操作。

你可以使用不同的随机种子（`-s` 标志），或直接不指定种子即可获得不同的随机生成的序列。

你可以通过 `-f` 标志调整分叉操作（相对于退出操作）所占的比例。

你可以使用 `-A` 标志指定特定的 fork 和退出序列。例如，要实现 a fork b，b 随后 fork c；c 退出，最后 fork d 的流程，只需输入（此处同时展示 -c 选项以解决该问题）： 

```sh
prompt> ./fork.py -A a+b,b+c,c-,a+d -c

                           Process Tree:
                               a

Action: a forks b
                               a
                               └── b
Action: b forks c
                               a
                               └── b
                                   └── c
Action: c EXITS
                               a
                               └── b
Action: a forks d
                               a
                               ├── b
                               └── d
```

你仅能通过 `-F` 标志展示最终输出结果（并尝试推测所有中间步骤以达成该结果）。

最后，你可以使用 `-P` 标志更改树的打印样式。
