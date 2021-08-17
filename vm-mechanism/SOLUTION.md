# Question 1

## Seed 1

Base: 13884
Limit: 290

VA 0: 782 - SEGMENTATION VIOLATION
VA 1: 261 - 1415
VA 2: 507 - SEGMENTATION VIOLATION
VA 3: 460 - SEGMENTATION VIOLATION
VA 4: 667 - SEGMENTATION VIOLATION

## Seed 2

Base: 15529
Limit: 500

VA 0:  57 - 15586
VA 1:  86 - 15615
VA 2: 855 - SEGMENTATION VIOLATION
VA 3: 753 - SEGMENTATION VIOLATION
VA 4: 685 - SEGMENTATION VIOLATION

## Seed 3

Base: 8916
Limit: 316

VA 0: 378 - SEGMENTATION VIOLATION
VA 1: 618 - SEGMENTATION VIOLATION
VA 2: 640 - SEGMENTATION VIOLATION
VA 3:  67 - 8983
VA 4:  13 - 8929

# Question 2

The bounds register must be set to greater than 929.

# Question 3

The largest virtual address is 867.
The physical memory size is 16k (16384).
If the base is set to 15517, we can fit all generated
virtual addresses in physical memory.
However, the virtual address space size is 1k.
If we want to fit all possible virtual addresses in
physical memory (regardless of bounds), then the
maximum base is 15k.

# Question 4

Skipped.

# Question 5

Limit 10: 4/500
Limit 100: 47/500
Limit 1000: 486/500
Limit 10000: 500/500


