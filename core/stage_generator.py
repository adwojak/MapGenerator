from random import choice, randint, randrange

from core.constants import (
    DOWN,
    EASY_PATH,
    EMPTY_SPACE,
    EXIT,
    LEFT,
    OPPOSITE_FACES,
    RIGHT,
    STARTING,
    UP,
)
from core.rooms import EasyPathRoom, ExitRoom, StartingRoom


class StageGenerator:
    SQUARE_SIZE = 11

    SPECIAL_ROOMS_WAGE = 0.13
    HARD_ROOMS_WAGE = 0.25

    TOTAL_ROOMS = (SQUARE_SIZE - 2) * (SQUARE_SIZE - 2)
    SPECIAL_ROOMS = int(SPECIAL_ROOMS_WAGE * TOTAL_ROOMS)
    HARD_ROOMS = int(HARD_ROOMS_WAGE * TOTAL_ROOMS)
    EASY_ROOMS = TOTAL_ROOMS - SPECIAL_ROOMS - HARD_ROOMS

    START = 0
    END = SQUARE_SIZE - 1

    generated_stage = None
    rooms = {}

    def __init__(self):
        self.generated_stage = [
            [EMPTY_SPACE] * self.SQUARE_SIZE for _ in range(self.SQUARE_SIZE)
        ]

    def is_easy_path_even(self):
        return abs(self.rooms[STARTING].x - self.rooms[EXIT].x) - 1 % 2 == 0

    def randomize_position_on_any_face(self):
        x_position = randint(self.START, self.END)
        if x_position in [self.START, self.END]:
            return [x_position, randrange(self.START + 1, self.END)]
        return [x_position, choice([self.START, self.END])]

    def randomize_position_on_face(self, face):
        single_coordinate = randint(self.START + 1, self.END - 1)
        return {
            DOWN: (single_coordinate, self.END),
            UP: (single_coordinate, 0),
            LEFT: (0, single_coordinate),
            RIGHT: (self.END, single_coordinate),
        }[face]

    def generate_entrance(self):
        starting_x, starting_y = self.randomize_position_on_any_face()
        return StartingRoom(
            starting_x, starting_y, self.get_face(starting_x, starting_y)
        )

    def generate_exit(self):
        starting_room_face = self.rooms[STARTING].face
        exit_room_face = OPPOSITE_FACES[starting_room_face]
        exit_x, exit_y = self.randomize_position_on_face(exit_room_face)
        return ExitRoom(exit_x, exit_y, exit_room_face)

    def insert_easy_path_rooms(self):
        self.rooms[EASY_PATH] = []
        min_value = 1
        starting_left_or_right = self.rooms["STARTING"].x in [0, 10]
        for x in range(min_value, int(self.END / 2) + min_value):
            if starting_left_or_right:
                self.rooms[EASY_PATH].append(
                    EasyPathRoom(2 * x - 1, randint(1, self.END - 1))
                )
            else:
                self.rooms[EASY_PATH].append(
                    EasyPathRoom(randint(1, self.END - 1), 2 * x - 1)
                )
        # Now need to add connections

    def get_face(self, x_position, y_position):
        if x_position == 0:
            return LEFT
        elif x_position == self.END:
            return RIGHT
        elif y_position == 0:
            return UP
        elif y_position == self.END:
            return DOWN

    def generate_rooms(self):
        self.rooms[STARTING] = self.generate_entrance()
        self.rooms[EXIT] = self.generate_exit()
        self.insert_easy_path_rooms()

    def insert_rooms_into_stage(self):
        for kind, room_or_group in self.rooms.items():
            if isinstance(room_or_group, list):
                for room in room_or_group:
                    self.generated_stage[room.y][room.x] = room.symbol
            else:
                self.generated_stage[room_or_group.y][
                    room_or_group.x
                ] = room_or_group.symbol

    def generate_stage(self):
        self.generate_rooms()
        self.insert_rooms_into_stage()
        return self.generated_stage
