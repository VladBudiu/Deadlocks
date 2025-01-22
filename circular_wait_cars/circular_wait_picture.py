import threading
import time
import tkinter as tk
import intersection2

# Create locks
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread_1():
    lock1.acquire()
    print("Thread 1 acquired lock1")

    time.sleep(1)

    print("Thread 1 waiting for lock2")
    lock2.acquire()
    print("Thread 1 acquired lock2")

    lock1.release()
    lock2.release()

def thread_2():
    lock2.acquire()
    print("Thread 2 acquired lock2")

    time.sleep(1)

    print("Thread 2 waiting for lock1")
    lock1.acquire()
    print("Thread 2 acquired lock1")

    lock1.release()
    lock2.release()

def detect_deadlock():
    # time.sleep(3)  # Allow threads to potentially deadlock
    running = True
    while running:
        if lock1.locked() and lock2.locked():
            time.sleep(2)
            print("Deadlock detected! Visualizing...")
            intersection2.draw_intersection_with_moving_cars()
            running = False


# Create and start threads
t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)

t1.start()
t2.start()

# Start a thread to detect deadlock
deadlock_detector = threading.Thread(target=detect_deadlock)
deadlock_detector.start()

# Wait for the threads to finish
t1.join()
t2.join()

deadlock_detector.join()

print("Main thread finished")
