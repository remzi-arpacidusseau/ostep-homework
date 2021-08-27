# Question 1

`gettimeofday()` is precise to a microsecond.
In order to time an operation precisely, the
operation must take equal to or more than
one microsecond.
Or, we can time 1000 operations that each
take 1 or more nanoseconds.
From initial tests, the average memory access
takes > 3 ns.
Therefore, we can safely assume that
1000 iterations of each page access should be
timed correctly.
However, if the average memory access
becomes closer to 1, this may indicate an issue
with precision.

Note: It might be simple as saying
total time must be greater than 1us. If less
than 1us, then we have precision error and
averages will not be correct.
Thus, if each operation takes 1ns, we must have
at least 1000 operations.

# Question 2

Completed.

# Question 3

Accurate measurements are achieved starting
at 1000 iterations:
```
num_pages: 1, total_usec: 5, nsec_per_access: 5.000000
num_pages: 2, total_usec: 7, nsec_per_access: 3.500000
num_pages: 4, total_usec: 14, nsec_per_access: 3.500000
num_pages: 8, total_usec: 26, nsec_per_access: 3.250000
num_pages: 16, total_usec: 188, nsec_per_access: 11.750000
num_pages: 32, total_usec: 341, nsec_per_access: 10.656250
...
```

# Question 4

TODO: graph

# Question 5

Using `volatile` per
https://stackoverflow.com/a/2219839.

# Question 6

If don't pin thread to a CPU core, then
the time per access will be larger
because the TLB is tied to a core.
Therefore, when switching cores,
the TLB will be empty in the enw core.
Overall,this will led to larger percentage
of TLB misses. And therefore larger overall
time.

# Question 7

This will affect timing because the
time spent initializing the array will
contirbute to overall time. Therefore,
time per access will be greater.

One way to avoid is to initialize the array 
before starting the timer and touch each array
element.
