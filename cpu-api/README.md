
# Overview

The simulator `fork.py` is a simple tool to show what a process tree
looks like when processes are created and destroyed.

To run it, just:
```sh
prompt> ./fork.py
```

What you'll see then is a list of actions, such as whether a process
calls `fork` to create another process, or whether a process calls
`exit` to stop running.

Each process that is running can have multiple children (or
none). Every process, except the initial process (which we call `a`
here for simplicity), has a single parent. Thus, all processes are
related in a tree, rooted at the initial process. We will call this
tree the `Process Tree` and understanding what it looks like as
processes are created and destroyed is the point of this simple
homework. 

# Simple Example

Here is a simple example:
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

From the output, you can see two things. First, on the right, is the
initial state of the system. As you can see, it contains one process,
`a`. Operating systems often create one or a few initial processes to
get things going; on Unix, for example, the initial process is called
`init` which spawns other processes as the system runs.

Second, on the left, you can see a series of `Action` listings, in
which various actions take place, and then a question is posed about
the state of the process tree is at that point.

To solve, and show all outputs, use the `-c` flag, as follows:
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

As you can see, the expected tree that results (shown left-to-right)
from a particular operation is shown now. After the first action, `a
forks b`, you see a very simple tree, with `a` shown as `b`'s
parent. After a few more forks, a call to `exit` is made by `d`, which
reduces the tree. Finally, `e` is created, and the final tree, with
`a` as parent of `b`, `c`, and `e` (which are considered "siblings"),
as the final state.

In a simplified mode, you can just test yourself by trying to write
down the final process tree, using the `-F` flag:

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

Once again, you can use the `-c` flag to compute the answer and see if
you were right (in this case, you should be, because it's the same
problem!)

# Other Options

A number of other options exist with the `fork` simulator.

You can flip the question around with the `-t` flag, which allows you
to view process tree states and then guess what action must have taken
place.

You can use different random seeds (`-s` flag) or just don't specify
one to get different randomly generated sequences.

You can change what percent of actions are forks (vs exits) with
the `-f` flag.

You can specify specific fork and exit sequences with the `-A`
flag. For example, to have `a` fork `b`, `b` then fork `c`; `c`
exit, and finally, `a` fork `d`, just type (we show `-c` here to solve
the problem, too): 

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

You can only show the final output (and see if you can guess all the
intermediates to get there) with the `-F` flag.

Finally, you can change the printing style of the tree with the `-P`
flag. 









