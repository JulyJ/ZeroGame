from os import listdir, path as os_path

from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:

    def __init__(self):
        self.client = AsyncIOMotorClient('mongodb://localhost:27017')
        self.db = self.client.zerogame

        self.filepath = os_path.abspath(__file__) + '/../../' + '/items/'
        for filename in listdir(self.filepath):
            self.update_items(filename)

    def update_items(self, filename):
        """
        This function parses game process items (loot, event, etc) in line-separated text file and
        puts them into separate mongoDB collections.
        """
        file = self.filepath + filename
        name, _, _ = filename.partition('.')
        for line in [line.rstrip('\n') for line in open(file)]:
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
