#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  int* ptr; 
  ptr = NULL;
  int i = *ptr;
  printf("Ptr dereference: %d\n", i);
}
