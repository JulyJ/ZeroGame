from bson import ObjectId

from .config import log


class User:

    def __init__(self, db, data, **kw):
        self.db = db
        self.collection = self.db.users
        self.email = data.get('email')
        self.name = data.get('name')
        self.character_name = data.get('character_name')

    async def check_user(self, **kw):
        return await self.collection.find_one({'email': self.email})

    async def get_email(self, **kw):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        return user.get('email')

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
