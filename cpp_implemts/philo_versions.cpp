// C++ equivalent of philosophers_all_versions.py
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>
#include <random>
#include <atomic>

const int NUM_PHILOSOPHERS = 5;
std::vector<std::mutex> forks(NUM_PHILOSOPHERS);
std::random_device rd;
std::mt19937 gen(rd());
std::uniform_int_distribution<int> dist(1, 3);
std::atomic<bool> deadlock_detected(false);

void philosopher_deadlock(int id) {
    int left_fork = id;
    int right_fork = (id + 1) % NUM_PHILOSOPHERS;

    while (!deadlock_detected) {
        std::cout << "[Philosopher " << id << "] Thinking..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500)); // Reduced thinking time

        std::cout << "[Philosopher " << id << "] Hungry, trying to acquire forks." << std::endl;
        forks[left_fork].lock();
        std::cout << "[Philosopher " << id << "] Picked up left fork." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200)); // Small delay to increase deadlock probability

        if (!forks[right_fork].try_lock()) {
            std::cout << "[Philosopher " << id << "] Could not acquire right fork, releasing left fork." << std::endl;
            forks[left_fork].unlock();
            continue;
        }
        std::cout << "[Philosopher " << id << "] Picked up right fork." << std::endl;

        std::cout << "[Philosopher " << id << "] Eating..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        forks[left_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released left fork." << std::endl;
        forks[right_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released right fork." << std::endl;
    }
}

void philosopher_prevention(int id) {
    int left_fork = id;
    int right_fork = (id + 1) % NUM_PHILOSOPHERS;

    while (true) {
        std::cout << "[Philosopher " << id << "] Thinking..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        std::cout << "[Philosopher " << id << "] Hungry, acquiring forks in order." << std::endl;
        int first_fork = std::min(left_fork, right_fork);
        int second_fork = std::max(left_fork, right_fork);
        forks[first_fork].lock();
        std::cout << "[Philosopher " << id << "] Picked up first fork." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200)); // Small delay to prevent deadlock
        forks[second_fork].lock();
        std::cout << "[Philosopher " << id << "] Picked up second fork." << std::endl;

        std::cout << "[Philosopher " << id << "] Eating..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        forks[first_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released first fork." << std::endl;
        forks[second_fork].unlock();
        std::cout << "[Philosopher " << id << "] Released second fork." << std::endl;
    }
}

void detect_deadlock() {
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Allow some time for potential deadlock
    while (true) {
        for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
            if (forks[i].try_lock()) {
                forks[i].unlock();
            } else {
                deadlock_detected = true;
                std::cout << "[Detector] Deadlock detected! Switching to deadlock prevention." << std::endl;
                return;
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
}

int main() {
    std::vector<std::thread> philosophers;
    std::thread detector(detect_deadlock);

    std::cout << "Running Deadlock-Prone Version..." << std::endl;
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        philosophers.emplace_back(philosopher_deadlock, i);
    }
    for (auto& p : philosophers) {
        p.join();
    }

    detector.join();

    std::cout << "Running Deadlock Prevention Version..." << std::endl;
    philosophers.clear();
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        philosophers.emplace_back(philosopher_prevention, i);
    }
    for (auto& p : philosophers) {
        p.join();
    }

    return 0;
}
