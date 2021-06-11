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


class StageGenerator:
    SPECIAL_ROOMS_WAGE = 0.13
    HARD_ROOMS_WAGE = 0.25

    START = 0
    EASY_PATH_ROOMS_SKIP = 4

    def __init__(self):
        self.rooms = {}
        self.horizontal_length = 20
        self.horizontal_end = self.horizontal_length - 1
        self.vertical_length = 8
        self.vertical_end = self.vertical_length - 1
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

    def merge_easy_path_points(self, path_points):
        rooms = []
        starting_x, starting_y = self.rooms[STARTING].location
        exit_location = self.rooms[EXIT].location

        first_point_x, first_point_y = path_points[0]
        # print(starting_point)
        # print(exit_location)
        for x in range(1, self.EASY_PATH_ROOMS_SKIP):
            difference = abs(starting_y - first_point_y) / x
            # TODO HERE
            if starting_y >= first_point_y:
                print(x, difference)
        # for point in path_points:
        #     print(point)
        return rooms

    def insert_easy_path_rooms(self):
        rooms = []
        path_points = []
        start = self.START + 1
        end = self.horizontal_end
        for x in range(
            max(start, self.EASY_PATH_ROOMS_SKIP), end, self.EASY_PATH_ROOMS_SKIP
        ):
            path_points.append((x, rnd.randint(start, self.vertical_end)))
        for point in path_points:
            rooms.append(EasyPathRoom(*point))
        self.rooms[EASY_PATH] = rooms
        self.rooms[EASY_PATH].extend(self.merge_easy_path_points(path_points))

    # def append_vertical_path_rooms(self, previous_room_x, location):
    #     rooms = []
    #     for x in range(abs(previous_room_x - location[0])):
    #         if previous_room_x > location[0]:
    #             self.free_slots.remove((previous_room_x - x, location[1]))
    #             rooms.append(EasyPathRoom(previous_room_x - x, location[1]))
    #         else:
    #             self.free_slots.remove((previous_room_x + x, location[1]))
    #             rooms.append(EasyPathRoom(previous_room_x + x, location[1]))
    #     self.free_slots.remove(location)
    #     rooms.append(EasyPathRoom(*location))
    #     return rooms
    #
    # def generate_vertical_path(self, min_value):
    #     rooms = []
    #     previous_room, last_room = sorted(
    #         [self.rooms["STARTING"], self.rooms["EXIT"]],
    #         key=lambda obj: obj.face == UP,
    #         reverse=True,
    #     )
    #     previous_room_x = previous_room.x
    #     for x in range(min_value, self.END):
    #         if rooms:
    #             previous_room_x = rooms[-1].x
    #         location = (rnd.randint(1, self.END - 1), x - 1)
    #         rooms.extend(self.append_vertical_path_rooms(previous_room_x, location))
    #     rooms.extend(
    #         self.append_vertical_path_rooms(rooms[-1].x, (last_room.x, last_room.y - 1))
    #     )
    #     return rooms
    #
    # def generate_horizontal_path(self, min_value):
    #     rooms = []
    #     for x in range(min_value, int(self.END) + 1):
    #         rooms.append(EasyPathRoom(x - 1, rnd.randint(1, self.END - 1)))
    #     return rooms
    #
    # def insert_easy_path_rooms(self):
    #     min_value = 2
    #     starting_left_or_right = self.rooms["STARTING"].x in [0, 10]
    #     if starting_left_or_right:
    #         self.rooms[EASY_PATH] = self.generate_horizontal_path(min_value)
    #     else:
    #         self.rooms[EASY_PATH] = self.generate_vertical_path(min_value)

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

        self.rooms[STARTING] = self.generate_entrance(LEFT)
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
