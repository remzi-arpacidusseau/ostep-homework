#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "wait_and_fork.h"

int main(int argc, char *argv[]) {
    // process a
    if (fork_or_die() == 0) {
        printf("hello.\n");
        exit(0);
    } 
    wait_or_die();
    printf("goodbye.\n");
    return 0;
}