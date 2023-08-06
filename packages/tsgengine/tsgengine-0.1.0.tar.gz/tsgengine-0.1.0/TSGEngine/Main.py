from TSGEngine.World import World
from TSGEngine.Window import GLFWWindowHandler
from TSGEngine.Input import InputHandler

import time


class Main:
    def __init__(self):
        self.window = GLFWWindowHandler()
        self.settings = None
        self.logger = None

        # world and handler
        self.world = World()
        self.input_handler = InputHandler()

    def initialize(self):
        self.window.initialize()
        self.world.initialize()

    def past_window_initialize(self):
        self.world.shader_manager.initialize()
        self.window.set_callback('key', self.input_handler.input_callback)
        self.world.input_manager = self.input_handler
        self.world.past_window_initialize()

    def loop(self, gui_func=None):
        while not self.window.should_close():
            self.step(gui_func)

    def step(self, inserted_func=None):
        start_time = time.perf_counter()

        self.window.pool_events()

        self.world.step()

        if inserted_func:
            inserted_func()

        self.window.swap_buffers()

        self.world.dt = time.perf_counter() - start_time

        # print(1 / self.world.dt)  # print fps

# TODO: unsure about funcs? Do it in the main class
