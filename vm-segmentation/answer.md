
# My solutions

Q1:
```
> ./segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 0
ARG seed 0
ARG address space size 128
ARG phys mem size 512

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 20

  Segment 1 base  (grows negative) : 0x00000200 (decimal 512)
  Segment 1 limit                  : 20

Virtual Address Trace
  VA  0: 0x0000006c (decimal:  108) --> segment 1 -> PA(492)
  VA  1: 0x00000061 (decimal:   97) --> segment 1 -> segmentation violation
  VA  2: 0x00000035 (decimal:   53) --> segment 1 -> segmentation violation
  VA  3: 0x00000021 (decimal:   33) --> segment 1 -> segmentation violation
  VA  4: 0x00000041 (decimal:   65) --> segment 1 -> segmentation violation

Virtual Address Trace
  VA  0: 0x00000011 (decimal:   17) --> PA (seg 0, 17)
  VA  3: 0x00000020 (decimal:   32) --> segmentation violation
  VA  4: 0x0000003f (decimal:   63) --> segmentation violation

Virtual Address Trace
  VA  0: 0x0000007a (decimal:  122) --> PA (seg 1, 506)
  VA  1: 0x00000079 (decimal:  121) --> PA (seg 1, 505)
  VA  2: 0x00000007 (decimal:    7) --> PA (seg 0, 7)
  VA  3: 0x0000000a (decimal:   10) --> PA (seg 0, 10)
  VA  4: 0x0000006a (decimal:  106) --> segmentation violation
```

Q2:
```
highest legal virtual address in segment 0 -> 0x00000013
lowest legal virtual address in segment 1 -> 0x0000006c
lowest and highest illegal addresses in this entire address space -> 0x00000014, 0x0000006b

> ./segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 2 -A 19,20,107,108 -c
Virtual Address Trace
  VA  0: 0x00000013 (decimal:   19) --> VALID in SEG0: 0x00000013 (decimal:   19)
  VA  1: 0x00000014 (decimal:   20) --> SEGMENTATION VIOLATION (SEG0)
  VA  2: 0x0000006b (decimal:  107) --> SEGMENTATION VIOLATION (SEG1)
  VA  3: 0x0000006c (decimal:  108) --> VALID in SEG1: 0x000001ec (decimal:  492)
```

Q3:
```
./segmentation.py -a 16 -p 128 -b 0 -l 2 -B 16 -L 2
```


Q4:
Assume we want to generate a problem where roughly 90% of the randomly-generated virtual addresses are valid (not segmentation violations). 
How should you configure the simulator to do so? -l + -L should cover 90% addresses in address space
Which parameters are important to getting this outcome? -l -L for lengths

Q5:
Can you run the simulator such that no virtual addresses are valid? How?
Just set lengths to zero
```
> ./segmentation.py -a 16 -p 128 -b 0 -l 0 -B 16 -L 0 -c -A 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
ARG seed 0
ARG address space size 16
ARG phys mem size 128

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 0

  Segment 1 base  (grows negative) : 0x00000010 (decimal 16)
  Segment 1 limit                  : 0

Virtual Address Trace
  VA  0: 0x00000000 (decimal:    0) --> SEGMENTATION VIOLATION (SEG0)
  VA  1: 0x00000001 (decimal:    1) --> SEGMENTATION VIOLATION (SEG0)
  VA  2: 0x00000002 (decimal:    2) --> SEGMENTATION VIOLATION (SEG0)
  VA  3: 0x00000003 (decimal:    3) --> SEGMENTATION VIOLATION (SEG0)
  VA  4: 0x00000004 (decimal:    4) --> SEGMENTATION VIOLATION (SEG0)
  VA  5: 0x00000005 (decimal:    5) --> SEGMENTATION VIOLATION (SEG0)
  VA  6: 0x00000006 (decimal:    6) --> SEGMENTATION VIOLATION (SEG0)
  VA  7: 0x00000007 (decimal:    7) --> SEGMENTATION VIOLATION (SEG0)
  VA  8: 0x00000008 (decimal:    8) --> SEGMENTATION VIOLATION (SEG1)
  VA  9: 0x00000009 (decimal:    9) --> SEGMENTATION VIOLATION (SEG1)
  VA 10: 0x0000000a (decimal:   10) --> SEGMENTATION VIOLATION (SEG1)
  VA 11: 0x0000000b (decimal:   11) --> SEGMENTATION VIOLATION (SEG1)
  VA 12: 0x0000000c (decimal:   12) --> SEGMENTATION VIOLATION (SEG1)
  VA 13: 0x0000000d (decimal:   13) --> SEGMENTATION VIOLATION (SEG1)
  VA 14: 0x0000000e (decimal:   14) --> SEGMENTATION VIOLATION (SEG1)
  VA 15: 0x0000000f (decimal:   15) --> SEGMENTATION VIOLATION (SEG1)
```