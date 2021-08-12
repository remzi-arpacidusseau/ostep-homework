# Question 1

## Seed 1

Total tickets: 153
Job0: 0-83, Job1: 84-108, Job2: 109-152
Winners:
1. 119,Job2 (Job2 remaining 3)
2. 9,Job0 (Job 0 remaining 0)

Total tickets: 69
Job1:0-24,Job2:25-68
3. 19,Job1 (Job1 remaining 6)
4. 57, Job2 (Job2 remaining 2)
5. 37, Job2 (Job2 remaining 1)
6. 68, Job2 (Job2 remaining 0)

**The rest is Job1**

## Seed 2

Total tickets: 197
Job0: 0-93, Job1: 94-166, Job2: 167-196

1. 169, Job2 (Job2 remaining 5)
2. 42, Job0 (Job0 remaining 8)
3. 54, Job0 (Job0 remaining 7)
4. 192, Job2 (Job2 remaining 5)
5. 28, Job0 (Job0 remaining 6)
6. 123, Job1 (Job1 remaining 7)
7. 22, Job0 (Job0 remaining 5)
8. 167, Job2 (Job2 remaining 4)
9. 53, Job0 (Job0 remaining 4)
10. 63, Job0 (Job0 remaining 3)
11. 28, Job0 (Job0 remaining 2)
12. 124, Job1 (Job1 remaining 6)
13. 70, Job0 (Job0 remaining 1)
14. 61, Job0 (Job0 remaining 0)
Job0 Done
Total tickets: 103
Job0: --, Job1: 0-72, Job2: 73-102
15. 55, Job1 (Job1 remaining 5)
16. 92, Job2 (Job2 remaining 3)
17. 48, Job1 (Job1 remaining 4)
18. 16, Job1 (Job1 remaining 3)
19. 41, Job1 (Job1 remaining 2)
20. 87, Job2 (Job2 remaining 2)
21. 47, Job1 (Job1 remaining 1)
22. 65, Job1 (Job1 remaining 0)
Job1 Done
**Remaining is Job2**

## Seed 3

Total tickets: 120
Job0: 0-53, Job1: 54-113, Job2: 114-119

1. 88, Job1 (Job1 remaining 2)
2. 109, Job1 (Job1 remaining 1)
3. 34, Job0 (Job0 remaining 1)
4. 91, Job1 (Job1 remaining 0)
Job1 Done
Total tickets: 60
Job0: 0-53, Job1: --, Job2: 54-59
5. 5, Job0 (Job0 remaining 0)
Job0 Done
**Remaining are Job2**

## Question 2

When the number of tickets are imbalanced as such, the job with more tickets
is likely to complete before the other job starts.
It is possible job0 will run before job1, but not likely.
Specifically, there is a 1 in 101 chance of this occuring.
This imblanace causes the average response time to increase.

# Question 3

Unfairness metric: Tc1/Tc2
Gather unfairness metrics:
1. 196/200 = 0.98
2. 190/200 = 0.95
3. 196/200 = 0.98
4. 199/200 = 0.995
5. 181/200 = 0.905
6. 193/200 = 0.965
7. 185/200 = 0.925
8. 191/200 = 0.955
9. 192/200 = 0.96
10. 197/200 = 0.985

Avg5 = 0.962
Avg10 = 0.96

## As quantum size gets larger...

q=2
1. 194/200 = 0.97
2. 198/200 = 0.99
3. 194/200 = 0.97
4. 188/200 = 0.94
5. 170/200 = 0.85

Avg = 0.944

q=5
1. 190/200 = 0.95
2. 175/200 = 0.875
3. 185/200 = 0.925
4. 185/200 = 0.925
5. 190/200 = 0.95

Avg = 0.925
