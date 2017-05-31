from aiohttp import web
import aiohttp_jinja2
import jinja2
from os import path

from .routes import setup_routes


def run():
    templates_path = str(path.dirname(__file__) + '/templates/')

    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(templates_path))
    setup_routes(app)
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    run()
