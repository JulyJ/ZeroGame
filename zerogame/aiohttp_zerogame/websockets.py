import sockjs
from aiohttp_session import get_session

from .config import log
from .user import User


class WebSocket:
    async def msg_handler(self, msg, ws_session, *args, **kwargs):

        ws_session.aio_session = await get_session(request=ws_session.request)
        id = ws_session.aio_session.get('user')
        try:
            ws_session.user = User(ws_session.app.db, {'id': id})
        except AttributeError as e:
            log.debug('AttributeError: %s' % e)
            return
        await ws_session.user.get_user(id)
        if msg.tp == sockjs.MSG_OPEN:
            ws_session.manager.broadcast('{} started journey.'.format(
                ws_session.user.character_name))
            ws_session.app['websockets'].append(ws_session)
        elif msg.tp == sockjs.MSG_MESSAGE:
            ws_session.manager.broadcast(msg.data)
        elif msg.tp == sockjs.MSG_CLOSED:
            ws_session.app['websockets'].remove(ws_session)


class RequestSessionManager(sockjs.SessionManager):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    def get(self, *args, **kwargs):
        ws_session = super().get(*args, **kwargs)
        ws_session.request = kwargs.get('request', None)
        ws_session.app = self.app
        return ws_session
