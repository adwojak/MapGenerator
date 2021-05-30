from random import choice, randrange

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"


class MapGenerator:
    SQUARE_SIZE = 11
    START = 0
    END = SQUARE_SIZE - 1

    COMPLEXITY = 1
    EXIT_ROOMS = 1

    ROOMS_CONTENT = ["S"]

    WALLS_TO_DISABLE = [LEFT, UP, RIGHT, DOWN]

    def get_randomize_location_method(self, room):
        return {"S": self.randomize_entrance_location([UP, DOWN])}[room]

    def randomize_entrance_location(self, disable_walls=None):
        if not disable_walls:
            disable_walls = []
        if len(disable_walls) > 3:
            raise Exception("Cannot generate such an entrance!")

        x_boundaries = (self.START, self.SQUARE_SIZE)
        y_boundaries = (self.START, self.SQUARE_SIZE)

        if "LEFT" in disable_walls:
            x_boundaries = (x_boundaries[0] + 1, x_boundaries[1])
        if "RIGHT" in disable_walls:
            x_boundaries = (x_boundaries[0], x_boundaries[1] - 1)
        if "UP" in disable_walls:
            y_boundaries = (y_boundaries[0] + 1, y_boundaries[1])
        if "DOWN" in disable_walls:
            y_boundaries = (y_boundaries[0], y_boundaries[1] - 1)

        # BUG

        x_min_boundary, x_max_boundary = x_boundaries
        y_min_boundary, y_max_boundary = y_boundaries

        x_position = randrange(x_min_boundary, x_max_boundary)
        if x_position in [self.START, self.END]:
            return [x_position, randrange(y_min_boundary, y_max_boundary)]
        return [x_position, choice([y_min_boundary, y_max_boundary])]

    def insert_room(self, generated_map, location, room_kind):
        x_position, y_position = location
        generated_map[x_position][y_position] = room_kind
        return generated_map

    def generate_empty_map(self):
        return [["."] * self.SQUARE_SIZE for _ in range(self.SQUARE_SIZE)]

    def generate_map(self):
        generated_map = self.generate_empty_map()
        for room in self.ROOMS_CONTENT:
            generated_map = self.insert_room(
                generated_map, self.get_randomize_location_method(room), room
            )
        return generated_map


map_generator = MapGenerator()
[print(x) for x in map_generator.generate_map()]
# aa = map_generator.ggg()
# print(aa)
