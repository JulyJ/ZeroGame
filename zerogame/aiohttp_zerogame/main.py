import base64
from os import path

import aiohttp_debugtoolbar
import aiohttp_jinja2
import asyncio
import jinja2
from aiohttp import web
from aiohttp_session import session_middleware, setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet


from config import log, DEBUG_MODE
from middlewares import authorize, mongo_handler
from routes import setup_routes
from db import MongoClient


class Server:
    async def init_server(self, loop):
        secret_key = self.make_secret()
        middle = [
            session_middleware(EncryptedCookieStorage(secret_key)),
            authorize,
            mongo_handler
        ]
        templates_path = str(path.dirname(__file__) + '/templates/')

        if DEBUG_MODE:
            middle.append(aiohttp_debugtoolbar.middleware)

        app = web.Application(
            loop=loop,
            middlewares=middle
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

        app.client = MongoClient()
        app.db = app.client.db

        app['websockets'] = []
        app.on_shutdown.append(self.on_shutdown)

        handler = app.make_handler()
        server_generator = loop.create_server(handler, host='localhost', port=8080)
        return server_generator, handler, app

    def run_server(self):
        loop = asyncio.get_event_loop()
        server_generator, handler, app = loop.run_until_complete(self.init_server(loop))
        server = loop.run_until_complete(server_generator)
        log.debug('Starting server %s' % str(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            log.debug('Stopping server...')
        finally:
            loop.run_until_complete(self.shutdown(server, app, handler))
            loop.close()
            log.debug('Server stopped.')

    @staticmethod
    async def shutdown(server, app, handler):
        server.close()
        await app.shutdown()
        await handler.finish_connections(10.0)
        await app.cleanup()

    @staticmethod
    def make_secret():
        # secret_key must be 32 url-safe base64-encoded bytes
        fernet_key = fernet.Fernet.generate_key()
        return base64.urlsafe_b64decode(fernet_key)

    @staticmethod
    async def on_shutdown(app):
        for ws in app['websockets']:
            await ws.close(code=1001, message='Server shutdown')


def run():
    server = Server()
    server.run_server()


if __name__ == '__main__':
    run()
