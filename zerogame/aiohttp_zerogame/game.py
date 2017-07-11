from asyncio import sleep
from time import gmtime, strftime
from random import randrange
from uuid import uuid4

from .config import log


async def room_broadcast(room, event):
    for member in room.members:
        member.send(event)

class Game:
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.running = True

    async def run_game(self):
        while self.running:
            for room in self.app['rooms']:
                await self.send_events(room)
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
        self.quest = False

    async def append_room(self):
        self.app['rooms'].append(self)
        log.debug('Room {} created'.format(self.uuid))
        await self.start_quest()

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

    async def start_quest(self):
        if self.quest == False:
            quest = Quest(self.app.db)
            self.quest_name = await quest.get_quest()
            log.debug('Quest "{}" started.'.format(self.quest_name))
            self.quest = True


class Quest:
    def __init__(self, db):
        self.db = db
        self.reward = randrange(1000, 10000, 100)
        self.length = randrange(600, 3600, 100)
        self.start_time = gmtime()
        self.completed = False

    async def get_quest(self):
        async for quest in self.db['quests'].aggregate([{'$sample': {'size': 1}}]):
            return quest.get('item')

    async def check_quest_status(self):
        if gmtime()+gmtime(self.length) >= self.start_time:
            self.completed = True

    async def run_quest(self):
        while not self.completed:
            self.check_quest_status()
            # await sleep(100)
