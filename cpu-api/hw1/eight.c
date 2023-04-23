#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "wait_and_fork.h"

int main() {
    int pipefd[2]; 

    // Create the pipe
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }

    // Create the first child process
    pid_t child1_pid = fork_or_die();
    if (child1_pid == 0) {
        // In the first child process

        close(pipefd[0]); // Close the read end of the pipe
        dup2(pipefd[1], STDOUT_FILENO); // Redirect standard output to the write end of the pipe
        close(pipefd[1]); // Close the write end of the pipe (not needed anymore)

        execlp("ls", "ls", NULL); // Execute "ls" command

        // If we reach here, an error occurred
        perror("execlp");
        exit(1);
    }

    // Create the second child process
    pid_t child2_pid = fork_or_die();
    if (child2_pid == 0) {
        // In the second child process

        close(pipefd[1]); // Close the write end of the pipe
        dup2(pipefd[0], STDIN_FILENO); // Redirect standard input to the read end of the pipe
        close(pipefd[0]); // Close the read end of the pipe (not needed anymore)

        execlp("sort", "sort", NULL); // Execute "sort" command

        // If we reach here, an error occurred
        perror("execlp");
        exit(1);
    }

    // In the parent process
    close(pipefd[0]); // Close the read end of the pipe
    close(pipefd[1]); // Close the write end of the pipe

    // Wait for both child processes to finish
    waitpid(child1_pid, NULL, 0);
    waitpid(child2_pid, NULL, 0);

    return 0;
}