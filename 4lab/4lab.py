import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import matplotlib.lines
import matplotlib.patches
from tkinter import *
from tkinter.ttk import *
import random


def clipping(lines, window):
    """
    get indexes of segments that are included in the window
    :param lines: generated segments
    :param window: window
    :return: array of indexes
    """
    def get_y(x, line):
        """
        getting y coordinate of point
        :param x: x coordinate
        :param line: generated segment
        :return: y coordinate
        """
        return (x - line[0][0])/(line[1][0] - line[0][0])*(line[1][1] - line[0][1]) + line[0][1]

    def proof(i):
        """
        function for checking the inclusion of segment
        :param i: index of segment
        :return: 0 if not included and 1 if included
        """
        line = lines[i].copy()
        bytes = [0, 0]

        # finding minimum and maximum x of points of segment
        min_p = line[0].copy()
        max_p = line[1].copy()
        if min(line[0][0], line[1][0]) == line[1][0]:
            min_p, max_p = max_p.copy(), min_p.copy()

        points = [[min_p.copy(), max_p.copy()]]

        # moving along the segment and checking the entry conditions
        for i in range(min_p[0], max_p[0], 1):
            points[0][0][0] = i
            points[0][0][1] = get_y(i, line)
            bytes[0] = get_bytes(points, 0, 0)
            bytes[1] = get_bytes(points, 0, 1)
            if bytes[0] == 0 or bytes[1] == 0:
                return 1
            elif bytes[0] == bytes[1]:
                return 0
            points[0][1][0] = max_p[0] - (i - min_p[0] + 1)
            points[0][1][1] = get_y(points[0][1][0], line)
            bytes[1] = get_bytes(points, 0, 1)
            if bytes[0] == 0 or bytes[1] == 0:
                return 1
            elif bytes[0] == bytes[1]:
                return 0
        return 2

    # [0, 1, 2, 4, 5, 6, 8, 9, 10]
    def get_bytes(lines, i, j):
        """
        Getting array of bytes as an integer (for ease of operation) according to the rule

        :param lines: generated segments
        :param i: number of segment
        :param j: number of point of segment
        :return: array of bytes as an integer
        """
        if (lines[i][j][0] >= min(window[0][0], window[1][0])) and (lines[i][j][0] <= max(window[1][0], window[0][0])):
            if lines[i][j][1] >= min(window[0][1], window[1][1]):
                if lines[i][j][1] <= max(window[0][1], window[1][1]):
                    return 0
                else:
                    return 1
            else:
                return 2
        elif (lines[i][j][0] >= min(window[0][0], window[1][0])) and (lines[i][j][0] > max(window[1][0], window[0][0])):
            if lines[i][j][1] >= min(window[0][1], window[1][1]):
                if lines[i][j][1] <= max(window[0][1], window[1][1]):
                    return 4
                else:
                    return 5
            else:
                return 6
        else:
            if lines[i][j][1] >= min(window[0][1], window[1][1]):
                if lines[i][j][1] <= max(window[0][1], window[1][1]):
                    return 8
                else:
                    return 9
            else:
                return 10

    mas = np.zeros(8)
    mas_in = np.zeros(4)

    # generating of bytes
    for i in range(4):
        for j in range(2):
            mas[i * 2 + j] = get_bytes(lines, i, j)

    # getting result
    for i in range(4):
        if mas[i*2] == 0 or mas[i*2 + 1] == 0:
            mas_in[i] = 1
        elif mas[i*2] == mas[i*2 + 1]:
            mas_in[i] == 0
        else:
            mas_in[i] = proof(i)
    return mas_in


