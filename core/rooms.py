from core.constants import EASY_PATH, EXIT, MIDDLE, ROOM_KINDS, STARTING


class Room:
    x = None
    y = None
    kind = None
    symbol = None
    face = None

    def __init__(self, x, y, face=None):
        self.x = x
        self.y = y
        self.symbol = ROOM_KINDS[self.kind]
        self.face = face or MIDDLE

    @property
    def location(self):
        return self.x, self.y


class StartingRoom(Room):
    kind = STARTING

    def __init__(self, x, y, face):
        super().__init__(x, y, face)


class ExitRoom(StartingRoom):
    kind = EXIT


class EasyPathRoom(Room):
    kind = EASY_PATH
