class Sphere:
    def __init__(self, _center=[0, 0, 0], _radius=1, _color=[0, 0, 0],
                    _specular=500, _reflective=0):

        self.center = _center
        self.radius = _radius
        self.color = _color
        self.specular = _specular
        self.reflective = _reflective

    def get_elements(self):
        return {'center': self.center, 'radius': self.radius, 'color': self.color, 'specular': self.specular, 'reflective': self.reflective}


Lights_type = ['ambient', 'point', 'directional']


class Light:
    global Lights_type

    def __init__(self, _type, _intensity, _position=None, _direction=None):
        self.type = Lights_type[_type]
        self.intensity = _intensity
        self.position = _position
        self.direction = _direction

    def get_elements(self):
        return {'type': self.type, 'intensity': self.intensity, 'position': self.position, 'direction': self.direction}
