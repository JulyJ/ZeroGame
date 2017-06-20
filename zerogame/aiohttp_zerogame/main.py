from base64 import urlsafe_b64decode
from os import path

import aiohttp_debugtoolbar
import aiohttp_jinja2
import asyncio
import jinja2
from aiohttp import web, WSCloseCode
from aiohttp_session import session_middleware, setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography.fernet import Fernet
from sockjs import add_endpoint


from .config import log, DEBUG_MODE
from .game import Game
from .middlewares import authorize, mongo_handler
from .routes import setup_routes
from .db import MongoClient
from .websockets import WebSocket, RequestSessionManager


class Server:
    async def init_server(self, loop):
        secret_key = self.make_secret()
        middle = [
            session_middleware(EncryptedCookieStorage(secret_key)),
            authorize,
            mongo_handler,
        ]
        templates_path = path.join(path.dirname(__file__), 'templates/')

        if DEBUG_MODE:
            middle.append(aiohttp_debugtoolbar.middleware)

        app = web.Application(
            loop=loop,
            middlewares=middle,
            debug=DEBUG_MODE
        )
        aiohttp_jinja2.setup(
            app,
            loader=jinja2.FileSystemLoader(templates_path)
        )

        if DEBUG_MODE:
            aiohttp_debugtoolbar.setup(app)

        setup_routes(app)

        setup_session(
            app,
            EncryptedCookieStorage(secret_key)
        )

        app.mongo = MongoClient()
        await app.mongo.update_names()
        app.db = app.mongo.db

        app.ws = WebSocket()
        app['websockets'] = []
        request_session_manager = RequestSessionManager(
            name='ws',
            app=app,
            handler=app.ws.msg_handler,
            loop=loop,
        )
        add_endpoint(app=app,
                     prefix='/ws',
                     handler=app.ws.msg_handler,
                     name='ws',
                     manager=request_session_manager
                     )

        handler = app.make_handler(debug=DEBUG_MODE)
        server_generator = loop.create_server(handler, host='localhost', port=8080)

        game = Game(app, handler)
        app.game = game

        return server_generator, handler, app, game

    def run_server(self):

        loop = asyncio.get_event_loop()
        server_generator, handler, app, game = loop.run_until_complete(self.init_server(loop))
        server = loop.run_until_complete(server_generator)
        log.debug('Starting server %s' % str(server.sockets[0].getsockname()))
        try:
            loop.run_until_complete(game.run_game())
            loop.run_forever()
        except KeyboardInterrupt:
            log.debug('Stopping server...')
        finally:
            loop.run_until_complete(self.shutdown(server, app, handler, game))
            log.debug('Server stopped.')

    @staticmethod
    async def shutdown(server, app, handler, game):
        server.close()
        app.mongo.client.close()
        game.close()
        await server.wait_closed()
        await app.shutdown()
        for ws in app['websockets']:
            ws.close(WSCloseCode.GOING_AWAY)
            log.debug('Session {} closed.'.format(ws.id))
        await app.cleanup()

    @staticmethod
    def make_secret():
        # secret_key must be 32 url-safe base64-encoded bytes
        fernet_key = Fernet.generate_key()
        return urlsafe_b64decode(fernet_key)


def run():
    server = Server()
    server.run_server()
