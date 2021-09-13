# Question 1

The program exits with a segmantation fault.

# Question 2

Compiled with `-g` flag, the debugger shows
the reason for the exit as:
"EXC_BAD_ACCESS (code=1, address=0x0)".
Note: I run with lldb instead of gbd.

# Question 3

Valgrind outputs the following:
==1366== Invalid read of size 4
==1366==    at 0xXXXXXX: main (null.c:7)
==1366==  Address 0x0 is not stack'd, malloc'd or (recently) free'd
==1366==
==1366==
==1366== Process terminating with default action of signal 11 (SIGSEGV)
==1366==  Access not within mapped region at address 0x0
==1366==    at 0xXXXXXX: main (null.c:7)

My understanding is Valgrind recognized the attempt to access memory at Address 0 (0x0).
The program had not allocated memory in this location (neither in stack or heap).
As the later section states, the memory address is not within the mapped region.

# Question 4

When the program runs, it exits without issue (return code 0).

With gdb, there does not appear to be any identified issues.

Valgrind did identify the memory leak:
==1466== LEAK SUMMARY:
==1466==    definitely lost: 4 bytes in 1 blocks

# Question 5

When I run malloc-array, the program runs successfully and exits without error.

As with Question 4, valgrind did identify the memory leak:
==1536== LEAK SUMMARY:
==1536==    definitely lost: 400 bytes in 1 blocks

Is this program correct? I believe it's observed behavior is correct,
but it is unexpected to have a memory leak.
In that regard, the program is not correct.

# Question 6

The program does run. When run with Valgrind, receive the following error:
==1324== Invalid read of size 4

# Question 7

I attempt a read of `data[50]`. The program runs without problem. Valgrind
does identify the problem as a read of memory that had been freed.

# Question 8

As expected, when the vector is constructed of an array, its gets
are order of magnitude more performant than the vector as a list.
However, the vector as a list has slightly more perfomant adds.
When testing the adds, the list performed slightly better.
However, I believe the difference could be more significant in certain
situations when using realloc. If there are not contiguous memory
blocks, realloc will need to move all existing data. This will slow
performance of the array vector.