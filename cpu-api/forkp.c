#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
  int x = 100;
  pid_t pid = fork();
  if (pid == -1) {
    perror("forkp");
    return 1;
  } else if (pid == 0) {
    // Child process
    printf("child: before: x=%d\n", x);
    x = 101;
    printf("child: after: x=%d\n", x);
  } else {
    // Parent process
    printf("parent: before: x=%d\n", x);
    x = 102;
    printf("parent: after: x=%d\n", x);
  }
  return 0;
}
