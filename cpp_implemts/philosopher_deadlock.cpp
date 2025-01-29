// C++ equivalent of philosophers_all_versions.py
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>

const int NUM_PHILOSOPHERS = 5;
std::vector<std::mutex> forks(NUM_PHILOSOPHERS);

void philosopher_deadlock(int id) {
    int left_fork = id;
    int right_fork = (id + 1) % NUM_PHILOSOPHERS;

    while (true) {
        std::cout << "[Philosopher " << id << "] Thinking..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500)); // Reduced thinking time

        std::cout << "[Philosopher " << id << "] Hungry, trying to acquire forks." << std::endl;
        forks[left_fork].lock();
        std::cout << "[Philosopher " << id << "] Picked up left fork." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200)); // Small delay to increase deadlock probability
        forks[right_fork].lock();
        std::cout << "[Philosopher " << id << "] Picked up right fork." << std::endl;

        std::cout << "[Philosopher " << id << "] Eating..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        forks[left_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released left fork." << std::endl;
        forks[right_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released right fork." << std::endl;
    }
}

int main() {
    std::vector<std::thread> philosophers;
    std::cout << "Running Deadlock-Prone Version..." << std::endl;
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        philosophers.emplace_back(philosopher_deadlock, i);
    }
    for (auto& p : philosophers) {
        p.join();
    }
    return 0;
}
