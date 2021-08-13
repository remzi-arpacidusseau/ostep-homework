#include <stdlib.h>
#include <stdio.h>

typedef int* vector;

vector createV(void) {
  return (vector) malloc(sizeof(int));
}

vector add(vector v, int i) {
  int size = *v;
  int new_size = size+1;
  vector ptr = realloc(v, (1+new_size) * sizeof(int));
  ptr[0] = new_size;
  ptr[new_size] = i;
  return ptr; 
}

int get(vector v, int i) {
  return v[1+i];
}

int size(vector v) {
  return v[0];
}

int main(int argc, char* argv[]) {
  vector v = createV();
  v = add(v, 123);
  int x = get(v, 0);
  printf("Value retrieved: %d\n", x);
  return 0;
}
