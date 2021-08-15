#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef struct {
  size_t size;
  int* d;
} vector;

typedef struct list_node {
  int n;
  struct list_node* next;
} list_node;

typedef struct {
  size_t size;
  list_node* last;
  list_node* nodes;
} list;

int ADDS_AND_GETS = 100000;

vector* createV(void) {
  vector* v = (vector*) malloc(sizeof(vector));
  if (v == NULL) {
    printf("Failed to malloc vector.\n");
    exit(1);
  }
  v->size = 0;
  v->d = NULL;
  return v;
}

vector* addV(vector* v, int i) {
  size_t new_size = v->size + 1;
  v->d = realloc(v->d, new_size * sizeof(int));
  if (v->d == NULL) {
    printf("Failed to realloc data.\n");
    exit(1);
  }
  v->d[new_size-1] = i;
  v->size = new_size;
  return v; 
}

int getV(vector* v, int i) {
  if (v->d == NULL) {
    printf("No values in vector.\n");
    exit(1);
  }
  return v->d[i];
}

size_t sizeV(vector* v) {
  return v->size;
}

list* createL() {
  list* l = (list*) malloc(sizeof(*l));
  if (l == NULL) {
    printf("Unable to allocate list.\n");
    exit(1);
  }
  l->size = 0;
  l->nodes = NULL;
  l->last = NULL;
  return l;
}

void addL(list* l, int i) {
  list_node* node = (list_node*) malloc(sizeof(*node));
  if (node == NULL) {
    printf("Unable to allocate list node.\n");
    exit(1);
  }
  node->n = i;
  node->next = NULL;
  if (l->last != NULL) {
    l->last->next = node;
  } else {
    l->nodes = node;
  }
  l->last = node;
  l->size++;
}

int getL(list* l, int i) {
  list_node* c = l->nodes;
  int ci = 0;
  while (c != NULL) {
    if (ci == i) {
      return c->n;
    }
    c = c->next;
    ci++;
  }
  printf("Out of bounds.\n");
  exit(1);
}

void test_vector() {
  double cpu_time_used = 0;
  clock_t start, end;
  int x;
  
  start = clock();
  vector* v = createV();
  for (int n = 0; n < ADDS_AND_GETS; n++) {
    addV(v, n);
  }
  end = clock();
  cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
  printf("vector add time used: %f\n", cpu_time_used);

  start = clock();
  for (int n = 0; n < ADDS_AND_GETS; n++) {
    x = getV(v, n);
  }
  end = clock();
  cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
  printf("vector get time used: %f\n", cpu_time_used);

  free(v->d);
  free(v);
}

void test_list() {
  double cpu_time_used = 0;
  clock_t start, end;
  int x;

  start = clock();
  list* l = createL();
  for (int n = 0; n < ADDS_AND_GETS; n++) {
    addL(l, n);
  }
  end = clock();
  cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
  printf("list add time used: %f\n", cpu_time_used);

  start = clock();
  for (int n = 0; n < ADDS_AND_GETS; n++) {
    x = getL(l, n);
  }
  end = clock();
  cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
  printf("list get time used: %f\n", cpu_time_used);

  free(l->nodes);
  free(l);
}

void test_list_correct() {
  list* l = createL();
  addL(l, 123);
  addL(l, 234);
  addL(l, 345);
  printf("getL: %d\n", getL(l, 0));
  printf("getL: %d\n", getL(l, 1));
  printf("getL: %d\n", getL(l, 2));
}

int main(int argc, char* argv[]) {
  test_vector();
  test_list();
  //test_list_correct();
  return 0;
}
