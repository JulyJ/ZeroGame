from json import loads

from sockjs import MSG_CLOSED, MSG_MESSAGE, MSG_OPEN, SessionManager
from aiohttp_session import get_session

from .config import log
from .user import User
from .game import Room
from .elements.encounter import Encounter
from .elements.methods import ws_message, room_broadcast


class WebSocket:
    def __init__(self):
        self.ws_session = None

    async def msg_handler(self, msg, ws_session):
        self.ws_session = ws_session
        self.ws_session.aio_session = await get_session(request=self.ws_session.request)

        if msg.tp == MSG_OPEN:
            pass
        elif msg.tp == MSG_MESSAGE:
            await self.route_message(msg)
        elif msg.tp == MSG_CLOSED:
            for ws in self.ws_session.room.members:
                ws.send(await ws_message('{} ended journey.'.format(
                    self.ws_session.user.character_name)))
            self.ws_session.app.websockets.remove(self.ws_session)

    async def start_journey(self, user_data):
        self.ws_session.app.websockets.append(self.ws_session)
        self.ws_session.room = await self.find_room()
        email = user_data.get('email')
        try:
            self.ws_session.user = User(self.ws_session.app.db, {'email': email})
        except AttributeError as e:
            log.debug('AttributeError: %s' % e)
            return
        await self.ws_session.user.get_user()

        self.ws_session.room.members.append(self.ws_session)
        log.debug('Session {f.id} was appended to room {f.room.uuid}'.format(f=self.ws_session))
        await room_broadcast(
            self.ws_session.room,
            '{} started journey.'.format(
                self.ws_session.user.character_name))
        self.ws_session.send(await ws_message(self.ws_session.user.level, 'level'))

    async def stop_journey(self, user_data):
        try:
            self.ws_session.room.members.remove(self.ws_session)
        except ValueError:
            log.debug('Session {f.id} in {f.room.uuid} room is inactive'.format(f=self.ws_session))
        log.debug('Session {f.id} was removed from room {f.room.uuid}'.format(f=self.ws_session))
        await self.ws_session.room.check_room()
        self.ws_session.close()

    async def find_room(self):
        for room in self.ws_session.app.rooms:
            await room.check_room()
            if room.available:
                return room
        room = Room(self.ws_session.app)
        await room.append_room()
        return room

    async def start_encounter(self, user_data):
        if not self.ws_session.encounter:
            encounter = Encounter(self.ws_session.app)
            self.ws_session.encounter = encounter
            await encounter.start_encounter(self.ws_session)
            await room_broadcast(
                self.ws_session.room,
                '{} paused journey.'.format(
                    self.ws_session.user.character_name)
            )
            log.debug('user {u} started encounter {e}'.format(
                u=self.ws_session,
                e=encounter.name
            ))

    async def resume_journey(self):
        self.ws_session.room = await self.find_room()
        self.ws_session.room.members.append(self.ws_session)
        log.debug('Session {f.id} was appended to room {f.room.uuid}'.format(f=self.ws_session))
        await room_broadcast(
            self.ws_session.room,
            '{} resumed journey.'.format(
                self.ws_session.user.character_name)
        )
        self.ws_session.send(await ws_message(self.ws_session.user.level, 'level'))

    async def stop_encounter(self, user_data):
        if self.ws_session.encounter:
            log.debug('user {u} stopped encounter {e}'.format(
                u=self.ws_session,
                e=self.ws_session.encounter.name
            ))
            await self.ws_session.encounter.stop_encounter(self.ws_session)
            await self.resume_journey()
            self.ws_session.encounter = None

    @staticmethod
    async def unknown_command(user_data):
        log.debug('Unknown ws command received from server')

    async def route_message(self, msg):
        commands = {
            'start_journey': self.start_journey,
            'stop_journey': self.stop_journey,
            'start_encounter': self.start_encounter,
            'stop_encounter': self.stop_encounter
        }
        json_data = loads(msg.data)
        if 'command' in json_data:
            await commands.get(
                json_data.get('command'),
                self.unknown_command
            )(json_data.get('command_data', None))
        else:
            self.unknown_command((json_data.get('command_data', None)))


class RequestSessionManager(SessionManager):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    def get(self, *args, **kwargs):
        ws_session = super().get(*args, **kwargs)
        ws_session.request = kwargs.get('request', None)
        ws_session.app = self.app
        ws_session.room = None
        ws_session.encounter = None
        return ws_session
