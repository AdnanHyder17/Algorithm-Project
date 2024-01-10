import tkinter as tk
import time


def brute_force_convex_hull(points):
    """ Calculate the convex hull of a set of points using brute force method """
    if len(points) < 3:
        return points

    def on_the_left(p1, p2, p3):
        """ Check if point p3 is on the left side of the line from p1 to p2 """
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

    hull = []
    non_hull = []
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                left_side = True
                for k in range(len(points)):
                    if k != i and k != j:
                        if not on_the_left(points[i], points[j], points[k]):
                            left_side = False
                            break
                if left_side:
                    hull.append((points[i], points[j]))
                else:
                    non_hull.append((points[i], points[j]))
    return hull, non_hull

def on_canvas_click(event):
    """ Handle canvas click events to add points and update convex hull """
    x, y = event.x, event.y
    points.append((x, y))
    draw_point(x, y)

def draw_point(x, y):
    """ Draw a point on the canvas """
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='black')

def draw_hull_lines(lines, color):
    """ Draw lines on the canvas with a delay between each line """
    for line in lines:
        canvas.create_line(line[0], line[1], tags='line', fill=color)
        canvas.update()  # Update the canvas to show the line
        canvas.after(250)  # Delay in milliseconds (adjust as needed)

def draw_hull(hull, non_hull):
    """ Draw the convex hull and non-convex hull lines """
    canvas.delete('line')  # Remove old lines

    # Draw non-convex hull lines in black
    draw_hull_lines(non_hull, 'black')

    # Draw convex hull lines in red
    draw_hull_lines(hull, 'red')

def calculate_hull():
    start_time = time.time()  # Record the start time
    hull, non_hull = brute_force_convex_hull(points)
    draw_hull(hull, non_hull)
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.6f} seconds")

# Setting up the main window and canvas
root = tk.Tk()
root.title("Convex Hull - Brute Force")
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()
canvas.bind('<Button-1>', on_canvas_click)

calculate_button = tk.Button(root, text="Calculate Convex Hull", command=calculate_hull)
calculate_button.pack()
points = []
root.mainloop()