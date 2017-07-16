from time import gmtime, strftime


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
