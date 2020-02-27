from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from tkinter import *
from tkinter.ttk import *
import numpy as np


# def init():
#     ambient = (1.0, 1.0, 1.0, 1)
#     lightpos = (1.0, 1.0, 1.0)
#
#     glClearColor(0.0, 0.0, 0.0, 0.0)
#     glClearDepth(1.0)
#     glDepthFunc(GL_LESS)
#     glEnable(GL_DEPTH_TEST)
#     glShadeModel(GL_SMOOTH)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(45.0, float(300) / float(300), 0.1, 100.0)
#     glMatrixMode(GL_MODELVIEW)
#
#
# def keyPressed(*args):
#     if args[0] == '\033':
#         sys.exit()
#
#
# def rotate_figure(os='x', angle_s='0'):
#     # def draw():
#     #     glClear(GL_COLOR_BUFFER_BIT)
#     #     glPushMatrix()
#     #
#     #     glBegin(GL_POLYGON)
#     #     glColor3f(0.0, 1.0, 0.0)
#     #     for i in range(24):
#     #         glVertex3f(res_matrix[i][0], res_matrix[i][1], res_matrix[i][2])
#     #     glEnd()
#     #
#     #     glutSwapBuffers()
#
#     print(os, angle_s)
#     angle = int(angle_s)
#     matrix = [
#         [0.5, -0.5, -0.5, 1], [0.5,  0.5, -0.5, 1], [-0.5,  0.5, -0.5, 1], [-0.5, -0.5, -0.5, 1],
#         [0.5, -0.5, 0.5, 1], [0.5,  0.5, 0.5, 1], [-0.5,  0.5, 0.5, 1], [-0.5, -0.5, 0.5, 1],
#         [0.5, -0.5, -0.5, 1], [0.5,  0.5, -0.5, 1], [0.5,  0.5,  0.5, 1], [0.5, -0.5,  0.5, 1],
#         [-0.5, -0.5,  0.5, 1], [-0.5,  0.5,  0.5, 1], [-0.5,  0.5, -0.5, 1], [-0.5, -0.5, -0.5, 1],
#         [0.5,  0.5,  0.5, 1], [0.5,  0.5, -0.5, 1], [-0.5,  0.5, -0.5, 1], [-0.5,  0.5,  0.5, 1],
#         [0.5, -0.5, -0.5, 1], [0.5, -0.5,  0.5, 1], [-0.5, -0.5,  0.5, 1], [-0.5, -0.5, -0.5, 1]
#     ]
#     matrix = np.dot(matrix, 100)
#     T = [[]]
#     res_matrix = [[]]
#     cos_count = np.cos(angle)
#     sin_count = np.sin(angle)
#     print(cos_count, ' ', sin_count)
#
#     if os == "x":
#         T = [[1, 0, 0, 0], [0, cos_count, sin_count, 0], [0, -sin_count, cos_count, 0], [0, 0, 0, 1]]
#         T = np.dot(T, 100)
#         res_matrix = np.dot(matrix, T.transpose())
#     elif os == "y":
#         T = [[cos_count, 0, -sin_count, 0], [0, 1, 0, 0], [sin_count, 0, cos_count, 0], [0, 0, 0, 1]]
#         T = np.dot(T, 100)
#         res_matrix = np.dot(matrix, T)
#     elif os == "z":
#         T = [[cos_count, sin_count, 0, 0], [-sin_count, cos_count, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
#         T = np.dot(T, 100)
#         res_matrix = np.dot(matrix, T)
#     else:
#         res_matrix = matrix
#
#     #draw()
#     glClear(GL_COLOR_BUFFER_BIT)
#     glPushMatrix()
#
#     glBegin(GL_POLYGON) #GL_QUADS
#     glColor3f(0.0, 1.0, 0.0)
#     for i in range(24):
#         glVertex3f(res_matrix[i][0], res_matrix[i][1], res_matrix[i][2])
#     glEnd()
#
#     glutSwapBuffers()
#
# def main_window():
#     def click():
#         angle_f = angle_field.get()
#         if angle_f == '':
#             angle_f = '0'
#         rotate_figure(os_combo.get(), angle_f)
#         glutPostRedisplay()
#
#     window = Tk()
#     window.title("first lab")
#     window.geometry('500x250')
#
#     os_lbl = Label(window, text="Select the axis: ", font=("Arial", 14)).place(x=10, y=10)
#     angle_lbl = Label(window, text="Enter the angle:", font=("Arial", 14)).place(x=10, y=50)
#
#     os_combo = Combobox(window)
#     os_combo["values"] = ("x", "y", "z")
#     os_combo.current(0)
#     os_combo.place(x=150, y=10)
#
#     angle_field = Entry(window, width=10)
#     angle_field.place(x=150, y=50)
#
#     ok_button = Button(window, text="Ok", command=click)
#     ok_button.place(x=150, y=100)
#
#     #window.mainloop()
#
#
# def main():
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) #GLUT_DOUBLE | GLUT_RGB
#     glutInitWindowSize(300, 300)
#     glutInitWindowPosition(50, 50)
#     glutInit(sys.argv)
#     glutCreateWindow(b"Happy New Year!")
#     glutDisplayFunc(rotate_figure())
#     glutIdleFunc(rotate_figure())
#     glutKeyboardFunc(keyPressed)
#     init()
#     #main_window()
#     glutMainLoop()

ESCAPE = '\033'

window = 0

# rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0

DIRECTION = 1


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y): #*args
    if key == ESCAPE: #args[0]
        sys.exit()
    elif key == GLUT_KEY_UP:
        glRotatef(30, 1.0, 0.0, 0.0)
    elif key == 'w':
        glRotatef(30, 1.0, 0.0, 0.0)


def DrawGLScene():
    global X_AXIS, Y_AXIS, Z_AXIS
    global DIRECTION

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)

    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)

    # Draw Cube (multiple quads)
    glBegin(GL_QUADS)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()

    X_AXIS = X_AXIS - 0.30
    Z_AXIS = Z_AXIS - 0.30

    glutSwapBuffers()


def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow('OpenGL Python Cube')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutSpecialFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()