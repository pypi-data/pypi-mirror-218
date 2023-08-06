from TSGEngine.World.Components import Mesh, Transform
from TSGEngine.Core.Math import normalize


class Circle:
    def __init__(self, radius=1, subdivisions=0, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
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

        self.subdivide(subdivisions)

        self.transform.translate(position[0], position[1], position[2])
        self.transform.scale_obj(radius, radius, radius)
        self.transform.scale_obj(scale[0], scale[1], scale[2])
        self.transform.rotate(rotation[0], rotation[1], rotation[2])

    def subdivide(self, subdivisions=1):
        # subdivisions:
        vertices = list(self.mesh.vertices)
        triangles = list(self.mesh.triangles)

        vertices_copy = vertices.copy()
        vertices = []

        # vertices normalization
        for vertices_id in range(0, len(vertices_copy), 3):
            new_point = normalize(
                vertices_copy[vertices_id + 0],
                vertices_copy[vertices_id + 1],
                vertices_copy[vertices_id + 2])
            vertices += [new_point[0], new_point[1], new_point[2]]

        for _ in range(subdivisions):
            new_triangles = []

            for triangle_id in range(0, len(triangles), 3):
                triangle = [triangles[triangle_id], triangles[triangle_id + 1], triangles[triangle_id + 2]]

                new_point = normalize(
                    (vertices[triangle[1] * 3 + 0] + vertices[triangle[2] * 3 + 0]) / 2 * 1.1,
                    (vertices[triangle[1] * 3 + 1] + vertices[triangle[2] * 3 + 1]) / 2 * 1.1,
                    (vertices[triangle[1] * 3 + 2] + vertices[triangle[2] * 3 + 2]) / 2 * 1.1)

                new_triangles += [triangle[0], triangle[1], int(len(vertices) / 3),
                                  triangle[0], int(len(vertices) / 3), triangle[2]]
                vertices += [new_point[0], new_point[1], new_point[2]]

            triangles = new_triangles

        self.mesh.vertices = vertices
        self.mesh.triangles = triangles

    def get_components(self):
        return [self.transform, self.mesh]
