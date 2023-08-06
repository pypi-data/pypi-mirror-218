from dataclasses import dataclass
from TSGEngine.Rendering import Mesh as Mesh_api
from numpy import uint32, array, float32


@dataclass
class Mesh:
    def __init__(self):
        self._vertices = array([], dtype=float32)
        self._colors = array([], dtype=float32)
        self._triangles = array([], dtype=uint32)
        self._texcoord = array([], dtype=float32)

        self.shader_name = 'main'

        self.mesh_api = Mesh_api()

    @property
    def VAO(self):
        return self.mesh_api.VAO

    @property
    def VBO(self):
        return self.mesh_api.VBO

    @property
    def EBO(self):
        return self.mesh_api.EBO

    @property
    def num_points(self):
        return len(self._triangles)

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self.bind_new_vbo(vertices=vertices)

    @property
    def triangles(self):
        return self._triangles

    @triangles.setter
    def triangles(self, indexes):
        self.bind_new_ebo(indexes)

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        self.bind_new_vbo(colors=colors)

    @property
    def texcoord(self):
        return self._texcoord

    @texcoord.setter
    def texcoord(self, texcoord):
        self.bind_new_vbo(texcoord=texcoord)

    def bind_new_vbo(self, vertices=None, colors=None, texcoord=None, texture_normalization=False):
        # checks for given colors and vertices
        if vertices is not None:
            vertices = array(vertices, dtype=float32)
        else:
            vertices = self.vertices

        if colors is not None:
            colors = array(colors, dtype=float32)
        else:
            colors = self.colors

        if texcoord is not None:
            texcoord = array(texcoord, dtype=float32)
        else:
            texcoord = self.texcoord

        if len(texcoord) > 0 and texture_normalization:
            if max(texcoord) > 1 or min(texcoord) < 0:
                texcoord -= min(texcoord)
                texcoord /= max(texcoord)

        # resizes colors to vertices len
        if len(vertices) > len(colors):
            # noinspection PyTypeChecker
            colors.resize(len(vertices), refcheck=False)

        if len(vertices) / 3 * 2 > len(texcoord):
            # noinspection PyTypeChecker
            texcoord.resize(int(len(vertices) / 3 * 2), refcheck=False)

        # creates vbo array cuz renderer use combined array
        arr = []
        for i in range(1, int(len(vertices) / 3) + 1):
            arr += [vertices[(3 * i - 1) - 2], vertices[(3 * i - 1) - 1], vertices[(3 * i - 1)],
                    colors[(3 * i - 1) - 2], colors[(3 * i - 1) - 1], colors[(3 * i - 1)],
                    texcoord[(2 * i - 1) - 1], texcoord[(2 * i - 1)]]

        arr = array(arr, dtype=float32)

        # only applies array to vbo if length of vertices is not zero
        if len(arr) > 0:
            self.mesh_api.rebind_VBO(self.VBO, self._vertices, vertices, arr)

        # Saves colors and vertices so you can access trough code
        self._vertices = vertices
        self._colors = colors
        self._texcoord = texcoord

    def bind_new_ebo(self, ebo):
        # saves ebo as compatible array
        ebo = array(ebo, dtype=uint32)

        self.mesh_api.rebind_EBO(self.EBO, self._triangles, ebo)

        # Saves triangles so you can access this trough code
        self._triangles = ebo
