#ifndef __pc_header_h__
#define __pc_header_h__

#define MAX_THREADS (100)  // maximum number of producers/consumers

int producers = 1;         // number of producers
int consumers = 1;         // number of consumers

int *buffer;               // the buffer itself: malloc in main()
int max;                   // size of the producer/consumer buffer

int use_ptr  = 0;          // tracks where next consume should come from
int fill_ptr = 0;          // tracks where next produce should go to
int num_full = 0;          // counts how many entries are full

int loops;                 // number of items that each producer produces

#define EMPTY         (-2) // buffer slot has nothing in it
#define END_OF_STREAM (-1) // consumer who grabs this should exit

#endif // __pc_header_h__
 
