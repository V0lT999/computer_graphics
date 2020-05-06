import numpy as np
from figures import Sphere
from figures import Light
import drawing
from tqdm import tqdm, trange
from multiprocessing import Process, Manager
from multiprocessing import Pool

thread_count = 0
N = 3
Cw = 600    # width of window
Ch = 600    # height of window
Vw = 1    # width of screen
Vh = 1   # height of screen
d = 1     # distance from camera
center_window = np.array([0, 0, 0])

spheres = []
lights = []
BACKGROUND_COLOR = [255, 255, 255]

spheres.append(Sphere([0, -1, 3], 1, [255, 0, 0], _specular=500))
spheres.append(Sphere([2, 0, 4], 1, [0, 0, 255], _specular=500))
spheres.append(Sphere([-2, 0, 4], 1, [0, 255, 0], _specular=10))
spheres.append(Sphere([0, -5001, 0], 5000, [250, 250, 50], _specular=1000))

lights.append(Light(0, 0.2))
lights.append(Light(1, 0.6, _position=[2, 1, 0]))
lights.append(Light(2, 0.2, _direction=[1, 4, 4]))


hash_map = []


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

    P = O + closest_t*D
    N = P - closest_sphere.get_elements()['center']
    N = N / np.linalg.norm(N)
    return np.array(closest_sphere.get_elements()['color']) * ComputeLighing(P, N, -D, closest_sphere.get_elements()['specular'])


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

def ComputeLighing(P, N, V, s):
    global lights
    i = 0.0
    for light in lights:
        if light.get_elements()['type'] == 'ambient':
            i += light.get_elements()['intensity']
        else:
            L = []
            if light.get_elements()['type'] == 'point':
                L = (light.get_elements()['position'] - P).copy()
            else:
                L = light.get_elements()['direction'].copy()

            #diffuse
            NL = np.dot(N, L)
            if NL > 0:
                i += light.get_elements()['intensity']*NL/(np.linalg.norm(N)*np.linalg.norm(L))

            #mirror
            if s != -1:
                R = 2*N*np.dot(N, L) - L
                RV = np.dot(R, V)
                if RV > 0:
                    i += light.get_elements()['intensity']*np.power(RV/(np.linalg.norm(R)*np.linalg.norm(V)), s)

    return i


def processing(i, array):
    global Ch
    global center_window
    global thread_count

    hash_mapp = []
    text = 'progressbar #{position}'.format(position=i)
    bar = tqdm(array, position=0, desc=text, leave=True)
    for x in bar:
        for y in range(-Ch//2, Ch//2, 1):
            D = CanvasToViewport(x, y)
            color = TraceRay(center_window, D, 1, np.inf)

            x1 = Cw / 2 + x
            y1 = Ch / 2 - y - 1

            if x1 < 0 or x1 > Cw or y1 < 0 or y1 > Ch:
                return
            else:
                _color = [min(255, color[0]), min(255, color[1]), min(255, color[2])]
                hash_mapp.append([x1, y1, _color])

    return hash_mapp

def main():
    global Cw
    global Ch
    global center_window
    drawing.set_window(Cw, Ch)

    global thread_count
    thread_count = 4
    mas = np.array(np.linspace(-Cw/2, Cw/2, Cw))
    global hash_map
    hash_map = Manager().list()
    part = Cw // thread_count

    pool = Pool(processes=thread_count)
    output = [pool.apply_async(processing, args=(i, mas[i*part:(i + 1)*part])) for i in range(thread_count)]
    result_buf = [p.get() for p in output]
    result = []
    for row in result_buf:
        for j in row:
            result.append(j)

    drawing.draw_qt_points(result)


if __name__ == "__main__":
    main()
