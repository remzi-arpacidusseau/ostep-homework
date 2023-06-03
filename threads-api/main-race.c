#include <stdio.h>
#include "common_threads.h"

int balance = 0;
pthread_mutex_t lock; // Declare a mutex lock

void* worker(void* arg) {
    pthread_mutex_lock(&lock); // Acquire the lock
    balance++; // protected access 
    pthread_mutex_unlock(&lock); // Release the lock
    return NULL;
}

int main(int argc, char *argv[]) {
    pthread_mutex_init(&lock, NULL); // Initialize the mutex lock
    pthread_t p;
    Pthread_create(&p, NULL, worker, NULL);
    pthread_mutex_lock(&lock); // Acquire the lock
    balance++; // protected access
    pthread_mutex_unlock(&lock); // Release the lock
    Pthread_join(p, NULL);
    pthread_mutex_destroy(&lock); // Destroy the mutex lock
    return 0;
}
