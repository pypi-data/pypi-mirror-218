from TSGEngine.Physics.Components.Collider import Collider


class RectangleCollider(Collider):
    min: list[float, float, float]
    max: list[float, float, float]

    def __init__(self):
        super().__init__()
        self.max = [0, 0, 0]
        self.min = [0, 0, 0]

    def initialize_bounding_box(self, vertices: list) -> None:
        x_list = []
        y_list = []
        z_list = []

        for axis_point_id in range(0, len(vertices), 3):
            x_list.append(vertices[axis_point_id])
            y_list.append(vertices[axis_point_id + 1])
            z_list.append(vertices[axis_point_id + 2])

        self.min = [min(x_list), min(y_list), min(z_list)]
        self.max = [max(x_list), max(y_list), max(z_list)]

        self.center = [(self.min[0] + self.max[0]) / 2,
                       (self.min[1] + self.max[1]) / 2,
                       (self.min[2] + self.max[2]) / 2]
