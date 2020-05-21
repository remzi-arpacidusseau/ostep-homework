
# Overview

This is the README for `ffs.py`, a simulator of FFS allocation policies. Use it
to study FFS behavior under different file and directory creation scenarios.

The tool is invoked by specifying a command file with the -f flag, which
consists of a series of file create, file delete, and directory create
operations. 

For example, run:

```sh
prompt> ./ffs.py -f in.example1 -c
```

to see the output from the first example in the chapter on how FFS based
allocation works. 

The file `in.example1` consists of the following commands:

```sh
dir /a
dir /b
file /a/c 2
file /a/d 2
file /a/e 2
file /b/f 2
```

This tells the simulator to create two directories (/a and /b) and four files
(/a/c, /a/d, /a/e, and /b/f). The root directory is created by default.

The output of the simulator is the location of the inodes and data blocks of
all extant files and directories. For example, from the run above, we would
end up seeing (with the -c flag on, to show you the results):

```sh
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

This first part of the output shows us various parameters of the simulation,
from the number of FFS cylinder groups that are created, to some policy
details. But the main part of the output is the actual allocation map:

```sh
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

For this instantiation, we have created a file system with 10 groups, each
with 10 inodes and 30 data blocks. Each group just shows the inodes and data
blocks, and how they are allocated. If they are free, a - is shown; otherwise,
a different symbol is shown per file.

If you want to see a mapping of the symbols to file names, you should use
the -M flag:

```sh
prompt> ./ffs.py -f in.example1 -c -M
```

You'll then see a table at the bottom of the output shows the meanings of each symbol:

```sh
symbol  inode#  filename     filetype
/            0  /            directory
a           10  /a           directory
c           11  /a/c           regular
d           12  /a/d           regular
e           13  /a/e           regular
b           20  /b           directory
f           21  /b/f           regular
```

Here, you can see the root directory is represented by the symbol /, the file
/a by the symbol a, and so forth.

Looking at the output, you can thus see a number of interesting things: 
- The root inode is in the first slot of the Group 0's piece of the inode table
- The root data block is found in the first allocated data block (Group 0)
- Directory /a was placed in Group 1, directory /b in Group 2
- The files (inodes and data) for each regular file are found in 
  the same group as their parent inodes (as per FFS)

The rest of the options let you play around with FFS and some minor
variants. They are:

```sh
prompt> ./ffs.py -h
Usage: ffs.py [options]

Options:
  -h, --help            show this help message and exit
  -s SEED, --seed=SEED  the random seed
  -n NUM_GROUPS, --num_groups=NUM_GROUPS
                        number of block groups
  -d BLOCKS_PER_GROUP, --datablocks_per_groups=BLOCKS_PER_GROUP
                        data blocks per group
  -i INODES_PER_GROUP, --inodes_per_group=INODES_PER_GROUP
                        inodes per group
  -L LARGE_FILE_EXCEPTION, --large_file_exception=LARGE_FILE_EXCEPTION
                        0:off, N>0:blocks in group before spreading file to
                        next group
  -f INPUT_FILE, --input_file=INPUT_FILE
                        command file
  -I, --spread_inodes   Instead of putting file inodes in parent dir group,
                        spread them evenly around all groups
  -D, --spread_data     Instead of putting data near inode,
                        spread them evenly around all groups
  -A ALLOCATE_FARAWAY, --allocate_faraway=ALLOCATE_FARAWAY
                        When picking a group, examine this many groups at a
                        time
  -C CONTIG_ALLOCATION_POLICY,
  --contig_allocation_policy=CONTIG_ALLOCATION_POLICY
                        number of contig free blocks needed to alloc
  -T, --show_spans      show file and directory spans
  -M, --show_symbol_map
                        show symbol map
  -B, --show_block_addresses
                        show block addresses alongside groups
  -S, --do_per_file_stats
                        print out detailed inode stats
  -v, --show_file_ops   print out detailed per-op success/failure
  -c, --compute         compute answers for me
```

We'll explore more of these options in the homework.



