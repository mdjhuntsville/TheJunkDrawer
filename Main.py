import tkinter as tk
from tkinter import Menu
import math
import time
import random

# Function to exit the application
def exit_app():
    root.destroy()

# Function to redraw the triangle, booster, balls, polygons, and collision states
def draw_shape():
    canvas.delete("all")

    if collision_state["active"]:
        # Draw a red circle indicating collision
        canvas.create_oval(
            collision_state["x"] - 50,
            collision_state["y"] - 50,
            collision_state["x"] + 50,
            collision_state["y"] + 50,
            fill="red",
            outline=""
        )
    else:
        angle_rad = math.radians(triangle_angle + 90)  # Corrected angle adjustment
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        # Calculate rotated triangle vertices
        rotated_triangle = []
        for x, y in triangle_points:
            rotated_x = x * cos_theta - y * sin_theta + ship_x
            rotated_y = x * sin_theta + y * cos_theta + ship_y
            rotated_triangle.append((rotated_x, rotated_y))

        # Calculate rotated booster vertices
        rotated_booster = []
        for x, y in booster_points:
            rotated_x = x * cos_theta - y * sin_theta + ship_x
            rotated_y = x * sin_theta + y * cos_theta + ship_y
            rotated_booster.append((rotated_x, rotated_y))

        # Draw the triangle
        canvas.create_polygon(rotated_triangle, fill="", outline="white", width=2)

        # Draw the booster
        canvas.create_polygon(rotated_booster, fill="", outline="cyan", width=2)

    # Draw active balls
    for ball in balls:
        canvas.create_oval(ball[0] - 5, ball[1] - 5, ball[0] + 5, ball[1] + 5, fill="orange")

    # Draw polygons
    for polygon in polygons:
        x, y, size = polygon["x"], polygon["y"], polygon["size"]
        half_size = size / 2
        points = [
            (x - half_size, y - half_size),
            (x + half_size, y - half_size),
            (x + half_size, y + half_size),
            (x - half_size, y + half_size)
        ]
        canvas.create_polygon(points, fill="", outline="green", width=2)

    # Draw temporary yellow circles
    for yellow_circle in yellow_circles[:]:
        canvas.create_oval(
            yellow_circle["x"] - 10, yellow_circle["y"] - 10,
            yellow_circle["x"] + 10, yellow_circle["y"] + 10,
            fill="yellow", outline=""
        )

    # Check if all polygons are cleared
    if not polygons:
        canvas.create_text(350, 350, text="YOU WIN. New Game in 15sec.", fill="white", font=("Arial", 24))
        root.after(15000, restart_game)

# Function to rotate the triangle to the left
def rotate_left(event):
    global triangle_angle
    if not collision_state["active"]:
        triangle_angle -= 10
        draw_shape()

# Function to rotate the triangle to the right
def rotate_right(event):
    global triangle_angle
    if not collision_state["active"]:
        triangle_angle += 10
        draw_shape()

# Function to move the ship forward based on the direction of the triangle's north point
def move_forward(event):
    global ship_x, ship_y
    if not collision_state["active"]:
        angle_rad = math.radians(triangle_angle)
        ship_x += math.cos(angle_rad) * 10
        ship_y += math.sin(angle_rad) * 10

        # Edge wrapping logic
        if ship_x > 720:
            ship_x = -20
        elif ship_x < -20:
            ship_x = 720

        if ship_y > 720:
            ship_y = -20
        elif ship_y < -20:
            ship_y = 720

        draw_shape()

# Function to shoot a ball from the tip of the triangle
def shoot_ball(event):
    global balls, last_shot_time
    if not collision_state["active"]:
        current_time = time.time()
        if current_time - last_shot_time >= 0.5:  # Decreased shooting rate limit by half
            last_shot_time = current_time
            angle_rad = math.radians(triangle_angle)
            ball_x = ship_x + math.cos(angle_rad) * 12.5  # Adjusted for smaller ship size
            ball_y = ship_y + math.sin(angle_rad) * 12.5
            balls.append([ball_x, ball_y, angle_rad])
            update_balls()

# Function to update the positions of all balls
def update_balls():
    global balls
    for ball in balls[:]:
        ball[0] += math.cos(ball[2]) * 4  # Increased ball speed by 2x
        ball[1] += math.sin(ball[2]) * 4

        # Check for collision with polygons
        for polygon in polygons[:]:
            if abs(ball[0] - polygon["x"]) < polygon["size"] / 2 and abs(ball[1] - polygon["y"]) < polygon["size"] / 2:
                handle_polygon_collision(polygon, ball)
                if ball in balls:
                    balls.remove(ball)

        # Remove ball if it goes off screen
        if ball[0] < -20 or ball[0] > 720 or ball[1] < -20 or ball[1] > 720:
            balls.remove(ball)

    draw_shape()
    if balls:
        root.after(50, update_balls)

# Function to handle polygon collision with a ball
def handle_polygon_collision(polygon, ball):
    global polygons, yellow_circles
    size = polygon["size"]
    if size == polygon_sizes["Big_Polygon"]:
        create_medium_polygons(polygon)
    elif size == polygon_sizes["Medium_Polygon"]:
        create_small_polygons(polygon)
    elif size == polygon_sizes["Small_Polygon"]:
        yellow_circles.append({"x": polygon["x"], "y": polygon["y"]})
        root.after(200, lambda: yellow_circles.remove({"x": polygon["x"], "y": polygon["y"]}))
    polygons.remove(polygon)