def draw_lines(lines, window, mas_true_points):
    """
    Drawing lines

    :param lines: generated segments
    :param window: windows coordinates
    :param mas_true_points: array of points that hit the screen
    :return: -
    """

    # red is false and lime is true
    colors = ['red', 'lime']

    color = colors[0]

    for i in range(4):
        color = colors[0]
        if mas_true_points[i] == 1:
            color = colors[1]
        plt.plot([lines[i][0][0], lines[i][1][0]], [lines[i][0][1], lines[i][1][1]], color=color)

    plt.plot([window[0][0], window[1][0]], [window[0][1], window[0][1]], color='orange')
    plt.plot([window[0][0], window[0][0]], [window[0][1], window[1][1]], color='orange')
    plt.plot([window[0][0], window[1][0]], [window[1][1], window[1][1]], color='orange')
    plt.plot([window[1][0], window[1][0]], [window[0][1], window[1][1]], color='orange')

    rect = matplotlib.patches.Rectangle(window[0], window[1][0] - window[0][0], window[1][1] - window[1][0])

    plt.show()

def generate_lines():
    """
    generation of segments
    :return: array of generated segments coordinates
    """
    coordinates = np.array([[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]])
    N = random.randint(5, 1000)
    for i in range(4):
        coordinates[i][0][0], coordinates[i][0][1], coordinates[i][1][0], coordinates[i][1][1] = random.randint(0, N),\
            random.randint(0, N), random.randint(0, N), random.randint(0, N)
    return coordinates


def main_window():
    """
    main function with GUI and default values
    """
    points = [(0, 0, 1), (1, 1, 1), (1, 0, 0), (0, 1, 0)]
    default_window_points = np.array([[150, 100], [200, 250]])
    res_points = generate_lines()
    window_points = np.array([[0, 0], [0, 0]])

    def counts():
        point = [0.0, 0.0]
        # 1point
        if x1_field.get() != '':
            window_points[0][0] = float(x1_field.get())
        else:
            window_points[0][0] = float(window_points[0][0])

        if y1_field.get() != '':
            window_points[0][1] = float(y1_field.get())
        else:
            window_points[0][1] = float(window_points[0][1])
        res_points[0] = tuple(point.copy())

        # 2point
        if x2_field.get() != '':
            window_points[1][0] = float(x2_field.get())
        else:
            window_points[1][0] = float(window_points[1][0])

        if y2_field.get() != '':
            window_points[1][1] = float(y2_field.get())
        else:
            window_points[1][1] = float(window_points[1][1])

        res_points[1] = tuple(point.copy())

    def click():
        counts()
        res_points = generate_lines()
        mas_true_points = clipping(res_points, window_points)
        draw_lines(res_points, window_points, mas_true_points)

    def reset():
        x1_field.delete(0, END)
        y1_field.delete(0, END)

        x2_field.delete(0, END)
        y2_field.delete(0, END)

    def set_my_points():
        x1_field.delete(0, END)
        y1_field.delete(0, END)

        x2_field.delete(0, END)
        y2_field.delete(0, END)

        x1_field.insert(0, default_window_points[0][0])
        y1_field.insert(0, default_window_points[0][1])

        x2_field.insert(0, default_window_points[1][0])
        y2_field.insert(0, default_window_points[1][1])

    window = Tk()
    window.title("fourth lab")
    window.geometry('500x500')

    input_lbl = Label(window, text="Input the angular coordinates of the window:", font=("Arial", 14)).place(x=10, y=10)

    x1_lbl = Label(window, text="x1: ", font=("Arial", 14)).place(x=10, y=50)
    x1_field = Entry(window, width=10)
    x1_field.place(x=50, y=50)
    y1_lb = Label(window, text="y1: ", font=("Arial", 14)).place(x=150, y=50)
    y1_field = Entry(window, width=10)
    y1_field.place(x=190, y=50)

    x2_lbl = Label(window, text="x2: ", font=("Arial", 14)).place(x=10, y=90)
    x2_field = Entry(window, width=10)
    x2_field.place(x=50, y=90)
    y2_lb = Label(window, text="y2: ", font=("Arial", 14)).place(x=150, y=90)
    y2_field = Entry(window, width=10)
    y2_field.place(x=190, y=90)

    ok_button = Button(window, text="Ok", command=click)
    ok_button.place(x=50, y=150)

    reset_button = Button(window, text="Reset", command=reset)
    reset_button.place(x=200, y=150)

    my_points_button = Button(window, text="My_points", command=set_my_points)
    my_points_button.place(x=350, y=150)

    window.mainloop()


if __name__ == "__main__":
    main_window()