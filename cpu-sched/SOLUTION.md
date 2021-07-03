# Question 1

## SJF

Turnaround
* 0: 200
* 1: 400
* 2: 600
Avg: 400

Response
* 0: 0
* 1: 200
* 2: 400
Avg: 200

Wait
* 0: 0
* 1: 200
* 2: 400
Avg: 200

## FIFO

Same

# Question 2

## SJF

Response
* 0: 0
* 1: 100
* 2: 300
Avg: 133.33

Turnaround
* 0: 100
* 1: 300
* 2: 600
Avg: 333.33

Wait
* 0: 0
* 1: 100
* 2: 300
Avg: 133.33

## FIFO

Same

# Question 3
`
Response
* 0: 0
* 1: 1
* 2: 2
Avg: 1 

Turnaround
* 0: 298 
* 1: 299 + 200 = 499 
* 2: 500 + 100 = 600 
Avg: 465.67

Wait
* 0: 198 
* 1: 199 + 100 = 299 
* 2: 200 + 100 = 300
Avg: 265.67 

# Question 4

SJF and FIFO deliver the same turnaround times if the jobs are "created" in 
weakly increasing order.

# Question 5

SJF and RR deliver the same response times for workloads whose job lengths
(excluding the last job's length) are less then or equal to the 
quantum length.

# Question 6

As job lengths increase for SJF workloads, we should see an increase in response 
time averages. The first job will not see an increase. The increase in response
time will be a function of the job's position in the job list: the larger the
index in the job list, the larger the increase will be to the job's response
time.

Example:
Starting with job list 5,10,15 and increasing by 10, the response times are:

5,10,15
0,5,15

15,20,25
0,15,35

25,30,35
0,25,55

# Question 7

As quantum lengths increase, the average response times increase.

The worst response time will be:
worst_response_time = min(ql, jl[0]) + min(ql, jl[1]) + ... + min(ql, jl[n-1])
