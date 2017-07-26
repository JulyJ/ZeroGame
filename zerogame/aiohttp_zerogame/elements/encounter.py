from asyncio import sleep
from random import randrange
from time import gmtime, mktime

from ..config import DEBUG_MODE
from ..game import EncounterRoom
from .methods import add_user, kick_user, get_random_item, ws_message


class Encounter:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.events = None
        self.experience = randrange(10, 100, 10)
        self.name = None
        self.price = 1000
        self.room = None
        self.running = False
        self.session = None
        self.start_time = gmtime()

        if DEBUG_MODE:
            self.length = randrange(6, 36, 1)

    async def get_event(self):
        return (await get_random_item(self.db, self.events)).get('item')

    async def run_encounter(self):
        self.session.send(
            await ws_message(
                await self.get_event()
            )
        )
        await sleep(randrange(20))

    async def start_encounter(self, session):
        self.session = session
        if session.user.points - self.price > 0:
            self.running = True
            session.user.points -= self.price
            session.send(
                await ws_message(
                    '{name} started. Price is {price}. Remaining {points}'.format(
                        name=self.name,
                        price=self.price,
                        points=session.user.points
                    )
                )
            )
            self.room = EncounterRoom(self.app)
            await self.room.append_room(encounter=True)
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
            session.send(
                await ws_message("Stop encounter when you will be ready to resume your journey.")
            )

    async def stop_encounter(self, session):
        if self.running:
            time = int(mktime(gmtime())) - int(mktime(self.start_time))
            experience = self.experience * time
            session.user.experience += experience
            await session.user.write_user_data()
            session.send(
                await ws_message(
                    "{enc} lasted {t} seconds. {n} received {e} experience".format(
                        enc=self.name,
                        t=time,
                        n=session.user.character_name,
                        e=experience
                    )
                )
            )
            await session.user.level_up_broadcast(
                self.room,
                session
            )
            self.running = False
        await kick_user(session)
        await self.room.delete_room(encounter=True)


class Archeology(Encounter):
    def __init__(self, app):
        super().__init__(app)
        self.events = 'archeology_events'
        self.name = 'Archeology'


class Battle(Encounter):
    def __init__(self, app):
        super().__init__(app)
        self.events = 'battle_events'
        self.name = 'Battle'


class Dungeon(Encounter):
    def __init__(self, app):
        super().__init__(app)
        self.events = 'dungeon_events'
        self.name = 'Dungeon'


class Fishing(Encounter):
    def __init__(self, app):
        super().__init__(app)
        self.events = 'fishing_events'
        self.name = 'Fishing'


class Mining(Encounter):
    def __init__(self, app):
        super().__init__(app)
        self.events = 'mining_events'
        self.name = 'Mining'
