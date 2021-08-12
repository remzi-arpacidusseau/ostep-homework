#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  int* ptr = (int*) malloc(sizeof(int));
  printf("Allocated mem at: %p\n", ptr);
  *ptr = 1;
  printf("Assign 1 to ptr reference\n");
  return 0;
}
