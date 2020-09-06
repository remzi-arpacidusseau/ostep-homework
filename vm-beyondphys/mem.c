#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <sys/time.h>

// Simple routine to return absolute time (in seconds).
double Time_GetSeconds() {
    struct timeval t;
    int rc = gettimeofday(&t, NULL);
    assert(rc == 0);
    return (double) ((double)t.tv_sec + (double)t.tv_usec / 1e6);
}

// Program that allocates an array of ints of certain size,
// and then proceeeds to update each int in a loop, forever.
int main(int argc, char *argv[]) {
    if (argc != 2) {
	fprintf(stderr, "usage: spin <memory (MB)>\n");
	exit(1);
    }
    long long int size = (long long int) atoi(argv[1]);
    long long int size_in_bytes = size * 1024 * 1024;

    printf("allocating %lld bytes (%.2f MB)\n", 
	   size_in_bytes, size_in_bytes / (1024 * 1024.0));

    // the big memory allocation happens here
    int *x = malloc(size_in_bytes);
    if (x == NULL) {
	fprintf(stderr, "memory allocation failed\n");
	exit(1);
    }

    long long int num_ints = size_in_bytes / sizeof(int);
    printf("  number of integers in array: %lld\n", num_ints);

    // now the main loop: each time through, touch each integer
    // (and increment its value by 1).
    long long int i = 0;
    double time_since_last_print = 2.0; 
    double t = Time_GetSeconds();
    int loop_count = 0;
    while (1) {
	x[i++] += 1; // main work of loop done here.

	// if we've gone through the whole loop, reset a bunch of stuff
	// and then (perhaps) print out some statistics. 
	if (i == num_ints) {
	    double delta_time = Time_GetSeconds() - t;
	    time_since_last_print += delta_time;
	    if (time_since_last_print >= 0.2) { // only print every .2 seconds
		printf("loop %d in %.2f ms (bandwidth: %.2f MB/s)\n", 
		       loop_count, 1000 * delta_time, 
		       size_in_bytes / (1024.0*1024.0*delta_time));
		time_since_last_print = 0;
	    }

	    i = 0;
	    t = Time_GetSeconds();
	    loop_count++;
	}
    }

    return 0;
}

