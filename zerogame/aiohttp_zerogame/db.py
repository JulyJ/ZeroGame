from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:
    def __init__(self):
        self.client = AsyncIOMotorClient('mongodb://localhost:27017')
        self.db = self.client.zerogame
