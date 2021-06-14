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


class EasyPathRoom2(EasyPathRoom):
    kind = "EASY_PATH2"


class StageGenerator:
    SPECIAL_ROOMS_WAGE = 0.13
    HARD_ROOMS_WAGE = 0.25

    START = 0

    def __init__(self):
        self.rooms = {}
        self.horizontal_length = 8
        self.horizontal_end = self.horizontal_length - 1
        self.vertical_length = 20
        self.vertical_end = self.vertical_length - 1
        self.easy_path_points_count = 4
        self.total_rooms = (self.horizontal_length - 2) * (self.vertical_length - 2)
        self.special_rooms = int(self.SPECIAL_ROOMS_WAGE * self.total_rooms)
        self.hard_rooms = int(self.HARD_ROOMS_WAGE * self.total_rooms)
        self.easy_rooms = self.total_rooms = self.special_rooms - self.hard_rooms

        self.generated_stage = [
            [EMPTY_SPACE] * self.horizontal_length for _ in range(self.vertical_length)
        ]
        self.free_slots = [
            (x, y)
            for x in range(1, self.horizontal_length)
            for y in range(1, self.vertical_length)
        ]

    def randomize_position_on_face(self, face):
        end = self.horizontal_end if face in [UP, DOWN] else self.vertical_end
        single_coordinate = rnd.randint(self.START + 1, end - 1)
        return {
            DOWN: (single_coordinate, self.vertical_end),
            UP: (single_coordinate, 0),
            LEFT: (0, single_coordinate),
            RIGHT: (self.horizontal_end, single_coordinate),
        }[face]

    def _generate_entrance_location(self):
        x_position = rnd.randint(self.START, self.horizontal_end)
        if x_position in [self.START, self.horizontal_end]:
            return [x_position, rnd.randrange(self.START + 1, self.vertical_end)]
        return [x_position, rnd.choice([self.START, self.vertical_end])]

    def generate_entrance(self, face=None):
        if face:
            starting_x, starting_y = self.randomize_position_on_face(face)
        else:
            starting_x, starting_y = self._generate_entrance_location()
        return StartingRoom(
            starting_x, starting_y, self.get_face(starting_x, starting_y)
        )

    def generate_exit(self):
        starting_room_face = self.rooms[STARTING].face
        exit_room_face = OPPOSITE_FACES[starting_room_face]
        exit_x, exit_y = self.randomize_position_on_face(exit_room_face)
        return ExitRoom(exit_x, exit_y, exit_room_face)

    def append_basic_rooms(self, path_points):
        starting, exiting = self.rooms[STARTING].location, self.rooms[EXIT].location
        if self.rooms[STARTING].face == RIGHT:
            starting, exiting = exiting, starting
        path_points.insert(0, starting)
        path_points.append(exiting)
        return path_points

    # def merge_easy_path_points(self, path_points):
    #     rooms = []
    #     path_points = self.append_basic_rooms(path_points)
    #
    #     for point in range(len(path_points) - 1):
    #         rest, total_vertical_moves = 0, 0
    #         first_point_x, first_point_y = path_points[point]
    #         second_point_x, second_point_y = path_points[point + 1]
    #
    #         x_diff = abs(first_point_x - second_point_x) - 1
    #         y_diff = abs(first_point_y - second_point_y)
    #         points_difference = round(Decimal(y_diff) / Decimal(x_diff), 10)
    #
    #         for _ in range(x_diff):
    #             rest = round_value(rest + round(points_difference, 10))
    #             x_move = first_point_x + 1 + _
    #
    #             if rest >= 1:
    #                 vertical_moves = int(rest)
    #                 total_vertical_moves += vertical_moves
    #                 rest %= 1
    #
    #                 if first_point_y > second_point_y:
    #                     rooms.append(
    #                         (
    #                             x_move,
    #                             first_point_y - total_vertical_moves + vertical_moves,
    #                         )
    #                     )
    #                     for move in range(vertical_moves):
    #                         rooms.append(
    #                             (x_move, first_point_y - total_vertical_moves + move)
    #                         )
    #                 else:
    #                     rooms.append(
    #                         (
    #                             x_move,
    #                             first_point_y + total_vertical_moves - vertical_moves,
    #                         )
    #                     )
    #                     for move in range(vertical_moves):
    #                         rooms.append(
    #                             (x_move, first_point_y + total_vertical_moves - move)
    #                         )
    #             else:
    #                 if first_point_y > second_point_y:
    #                     rooms.append((x_move, first_point_y - total_vertical_moves))
    #                 else:
    #                     rooms.append((x_move, first_point_y + total_vertical_moves))
    #     return rooms

    def merge_easy_path_points(self, path_points):
        rooms = []
        path_points = self.append_basic_rooms(path_points)

        for point in range(len(path_points) - 1):
            rest, total_vertical_moves = 0, 0
            first_point_x, first_point_y = path_points[point]
            second_point_x, second_point_y = path_points[point + 1]

            x_diff = abs(first_point_x - second_point_x) - 1
            y_diff = abs(first_point_y - second_point_y)
            points_difference = round(Decimal(y_diff) / Decimal(x_diff), 10)

            for _ in range(x_diff):
                rest = round_value(rest + round(points_difference, 10))
                x_move = first_point_x + 1 + _

                if rest >= 1:
                    vertical_moves = int(rest)
                    total_vertical_moves += vertical_moves
                    rest %= 1

                    if first_point_y > second_point_y:
                        rooms.append(
                            (
                                x_move,
                                first_point_y - total_vertical_moves + vertical_moves,
                            )
                        )
                        for move in range(vertical_moves):
                            rooms.append(
                                (x_move, first_point_y - total_vertical_moves + move)
                            )
                    else:
                        rooms.append(
                            (
                                x_move,
                                first_point_y + total_vertical_moves - vertical_moves,
                            )
                        )
                        for move in range(vertical_moves):
                            rooms.append(
                                (x_move, first_point_y + total_vertical_moves - move)
                            )
                else:
                    if first_point_y > second_point_y:
                        rooms.append((x_move, first_point_y - total_vertical_moves))
                    else:
                        rooms.append((x_move, first_point_y + total_vertical_moves))
        return rooms

    def insert_easy_path_rooms(self):
        path_points = [
            (
                int((self.horizontal_length - 2) / self.easy_path_points_count) * x,
                rnd.randint(self.START + 1, self.vertical_end),
            )
            for x in range(1, self.easy_path_points_count)
        ]
        rooms = [EasyPathRoom(*point) for point in path_points]
        self.rooms[EASY_PATH] = rooms
        self.rooms[EASY_PATH].extend(
            [
                EasyPathRoom2(*location)
                for location in self.merge_easy_path_points(path_points)
            ]
        )

    def get_face(self, x_position, y_position):
        if x_position == 0:
            return LEFT
        elif x_position == self.horizontal_end:
            return RIGHT
        elif y_position == 0:
            return UP
        elif y_position == self.vertical_end:
            return DOWN

    def generate_rooms(self):
        # for x in range(100000):
        #     self.rooms[x] = self.generate_entrance()
        #     self.rooms[STARTING] = self.generate_entrance()
        #     self.rooms[x] = self.generate_exit()

        self.rooms[STARTING] = self.generate_entrance(UP)
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
