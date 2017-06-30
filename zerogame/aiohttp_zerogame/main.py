from base64 import urlsafe_b64decode
from os import path

from aiohttp import web, WSCloseCode
from aiohttp_debugtoolbar import (setup as debugtoolbar_setup,
                                  middleware as debugtoolbar_middleware)
from aiohttp_jinja2 import setup as jinja2_setup
from aiohttp_session import session_middleware, setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from asyncio import set_event_loop
from cryptography.fernet import Fernet
from jinja2 import FileSystemLoader
from sockjs import add_endpoint
from uvloop import new_event_loop


from .config import log, DEBUG_MODE
from .game import Game
from .middlewares import authorize, mongo_handler
from .routes import setup_routes, setup_cors
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
            middle.append(debugtoolbar_middleware)

        app = web.Application(
            loop=loop,
            middlewares=middle,
            debug=DEBUG_MODE
        )
        jinja2_setup(
            app,
            loader=FileSystemLoader(templates_path)
        )

        if DEBUG_MODE:
            debugtoolbar_setup(app)

        setup_routes(app)
        setup_cors(app)

        setup_session(
            app,
            EncryptedCookieStorage(secret_key)
        )

        app.mongo = MongoClient()
        await app.mongo.update_names()
        app.db = app.mongo.db

        app.ws = WebSocket()
        app['websockets'] = []
        app['rooms'] = []
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

        loop = new_event_loop()
        set_event_loop(loop)
        loop.set_debug(DEBUG_MODE)

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
        loop.close()

    @staticmethod
    async def shutdown(server, app, handler, game):
        server.close()
        app.mongo.client.close()
        game.close()
        await server.wait_closed()
        await app.shutdown()
        await handler.shutdown(1)
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
