from time import time

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from bson.objectid import ObjectId

from .config import log
from .user import User


def redirect(request, router_name):
    url = request.app.router[router_name].url()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    redirect(request, 'main')


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
        user = User(request.db, data)
        result = await user.check_user()
        if isinstance(result, ObjectId):
            session = await get_session(self.request)
            log.debug('Session: {}'.format(session))
            set_session(session, str(result), self.request)
        else:
            await user.create_user()
            return {'text': 'Started for {}'.format(name)}
