from asyncio import sleep
from time import gmtime, strftime, mktime
from random import randrange
from uuid import uuid4

from .config import log
from .methods import room_broadcast


class Game:
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.running = True

    async def run_game(self):
        while self.running:
            for room in self.app['rooms']:
                await self.send_events(room)
                await self.check_quest(self.app, room)
            await sleep(1)

    async def send_events(self, room):
        for ws in room.members:
            event = await self.get_event(ws)
            await room_broadcast(room, event)

    async def get_event(self, ws):
        story = Story(self.app.db, character=ws.user.character_name)
        event = await story.get_event()
        await sleep(randrange(15))
        return '[{time}] [{character}] {event}'.format(
            character=ws.user.character_name,
            event=event,
            time=strftime("%H:%M:%S", gmtime())
        )

    async def check_quest(self, app, room):  # TODO check if current quest is valid or start new
        quest = Quest(app, room)
        await quest.run_quest()

    def close(self):
        self.running = False


class Story:
    def __init__(self, db, character, **kwargs):
        self.collection = db.stories
        self.db = db
        self.character = character

    async def save(self, character, story, **kw):
        result = await self.collection.insert(
            {
                'character': character,
                'story': story,
                'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())
            }
        )
        return result

    async def get_random_item(self, name):
        pipeline = [{'$sample': {'size': 1}}]
        async for doc in self.db[name].aggregate(pipeline):
            return doc

    async def get_event(self):
        items = {}
        names = await self.get_names()

        for name in names:
            item = await self.get_random_item(name)
            items[name] = item.get('item')
        items['character'] = self.character

        return items['events'].format_map(items)

    async def get_names(self):
        names = []
        async for doc in self.db.names.find({}):
            names.append(doc.get('name'))
        return names


class Room:
    def __init__(self, app):
        self.uuid = uuid4()
        self.capacity = 4
        self.available = True
        self.members = []
        self.app = app

    async def append_room(self):
        self.app['rooms'].append(self)
        log.debug('Room {} created'.format(self.uuid))

    async def delete_room(self):
        self.app['rooms'].remove(self)
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


class Quest:
    def __init__(self, app, room):
        self.room = room
        self.app = app
        self.db = app.db
        self.running = True
        self.reward = randrange(1000, 10000, 100)
        self.length = randrange(6000, 36000, 1000)
        self.start_time = gmtime()
        self.name = None

    async def get_quest_name(self):
        async for quest in self.db['quests'].aggregate([{'$sample': {'size': 1}}]):
            self.name = quest.get('item')

    async def check_quest_status(self):
        if mktime(gmtime()) - self.length >= mktime(self.start_time):
            await self.quest_completed()

    async def quest_completed(self):
        await room_broadcast(self.room, 'Quest {n} completed! Reward is {r} points.'.format(
            n=self.name,
            r=self.reward
        ))

    async def run_quest(self):
        await self.get_quest_name()
        while self.running:
            await self.check_quest_status()
            await sleep(100)

    def close(self):
        self.running = False
