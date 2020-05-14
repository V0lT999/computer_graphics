import numpy as np

from figures import Sphere
from figures import Light
import drawing

from tqdm import tqdm, trange

from multiprocessing import Pool

thread_count = 0  # the thread's count
Cw = 600    # width of window
Ch = 600    # height of window
Vw = 1    # width of screen
Vh = 1   # height of screen
d = 1     # distance from camera
center_window = np.array([0, 0, 0])
recursion_depth = 2  # specularity

# object initialization
spheres = []
lights = []
BACKGROUND_COLOR = [150, 150, 150]

spheres.append(Sphere([0, -1, 3], 1, [255, 0, 0], _specular=500, _reflective=0.2, _camera=center_window.copy()))
spheres.append(Sphere([2, 0, 4], 1, [0, 0, 255], _specular=500, _reflective=0, _camera=center_window.copy()))
spheres.append(Sphere([-2, 0, 4], 1, [0, 255, 0], _specular=10, _reflective=0.4, _camera=center_window.copy()))
spheres.append(Sphere([0, -5001, 0], 5000, [250, 250, 50], _specular=1000, _reflective=0, _camera=center_window.copy()))

lights.append(Light(0, 0.2))
lights.append(Light(1, 0.6, _position=[2, 1, 0]))
lights.append(Light(2, 0.2, _direction=[1, 4, 4]))


def CanvasToViewport(x, y):
    """
    change coordinate system
    :param x: system x
    :param y: system y
    :return: new coordinates
    """
    global Cw, Ch, Vw, Vh, d
    return np.array([x*Vw/Cw, y*Vh/Ch, d])


def ClosestIntersection(O, D, t_min, t_max):
    """
    Finding intersections of rays with a sphere
    :param O: Starting point of the beam
    :param D: Ray coordinates
    :param t_min: minimum parameter
    :param t_max: maximum parameter
    :return: closest_sphere and closest t parameter
    """
    closest_t = np.inf
    closest_sphere = None
    global spheres

    DD = np.dot(D, D)

    for sphere in spheres:
        t1, t2 = IntersectRaySphere(O, D, DD, sphere)
        if t1 > t_min and t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t2 > t_min and t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    return closest_sphere, closest_t


def ClosestIntersection_P(O, D, t_min, t_max):
    """
    Finding intersections of rays with spheres when mirroring
    :param O: Starting point of the beam
    :param D: Ray coordinates
    :param t_min: minimum parameter
    :param t_max: maximum parameter
    :return: closest_sphere and closest t parameter
    """
    closest_t = np.inf
    closest_sphere = None
    global spheres

    DD = np.dot(D, D)

    for sphere in spheres:
        t1, t2 = IntersectRaySphere_P(O, D, DD, sphere)
        if t1 > t_min and t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t2 > t_min and t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    return closest_sphere, closest_t


def ReflectRay(R, N):
    """
    counting the reflection beam
    :param R: ray
    :param N: normal line
    :return: reflection beam
    """
    return 2*N*np.dot(N, R) - R


def TraceRay(O, D, t_min, t_max, depth):
    """
    Counts the color of the sphere at the nearest point t in the interval
    :param O: Starting point of the beam
    :param D: Ray coordinates
    :param t_min: minimum parameter
    :param t_max: maximum parameter
    :param depth: parameter of the mirror index
    :return: color of point
    """
    global BACKGROUND_COLOR

    closest_sphere, closest_t = ClosestIntersection(O, D, t_min, t_max)

    if closest_sphere is None:
        return BACKGROUND_COLOR

    P = np.array(O + closest_t*D)
    N = P - closest_sphere.get_elements()['center']
    N = N / np.linalg.norm(N)
    local_color = np.array(closest_sphere.get_elements()['color']) * ComputeLighing(P, N, -D, closest_sphere.get_elements()['specular'])

    reflective = closest_sphere.get_elements()['reflective']
    if depth <= 0 or reflective <= 0:
        return local_color

    R = ReflectRay(-D, N)
    reflected_color = TraceRay_P(P, R, 0.001, np.inf, depth - 1)

    return np.array(np.dot(local_color, (1 - reflective)) + np.dot(reflected_color, reflective))


