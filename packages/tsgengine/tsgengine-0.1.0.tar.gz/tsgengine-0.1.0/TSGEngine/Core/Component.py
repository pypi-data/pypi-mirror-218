class Components:
    def __init__(self):
        self.components = {}

    def add_component(self, name: str, uninitialized_component):
        self.components[name] = uninitialized_component
