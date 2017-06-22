from os.path import dirname, abspath, join

from .auth import AuthRoute
from .views import PageViews, StopJourney


views = PageViews()
route = AuthRoute()
routes = [
    ('GET', '/index', views.index, 'index'),
    ('*', '/start', views.start, 'login'),
    ('*', '/stop_journey', StopJourney, 'stop_journey'),
    ('GET', '/oauth/{provider}', route.oauth, 'oauth')
    ]


def setup_routes(app):
    for method, path, handler, name in routes:
        app.router.add_route(method, path, handler, name=name)
    app.router.add_static('/static/',
                          join(dirname(dirname(abspath(__file__))), 'static'),
                          name='static')
