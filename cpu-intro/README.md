
# Overview

This program, called process-run.py, allows you to see how the state of a
process state changes as it runs on a CPU. As described in the chapter,
processes can be in a few different states:

```sh
RUNNING - the process is using the CPU right now
READY   - the process could be using the CPU right now
          but (alas) some other process is
BLOCKED - the process is waiting on I/O
          (e.g., it issued a request to a disk)
DONE    - the process is finished executing
```

In this homework, we'll see how these process states change as a program
runs, and thus learn a little bit better how these things work.

To run the program and get its options, do this:

```sh
prompt> ./process-run.py -h
```

If this doesn't work, type `python` before the command, like this:

```sh
prompt> python process-run.py -h
```

What you should see is this:

```sh
Usage: process-run.py [options]

Options:
  -h, --help            show this help message and exit
  -s SEED, --seed=SEED  the random seed
  -l PROCESS_LIST, --processlist=PROCESS_LIST
                        a comma-separated list of processes to run, in the
                        form X1:Y1,X2:Y2,... where X is the number of
                        instructions that process should run, and Y the
                        chances (from 0 to 100) that an instruction will use
                        the CPU or issue an IO
  -L IO_LENGTH, --iolength=IO_LENGTH
                        how long an IO takes
  -S PROCESS_SWITCH_BEHAVIOR, --switch=PROCESS_SWITCH_BEHAVIOR
                        when to switch between processes: SWITCH_ON_IO,
                        SWITCH_ON_END
  -I IO_DONE_BEHAVIOR, --iodone=IO_DONE_BEHAVIOR
                        type of behavior when IO ends: IO_RUN_LATER,
                        IO_RUN_IMMEDIATE
  -c                    compute answers for me
  -p, --printstats      print statistics at end; only useful with -c flag
                        (otherwise stats are not printed)
```

The most important option to understand is the PROCESS_LIST (as specified by
the -l or --processlist flags) which specifies exactly what each running
program (or 'process') will do. A process consists of instructions, and each
instruction can just do one of two things:
- use the CPU
- issue an IO (and wait for it to complete)

When a process uses the CPU (and does no IO at all), it should simply
alternate between RUNNING on the CPU or being READY to run. For example, here
is a simple run that just has one program being run, and that program only
uses the CPU (it does no IO).

```sh
prompt> ./process-run.py -l 5:100
Produce a trace of what would happen when you run these processes:
Process 0
  cpu
  cpu
  cpu
  cpu
  cpu

Important behaviors:
  System will switch when the current process is FINISHED or ISSUES AN IO
  After IOs, the process issuing the IO will run LATER (when it is its turn)

prompt>
```

Here, the process we specified is "5:100" which means it should consist of 5
instructions, and the chances that each instruction is a CPU instruction are
100%.

You can see what happens to the process by using the -c flag, which computes the
answers for you:

```sh
prompt> ./process-run.py -l 5:100 -c
Time     PID: 0        CPU        IOs
  1     RUN:cpu          1
  2     RUN:cpu          1
  3     RUN:cpu          1
  4     RUN:cpu          1
  5     RUN:cpu          1
```

This result is not too interesting: the process is simple in the RUN state and
then finishes, using the CPU the whole time and thus keeping the CPU busy the
entire run, and not doing any I/Os.

Let's make it slightly more complex by running two processes:

```sh
prompt> ./process-run.py -l 5:100,5:100
Produce a trace of what would happen when you run these processes:
Process 0
  cpu
  cpu
  cpu
  cpu
  cpu

Process 1
  cpu
  cpu
  cpu
  cpu
  cpu

Important behaviors:
  Scheduler will switch when the current process is FINISHED or ISSUES AN IO
  After IOs, the process issuing the IO will run LATER (when it is its turn)
```

In this case, two different processes run, each again just using the CPU. What
happens when the operating system runs them? Let's find out:

```sh
prompt> ./process-run.py -l 5:100,5:100 -c
Time     PID: 0     PID: 1        CPU        IOs
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

As you can see above, first the process with "process ID" (or "PID") 0 runs,
while process 1 is READY to run but just waits until 0 is done. When 0 is
finished, it moves to the DONE state, while 1 runs. When 1 finishes, the trace
is done.

Let's look at one more example before getting to some questions. In this
example, the process just issues I/O requests. We specify here that I/Os take 5
time units to complete with the flag -L.

```sh
prompt> ./process-run.py -l 3:0 -L 5
Produce a trace of what would happen when you run these processes:
Process 0
  io
  io_done
  io
  io_done
  io
  io_done

Important behaviors:
  System will switch when the current process is FINISHED or ISSUES AN IO
  After IOs, the process issuing the IO will run LATER (when it is its turn)
