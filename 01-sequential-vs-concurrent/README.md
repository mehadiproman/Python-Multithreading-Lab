1. Sequential Execution

0s                 2s                 4s                 6s

Task A
████████████████████

Task B
                   ████████████████████

Task C
                                      ████████████████████

---------------------------------------------------------------------------

2. 2-second task

CPU work:

██........................██

Waiting:

..████████████████████████..


3. 

Task A → WAITING

Task B → hasn't started

Task C → hasn't started


4. 

CONCURRENT

A ██████████
B ██████████
C ██████████

Total ≈ 2 sec

Python Process

┌──────────────────────────────────────────────┐
│                                              │
│                Main Thread                   │
│                    │                         │
│        ┌───────────┼───────────┐             │
│        ↓           ↓           ↓             │
│    Thread A    Thread B    Thread C          │
│        │           │           │             │
│      Task A      Task B      Task C          │
│                                              │
└──────────────────────────────────────────────┘