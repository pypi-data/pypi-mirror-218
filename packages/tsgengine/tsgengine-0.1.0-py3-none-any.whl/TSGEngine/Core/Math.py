import glm
import numpy

value_ptr = glm.value_ptr
_normalize = glm.normalize
dot = glm.dot

array = numpy.array
float32 = numpy.float32

vec2 = glm.vec2
vec3 = glm.vec3
vec4 = glm.vec4

mat4 = glm.mat4


def dot_vec3_list_by_matrix(vec, matrix):
    vec = matrix * vec4(vec[0], vec[1], vec[2], 1)

    return [vec[0], vec[1], vec[2]]


def normalize(*vec):
    if len(vec) == 3:
        vec = vec3(vec[0], vec[1], vec[2])
    if not (list(vec)[0] == 0 and list(vec)[1] == 0 and list(vec)[2] == 0):
        vec = _normalize(vec)
    return vec[0], vec[1], vec[2]


def flatten(input_list):
    return [item for sublist in input_list for item in sublist]


def flatten_vec3_list(input_list):
    return flatten([var for var in [[vec.x, vec.y, vec.z] for vec in input_list]])


def translate_matrix(matrix, vector):
    matrix = glm.translate(matrix, vector)
    return matrix


def rotate_matrix(matrix, angle, axis_vector):
    matrix = glm.rotate(matrix, angle, axis_vector)
    return matrix


def scale_matrix(matrix, scale_vector):
    matrix = glm.scale(matrix, scale_vector)
    return matrix
