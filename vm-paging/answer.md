
# Overview

Q1:

The size of a linear page table grows proportionally to the growth of the address space size.
But disproportinoal to the growth of page size.

Q2:

When input values of u are lower, there are more invalid Virtual Address Trace.

Q3:

Now let’s try some different random seeds,and some different(and sometimes quite crazy) address-space parameters, for variety:
```
-P 8 -a 32 -p 1024 -v -s 1 
-P 8k -a 32k -p 1m -v -s 2 
-P 1m -a 256m -p 512m -v -s 3
```
Which of these parameter combinations are unrealistic? Why?
```
-P 8 -a 32 -p 1024 -v -s 1
```
This case is unrealistic because size of page table is large compare to address space.

Q4:

Can you find the limits of where the program doesn’t work anymore? 
For example, what happens if the address-space size is bigger than physical memory?
Will get this error: *Error: physical memory size must be GREATER than address space size (for this simulation)*

Furthermore, physical space must be at least twice as big as virtual address space.


