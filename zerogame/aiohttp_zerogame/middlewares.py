from aiohttp import web
from aiohttp_session import get_session

from .config import log
from .routes import routes


async def authorize(app, handler):
    async def middleware(request):
        def check_path(path):
            return not (any(path.startswith(route_path) for _, route_path, _, _ in routes)
                        or request.path.startswith('/static/')
                        or request.path.startswith('/_debugtoolbar'))

        session = await get_session(request)
        if session.get("user"):
            last_visit = session.get('last_visit', None)
            log.debug('Last visited set: {}'.format(last_visit))
            return await handler(request)
        elif check_path(request.path):
            url = request.app.router['index'].url()
            raise web.HTTPFound(url)
            return handler(request)
        else:
            return await handler(request)

    return middleware


async def mongo_handler(app, handler):
    async def middleware(request):
        request.db = app.db
        response = await handler(request)
        return response
    return middleware
