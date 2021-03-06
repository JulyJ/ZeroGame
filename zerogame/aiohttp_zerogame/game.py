from asyncio import sleep
from random import randrange
from time import gmtime, strftime
from uuid import uuid4

from .config import log
from .elements.methods import room_broadcast
from .elements.story import Story
from .elements.quest import Quest


class Game:
    def __init__(self, app):
        self.app = app
        self.quest = None
        self.running = True

    @staticmethod
    async def iterator(items):
        for i in items:
            yield i
            await sleep(0.5)

    async def run_game(self):
        while self.running:
            async for room in self.iterator(self.app.rooms):
                await self.send_events(room)
                await self.check_quest(self.app, room)
            async for room in self.iterator(self.app.encounters):
                await self.check_encounter(room)
            await sleep(0.5)

    async def send_events(self, room):
        async for ws in self.iterator(room.members):
            event = await self.get_event(ws)
            await room_broadcast(room, event)

    async def check_encounter(self, room):
        async for member in self.iterator(room.members):
            if member.encounter.running:
                await member.encounter.run_encounter()

    async def get_event(self, ws):
        story = Story(self.app.db, character=ws.user.character_name)
        event = await story.get_event()
        await sleep(randrange(20))
        return '[{time}] [{character}] {event}'.format(
            character=ws.user.character_name,
            event=event,
            time=strftime("%H:%M:%S", gmtime())
        )

    async def start_quest(self, app, room):
        self.quest = Quest(app, room)
        self.quest.name = await self.quest.get_quest_name()

    async def check_quest(self, app, room):
        if not room.quest:
            await self.start_quest(app, room)
        else:
            await self.quest.run_quest()

    def close(self):
        self.running = False


class Room:
    def __init__(self, app):
        self.app = app
        self.available = True
        self.capacity = 4
        self.members = []
        self.quest = None
        self.uuid = uuid4()

    async def append_room(self, encounter=False):
        if not encounter:
            self.app.rooms.append(self)
        else:
            self.app.encounters.append(self)
        log.debug('Room {} created'.format(self.uuid))

    async def delete_room(self, encounter=False):
        if not encounter:
            self.app.rooms.remove(self)
        else:
            self.app.encounters.remove(self)
        log.debug('Room {} deleted'.format(self.uuid))

    async def check_room(self):
        if len(self.members) >= 4:
            self.available = False
            log.debug('Room {} is full.'.format(self.uuid))
        elif len(self.members) == 0:
            await self.delete_room()
        else:
            self.available = True
            log.debug('Room {} is available.'.format(self.uuid))


class EncounterRoom(Room):
    def __init__(self, app):
        super().__init__(app)
        self.capacity = 1
