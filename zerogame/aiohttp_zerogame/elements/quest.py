from asyncio import sleep
from random import randrange
from time import gmtime, mktime

from ..config import log, DEBUG_MODE
from .methods import room_broadcast, get_random_item


class Quest:
    def __init__(self, app, room):
        self.app = app
        self.db = app.db
        self.experience = randrange(1000, 3000, 1000)
        self.length = randrange(60, 360, 10)
        self.name = None
        self.points = randrange(100, 1000, 100)
        self.room = room
        self.running = True
        self.start_time = gmtime()

        if DEBUG_MODE:
            self.length = randrange(6, 36, 1)

    async def get_quest_name(self):
        self.name = (await get_random_item(self.db, 'quests')).get('item')
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
                r=self.points,
                e=self.experience
                )
            )
        self.running = False
        log.debug("Quest {r.quest} completed in room {r.uuid}".format(
            r=self.room
        ))

        members = len(self.room.members)
        for member in self.room.members:
            member.user.experience += self.experience//members
            member.user.points += self.points//members
            log.debug("{u.name} now has {u.experience} exp and {u.points} points".format(
                u=member.user
            ))
            await member.user.level_up_broadcast(
                self.room,
                member
            )

            await member.user.write_user_data()
            self.room.quest = None

    async def run_quest(self):
        await self.check_quest_status()
        await sleep(1)
