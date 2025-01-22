import tkinter as tk
import threading
import time
import ctypes
import kill_threads
from PIL import Image, ImageTk, ImageOps


###############################################################################
# 1. Optional Concurrency Threads (Do Not Affect Rollback)
###############################################################################
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread_1():
    lock1.acquire()
    print("[Thread 1] Acquired lock1")
    time.sleep(1)
    print("[Thread 1] Waiting for lock2")
    lock2.acquire()
    print("[Thread 1] Acquired lock2")
    time.sleep(2)
    lock2.release()
    print("[Thread 1] Released locks")

def thread_2():
    lock2.acquire()
    print("[Thread 2] Acquired lock2")
    time.sleep(1)
    print("[Thread 2] Waiting for lock1")
    lock1.acquire()
    print("[Thread 2] Acquired lock1")
    time.sleep(2)
    lock1.release()
    lock2.release()
    print("[Thread 2] Released locks")


###############################################################################
# 2. GUI Code: Rollback to START Positions on Collision, Then Different Speeds
###############################################################################
def draw_intersection_with_moving_cars():
    """
    1) Cars start outside the intersection, all moving at the same speed.
    2) If they collide, reset them to their initial starting positions.
    3) After resetting, each car moves at a distinct speed so they won't collide again.
    4) They then pass fully through the intersection and off the canvas.
    """

    #####################
    # 2.1 Collision Test
    #####################

    CLOSE_WINDOW_WHEN_DONE = True #useful variable to close the window when the cars are done moving


    def boxes_collide(box1, box2):
        """Check if two bounding boxes overlap."""
        if not box1 or not box2:
            return False
        return not (
            box1[2] < box2[0] or  # box1's right < box2's left
            box1[0] > box2[2] or  # box1's left  > box2's right
            box1[3] < box2[1] or  # box1's bottom < box2's top
            box1[1] > box2[3]     # box1's top > box2's bottom
        )

    def any_collision():
        """Check collisions among all four cars (pairwise)."""
        bbox_top    = canvas.bbox(car_top)
        bbox_bottom = canvas.bbox(car_bottom)
        bbox_left   = canvas.bbox(car_left)
        bbox_right  = canvas.bbox(car_right)

        pairs = [
            (bbox_top,    bbox_bottom),
            (bbox_top,    bbox_left),
            (bbox_top,    bbox_right),
            (bbox_bottom, bbox_left),
            (bbox_bottom, bbox_right),
            (bbox_left,   bbox_right),
        ]
        for (b1, b2) in pairs:
            if boxes_collide(b1, b2):
                return True
        return False

    ##################################
    # 2.2 Movement & "Rollback" Logic
    ##################################
    # Speeds:
    #  - Before collision: all cars have the same speed.
    #  - After collision (once reset to start): each car has a distinct speed.
    SPEED_BEFORE = 10
    SPEEDS_AFTER = {
        "car_top":    7,
        "car_bottom": 12,
        "car_left":   9,
        "car_right":  15,
    }
    DELAY = 200  # ms delay between moves

    # This flag tracks whether we've already rolled back once
    after_reset = False

    # -----------------------
    # 2.2.1: Initial Positions
    # -----------------------
    # Store the initial starting positions so we can reset to them on collision.
    init_top_x,    init_top_y    = 225, -60
    init_bottom_x, init_bottom_y = 275, 560
    init_left_x,   init_left_y   = -60, 275
    init_right_x,  init_right_y  = 560, 225

    # Current positions (these will update in move_cars)
    car_top_x,    car_top_y    = init_top_x,    init_top_y
    car_bottom_x, car_bottom_y = init_bottom_x, init_bottom_y
    car_left_x,   car_left_y   = init_left_x,   init_left_y
    car_right_x,  car_right_y  = init_right_x,  init_right_y

    def reset_to_start():
        """Move all cars back to their initial starting positions."""
        print("[NOTE] Deadlock scenario: all car threads are waiting for each other, they cannot leave the intersection.")
        time.sleep(3)  # pause for effect
        print("[GUI] Collision! Resetting cars back to the beginning, then they'll move at different speeds...")
        time.sleep(2)  # pause for effect
        nonlocal car_top_x, car_top_y
        nonlocal car_bottom_x, car_bottom_y
        nonlocal car_left_x, car_left_y
        nonlocal car_right_x, car_right_y

        # Set the current positions to the initial ones
        car_top_x,    car_top_y    = init_top_x,    init_top_y
        car_bottom_x, car_bottom_y = init_bottom_x, init_bottom_y
        car_left_x,   car_left_y   = init_left_x,   init_left_y
        car_right_x,  car_right_y  = init_right_x,  init_right_y

        # Update the canvas with these positions
        canvas.coords(car_top,    car_top_x,    car_top_y)
        canvas.coords(car_bottom, car_bottom_x, car_bottom_y)
        canvas.coords(car_left,   car_left_x,   car_left_y)
        canvas.coords(car_right,  car_right_x,  car_right_y)

    def move_cars():
        nonlocal car_top_x, car_top_y
        nonlocal car_bottom_x, car_bottom_y
        nonlocal car_left_x, car_left_y
        nonlocal car_right_x, car_right_y
        nonlocal after_reset

        # 1) Determine the correct speeds based on whether we have reset yet
        if not after_reset:
            sp_top    = SPEED_BEFORE
            sp_bottom = SPEED_BEFORE
            sp_left   = SPEED_BEFORE
            sp_right  = SPEED_BEFORE
        else:
            sp_top    = SPEEDS_AFTER["car_top"]
            sp_bottom = SPEEDS_AFTER["car_bottom"]
            sp_left   = SPEEDS_AFTER["car_left"]
            sp_right  = SPEEDS_AFTER["car_right"]

        # 2) Move each car
        if not after_reset:
            # BEFORE collision: move them toward the center (~250)
            if car_top_y + sp_top < 250:
                car_top_y += sp_top
                canvas.coords(car_top, car_top_x, car_top_y)

            if car_bottom_y - sp_bottom > 250:
                car_bottom_y -= sp_bottom
                canvas.coords(car_bottom, car_bottom_x, car_bottom_y)

            if car_left_x + sp_left < 250:
                car_left_x += sp_left
                canvas.coords(car_left, car_left_x, car_left_y)

            if car_right_x - sp_right > 250:
                car_right_x -= sp_right
                canvas.coords(car_right, car_right_x, car_right_y)
        else:
            # AFTER reset: let them pass entirely off screen
            # (top goes downward off screen, etc.)
            if car_top_y < 550:  # off screen bottom
                car_top_y += sp_top
                canvas.coords(car_top, car_top_x, car_top_y)

            if car_bottom_y > -50:  # off screen top
                car_bottom_y -= sp_bottom
                canvas.coords(car_bottom, car_bottom_x, car_bottom_y)

            if car_left_x < 550:  # off screen right
                car_left_x += sp_left
                canvas.coords(car_left, car_left_x, car_left_y)

            if car_right_x > -50:  # off screen left
                car_right_x -= sp_right
                canvas.coords(car_right, car_right_x, car_right_y)

        # 3) Check collision
        if any_collision():
            # If we haven't already reset, do it now
            if not after_reset:
                reset_to_start()
                after_reset = True  # cars now have different speeds
            else:
                pass
            # Schedule next move anyway (so they keep going)
            window.after(DELAY, move_cars)
            return

        # 4) Determine if we continue
        if not after_reset:
            # If still not at center, keep moving
            if (car_top_y < 250 or
                car_bottom_y > 250 or
                car_left_x < 250 or
                car_right_x > 250):
                window.after(DELAY, move_cars)
            else:
                print("[GUI] All cars reached the center without colliding!")
        else:
            # Once reset, keep moving until they exit
            all_offscreen = (
                car_top_y    > 550 and
                car_bottom_y < -50 and
                car_left_x   > 550 and
                car_right_x  < -50
            )
            if not all_offscreen:
                window.after(DELAY, move_cars)
            else:
                print("[GUI] All cars have exited the intersection after reset.")
                if CLOSE_WINDOW_WHEN_DONE:
                    print("[GUI] Closing the window now.")
                    window.destroy()  # closes the Tk window


    ##################################
    # 2.3 Tkinter: Window/Canvas Setup
    ##################################
    window = tk.Tk()
    window.title("Rollback to Beginning on Collision (Then Different Speeds)")

    canvas = tk.Canvas(window, width=500, height=500, bg="white")
    canvas.pack()

    # Draw roads
    canvas.create_rectangle(200, 0,   300, 500, fill="gray")  # vertical
    canvas.create_rectangle(0,   200, 500, 300, fill="gray")  # horizontal

    # Dashed lane dividers (vertical)
    for y in range(0, 500, 40):
        canvas.create_line(245, y, 245, y + 20, fill="white", dash=(5,2))
        canvas.create_line(255, y, 255, y + 20, fill="white", dash=(5,2))

    # Dashed lane dividers (horizontal)
    for x in range(0, 500, 40):
        canvas.create_line(x, 245, x + 20, 245, fill="white", dash=(5,2))
        canvas.create_line(x, 255, x + 20, 255, fill="white", dash=(5,2))

    ##################################
    # 2.4 Load Car Images
    ##################################
    base_car_image = Image.open("car.png").resize((30, 50))  # assume faces right

    car_right_image = ImageTk.PhotoImage(base_car_image)  # faces right
    car_left_image  = ImageTk.PhotoImage(ImageOps.mirror(base_car_image))
    car_down_image  = ImageTk.PhotoImage(base_car_image.rotate(90, expand=True))
    car_up_image    = ImageTk.PhotoImage(base_car_image.rotate(-90, expand=True))

    ##################################
    # 2.5 Create Car Sprites on Canvas
    ##################################
    car_top    = canvas.create_image(init_top_x,    init_top_y,    image=car_down_image)
    car_bottom = canvas.create_image(init_bottom_x, init_bottom_y, image=car_up_image)
    car_left   = canvas.create_image(init_left_x,   init_left_y,   image=car_left_image)
    car_right  = canvas.create_image(init_right_x,  init_right_y,  image=car_right_image)

    # Keep references to avoid garbage-collection
    canvas.car_down_image  = car_down_image
    canvas.car_up_image    = car_up_image
    canvas.car_left_image  = car_left_image
    canvas.car_right_image = car_right_image

    ##################################
    # 2.6 Start the Movement
    ##################################
    window.after(DELAY, move_cars)
    window.mainloop()


