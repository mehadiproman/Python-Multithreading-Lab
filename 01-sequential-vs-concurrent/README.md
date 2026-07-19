# 01 — Sequential vs Concurrent Execution

This experiment explores the fundamental difference between **sequential** and **concurrent** execution using simulated I/O-bound tasks in Python.

The goal is to understand **why concurrency can improve the execution time of independent tasks that spend significant time waiting**.

---

## Objective

By the end of this experiment, I wanted to understand:

* How sequential execution works
* What problem occurs when independent tasks spend time waiting
* What concurrent execution means
* How threads allow waiting periods to overlap
* The basic purpose of `Thread`, `start()`, and `join()`
* Why concurrency can improve I/O-bound workloads
* Why using threads does not automatically make every program faster

---

## 1. Sequential Execution

In sequential execution, one task must finish before the next task begins.

```text
Task A → Finish
             ↓
         Task B → Finish
                      ↓
                  Task C → Finish
```

For three tasks that each take approximately 2 seconds:

```text
Time     0s        2s        4s        6s
         │         │         │         │

Task A   ██████████

Task B             ██████████

Task C                       ██████████
```

The approximate total execution time is:

```text
2s + 2s + 2s ≈ 6 seconds
```

### Key Observation

While one task is waiting, the next independent task has not started yet.

For I/O-bound operations such as network requests, file operations, API calls, and database queries, this can cause waiting time to accumulate.

---

## 2. Simulating I/O-Bound Work

The experiment uses:

```python
time.sleep(2)
```

This simulates a task spending time **waiting** rather than performing continuous CPU-intensive computation.

Conceptually:

```text
Task starts
    │
    ↓
Small amount of work
    │
    ↓
WAITING FOR I/O ............
    │
    ↓
I/O becomes available
    │
    ↓
Task finishes
```

Real-world examples of this type of waiting include:

* Network requests
* API calls
* Database queries
* File reads and writes
* File downloads

---

## 3. Sequential Experiment

The first experiment executes three independent tasks sequentially.

```text
Main Thread

    │
    ├── Task A
    │      └── wait
    │
    ├── Task B
    │      └── wait
    │
    └── Task C
           └── wait
```

Expected execution pattern:

```text
Task A started
Task A finished

Task B started
Task B finished

Task C started
Task C finished
```

### Result

```text
Expected execution time: ~6 seconds
```

The waiting time of every task accumulates because each task must return before the next function call begins.

---

## 4. Concurrent Execution

The second experiment executes the same independent tasks using multiple threads.

Instead of waiting for each task before starting the next one:

```text
Task A ██████████
            Task B ██████████
                        Task C ██████████
```

the tasks can have overlapping lifetimes:

```text
Task A ██████████
Task B ██████████
Task C ██████████
```

Conceptually:

```text
                  Main Thread
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Thread A     Thread B     Thread C
          │            │            │
       Task A        Task B        Task C
          │            │            │
       waiting       waiting       waiting
          │            │            │
          └────────────┼────────────┘
                       ↓
                 Main continues
```

The tasks are **concurrent** because they can make progress during overlapping periods of time.

---

## 5. Core Threading Concepts

### `Thread`

A thread represents a separate path of execution within a process.

```python
thread = threading.Thread(
    target=task,
    args=("Task A", 2)
)
```

Mental model:

```text
Create Worker
     │
     ├── Job → task()
     │
     └── Input → ("Task A", 2)
```

Creating a `Thread` object does not immediately start its execution.

---

### `start()`

```python
thread.start()
```

`start()` begins the thread's execution.

The thread then executes its assigned target function.

```text
Main Thread
     │
     ├── start Thread A ───→ Task A
     │
     ├── start Thread B ───→ Task B
     │
     └── start Thread C ───→ Task C
```

The main thread does not need to wait for Thread A to finish before starting Thread B.

---

### `join()`

```python
thread.join()
```

`join()` makes the **calling thread wait until the target thread finishes**.

In this experiment:

```text
START ALL THREADS
        ↓
Threads execute concurrently
        ↓
JOIN ALL THREADS
        ↓
Main thread continues
```

This ensures execution-time measurement and later program logic happen only after all worker threads have completed.

---

## 6. Sequential vs Concurrent

