from json import loads

from sockjs import MSG_CLOSED, MSG_MESSAGE, MSG_OPEN, SessionManager
from aiohttp_session import get_session

from .config import log
from .user import User


class WebSocket:
    async def msg_handler(self, msg, ws_session, *args, **kwargs):
        self.ws_session = ws_session
        self.ws_session.aio_session = await get_session(request=self.ws_session.request)

        if msg.tp == MSG_OPEN:
            pass
        elif msg.tp == MSG_MESSAGE:
            await self.route_message(msg)
        elif msg.tp == MSG_CLOSED:
            self.ws_session.app['websockets'].remove(self.ws_session)

    async def start_journey(self, user_data):
        self.ws_session.app['websockets'].append(self.ws_session)

        try:
            self.ws_session.user = User(self.ws_session.app.db, {'id': user_data.get('id')})
        except AttributeError as e:
            log.debug('AttributeError: %s' % e)
            return
        await self.ws_session.user.get_user(id)

        self.ws_session.manager.broadcast('{} started journey.'.format(
            self.ws_session.user.character_name))

    async def stop_journey(self, user_data):
        self.ws_session.close()


    @staticmethod
    async def unknown_command():
        log.debug('Unknown ws command received from server')

    async def route_message(self, msg):
        commands = {
            'start_journey': self.start_journey,
            'stop_journey': self.stop_journey,
        }
        json_data = loads(msg.data)
        if 'command' in json_data:
            await commands.get(
                json_data.get('command'),
                self.unknown_command
            )(json_data.get('command_data', None))
        else:
            self.unknown_command()


class RequestSessionManager(SessionManager):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    def get(self, *args, **kwargs):
        ws_session = super().get(*args, **kwargs)
        ws_session.request = kwargs.get('request', None)
        ws_session.app = self.app
        return ws_session
