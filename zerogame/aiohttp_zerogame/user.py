from bson import ObjectId

from asyncio import CancelledError

from .config import log


class User:

    def __init__(self, db, data, **kw):
        self.db = db
        self.collection = self.db.users
        self.id = data.get('id')
        self.email = data.get('email')
        self.name = data.get('name')
        self.character_name = data.get('character_name')

    async def check_user(self, **kw):
        return await self.collection.find_one({'email': self.email})

    async def get_character(self, **kw):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        return user.get('character_name')

    async def create_user(self, **kw):
        user = await self.check_user()
        if not user:
            result = await self.collection.insert({
                'email': self.email,
                'name': self.name,
                'character_name': self.character_name
            })
            log.debug('Creating user: {}'.format(self.email))
        else:
            result = 'User exists'
            log.debug('Existing user: {}'.format(self.email))
        return result

    async def get_user(self, id):
        try:
            user = await self.collection.find_one({'_id': ObjectId(self.id)})
        except CancelledError:
            log.debug('Async operation was canceled.')
            return
        self.email = user.get('email')
        self.name = user.get('name')
        self.character_name = user.get('character_name')
