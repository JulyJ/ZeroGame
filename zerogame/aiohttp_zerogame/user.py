from asyncio import CancelledError
from math import sqrt
from passlib.hash import pbkdf2_sha256

from .config import log


class User:

    def __init__(self, db, data, **kw):
        self.db = db
        self.collection = self.db.users
        self.id = data.get('id')
        self.email = data.get('email')
        self.name = data.get('name')
        self.password = data.get('password')
        self.character_name = data.get('character_name')
        self.level = 0

    async def check_user(self, **kw):
        return await self.collection.find_one({'email': self.email})

    async def get_property(self, property, **kw):
        user = await self.collection.find_one({'email': self.email})
        return user.get(property)

    async def auth(self):
        return pbkdf2_sha256.verify(self.password, await self.get_property('hash'))

    async def create_user(self, **kw):
        user = await self.check_user()
        if not user:
            result = await self.collection.insert({
                'email': self.email,
                'hash': pbkdf2_sha256.hash(self.password),
                'name': self.name,
                'character_name': self.character_name,
                'points': 0,
                'experience': 0
            })
            log.debug('Creating user: {}'.format(self.email))
        else:
            result = 'User exists'
            log.debug('Existing user: {}'.format(self.email))
        return result

    async def get_user(self):
        try:
            user = await self.collection.find_one({'email': self.email})
        except CancelledError:
            log.debug('Async operation was canceled.')
            return
        self.email = user.get('email')
        self.name = user.get('name')
        self.character_name = user.get('character_name')
        self.hash = user.get('hash')
        self.id = user.get('_id')
        self.points = user.get('points')
        self.experience = user.get('experience')
        self.level = await self.check_level()

    async def write_user_data(self):
        await self.collection.update(
            {'email': self.email},
            {
                '$set':
                    {
                        'points': self.points,
                        'experience': self.experience
                    }
            },
            upsert=True
        )
        log.debug('Updating user: {}'.format(self.email))

    async def check_level(self):
        return 0.1 * sqrt(self.experience)
