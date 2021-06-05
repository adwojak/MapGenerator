from core.constants import EXIT, MIDDLE, ROOM_KINDS, STARTING


class Room:
    x_position = None
    y_position = None
    kind = None
    symbol = None
    face = None

    def __init__(self, x_position, y_position, face=None):
        self.x_position = x_position
        self.y_position = y_position
        self.symbol = ROOM_KINDS[self.kind]
        self.face = face or MIDDLE

    @property
    def location(self):
        return self.x_position, self.y_position


class StartingRoom(Room):
    kind = STARTING

    def __init__(self, x_position, y_position, face):
        super().__init__(x_position, y_position, face)


class ExitRoom(StartingRoom):
    kind = EXIT
