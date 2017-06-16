import sockjs
from aiohttp.web import View


class WebSocket(View):
    def __init__(self):
        self.character = 'John Doe'

    async def msg_handler(self, msg, session):
        if msg.tp == sockjs.MSG_OPEN:
            session.manager.broadcast('<b>Journey for {} started.</b>'.format(self.character))
        elif msg.tp == sockjs.MSG_MESSAGE:
            session.manager.broadcast(msg.data)
        elif msg.tp == sockjs.MSG_CLOSED:
            session.manager.broadcast('<b>Journey for {} ended.</b>'.format(self.character))
