from TSGEngine.Rendering import Shader
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

fallback_shader = [
    ['''
    #version 330\n

    out vec4 outputColour;\n
    
    void main()\n
    {\n\t
        outputColour = vec4(0.0, 0.0, 0.0, 0.0);\n
    }''', GL_FRAGMENT_SHADER],
    ['''
    #version 330\n
    
    layout (location=0) in vec3 position;\n
    
    void main()\n
    {\n\t
        gl_Position = vec4(position.x, position.y, position.z, 1.0);\n
    }''', GL_VERTEX_SHADER]
]


class ShaderHandler:
    def __init__(self):
        self.shaders = {}
        self.fallback_shader = None

    def initialize(self):
        self._add_fallback_shader()

    def add_shader(self, name: str, *files):
        self.shaders[name] = Shader(*files, fallback_shader=self.fallback_shader)

    def _add_fallback_shader(self):
        shader = Shader(*fallback_shader, auto_compile=False)
        self.fallback_shader = shader.initialize()
