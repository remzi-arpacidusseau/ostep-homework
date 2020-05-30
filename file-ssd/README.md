
# Overview

Welcome to `ssd.py`, yet another wonderful simulator provided to you,
for free, by the authors of OSTEP, which is also free. Pretty soon,
you're going to think that everything important in life is free! And,
it turns out, it kind of is: the air you breathe, the love you give
and receive, and a book about operating systems. What else do you
need?

To run the simulator, you just do the usual:

```sh
prompt> ./ssd.py
```

The simulator models a few different types of SSDs. The first is what we'll
call an "ideal" SSD, which actually isn't much an SSD at all; it's more like a
perfect memory. To simulate this SSD, type:

```sh
prompt> ./ssd.py -T ideal
```

To see how this one works, let's create a little workload. A workload, for an
SSD, is just a series of low-level I/O operations issued to the device. There
are three operations supported by ssd.py: read (which takes an address to
read, and returns the data), write (which takes an address and a piece of data
to write, in this case, a single letter), and trim (which takes an
address). The trim operation is used to indicate a previously written block is
no longer live (i.e., the file it was in was deleted); this is particular
useful for a log-based SSD, which can reclaim the block's space during garbage
collection and free up space in the FTL. Let's run a simple workload
consisting of just one write:

```sh
prompt> ./ssd.py -T ideal -L w10:a -l 30 -B 3 -p 10
```

The `-L` flag allows us to specify a comma-separated list of commands. Here, to
write to logical page 10, we include the command "w10:a" which means "write"
to logical page "10" the data of "a". We also include a few other specifics
about the size of the SSD with the flags `-l 30 -B 3 -p 10`, but let's
ignore those for now.

What you should see on the screen, after running the above:

```sh
FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii iiiiiiiiii iiiiiiiiii
Data
Live


FTL    10: 10
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State viiiiiiiii iiiiiiiiii iiiiiiiiii
Data             a
Live             +
```

The first chunk of information shows the initial state of the SSD, and the
second chunk shows its final state. Let's walk through each piece to make sure
you understand what they mean.

The first line of each chunk of output shows the contents of the FTL. This
simulator only models a simple page-mapped FTL; thus, each entry within it
shows the logical-to-physical page mapping for any live data items.

In the initial state, the FTL is empty:

```sh
FTL   (empty)
```

However, in the final state, you can see that the FTL maps logical page 10 to
physical page 10:

```sh
FTL    10: 10
```

The reason for this simple mapping is that we are running the "ideal" SSD,
which really just acts like a memory; if you write to logical page X, this SSD
will just (magically) write the data to physical page X (indeed, you don't
even really need the FTL for this; we'll just use the ideal SSD to show how
much extra work a real SSD does, in terms of erases and data copying, as
compared to an ideal memory). 

The next lines of output just label the blocks and physical pages of the
underlying Flash the simulator is modeling:

```sh
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
```

In this simulation, you can see that the SSD has 3 physical Flash blocks, and
that each block has 10 physical pages. Each block is numbered (0, 1, and 2),
as is each page (from 00 to 29); to keep the display compact (width-wise), the
page numbering is shown across two lines. Thus, physical page "10" is labeled
with a "1" on the first line, and a "0" on the second.

The next line shows the state of each page, i.e., whether it is INVALID (i),
ERASED (E), or VALID (v), as per the chapter:

```sh
State viiiiiiiii iiiiiiiiii iiiiiiiiii
```

The states for the "ideal" SSD are a bit weird, in that you can have "v" and
"i" mixed in a block, and that the block is never "E" for erased. Below, with
the more realistic "direct" and "log" SSDs, you'll see "E" too.

The final two lines show the "contents" of any written-to pages (on the "Data"
row) and whether that data is currently live (that is, referred to in the
FTL) in the "Live" row:

```sh
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
Data             a
Live             +
```

Here, we can see that on Block 2 (i.e., Page 10), there is the data "a", and
it is indeed live (shown by the "+" symbol).

Let's expand our workload a little bit, before getting to the more realistic
types of SSDs. After writing the data, let's read it, and then let's use trim
to delete it:

```sh
prompt> ./ssd.py -T ideal -L w10:a,r10,t10 -l 30 -B 3 -p 10
```

If you run this, you'll see two identical states: the initial (empty) state,
and the final (also empty!) state. Not too exciting! To see more of what is
going on, you'll have to use some more flags. Yes, this SSD simulator uses a
lot of flags; sorry, all lovers of parsimony! But alas, there is some
complexity here we must explore.

