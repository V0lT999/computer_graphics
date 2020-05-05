import numpy as np
from figures import Sphere
import drawing
from tqdm import tqdm

N = 3
Cw = 600    # width of window
Ch = 600    # height of window
Vw = 1    # width of screen
Vh = 1   # height of screen
d = 1     # distance from camera

spheres = []
BACKGROUND_COLOR = [255, 255, 255]

spheres.append(Sphere([0, -1, 3], 1, [255, 0, 0]))
spheres.append(Sphere([2, 0, 4], 1, [0, 0, 255]))
spheres.append(Sphere([-2, 0, 4], 1, [0, 255, 0]))


def CanvasToViewport(x, y):   # coordinates on screen
    global Cw, Ch, Vw, Vh, d
    return np.array([x*Vw/Cw, y*Vh/Ch, d])


def TraceRay(O, D, t_min, t_max):
    closest_t = np.inf
    closest_sphere = None
    global spheres
    global BACKGROUND_COLOR
    for sphere in spheres:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if t1 > t_min and t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t2 > t_min and t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere is None:
        return BACKGROUND_COLOR

    return closest_sphere.get_elements()['color']


def IntersectRaySphere(O, D, sphere):
    elements = sphere.get_elements()
    C = elements['center']
    r = elements['radius']
    OC = O - C

    k1 = np.dot(D, D)
    k2 = 2*np.dot(OC, D)
    k3 = np.dot(OC, OC) - r*r

    discriminant = k2*k2 - 4*k1*k3
    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-k2 + np.sqrt(discriminant)) / (2*k1)
    t2 = (-k2 - np.sqrt(discriminant)) / (2*k1)
    return t1, t2


def main():
    global Cw
    global Ch
    drawing.set_window(Cw, Ch)
    O = np.array([0, 0, 0])

    for x in tqdm(range(-Cw//2, Cw//2, 1)):
        for y in range(-Ch//2, Ch//2, 1):
            D = CanvasToViewport(x, y)
            color = TraceRay(O, D, 1, np.inf)
            drawing.put_pixel(x, y, color)
    drawing.draw_qt_points()


if __name__ == "__main__":
    main()
