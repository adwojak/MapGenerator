from decimal import Decimal

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
from core.rnd import rnd
from core.rooms import EasyPathRoom, ExitRoom, StartingRoom
from core.utils import round_value

ALL_FACES = [LEFT, RIGHT, UP, DOWN]


class EasyPathRoom2(EasyPathRoom):
    kind = "EASY_PATH2"


class StageGenerator:
    def __init__(
        self,
        vertical_length=None,
        horizontal_length=None,
        entrance_face=None,
        exit_face=None,
    ):
        self.vertical_length = vertical_length or rnd.randint(8, 30)
        self.horizontal_length = horizontal_length or rnd.randint(
            8 + self.vertical_length, 30 + self.vertical_length
        )
        self.entrance_face = entrance_face or self.generate_entrance_face(exit_face)
        self.exit_face = exit_face or self.generate_exit_face()

        self.rooms = {}
        self.generated_stage = [
            [EMPTY_SPACE] * self.horizontal_length for _ in range(self.vertical_length)
        ]

        self.horizontal_end = self.horizontal_length - 1
        self.vertical_end = self.vertical_length - 1
        self.START = 0

    def generate_path(self):
        # get most left room
        left_room = self.rooms[EXIT]
        right_room = self.rooms[STARTING]

        self.rooms[EASY_PATH] = []
        # point under Exit
        self.rooms[EASY_PATH].append(EasyPathRoom(left_room.x, left_room.y + 1))

        # point left to Start
        self.rooms[EASY_PATH].append(EasyPathRoom(right_room.x - 1, right_room.y))

        print(
            f"x diff with abs: {left_room.x} - {right_room.x - 1} = {abs(left_room.x - (right_room.x - 1))}"
        )
        print(
            f"y diff with abs: {left_room.y + 1} - {right_room.y} = {abs(left_room.y + 1 - right_room.y)}"
        )
        # TODO here to create paths

    def generate_entrance_face(self, exit_face):
        all_faces = ALL_FACES.copy()
        if exit_face:
            all_faces.remove(exit_face)
        return rnd.choice(all_faces)

    def generate_exit_face(self):
        all_faces = ALL_FACES.copy()
        all_faces.remove(self.entrance_face)
        return rnd.choice(all_faces)

    def randomize_position_on_face(self, face):
        end = self.horizontal_end if face in [UP, DOWN] else self.vertical_end
        single_coordinate = rnd.randint(self.START + 1, end - 1)
        return {
            DOWN: (single_coordinate, self.vertical_end),
            UP: (single_coordinate, 0),
            LEFT: (0, single_coordinate),
            RIGHT: (self.horizontal_end, single_coordinate),
        }[face]

    def generate_face_room(self, room_kind, room_face):
        position_x, position_y = self.randomize_position_on_face(room_face)
        return {STARTING: StartingRoom, EXIT: ExitRoom}[room_kind](
            position_x, position_y, room_face
        )

    def generate_rooms(self):
        # self.rooms[STARTING] = self.generate_face_room(STARTING, self.entrance_face)
        # self.rooms[EXIT] = self.generate_face_room(EXIT, self.exit_face)
        self.rooms[STARTING] = {STARTING: StartingRoom, EXIT: ExitRoom}[STARTING](
            17, 4, self.entrance_face
        )
        self.rooms[EXIT] = {STARTING: StartingRoom, EXIT: ExitRoom}[EXIT](
            10, 0, self.exit_face
        )
        self.generate_path()

    def insert_rooms_into_stage(self):
        for kind, room_or_group in self.rooms.items():
            if isinstance(room_or_group, list):
                for room in room_or_group:
                    self.generated_stage[room.y][room.x] = room
            else:
                self.generated_stage[room_or_group.y][room_or_group.x] = room_or_group

    def generate_stage(self):
        # for x in range(111111):
        #     self.generate_rooms()
        #     self.insert_rooms_into_stage()
        self.generate_rooms()
        self.insert_rooms_into_stage()
        return self.generated_stage
