# Question 1

To construct a Page Table Entry address from a two level page table, two registers are required.
Two registers are required in order to store the two distinct values: PFN of the Page
Directory Entry and the Page Table Index.
Although the values in the two registers will be added together (resulting in a single value),
before this can occur, both values must be manipulated independently.
A shift operation is performed upon the PDE.PFN and multiplication perfoed on the PTIndex.
The results of both operations are store din their distinct registers.

With a three level page table, only two registers will be required. Although we must
store and manipulate three values (a PFN from Page Directory Entry 0, PFN from Page Directory
Entry 1, and PTIndex), we only need to store two values at a time.
We utilize the PDE of the first PDIndex and the second PDIndex to calculate the address of the
second Page Directory Entry. Once this is calculated, we no longer need to store the first PDE
value or address. To calculate the PTE address, we only require the PFN of the second
Page Directory Entry and the PTIndex.

# Question 2

Answers in notebook.

Each lookup requires three memory references.
1. Access Page Directory Entry.
2. Access Page Table Entry.
3. Access value in Physical Memory.

# Question 3

Cache memory has limited size. Let's assume it manages size via LRU.

Assume the use of a TLB. Then, direct memory access of the page table will not occur while
the page table entry is cached in the TLB. 
If during this time the cache becomes full, the memory cached PTE is likely to be evicted
because it has not been accessed recently (due to the TLB).
When the TLB evicts the page table entry and a memory lookup of the PTE must be
performed, this will result in a cache miss.

Assume instead that a TLB was not used. Then, every memory access will require the additional
lookup of the PTE. Therefore, the recency of the page table entry will be high.
Therefore, the cache memory is less likely to evit the page table entry and instead evit other
data. This could likewise result in a higher amount of misses if that evicted data is accessed
later.
