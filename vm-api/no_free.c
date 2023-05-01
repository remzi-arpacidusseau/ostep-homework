#include "stdlib.h"
#include "stdio.h"
#include <stdlib.h>

int main() {
    int* dont_free_this_ptr = malloc(10000*sizeof(int));
    return 0;
}