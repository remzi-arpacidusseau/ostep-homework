
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




