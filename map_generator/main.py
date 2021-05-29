from random import choice, randrange


class Map:
    SQUARE_SIZE = 11
    START = 0
    END = SQUARE_SIZE - 1

    COMPLEXITY = 1
    EXIT_ROOMS = 1

    ENTRANCE_ROOM_LOCATION = int(SQUARE_SIZE / 2)

    def randomize_exit_location(self):
        x_position = randrange(self.START, self.SQUARE_SIZE)
        if x_position in [self.START, self.END]:
            return [x_position, randrange(self.START, self.SQUARE_SIZE)]
        return [x_position, choice([self.START, self.END])]

    def create_map(self):
        aa = [["x"] * self.SQUARE_SIZE] * self.SQUARE_SIZE
        # Overwriting error
        return aa


mappp = Map()
print(mappp.create_map())
