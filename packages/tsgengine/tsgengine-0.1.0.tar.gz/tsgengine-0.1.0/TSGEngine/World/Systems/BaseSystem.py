class BaseSystem:
    priority = 0
    world = None
    execution_time = -1
    fixed_execution_time = -1

    def process(self, *args, **kwargs):
        pass

    def fixed_process(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self