def detect_deadlock(t1, t2):
    time.sleep(2)  # Allow threads to potentially deadlock
    running = True
    while running:
        if lock1.locked() and lock2.locked():
            time.sleep(2)
            print("Deadlock detected! Visualizing...")
            draw_intersection_with_moving_cars()
            running = False
            print("Killing threads...\n(In this case it consists of raising an exception as there is no explicit way in python to kill a thread)")
            print("This is a workaround to kill the threads, as they are still stuck in the deadlock, will only stop after the exception is raised and the deadlock is resolved")
            print("uncomment the kill_thread function to see it functioning, the threads should not do anything even after the deadlock is resolved")
            # kill_threads.kill_thread(t2)
            # kill_threads.kill_thread(t1)
            print("'Threads killed'\nReleasing one of the locks to stop the deadlock...")
            lock1.release()
    
###############################################################################
# 3. Main: Start Threads, GUI, and Deadlock Detection
###############################################################################
if __name__ == "__main__":
    # Optional concurrency threads:
    t1 = threading.Thread(target=thread_1)
    t2 = threading.Thread(target=thread_2)
    t1.start()
    t2.start()

    # Run the Tkinter GUI
   # draw_intersection_with_moving_cars()
    deadlock_detector = threading.Thread(target=detect_deadlock(t1, t2))
    deadlock_detector.start()

    # Wait for threads
    t1.join()
    t2.join()
    print("[Main] Done.")
