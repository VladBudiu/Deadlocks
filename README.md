# Deadlocks and Concurrency Demonstrations

Project Overview

This project provides a comprehensive exploration of concurrency issues, such as deadlocks, resource starvation, and circular waits. Through various examples and simulations implemented in Python and C++, the project demonstrates these problems and offers solutions to mitigate or prevent them. The project is intended as an educational resource for understanding concurrency challenges in multithreaded programming.


Prerequisites:

Required Software:
    Python 3.10+
    Python libraries: tkinter, Pillow (Install using pip install pillow)
    C++ compiler (e.g., GCC or Clang)

    


Features

1. Deadlock Examples

self_deadlock.py: Demonstrates a scenario where a single thread enters a deadlock due to incorrect locking mechanisms.

resource_starvation.py: Illustrates resource starvation, a situation where some threads are perpetually denied access to required resources.

2. Dining Philosophers Problem

Located in the philosphers/ directory, this classic concurrency problem is implemented in various ways:

philosopher_deadlock.py: Focuses on the simple deadlock-prone implementation of the problem.

philosopher_random.py: Introduces randomness to reduce contention among philosophers.

philosophers_all_versions.py: Combines multiple implementations, including a simple (deadlock-prone), randomized (to reduce the likelihood of deadlocks), and ordered (to prevent deadlocks).


3. Circular Waits

Found in the circular_wait_cars/ directory, these scripts simulate circular wait scenarios in a road intersection:

circular_wait_with_rollback.py: A simulation where cars enter a deadlock at an intersection and are reset to starting positions with different speeds to resolve the deadlock(the current rollback mechanism).

circular_wait_picture.py: Visualizes the circular wait condition using Tkinter.

helper functions:
kill_threads.py: Demonstrates thread termination as a workaround for deadlocks.
draw_intersection.py: draws the cars and intersection for the initial visual representation of the circular wait example (circular_wait_picture.py)


Under work:
    Implementation of all the presented deadlock scenarios in C++