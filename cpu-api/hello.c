#include <unistd.h>
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>

int main(int argc, char** argv) {
  char* flag = "flag";
  int fd = open("./tmp.txt", O_CREAT | O_RDWR | O_TRUNC | O_DSYNC,
      S_IRUSR | S_IWUSR);
  if (fd == -1) {
    perror("hello");
    return 1;
  }
  
  pid_t child_pid = fork();
  if (child_pid == -1) {
    perror("fork");
    return 1;
  }

  if (child_pid == 0) {
    // Child
    printf("hello\n");
    if (write(fd, flag, sizeof(flag)) == -1) {
      perror("write");
      return 1;
    }
  } else {
    // Parent
    char buffer[5];
    struct timespec ts;
    ts.tv_sec = 0;
    ts.tv_nsec = 100 * 1000000; // 100 ms
    buffer[4] = '\0';
    while (strcmp(buffer, flag) != 0) {
      lseek(fd, 0, SEEK_SET);
      if (read(fd, buffer, sizeof(buffer)-1) == -1) {
        perror("read");
        return 1;
      }
      nanosleep(&ts, &ts);
    }
    printf("goodbye\n");
  }

  close(fd);
  return 0;
}
