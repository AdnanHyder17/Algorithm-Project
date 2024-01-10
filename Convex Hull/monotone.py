import tkinter as tk
import time

class ConvexHullApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Convex Hull Visualization")

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.points = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.solve_button = tk.Button(self.master, text="Solve Convex Hull", command=self.solve_convex_hull)
        self.solve_button.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def solve_convex_hull(self):
        start_time = time.time()
        if len(self.points) >= 3:
            hull_points = self.monotone_chain_algorithm(self.points)
            self.draw_convex_hull_with_delay(hull_points)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Convex Hull Computation Time: {execution_time:.6f} seconds")

    def monotone_chain_algorithm(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        points.sort()

        lower_hull = []
        for p in points:
            while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], p) != 2:
                lower_hull.pop()
            lower_hull.append(p)

        upper_hull = []
        for p in reversed(points):
            while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], p) != 2:
                upper_hull.pop()
            upper_hull.append(p)

        # Concatenate the lower and upper hulls excluding duplicate points
        convex_hull = lower_hull + upper_hull[1:-1]

        return convex_hull

    def draw_convex_hull_with_delay(self, hull_points):
        self.canvas.delete("convex_hull")
        for i in range(len(hull_points) - 1):
            x1, y1 = hull_points[i]
            x2, y2 = hull_points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="convex_hull")
            self.master.update()  # Force update to immediately show the line
            time.sleep(0.25)  # Introduce a delay of 250 milliseconds

        # Connect the last and first points
        x1, y1 = hull_points[-1]
        x2, y2 = hull_points[0]
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="convex_hull")

if __name__ == "__main__":
    root = tk.Tk()

    app = ConvexHullApp(root)
    
    root.mainloop()