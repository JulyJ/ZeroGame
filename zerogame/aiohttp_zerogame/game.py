class Story:

    def __init__(self, db, **kwargs):
        self.collection = db.stories

    async def get_story(self):
        stories = self.collection.find().sort([('time', 1)])
        return await stories.to_list(length=None)
