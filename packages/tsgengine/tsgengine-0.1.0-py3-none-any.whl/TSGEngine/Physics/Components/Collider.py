class Collider:
    center: list[float, float, float]

    def __init__(self):
        self.center = [0, 0, 0]

        self.colliding = False
        self.collision_point = [0, 0, 0]
        self.colliding_entity = None
        self.collision_count = 0