One useful flag is `-C`, which just shows every command that was issued, and
whether is succeeded or not.

```sh
prompt> ./ssd.py -T ideal -L w10:a,r10,t10 -l 30 -B 3 -p 10 -C

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii iiiiiiiiii iiiiiiiiii
Data
Live

cmd   0:: write(10, a) -> success
cmd   1:: read(10) -> a
cmd   2:: trim(10) -> success

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii viiiiiiiii iiiiiiiiii
Data             a
Live

prompt> 
```

Here, you can see the write, read, and trim, and you can also see what each
command returned: success, the data read, and success, respectively. This will
be more interesting later, when the simulator generates the operations
randomly. 

Similarly, the `-F` flag shows the state of the Flash between each operation,
instead of just at the end. Note the subtle changes at each step:

```sh
prompt> ./ssd.py -T ideal -L w10:a,r10,t10 -l 30 -B 3 -p 10 -F

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii iiiiiiiiii iiiiiiiiii
Data
Live

FTL    10: 10
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii viiiiiiiii iiiiiiiiii
Data             a
Live             +

FTL    10: 10
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii viiiiiiiii iiiiiiiiii
Data             a
Live             +

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii viiiiiiiii iiiiiiiiii
Data             a
Live

prompt> 
```

Of course, you can use `-C` and `-F` in concert to show everything (an exercise
left to the reader). 

The simulator also lets you generate random workloads, instead of specifying
operations yourself. Use the "-n" flag for this, with an associated number (we
also specify a random seed with "-s" to get a particular workload):

```sh
prompt> ./ssd.py -T ideal -l 30 -B 3 -p 10 -n 5 -s 10
```

If you run this with `-C`, `-F`, or both, you'll see either the exact commands,
the intermediate states of the Flash, or both. However, you can also use the
"-q" flag to quiz yourself on what you think the commands are. Thus, run the
following: 

```sh
prompt> ./ssd.py -T ideal -l 30 -B 3 -p 10 -n 5 -s 10 -q
(output omitted for brevity)
```

Now, by examining the intermediate states, see if you can discern what the
commands must have been (writes and trims are left completely unspecified,
whereas reads just ask you to figure out which data was returned).

You can then either manually use `-C -F` to show everything, or just add the
`-c` flag to "solve" the problem for you, to check your answers.

Let's now do the same thing (a random workload of five operations) but use
different more realistic SSDs. The first is the "direct" SSD mentioned in the
chapter. This too isn't particularly realistic, but at least uses erases and
programs to update the Flash. Specifically, when a logical page is written, it
is mapped directly to the physical page of the same number. This mapping
necessitates first a read of all the live data in that block, then an erase of
the block, and then a series of programs to restore all previously live data
as well as write the new data to Flash. Let's run it, show the commands (-C)
but not the intermediate states (no -F):

```sh
prompt> ./ssd.py -T direct -l 30 -B 3 -p 10 -n 5 -s 10 -C 

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii iiiiiiiiii iiiiiiiiii
Data
Live

cmd   0:: write(12, z) -> success
cmd   1:: write(19, 9) -> success
cmd   2:: write(9, f) -> success
cmd   3:: trim(9) -> success
cmd   4:: read(19) -> 9

FTL    12: 12  19: 19
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State EEEEEEEEEv EEvEEEEEEv iiiiiiiiii
Data           f   z      9
Live               +      +

prompt> 
```

As you can see from the final state, the FTL contains two live mappings:
logical page 12 refers to physical page 12, and 19 to 19 (remember, this is
the direct mapping). You can also see three data pages with information within
them: physical page 9 contains "f", 12 contains "z", and 19 contains "9" (data
can be letters or numbers or really any single character). However, also note
that "9" has been trimmed; this removes its entry from the FTL, but the data
lies their dormant (for now). If you then tried to read logical page 9, it no
longer would succeed:

```sh
prompt> ./ssd.py -T direct -l 30 -B 3 -p 10 -C -L w9:f,t9,r9

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii iiiiiiiiii iiiiiiiiii
Data
Live

cmd   0:: write(9, f) -> success
cmd   1:: trim(9) -> success
cmd   2:: read(9) -> fail: uninitialized read

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State EEEEEEEEEv iiiiiiiiii iiiiiiiiii
Data           f
Live

prompt>
```

One last SSD we should pay attention to is the actual most realistic one,
which uses log-structuring (as do most real SSDs). To use it, just change the
SSD type to "log" (we'll again turn on -C so we can just know which operations
took place, instead of quizzing ourselves):

