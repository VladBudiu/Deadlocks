import tkinter as tk
from PIL import Image, ImageTk, ImageOps

def draw_intersection_with_moving_cars():
    ############################################################
    # 1. Helper Functions
    ############################################################
    def boxes_collide(box1, box2):
        """
        Check if two bounding boxes overlap.
        Each box is a tuple of (x1, y1, x2, y2).
        """
        if not box1 or not box2:
            return False
        return not (
            box1[2] < box2[0] or  # box1's right < box2's left
            box1[0] > box2[2] or  # box1's left  > box2's right
            box1[3] < box2[1] or  # box1's bottom < box2's top
            box1[1] > box2[3]     # box1's top > box2's bottom
        )

    def any_collision():
        """
        Check collisions among all four cars (pairwise).
        Returns True if any two bounding boxes overlap.
        """
        bbox_top    = canvas.bbox(car_top)
        bbox_bottom = canvas.bbox(car_bottom)
        bbox_left   = canvas.bbox(car_left)
        bbox_right  = canvas.bbox(car_right)

        # Pairs of bounding boxes to test
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

    ############################################################
    # 2. Movement Function
    ############################################################
    def move_cars():
        nonlocal car_top_y, car_bottom_y, car_left_x, car_right_x

        # Move top car DOWNWARD until near the intersection
        # (stop around y=200, the top of the intersection).
        if car_top_y + STEP < 250:
            car_top_y += STEP
            canvas.coords(car_top, car_top_x, car_top_y)

        # Move bottom car UPWARD until near the intersection
        # (stop around y=300, the bottom of the intersection).
        if car_bottom_y - STEP > 250:
            car_bottom_y -= STEP
            canvas.coords(car_bottom, car_bottom_x, car_bottom_y)

        # Move left car RIGHTWARD until near the intersection
        # (stop around x=200, the left of the intersection).
        if car_left_x + STEP < 250:
            car_left_x += STEP
            canvas.coords(car_left, car_left_x, car_left_y)

        # Move right car LEFTWARD until near the intersection
        # (stop around x=300, the right of the intersection).
        if car_right_x - STEP > 250:
            car_right_x -= STEP
            canvas.coords(car_right, car_right_x, car_right_y)

        # Check collision
        if any_collision():
            # If collision, stop moving (don’t reschedule)
            return

        # If any car still hasn't reached its “stop” zone, keep moving
        if (car_top_y < 250 or
            car_bottom_y > 250 or
            car_left_x < 250 or
            car_right_x > 250):
            window.after(DELAY, move_cars)

    ############################################################
    # 3. Create the Window and Canvas
    ############################################################
    window = tk.Tk()
    window.title("4-Way Intersection with Moving Cars")

    canvas = tk.Canvas(window, width=500, height=500, bg="white")
    canvas.pack()

    # Draw the roads
    canvas.create_rectangle(200, 0,   300, 500, fill="gray")  # Vertical road
    canvas.create_rectangle(0,   200, 500, 300, fill="gray")  # Horizontal road

    # Draw lane dividers for the vertical road (x=245 and x=255).
    # These are dashed white lines at intervals, just decorative.
    for y in range(0, 500, 40):
        canvas.create_line(245, y, 245, y + 20, fill="white", dash=(5,2))
        canvas.create_line(255, y, 255, y + 20, fill="white", dash=(5,2))

    # Draw lane dividers for the horizontal road (y=245 and y=255).
    for x in range(0, 500, 40):
        canvas.create_line(x, 245, x + 20, 245, fill="white", dash=(5,2))
        canvas.create_line(x, 255, x + 20, 255, fill="white", dash=(5,2))

    ############################################################
    # 4. Load/Rotate Car Images
    ############################################################
    # Base car image is assumed to face RIGHT
    car_image = Image.open("car.png").resize((30, 50))

    car_left_image = ImageTk.PhotoImage(car_image)  # faces right
    # Mirror (left)
    car_right_image  = ImageTk.PhotoImage(ImageOps.mirror(car_image))
    # Rotate 90 deg from "right" => faces UP
    car_down_image    = ImageTk.PhotoImage(car_image.rotate(90, expand=True))
    # Rotate -90 deg from "right" => faces DOWN
    car_up_image  = ImageTk.PhotoImage(car_image.rotate(-90, expand=True))

    ############################################################
    # 5. Position Each Car in Its Lane
    ############################################################
    # Lanes:
    #  - top car: x=225 (left side of vertical road), traveling DOWN
    #  - bottom car: x=275 (right side), traveling UP
    #  - left car: y=275 (bottom side of horizontal road), traveling RIGHT
    #  - right car: y=225 (top side), traveling LEFT

    # Start them well outside the intersection
    car_top_x    = 225
    car_top_y    = -60  # off-canvas at top
    car_bottom_x = 275
    car_bottom_y = 560  # off-canvas at bottom
    car_left_x   = -60  # off-canvas at left
    car_left_y   = 275
    car_right_x  = 560  # off-canvas at right
    car_right_y  = 225

    # Create them on the canvas
    # Top car (facing down)
    car_top    = canvas.create_image(car_top_x, car_top_y, image=car_down_image)
    # Bottom car (facing up)
    car_bottom = canvas.create_image(car_bottom_x, car_bottom_y, image=car_up_image)
    # Left car (facing right)
    car_left   = canvas.create_image(car_left_x, car_left_y, image=car_right_image)
    # Right car (facing left)
    car_right  = canvas.create_image(car_right_x, car_right_y, image=car_left_image)

    # Keep references so they aren't garbage-collected
    canvas.car_up_image    = car_up_image
    canvas.car_down_image  = car_down_image
    canvas.car_left_image  = car_left_image
    canvas.car_right_image = car_right_image

    ############################################################
    # 6. Start the Movement
    ############################################################
    STEP  = 10   # how many pixels each move step
    DELAY = 200  # time (ms) between moves

    window.after(DELAY, move_cars)
    window.mainloop()

