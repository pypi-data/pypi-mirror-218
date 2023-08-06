from .BaseSystem import BaseSystem
from TSGEngine.Rendering import Renderer

# Component
from TSGEngine.World.Components import Mesh


class RenderSystem(BaseSystem):
    def __init__(self):
        self.renderer = Renderer()

        self.shader_mesh_list = {}

        # shader mesh list validation
        self._shaders_len = 0
        self._entity_len = 0

    def process(self, *args, **kwargs):
        # validation
        pass

        # draw
        self.renderer.clear_background()

        # for entity, component in self.world.get_entities_with_component(Mesh):
        #     self.renderer.draw_single_entity(entity, component, self.world)
        array = self._generate_mesh_entity_array()
        self.renderer.draw_mesh_shader_array(array)

    def _generate_mesh_entity_array(self):
        return_dict = {}

        for entity, component in self.world.get_entities_with_component(Mesh):
            program = self.world.shader_manager.shaders[component.shader_name]
            if program not in return_dict:
                return_dict[program] = [entity]
            else:
                return_dict[program] += [entity]

        return return_dict
