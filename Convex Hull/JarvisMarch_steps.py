import tkinter as tk
from tkinter import ttk
from functools import cmp_to_key
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or counterclockwise

def jarvis_scan(points):
    n = len(points)
    if n < 3:
        return "Convex hull not possible"

    hull = []

    # Find the point with the lowest y-coordinate (and leftmost if ties)
    l = min(range(n), key=lambda i: (points[i].y, points[i].x))
    p = l
    q = 0
    while True:
        hull.append(p)
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == l:
            break

    return hull

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull Visualization")

        self.points = []

        self.canvas = tk.Canvas(root, width=700, height=700, bg="#C8A2C8", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.calculate_button = ttk.Button(root, text="Calculate Convex Hull", command=self.calculate_convex_hull)
        self.calculate_button.pack(pady=5)

        self.reset_button = ttk.Button(root, text="Reset Graph", command=self.reset_graph)
        self.reset_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.add_point)

        self.draw_axes()

    def add_point(self, event):
        x, y = event.x, event.y
        if 50 <= x <= 650 and 50 <= y <= 650:  # Bounds to prevent points outside the canvas
            new_point = Point(x, y)
            self.points.append(new_point)
            self.redraw_canvas()

    def redraw_canvas(self):
        # Clear previous points and lines
        self.canvas.delete("all")
        self.draw_axes()
        self.draw_points()

    def draw_axes(self):
        for i in range(50, 701, 50):
            # x-axis
            self.canvas.create_line(i, 650, i, 655, fill="white", width=1)
            self.canvas.create_text(i, 665, text=str(int(i - 50)), fill="white", anchor=tk.N)

            # y-axis
            self.canvas.create_line(650, i, 655, i, fill="white", width=1)
            self.canvas.create_text(665, i, text=str(int(i - 50)), fill="white", anchor=tk.W)

    def draw_points(self):
        for point in self.points:
            self.canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill="#800080", outline="#800080")

    def calculate_convex_hull(self):
        if len(self.points) < 3:
            print("Convex hull requires at least three points.")
            return

        self.start_time = time.time()  # Record the start time

        hull_indices = jarvis_scan(self.points)
        hull_points = [self.points[i] for i in hull_indices]

        # Draw convex hull lines with a delay
        for i in range(len(hull_points)):
            next_idx = (i + 1) % len(hull_points)
            x1, y1 = hull_points[i].x, hull_points[i].y
            x2, y2 = hull_points[next_idx].x, hull_points[next_idx].y
            self.root.after(i * 500, lambda x1=x1, y1=y1, x2=x2, y2=y2: self.draw_line(x1, y1, x2, y2))

        # Record the end time after the last line is drawn
        self.root.after(len(hull_points) * 500, self.record_execution_time)

    def record_execution_time(self):
        end_time = time.time()
        execution_time = end_time - self.start_time
        print(f"Total execution time: {execution_time:.6f} seconds")

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, fill="#800080", width=2)
        self.root.update()

    def reset_graph(self):
        self.points = []
        self.redraw_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    
    app = ConvexHullApp(root)

    root.mainloop()
