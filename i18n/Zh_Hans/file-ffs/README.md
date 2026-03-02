# 概述

这是 `ffs.py`的 README 文件，一个 FFS（快速文件系统）分配策略的模拟器。使用它来研究不同文件和目录创建场景下的 FFS 行为。

该工具通过用 -f 标志指定一个命令文件来调用，该文件由一系列文件创建、文件删除和目录创建操作组成。

例如，运行：

```
prompt> ./ffs.py -f in.example1 -c
```

查看本章中关于 FFS 分配如何工作的第一个示例的输出。

文件 `in.example1`包含以下命令：

```
dir /a
dir /b
file /a/c 2
file /a/d 2
file /a/e 2
file /b/f 2
```

这告诉模拟器创建两个目录（/a 和 /b）和四个文件（/a/c, /a/d, /a/e 和 /b/f）。根目录默认创建。

模拟器的输出是所有现有文件和目录的 inode 和数据块的位置。例如，从上面的运行中，我们最终会看到（使用 -c 标志显示结果）：

```
prompt> ./ffs.py -f in.example1 -c

num_groups:       10
inodes_per_group: 10
blocks_per_group: 30

free data blocks: 289 (of 300)
free inodes:      93 (of 100)

spread inodes?    False
spread data?      False
contig alloc:     1

      0000000000 0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789 0123456789

group inodes     data
    0 /--------- /--------- ---------- ----------
    1 acde------ accddee--- ---------- ----------
    2 bf-------- bff------- ---------- ----------
    3 ---------- ---------- ---------- ----------
    4 ---------- ---------- ---------- ----------
    5 ---------- ---------- ---------- ----------
    6 ---------- ---------- ---------- ----------
    7 ---------- ---------- ---------- ----------
    8 ---------- ---------- ---------- ----------
    9 ---------- ---------- ---------- ----------

prompt>
```

输出的第一部分向我们展示了模拟的各种参数，从创建的 FFS 柱面组的数量到一些策略细节。但输出的主要部分是实际的分配图：

```
0000000000 0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789 0123456789

group inodes     data
    0 /--------- /--------- ---------- ----------
    1 acde------ accddee--- ---------- ----------
    2 bf-------- bff------- ---------- ----------
    3 ---------- ---------- ---------- ----------
    4 ---------- ---------- ---------- ----------
    5 ---------- ---------- ---------- ----------
    6 ---------- ---------- ---------- ----------
    7 ---------- ---------- ---------- ----------
    8 ---------- ---------- ---------- ----------
    9 ---------- ---------- ---------- ----------
```

对于这个实例，我们创建了一个包含 10 个组的文件系统，每个组有 10 个 inode 和 30 个数据块。每个组只显示 inode 和数据块，以及它们是如何分配的。如果它们是空闲的，则显示 -；否则，每个文件显示不同的符号。

如果你想查看符号到文件名的映射，你应该使用 -M 标志：

```
prompt> ./ffs.py -f in.example1 -c -M
```

然后，你会在输出的底部看到一个表格，显示了每个符号的含义：

```
symbol  inode#  filename     filetype
/            0  /            directory
a           10  /a           directory
c           11  /a/c           regular
d           12  /a/d           regular
e           13  /a/e           regular
b           20  /b           directory
f           21  /b/f           regular
```

在这里，你可以看到根目录由符号 / 表示，文件 /a 由符号 a 表示，依此类推。

查看输出，你可以看到许多有趣的东西：

- 根 inode 在第 0 组的 inode 表的第一个槽位中
- 根数据块在第一个分配的数据块（第 0 组）中
- 目录 /a 被放置在第 1 组，目录 /b 在第 2 组
- 每个常规文件的文件（inode 和数据）与其父目录的 inode 位于同一组中（根据 FFS 规则）

其余选项让你可以试验 FFS 及其一些微小变体。它们是：

```
prompt> ./ffs.py -h
Usage: ffs.py [options]

Options:
  -h, --help            显示此帮助信息并退出
  -s SEED, --seed=SEED  随机种子
  -n NUM_GROUPS, --num_groups=NUM_GROUPS
                        块组的数量
  -d BLOCKS_PER_GROUP, --datablocks_per_groups=BLOCKS_PER_GROUP
                        每组的数据块数
  -i INODES_PER_GROUP, --inodes_per_group=INODES_PER_GROUP
                        每组的 inode 数
  -L LARGE_FILE_EXCEPTION, --large_file_exception=LARGE_FILE_EXCEPTION
                        0:关闭，N>0:组中的块数，达到此数后文件将扩展到下一个组
  -f INPUT_FILE, --input_file=INPUT_FILE
                        命令文件
  -I, --spread_inodes   将文件 inode 均匀分布到所有组中，而不是放在父目录所在的组
  -D, --spread_data     将数据块均匀分布到所有组中，而不是放在 inode 附近
  -A ALLOCATE_FARAWAY, --allocate_faraway=ALLOCATE_FARAWAY
                        选择组时，每次检查这么多组
  -C CONTIG_ALLOCATION_POLICY,
  --contig_allocation_policy=CONTIG_ALLOCATION_POLICY
                        分配所需的连续空闲块数
  -T, --show_spans      显示文件和目录的跨度
  -M, --show_symbol_map
                        显示符号映射
  -B, --show_block_addresses
                        在组旁边显示块地址
  -S, --do_per_file_stats
                        打印详细的 inode 统计信息
  -v, --show_file_ops   打印每个操作的详细成功/失败信息
  -c, --compute         为我计算答案
```

我们将在作业中探索更多这些选项。
