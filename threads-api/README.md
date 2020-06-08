
# Overview

In this homework, you'll use a real tool on Linux to find problems in
multi-threaded code. The tool is called `helgrind` (available as part of the
valgrind suite of debugging tools).

See `http://valgrind.org/docs/manual/hg-manual.htm` for details about
the tool, including how to download and install it (if it's not
already on your Linux system).

You'll then look at a number of multi-threaded C programs to see how you can
use the tool to debug problematic threaded code.

First things first: download and install `valgrind` and the related `helgrind` tool. 

Then, type `make` to build all the different programs. Examine the `Makefile`
for more details on how that works.

Then, you have a few different C programs to look at:
- `main-race.c`: A simple race condition
- `main-deadlock.c`: A simple deadlock
- `main-deadlock-global.c`: A solution to the deadlock problem
- `main-signal.c`: A simple child/parent signaling example
- `main-signal-cv.c`: A more efficient signaling via condition variables
- `common_threads.h`: Header file with wrappers to make code check errors and be more readable

With these programs, you can now answer the questions in the textbook.




