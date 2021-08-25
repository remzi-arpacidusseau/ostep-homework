# Question 1

If page size is kept constant, as address space grows, page-table size increases.

If address space size is kept constant, as page size grows, page-table size decreases.

Using too large a page size could lead to internal fragmentation.

# Question 2

## 1

VA 0x00003a39 (decimal:    14905) --> invalid (VPN 14)
VA 0x00003ee5 (decimal:    16101) --> invalid (VPN 15)
VA 0x000033da (decimal:    13274) --> invalid (VPN 12)
VA 0x000039bd (decimal:    14781) --> invalid (VPN 14)
VA 0x000013d9 (decimal:     5081) --> invalid (VPN 4)

## 2

VA 0x00003986 (decimal:    14726) --> invalid (VPN 14)
VA 0x00002bc6 (decimal:    11206) --> 0x4fc6 (VPN 10)
VA 0x00001e37 (decimal:     7735) --> invalid (VPN 7)
VA 0x00000671 (decimal:     1649) --> invalid (VPN 1)
VA 0x00001bc9 (decimal:     7113) --> invalid (VPN 6)

Rest on paper notebook...

# Question 3

As the percentage of pages that are allocated in each address space increases,
the number of valid page entries increases.

# Question 4

With 32 bit architecture, and assuming the PTE size is 4 bytes (32 bits), then a system
with 128 PTEs will have a total page table size of 512 bytes (128 * 4).
A system with phsyical memory size 1024 bytes would dedicate half of its physical
memory to the page table.

A system with a physical memory size of 512m and address space size of 256m may only be able to
handle a small number of processes because each address space is half the size of physical
memory. However, it might be unlikely for each process to use the entirety of its
virtual address space. But as number of processes increases, available space will be
limited.

# Question 5

When address space sixe is bigger than physical memory, the program raises
and exception:
`Error: physical memory size must be GREATER than address space size (for this simulation)`

Other ways to break program:
* page size is bigger than virtual address space
* page size is not a power of 2
* address space is not a power of 2
* page size is 0
