# Question 1

Predictions documented in notebook.

Over time, the free list size grows as the memory segments become divided.
A natural side effect of this division is the median size of segments
decreases. This can cascade if Alloc requests are made and there are no
segments with the exact requested size.

# Question 2

With the `WORST` policy, the median free memory
segment size is larger than with the `BEST` policy.

However, the maximum memory chunk size is smaller with `WORST` policy.

# Question 3

Using `FIRST` policy, in this case, is equivalent to `BEST` policy.

However, compared to `WORST` and `BEST` policies, `FIRST` will perform
faster searches because it searches fewer memory chunks.

But, this could lead to more fragmentation that `BEST` policy does. 
For example, if searching for memory size x, and there exists
a segment with size x, `BEST` will return that segment.
But, with `FIRST`, if there exists a segment of size x+1 that
is ordered before segment of size x, then `FIRST` will divide this segment
into an additional segment.

# Question 4

Because both `WORST` and `BEST` policies require iterating through all
memory segments, the ordering does not affect search performance.

With `FIRST` policy, ordering does affect search performance.
In the simulation, with `SIZESORT-`, each search resulted in a search of
only one element. This is because the largest element was kept in the first
position. Thus, every alloc request could be provided with a part from
this large segment.
With `SIZESORT+` and `ADDRSORT`, the performance in this experiment was
equiavalent. However, `ADDRSORT` could hav ebetter performance when
there are a large number of small segments with larger address values.
But, `SIZESORT-` could lead to less fragmentation when requesting 
allocations of smaller sizes.

# Question 5

With larger random allocation size (-n 1000)...
later alloc requests fail because there are no memory segments
larger enough to allocate.

With coallescing, the free list size does not grow as large.
When ordering is set to ADDRSORT, the free list remains close to size 1.

# Question 6

As allocation percentage approaches 100, the max list size decreases.
That is because fewer memory segments are freed, which means less
fragmentation.

The opposite is true as allocation percentage approaches 0.
The  max list size increases.

# Question 7

To generate a highly fragmented free list...

For `BEST` policy, request allocation and immediately free.
Each request should be strictly smaller than the last.
Eg: +10,-0,+9,-1,+8,-2, ...

For `WORST` policy, request allocation and immediately free.
But each allocation request should be a minimal size.
Eg: +1,-0,+1,-1,+1,-2, ...

For `FIRST`, request allocation and immediately free.
Size should be max_size-1.
Eg: +99,-0,+98,-1,+97,-2, ...
