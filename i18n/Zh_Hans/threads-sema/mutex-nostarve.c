#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include "common_threads.h"

//
// Here, you have to write (almost) ALL the code. Oh no!
// How can you show that a thread does not starve
// when attempting to acquire this mutex you build?
//

typedef __ns_mutex_t {
} ns_mutex_t;

void ns_mutex_init(ns_mutex_t *m) {
}

void ns_mutex_acquire(ns_mutex_t *m) {
}

void ns_mutex_release(ns_mutex_t *m) {
}


void *worker(void *arg) {
    return NULL;
}

int main(int argc, char *argv[]) {
    printf("parent: begin\n");
    printf("parent: end\n");
    return 0;
}

