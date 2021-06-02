from random import choice, randint, randrange

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
MIDDLE = "MIDDLE"

OPPOSITE_FACES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

STARTING = "STARTING"

ROOM_TYPES = {STARTING: "S"}


class Room:
    x_position = None
    y_position = None
    kind = None
    symbol = None
    face = None

    def __init__(self, x_position, y_position, kind, symbol, face=None):
        self.x_position = x_position
        self.y_position = y_position
        self.kind = kind
        self.symbol = symbol
        self.face = face or MIDDLE

    @property
    def location(self):
        return self.x_position, self.y_position


class StartingRoom(Room):
    room_type = STARTING
    symbol = ROOM_TYPES[room_type]

    def __init__(self, x_position, y_position, face):
        super().__init__(x_position, y_position, self.room_type, self.symbol, face)


class MapGenerator:
    SQUARE_SIZE = 11
    START = 0
    END = SQUARE_SIZE - 1

    COMPLEXITY = 1
    EXIT_ROOMS = 1

    generated_map = None
    rooms = {}

    def randomize_position_on_face(self):
        x_position = randint(self.START, self.END)
        if x_position in [self.START, self.END]:
            return [x_position, randrange(self.START + 1, self.END)]
        return [x_position, choice([self.START, self.END])]

    def generate_entrance(self):
        starting_x, starting_y = self.randomize_position_on_face()
        return StartingRoom(
            starting_x, starting_y, self.get_face(starting_x, starting_y)
        )

    def generate_empty_map(self):
        return [["."] * self.SQUARE_SIZE for _ in range(self.SQUARE_SIZE)]

    def generate_rooms(self):
        self.rooms[STARTING] = self.generate_entrance()

    def get_face(self, x_position, y_position):
        if x_position == 0:
            return LEFT
        elif x_position == self.END:
            return RIGHT
        elif y_position == 0:
            return UP
        elif y_position == self.END:
            return DOWN

    def insert_rooms_into_map(self):
        for room_type, room in self.rooms.items():
            self.generated_map[room.y_position][room.x_position] = room.symbol

    def generate_map(self):
        self.generated_map = self.generate_empty_map()
        self.generate_rooms()
        self.insert_rooms_into_map()
        return self.generated_map


map_generator = MapGenerator()
[print(x) for x in map_generator.generate_map()]
