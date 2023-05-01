
# Homework


Q1. compile and run null.c, output:
```sh
[1]    34220 segmentation fault  ./null
```

Q2. use lldb and -g flag, lldb show:

```sh
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x0)
    frame #0: 0x0000000100003f6b null`main at null.c:6:34
   3
   4   	int main() {
   5   	    int* ptr = NULL;
-> 6   	    printf("Inside ptr is %d\n", *ptr);
   7
   8   	    return 0;
   9   	}
Likely cause: ptr accessed 0x0
```

Q3. valgrind --leak-check=yes ./null output:

```sh
==47432== Invalid read of size 4
==47432==    at 0x100003F6B: main (null.c:6)
==47432==  Address 0x0 is not stack'd, malloc'd or (recently) free'd
```

Q4. no free memory until exit
```sh
# LLDB output
Process 47625 exited with status = 0 (0x00000000) #normal
# valgrind output
==47677== 40,000 bytes in 1 blocks are definitely lost in loss record 41 of 41
==47677==    at 0x100124545: malloc (in /usr/local/Cellar/valgrind/HEAD-085775b/libexec/valgrind/vgpreload_memcheck-amd64-darwin.so)
==47677==    by 0x100003F88: main (no_free.c:6)

```

Q5. invalid write to location out of bound
```sh
==48161== Invalid write of size 4
==48161==    at 0x100003F81: main (out_bound.c:7)
==48161==  Address 0x100825770 is 0 bytes after a block of size 400 allocd
==48161==    at 0x100124545: malloc (in /usr/local/Cellar/valgrind/HEAD-085775b/libexec/valgrind/vgpreload_memcheck-amd64-darwin.so)
==48161==    by 0x100003F78: main (out_bound.c:6)
```

Q6. read after free
```sh
# normal output, correct
data[50] = 50
# valgrind output
==48631== Invalid read of size 4
==48631==    at 0x100003F38: main (read_free_arr.c:10)
==48631==  Address 0x1008256a8 is 200 bytes inside a block of size 400 free'd
==48631==    at 0x10012491D: free (in /usr/local/Cellar/valgrind/HEAD-085775b/libexec/valgrind/vgpreload_memcheck-amd64-darwin.so)
==48631==    by 0x100003F33: main (read_free_arr.c:8)
==48631==  Block was alloc'd at
==48631==    at 0x100124545: malloc (in /usr/local/Cellar/valgrind/HEAD-085775b/libexec/valgrind/vgpreload_memcheck-amd64-darwin.so)
==48631==    by 0x100003F18: main (read_free_arr.c:6)
```
