import sys, os.path
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/lab1mpl/'))
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
import lab1_library as lb


def main():
    main_window()


def Roberts(data):
    """
    The Roberts algorithm
    :param data: matrix of the coordinates of the cube
    :return: the matrix of transformed coordinates of the cube
    """
    verts = data[0]
    W = np.zeros(3)
    P = [1, -1, 1]

    # search for the barycenter of a cube
    for i in range(2):
        max_value = -10
        min_value = 10
        for point in verts:
            max_value1 = max(point[j][0] for j in range(len(point)))
            max_value = max(max_value, max_value1)
            min_value1 = min(point[j][0] for j in range(len(point)))
            min_value = min(min_value, min_value1)
        W[i] = (max_value + min_value)/2

    new_data = []

    # loop across all faces
    for vector in verts:
        # find the coordinates of two vectors that lie in the plane of the face
        Vec1_x = vector[0][0] - vector[1][0]
        Vec2_x = vector[2][0] - vector[1][0]
        Vec1_y = vector[0][1] - vector[1][1]
        Vec2_y = vector[2][1] - vector[1][1]
        Vec1_z = vector[0][2] - vector[1][2]
        Vec2_z = vector[2][2] - vector[1][2]

        # calculate the coefficients of the plane equation
        A = Vec1_y*Vec2_z - Vec2_y*Vec1_z
        B = Vec1_z*Vec2_x - Vec2_z*Vec1_x
        C = Vec1_x*Vec2_y - Vec2_x*Vec1_y
        D = -(A*vector[0][0] + B*vector[0][1] + C*vector[0][2])

        # find the coefficient that changes the sign of the plane
        m = -(A*W[0] + B*W[1] + C*W[2] + D)

        # correcting the direction of the plane
        A = A*m
        B = B*m
        C = C*m
        D = D*m

        # defining the visibility of faces
        if (A*P[0] + B*P[1] + C*P[2] + D) > 0:
            new_data.append(vector)

    return new_data


def main_window():
    """
    GUI function
    """
    def click():
        angle_f = angle_field.get()
        if angle_f == '':
            angle_f = '0'
        data = lb.rotate_figure(os_combo.get(), angle_f)
        data[0] = Roberts(data)
        lb.plt_show(data)

    def reset():
        lb.plt_show(lb.rotate_figure())


    window = Tk()
    window.title("first lab")
    window.geometry('500x250')

    os_lbl = Label(window, text="Select the axis: ", font=("Arial", 14)).place(x=10, y=10)
    angle_lbl = Label(window, text="Enter the angle:", font=("Arial", 14)).place(x=10, y=50)

    os_combo = Combobox(window)
    os_combo["values"] = ("x", "y", "z")
    os_combo.current(0)
    os_combo.place(x=150, y=10)

    angle_field = Entry(window, width=10)
    angle_field.place(x=150, y=50)

    ok_button = Button(window, text="Ok", command=click)
    ok_button.place(x=150, y=100)

    reset_button = Button(window, text="Reset", command=reset)
    reset_button.place(x=300, y=100)

    window.mainloop()


if __name__ == "__main__":
    main()
