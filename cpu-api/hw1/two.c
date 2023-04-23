#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "wait_and_fork.h"

void check_write(ssize_t n_bytes, const char * name) {
    if (n_bytes == -1) {
        printf("cannot write in: %s\n", name);
    }
    return;
}

int main(int argc, char *argv[]) {
    int file_descriptor = open("./two.output", O_CREAT|O_WRONLY|O_TRUNC, S_IRWXU);
    const char * words = "Hello hello here";
    // process a
    if (fork_or_die() == 0) {
        const char *name = "child";
        check_write(write(file_descriptor, words, strlen(words)), name);
        exit(0);
    } else {
        const char *name = "parent";
        check_write(write(file_descriptor, words, strlen(words)), name);
    }
    wait_or_die();
    return 0;
}