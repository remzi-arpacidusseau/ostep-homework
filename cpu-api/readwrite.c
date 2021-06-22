#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char** argv) {
  int fd = open("./flag.txt", O_CREAT | O_TRUNC | O_RDWR | O_SYNC, 
      S_IRUSR | S_IWUSR);
  if (fd == -1) {
    perror("open");
    return 1;
  }

  char* to_write = "Hello world";
  if (write(fd, to_write, strlen(to_write)) == -1) {
    perror("write");
    return 1;
  }
  sync();

  char buffer[256];
  lseek(fd, 0, SEEK_SET);
  ssize_t br = read(fd, buffer, sizeof(buffer));
  if (br == -1) {
    perror("read");
    return 1;
  }
  buffer[br] = '\0';
  printf("buffer: %s", buffer);
  close(fd);
  return 0;
}