def TraceRay_P(O, D, t_min, t_max, depth):
    """
        Counts the color of the sphere at the nearest point t in the interval when mirroring
        :param O: Starting point of the beam
        :param D: Ray coordinates
        :param t_min: minimum parameter
        :param t_max: maximum parameter
        :param depth: parameter of the mirror index
        :return: color of point
        """
    global BACKGROUND_COLOR

    closest_sphere, closest_t = ClosestIntersection_P(O, D, t_min, t_max)

    if closest_sphere is None:
        return BACKGROUND_COLOR

    # the calculation of the local color
    P = np.array(O + closest_t*D)
    N = P - closest_sphere.get_elements()['center']
    N = N / np.linalg.norm(N)
    local_color = np.array(closest_sphere.get_elements()['color']) * ComputeLighing(P, N, -D, closest_sphere.get_elements()['specular'])

    # If we have reached the recursion limit or the object is not reflective, then we are done
    reflective = closest_sphere.get_elements()['reflective']
    if depth <= 0 or reflective <= 0:
        return local_color

    # Calculating the color of the reflected beam
    R = ReflectRay(-D, N)
    reflected_color = TraceRay_P(P, R, 0.001, np.inf, depth - 1)

    return np.array(np.dot(local_color, (1 - reflective)) + np.dot(reflected_color, reflective))


def IntersectRaySphere(O, D, DD, sphere):
    """
    Solves the square equation
    :param O: Starting point of the beam
    :param D: Ray coordinates
    :param DD: dot(D, D)
    :param sphere: sphere
    :return: Intersection
    """
    global center_window

    rr = sphere.get_rr()
    OC = sphere.get_oc()
    k3 = sphere.get_ococ() - rr


    k1 = DD
    k2 = 2*np.dot(OC, D)

    discriminant = k2*k2 - 4*k1*k3
    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-k2 + np.sqrt(discriminant)) / (2*k1)
    t2 = (-k2 - np.sqrt(discriminant)) / (2*k1)
    return t1, t2


def IntersectRaySphere_P(O, D, DD, sphere):
    """
    Solves the square equation when mirroring
    :param O: Starting point of the beam
    :param D: Ray coordinates
    :param DD: dot(D, D)
    :param sphere: sphere
    :return: Intersection
    """
    global center_window

    rr = sphere.get_rr()
    OC = O - sphere.get_elements()['center']
    k3 = np.dot(OC, OC) - rr

    k1 = DD
    k2 = 2*np.dot(OC, D)

    discriminant = k2*k2 - 4*k1*k3
    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-k2 + np.sqrt(discriminant)) / (2*k1)
    t2 = (-k2 - np.sqrt(discriminant)) / (2*k1)
    return t1, t2


def ComputeLighing(P, N, V, s):
    """
    Calculation of lighting
    :param P: to calculate the intersection
    :param N: calculating the sphere normal at the intersection point
    :param V: overview vector
    :param s: the reflection rate
    :return: the lighting coefficient
    """
    global lights
    i = 0.0
    for light in lights:
        if light.get_elements()['type'] == 'ambient':
            i += light.get_elements()['intensity']
        else:
            L = []
            if light.get_elements()['type'] == 'point':
                L = (light.get_elements()['position'] - P).copy()
                t_max = 1
            else:
                L = light.get_elements()['direction'].copy()
                t_max = np.inf

            #shadow
            shadow_sphere, shadow_t = ClosestIntersection_P(P, L, 0.001, t_max)
            if shadow_sphere != None:
                continue

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
    """
    counting function for a single stream
    :param i: index of stream
    :param array: coordinates array
    :return: counted rays
    """
    global Ch
    global center_window
    global recursion_depth

    hash_mapp = []
    text = 'progressbar #{position}'.format(position=i)
    bar = tqdm(array, position=0, desc=text, leave=True)
    for x in bar:
        for y in range(-Ch//2, Ch//2, 1):
            D = CanvasToViewport(x, y)
            color = TraceRay(center_window.copy(), D, 1, np.inf, recursion_depth)

            x1 = Cw / 2 + x
            y1 = Ch / 2 - y - 1

            if x1 < 0 or x1 > Cw or y1 < 0 or y1 > Ch:
                return
            else:
                _color = [min(255, color[0]), min(255, color[1]), min(255, color[2])]
                hash_mapp.append([x1, y1, _color])

    return hash_mapp

def main():
    """
    main function
    """
    global Cw
    global Ch
    drawing.set_window(Cw, Ch)

    print("I'm sorry, Python is soooo slow :( please wait\n ")

    global thread_count
    thread_count = 4
    mas = np.array(np.linspace(-Cw/2, Cw/2, Cw))
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
