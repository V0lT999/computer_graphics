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