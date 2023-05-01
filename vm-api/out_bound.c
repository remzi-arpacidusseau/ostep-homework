#include "stdlib.h"
#include "stdio.h"
#include <stdlib.h>

int main() {
    int* data = malloc(100*sizeof(int));
    data[100] = 0;
    return 0;
}