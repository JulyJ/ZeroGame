from aiohttp import web
from aiohttp_session import get_session

from .routes import routes
from .settings import log


async def authorize(app, handler):
    async def middleware(request):
        def check_path(path):
            result = True
            for r in routes:
                if path.startswith(r[1]):
                    result = False
            return result

        session = await get_session(request)
        if session.get("user"):
            last_visit = session['last_visit'] if 'last_visit' in session else None
            log.debug('Last visited: {}'.format(last_visit))
            return await handler(request)

        elif check_path(request.path):
            url = request.app.router['index'].url()
            raise web.HTTPFound(url)
            return handler(request)
        else:
            return await handler(request)
    return middleware
