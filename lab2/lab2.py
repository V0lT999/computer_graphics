import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from tkinter import *
from tkinter.ttk import *


def B(x, k, i, t):
    if k == 0:
        return 1.0 if t[i] <= x < t[i+1] else 0.0
    if t[i+k] == t[i]:
        c1 = 0.0
    else:
        c1 = (x - t[i])/(t[i+k] - t[i]) * B(x, k-1, i, t)
    if t[i+k+1] == t[i+1]:
        c2 = 0.0
    else:
       c2 = (t[i+k+1] - x)/(t[i+k+1] - t[i+1]) * B(x, k-1, i+1, t)
    return c1 + c2


def bspline(x, t, c, k):
    n = len(t) - k - 1
    assert (n >= k+1) and (len(c) >= n)
    return sum(c[i] * B(x, k, i, t) for i in range(n))


def draw_spline(points):
    # x = [points[i][0] for i in range(7)]
    # y = [points[i][1] for i in range(7)]
    #
    # data = np.array(points)
    #
    # colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    # length = len(x)
    # u3 = np.linspace(0, 1, 70, endpoint=False)
    # plt.plot(x, y, 'k--', label='Control polygon', marker='o', markerfacecolor='red')
    # plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
    # plt.title('Cubic B-spline curve evaluation')
    # for k in range(1, 7):
    #     number_of_internal_knots = length - k + 1
    #     knot_vector = np.linspace(0, 1, number_of_internal_knots, endpoint=True)
    #     knot_vector = np.append([0] * k, knot_vector)
    #     knot_vector = np.append(knot_vector, [1] * k)
    #     plt.plot([bspline(z, knot_vector, x, k) for z in u3],
    #              [bspline(z, knot_vector, y, k) for z in u3],
    #              colors[k - 1], lw=2, label=f'B-spline curve {k} degree')
    colors = ['r', 'orange', 'yellow', 'lime', 'b', 'navy', 'm']
    lin_p = np.linspace(0, 1, 100, endpoint=False)
    xx = [points[i][0] for i in range(7)]
    yy = [points[i][1] for i in range(7)]

    data = np.array(points)

    for k in range(1, 7):
        t = np.linspace(0, 1, 7 - k + 1, endpoint=True)
        t = np.append([0] * k, t)
        t = np.append(t, [1] * k)

        plt.plot([bspline(x, t, xx, k) for x in lin_p],
                 [bspline(x, t, yy, k) for x in lin_p], colors[k-1], lw=2, label=f'B-spline of degree {k}')

    # tck, u = interpolate.splprep(data.transpose(), s=0)
    # unew = np.arange(0, 1.01, 0.01)
    # out = interpolate.splev(unew, tck)
    #
    # plt.figure()
    # plt.plot(out[0], out[1], color='orange')
    plt.legend(loc='upper right')
    plt.plot(data[:, 0], data[:, 1], 'ob')
    plt.show()


