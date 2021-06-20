# Question 1

CPU utilization should be 100%. Both processes probability of using CPU is 100%.
When process 1 completes, process 2 will immediately start.
Therefore, the CPU will be utilized 100%.

# Question 2

Both process will take 11 ticks to complete.
The first process requires 4 instructions; all 4 will be CPU instructions
because the probability is set to 100%.
The second process is a single instruction; it will be an IO instruction
becuase the probability is set to 0%.
IO instructions will take 5 tickets by default.
Plus, it will require 2 additional instructions: a CPU instruction to initiate
IO and a CPU instruction when IO is complete.

# Question 3

I'm not sure what the behavior will becasue I don't know what the default
PROCESS_SWITCH_BEHAVIOR is.
If it is SWITCH_ON_IO, then the total time will be 7 ticks. This will be
composed of the 5 ticks of the first processes IO instruction, plus the 2 CPU
instructions the first process must issue to start the IO and handle
completion of IO.
If the default is SWITCH_ON_END, then the total time will still be 11 ticks.
In other words, changing order of the processes won't affect total time.

The total time was 7. That means the default is SWITCH_ON_IO.

# Question 4

The answer was captured in Question 3.
Changing the PROCESS_SWITCH_BEHAVIOR to SWITCH_ON_END will cause total time to
be 11. This is because the second process will not execute until the first
process's IO instructions complete.

# Question 5

I expect the behavior to be the same as occured for question 3. Total time
will be 7. While the IO instructions for process 1 are handled by IO,
the CPU instructions for process 2 can be handled by the CPU. Therefore,
the time to complete process 2 does not add to the total time; process 1
is the long poll.

# Question 6

When each IO instruction is issued by the first process, the the next ready
process will issue 5 CPU instructions. These will be handled by the CPU
while the IO handles the 5 IO instructions. In other words, each IO
instruction will not complete until after each subsequent process completes.
Therefore, IO_RUN_LATER will not cause the processes to be handled differently
than if the setting were IO_RUN_IMMEDIATE.
Therefore this is effective utilization fo resources because the CPU is not idle.

My understanding of IO_RUN_LATER was incorrect. It seems that it causes other READY
processes to run BEFORE returning control to the process which issues the IO.
Therefore, processes 2,3,4 run after process 1 initiates RUN:io.
Control is returned to process 1 after process 4 completes.
So, each IO command takes 7 ticks to complete (21 total).
The other 3 processes take 15 tickets to complete.
However, the 5 CPU instructions initiated by process 2 are handled while waiting
for the first IO command initiated by process 1.
Therefore, total time is 31 ticks.
This is not effective utilization of resources. The CPU is idle while the last
two IO commands initiated by process 1 execute. Plus, IO is idle during the CPU
instructions initiated by processes 3 and 4.

# Question 7

The described simulation will execute as I initially described for Question 6.
As each command is executed by process 1, the CPU instructions of processes
2,3,4 can be executed by the CPU while waiting for the IO command to complete.
This will yield a more effective utilization of resources because no resource
is idle.
Additionally, running a process that just completed an IO is a good idea because
it is likely that process will initiate another IO.

# Question 8

For the first randomly generated processes, I think all 3 instructions of
process 1 will be completed while waiting for process 0's first IO instruction
to complete.

The second randomly generated processes: The first CPU command of process 1 will
complete while waiting for the first IO command of process 0.
Then, process 1's two IO commands will not execute until after process 0 completes
its final CPU instruction, at which point process 0 will complete.

I was wrong for the second process. While process 0 is waiting for its IO to
complete, process 1 can start its own IO command. The commands are staggered,
so the CPU is idle when each process's IO command completes. Therefore,
each process can immediately initiate the next IO instruction without
needing to wait.

Using IO_RUN_LATER for the first command should have no effect because the
3 instructions process 1 initiates will complete before process 0's
IO instruction completes.

Using IO_RUN_LATER for the second command should have no effect either because 
neither command is ready when the other completes an IO instruction.

Using SWITCH_ON_END will cause first simulation ro take longer to run.
This is because process 1 won't gain control until after process 0 completes.
Therefore, process 1's CPU instructions will not execute while waiting on
process 0's IO instructions.

Using SWITCH_ON_END will cause the second simulation to take longer for the same
reason as above.
