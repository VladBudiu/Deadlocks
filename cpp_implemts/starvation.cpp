// C++ equivalent of resource_starvation.py
#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
#include <vector>

std::mutex lock1;

void thread_with_exception() {
    try {
        lock1.lock();
        std::cout << "[Exception Thread] Lock acquired" << std::endl;
        throw std::runtime_error("An exception occurred and lock was not released");
    } catch (const std::exception &e) {
        std::cout << "[Exception Thread] Exception caught: " << e.what() << std::endl;
    }
    // Ensure the lock is always released
    if (lock1.try_lock()) {
        lock1.unlock();
        std::cout << "[Exception Thread] Lock released after exception handling" << std::endl;
    }
}

void waiting_thread(int thread_id) {
    std::cout << "[Thread " << thread_id << "] Trying to acquire lock" << std::endl;
    if (lock1.try_lock()) {
        std::cout << "[Thread " << thread_id << "] Acquired lock" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1)); // Simulate work
        lock1.unlock();
        std::cout << "[Thread " << thread_id << "] Released lock" << std::endl;
    } else {
        std::cout << "[Thread " << thread_id << "] Could not acquire lock (potential starvation)" << std::endl;
    }
}

int main() {
    std::thread exception_thread(thread_with_exception);
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::vector<std::thread> waiting_threads;
    for (int i = 1; i <= 3; i++) {
        waiting_threads.emplace_back(waiting_thread, i);
    }
    
    exception_thread.join();
    for (auto& t : waiting_threads) {
        t.join();
    }
    
    std::cout << "[Main] Program finished" << std::endl;
    return 0;
}
