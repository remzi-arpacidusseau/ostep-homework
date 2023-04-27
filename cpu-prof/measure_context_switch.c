#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/types.h>
#include <sys/wait.h>

#define NUM_MEASUREMENTS 1000

double measure_context_switch() {
    int pipe1[2], pipe2[2];
    pid_t pid;
    char buf[1];

    if (pipe(pipe1) == -1 || pipe(pipe2) == -1) {
        perror("pipe");
        return -1;
    }

    pid = fork();

    if (pid == -1) {
        perror("fork");
        return -1;
    } else if (pid == 0) {
        // Child process
        for (int i = 0; i < NUM_MEASUREMENTS; ++i) {
            if (read(pipe1[0], buf, 1) != 1) {
                perror("read");
                exit(EXIT_FAILURE);
            }
            if (write(pipe2[1], "a", 1) != 1) {
                perror("write");
                exit(EXIT_FAILURE);
            }
        }
        exit(EXIT_SUCCESS);
    } else {
        // Parent process
        struct timespec start, end;

        if (clock_gettime(CLOCK_REALTIME, &start) == -1) {
            perror("clock_gettime");
            return -1;
        }

        for (int i = 0; i < NUM_MEASUREMENTS; ++i) {

            if (write(pipe1[1], "a", 1) != 1) {
                perror("write");
                return -1;
            }
            if (read(pipe2[0], buf, 1) != 1) {
                perror("read");
                return -1;
            }

        }

        int status;
        wait(&status);

        if (clock_gettime(CLOCK_REALTIME, &end) == -1) {
            perror("clock_gettime");
            return -1;
        }

        double time_taken = (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);

        double avg_time_taken = time_taken / (2 * NUM_MEASUREMENTS); // Divide by 2 for one-way context switch time
        return avg_time_taken;
    }
}

int main() {
    double context_switch_time = measure_context_switch();
    if (context_switch_time >= 0) {
        printf("Average context switch time (over %d measurements): %lf ns\n", NUM_MEASUREMENTS, context_switch_time);
    } else {
        printf("Error: Unable to measure context switch time.\n");
    }
    return 0;
}
