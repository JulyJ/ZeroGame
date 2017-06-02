from time import time
import aiohttp_jinja2
from aiohttp_session import get_session


class PageViews:
    @staticmethod
    async def index(request):
        session = await get_session(request)
        session['last_visit'] = time()
        response = aiohttp_jinja2.render_template('index.html',
                                                  request,
                                                  {'text': 'Zero Game'}
                                                  )
        return response

    @aiohttp_jinja2.template('start.html')
    async def start(self, request):
        data = await request.post()
        name = data['name'] if 'name' in data else 'John Doe'
        return {'text': 'Started for {}'.format(name)}
