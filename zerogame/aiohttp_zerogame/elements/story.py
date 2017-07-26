from time import gmtime, strftime

from .methods import get_random_item


class Story:
    def __init__(self, db, character):
        self.character = character
        self.collection = db.stories
        self.db = db

    async def save(self, character, story):
        result = await self.collection.insert(
            {
                'character': character,
                'story': story,
                'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())
            }
        )
        return result

    async def get_event(self):
        items = {}
        names = await self.get_names()

        for name in names:
            item = await get_random_item(self.db, name)
            items[name] = item.get('item')
        items['character'] = self.character

        return items['events'].format_map(items)

    async def get_names(self):
        names = []
        async for doc in self.db.names.find({}):
            names.append(doc.get('name'))

        return names
