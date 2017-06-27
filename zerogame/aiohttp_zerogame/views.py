from json import dumps
from time import time

from aiohttp.web import View, HTTPFound, HTTPForbidden, Response
import aiohttp_jinja2
from aiohttp_session import get_session

from .config import client_url
from .user import User


def set_session(session, user_id):
    session['user'] = str(user_id)
    session['last_visit'] = time()


def redirect(request, router):
    url = request.app.router[router].url()
    raise HTTPFound(url)


class PageViews:
    def __init__(self):
        self._session = None

    @staticmethod
    async def index(request):
        session = await get_session(request)
        session['last_visit'] = time()
        return aiohttp_jinja2.render_template('index.html',
                                              request,
                                              {'text': 'Zero Game'}
                                              )

    @aiohttp_jinja2.template('start.html')
    async def start(self, request):
        data = await request.post()
        user = User(request.db, data)
        result = await user.check_user()
        if not isinstance(result, dict):
            await user.create_user()
            result = await user.check_user()
        session = await get_session(request)
        set_session(session, str(result['_id']))
        return {'text': 'Started!',
                'home_url': '/'}


class StopJourney(View):
    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'index')
        else:
            raise HTTPForbidden()


class ClientStart(View):
    async def options(self):   # https://github.com/aio-libs/aiohttp-cors/issues/41
        return Response(headers={'Allow': 'OPTIONS, POST',
                                 'Access-Control-Allow-Origin': client_url,
                                 'Access-Control-Allow-Headers': 'Content-Type'})

    async def post(self, **kw):
        data = await self.request.json()
        user = User(self.request.db, data)
        result = await user.check_user()
        if not isinstance(result, dict):
            await user.create_user()
            result = await user.check_user()
        session = await get_session(self.request)
        set_session(session, str(result['_id']))
        return Response(
            text=dumps({
                'id': str(result['_id']),
                'name': str(result['name']),
                'character_name': str(result['character_name']),
                'email': str(result['email'])
            })
        )
