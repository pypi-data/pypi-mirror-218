from ctypes import c_void_p
from OpenGL import GL


class Mesh:
    def __init__(self):
        self.triangles = GL.GL_TRIANGLES
        self.texture_ids = [GL.GL_TEXTURE0, GL.GL_TEXTURE1, GL.GL_TEXTURE2, GL.GL_TEXTURE3, GL.GL_TEXTURE4]

        # buffers
        self.VAO, self.VBO, self.EBO = self.generate_buffers()

    def generate_buffers(self):
        # Creates buffers
        VAO = GL.glGenVertexArrays(1)
        VBO = GL.glGenBuffers(1)
        EBO = GL.glGenBuffers(1)

        # Binds all arrays
        GL.glBindVertexArray(VAO)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)

        # pointer to vertices
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 32,
                                 c_void_p(0))
        GL.glEnableVertexAttribArray(0)

        # pointer to colors
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 32,
                                 c_void_p(12))
        GL.glEnableVertexAttribArray(1)

        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, 32,
                                 c_void_p(24))
        GL.glEnableVertexAttribArray(2)

        # unbind because we don't draw right now
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

        return VAO, VBO, EBO

    def rebind_VBO(self, VBO, _vertices, vertices, arr):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)

        # If buffer size don't changed it just rewrites data
        if len(_vertices) == len(vertices):
            GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, arr.nbytes, arr)
        # Else it just allocates new data
        else:
            GL.glBufferData(GL.GL_ARRAY_BUFFER, arr.nbytes, arr, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def rebind_EBO(self, EBO, _triangles, ebo):
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)

        # Same as vbo checker
        if len(_triangles) == len(ebo):
            GL.glBufferSubData(GL.GL_ELEMENT_ARRAY_BUFFER, 0, ebo.nbytes, ebo)
        else:
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, ebo.nbytes, ebo, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)