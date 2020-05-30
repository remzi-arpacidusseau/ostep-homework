
# Overview

This homework introduces `fsck.py`, a simple file system simulator. Some
familiarity with the `vsfs.py` simulator (described in an earlier chapter on
file system implementation) would be useful, but is not necessary.

The file system the tool changes the on-disk state of the file system, and
then leaves it to you, the user, to detect the problem, much like a file
system consistency checker would do (e.g., fsck). The file system itself is
based on a simplified VSFS, the very simple file system described in an
earlier chapter. The tool first generates an on-disk file system; then, either
randomly or through more specific controls, the tool changes the on-disk state
of one aspect of the file system. 

The challenge for you, the user, is to figure out which part of the file
system's on-disk state was changed and hence has become inconsistent. In many
cases, the problem should be readily detected; in others, perhaps less so.

Let's get into the details. Here is an example run of the tool:

```sh
prompt> ./fsck.py -S 1
...
Final state of file system:

inode bitmap 1100100010000010
inodes       [d a:0 r:4] [f a:-1 r:1] [] [] [d a:8 r:2] [] [] [] 
             [d a:6 r:2] [] [] [] [] [f a:15 r:1] [f a:12 r:1] []
data bitmap  1000001010001001
data         [(.,0) (..,0) (g,8) (t,14) (w,4) (m,13)] [] [] [] [] [] 
             [(.,8) (..,0)] [] [(.,4) (..,0) (p,1)] [] [] [] [z] [] [] [g]

Can you figure out how the file system was corrupted?

prompt> 
```

In this case, we run the tool with flag `-S` set to 1 (for reasons
that will be clear later). To understand the change to on-disk state,
and the possible inconsistency, first you have to understand the file
system format. It is (as promised!) very simple.

First, there is an inode bitmap, which marks whether each corresponding inode
is allocated (1) or free (0); in this case, there are 16 inodes, with inodes
0, 1, 5, 9, and 14 marked as allocated.

Second, there are 16 inodes. Unallocated inodes are shown as empty brackets --
`[]` -- whereas allocated inodes have contents such as [f a:15 r:1] above. Each
allocated inode has three fields. The first is the type of the file, either
'd' for a directory or 'f' for a regular file. The second is a single address
field 'a' which either points to a single data block (in this limited file
system, files/directories can only contain a single block) or has a -1
indicating the file is empty. The third is a reference count; for regular
files, this represents the number of times this file is linked into the file
system; for directories, it represents the number of directories within this
directory.

Third is the data bitmap. Much like the inode bitmap, it indicates whether
each data block in the file system is allocated or free.

Finally, there are the data blocks themselves. For regular files, data block
contents are arbitrary (but usually contain something simple, like a letter;
in real life, these would just contain a block of file data), whereas
directory contents are structured as a list of (name, inode number) pairs.

The root directory in this file system is always inode number 0; it is from
this point that you can start in order to build knowledge of the entire file
system and its contents.

This particular file system contains the following files and directories:
```sh
  Directories: '/', '/g', '/w'
  Files:       '/t', '/m', '/w/p'
```

Can you see why? Spend some time, starting with the root directory, and
see if you can figure it out. If not, well, this homework will be hard for
you. 

Now, let's get to the inconsistency part. This particular file system has a
simple specific inconsistency within it. Can you see it?

Once you've spent some time on this, run the tool with the `-c` flag to see if
you were right:

```sh
prompt> ./fsck.py -S 1 -c

Initial state of file system:

inode bitmap 1100100010000110
inodes       [d a:0 r:4] [f a:-1 r:1] [] [] [d a:8 r:2] [] [] [] [d a:6 r:2]
             [] [] [] [] [f a:15 r:1] [f a:12 r:1] []
data bitmap  1000001010001001
data         [(.,0) (..,0) (g,8) (t,14) (w,4) (m,13)] [] [] [] [] [] 
             [(.,8) (..,0)] [] [(.,4) (..,0) (p,1)] [] [] [] [z] [] [] [g]

CORRUPTION::INODE BITMAP corrupt bit 13

Final state of file system:

inode bitmap 1100100010000010
inodes       [d a:0 r:4] [f a:-1 r:1] [] [] [d a:8 r:2] [] [] [] [d a:6 r:2]
             [] [] [] [] [f a:15 r:1] [f a:12 r:1] []
data bitmap  1000001010001001
data         [(.,0) (..,0) (g,8) (t,14) (w,4) (m,13)] [] [] [] [] [] 
             [(.,8) (..,0)] [] [(.,4) (..,0) (p,1)] [] [] [] [z] [] [] [g]

prompt> 
```

As you can see from the output, the inode bitmap was changed in bit 13,
marking that bit free when actually the inode is allocated. You can see the
inconsistency by looking at inode 13 itself, which looks like this:
`[f a:15 r:1]` (a regular file, pointing to data block 15). You also know that
this file is in the root directory (/m). Thus, concluding that the inode
bitmap changed here is fairly straightforward.

Many other corruptions are possible (but the tool only introduces one state
change at a time, to keep your life simple). Do the homework to find out 
more about them.

The other flags available for the tool are:

```sh
prompt> ./fsck.py -h
Options:
  -h, --help            show this help message and exit
  -s SEED, --seed=SEED  first random seed (for a filesystem)
  -S SEEDCORRUPT, --seedCorrupt=SEEDCORRUPT
                        second random seed (for corruptions)
  -i NUMINODES, --numInodes=NUMINODES
                        number of inodes in file system
  -d NUMDATA, --numData=NUMDATA
                        number of data blocks in file system
  -n NUMREQUESTS, --numRequests=NUMREQUESTS
                        number of requests to simulate
  -p, --printFinal      print the final set of files/dirs
  -w WHICHCORRUPT, --whichCorrupt=WHICHCORRUPT
                        do a specific corruption
  -c, --compute         compute answers for me
  -D, --dontCorrupt     don't actually corrupt file system
```

The reason for two random seeds is worth describing. The first one, `-s`,
creates different random file systems. The second one, `-S`, inserts different
file system state changes (corruptions). Thus, you can generate one particular
random file system and then try a bunch of different random corruptions upon
it. 

Some other flags just control the size of the file system (`-i` and `-d`), whereas
others determine how many file operations are run against the file system
(`-n`). The `-p` flag prints the contents of the (non-corrupted) file system; the
`-w` flag allows you to specify a particular corruption (although this is mostly
for testing); the `-D` flag turns off corruption to, allowing you to examine an
intact file system.









