// C++ equivalent of circular_wait_picture.py
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

    lock2.unlock();
    lock1.unlock();
}

void thread2() {
    lock2.lock();
    std::cout << "[Thread 2] Acquired lock2" << std::endl;

    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << "[Thread 2] Waiting for lock1" << std::endl;
    lock1.lock();
    std::cout << "[Thread 2] Acquired lock1" << std::endl;

    lock1.unlock();
    lock2.unlock();
}

void detect_deadlock() {
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(2));
        // Simulated deadlock detection (not directly implementable without external libraries)
        std::cout << "[Detector] Monitoring for potential deadlock (placeholder logic)" << std::endl;
    }
}

int main() {
    std::thread t1(thread1);
    std::thread t2(thread2);
    std::thread deadlock_detector(detect_deadlock);

    t1.join();
    t2.join();
    deadlock_detector.detach();  // Let the detector run independently

    std::cout << "[Main] Program finished" << std::endl;
    return 0;
}
