from tqdm import tqdm

import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

pixels = []
Cw = 0
Ch = 0


def set_window(x, y):
    global Cw
    global Ch
    Ch = y
    Cw = x


def put_pixel(hash_map, x, y, color):
    x1 = Cw/2 + x
    y1 = Ch/2 - y - 1

    if x1 < 0 or x1 > Cw or y1 < 0 or y1 > Ch:
        return
    else:
        _color = [min(255, color[0]), min(255, color[1]), min(255, color[2])]
        hash_map.append([x1, y1, _color])


class DrawQt(QWidget):

    global Cw
    global Ch
    global pixels

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(50, 50, Cw, Ch)
        self.setWindowTitle('Ray Tracing')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        size = self.size()

        print(len(pixels))

        for pixel in tqdm(pixels):
            qp.setPen(QColor(pixel[2][0], pixel[2][1], pixel[2][2]))
            # print(pixel[0], pixel[1], pixel[2])
            qp.drawPoint(pixel[0], pixel[1])


def draw_qt_points(hash_map):
    global pixels
    pixels = hash_map
    app = QApplication(sys.argv)
    ex = DrawQt()
    sys.exit(app.exec_())