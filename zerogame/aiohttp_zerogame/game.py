from asyncio import sleep
from datetime import datetime
from random import randrange

from .config import log

class Story:
    def __init__(self, db, character, **kwargs):
        self.collection = db.stories
        self.db = db
        self.character = character

    async def save(self, character, story, **kw):
        result = await self.collection.insert({
                                               'character': character,
                                               'story': story,
                                               'time': datetime.now()
                                               })
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


class Journey:
    def __init__(self, app):
        self.app = app

    async def get_event(self, ws):
        story = Story(self.app.db, character=ws.user.character_name)
        event = await story.get_event()
        await sleep(randrange(15))
        return '[{character}] {event}'.format(
            character=ws.user.character_name,
            event=event
        )


class Game:
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.running = True

    async def run_game(self):
        while self.running:
            for ws in self.app['websockets']:
                journey = Journey(self.app)
                try:
                    ws.manager.broadcast(await journey.get_event(ws))
                except AttributeError as e:
                    log.debug('AttributeError: %s' % e)
                    self.app['websockets'].remove(ws)
                    log.debug('Session removed: %s' %ws.id)
                    continue
            await sleep(1)

    def close(self):
        pass
