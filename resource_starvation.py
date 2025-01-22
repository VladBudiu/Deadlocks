import threading
import time

lock1 = threading.Lock()

def thread_with_exception():
    try:
        lock1.acquire()
        print("Lock acquired by exception thread")
        raise Exception("An exception occurred and lock was not released")
        # lock1.release() is never reached due to the exception
    except Exception as e:
        print("Exception caught:", e)
    finally:
        # Intentionally commenting out lock release to simulate starvation
        lock1.release()
        pass

def waiting_thread(thread_id):
    print(f"Thread {thread_id} trying to acquire lock")
    acquired = lock1.acquire(timeout=5)  # Adding timeout to detect starvation
    if acquired:
        print(f"Thread {thread_id} acquired lock")
        lock1.release()
    else:
        print(f"Thread {thread_id} could not acquire lock (starvation)")

# Create threads
exception_thread = threading.Thread(target=thread_with_exception)
waiting_threads = [threading.Thread(target=waiting_thread, args=(i,)) for i in range(1, 4)]

# Start the exception thread
exception_thread.start()

# Ensure the exception thread executes first
time.sleep(1)

# Start waiting threads
for thread in waiting_threads:
    thread.start()

# Join threads
exception_thread.join()
for thread in waiting_threads:
    thread.join()

print("Program finished")