| Sequential                              | Concurrent                                                |
| --------------------------------------- | --------------------------------------------------------- |
| Tasks execute one after another         | Multiple tasks can make progress during overlapping time  |
| Waiting time accumulates                | Independent waiting periods can overlap                   |
| Simple execution flow                   | Requires concurrency management                           |
| ~6s for three 2-second sequential tasks | ~2s idealized for three concurrent 2-second waiting tasks |

The important conclusion is **not**:

> Threads make Python programs faster.

The more accurate conclusion is:

> Threads can reduce total elapsed time for suitable I/O-bound workloads by allowing independent waiting periods to overlap.

---

## 7. Important `start()` and `join()` Experiment

Two different thread structures were considered.

### Start and Immediately Join

```text
start A
join A

start B
join B

start C
join C
```

Execution becomes effectively sequential:

```text
A ██████████
            B ██████████
                        C ██████████
```

Even though threads are being used, useful concurrency has been lost because the main thread waits after starting each worker.

### Start All, Then Join All

```text
start A
start B
start C

join A
join B
join C
```

Now the worker lifetimes can overlap:

```text
A ██████████
B ██████████
C ██████████
```

This creates an important mental pattern:

```text
CREATE
   ↓
START ALL
   ↓
RUN CONCURRENTLY
   ↓
JOIN ALL
   ↓
CONTINUE
```

### Key Lesson

Using threads does not automatically create useful concurrency.

**How threads are started and synchronized determines the execution behavior.**

---

## 8. Different Task Durations

Consider three independent tasks:

```text
Task A = 2 seconds
Task B = 4 seconds
Task C = 1 second
```

### Sequential

Approximate execution time:

```text
2 + 4 + 1 ≈ 7 seconds
```

```text
A ██
     B ████
            C █
```

### Concurrent

Their waiting periods can overlap:

```text
A ██
B ████
C █
```

The idealized total time approaches the duration of the longest task:

```text
max(2, 4, 1) ≈ 4 seconds
```

Real applications also have scheduling, resource, network, and threading overhead, so this is a mental model rather than a universal performance formula.

---

## 9. Mental Model

### Sequential

```text
ONE EXECUTION FLOW

Main Thread

Task A
   │
   └── waiting
         ↓
      finished
         ↓
Task B
   │
   └── waiting
         ↓
      finished
         ↓
Task C
```

Waiting periods accumulate.

### Concurrent

```text
                    PROCESS
                       │
                  Main Thread
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Thread A     Thread B     Thread C
          │            │            │
       Task A        Task B        Task C
          │            │            │
       waiting       waiting       waiting
          │            │            │
          └────────────┼────────────┘
                       │
                     join()
                       │
                       ↓
                Main continues
```

Independent waiting periods can overlap.

---

## 10. Key Takeaways

* **Sequential execution** performs tasks one after another.
* Sequential execution is not inherently bad; many operations logically depend on previous operations.
* Independent I/O-bound tasks may waste elapsed time when executed sequentially because their waiting periods accumulate.
* **Concurrency** allows multiple tasks to make progress during overlapping periods of time.
* Threads are one mechanism for introducing concurrency.
* `Thread(...)` prepares a worker with a target function and arguments.
* `start()` begins thread execution.
* `join()` makes the calling thread wait for another thread to complete.
* Starting all workers before joining them allows their lifetimes to overlap.
* Threads do not automatically make programs faster.
* The type of workload and the structure of concurrency determine whether threading is useful.

---

## Questions I Can Now Answer

After completing this experiment, I should be able to explain:

1. What is sequential execution?
2. What is concurrent execution?
3. What is the difference between sequential and concurrent progress?
4. Why does waiting time accumulate during sequential I/O-bound work?
5. What is an I/O-bound task?
6. Why can concurrency help independent I/O-bound tasks?
7. What does `threading.Thread()` represent?
8. What does `start()` do?
9. What does `join()` do?
10. Why should independent workers often be started before they are joined?
11. Why does `start → join → start → join` behave differently from `start all → join all`?
12. Does multithreading always make a Python program faster?

---

## Next

**02 — Thread Basics**

The next experiment goes deeper into:

```text
Thread
├── Main Thread vs Worker Thread
├── target
├── args
├── Thread creation
├── Thread execution
└── Multiple worker threads
```

The goal is to move from simply observing concurrency to understanding **what a thread actually represents and how Python manages thread execution**.
