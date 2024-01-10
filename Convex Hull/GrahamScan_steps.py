import tkinter as tk
from tkinter import ttk
import math
import time

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull Visualization")

        self.points = []

        self.canvas = tk.Canvas(root, width=700, height=700, bg="#6495ED", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.calculate_button = ttk.Button(root, text="Calculate Convex Hull", command=self.calculate_convex_hull)
        self.calculate_button.pack(pady=5)

        self.reset_button = ttk.Button(root, text="Reset Graph", command=self.reset_graph)
        self.reset_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.add_point)

        self.draw_axes()

    def add_point(self, event):
        x, y = event.x, 700 - event.y  # Invert the Y-coordinate
        if 50 <= x <= 650 and 50 <= 700 - y <= 650:  # Bounds to prevent points outside the canvas
            new_point = (x, 700 - y)  # Invert the Y-coordinate for storing in the points list
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
            self.canvas.create_text(665, i, text=str(int(650 - i)), fill="white", anchor=tk.W)

    def draw_points(self):
        for point in self.points:
            self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="#FFD700",
                                    outline="#FFD700")

    def find_lowest_point(self):
        if not self.points:
            return None
        return min(self.points, key=lambda p: p[1])

    def calculate_convex_hull(self):
        start_time = time.time()  # Record the start time

        lowest_point = self.find_lowest_point()

        if lowest_point is None:
            print("No points to calculate convex hull.")
            return

        hull_points = self.graham_scan(self.points, lowest_point)

        # Draw convex hull lines with a delay
        for i in range(len(hull_points)):
            next_idx = (i + 1) % len(hull_points)
            x1, y1 = hull_points[i][0], hull_points[i][1]
            x2, y2 = hull_points[next_idx][0], hull_points[next_idx][1]
            self.draw_line(x1, y1, x2, y2)

        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time:.6f} seconds")

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, fill="#FFD700", width=2)
        self.root.update()
        self.root.after(500)  # Pause for a short time to visualize step

    def reset_graph(self):
        self.points = []
        self.redraw_canvas()

    def graham_scan(self, points, lowest_point):
        def ccw(p1, p2, p3):
            return (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])

        points.sort(key=lambda p: (math.atan2(p[1] - lowest_point[1], p[0] - lowest_point[0]) + 2 * math.pi) % (2 * math.pi))

        upper_hull = []
        for p in points:
            while len(upper_hull) >= 2 and ccw(upper_hull[-2], upper_hull[-1], p) <= 0:
                upper_hull.pop()
            upper_hull.append(p)

        lower_hull = []
        for p in reversed(points):
            while len(lower_hull) >= 2 and ccw(lower_hull[-2], lower_hull[-1], p) <= 0:
                lower_hull.pop()
            lower_hull.append(p)

        return upper_hull[:-1] + lower_hull[:-1]

if __name__ == "__main__":
    root = tk.Tk()
    
    app = ConvexHullApp(root)

    root.mainloop()
