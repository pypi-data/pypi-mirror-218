from TSGEngine.Utility import DestructibleClass
from TSGEngine.World.Components import Transform


class Entity(DestructibleClass):
    id: int
    world = None

    def __init__(self):
        self.components = {}

        self.transform = Transform()
        self.add_component(self.transform)

    def add_component(self, *components):
        try:
            components = components[0].get_components()
        except AttributeError:
            pass
        finally:
            for component in components:
                self.components[type(component)] = component
            for component in components:
                if isinstance(component, Transform):
                    self.transform = component
                    break

    def remove_component(self, *components_classes):
        for component_class in components_classes:
            del self.components[component_class]

    def destroy(self):
        del self.world.entities[self.id]
        del self.world
        super().destroy()
