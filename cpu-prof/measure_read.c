#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>

#define NUM_MEASUREMENTS 1000

// Function to measure the cost of a system call
double measure_syscall_cost() {
    struct timespec start, end;
    char buf[1];
    int fd;

    // Open a file for reading
    if ((fd = open("/dev/zero", O_RDONLY)) == -1) {
        perror("open");
        return -1;
    }

    // Measure the start time
    if (clock_gettime(CLOCK_REALTIME, &start) == -1) {
        perror("clock_gettime");
        close(fd);
        return -1;
    }

    for (int i = 0; i < NUM_MEASUREMENTS; ++i) {

        // Execute the system call (in this case, a simple read)
        if (read(fd, buf, 1) != 1) {
            perror("read");
            close(fd);
            return -1;
        }

    }

    // Measure the end time
    if (clock_gettime(CLOCK_REALTIME, &end) == -1) {
        perror("clock_gettime");
        close(fd);
        return -1;
    }

    // Calculate the time taken for the system call in nanoseconds
    double time_taken = (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);

    // Close the file
    close(fd);

    // Calculate the average time taken for the system call
    double avg_time_taken = time_taken / NUM_MEASUREMENTS;
    return avg_time_taken;
}

int main() {
    double syscall_cost = measure_syscall_cost();
    if (syscall_cost >= 0) {
        printf("Average cost of read system call (over %d measurements): %lf ns\n", NUM_MEASUREMENTS, syscall_cost);
    } else {
        printf("Error: Unable to measure system call cost.\n");
    }
    return 0;
}