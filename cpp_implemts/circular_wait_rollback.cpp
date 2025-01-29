// C++ equivalent of circular_wait_with_rollback.py
#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

// Declare locks
std::mutex lock1;
std::mutex lock2;

void thread1() {
    lock1.lock();
    std::cout << "[Thread 1] Acquired lock1" << std::endl;

    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << "[Thread 1] Waiting for lock2" << std::endl;
    lock2.lock();
    std::cout << "[Thread 1] Acquired lock2" << std::endl;

    std::this_thread::sleep_for(std::chrono::seconds(2));
    lock2.unlock();
    lock1.unlock();
    std::cout << "[Thread 1] Released locks" << std::endl;
}

void thread2() {
    lock2.lock();
    std::cout << "[Thread 2] Acquired lock2" << std::endl;

    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << "[Thread 2] Waiting for lock1" << std::endl;
    lock1.lock();
    std::cout << "[Thread 2] Acquired lock1" << std::endl;

    std::this_thread::sleep_for(std::chrono::seconds(2));
    lock1.unlock();
    lock2.unlock();
    std::cout << "[Thread 2] Released locks" << std::endl;
}

void detect_deadlock(std::thread& t1, std::thread& t2) {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(2));
        if (lock1.try_lock() == false && lock2.try_lock() == false) {
            std::cout << "[Detector] Deadlock detected! Rolling back..." << std::endl;
            lock1.unlock();
            std::cout << "[Detector] Released lock1 to resolve deadlock" << std::endl;
            break;
        }
    }
}

int main() {
    std::thread t1(thread1);
    std::thread t2(thread2);
    std::thread deadlock_detector(detect_deadlock, std::ref(t1), std::ref(t2));

    t1.join();
    t2.join();
    deadlock_detector.join();

    std::cout << "[Main] Program finished" << std::endl;
    return 0;
}
