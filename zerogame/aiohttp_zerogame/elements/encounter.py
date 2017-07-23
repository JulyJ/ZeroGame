from random import randrange
from time import gmtime

from ..config import DEBUG_MODE
from ..game import Room
from .methods import add_user, kick_user


class Encounter:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.cost = randrange(100, 1000, 100)
        self.experience = randrange(10000, 30000, 1000)
        self.start_time = gmtime()
        self.length = randrange(60, 360, 10)
        self.name = None

        if DEBUG_MODE:
            self.length = randrange(6, 36, 1)

    async def start_encounter(self, session):
        enc_room = Room(self.app)
        await kick_user(session)
        await add_user(enc_room, session)
        for room in self.app['rooms']:
            await room.check_room()

    async def stop_encounter(self, session):
        await kick_user(session)


class Dungeon(Encounter):
    pass


class Battle(Encounter):
    pass


class Fishing(Encounter):
    pass


class Archeology(Encounter):
    pass


class Mining(Encounter):
    pass
