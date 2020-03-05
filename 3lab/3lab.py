import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *

N = 15

def bilinear_surface(verts):
    def get_matrix():
        dots = np.linspace(0, 1, N)
        all_verts = np.transpose([np.tile(dots, len(dots)), np.repeat(dots, len(dots))])
        for i in range(len(all_verts)):
            matrix_a = [1 - all_verts[i][0], all_verts[i][0]]
            matrix_b = [[1 - all_verts[i][1]], [all_verts[i][1]]]
            result[i] = np.dot(bilinear_matrix[0][0], matrix_a[0] * matrix_b[0][0]) + \
                        np.dot(bilinear_matrix[0][1], matrix_a[0] * matrix_b[1][0]) + \
                        np.dot(bilinear_matrix[1][0], matrix_a[1] * matrix_b[0][0]) + \
                        np.dot(bilinear_matrix[1][1], matrix_a[1] * matrix_b[1][0])

    result = np.zeros((N*N, 3))
    #bilinear_matrix = [[[0, 0, 1], [1, 1, 1]], [[1, 0, 0], [0, 1, 0]]]
    bilinear_matrix = [[verts[0], verts[1]], [verts[2], verts[3]]]

    get_matrix()

    result = np.array(result)
    result_x, result_y, result_z = np.array(result[:, 0]), np.array(result[:, 1]), np.array(result[:, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    r = [-1, 1]

    X, Y = np.meshgrid(r, r)
    # plot vertices
    #ax.scatter3D(result[:, 0], result[:, 1], result[:, 2])
    #ax.add_collection3d(Poly3DCollection(result, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    for i in range(len(result)):
        ax.scatter(result_x[i], result_y[i], result_z[i])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

def main_window():
    points = [(0, 0, 1), (1, 1, 1), (1, 0, 0), (0, 1, 0)]
    my_points = [(0, 3, 1), (1, 4, 1), (0, 4, 0), (1, 3, 0)]
    res_points = points.copy()

    def counts():
        point = [0.0, 0.0, 0.0]
        #1point
        if x1_field.get() != '':
            point[0] = float(x1_field.get())
        else:
            point[0] = float(res_points[0][0])

        if y1_field.get() != '':
            point[1] = float(y1_field.get())
        else:
            point[1] = float(res_points[0][1])

        if z1_field.get() != '':
            point[2] = float(z1_field.get())
        else:
            point[2] = float(res_points[0][2])
        res_points[0] = tuple(point.copy())

        #2point
        if x2_field.get() != '':
            point[0] = float(x2_field.get())
        else:
            point[0] = float(res_points[1][0])

        if y2_field.get() != '':
            point[1] = float(y2_field.get())
        else:
            point[1] = float(res_points[1][1])

        if z2_field.get() != '':
            point[2] = float(z2_field.get())
        else:
            point[2] = float(res_points[1][2])

        res_points[1] = tuple(point.copy())

        #3point
        if x3_field.get() != '':
            point[0] = float(x3_field.get())
        else:
            point[0] = float(res_points[2][0])

        if y3_field.get() != '':
            point[1] = float(y3_field.get())
        else:
            point[1] = float(res_points[2][1])

        if z3_field.get() != '':
            point[2] = float(z3_field.get())
        else:
            point[2] = float(res_points[2][2])

        res_points[2] = tuple(point.copy())

        #4point
        if x4_field.get() != '':
            point[0] = float(x4_field.get())
        else:
            point[0] = float(res_points[3][0])

        if y4_field.get() != '':
            point[1] = float(y4_field.get())
        else:
            point[1] = float(res_points[3][1])

        if z4_field.get() != '':
            point[2] = float(z4_field.get())
        else:
            point[2] = float(res_points[3][2])

        res_points[3] = tuple(point.copy())

    def click():
        counts()
        points.copy()
        bilinear_surface(res_points)

    def reset():
        x1_field.delete(0, END)
        y1_field.delete(0, END)
        z1_field.delete(0, END)

        x2_field.delete(0, END)
        y2_field.delete(0, END)
        z2_field.delete(0, END)

        x3_field.delete(0, END)
        y3_field.delete(0, END)
        z3_field.delete(0, END)

        x4_field.delete(0, END)
        y4_field.delete(0, END)
        z4_field.delete(0, END)

        x1_field.insert(0, points[0][0])
        y1_field.insert(0, points[0][1])
        z1_field.insert(0, points[0][2])

        x2_field.insert(0, points[1][0])
        y2_field.insert(0, points[1][1])
        z2_field.insert(0, points[1][2])

        x3_field.insert(0, points[2][0])
        y3_field.insert(0, points[2][1])
        z3_field.insert(0, points[2][2])

        x4_field.insert(0, points[3][0])
        y4_field.insert(0, points[3][1])
        z4_field.insert(0, points[3][2])


    def rotate():
        alfa = int(angle_field.get())
        cos_alfa = np.cos(alfa)
        sin_alfa = np.sin(alfa)
        matrix = np.zeros((3,3))
        if os_combo.get() == 'x':
            matrix = np.array([[1, 0, 0], [0, cos_alfa, -sin_alfa], [0, sin_alfa, cos_alfa]])
        else:
            matrix = np.array([[cos_alfa, 0, sin_alfa], [0, 1, 0], [-sin_alfa, 0, cos_alfa]])

        for i in range(4):
            res_points[i] = np.dot(res_points[i], matrix)

        bilinear_surface(res_points)

    def set_my_points():
        x1_field.delete(0, END)
        y1_field.delete(0, END)
        z1_field.delete(0, END)

        x2_field.delete(0, END)
        y2_field.delete(0, END)
        z2_field.delete(0, END)

        x3_field.delete(0, END)
        y3_field.delete(0, END)
        z3_field.delete(0, END)

        x4_field.delete(0, END)
        y4_field.delete(0, END)
        z4_field.delete(0, END)

        x1_field.insert(0, my_points[0][0])
        y1_field.insert(0, my_points[0][1])
        z1_field.insert(0, my_points[0][2])

        x2_field.insert(0, my_points[1][0])
        y2_field.insert(0, my_points[1][1])
        z2_field.insert(0, my_points[1][2])

        x3_field.insert(0, my_points[2][0])
        y3_field.insert(0, my_points[2][1])
        z3_field.insert(0, my_points[2][2])

        x4_field.insert(0, my_points[3][0])
        y4_field.insert(0, my_points[3][1])
        z4_field.insert(0, my_points[3][2])
        
    window = Tk()
    window.title("first lab")
    window.geometry('500x500')

    x1_lbl = Label(window, text="x1: ", font=("Arial", 14)).place(x=10, y=10)
    x1_field = Entry(window, width=10)
    x1_field.place(x=50, y=10)
    y1_lb = Label(window, text="y1: ", font=("Arial", 14)).place(x=150, y=10)
    y1_field = Entry(window, width=10)
    y1_field.place(x=190, y=10)
    z1_lbl = Label(window, text="z1: ", font=("Arial", 14)).place(x=290, y=10)
    z1_field = Entry(window, width=10)
    z1_field.place(x=330, y=10)

    x2_lbl = Label(window, text="x2: ", font=("Arial", 14)).place(x=10, y=50)
    x2_field = Entry(window, width=10)
    x2_field.place(x=50, y=50)
    y2_lb = Label(window, text="y2: ", font=("Arial", 14)).place(x=150, y=50)
    y2_field = Entry(window, width=10)
    y2_field.place(x=190, y=50)
    z2_lbl = Label(window, text="z2: ", font=("Arial", 14)).place(x=290, y=50)
    z2_field = Entry(window, width=10)
    z2_field.place(x=330, y=50)

    x3_lbl = Label(window, text="x3: ", font=("Arial", 14)).place(x=10, y=90)
    x3_field = Entry(window, width=10)
    x3_field.place(x=50, y=90)
    y3_lb = Label(window, text="y3: ", font=("Arial", 14)).place(x=150, y=90)
    y3_field = Entry(window, width=10)
    y3_field.place(x=190, y=90)
    z3_lbl = Label(window, text="z3: ", font=("Arial", 14)).place(x=290, y=90)
    z3_field = Entry(window, width=10)
    z3_field.place(x=330, y=90)

    x4_lbl = Label(window, text="x4: ", font=("Arial", 14)).place(x=10, y=130)
    x4_field = Entry(window, width=10)
    x4_field.place(x=50, y=130)
    y4_lb = Label(window, text="y4: ", font=("Arial", 14)).place(x=150, y=130)
    y4_field = Entry(window, width=10)
    y4_field.place(x=190, y=130)
    z4_lbl = Label(window, text="z4: ", font=("Arial", 14)).place(x=290, y=130)
    z4_field = Entry(window, width=10)
    z4_field.place(x=330, y=130)

    ok_button = Button(window, text="Ok", command=click)
    ok_button.place(x=110, y=290)

    reset_button = Button(window, text="Reset", command=reset)
    reset_button.place(x=260, y=290)

    my_points_button = Button(window, text="My_points", command=set_my_points)
    my_points_button.place(x=410, y=290)

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