import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *


def plt_show(data):
    verts = data[0]
    res_matrix = data[1]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r = [-1, 1]

    X, Y = np.meshgrid(r, r)
    # plot vertices
    ax.scatter3D(res_matrix[:, 0], res_matrix[:, 1], res_matrix[:, 2])

    # plot sides
    ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    ax.scatter([1], [-1], [1])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt. show()

def rotate_figure(os='y', angle_s='0'):
    angle = int(angle_s)

    matrix = [
        [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5],
        [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5]
    ]
    T = [[]]
    res_matrix = np.zeros((8, 3))
    cos_count = np.cos(angle)
    sin_count = np.sin(angle)

    if os == "x":
        T = np.array([[1, 0, 0], [0, cos_count, sin_count], [0, -sin_count, cos_count]])
        res_matrix = np.dot(matrix, T.transpose())
    elif os == "y":
        T = np.array([[cos_count, 0, -sin_count], [0, 1, 0], [sin_count, 0, cos_count]])
        res_matrix = np.dot(matrix, T)
    elif os == "z":
        T = np.array([[cos_count, sin_count, 0], [-sin_count, cos_count, 0], [0, 0, 1]])
        res_matrix = np.dot(matrix, T)
    else:
        res_matrix = matrix

    verts = [[res_matrix[0], res_matrix[1], res_matrix[2], res_matrix[3]],
             [res_matrix[4], res_matrix[5], res_matrix[6], res_matrix[7]],
             [res_matrix[0], res_matrix[1], res_matrix[5], res_matrix[4]],
             [res_matrix[2], res_matrix[3], res_matrix[7], res_matrix[6]],
             [res_matrix[1], res_matrix[2], res_matrix[6], res_matrix[5]],
             [res_matrix[4], res_matrix[7], res_matrix[3], res_matrix[0]],
    ]

    return [verts, res_matrix]
