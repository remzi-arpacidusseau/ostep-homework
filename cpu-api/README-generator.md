
# Overview: `generator.py`

This tool, `generator.py`, allows the user to create little C programs
that exercise `fork` in different ways so as to gain better
understanding of how `fork` works.

The simplest usage is just as follows:
```sh
prompt> ./generator.py
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
    // thread a
    if (fork_or_die() == 0) {
        sleep(1);
        // thread b
        exit(0);
    }
    wait_or_die();
    if (fork_or_die() == 0) {
        sleep(4);
        // thread c
        exit(0);
    }
    wait_or_die();
    if (fork_or_die() == 0) {
        sleep(4);
        // thread d
        if (fork_or_die() == 0) {
            sleep(2);
            // thread e
            exit(0);
        }
        if (fork_or_die() == 0) {
            sleep(2);
            // thread f
            exit(0);
        }
        wait_or_die();
        wait_or_die();
        exit(0);
    }
    wait_or_die();
    return 0;
}
```
