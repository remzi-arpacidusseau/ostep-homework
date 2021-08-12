#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  int* data = (int*) malloc(100 * sizeof(int));
  printf("Allocated data array: %p\n", data);
  data = 0;
  printf("Set data ptr to 0\n");
  return 0;
}
