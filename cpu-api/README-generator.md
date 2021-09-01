
# Overview: `generator.py`

This tool, `generator.py`, allows the user to create little C programs
that exercise `fork` in different ways so as to gain better
understanding of how `fork` works.

A sample usage is just as follows:
```sh
prompt> ./generator.py -n 1 -s 0
```

The output you will see when you run this is a randomly generated C
program. In this case, you will see something like this:

```c
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>

void wait_or_die() {
    int rc = wait(NULL);
    assert(rc > 0);
}

int fork_or_die() {
    int rc = fork();
    assert(rc >= 0);
    return rc;
}

int main(int argc, char *argv[]) {
    // process a
    if (fork_or_die() == 0) {
        sleep(6);
        // process b
        exit(0);
    }
    wait_or_die();
    return 0;
}
```

Let's understand this code a bit. The first part (from the top, up to
the beginning of `main()`) will be included in every generated C
program. The two pieces of code, `wait_or_die()` and `fork_or_die()`,
are just simple wrappers to the `wait` and `fork` system calls, and
either succeed (as they usually will) or detect an error (by checking
the return code, stored in `rc`) and exit, via the `assert()`
call. The wrappers are useful when it's OK to simply exit upon failure
(which it is here, but not always), and make the code in `main()`
easier to read.

Aside: `assert()`, if you're not familiar with it, is a macro that
simply checks the truth of the expression you pass to it. If the
assertion is true, `assert()` simply returns and the program
continues. If it is false, the process will exit.

The interesting part of the code, which changes with different random
seeds, is found in `main()`. Here we see the main process, which we
will refer to as "process a" (or just "a" for short) start, call
`fork_or_die()` to create another process, and then wait for that
process to complete (by calling `wait_or_die()`).

The child process (called "b") just sleeps for some period of time
(here, 4 seconds) and then exits.

The challenge for you, then, is to predict what the output will look
like when this program runs. As usual, we can get the result simply by
using the `-c` flag:

```sh
prompt> ./generator.py -n 1 -s 0 -c
  0 a+
  0 a->b
  6      b+
  6      b-
  6 a<-b
prompt> 
```

The way to read the output is as follows. The first column shows the
time when certain events take place. In this case, there are two
events that happen at time 0. First, process a starts running (shown
by `a+`); then, a forks and creates b (shown by `a->b`).

Then, b starts running and immediately sleeps for 6 seconds, as shown
in the code. Once this sleep is done, b prints that it has been
created (`b+`), but it doesn't do much; in fact, it just exits, which
is shown as well (`b-`). These are shown to both happen at time 6 in
the output; however, in reality, we know that `b+` happens just before
`b-`.

Finally, once b has exited, the `wait_or_die()` call in its parent
process, a, returns, and then a final print out takes place (`a<-b`)
to indicate this has happened.

A number of flags control the randomly generated code that gets
created. They are:
* `-s SEED` - different random seeds yield different programs
* `-n NUM_ACTIONS` - how many actions (`fork`, `wait`) a program should include
* `-f FORK_CHANCE` - the chances, from 1-99 percent, that a `fork()` will be added
* `-w WAIT_CHANCE` - same, but a `wait()` (of course, there must be an outstanding `fork` for this to be called)
* `-e EXIT_CHANCE` - same, but the chances the process will `exit`
* `-S MAX_SLEEP_TIME` - the max sleep time that is chosen when adding sleeps into the code

There are also a few flags that control which C files get created for the code:
* `-r READABLE` - this is the file shown to you (and optimized for readability)
* `-R RUNNABLE` - this is the file that will be compiled and run; it is identical to the above but adds print statements and such

Finally, there is one other flag, `-A`, that lets you specify a
program exactly. For example:

```sh
prompt> ./generator.py -A "fork b,1 {} wait"
```

The resulting C code:
```c
int main(int argc, char *argv[]) {
    // process a
    if (fork_or_die() == 0) {
        sleep(1);
        // process b
        exit(0);
    }
    wait_or_die();
    return 0;
}
```

This command creates the default process ("a"), which then creates "b"
which sleeps for 1 but doesn't do anything else; in the meanwhile, "a"
then waits for "b" to complete.

More complex examples can be created. For example:
* `-A "fork b,1 {} fork c,2 {} wait wait"` - process "a" creates two
processes, "b" and "c", and then waits for both
* `-A "fork b,1 {fork c,2 {} fork d,3 {} wait wait} wait"` - process
"a" creates "b" and then waits for it to complete; "b" creates "c" and
"d" and waits for them to complete.

Read through and do the homework questions to gain a fuller
understanding of `fork`.



