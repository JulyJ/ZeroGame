from os import listdir
from os.path import dirname, abspath, join

from aiofiles import open
from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:

    def __init__(self):
        self.client = AsyncIOMotorClient('mongodb://localhost:27017')
        self.db = self.client.zerogame

    async def update_names(self):
        self.filepath = join(dirname(dirname(abspath(__file__))), 'items')
        for filename in listdir(self.filepath):
            await self.update_items(filename)

    async def update_items(self, filename):
        """
        This function parses game process items (loot, event, etc) in line-separated text file and
        puts them into separate mongoDB collections.
        """
        file = join(self.filepath, filename)
        name, _, _ = filename.partition('.')
        async with open(file, mode='r') as f:
            async for line in f:
                line = line.rstrip('\n')
                self.db[name].update(
                    {'item': line},
                    {'item': line},
                    True
                )
        self.db.names.update(
            {'name': name},
            {'name': name},
            True
        )
