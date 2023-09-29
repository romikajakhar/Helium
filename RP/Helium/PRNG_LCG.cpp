#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define RAND_LOCAL_MAX 2147483647

uint32_t next = 2063485727; // global variable

uint32_t rand_num() {
    next = (next * 1103515245 + 12345) % RAND_LOCAL_MAX;
    return next;
}

int main() {
    int j;

    for (j = 0; j < 10; j++) {
        printf("%u\n", rand_num() % 8);
       // printf("%u\n", next);
    }

    return 0;
}



