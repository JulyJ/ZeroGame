from aiohttp import web
import aiohttp_jinja2
import asyncio
import jinja2
from os import path

from .routes import setup_routes
from .settings import log


async def on_shutdown(app):
    for ws in app['websock']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, app, handler):
    server.close()
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()


async def run(loop):
    templates_path = str(path.dirname(__file__) + '/templates/')

    app = web.Application(loop=loop)
    app['websock'] = []
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(templates_path))
    setup_routes(app)
    app.on_shutdown.append(on_shutdown)
    handler = app.make_handler()
    server_generator = loop.create_server(handler, host='127.0.0.1', port=8080)
    return server_generator, handler, app


loop = asyncio.get_event_loop()
server_generator, handler, app = loop.run_until_complete(run(loop))
server = loop.run_until_complete(server_generator)
try:
    loop.run_forever()
except KeyboardInterrupt:
    log.debug('Stopping server...')
finally:
    loop.run_until_complete(shutdown(server, app, handler))
    loop.close()
    log.debug('Server stopped.')
