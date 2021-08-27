#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <pthread.h>

int stick_this_thread_to_core(int core_id);

int main(int argc, char* argv[]) {
  if (argc != 4) {
    fprintf(stderr, "usage: tlb <pagesize> <num_pages> <numtrials>\n");
    return 0;
  }
  int pagesize = atoi(argv[1]);
  int num_pages = atoi(argv[2]);
  int numtrials = atoi(argv[3]);
  
  int ints_per_page = pagesize / sizeof(int);
  int a_size = num_pages * ints_per_page;
  int* a = (int*) calloc(a_size, sizeof(int));

  if (a == NULL) {
    perror("malloc array failed");
    return 0;
  }

  struct timeval* start_tv = (struct timeval*) malloc(sizeof(start_tv));
  struct timeval* end_tv = (struct timeval*) malloc(sizeof(end_tv));

  cpu_set_t cpuset;
  pthread_t thread;
  thread = pthread_self();
  CPU_ZERO(&cpuset);
  CPU_SET(0, &cpuset);
  int s = pthread_setaffinity_np(thread, sizeof(cpuset), &cpuset);
  if (s != 0) {
    perror("setaffinity");
    return 0;
  }

  gettimeofday(start_tv, NULL);

  for (int n = 0; n < numtrials; n++) {
    for (int i = 0; i < a_size; i += ints_per_page) {
      // https://stackoverflow.com/a/2219839
      ((int volatile *)a)[i] += 1;
    }
  }
 
  gettimeofday(end_tv, NULL);

  long long total_accesses = (long long) numtrials * num_pages;
  long diff_sec = end_tv->tv_sec - start_tv->tv_sec;
  long diff_usec = end_tv->tv_usec - start_tv->tv_usec;
  long total_usec = (1000000 * diff_sec) + diff_usec;
  double usec_per_access = ((double) total_usec) / total_accesses;
  double nsec_per_access = usec_per_access * 1000;


  //printf("numtrials: %d\n", numtrials);
  //printf("start sec: %ld, start us: %ld\n", start_tv->tv_sec, start_tv->tv_usec);
  //printf("end sec: %ld, end us: %ld\n", end_tv->tv_sec, end_tv->tv_usec);
  //printf("diff sec: %ld, diff us: %ld\n", diff_sec, diff_usec);
  //printf("total usec: %ld\n", total_usec);
  //printf("a_size: %d\n", a_size);
  //printf("total accesses: %lld\n", total_accesses);
  //printf("usec per access: %f\n", usec_per_access);
  //printf("nsec per access: %f\n", nsec_per_access);
  printf("num_pages: %d, total_usec: %ld, nsec_per_access: %f\n",
      num_pages, total_usec, nsec_per_access);

  free(a);
  free(start_tv);
  free(end_tv);
}
