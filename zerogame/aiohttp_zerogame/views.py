from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session


class PageViews():
    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        session = await get_session(request)
        return {'text': 'Zero Game'}

    @aiohttp_jinja2.template('start.html')
    async def start(self, request):
        data = await request.post()
        name = data['name'] if 'name' in data else 'John Doe'
        return {'text': 'Started for {}'.format(name)}


class WebSocket(web.View):
    pass
