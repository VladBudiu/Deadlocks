// C++ equivalent of philosopher_random.py
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>
#include <random>

const int NUM_PHILOSOPHERS = 5;
std::vector<std::mutex> forks(NUM_PHILOSOPHERS);
std::random_device rd;
std::mt19937 gen(rd());
std::uniform_int_distribution<int> dist(1, 3);

void philosopher(int id) {
    int left_fork = id;
    int right_fork = (id + 1) % NUM_PHILOSOPHERS;

    while (true) {
        // Thinking
        std::cout << "[Philosopher " << id << "] Thinking..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(dist(gen)));

        // Hungry
        std::cout << "[Philosopher " << id << "] Hungry, trying to acquire forks." << std::endl;
        
        // Picking up forks in a random order to prevent circular wait
        if (id % 2 == 0) {
            forks[left_fork].lock();
            std::cout << "[Philosopher " << id << "] Picked up left fork." << std::endl;
            forks[right_fork].lock();
            std::cout << "[Philosopher " << id << "] Picked up right fork." << std::endl;
        } else {
            forks[right_fork].lock();
            std::cout << "[Philosopher " << id << "] Picked up right fork." << std::endl;
            forks[left_fork].lock();
            std::cout << "[Philosopher " << id << "] Picked up left fork." << std::endl;
        }

        // Eating
        std::cout << "[Philosopher " << id << "] Eating..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(dist(gen)));

        // Put down forks
        forks[left_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released left fork." << std::endl;
        forks[right_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released right fork." << std::endl;
    }
}

int main() {
    std::vector<std::thread> philosophers;
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        philosophers.emplace_back(philosopher, i);
    }
    
    for (auto& p : philosophers) {
        p.join();
    }

    return 0;
}
