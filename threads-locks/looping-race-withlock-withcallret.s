.var mutex
.var count

.main
.top	
push mutex
call .lock
pop

# critical section
mov  count, %ax     # get the value at the address
add  $1, %ax        # increment it
mov  %ax, count     # store it back

# release lock
push mutex
call .unlock
pop

# see if we're still looping
sub  $1, %bx
test $0, %bx
jgt .top	

halt

.lock
.acquire
mov  -4(%sp), %ax   # get addr of flag
mov  $1, %cx        # 
xchg %cx, (%ax)     # atomic swap of 1 and flag
test $0, %cx        # if we get 0 back: lock is free!
jne  .acquire       # if not, try again
ret

.unlock
mov  -4(%sp), %ax   # all done: release lock by clearing it
mov  $0, (%ax)      # 
ret


