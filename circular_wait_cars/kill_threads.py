import threading
import ctypes
import time

def _get_thread_id(thread: threading.Thread) -> int:
    """
    Tries to extract the 'thread id'.  
    """
    # Thread objects in Python 3.x have a private attribute "_thread_id".
    if hasattr(thread, "_thread_id"):
        return thread._thread_id


    if hasattr(thread, "native_id"):
        return thread.native_id

    raise ValueError("Could not find the thread ID via _thread_id")


def kill_thread(thread: threading.Thread):
    """
    Forcibly raise an exception in a thread to (attempt to) kill it.
    """
    tid = _get_thread_id(thread)
    if not tid:
        print("Could not determine thread id, can't kill thread.")
        return

    # If it’s 0, something went wrong; if >1, we’ve targeted multiple threads.
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid),
        ctypes.py_object(SystemExit)  # we inject SystemExit, could also use another exception
    )
    if res == 0:
        print("Thread id not found - no exception raised.")
    elif res > 1:
        # If we get here, we actually affected multiple threads—undo the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        print("Multiple threads were affected, undone the effect. Target not singular.")
    else:
        print(f"Successfully raised exception in thread {thread.name} (id {tid}).")


