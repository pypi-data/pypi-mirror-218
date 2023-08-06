import pathlib

from OpenGL.GL import shaders
from OpenGL import GL

from TSGEngine.Core.Math import value_ptr, mat4


class Shader:
    def __init__(self, *files, fallback_shader=None, auto_compile=True):
        self.files = list(files)

        if not issubclass(type(fallback_shader), shaders.ShaderProgram) and fallback_shader is not None:
            self.files.append(fallback_shader)
            fallback_shader = None

        self._source_codes = []
        self._shaders = []
        self._program = None
        self.fallback_shader = fallback_shader

        self._source_error = False
        self._shader_error = False
        self._program_error = False

        self.shaders_compiled = False
        self.program_compiled = False

        self.initialized = False

        self.activated = False

        if auto_compile:
            self.initialize()

    def initialize(self):
        if self.fallback_shader:
            self._initialize_files()
        else:
            self._source_codes = self.files

        self._compile_shaders()
        self._compile_program()
        self.initialized = True

        if not self.fallback_shader:
            return self._program

    def activate(self):
        GL.glUseProgram(self._program)
        self.activated = True

    def deactivate(self):
        GL.glUseProgram(0)
        self.activated = False

    def set_uniform(self, name, value):
        if not self.activated:
            self.activate()

        location = GL.glGetUniformLocation(self._program, name)
        if location == -1:
            return

        if type(value) == float:
            GL.glUniform1f(location, value)
        elif type(value) == int:
            GL.glUniform1i(location, value)
        elif type(value) == bool:
            GL.glUniform1i(location, int(value))
        elif type(value) == mat4:
            GL.glUniformMatrix4fv(location, 1, False, value_ptr(value))

        # self.deactivate()

    def _initialize_files(self):
        self._check_files()

        for file in self.files:
            file = pathlib.Path(file).absolute()
            self._source_codes.append([file.open('r').read(), file.suffix])

        for index in range(len(self._source_codes)):
            if self._source_codes[index][1] == '.vert':
                self._source_codes[index][1] = GL.GL_VERTEX_SHADER
            elif self._source_codes[index][1] == '.tesc':
                self._source_codes[index][1] = GL.GL_TESS_CONTROL_SHADER
            elif self._source_codes[index][1] == '.tese':
                self._source_codes[index][1] = GL.GL_TESS_EVALUATION_SHADER
            elif self._source_codes[index][1] == '.geom':
                self._source_codes[index][1] = GL.GL_GEOMETRY_SHADER
            elif self._source_codes[index][1] == '.frag':
                self._source_codes[index][1] = GL.GL_FRAGMENT_SHADER
            elif self._source_codes[index][1] == '.comp':
                self._source_codes[index][1] = GL.GL_COMPUTE_SHADER
            else:
                self._source_error = True

    def _compile_shaders(self):
        if self._source_error:
            self._shader_error = True
            return

        try:
            for source in self._source_codes:
                self._shaders.append(shaders.compileShader(*source))
            self.shaders_compiled = True
        except RuntimeError as exception:
            self._shader_error = True

    def _compile_program(self):
        if (not self.program_compiled and not self._shader_error) or \
           (self.program_compiled and self._program_error and not self._shader_error):
            self._program = shaders.compileProgram(*self._shaders)
            self._program_error = False
        else:
            self._program = self.fallback_shader
            self._program_error = True

        self.program_compiled = True

    def _check_files(self):
        if len(self.files) == 0:
            self._source_error = True
            return

        for file in self.files:
            if not pathlib.Path(file).absolute().exists():
                self._source_error = True
                return

        if len(self.files) == 1 and (directory := pathlib.Path(self.files[0]).absolute()).is_dir():
            self.files = [file for file in directory.glob('*.*')]
