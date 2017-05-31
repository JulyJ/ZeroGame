from os import path

from .views import index, start


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/start', start)
    app.router.add_static('/static/',
                          path=path.abspath(__file__)+'/../../'+'/static/',
                          name='static')
