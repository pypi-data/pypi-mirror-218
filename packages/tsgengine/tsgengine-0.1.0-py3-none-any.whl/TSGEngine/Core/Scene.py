from TSGEngine.Logger import log


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scenes = []
        self.selected_scene = None

    @property
    def active_scenes_children(self):
        return [children for children in [self.scenes[current_scene] for current_scene in self.active_scenes]]

    def create_scene(self, name, activate=False, select=False):
        if name not in self.scenes:
            self.scenes[name] = []

            if activate:
                self.activate_scene(name)

            if select:
                self.select_scene(name)

            log(f"Created scene with name {name}, {'activated' if activate else 'not activated'}, "
                f"{'selected' if select else 'not selected'}", "Scene manager", 'Info')

            return self.scenes[name]

    def select_scene(self, name):
        if name in self.scenes:
            log(f'Selected scene {name}', "Scene manager")
            self.selected_scene = name

    def activate_scene(self, name):
        if name in self.scenes:
            log(f'Activated scene {name}', "Scene manager")
            self.active_scenes.append(name)

    def deactivate_scene(self, name):
        if name in self.scenes:
            log(f'Deactivated scene {name}', "Scene manager")
            self.active_scenes.remove(name)
