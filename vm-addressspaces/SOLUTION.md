# Question 4

When I run `memory-user` with 100MB, the used memory value (returned by `free`) increases by 100MB.
This is expected.

When run with 500MB, the used memory value increases by slightly more than 500MB (501MB).
This is slightly unexpected. I assume there is overhead associated with this program beyond
the allocated memory (via `malloc`).

When run with a large number beyond the total memory (1000MB), the program returns an error
that originates with `malloc` unable to allocate memory. This is expected.

# Question 7

There are more entities than I assumed there would be.
The first few properties in the mapping appear to be `memory-user` code.
The following mappings, labelled `anon`, might be the heap. I see the associated value
is close to the value I pass to `memory-user` program. For example, passing 100MB to the program,
pmap shows an `anon` entry with 102404KB.
I then see what appear to be library entries (`libc`, `ld`).
Finally, towards the end, is the stack.
As specified in the question, there are more entries that I would have expected according to my
mental model of code/stack/heap. Specifically, the code is intermingled with the heap. The stack
does not start at the highest address value.
