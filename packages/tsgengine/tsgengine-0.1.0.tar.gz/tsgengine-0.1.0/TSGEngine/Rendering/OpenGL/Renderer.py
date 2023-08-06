import ctypes

from TSGEngine.World.Components import Transform
from TSGEngine.World.Components import Mesh
from OpenGL import GL


class Renderer:
    def __init__(self):
        pass

    @staticmethod
    def initialize():
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

    @staticmethod
    def clear_background():
        background_color = (0.2, 0.3, 0.3, 1.0)

        GL.glClearColor(*background_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    def draw_all_meshes(self, world):
        for entity, mesh in world.get_entities_with_component(Mesh.Mesh):
            self.draw_single_entity(entity, mesh, world)

    @staticmethod
    def draw_mesh_shader_array(array):
        for shader in array:
            shader.activate()

            for entity in array[shader]:
                transform = entity.components[Transform]
                mesh = entity.components[Mesh.Mesh]

                shader.set_uniform('transform', transform.matrix)

                GL.glBindVertexArray(mesh.mesh_api.VAO)

                # render elements in VAO
                GL.glDrawElements(mesh.mesh_api.triangles, len(mesh.triangles), GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

            shader.deactivate()

    @staticmethod
    def draw_single_entity(entity, mesh, world):
        if Mesh in entity.components:
            shader = world.shader_manager[mesh.shader_name]

            shader.activate()

            shader.set_uniform('transform', entity.get_component(Transform).matrix)

            GL.glBindVertexArray(mesh.VAO)

            # render elements in VAO
            GL.glDrawElements(mesh.primitive_type, mesh.num_points, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))
