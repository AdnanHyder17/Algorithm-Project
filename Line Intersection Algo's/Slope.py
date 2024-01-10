import tkinter as tk

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def slope(p1, p2):
    if p2.x - p1.x == 0:
        return float('inf')  # Vertical line, slope is infinity
    return (p2.y - p1.y) / (p2.x - p1.x)

def intersect(l1, l2):
    slope1 = slope(l1[0], l1[1])
    slope2 = slope(l2[0], l2[1])

    if slope1 == slope2:
        return False  # Lines are either parallel or coincident

    # Check if the intersection point is within the line segments
    x_intersect = (
        (slope1 * l1[0].x - slope2 * l2[0].x + l2[0].y - l1[0].y) /
        (slope1 - slope2)
    )
    y_intersect = slope1 * (x_intersect - l1[0].x) + l1[0].y

    x_range_l1 = min(l1[0].x, l1[1].x), max(l1[0].x, l1[1].x)
    y_range_l1 = min(l1[0].y, l1[1].y), max(l1[0].y, l1[1].y)

    x_range_l2 = min(l2[0].x, l2[1].x), max(l2[0].x, l2[1].x)
    y_range_l2 = min(l2[0].y, l2[1].y), max(l2[0].y, l2[1].y)

    return (
        x_range_l1[0] <= x_intersect <= x_range_l1[1] and
        y_range_l1[0] <= y_intersect <= y_range_l1[1] and
        x_range_l2[0] <= x_intersect <= x_range_l2[1] and
        y_range_l2[0] <= y_intersect <= y_range_l2[1]
    )

class LineDrawer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg="#F0EADC")  # Pastel background color
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.points = []
        self.lines = []

        # Draw axes
        self.canvas.create_line(0, 200, 400, 200, fill="#C7C7C7")  # Horizontal axis (pastel gray)
        self.canvas.create_line(200, 0, 200, 400, fill="#C7C7C7")  # Vertical axis (pastel gray)

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.draw_point(x, y)

        if len(self.points) == 2:
            self.draw_line(self.points)
            self.lines.append((self.points[0], self.points[1]))
            self.points = []

            if len(self.lines) == 2:
                if intersect(self.lines[0], self.lines[1]):
                    self.show_result("Lines intersect!")
                else:
                    self.show_result("Lines do not intersect!")

    def draw_point(self, x, y):
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#6A0572")  # Pastel purple

    def draw_line(self, points):
        x1, y1 = points[0].x, points[0].y
        x2, y2 = points[1].x, points[1].y
        self.canvas.create_line(x1, y1, x2, y2, fill="#118AB2")  # Pastel blue

    def show_result(self, result):
        self.canvas.create_text(200, 20, text=result, fill="#EF476F", font=("Helvetica", 12))  # Pastel pink
        self.root.after(2000, self.reset)  # Reset after 2000 milliseconds (2 seconds)

    def reset(self):
        self.canvas.delete("all")

        # Draw axes
        self.canvas.create_line(0, 200, 400, 200, fill="#C7C7C7")  # Horizontal axis (pastel gray)
        self.canvas.create_line(200, 0, 200, 400, fill="#C7C7C7")  # Vertical axis (pastel gray)

        self.points = []
        self.lines = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Slope Method")
    line_drawer = LineDrawer(root)
    root.mainloop()
