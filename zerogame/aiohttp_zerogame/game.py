from asyncio import sleep
from datetime import datetime

from .user import User
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
    def __init__(self, app, handler, *args, **kwargs):
        self.app = app
        self.handler = handler

    async def get_event(self, ws_session, session):
        user = User(self.app.db, {'id': session.get('user')})
        story = Story(self.app.db, await user.get_character())
        event = await story.get_event()
        await sleep(10)
        return '[{character}] {event}'.format(
            character=self.character,
            event=event
        )


class Game:
    def __init__(self, app, handler, *args, **kwargs):
        self.app = app
        self.handler = handler

    async def run_game(self):
        while True:
            log.debug('game is running...')
            await sleep(10)
