#include <stdio.h>
#include <stdlib.h>    
#include <sys/_types/_pid_t.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char *argv[]) {

    pid_t process_id = getpid();
    printf("Process ID of the program: %d\n", process_id);

    if (argc == 1) {
        printf("Please give number of megabytes you would like to allocate.\n");
        return 1;
    }

    int megabytes_wanted = atoi(argv[1]);

    // dynamically allocate array on heap
    int* my_array = (int*)malloc(megabytes_wanted * 1000000);
    
    if (my_array == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    int runtime;
    if (argc == 2) {
        runtime = 20;
    } else if (argc == 3) {
        runtime = atoi(argv[1]);
    } else {
        printf("Please give # of MB and/or run duration in seconds only.\n");
        return 1;
    }


    int arr_size = megabytes_wanted * 1000000 / sizeof(int);

    time_t start_time, current_time;
    time(&start_time);

    while (1) {
        time(&current_time);
        if (difftime(current_time, start_time) >= runtime) {
            break; // Exit the loop
        }

        // touch all entries
        for (int i=0; i < arr_size; i++) {
            my_array[i] = 1;
        }
    }


    free(my_array);

    return 0;
}