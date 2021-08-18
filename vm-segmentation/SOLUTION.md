# Question 1

## Seed 0

Segment 0 base: 0
Segment 0 limit: 20

Segment 1 base: 512
Segment 1 limit: 20

VA 0: 108 - (Seg1) 492
VA 1:  97 - (Seg1) SEGMENTATION VIOLATION
VA 2:  53 - (Seg0) SEGMENTATION VIOLATION
VA 3:  33 - (Seg0) SEGMENTATION VIOLATION
VA 4:  65 - (Seg1) SEGMENTATION VIOLATION

## Seed 1

Segment 0 base: 0
Segment 0 limit: 20

Segment 1 base: 512
Segment 1 limit: 20

VA 0:  17 - (Seg0) 17
VA 1: 108 - (Seg1) 492
VA 2:  97 - (Seg1) SEGMENTATION VIOLATION
VA 3:  32 - (Seg0) SEGMENTATION VIOLATION
VA 4:  63 - (Seg0) SEGMENTATION VIOLATION

## Seed 2

Segment 0 base: 0
Segment 0 limit: 20

Segment 1 base: 512
Segment 1 limit: 20

VA 0: 122 - (Seg1) 506 
VA 1: 121 - (Seg1) 505
VA 2:   7 - (Seg0) 7
VA 3:  10 - (Seg0) 10
VA 4: 106 - (Seg1) SEGMENTATION VIOLATION

# Question 2

Address space size:   128
Physical memory size: 512

Segment 0 base: 0
Segment 0 limit: 20

Segment 1 base: 512
Segment 1 limit: 20

Highest legal virtual address space in segment 0: 19
Lowest legal virtual address space in segment 1: 108

Highest illegal: 63
Lowest illegal: 64

Command to test:
` ./segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 \
      -c -A 19,20,63,64,108,107`
Result:
```
Virtual Address Trace
VA  0: 0x00000013 (decimal:   19) --> VALID in SEG0: 0x00000013 (decimal:   19)
VA  1: 0x00000014 (decimal:   20) --> SEGMENTATION VIOLATION (SEG0)
VA  2: 0x0000003f (decimal:   63) --> SEGMENTATION VIOLATION (SEG0)
VA  3: 0x00000040 (decimal:   64) --> SEGMENTATION VIOLATION (SEG1)
VA  4: 0x0000006c (decimal:  108) --> VALID in SEG1: 0x000001ec (decimal:  492)
VA  5: 0x0000006b (decimal:  107) --> SEGMENTATION VIOLATION (SEG1)
```

# Question 3

Base0: 0
Limit0: 2

Base1: 127
Limit1: 2

# Question 4

In order to generate a problem where 90% of the randomly generated
virtual addresses are valid, we need to configure the base and limit
of each segment to "cover" 90% of the virtual address space.

If our virtual address space size is x, then set l0 and l1 such that:
l1+l0 == 0.9x

# Question 5

A simple way to run the simulator so that no virtual addresses are valid is to set the limits of both segment to 0.
