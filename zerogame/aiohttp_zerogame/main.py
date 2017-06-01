import asyncio
from aiohttp import web
import aiohttp_debugtoolbar
import aiohttp_jinja2
from aiohttp_session import session_middleware, setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64
from cryptography import fernet
import jinja2
from os import path

from .routes import setup_routes
from .settings import log, DEBUG
from .middlewares import authorize


class Server:
    async def init_server(self, loop):
        secret_key = self.make_secret()
        templates_path = str(path.dirname(__file__) + '/templates/')
        middle = [
            session_middleware(EncryptedCookieStorage(secret_key)),
            authorize
        ]

        if DEBUG:
            middle.append(aiohttp_debugtoolbar.middleware)

        app = web.Application(loop=loop, middlewares=middle)
        app['websock'] = []
        aiohttp_jinja2.setup(app,
                             loader=jinja2.FileSystemLoader(templates_path))
        setup_routes(app)
        setup_session(app, EncryptedCookieStorage(secret_key))

        if DEBUG:
            aiohttp_debugtoolbar.setup(app)

        app.on_shutdown.append(self.on_shutdown)
        handler = app.make_handler()
        server_generator = loop.create_server(handler, host='127.0.0.1', port=8080)
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
    async def on_shutdown(app):
        for ws in app['websock']:
            await ws.close(code=1001, message='Server shutdown')

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


def run():
    server = Server()
    server.run_server()


if __name__ == '__main__':
    run()
