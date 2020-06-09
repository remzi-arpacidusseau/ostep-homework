.var mutex
.var count

.main
.top
mov  %sp, %bp
lea  mutex, %ax
push %ax
call .lock
pop

# critical section
mov  count, %ax     # get the value at the address
add  $1, %ax        # increment it
mov  %ax, count     # store it back

# release lock
lea  mutex, %ax
push %ax
call .unlock
pop

# see if we're still looping
sub  $1, %bx
test $0, %bx
jgt .top	

halt

.lock
.acquire
push %bp
mov  %sp, %bp
mov  8(%bp), %ax    # get addr of flag
mov  (%ax),   %cx   # get value of flag 
test $0, %cx        # if we get 0 back: lock is free!
jne  .acquire       # if not, try again
mov  $1, (%cx)      # store 1 into flag
pop  %bp
ret

.unlock
mov  8(%bp), %ax    # all done: release lock by clearing it
mov  $0, (%ax)      # clear
ret
