#ifndef WAIT_AND_FORK
#define WAIT_AND_FORK
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>

void wait_or_die();
int fork_or_die();

#endif