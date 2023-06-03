# Solutions

**Q1:**  
First build main-race.c. Examine the code so you can see the (hopefully obvious) data race in the code. Now run helgrind (by typing `valgrind --tool=helgrind main-race`) to see how it reports the race. Does it point to the right lines of code? What other information does it give to you?

**A1:**  
*It showed the right lines of code (8, 15) and possible race conditions, but did not reveal the variable name.*
```bash
==30760== Possible data race during read of size 4 at 0x100008020 by thread #2
==30760== Locks held: none
==30760==    at 0x100003E1A: worker (main-race.c:8)
==30760==    by 0x100630108: _pthread_start (in /usr/lib/system/libsystem_pthread.dylib)
==30760==    by 0x10062BB8A: thread_start (in /usr/lib/system/libsystem_pthread.dylib)
==30760==
==30760== This conflicts with a previous write of size 4 by thread #1
==30760== Locks held: none
==30760==    at 0x100003EAE: main (main-race.c:15)
==30760==  Address 0x100008020 is in a rw- mapped file ./main-race segment
```

**Q2:**  
What happens when you remove one of the offending lines of code? Now add a lock around one of the updates to the shared variable, and then around both. What does helgrind report in each of these cases?

**A2:**  
*When removing only one line, the output from helgrind showed some false positive data race for pthread create and join APIs. For adding one lock, helgrind still catch the error. But when adding mutex for both update, the outputs left with false positive info.*

**Q3:**  
Now let’s look at main-deadlock.c. Examine the code. This code has a problem known as deadlock (which we discuss in much more depth in a forthcoming chapter). Can you see what problem it might have?

**A3:**  
*If p1 hold m1 and p2 hold m2 before p1 hold m2 and p2 hold m1, this will never end and enter deadlock situation.*

**Q4:**  
Now run helgrind on this code. What does helgrind report?

**A4:**  
*Did not point out the deadlock scenario clearly.*
```bash
==31568== Possible data race during read of size 4 at 0x100008070 by thread #3
==31568== Locks held: none
==31568==    at 0x10062B5AD: pthread_mutex_lock (in /usr/lib/system/libsystem_pthread.dylib)
==31568==    by 0x100630108: _pthread_start (in /usr/lib/system/libsystem_pthread.dylib)
==31568==    by 0x10062BB8A: thread_start (in /usr/lib/system/libsystem_pthread.dylib)
==31568==
==31568== This conflicts with a previous write of size 4 by thread #2
==31568== Locks held: none
==31568==    at 0x10062B813: _pthread_mutex_check_init_slow (in /usr/lib/system/libsystem_pthread.dylib)
==31568==    by 0x10062B658: _pthread_mutex_lock_init_slow (in /usr/lib/system/libsystem_pthread.dylib)
==31568==    by 0x100003AF1: worker (main-deadlock.c:11)
==31568==    by 0x100630108: _pthread_start (in /usr/lib/system/libsystem_pthread.dylib)
==31568==    by 0x10062BB8A: thread_start (in /usr/lib/system/libsystem_pthread.dylib)
==31568==  Address 0x100008070 is in a rw- mapped file ./main-deadlock segment
```

**Q5:**  
Now run helgrind on main-deadlock-global.c. Examine the code; does it have the same problem that main-deadlock.c has? Should helgrind be reporting the same error? What does this tell you about tools like helgrind?

**A5:**  
*IMHO, it's correct with global lock. But helgrind stilled showed the same error which tells that helgrind might not be reliable.*

**Q6:**  
Let’s next look at main-signal.c. This code uses a variable (done) to signal that the child is done and that the parent can now continue. Why is this code inefficient? (what does the parent end up spending its time doing, particularly if the child thread takes a long time to complete?)

**A6:**  
*The while loop in main thread would contend for CPU until child change the cv.*

**Q7:**  
Now run helgrind on this program. What does it report? Is the code correct?

**A7:**  
*It did not catch anythin useful. The code is correct but not thread safe.*

**Q8:**  
Now look at a slightly modified version of the code, which is found in main-signal-cv.c. This version uses a condition variable to do the signaling (and associated lock). Why is this code preferred to the previous version? Is it correctness, or performance, or both?

**A8:**  
*It is more thread safe (lock protected) and performant (wait api suspend the thread until conditional variable is signaled thus avoid busy waiting).

**Q9:**  
Once again run helgrind on main-signal-cv. Does it report any errors?

**A9:**  
*Nothing useful.*
