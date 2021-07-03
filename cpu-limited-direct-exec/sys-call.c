#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>

int main(int argc, char** argv) {
  if (argc > 2) {
    printf("usage: sys-call [iterations]\n");
    return 1;
  }

  int is = 1000;
  if (argc == 2) {
    is = atoi(argv[1]);
  }
  
  struct timeval stv;
  struct timeval etv;

  gettimeofday(&stv, NULL);
  for (int i = 0; i < is; i++) {
    read(STDIN_FILENO, NULL, 0);
  }
  gettimeofday(&etv, NULL);
  
  time_t total_sec = etv.tv_sec - stv.tv_sec;
  suseconds_t total_us = etv.tv_usec - stv.tv_usec;
  long total = (total_sec * 1000000) + total_us;
  double avg = (double) total / is;

  printf("Start sec: %ld us: %d\n", stv.tv_sec, stv.tv_usec);
  printf("End sec: %ld us: %d\n", etv.tv_sec, etv.tv_usec);
  printf("Elapsed sec: %ld us: %d\n", total_sec, total_us);
  printf("Average us: %lf\n", avg);
  return 0;
}
