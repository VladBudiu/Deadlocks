import tkinter as tk
import threading
import time
import random
import math

NUM_PHILOSOPHERS = 5

# Philosopher states
STATE_THINKING = "THINKING"
STATE_HUNGRY = "HUNGRY"
STATE_EATING = "EATING"

class DiningPhilosophersDemo:
    def __init__(self):
        # Create the Tkinter window and canvas
        self.window = tk.Tk()
        self.window.title("Dining Philosophers Demo")

        self.canvas = tk.Canvas(self.window, width=600, height=600, bg="white")
        self.canvas.pack()

        # Data structures
        self.forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
        self.states = [STATE_THINKING for _ in range(NUM_PHILOSOPHERS)]
        
        # Each philosopher has:
        #  - A circle on canvas for visual
        #  - A text label inside that circle
        self.phil_circles = []
        self.phil_labels = []

        # Optionally, track forks in the GUI (small circles)
        self.fork_circles = []

        # Initialize the geometry on canvas
        self._create_table_graphics()

        # Create and start a thread for each philosopher
        for i in range(NUM_PHILOSOPHERS):
            t = threading.Thread(target=self.philosopher_thread, args=(i,))
            t.daemon = True  # Daemon so program can exit if main window closes
            t.start()

        # Start the Tkinter main loop
        self.window.mainloop()

    def _create_table_graphics(self):
        """
        Draws the round table, philosophers' circles, and fork positions in a circle.
        """
        # Draw a large circle (table) in the center for decoration
        self.canvas.create_oval(50, 50, 550, 550, fill="#ddd", outline="")

        center_x = 300
        center_y = 300
        radius_phil = 200  # distance from center to philosopher
        circle_r = 40      # radius of each philosopher’s circle

        # Place 5 philosophers evenly around the table
        for i in range(NUM_PHILOSOPHERS):
            angle = (2 * math.pi / NUM_PHILOSOPHERS) * i
            # Philosopher's center
            px = center_x + radius_phil * math.sin(angle)
            py = center_y - radius_phil * math.cos(angle)

            # Draw philosopher circle
            circle_id = self.canvas.create_oval(
                px - circle_r, py - circle_r, px + circle_r, py + circle_r,
                fill="white", outline="black", width=2
            )
            # Label with ID or name
            label_id = self.canvas.create_text(px, py, text=f"P{i}", font=("Arial", 14, "bold"))
            
            self.phil_circles.append(circle_id)
            self.phil_labels.append(label_id)

        #draw small circles for forks
        fork_r = 10
        for i in range(NUM_PHILOSOPHERS):
            # Fork is between philosopher i and (i+1)
            angle_f = (2 * math.pi / NUM_PHILOSOPHERS) * (i + 0.5)
            fx = center_x + (radius_phil * 0.7) * math.sin(angle_f)
            fy = center_y - (radius_phil * 0.7) * math.cos(angle_f)
            fork_id = self.canvas.create_oval(
                fx - fork_r, fy - fork_r, fx + fork_r, fy + fork_r,
                fill="gray", outline="black"
            )
            self.fork_circles.append(fork_id)

    def philosopher_thread(self, phil_id):
        """
        Each philosopher cycles:
          1. Think for a while
          2. Become hungry
          3. Pick up left fork, then right fork
          4. Eat
          5. Put down forks
          6. Repeat
        (approach that can lead to deadlock, deadlock scenario forcefully created in the philosopher_all_versions.py)
        """
        left_fork = phil_id
        right_fork = (phil_id + 1) % NUM_PHILOSOPHERS

        while True:
            # 1. THINK
            self.update_state(phil_id, STATE_THINKING)
            time.sleep(random.uniform(1, 3))  # random thinking time

            # 2. Become HUNGRY
            self.update_state(phil_id, STATE_HUNGRY)

            # 3. Try to pick up left fork, then right fork
            self.forks[left_fork].acquire()
            self.update_fork_locked(left_fork, locked=True)
            
            self.forks[right_fork].acquire()
            self.update_fork_locked(right_fork, locked=True)

            # 4. EAT
            self.update_state(phil_id, STATE_EATING)
            time.sleep(random.uniform(1, 3))  # random eating time

            # 5. Put down forks
            self.forks[left_fork].release()
            self.update_fork_locked(left_fork, locked=False)

            self.forks[right_fork].release()
            self.update_fork_locked(right_fork, locked=False)

            # Then loop back to thinking

    def update_state(self, phil_id, new_state):
        """
        Thread-safe update of philosopher's state (and color).
        """
        self.states[phil_id] = new_state

        # Because Tkinter isn't thread-safe, schedule on main thread:
        def _update():
            circle_id = self.phil_circles[phil_id]
            label_id = self.phil_labels[phil_id]

            if new_state == STATE_THINKING:
                color = "white"
            elif new_state == STATE_HUNGRY:
                color = "yellow"
            else:  # EATING
                color = "lightgreen"

            self.canvas.itemconfig(circle_id, fill=color)
            self.canvas.itemconfig(label_id, text=f"P{phil_id}\n{new_state}")

        self.window.after(0, _update)

    def update_fork_locked(self, fork_id, locked):
        """
        Thread-safe update of a fork's color if locked/unlocked.
        """
        def _update():
            fork_circle = self.fork_circles[fork_id]
            color = "red" if locked else "gray"
            self.canvas.itemconfig(fork_circle, fill=color)

        self.window.after(0, _update)

if __name__ == "__main__":
    DiningPhilosophersDemo()
