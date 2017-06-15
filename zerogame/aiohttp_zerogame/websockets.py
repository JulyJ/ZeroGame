import sockjs
from aiohttp.web import View
# from aiohttp_session import get_session
# from asyncio import sleep

# from .game import Story
# from .user import User


class WebSocket(View):
    def __init__(self):
        self.character = 'John Doe'
        self.journey = True

    async def msg_handler(self, msg, session):
        if msg.tp == sockjs.MSG_OPEN:
            session.manager.broadcast('<b>Journey for {} started.</b>'.format(self.character))
        elif msg.tp == sockjs.MSG_MESSAGE:
            session.manager.broadcast(msg.data)
        elif msg.tp == sockjs.MSG_CLOSED:
            self.journey = False
            session.manager.broadcast('<b>Journey for {} ended.</b>'.format(self.character))

    # async def get_event(self, character, resp):
    #     story = Story(self.request.db, character)
    #     event = await story.get_event()
    #     await send_str('[{character}] {event}'.format(
    #         character=character,
    #         event=event
    #     ))
    #     await sleep(10)
    #
    # async def get_character(self, session):
    #     user = User(self.request.db, {'id': session.get('user')})
    #     return await user.get_character()
    #
    # async def journey(self):
    #     while self.journey:
    #         await self.get_event(self.character, session)