```

What do you think the execution trace will look like? Let's find out:

```sh
prompt> ./process-run.py -l 3:0 -L 5 -c
Time    PID: 0       CPU       IOs
  1         RUN:io             1
  2        BLOCKED                           1
  3        BLOCKED                           1
  4        BLOCKED                           1
  5        BLOCKED                           1
  6        BLOCKED                           1
  7*   RUN:io_done             1
  8         RUN:io             1
  9        BLOCKED                           1
 10        BLOCKED                           1
 11        BLOCKED                           1
 12        BLOCKED                           1
 13        BLOCKED                           1
 14*   RUN:io_done             1
 15         RUN:io             1
 16        BLOCKED                           1
 17        BLOCKED                           1
 18        BLOCKED                           1
 19        BLOCKED                           1
 20        BLOCKED                           1
 21*   RUN:io_done             1
```

As you can see, the program just issues three I/Os. When each I/O is issued,
the process moves to a BLOCKED state, and while the device is busy servicing
the I/O, the CPU is idle.

To handle the completion of the I/O, one more CPU action takes place. Note
that a single instruction to handle I/O initiation and completion is not
particularly realistic, but just used here for simplicity.

Let's print some stats (run the same command as above, but with the -p flag)
to see some overall behaviors:

```sh
Stats: Total Time 21
Stats: CPU Busy 6 (28.57%)
Stats: IO Busy  15 (71.43%)
```

As you can see, the trace took 21 clock ticks to run, but the CPU was
busy less than 30% of the time. The I/O device, on the other hand, was
quite busy. In general, we'd like to keep all the devices busy, as
that is a better use of resources.

There are a few other important flags:
```sh
  -s SEED, --seed=SEED  the random seed
    this gives you way to create a bunch of different jobs randomly

  -L IO_LENGTH, --iolength=IO_LENGTH
    this determines how long IOs take to complete (default is 5 ticks)

  -S PROCESS_SWITCH_BEHAVIOR, --switch=PROCESS_SWITCH_BEHAVIOR
                        when to switch between processes: SWITCH_ON_IO, SWITCH_ON_END
    this determines when we switch to another process:
    - SWITCH_ON_IO, the system will switch when a process issues an IO
    - SWITCH_ON_END, the system will only switch when the current process is done

  -I IO_DONE_BEHAVIOR, --iodone=IO_DONE_BEHAVIOR
                        type of behavior when IO ends: IO_RUN_LATER, IO_RUN_IMMEDIATE
    this determines when a process runs after it issues an IO:
    - IO_RUN_IMMEDIATE: switch to this process right now
    - IO_RUN_LATER: switch to this process when it is natural to
      (e.g., depending on process-switching behavior)
