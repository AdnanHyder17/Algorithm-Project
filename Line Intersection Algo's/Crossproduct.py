import tkinter as tk

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def ccw(p1, p2, p3):
    return (p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y)

def intersect(l1, l2):
    test1 = ccw(l1[0], l1[1], l2[0]) * ccw(l1[0], l1[1], l2[1])
    test2 = ccw(l2[0], l2[1], l1[0]) * ccw(l2[0], l2[1], l1[1])
    return (test1 <= 0) and (test2 <= 0)

class LineDrawer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.points = []
        self.lines = []

        # Draw axes
        self.canvas.create_line(0, 200, 400, 200, fill="gray")  # Horizontal axis
        self.canvas.create_line(200, 0, 200, 400, fill="gray")  # Vertical axis

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
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def draw_line(self, points):
        x1, y1 = points[0].x, points[0].y
        x2, y2 = points[1].x, points[1].y
        self.canvas.create_line(x1, y1, x2, y2, fill="black")

    def show_result(self, result):
        self.canvas.create_text(200, 20, text=result, fill="red", font=("Helvetica", 12))
        self.root.after(1000, self.reset)  # Reset after 2000 milliseconds (2 seconds)

    def reset(self):
        self.canvas.delete("all")

        # Draw axes
        self.canvas.create_line(0, 200, 400, 200, fill="gray")  # Horizontal axis
        self.canvas.create_line(200, 0, 200, 400, fill="gray")  # Vertical axis

        self.points = []
        self.lines = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cross Product Method")
    line_drawer = LineDrawer(root)
    root.mainloop()
