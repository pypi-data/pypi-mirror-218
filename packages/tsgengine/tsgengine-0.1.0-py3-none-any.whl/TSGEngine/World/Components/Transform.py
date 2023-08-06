from dataclasses import dataclass
from TSGEngine.Core.Math import vec3, mat4, scale_matrix, translate_matrix


@dataclass
class Transform:
    position: vec3
    rotation: vec3
    scale: vec3

    def __init__(self):
        self._position = vec3(0, 0, 0)
        self._rotation = vec3(0, 0, 0)
        self._scale = vec3(1, 1, 1)
        self._matrix: mat4 = mat4(1)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, vector):
        if isinstance(vector, vec3):
            self._position = vector
        else:
            self._position = vec3(vector[0], vector[1], vector[2])

        self._apply_matrix()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, vector):
        if isinstance(vector, vec3):
            self._rotation = vector
        else:
            self._rotation = vec3(vector[0], vector[1], vector[2])

        self._apply_matrix()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, vector):
        if isinstance(vector, vec3):
            self._scale = vector
        else:
            self._scale = vec3(vector[0], vector[1], vector[2])

        self._apply_matrix()

    @property
    def matrix(self):
        return self._matrix

    def rotate(self, x_rotation=0, y_rotation=0, z_rotation=0):
        pass

    def scale_obj(self, x_scale=1, y_scale=1, z_scale=1):
        self.scale *= vec3(x_scale, y_scale, z_scale)
        self._apply_matrix()

    def translate(self, x_translation=0, y_translation=0, z_translation=0):
        vector = vec3(x_translation, y_translation, z_translation)
        self.position += vector
        self._apply_matrix()

    def _apply_matrix(self):
        matrix = mat4(1)

        self._matrix = translate_matrix(matrix, self.position)

        self._matrix = scale_matrix(self._matrix, self.scale)
