from random import choice, randrange


class MapGenerator:
    SQUARE_SIZE = 11
    START = 0
    END = SQUARE_SIZE - 1

    COMPLEXITY = 1
    EXIT_ROOMS = 1

    ROOMS_CONTENT = ["S"]

    def get_randomize_location_method(self, room):
        return {"S": self.randomize_entrance_location()}[room]

    def randomize_entrance_location(self):
        x_position = randrange(self.START, self.SQUARE_SIZE)
        if x_position in [self.START, self.END]:
            return [x_position, randrange(self.START, self.SQUARE_SIZE)]
        return [x_position, choice([self.START, self.END])]

    def insert_room(self, generated_map, location, room_kind):
        x_position, y_position = location
        generated_map[x_position][y_position] = room_kind
        return generated_map

    def generate_empty_map(self):
        return [["x"] * self.SQUARE_SIZE for _ in range(self.SQUARE_SIZE)]

    def generate_map(self):
        generated_map = self.generate_empty_map()
        for room in self.ROOMS_CONTENT:
            generated_map = self.insert_room(
                generated_map, self.get_randomize_location_method(room), room
            )
        return generated_map


map_generator = MapGenerator()
[print(x) for x in map_generator.generate_map()]
