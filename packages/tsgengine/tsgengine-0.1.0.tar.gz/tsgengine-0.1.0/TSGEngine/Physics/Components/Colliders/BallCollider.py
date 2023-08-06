from TSGEngine.Physics.Components.Collider import Collider


class BallCollider(Collider):
    def __init__(self):
        super().__init__()
        self.radius = 0

    def initialize_bounding_box(self, vertices: list) -> None:
        pass