```sh
prompt> ./ssd.py -T log -l 30 -B 3 -p 10 -s 10 -n 5 -C

FTL   (empty)
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State iiiiiiiiii iiiiiiiiii iiiiiiiiii
Data
Live

cmd   0:: write(12, z) -> success
cmd   1:: write(19, 9) -> success
cmd   2:: write(9, f) -> success
cmd   3:: trim(9) -> success
cmd   4:: read(19) -> 9

FTL    12:  0  19:  1
Block 0          1          2
Page  0000000000 1111111111 2222222222
      0123456789 0123456789 0123456789
State vvvEEEEEEE iiiiiiiiii iiiiiiiiii
Data  z9f
Live  ++

prompt>
```

Note how the log-structured SSD writes data to the Flash. First, the current
log block (Block 0, in this case) is erased. Then, the pages are programmed in
order. Use the -F flag to see each step for more detail.

The simulator can also show more statistics, including operation counts and
the estimated time that the modeled SSD would take to complete the given
workload. To see these, use the -S flag:

```sh
prompt> ./ssd.py -T log -l 30 -B 3 -p 10 -s 10 -n 5 -S

(stuff omitted)

Physical Operations Per Block
Erases   1          0          0          Sum: 1
Writes   3          0          0          Sum: 3
Reads    1          0          0          Sum: 1

Logical Operation Sums
  Write count 3 (0 failed)
  Read count  1 (0 failed)
  Trim count  1 (0 failed)

Times
  Erase time 1000.00
  Write time 120.00
  Read time  10.00
  Total time 1130.00
```

Here you can see the physical erases, writes, and reads per block as well as a
sum of each, then the number of logical writes, reads, and trims issued to the
device, and finally the estimated times. You can change the costs of low-level
operations such as read, program, and erase, with the -R, -W, and -E flags,
respectively. 

Finally, with the SSD in log-structured mode, there is a garbage collector (GC)
that can be configured to run periodically. This behavior is controlled by the
-G and -g flags, which set the high and low watermarks for determining whether
the garbage collector should run. Setting the high watermark to a value N
(i.e., -G N) means that when the GC notices that N blocks are in use, it
should run. Setting the low watermark to M (i.e., -G M) means that the GC
should run until only M blocks are in use. 

The -J flag is also useful here: it shows which low-level commands the GC
issues (reads and writes of live data, followed by erases of reclaimed
blocks). The following issues 60 operations, and sets the high and low
watermarks to 3 and 2, respectively.

```sh
prompt> ./ssd.py -T log -l 30 -B 3 -p 10 -s 10 -n 60 -G 3 -g 2 -C -F -J
```

Using `-C`, `-F`, and `-J` lets you really see what is happening, step
by step, inside the log-structured simulation.

There are a few other flags worth knowing. The entire time, we've been using
the following three flags to control the size of the simulated SSD:

```sh
  -l NUM_LOGICAL_PAGES, --logical_pages=NUM_LOGICAL_PAGES  number of logical pages in interface
  -B NUM_BLOCKS, --num_blocks=NUM_BLOCKS                   number of physical blocks in SSD
  -p PAGES_PER_BLOCK, --pages_per_block=PAGES_PER_BLOCK    pages per physical block
```

You can change these values to simulate larger or smaller SSDs than the simple
one we've been simulating so far.

One other set of controls lets you control randomly generated
workloads a bit more precisely. The `-P` flag lets you control how
many reads/writes/trims show up (probabilistically). For example,
using `-P 30/35/35` means that roughly 30% of operations will be
reads, 35% writes, and 35% trims.

The `-r` flag allows reads to be issued to non-live addresses (the default only
issues reads to live data). Thus, `-r 10` means roughly 10% of reads will
fail.

Finally, the `-K` and `-k` flags let you add some "skew" to a workload. A skew is
first specified by `-K`, e.g., `-K 80/20` makes 80% of writes target 20% of
the logical space (a hot/cold kind of workload). Skew is common in real
workloads, and has different effects on garbage collection, etc., so it is
good to be able to model. The related `-k` flag lets you specify when the skew
starts; specifically, `-k 50` means that after 50 writes, start doing the skew
(before then, the writes will be chosen at random from all possible pages in
the logical space).

Wow, have you gotten this far? You are some impressive person! We suspect you
will go far in life. Or, we suspect that you typed "cat README" and not "more
README" or "less README", in which case we suspect you are just learning about
"more" or "less", more or less.


