#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("usage: piper <string>\n");
    return 1;
  }

  int pipefd[2];
  if (pipe(pipefd) == -1) {
    perror("pipe");
    return 1;
  }

  pid_t child_1_pid = fork();
  if (child_1_pid == -1) {
    perror("piper");
    return 1;
  } 

  if (child_1_pid == 0) {
    // Child 1: writer
    printf("child1: pid(%d)\n", getpid());
    close(pipefd[0]); // Close read end of pipe
    if (write(pipefd[1], argv[1], strlen(argv[1])) == -1) {
      perror("write");
      return 1;
    }
    close(pipefd[1]);
    return 0;
  } 

  // Parent
  pid_t child_2_pid = fork();
  if (child_2_pid == -1) {
    perror("piper");
    return 1;
  } 
  
  if (child_2_pid == 0) {
    // Child 2
    char buffer[strlen(argv[1])];
    printf("child2: pid(%d)\n", getpid());
    close(pipefd[1]); // Close write end of pipe
    if (read(pipefd[0], buffer, strlen(argv[1])) == -1) {
      perror("read");
      return 1;
    }
    printf("child2: %s\n", buffer);
    close(pipefd[0]);
    return 0;
  }
  
  // Parent
  printf("parent: pid(%d)\n", getpid());
  waitpid(child_1_pid, NULL, 0);
  waitpid(child_2_pid, NULL, 0);
  return 0;
}
