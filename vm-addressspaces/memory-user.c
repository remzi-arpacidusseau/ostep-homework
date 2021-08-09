#include <stdio.h>
#include <stdlib.h>

long BYTES_IN_MB = 1048576;

int main(int argc, char* argv[]) {
  if (argc != 2) {
    printf("usage: memory-user <size in MB\n");
    return 1;
  }
  long size = strtol(argv[1], NULL, 10);
  printf("size: %ld\n", size);

  long size_in_bytes = size * BYTES_IN_MB;
  char* a = malloc(size_in_bytes);
  if (a == NULL) {
    printf("unable to allocate via malloc\n");
    return 1;
  }
  printf("allocated: %ld\n", size_in_bytes);
  while (1) {
    for (int i = 0; i < size_in_bytes; i++) {
      char c = a[i];
      a[i] = 1;
    }
  }
  free(a);
  return 0;
}
