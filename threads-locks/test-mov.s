.var flag   2
.var turn  
.var count

.main

# put address of flag into %cx
lea flag, %cx	

# assume thread ID is in %cx (0 or 1, scale by 4 to get proper flag address)
mov %ax, %bx   # ax: self
sub $1, %bx    # bx: 1 - self

.acquire
mov 16(%dx,%cx),%bx
mov 16(%dx,%cx,4),%bx
mov 16 (   %dx , %cx,3) , %bx
mov 16(%dx,%cx),%bx
mov %bx,    (%dx,%cx)
mov %bx,    (%dx,%cx,3)
mov (%dx,%cx),%bx
mov 16(,%cx,2),%bx
mov 16(,,2),%bx
mov 16( %ax,,2),%bx
mov (%dx),%bx
mov 16,%bx
mov - 16 (%dx,%cx,4),%bx
mov -16 (%dx,%cx,4),%bx
mov $-100,%cx	
mov -16  (%dx,%cx,  -4),   %bx
mov -16  (%dx,%cx,  -  4  ),   %bx


.spin1



.release
# mov $0, 0(%dx,%cx,4)



halt

