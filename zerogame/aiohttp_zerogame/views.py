from aiohttp import web
import aiohttp_jinja2


class PageViews():
    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {'text': 'Zero Game'}

    @aiohttp_jinja2.template('start.html')
    async def start(self, request):
        data = await request.post()
        name = data['name']
        return {'text': 'Started for {}'.format(name)}


class WebSocket(web.View):
    pass
