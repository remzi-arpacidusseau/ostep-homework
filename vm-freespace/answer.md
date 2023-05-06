
# My solutions


Q2: How are the results different when using a WORST fit policy to search the free list (-p WORST)? What changes? -> free lists is more fragmented than using BEST strategy.

Q3: What about when using FIRST fit (-p FIRST)? What speeds up when you use first fit? -> average search elements

Q5: Coalescing of a free list can be quite important. Increase the number of random allocations (say to -n 1000). What happens to larger allocation requests over time? Run with and without coalescing (i.e., without and with the -C flag). 
Use first fit policy here.
What differences in outcome do you see? -> the one without coalescing is severly fragemented.
How big is the free list over time in each case?  w/ 2, w/o 51
Does the ordering of the list matter in this case? Yes, use SIZESORT+ alleviate the fragmentation situation and has final length of free list as 31. But using SIZESORT- make fragementation worse and has final length of free list as 100. In ADDRSORT case, there is no big difference.
