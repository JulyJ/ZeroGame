from time import time

from aiohttp import web, WSMsgType
import aiohttp_jinja2
from aiohttp_session import get_session

from .config import log
from .user import User
from .game import Story


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
        if isinstance(result, dict):
            session = await get_session(request)
            log.debug('Session: {}'.format(session))
            set_session(session, str(result))
            return {'text': 'Started!',
                    'home_url': '/'}
        else:
            await user.create_user()
            return {'text': 'Started!',
                    'home_url': '/'}


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)
        user = User(self.request.db, {'id': session.get('user')})
        login = await user.get_email()

        for _ws in self.request.app['websockets']:
            _ws.send_str('game for {} started'.format(login))
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.tp == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    story = Story(self.request.db)
                    result = await story.save(user=login, msg=msg.data)
                    log.debug(result)
                    for _ws in self.request.app['websockets']:
                        _ws.send_str('(%s) %s' % (login, msg.data))
            elif msg.tp == WSMsgType.error:
                log.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            _ws.send_str('%s ended journey.' % login)
        log.debug('websocket connection closed')

        return ws
