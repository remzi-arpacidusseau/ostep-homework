#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

int main(int argc, char** argv) {
  pid_t child_pid = fork();
  if (child_pid == -1) {
    perror("closestdout");
    return 1;
  } else if (child_pid == 0) {
    // Child
    printf("child: pid(%d)\n", getpid());
    if (close(STDOUT_FILENO) == -1) {
      perror("closestdout");
      return 1;
    }
    printf("child: close stdout\n");
  } else {
    // Parent
    wait(NULL);
    printf("parent: pid(%d)\n", getpid());
  }
  return 0;
};