def main_window():
    points = [(3.28, 0.00), (4.00, 0.50), (4.40, 1.0), (4.60, 1.52), (5.00, 2.5), (5.00, 3.34), (4.70, 3.8)]
    res_points = points

    def counts():
        point = [0.0, 0.0]
        #1point
        if x1_field.get() != '':
            point[0] = float(x1_field.get())
        else:
            point[0] = float(res_points[0][0])

        if y1_field.get() != '':
            point[1] = float(y1_field.get())
        else:
            point[1] = float(res_points[0][1])

        res_points[0] = tuple(point)

        #2point
        if x2_field.get() != '':
            point[0] = float(x2_field.get())
        else:
            point[0] = float(res_points[1][0])

        if y2_field.get() != '':
            point[1] = float(y2_field.get())
        else:
            point[1] = float(res_points[1][1])

        res_points[1] = tuple(point)

        #3point
        if x3_field.get() != '':
            point[0] = float(x3_field.get())
        else:
            point[0] = float(res_points[2][0])

        if y3_field.get() != '':
            point[1] = float(y3_field.get())
        else:
            point[1] = float(res_points[2][1])

        res_points[2] = tuple(point)

        #4point
        if x4_field.get() != '':
            point[0] = float(x4_field.get())
        else:
            point[0] = float(res_points[3][0])

        if y4_field.get() != '':
            point[1] = float(y4_field.get())
        else:
            point[1] = float(res_points[3][1])

        res_points[3] = tuple(point)

        #5point
        if x5_field.get() != '':
            point[0] = float(x5_field.get())
        else:
            point[0] = float(res_points[4][0])

        if y5_field.get() != '':
            point[1] = float(y5_field.get())
        else:
            point[1] = float(res_points[4][1])

        res_points[4] = tuple(point)

        #6point
        if x6_field.get() != '':
            point[0] = float(x6_field.get())
        else:
            point[0] = float(res_points[5][0])

        if y6_field.get() != '':
            point[1] = float(y6_field.get())
        else:
            point[1] = float(res_points[5][1])

        res_points[5] = tuple(point)

        #7point
        if x7_field.get() != '':
            point[0] = float(x7_field.get())
        else:
            point[0] = float(res_points[6][0])

        if y7_field.get() != '':
            point[1] = float(y7_field.get())
        else:
            point[1] = float(res_points[6][1])

        res_points[6] = tuple(point)

    def click():
        counts()
        draw_spline(res_points)

    def reset():
        res_points = points
        draw_spline(points)

    def rotate():
        return 1

    window = Tk()
    window.title("first lab")
    window.geometry('500x500')

    x1_lbl = Label(window, text="x1: ", font=("Arial", 14)).place(x=10, y=10)
    x1_field = Entry(window, width=10)
    x1_field.place(x=50, y=10)
    y1_lb = Label(window, text="y1: ", font=("Arial", 14)).place(x=150, y=10)
    y1_field = Entry(window, width=10)
    y1_field.place(x=190, y=10)

    x2_lbl = Label(window, text="x2: ", font=("Arial", 14)).place(x=10, y=50)
    x2_field = Entry(window, width=10)
    x2_field.place(x=50, y=50)
    y2_lb = Label(window, text="y2: ", font=("Arial", 14)).place(x=150, y=50)
    y2_field = Entry(window, width=10)
    y2_field.place(x=190, y=50)

    x3_lbl = Label(window, text="x3: ", font=("Arial", 14)).place(x=10, y=90)
    x3_field = Entry(window, width=10)
    x3_field.place(x=50, y=90)
    y3_lb = Label(window, text="y3: ", font=("Arial", 14)).place(x=150, y=90)
    y3_field = Entry(window, width=10)
    y3_field.place(x=190, y=90)

    x4_lbl = Label(window, text="x4: ", font=("Arial", 14)).place(x=10, y=130)
    x4_field = Entry(window, width=10)
    x4_field.place(x=50, y=130)
    y4_lb = Label(window, text="y4: ", font=("Arial", 14)).place(x=150, y=130)
    y4_field = Entry(window, width=10)
    y4_field.place(x=190, y=130)

    x5_lbl = Label(window, text="x5: ", font=("Arial", 14)).place(x=10, y=170)
    x5_field = Entry(window, width=10)
    x5_field.place(x=50, y=170)
    y5_lb = Label(window, text="y5: ", font=("Arial", 14)).place(x=150, y=170)
    y5_field = Entry(window, width=10)
    y5_field.place(x=190, y=170)

    x6_lbl = Label(window, text="x6: ", font=("Arial", 14)).place(x=10, y=210)
    x6_field = Entry(window, width=10)
    x6_field.place(x=50, y=210)
    y6_lb = Label(window, text="y6: ", font=("Arial", 14)).place(x=150, y=210)
    y6_field = Entry(window, width=10)
    y6_field.place(x=190, y=210)

    x7_lbl = Label(window, text="x7: ", font=("Arial", 14)).place(x=10, y=250)
    x7_field = Entry(window, width=10)
    x7_field.place(x=50, y=250)
    y7_lb = Label(window, text="y7: ", font=("Arial", 14)).place(x=150, y=250)
    y7_field = Entry(window, width=10)
    y7_field.place(x=190, y=250)


    ok_button = Button(window, text="Ok", command=click)
    ok_button.place(x=150, y=290)

    reset_button = Button(window, text="Reset", command=reset)
    reset_button.place(x=300, y=290)

    combo_lbl = Label(window, text="Select the axis: ", font=("Arial", 14)).place(x=10, y=330)
    os_combo = Combobox(window)
    os_combo["values"] = ("x", "y")
    os_combo.current(0)
    os_combo.place(x=150, y=330)

    angle_lbl = Label(window, text="Enter the angle:", font=("Arial", 14)).place(x=10, y=370)
    angle_field = Entry(window, width=10)
    angle_field.place(x=150, y=370)

    rotate_button = Button(window, text="Rotate", command=rotate)
    rotate_button.place(x=300, y=370)

    #reset()

    window.mainloop()



if __name__ == "__main__":
    main_window()