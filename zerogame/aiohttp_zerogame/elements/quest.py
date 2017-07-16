from asyncio import sleep
from random import randrange
from time import gmtime, mktime

from config import log
from .methods import room_broadcast


class Quest:
    def __init__(self, app, room):
        self.room = room
        self.app = app
        self.db = app.db
        self.running = True
        self.reward = randrange(100, 1000, 100)
        self.length = randrange(600, 3600, 100)
        self.experience = randrange(100, 3000, 100)
        self.start_time = gmtime()
        self.name = None

    async def get_quest_name(self):
        async for quest in self.db['quests'].aggregate([{'$sample': {'size': 1}}]):
            self.name = quest.get('item')
        await room_broadcast(self.room, "Quest {} started".format(self.name))
        self.room.quest = self.name
        log.debug("Quest {r.quest} started in room {r.uuid}".format(
            r=self.room
        ))

    async def check_quest_status(self):
        if mktime(gmtime()) - self.length >= mktime(self.start_time):
            await self.quest_completed()
        else:
            return

    async def quest_completed(self):
        await room_broadcast(
            self.room,
            'Quest {n} completed! Reward is {r} points and {e} experience.'.format(
                n=self.room.quest,
                r=self.reward,
                e=self.experience
                )
            )
        self.running = False
        log.debug("Quest {r.quest} completed in room {r.uuid}".format(
            r=self.room
        ))
        members = len(self.room.members)
        for member in self.room.members:
            member.user.experience = self.experience//members
            member.user.points = self.reward//members
            log.debug("{u.name} gets {u.experience} exp and {u.points} points".format(
                u=member.user
            ))
            await member.user.write_user_data()
            self.room.quest = None

    async def run_quest(self):
        await self.check_quest_status()
        await sleep(1)