```

Now go answer the questions at the back of the chapter to learn more, please.

James' Homework:
Only wrong answers are specificed, otherwise I got them right :^)

1. python3 ./process-run.py -l 5:100,5:100
CPU Utilization?
- 100%

2. python3 ./process-run.py -l 4:100,1:0 (implied wait of 5)
Total time?
cpu x 4 = 4
        +
I/O x 1 = 1
        +
Wait x 5 = 5
        +
I/O done x 1 = 1

        = 4 + 1 + 5 + 1 = 11

3. python3 ./process-run.py -l 1:0,4:100 (implied wait of 5)

1.    I/O   ready   cpu:1
2.    Blocked   running   cpu:1    I/O: 1
3.    Blocked   running   cpu:1    I/O: 1
4.    Blocked   running   cpu:1    I/O: 1
5.    Blocked   running   cpu:1    I/O: 1
6.    Blocked   DONE      cpu:0    I/O: 1
7.    I/O_done  DONE      cpu:1

Time: 7

4. python3 ./process-run.py -l 1:0,4:100 -S SWITCH_ON_END (will wait until I/O is complete to switch process) (implied wait of 5)

1.    I/O   ready   cpu:1 I/O: 0
2.    Blocked   ready      cpu:0    I/O: 1
3.    Blocked   ready      cpu:0    I/O: 1
4.    Blocked   ready      cpu:0    I/O: 1
5.    Blocked   ready      cpu:0    I/O: 1
6.    Blocked   ready      cpu:0    I/O: 1
7.    I/O_done  ready      cpu:1    I/O: 0
8.    DONE      running    cpu:1    I/0: 0
9.    DONE      running    cpu:1    I/0: 0
10.   DONE      running    cpu:1    I/0: 0
11.   DONE      running    cpu:1    I/0: 0

5. python3 ./process-run.py -l 1:0,4:100 -S SWITCH_ON_IO
(Will switch whenever another process is waiting) (implied wait of 5)

1.    I/O       ready        cpu:1    I/O: 0
2.    Blocked   running      cpu:1    I/O: 1
3.    Blocked   running      cpu:1    I/O: 1
4.    Blocked   running      cpu:1    I/O: 1
5.    Blocked   running      cpu:1    I/O: 1
6.    Blocked   DONE         cpu:0    I/O: 1
7.    I/O_done  DONE         cpu:1    I/O: 0

6. python3 ./process-run.py -l 3:0,5:100,5:100,5:100 -S SWITCH_ON_IO -I IO_RUN_LATER
(Will switch whenever another process is waiting) (After an IO, other processes will finish
before switching back to finished IO) (implied wait of 5)

My Guess: wrong
Forgot the second and third I/O runs, but they would have been appended to the end by my logic.
In reality, the first I/O_done wouldn't be executed until after PID 3 is finished, meaning
the processes are executed all the way down the line before returning to the first one (PID 0).
I wonder if process scheduling handles this explicity in the future.
1.    I/O       ready     ready   ready   cpu:1    I/O: 0
2.    Blocked   running   ready   ready   cpu:1    I/O: 1
3.    Blocked   running   ready   ready   cpu:1    I/O: 1
4.    Blocked   running   ready   ready   cpu:1    I/O: 1
5.    Blocked   running   ready   ready   cpu:1    I/O: 1
6.    Blocked   running   ready   ready   cpu:1    I/O: 1
7.    I/O_done  DONE      ready   ready   cpu:1    I/O: 0
8.    DONE      DONE      running ready   cpu:1    I/O: 0
9.    DONE      DONE      running ready   cpu:1    I/O: 0
10.   DONE      DONE      running ready   cpu:1    I/O: 0
11.   DONE      DONE      running ready   cpu:1    I/O: 0
12.   DONE      DONE      running ready   cpu:1    I/O: 0
13.   DONE      DONE      DONE    running cpu:1    I/O: 0
14.   DONE      DONE      DONE    running cpu:1    I/O: 0
15.   DONE      DONE      DONE    running cpu:1    I/O: 0
16.   DONE      DONE      DONE    running cpu:1    I/O: 0
17.   DONE      DONE      DONE    running cpu:1    I/O: 0

System resources are used inefficiently because the second and third I/O processes
are run without other processes to run during the blocked period. I suspect if you
switch back on I/O finish to start a new I/O, it is much more efficient because then
you can go back to the CPU processes in the mean time.

7. python3 ./process-run.py -l 3:0,5:100,5:100,5:100 -S SWITCH_ON_IO -I IO_RUN_IMMEDIATE
(Will switch whenever another process is waiting) (Will switch back
to an I/O when it finishes.) (implied wait of 5)

1.    I/O       ready     ready   ready   cpu:1    I/O: 0
2.    Blocked   running   ready   ready   cpu:1    I/O: 1
3.    Blocked   running   ready   ready   cpu:1    I/O: 1
4.    Blocked   running   ready   ready   cpu:1    I/O: 1
5.    Blocked   running   ready   ready   cpu:1    I/O: 1
6.    Blocked   running   ready   ready   cpu:1    I/O: 1
7.    I/O_done  DONE      ready   ready   cpu:1    I/O: 0
8.    I/O       DONE      ready   ready   cpu:1    I/O: 0
9.    Blocked   DONE      running ready   cpu:1    I/O: 1
10.   Blocked   DONE      running ready   cpu:1    I/O: 1
11.   Blocked   DONE      running ready   cpu:1    I/O: 1
12.   Blocked   DONE      running ready   cpu:1    I/O: 1
13.   Blocked   DONE      running ready   cpu:1    I/O: 1
14.   I/O_done  DONE      DONE    ready   cpu:1    I/O: 0
15.   I/O       DONE      DONE    ready   cpu:1    I/O: 0
16.   Blocked   DONE      DONE    running cpu:1    I/O: 1
17.   Blocked   DONE      DONE    running cpu:1    I/O: 1
18.   Blocked   DONE      DONE    running cpu:1    I/O: 1
19.   Blocked   DONE      DONE    running cpu:1    I/O: 1
20.   Blocked   DONE      DONE    running cpu:1    I/O: 1
21.   I/O_done  DONE      DONE    DONE    cpu:1    I/O: 0

This is efficient because it allows the I/O process to start a new I/O
asap, maximizing the amount of time an I/O is running at the same time
as a CPU.

8. python3 ./process-run.py -s 1 -l 3:50,3:50 (random seed of 1 for chance jobs)

Processes:
Process 0
  cpu
  io
  io_done
  io
  io_done

Process 1
  cpu
  cpu
  cpu

1.  running   ready   cpu:1   I/O:0
2.  I/O       ready   cpu:1   I/O:0
3.  blocked   running cpu:1   I/O:1
4.  blocked   running cpu:1   I/O:1
5.  blocked   running cpu:1   I/O:1
6.  blocked   DONE    cpu:0   I/O:1
7.  blocked   DONE    cpu:0   I/O:1
8.  I/O_done  DONE    cpu:1   I/O:0
9.  I/O       DONE    cpu:1   I/O:0
10. blocked   DONE    cpu:0   I/O:1
11. blocked   DONE    cpu:0   I/O:1
12. blocked   DONE    cpu:0   I/O:1
13. blocked   DONE    cpu:0   I/O:1
14. blocked   DONE    cpu:0   I/O:1
15. I/O_done  DONE    cpu:1   I/O:0