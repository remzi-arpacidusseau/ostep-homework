#include <unistd.h>
#include <stdio.h>

int main(int argc, char** argv) {
  pid_t child_pid = fork();
  if (child_pid == -1) {
    perror("exec-ls");
    return 1;
  } else if (child_pid == 0) {
    // Child
    // char* myargs[2];
    // myargs[0] = "/bin/ls";
    // myargs[1] = NULL;
    // // Args as array, searches for executable
    // execvp(myargs[0], myargs);
    // // Args as list, does not search for executable
    // execl(myargs[0], myargs[0], myargs[1]);
    char* myargs[2];
    myargs[0] = "ls";
    myargs[1] = NULL;
    // Args as list, searches for executable
    execlp(myargs[0], myargs[0], myargs[1]);
  } else {
    // Parent
  }
  return 0;
}
