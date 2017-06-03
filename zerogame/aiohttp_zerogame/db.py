from aiopg.sa import create_engine
import sqlalchemy as sa

from .config import log
from .db_conf import conf


class DataBaseConnection:
    metadata = sa.MetaData()
    users = sa.Table('users', metadata,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('name', sa.String(255)))

    @staticmethod
    async def create_table(engine):
        async with engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS users')
            await conn.execute('''CREATE TABLE users (
                                      id serial PRIMARY KEY,
                                      name varchar(255))''')
            log.debug('Table created.')

    async def init_pg(self, app):
        engine = await create_engine(
            database=conf['database'],
            user=conf['user'],
            password=conf['password'],
            host=conf['host'],
            port=conf['port'],
            minsize=conf['minsize'],
            maxsize=conf['maxsize'],
            loop=app.loop
        )
        app.db = engine
        log.debug('Database connection opened.')
        await self.create_table(app.db)

    @staticmethod
    async def close_pg(app):
        app.db.close()
        await app.db.wait_closed()
        log.debug('Database connection closed.')
