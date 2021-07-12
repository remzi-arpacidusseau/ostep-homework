# Question 2

### Figure 8.2
3 queus. 1 job. 10ms quantum. 0 maxIO

### Figure 8.3
3 queue. 2 jobs. 10ms quantum. 0 maxIO.
job list: 0,200,0:100,20,0

### Figure 8.4
3 queues. 2 jobs. 10ms quantum. 0 maxIO.
job list: 0,200,0:50,20,1

### Figure 8.5 (Left)
3 queues. 3 jobs. 10ms quantum. 0 maxIO
job list: 0,10,200:100,100,1:100,100,1

### Figure 8.5 (Right)
3 queues. 3 jobs. 10ms quantum. 0 maxIO.
job list: 0,10,200:100,100,1:100,100,1
20 boost.

### Figure 8.7
3 queues.
job list: 0,150,0:0,150,0
quanta list: 10,20,40

# Question 3

To behave like a round robin scheduler, use a single queue.

# Question 4

To achieve 99% of the CPU, I set two jobs with an IO time of 1 and a quantum time
of 100.
The first job runs without IO. The second job runs with IO every 99 ticks.
This way, after the first job runs 100 ticks and moves to priority 0,
the second job runs for 99 ticks, issues a 1 tick IO (during which job 0 runs for
1 tick), and then resumes for another 99 ticks.

# Question 5

I think boost will need to occur every 200ms to guarantee a single,
long running job achieves at least 5% CPU. However, this relies on
the fact that on boost, any jobs not yet run in the top priority queue
are scheduled AFTER the boosted jobs.
That is because we need the job to run every 1 out of 20 intervals. So if there
are more than 20 jobs, it won't matter how often the boost occurs because
each the interval will be greater tha 1/20.
