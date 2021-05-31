from random import choice, randrange

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"


class Room:
    x_position = None
    y_position = None
    kind = None

    def __init__(self, x_position, y_position, kind):
        self.x_position = x_position
        self.y_position = y_position
        self.kind = kind

    @property
    def location(self):
        return self.x_position, self.y_position


class MapGenerator:
    SQUARE_SIZE = 11
    START = 0
    END = SQUARE_SIZE - 1

    COMPLEXITY = 1
    EXIT_ROOMS = 1

    def randomize_entrance_location(self):
        x_position = randrange(self.START, self.SQUARE_SIZE)
        if x_position in [self.START, self.END]:
            return [x_position, randrange(self.START + 1, self.END)]
        return [x_position, choice([self.START, self.END])]

    def generate_empty_map(self):
        return [["."] * self.SQUARE_SIZE for _ in range(self.SQUARE_SIZE)]

    def generate_map(self):
        generated_map = self.generate_empty_map()
        starting_x, starting_y = self.randomize_entrance_location()
        starting_room = Room(starting_x, starting_y, "STARTING")
        generated_map[aa[0]][aa[1]] = "E"
        return generated_map


map_generator = MapGenerator()
[print(x) for x in map_generator.generate_map()]