# Function to create two Medium_Polygons from a Big_Polygon
def create_medium_polygons(polygon):
    for _ in range(2):
        polygons.append({
            "x": polygon["x"],
            "y": polygon["y"],
            "dx": random.uniform(-2, 2),
            "dy": random.uniform(-2, 2),
            "size": polygon_sizes["Medium_Polygon"]
        })

# Function to create two Small_Polygons from a Medium_Polygon
def create_small_polygons(polygon):
    for _ in range(2):
        polygons.append({
            "x": polygon["x"],
            "y": polygon["y"],
            "dx": random.uniform(-2, 2),
            "dy": random.uniform(-2, 2),
            "size": polygon_sizes["Small_Polygon"]
        })

# Function to update polygons' positions and check for collisions
def update_polygons():
    global polygons
    for polygon in polygons:
        polygon["x"] += polygon["dx"]
        polygon["y"] += polygon["dy"]

        # Wrap around screen edges
        if polygon["x"] > 720:
            polygon["x"] = -20
        elif polygon["x"] < -20:
            polygon["x"] = 720

        if polygon["y"] > 720:
            polygon["y"] = -20
        elif polygon["y"] < -20:
            polygon["y"] = 720

        # Check for collision with the ship
        if not collision_state["active"] and abs(polygon["x"] - ship_x) < polygon["size"] / 2 and abs(polygon["y"] - ship_y) < polygon["size"] / 2:
            trigger_collision()

    draw_shape()
    root.after(50, update_polygons)

# Function to handle ship-polygon collision
def trigger_collision():
    global collision_state, ship_x, ship_y
    collision_state["active"] = True
    collision_state["x"] = ship_x
    collision_state["y"] = ship_y

    # Schedule respawn after 5 seconds
    root.after(5000, respawn_ship)

# Function to respawn the ship
def respawn_ship():
    global collision_state, ship_x, ship_y
    ship_x, ship_y = 350, 350  # Respawn in the center
    collision_state["active"] = False
    draw_shape()

# Function to restart the game
def restart_game():
    global ship_x, ship_y, triangle_angle, balls, polygons, collision_state, yellow_circles
    ship_x, ship_y = 350, 350
    triangle_angle = 0
    balls = []
    yellow_circles = []
    polygons = []
    collision_state = {"active": False, "x": 0, "y": 0}

    # Reinitialize polygons
    for _ in range(3):  # Create 3 Big_Polygons
        polygons.append({
            "x": random.uniform(0, 700),  # Random position
            "y": random.uniform(0, 700),
            "dx": random.uniform(-2, 2),  # Random velocity
            "dy": random.uniform(-2, 2),
            "size": polygon_sizes["Big_Polygon"]
        })

    draw_shape()

# Function to update the yellow circles
def update_yellow_circles():
    for yellow_circle in yellow_circles[:]:
        # Remove the circle after a short duration
        if "timer" not in yellow_circle:
            yellow_circle["timer"] = 200  # Duration in milliseconds

        yellow_circle["timer"] -= 50
        if yellow_circle["timer"] <= 0:
            yellow_circles.remove(yellow_circle)

    draw_shape()
    if yellow_circles:
        root.after(50, update_yellow_circles)

# Create the main window
root = tk.Tk()
root.title("Asteroid 2100")
root.geometry("700x700")
root.configure(bg="black")

# Create a canvas for drawing
canvas = tk.Canvas(root, width=700, height=700, bg="black", highlightthickness=0)
canvas.pack()

# Create a menu bar
menu_bar = Menu(root)

# Add File menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Define the triangle points (relative to the center, reduced size by 50%)
triangle_points = [(0, -12.5), (-7.5, 7.5), (7.5, 7.5)]  # Reduced ship size by half

# Define the booster points (relative to the center, at the back of the triangle)
booster_points = [(-5, 7.5), (5, 7.5), (2.5, 15), (-2.5, 15)]

# Initial position and angle of the ship
ship_x, ship_y = 350, 350
triangle_angle = 0

# List to track active balls
balls = []
last_shot_time = 0

# List to track polygons
polygons = []
polygon_sizes = {"Big_Polygon": 75, "Medium_Polygon": 40, "Small_Polygon": 15}

# List to track temporary yellow circles
yellow_circles = []

# Collision state
collision_state = {"active": False, "x": 0, "y": 0}

# Initialize polygons
for _ in range(6):  # Create 3 Big_Polygons
    polygons.append({
        "x": random.uniform(0, 700),  # Random position
        "y": random.uniform(0, 700),
        "dx": random.uniform(-4, 4),  # Random velocity
        "dy": random.uniform(-4, 4),
        "size": polygon_sizes["Big_Polygon"]
    })

# Draw the initial shape
draw_shape()

# Start polygon movement
update_polygons()

# Initialize yellow circle updates
update_yellow_circles()

# Bind arrow keys for rotation and movement
root.bind("<Left>", rotate_left)
root.bind("<Right>", rotate_right)
root.bind("<Up>", move_forward)
root.bind("<space>", shoot_ball)

# Run the application
root.mainloop()
