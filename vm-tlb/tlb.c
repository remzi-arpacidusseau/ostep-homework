#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define BILLION 1000000000L
#define PAGESIZE 4096

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <numPages> <numTrials>\n", argv[0]);
        return 1;
    }

    // struct timespec resolution;
    // clock_getres(CLOCK_MONOTONIC, &resolution);
    // printf("Clock resolution: %ld nanoseconds\n", resolution.tv_nsec);

    int numPages = atoi(argv[1]);
    int numTrials = atoi(argv[2]);

    int pageJump = PAGESIZE / sizeof(int);
    int arrSize = pageJump * numPages;

    // allocate a large array
    int a[arrSize];
    // initialize backwardly
    for (int i = arrSize - 1; i >= 0; i -= pageJump) {
        a[i] = 0;
    }

    struct timespec start, end;
    long long elapsed_time;

    // Clock start
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (volatile int t = 0; t < numTrials; ++t) {
        for (int i = 0; i < numPages * pageJump; i += pageJump) {
            a[i] += 1;
        }
    }

    // Clock end
    clock_gettime(CLOCK_MONOTONIC, &end);

    elapsed_time = BILLION * (end.tv_sec - start.tv_sec) + end.tv_nsec - start.tv_nsec;

    // take average
    double avgAccess = (double)elapsed_time / (numPages * numTrials);

    // nanoseconds
    printf("%f\n", avgAccess);

    return 0;
}