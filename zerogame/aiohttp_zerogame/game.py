from datetime import datetime
import random


class Story:
    def __init__(self, db, **kwargs):
        self.collection = db.stories

    async def get_story(self):
        stories = self.collection.find()[random.randrange(self.collection.count())]
        return await stories.to_list(length=None)

    async def save(self, character, story, **kw):
        result = await self.collection.insert({
                                               'character': character,
                                               'story': story,
                                               'time': datetime.now()
                                               })
        return result
