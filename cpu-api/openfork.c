#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
  int fd = open("./sample-open.txt", O_WRONLY|O_CREAT|O_TRUNC, S_IRWXU);
  if (fd == -1) {
    perror("openfork");
    return 1;
  }
  pid_t child_pid = fork();
  if (child_pid == -1) {
    perror("openfork");
    return 1;
  }
  char* buffer = "A larger amount of test to write "
    "to the file should appear here with even more text "
    "so that this is very long and might cause both to "
    "write to the same file at the same time but only if "
    "it is long enough to accomplish.";
  ssize_t w = write(fd, buffer, strlen(buffer));
  if (w == -1) {
    perror("openfork");
    return 1;
  }
  close(fd);
  return 0;
}
