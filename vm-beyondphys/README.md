
# Overview

In this homework, you'll be investigating swap performance with a simple
program found in `mem.c`. The program is really simple: it just allocates an
array of integers of a certain size, and then proceeds to loop through it
(repeatedly), incrementing each value in the array. 

Type `make` to build it (and look at the file `Makefile` for details about how
the build works).

Then, type `./mem` followed by a number to run it. The number is the size (in
MB) of the array. Thus, to run with a small array (size 1 MB):

```sh
prompt> ./mem 1
```

and to run with a larger array (size 1 GB):

```sh
prompt> ./mem 1024
```

The program prints out the time it takes to go through each loop as well as
the bandwidth (in MB/s). Bandwidth is particularly interesting to know as it
gives you a sense of how fast the system you're using can move through data;
on modern systems, this is likely in the GB/s range. 

Here is what the output looks like for a typical run:

```sh
prompt> ./mem 1000
allocating 1048576000 bytes (1000.00 MB)
  number of integers in array: 262144000
loop 0 in 448.11 ms (bandwidth: 2231.61 MB/s)
loop 1 in 345.38 ms (bandwidth: 2895.38 MB/s)
loop 2 in 345.18 ms (bandwidth: 2897.07 MB/s)
loop 3 in 345.23 ms (bandwidth: 2896.61 MB/s)
^C
prompt> 
```

The program first tells you how much memory it allocated (in bytes, MB, and in
the number of integers), and then starts looping through the array. The first
loop (in the example above) took 448 milliseconds; because the program
accessed the 1000 MB in just under half a second, the computed bandwidth is
(not surprisingly) just over 2000 MB/s. 

The program continues by doing the same thing over and over, for loops 1, 2,
etc. 

Important: to stop the program, you must kill it. This task is accomplished on
Linux (and all Unix-based systems) by typing control-C (^C) as shown above.

Note that when you run with small array sizes, each loop's performance numbers
won't be printed. For example:

```sh
prompt>  ./mem 1
allocating 1048576 bytes (1.00 MB)
  number of integers in array: 262144
loop 0 in 0.71 ms (bandwidth: 1414.61 MB/s)
loop 607 in 0.33 ms (bandwidth: 3039.35 MB/s)
loop 1215 in 0.33 ms (bandwidth: 3030.57 MB/s)
loop 1823 in 0.33 ms (bandwidth: 3039.35 MB/s)
^C
prompt> 
```

In this case, the program only prints out a sample of outputs, so as not to
flood the screen with too much output. 

The code itself is simple to understand. The first important part is a memory
allocation: 

```c
    // the big memory allocation happens here
    int *x = malloc(size_in_bytes);
```

Then, the main loop begins:

```c
    while (1) {
	x[i++] += 1; // main work of loop done here.
```


The rest is just timing and printing out information. See `mem.c` for details.

Much of the homework revolves around using the tool vmstat to monitor what is
happening with the system. Read the vmstat man page (type `man vmstat`) for
details on how it works, and what each column of output means.



