from TSGEngine.World.Systems.BaseSystem import BaseSystem
# All colliders import
from TSGEngine.Physics.Components.Colliders.RectangleCollider import RectangleCollider
from TSGEngine.Physics.Components.Colliders.BallCollider import BallCollider
from TSGEngine.Core.Math import dot_vec3_list_by_matrix


class CollisionSystem(BaseSystem):
    def process(self, *args, **kwargs):
        # TODO: multiple collisions
        rectangle_collider_entities = []

        for entity, component in self.world.get_entities_with_component(RectangleCollider):
            matrix = entity.transform.matrix
            applied_minmaxes = [dot_vec3_list_by_matrix(component.min, matrix),
                                dot_vec3_list_by_matrix(component.max, matrix)]
            rectangle_collider_entities.append([entity, component, applied_minmaxes])

        # Rectangle detection
        for first_entity_id in range(len(rectangle_collider_entities)):
            first_entity = rectangle_collider_entities[first_entity_id]

            first_min = first_entity[2][0]
            first_max = first_entity[2][1]

            for second_entity_id in range(first_entity_id + 1, len(rectangle_collider_entities)):
                second_entity = rectangle_collider_entities[second_entity_id]

                second_min = second_entity[2][0]
                second_max = second_entity[2][1]

                if (first_min[0] <= second_max[0] and
                        first_max[0] >= second_min[0] and
                        first_min[1] <= second_max[1] and
                        first_max[1] >= second_min[1] and
                        first_min[2] <= second_max[2] and
                        first_max[2] >= second_min[2]):

                    first_entity[1].collision_count += 1
                    second_entity[1].collision_count += 1

                    first_entity[1].colliding = True
                    first_entity[1].colliding_entity = second_entity[0]

                    second_entity[1].colliding = True
                    second_entity[1].colliding_entity = first_entity[0]

                    # detecting collision point
                    overlapX = max(0, min(first_max[0], second_max[0]) - max(first_min[0], second_min[0]))
                    overlapY = max(0, min(first_max[1], second_max[1]) - max(first_min[1], second_min[1]))
                    overlapZ = max(0, min(first_max[2], second_max[2]) - max(first_min[2], second_min[2]))

                    smallestOverlap = min(overlapX, overlapY, overlapZ)

                    closestIntersectionX = max(first_min[0], second_min[0]) + smallestOverlap / 2
                    closestIntersectionY = max(first_min[1], second_min[1]) + smallestOverlap / 2
                    closestIntersectionZ = max(first_min[2], second_min[2]) + smallestOverlap / 2

                    collision_point = [closestIntersectionX, closestIntersectionY, closestIntersectionZ]

                    first_entity[1].collision_point = collision_point.copy()
                    second_entity[1].collision_point = collision_point.copy()

            if first_entity[1].collision_count <= 0:
                first_entity[1].colliding = False
                first_entity[1].colliding_entity = None
                first_entity[1].collision_point = [0, 0, 0]
            else:
                first_entity[1].collision_count = 0

# TODO: fixed dt
