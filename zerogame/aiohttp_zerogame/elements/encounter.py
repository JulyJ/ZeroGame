from random import randrange
from time import gmtime

from ..config import DEBUG_MODE
from ..game import Room
from .methods import add_user, kick_user, get_random_item, ws_message


class Encounter:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.price = 1000
        self.experience = randrange(10000, 30000, 1000)
        self.start_time = gmtime()
        self.length = randrange(60, 360, 10)
        self.name = None
        self.room = None

        if DEBUG_MODE:
            self.length = randrange(6, 36, 1)

    async def start_encounter(self, session):
        if session.user.points - self.price > 0:
            session.user.points -= self.price
            session.send(
                await ws_message(
                    'Encounter started. Price is {price}. Remaining {points}'.format(
                        price=self.price,
                        points=session.user.points
                    )
                )
            )
            self.name = (await get_random_item(self.db, 'encounters')).get('item')
            self.room = Room(self.app)
            await kick_user(session)
            await add_user(self.room, session)
            for room in self.app.rooms:
                await room.check_room()
        else:
            session.send(
                await ws_message(
                    "Encounter price is {price}, you have not enough points ({points})".format(
                        price=self.price,
                        points=session.user.points
                    )
                )
            )

    async def stop_encounter(self, session):
        session.user.experience += self.experience
        await session.user.write_user_data()
        await session.user.level_up_broadcast(
            self.room,
            session
        )
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
