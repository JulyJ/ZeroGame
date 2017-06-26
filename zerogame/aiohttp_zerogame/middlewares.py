from aiohttp import web

from .routes import routes


async def mongo_handler(app, handler):
    async def middleware(request):
        request.db = app.db
        response = await handler(request)
        return response
    return middleware


async def authorize(app, handler):
    async def middleware(request):
        def check_path(path):
            return not (any(path.startswith(route_path) for _, route_path, _, _ in routes)
                        or request.path.startswith('/static/')
                        or request.path.startswith('/ws')
                        or request.path.startswith('/oauth')
                        or request.path.startswith('/client_start')
                        or request.path.startswith('/_debugtoolbar'))

        if check_path(request.path):
            url = request.app.router['index'].url()
            raise web.HTTPFound(url)
        return await handler(request)

    return middleware
