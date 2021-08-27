#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

int main(int argc, char* argv[]) {
  if (argc != 4) {
    fprintf(stderr, "usage: tlb <pagesize> <numpages> <numtrials>\n");
    return 0;
  }
  int pagesize = atoi(argv[1]);
  int numpages = atoi(argv[2]);
  int numtrials = atoi(argv[3]);
  
  int jump = pagesize / sizeof(int);
  int a_size = numpages * jump;
  int a[a_size];

  for (int i = 0; i < a_size; i++) {
    a[i] = 0;
  }

  struct timeval* start_tv = (struct timeval*) malloc(sizeof(start_tv));
  struct timeval* end_tv = (struct timeval*) malloc(sizeof(end_tv));


  gettimeofday(start_tv, NULL);

  for (int n = 0; n < numtrials; n++) {
    for (int i = 0; i < a_size; i += jump) {
      a[i] += 1;
    }
  }
 
  gettimeofday(end_tv, NULL);

  long long total_accesses = (long long) numtrials * a_size;
  long diff_sec = end_tv->tv_sec - start_tv->tv_sec;
  long diff_usec = end_tv->tv_usec - start_tv->tv_usec;
  long total_usec = (1000000 * diff_sec) + diff_usec;
  double usec_per_access = ((double) total_usec) / total_accesses;
  double nsec_per_access = usec_per_access * 1000;
  double nsec_per_access_v2 = ((double) total_usec) / (total_accesses / 1000);


  printf("numtrials: %d\n", numtrials);
  printf("start sec: %ld, start us: %ld\n", start_tv->tv_sec, start_tv->tv_usec);
  printf("end sec: %ld, end us: %ld\n", end_tv->tv_sec, end_tv->tv_usec);
  printf("diff sec: %ld, diff us: %ld\n", diff_sec, diff_usec);
  printf("total usec: %ld\n", total_usec);
  printf("a_size: %d\n", a_size);
  printf("total accesses: %lld\n", total_accesses);
  printf("usec per access: %f\n", usec_per_access);
  printf("nsec per access: %f\n", nsec_per_access);
  printf("nsec per access_v2: %f\n", nsec_per_access_v2);

  free(start_tv);
  free(end_tv);

  printf("done\n");
}
