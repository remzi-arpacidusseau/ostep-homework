// Common usage() prints out stuff for command-line help
void usage() {
    fprintf(stderr, "usage: \n");
    fprintf(stderr, "  -l <number of items each producer produces>\n");
    fprintf(stderr, "  -m <size of the shared producer/consumer buffer>\n");
    fprintf(stderr, "  -p <number of producers>\n");
    fprintf(stderr, "  -c <number of consumers>\n");
    fprintf(stderr, "  -P <sleep string: how each producer should sleep at various points in execution>\n");
    fprintf(stderr, "  -C <sleep string: how each consumer should sleep at various points in execution>\n");
    fprintf(stderr, "  -v [ verbose flag: trace what is happening and print it ]\n");
    fprintf(stderr, "  -t [ timing flag: time entire execution and print total time ]\n");
    exit(1);
}

// Common main() for all four programs
// - Does arg parsing
// - Starts producers and consumers
// - Once producers are finished, puts END_OF_STREAM
//   marker into shared queue to signal end to consumers
// - Then waits for consumers and prints some final info
int main(int argc, char *argv[]) {
    loops = 1;
    max = 1;
    consumers = 1;
    producers = 1;

    char *producer_pause_string = NULL;
    char *consumer_pause_string = NULL;

    opterr = 0;
    int c;
    while ((c = getopt (argc, argv, "l:m:p:c:P:C:vt")) != -1) {
	switch (c) {
	case 'l':
	    loops = atoi(optarg);
	    break;
	case 'm':
	    max = atoi(optarg);
	    break;
	case 'p':
	    producers = atoi(optarg);
	    break;
	case 'c':
	    consumers = atoi(optarg);
	    break;
	case 'P':
	    producer_pause_string = optarg;
	    break;
	case 'C':
	    consumer_pause_string = optarg;
	    break;
	case 'v':
	    do_trace = 1;
	    break;
	case 't':
	    do_timing = 1;
	    break;
	default:
	    usage();
	}
    }

    assert(loops > 0);
    assert(max > 0);
    assert(producers <= MAX_THREADS);
    assert(consumers <= MAX_THREADS);

    if (producer_pause_string != NULL)
	parse_pause_string(producer_pause_string, "producers", producers, producer_pause_times);
    if (consumer_pause_string != NULL) 
	parse_pause_string(consumer_pause_string, "consumers", consumers, consumer_pause_times);

    // make space for shared buffer, and init it ...
    buffer = (int *) Malloc(max * sizeof(int));
    int i;
    for (i = 0; i < max; i++) {
	buffer[i] = EMPTY;
    }

    do_print_headers();

    double t1 = Time_GetSeconds();

    // start up all threads; order doesn't matter here
    pthread_t pid[MAX_THREADS], cid[MAX_THREADS];
    int thread_id = 0;
    for (i = 0; i < producers; i++) {
	Pthread_create(&pid[i], NULL, producer, (void *) (long long) thread_id); 
	thread_id++;
    }
    for (i = 0; i < consumers; i++) {
	Pthread_create(&cid[i], NULL, consumer, (void *) (long long) thread_id); 
	thread_id++;
    }

    // now wait for all PRODUCERS to finish
    for (i = 0; i < producers; i++) {
	Pthread_join(pid[i], NULL); 
    }

    // end case: when producers are all done
    // - put "consumers" number of END_OF_STREAM's in queue
    // - when consumer sees -1, it exits
    for (i = 0; i < consumers; i++) {
	Mutex_lock(&m);
	while (num_full == max) 
	    Cond_wait(empty_cv, &m);
	do_fill(END_OF_STREAM);
	do_eos();
	Cond_signal(fill_cv);
	Mutex_unlock(&m);
    }

    // now OK to wait for all consumers
    int counts[consumers];
    for (i = 0; i < consumers; i++) {
	Pthread_join(cid[i], (void *) &counts[i]); 
    }

    double t2 = Time_GetSeconds();

    if (do_trace) {
	printf("\nConsumer consumption:\n");
	for (i = 0; i < consumers; i++) {
	    printf("  C%d -> %d\n", i, counts[i]);
	}
	printf("\n");
    }

    if (do_timing) {
	printf("Total time: %.2f seconds\n", t2-t1);
    }

    return 0;
}

