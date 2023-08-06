from TSGEngine.World.Components import Mesh, Transform


class Rectangle:
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.mesh = Mesh()
        self.transform = Transform()

        self.mesh.vertices = [
            0.0, 0.0, 0.0,
            0.5, 0.5, 0.0,
            0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0,
            -0.5, 0.5, 0.0,
        ]
        self.mesh.triangles = [
            0, 1, 2,
            0, 2, 3,
            0, 3, 4,
            0, 4, 1,
        ]

        self.transform.translate(position[0], position[1], position[2])
        self.transform.scale_obj(scale[0], scale[1], scale[2])
        self.transform.rotate(rotation[0], rotation[1], rotation[2])

    def get_components(self):
        return [self.transform, self.mesh]