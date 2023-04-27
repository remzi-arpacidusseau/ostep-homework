#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>
#include "wait_and_fork.h"


int main(int argc, char *argv[]) {
    int x = 100;
    // process a
    if (fork_or_die() == 0) {
        printf("X value in child process before change: %d\n", x);
        // process b
        x = 200;
        printf("X value in child process after change: %d\n", x);
        exit(0);
    } else {
        x = 50;
        printf("X value in parent process after change: %d\n", x);

    }
    wait_or_die();
    return 0;
}