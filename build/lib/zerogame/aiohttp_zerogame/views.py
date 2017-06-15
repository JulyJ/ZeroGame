from time import time

from aiohttp.web import View, HTTPFound, HTTPForbidden
import aiohttp_jinja2
from aiohttp_session import get_session

from zerogame.aiohttp_zerogame.config import log
from zerogame.aiohttp_zerogame.user import User


def set_session(session, user_id):
    session['user'] = str(user_id)
    session['last_visit'] = time()


def redirect(request, router):
    url = request.app.router[router].url()
    raise HTTPFound(url)


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
        user = User(request.db, data)
        result = await user.check_user()
        if not isinstance(result, dict):
            await user.create_user()
            result = await user.check_user()
        session = await get_session(request)
        log.debug('Session: {}'.format(session))
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
