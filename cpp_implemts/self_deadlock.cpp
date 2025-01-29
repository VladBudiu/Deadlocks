// C++ equivalent of self_deadlock.py
#include <iostream>
#include <thread>
#include <mutex>

std::mutex lock1;

void critical_section() {
    lock1.lock();
    std::cout << "[Thread] Lock acquired first time" << std::endl;
    
    // Simulate work in the critical section
    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << "[Thread] Trying to acquire the lock again" << std::endl;
    
    // This will cause a deadlock as the same thread tries to acquire the lock again
    lock1.lock();
    std::cout << "[Thread] Lock acquired second time (this line will never be reached)" << std::endl;

    lock1.unlock();
    lock1.unlock();
}

int main() {
    std::thread t(critical_section);
    t.join();
    
    std::cout << "[Main] Program finished" << std::endl;
    return 0;
}
