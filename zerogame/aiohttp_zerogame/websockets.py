import sockjs


class WebSocket:
    async def msg_handler(self, msg, ws_session, *args, **kwargs):
        if msg.tp == sockjs.MSG_OPEN:
            ws_session.manager.broadcast('<b>Journey started.</b>')
            ws_session.manager.app['websockets'].append(ws_session)
        elif msg.tp == sockjs.MSG_MESSAGE:
            ws_session.manager.broadcast(msg.data)
        elif msg.tp == sockjs.MSG_CLOSED:
            ws_session.manager.broadcast('<b>Journey ended.</b>')
            ws_session.manager.app['websockets'].remove(ws_session)


class RequestSessionManager(sockjs.SessionManager):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    def get(self, *args, **kwargs):
        ws_session = super().get(*args, **kwargs)
        ws_session.request = kwargs.get('request', None)
        return ws_session
