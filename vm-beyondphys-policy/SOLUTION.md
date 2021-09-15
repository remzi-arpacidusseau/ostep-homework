# Question 1

In notebook.

# Question 2

TODO: Revisit
Increasing cache size from 5 to 6 will allow LRU to approach OPT.

# Question 3

Random stream: 3,4,2,5,0,5,3,0,0,1

Expectations:
* FIFO: hit rate 3/10
* LRU: hit rate 3/10
* OPT: hit rate 4/10

# Question 4

Stream with locality: 1,0,0,1,2,1,1,1,1,3,3,1,0,2,6,5,6,6,8,8,8,8,6,8,8,7,2,3
(generated via local-trace.js);

Both LRU and CLOCK (with 2 bits) performed with a hitrate of around 57%.

Decreasing clock bits to 1 increased CLOCK policy hit rate to 60%.

# Question 5

With memory addresses generated via lackey, I ran the paging-policy program
with the following results:

cache size  hit rate
1           50.02
2           84.80
3           90.28
4           93.72
5           95.13

As seen, even with a cache size less than 5, the hit rate exceeds 90%.

