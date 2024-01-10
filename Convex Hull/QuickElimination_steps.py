import tkinter as tk
import random
import time

pointList = []

def on_canvas_click(event):
    x, y = event.x, event.y
    pointList.append([x, y])
    canvas.create_oval(x - 2.5, y - 2.5, x + 2.5, y + 2.5, fill="blue")

def calculate_quickhull():
    global pointList
    start_time = time.time()  # Record the start time
    convex_hull = quickhull(pointList)
    draw_convex_hull(convex_hull)
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.6f} seconds")


def quickhull(points: list):
    if len(points) < 3:
        return points

    leftmost = min(points, key=lambda x: x[0])
    rightmost = max(points, key=lambda x: x[0])

    convex_hull = [leftmost, rightmost]
    points.remove(leftmost)
    points.remove(rightmost)

    left_set = []
    right_set = []

    for point in points:
        if is_left(leftmost, rightmost, point):
            left_set.append(point)
        elif is_left(rightmost, leftmost, point):
            right_set.append(point)

    hull_recursive(leftmost, rightmost, left_set, convex_hull)
    hull_recursive(rightmost, leftmost, right_set, convex_hull)

    return convex_hull

def hull_recursive(a, b, point_set, convex_hull):
    if not point_set:
        return

    furthest_point = max(point_set, key=lambda x: find_distance(a, b, x))
    convex_hull.insert(convex_hull.index(b), furthest_point)
    point_set.remove(furthest_point)

    left_set = []
    for point in point_set:
        if is_left(a, furthest_point, point):
            left_set.append(point)

    right_set = []
    for point in point_set:
        if is_left(furthest_point, b, point):
            right_set.append(point)

    # Draw lines connecting points being considered with a delay
    canvas.create_line(a[0], a[1], furthest_point[0], furthest_point[1], fill="green")
    canvas.create_line(furthest_point[0], furthest_point[1], b[0], b[1], fill="green")

    win.update()
    win.after(500)  # 500 milliseconds delay

    hull_recursive(a, furthest_point, left_set, convex_hull)
    hull_recursive(furthest_point, b, right_set, convex_hull)

def is_left(a, b, c):
    ax, ay, bx, by, cx, cy = a[0], a[1], b[0], b[1], c[0], c[1]
    return ((bx - ax) * (cy - ay)) - ((cx - ax) * (by - ay)) > 0

def find_distance(a, b, p):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    px, py = p[0], p[1]
    return abs(((bx - ax) * (ay - py)) - ((ax - px) * (by - ay))) / ((bx - ax)**2 + (by - ay)**2)*0.5

def draw_convex_hull(convex_hull):
    for point in convex_hull:
        canvas.create_oval(point[0] - 3.75, point[1] - 3.75, point[0] + 3.75, point[1] + 3.75, fill="yellow")

    for i in range(len(convex_hull) - 1):
        canvas.create_line(convex_hull[i][0], convex_hull[i][1], convex_hull[i + 1][0], convex_hull[i + 1][1])

    # Connect the last and the first points to complete the convex hull
    canvas.create_line(convex_hull[-1][0], convex_hull[-1][1], convex_hull[0][0], convex_hull[0][1])

win = tk.Tk()
win.title("QuickHull")
win.geometry("700x700")

canvas = tk.Canvas(win, width=500, height=400, bg="white")
canvas.pack()

canvas.bind("<Button-1>", on_canvas_click)

calculate_button = tk.Button(win, text="Calculate QuickHull", command=calculate_quickhull, width=20, height=2)
calculate_button.pack(pady=10)

win.mainloop()