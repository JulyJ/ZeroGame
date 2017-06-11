from time import time, sleep

from aiohttp.web import WebSocketResponse, WSMsgType, View
import aiohttp_jinja2
from aiohttp_session import get_session

from zerogame.aiohttp_zerogame.config import log
from zerogame.aiohttp_zerogame.user import User
from zerogame.aiohttp_zerogame.game import Story, Event


def set_session(session, user_id):
    session['user'] = str(user_id)
    session['last_visit'] = time()


class PageViews:
    @staticmethod
    async def index(request):
        session = await get_session(request)
        session['last_visit'] = time()
        response = aiohttp_jinja2.render_template('index.html',
                                                  request,
                                                  {'text': 'Zero Game'}
                                                  )
        return response

    @aiohttp_jinja2.template('start.html')
    async def start(self, request):
        data = await request.post()
        user = User(request.db, data)
        result = await user.check_user()
        if not isinstance(result, dict):
            await user.create_user()
            result = await user.check_user()
        session = await get_session(request)
        log.debug('Session: {}'.format(session))
        set_session(session, str(result['_id']))
        return {'text': 'Started!',
                'home_url': '/'}


class WebSocket(View):
    async def get(self):
        resp = WebSocketResponse()
        await resp.prepare(self.request)

        session = await get_session(self.request)
        user = User(self.request.db, {'id': session.get('user')})
        character = await user.get_character()

        for ws in self.request.app['websockets']:
            await ws.send_str('game for {} started'.format(character))
        self.request.app['websockets'].append(resp)

        for i in range(11):
            for ws in self.request.app['websockets']:
                try:
                    event = Event(self.request.db, character)
                    await ws.send_str(await event.get_event())
                    sleep(2)
                except Exception as e:
                    log.debug('Exception: {e}'.format(e=e))

        async for msg in resp:
            log.debug(msg)
            if msg.tp == WSMsgType.text:
                if msg.data == 'close':
                    await resp.close()
                else:
                    story = Story(self.request.db)
                    result = await story.save(character, msg.data)
                    log.debug(result)
                    try:
                        for ws in self.request.app['websockets']:
                            await ws.send_str('(%s) %s' % (character, msg.data))
                    except Exception as e:
                        log.debug(e)
            elif msg.tp == WSMsgType.error:
                log.debug('ws connection closed with exception %s' % resp.exception())

        self.request.app['websockets'].remove(resp)
        for ws in self.request.app['websockets']:
            await ws.send_str('%s ended journey.' % character)
            log.debug('websocket connection closed')

        return resp
