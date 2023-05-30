Q1: use gettimeofday
-> use clock_gettime instead, reason ...

Q2: write tlb.c
-> how to get page size, for mac : getconf PAGESIZE

Q3: reliable result?
-> depends on granuality of used time function.
-> clock_gettime resolution on my computer is 1 microseconds (10E-6)
-> per page access is around few nanoseconds in small number of pages case
-> so it is better to run trials 10E3 times to get a reliable result

Q4: Why visualization makes data easier to digest?
-> we could observe trend from the graph

Q5: Compiler optimization
-> using -O0 (by default) for optimization already omits optimizations such as loop unrolling and register allocation but depends on compilers and vendors.
-> to be absolutely certain about this, use volatie

Q6: Pinning thread
-> not sure if we could ensure this on mac

Q7: Balance potential costs of initialization and zero demanding (memory management technique where a page of memory is not allocated and zeroed out until a process actually needs to use it.) if we do not initialize
-> initialize one element per page