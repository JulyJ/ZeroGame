from aiohttp.web import WebSocketResponse, View, WSMsgType
from aiohttp_session import get_session
from asyncio import sleep

from zerogame.aiohttp_zerogame.config import log
from zerogame.aiohttp_zerogame.user import User
from zerogame.aiohttp_zerogame.game import Story


class WebSocket(View):
    async def get_event(self, character, resp):
        story = Story(self.request.db, character)
        event = await story.get_event()
        for ws in self.request.app['websockets']:
            await ws.send_str('[{character}] {event}'.format(   #if ws close
                character=character,
                event=event
            ))
        await sleep(10)

    async def get(self):
        self.journey = True
        resp = WebSocketResponse()
        await resp.prepare(self.request)

        session = await get_session(self.request)
        user = User(self.request.db, {'id': session.get('user')})
        character = await user.get_character()

        for ws in self.request.app['websockets']:
            await ws.send_str('<b>game for {} started</b>'.format(character))
        self.request.app['websockets'].append(resp)

        while self.journey:
            await self.get_event(character, resp)
        async for msg in resp:
            if msg.type == WSMsgType.ERROR:
                self.request.app['websockets'].remove(resp)


        for ws in self.request.app['websockets']:
            await ws.send_str('%s ended journey.' % character)
            log.debug('websocket connection closed')

        return resp
