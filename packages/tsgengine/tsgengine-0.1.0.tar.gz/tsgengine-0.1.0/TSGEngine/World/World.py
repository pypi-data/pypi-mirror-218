import time

from TSGEngine.World.Entity.Entity import Entity
from TSGEngine.Core.Scene import SceneManager
from TSGEngine.Shaders import ShaderHandler

# Base systems
from TSGEngine.World.Systems import RenderSystem
from TSGEngine.Physics.Systems.Collision import CollisionSystem

from types import MethodType


class World:
    def __init__(self):
        self.entities = {}
        self.systems = {}
        self.components = {}

        self.scene_manager = SceneManager()
        self.shader_manager = ShaderHandler()
        self.input_manager = None
        self.texture_handler = None

        self._events = {}

        self.next_entity_id = 0
        self.dt = 0
        self._fixed_dt_counter = 0
        self._min_fixed_dt = 0.02
        self._max_fixed_dt = 0.02

    def initialize(self):
        self.scene_manager.create_scene('Base_scene', True, True)

        self.add_system(RenderSystem())
        self.add_system(CollisionSystem())

    def past_window_initialize(self):
        self.get_system(RenderSystem).renderer.initialize()

    def add_system(self, system):
        system.world = self
        self.systems[type(system)] = system

    def get_system(self, system_class):
        return self.systems[system_class]

    def delete_system(self, system_class):
        self.systems[system_class].world = None
        del self.systems[system_class]

    def get_time(self, system_class):
        return self.systems[system_class].execution_time

    def get_times(self):
        return [self.systems[system].execution_time for system in self.systems]

    def create_entity(self, *components, add_to_scene: bool = True):
        entity = Entity()
        entity.id = self.next_entity_id
        entity.world = self
        entity.add_component(*components)

        self.entities[entity.id] = entity

        self.next_entity_id += 1

        if add_to_scene:
            self.scene_manager.scenes[self.scene_manager.selected_scene].append(entity)

        return entity

    def destroy_entity(self, entity):
        if type(entity) == int:
            self.entities[entity].destroy()
            return 0

        entity.destroy()

    def add_component(self, entity, *components):
        if type(entity) == int:
            self.entities[entity].add_component(*components)
            return

        entity.add_component(*components)

    def remove_component(self, entity, *components_classes):
        if type(entity) == int:
            self.entities[entity].remove_component(*components_classes)
            return

        entity.remove_component(*components_classes)

    def get_entities_with_component(self, component, all_entities=False):
        if all_entities or self.scene_manager is None:
            for entity in self.entities:
                if component in self.entities[entity].components:
                    yield self.entities[entity], self.entities[entity].components[component]
        else:
            for scene in self.scene_manager.active_scenes:
                for entity in self.scene_manager.scenes[scene]:
                    if component in self.entities[entity.id].components:
                        yield self.entities[entity.id], self.entities[entity.id].components[component]

    def set_scene_manager(self, scene_manager):
        self.scene_manager = scene_manager

    def add_event(self, name, event):
        pass

    def remove_event(self, name):
        pass

    def run_event(self, name):
        pass

    def step(self):
        for system in self.systems:
            # normal process
            start_time = time.perf_counter()
            self.systems[system].process(dt=self.dt)
            self.systems[system].execution_time = time.perf_counter() - start_time

            # fixed process
            self._fixed_dt_counter += self.dt

            if self._fixed_dt_counter > self._min_fixed_dt:
                fixed_dt = min([self._fixed_dt_counter, self._max_fixed_dt])
                fixed_start_time = time.perf_counter()

                self.systems[system].fixed_process(fixed_dt=fixed_dt)
                self.systems[system].fixed_execution_time = time.perf_counter() - fixed_start_time

        if self._fixed_dt_counter > self._min_fixed_dt:
            self._fixed_dt_counter = 0

    # TODO: event system bound to world
