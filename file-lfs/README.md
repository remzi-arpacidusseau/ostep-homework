
# Overview

This homework involves a simulator of the log-structured file system, LFS. 
The simulator simplifies the book chapter's LFS a bit, but hopefully leaves
enough in place in order to illustrate some of the important properties of
such a file system.

To get start, run the following:

```sh
prompt> ./lfs.py -n 1 -o
```

What you will see is as follows:

```sh
INITIAL file system contents:
[   0 ] live checkpoint: 3 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
[   1 ] live [.,0] [..,0] -- -- -- -- -- --
[   2 ] live type:dir size:1 refs:2 ptrs: 1 -- -- -- -- -- -- --
[   3 ] live chunk(imap): 2 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

create file /ku3

FINAL file system contents:
[   0 ]  ?   checkpoint: 7 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
[   1 ]  ?   [.,0] [..,0] -- -- -- -- -- --
[   2 ]  ?   type:dir size:1 refs:2 ptrs: 1 -- -- -- -- -- -- --
[   3 ]  ?   chunk(imap): 2 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
[   4 ]  ?   [.,0] [..,0] [ku3,1] -- -- -- -- --
[   5 ]  ?   type:dir size:1 refs:2 ptrs: 4 -- -- -- -- -- -- --
[   6 ]  ?   type:reg size:0 refs:1 ptrs: -- -- -- -- -- -- -- --
[   7 ]  ?   chunk(imap): 5 6 -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

The output shows the initial file system state of an empty LFS, with a few
different blocks initialized. The first block (block 0) is the "checkpoint
region" of this LFS. For simplicity, this LFS only has one checkpoint region,
and it is always located at block address=0, and is always just the size
of a single block.

The contents of the checkpoint region are just disk addresses: locations
of chunks of the inode map. In this case, the checkpoint region has the
following contents:

```sh
checkpoint: 3 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

Let's call the leftmost entry (marked with a 3 here) the 0th entry,
the next one the 1st, and the last one (because there are 16) the
15th entry. Thus, we can think of them as:

```sh
checkpoint: 3 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    entry:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
```

This means that the first chunk of the inode map resides at disk address=3,
and that the rest of the inode map pieces have yet to be allocated (and 
hence are marked "--").

Let's now look at that chunk of the inode map ("imap" from now on). The
imap is just an array that tells you, for each inode number, its current
location on the disk. In the initial state shown above, we see this:

```sh
chunk(imap): 2 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

These chunks also have (by default) 16 entries, and again we can think of
them as such:

```sh
chunk(imap): 2 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     entry:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
```

Because each chunk of the imap has 16 entries, and because the checkpoint
region (CR) has 16 entries, we now know that the entire LFS has 16x16=256
inode numbers available for files. A small file system(!) but good enough
for our purposes.

We also now know that each chunk of the imap is responsible for a contiguous
group of inodes, and we know which ones depending on which entry in the CR
points to this chunk. Specifically, entry 0 of the CR points to a chunk of
the imap that has information about inode numbers 0...15; entry 1 of the CR
points to an imap chunk for inode numbers 16...31. 

In this specific example, we know the 0th entry of the CR points to block=3,
and in there, the 0th entry has a '2' in it. In our simulator, the root inode
is inode number=0, and thus this is the inode of the root directory of the 
file system. From the imap, we now know the location of inode number=0's
address is block=2. So let's look at block 2! We see: 

```sh
type:dir size:1 refs:2 ptrs: 1 -- -- -- -- -- -- --
```

This file metadata is a simplified inode, with file type (a directory), size
(1 block), reference count (how many directories it refers to, if this is a
directory), and some number of pointers to data blocks (in this case, one,
which points to block address=1). 

This finally leads us to the last bit of initial state, which is the contents 
of the directory. This directory only has one block in it (at address 1),
which has contents:

```sh
[.,0] [..,0] -- -- -- -- -- --
```

Herein lies an empty directory, with [name,inode number] pairs for itself
(".") and its parent (".."). In this special case (the root), the parent is
just itself, and both are inode number=0. Whew! We have now (hopefully)
understood the entire contents of the initial state of the file system.

What happens next in the default mode of the simulation is that one or more
operations are run against the file system, thus changing its state. In this
case, we know what the command because we had the simulator tell us via the 
"-o" flag (which shows each operation as it is run). That operation is:

```sh
create file /ku3
```

This means a file "ku3" was created in the root directory "/". To accomplish
this creation, a number of structures must be updated, which means that the
log was written to. You can see that four writes occur beyond the previous end
of the log (address=3), at blocks 4...7:

```sh
[.,0] [..,0] [ku3,1] -- -- -- -- --
type:dir size:1 refs:2 ptrs: 4 -- -- -- -- -- -- --
type:reg size:0 refs:1 ptrs: -- -- -- -- -- -- -- --
chunk(imap): 5 6 -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

These updates reflect how this version of LFS writes to the disk to create a
file: 
- A directory block update to include "ku3" and its inode number (1) in the root directory
- An updated root inode which now refers to block 4 where the latest contents of this directory are found
- A new inode for the newly created file (note the type) 
- A new version of the first imap chunk which now tells us where both inode 0 and inode 1 are located

However, this does not (quite) reflect all that must change. Because the inode
map itself has changed, the checkpoint region must also reflect where the
latest chunk of the first piece of the inode map resides. Thus, the CR is also
updated: 

```sh
checkpoint: 7 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

You might also have noticed one more thing in the output. In the initial file
system contents, there is a marker between the disk address and the contents
that says "live" for each entry, and in the final output there is a "?"
instead. This "?" is there so you can determine, for yourself, whether each
block is live or not. Start with the checkpoint region and see if you can
determine which group of blocks can be reached (and hence are live); all the
rest are thus dead and could be used again. 

To see if you are right, run again with `-c`:

```sh
prompt> ./lfs.py -n 1 -o -c

...
```

As you can now see, every time a structure is updated, garbage is left behind,
one of the main issues a non-update-in-place file system like LFS must deal
with. Fortunately, for you, we won't worry too much about garbage collection
in this simplified version of LFS.

You now have all the information you need to understand this version of LFS.

The other options, which let you play with various aspects of the simulator, include: 

```sh
prompt> ./lfs.py -h
Usage: lfs.py [options]

Options:
  -h, --help            show this help message and exit
  -s SEED, --seed=SEED  the random seed
  -N, --no_force        Do not force checkpoint writes after updates
  -D, --use_disk_cr     use disk (maybe old) version of checkpoint region
  -c, --compute         compute answers for me
  -o, --show_operations
                        print out operations as they occur
  -i, --show_intermediate
                        print out state changes as they occur
  -e, --show_return_codes
                        show error/return codes
  -n NUM_COMMANDS, --num_commands=NUM_COMMANDS
                        generate N random commands
  -p PERCENTAGES, --percentages=PERCENTAGES
                        percent chance of:
                        createfile,writefile,createdir,rmfile,linkfile,sync
                        (example is c30,w30,d10,r20,l10,s0)
  -a INODE_POLICY, --allocation_policy=INODE_POLICY
                        inode allocation policy: "r" for "random" or "s" for
                        "sequential"
  -L COMMAND_LIST, --command_list=COMMAND_LIST
                        command list in format:
                        "cmd1,arg1,...,argN:cmd2,arg1,...,argN:... where cmds
                        are:c:createfile, d:createdir, r:delete, w:write,
                        l:link, s:syncformat: c,filepath d,dirpath r,filepath
                        w,filepath,offset,numblks l,srcpath,dstpath s
```






