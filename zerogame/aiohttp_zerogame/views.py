from time import time

import aiohttp_jinja2
from aiohttp_session import get_session

from .config import log
from .user import User


def set_session(session, user_id):
    session['user'] = str(user_id)
    session['last_visit'] = time()


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
        if isinstance(result, dict):
            session = await get_session(request)
            log.debug('Session: {}'.format(session))
            set_session(session, str(result))
            return {'text': 'Started!',
                    'home_url': '/'}
        else:
            await user.create_user()
            return {'text': 'Started!',
                    'home_url': '/'}
