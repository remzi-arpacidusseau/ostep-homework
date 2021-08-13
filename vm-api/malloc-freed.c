#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  int* data = (int*) malloc(100 * sizeof(int));
  printf("Allocated array address: %p\n", data);
  for (int i = 0; i < 100; i++) {
    data[i] = i;
  }
  free(data);
  printf("Freed\n");
  printf("Attemt to print...");
  // printf("%d\n", data[0]);
  printf("%d\n", data[50]);
}
