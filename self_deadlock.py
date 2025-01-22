import threading

lock1 = threading.Lock()

def critical_section():
    lock1.acquire()
    print("Lock aquired first time")
    
    """
    Do some work here

    """
    print("Thread is trying to acquire the lock again, but it has not released it yet")
    try:
        lock1.acquire()
        print("Lock aquired second time")
    finally:
        lock1.release()

    lock1.release()


thread = threading.Thread(target=critical_section)
thread.start()
thread.join()
print("Thread finished")