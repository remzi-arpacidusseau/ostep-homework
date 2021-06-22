#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char** argv) {
  pid_t child_pid = fork();
  if (child_pid == -1) {
    perror("waitchild");
    return 1;
  } else if (child_pid == 0) {
    // Child
    printf("child: pid(%d)\n", getpid());
    // pid_t wait_for = wait(NULL);
    // perror(NULL);
    // printf("child: wait for %d\n", wait_for);
  } else {
    // Parent
    printf("parent: pid(%d)\n", getpid());
    // pid_t wait_for = wait(NULL);
    pid_t wait_for = waitpid(child_pid, NULL, 0);
    printf("parent: wait for %d\n", wait_for);
  }
  return 0;
}
