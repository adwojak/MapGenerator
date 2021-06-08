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
    free_slots = None
    rooms = {}

    def __init__(self):
        self.generated_stage = [
            [EMPTY_SPACE] * self.SQUARE_SIZE for _ in range(self.SQUARE_SIZE)
        ]
        self.free_slots = [
            (x, y) for x in range(1, self.END) for y in range(1, self.END)
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

    def append_vertical_path_rooms(self, previous_room_x, location):
        rooms = []
        for x in range(abs(previous_room_x - location[0])):
            if previous_room_x > location[0]:
                self.free_slots.remove((previous_room_x - x, location[1]))
                rooms.append(EasyPathRoom(previous_room_x - x, location[1]))
            else:
                self.free_slots.remove((previous_room_x + x, location[1]))
                rooms.append(EasyPathRoom(previous_room_x + x, location[1]))
        self.free_slots.remove(location)
        rooms.append(EasyPathRoom(*location))
        return rooms

    def generate_vertical_path(self, min_value):
        rooms = []
        previous_room, last_room = sorted(
            [self.rooms["STARTING"], self.rooms["EXIT"]],
            key=lambda obj: obj.face == UP,
            reverse=True,
        )
        previous_room_x = previous_room.x
        for x in range(min_value, self.END):
            if rooms:
                previous_room_x = rooms[-1].x
            location = (randint(1, self.END - 1), x - 1)
            rooms.extend(self.append_vertical_path_rooms(previous_room_x, location))
        rooms.extend(
            self.append_vertical_path_rooms(rooms[-1].x, (last_room.x, last_room.y - 1))
        )
        return rooms

    def generate_horizontal_path(self, min_value):
        rooms = []
        for x in range(min_value, int(self.END) + 1):
            rooms.append(EasyPathRoom(x - 1, randint(1, self.END - 1)))
        return rooms

    def insert_easy_path_rooms(self):
        min_value = 2
        starting_left_or_right = self.rooms["STARTING"].x in [0, 10]
        if starting_left_or_right:
            self.rooms[EASY_PATH] = self.generate_horizontal_path(min_value)
        else:
            self.rooms[EASY_PATH] = self.generate_vertical_path(min_value)

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
                    self.generated_stage[room.y][room.x] = room
            else:
                self.generated_stage[room_or_group.y][room_or_group.x] = room_or_group

    def generate_stage(self):
        self.generate_rooms()
        self.insert_rooms_into_stage()
        return self.generated_stage
