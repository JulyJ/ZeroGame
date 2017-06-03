from aiohttp_session import get_session

from .config import log


async def authorize(app, handler):
    async def middleware(request):
        session = await get_session(request)
        last_visit = session['last_visit'] if 'last_visit' in session else None
        log.debug('Last visited set: {}'.format(last_visit))
        return await handler(request)
    return middleware
