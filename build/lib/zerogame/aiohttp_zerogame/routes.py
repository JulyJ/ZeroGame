from os.path import dirname, abspath, join

from zerogame.aiohttp_zerogame.views import PageViews, StopJourney
from zerogame.aiohttp_zerogame.websockets import WebSocket


views = PageViews()
routes = [
    ('GET', '/index', views.index, 'index'),
    ('*', '/start', views.start, 'login'),
    ('GET', '/ws', WebSocket, 'game'),
    ('*', '/stop_journey', StopJourney, 'stop_journey')
    ]


def setup_routes(app):
    for method, path, handler, name in routes:
        app.router.add_route(method, path, handler, name=name)
    app.router.add_static('/static/',
                          join(dirname(dirname(abspath(__file__))), 'static'),
                          name='static')
