from asyncio import sleep
from time import gmtime, strftime
from random import randrange
from uuid import uuid4

from .config import log


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


class Game:
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.running = True

    async def run_game(self):
        while self.running:
            for room in self.app['rooms']:
                for ws in room.members:
                    event = await self.get_event(ws)
                    try:
                        for member in room.members:
                            member.send(event)
                    except AttributeError as e:
                        log.debug('AttributeError: %s' % e)
                        self.app['websockets'].remove(ws)
                        log.debug('Session removed: %s' % ws.id)
                        continue
            await sleep(1)

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
        pass
