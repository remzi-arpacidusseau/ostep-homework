#ifndef __common_h__
#define __common_h__

#include <assert.h>
#include <stdlib.h>

#define Malloc(s) ({ void *p = malloc(s); assert(p != NULL); p; })
#define Time_GetSeconds() ({ struct timeval t; int rc = gettimeofday(&t, NULL); assert(rc == 0); (double) t.tv_sec + (double) t.tv_usec/1e6; })

#endif // __common_h__
