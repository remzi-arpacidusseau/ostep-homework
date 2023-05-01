#include "stdlib.h"
#include "stdio.h"
#include <stdlib.h>

int main() {
    int* data = malloc(100*sizeof(int));
    data[50] = 50;
    free(data);

    printf("value at data[50]: %d\n", data[50]);
    return 0;
}