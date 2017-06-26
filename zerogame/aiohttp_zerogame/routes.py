from os.path import dirname, abspath, join

from aiohttp_cors import ResourceOptions, setup as cors_setup

from .auth import AuthRoute
from .views import PageViews, StopJourney, ClientStart


views = PageViews()
route = AuthRoute()
routes = [
    ('GET', '/index', views.index, 'index'),
    ('*', '/start', views.start, 'login'),
    ('*', '/stop_journey', StopJourney, 'stop_journey'),
    ('GET', '/oauth/{provider}', route.oauth, 'oauth'),
    ('OPTIONS', '/client_start', ClientStart, 'client_start'),
    ]


def setup_routes(app):
    for method, path, handler, name in routes:
        app.router.add_route(method, path, handler, name=name)
    app.router.add_static('/static/',
                          join(dirname(dirname(abspath(__file__))), 'static'),
                          name='static')


def setup_cors(app):
    cors = cors_setup(app)
    resource = cors.add(app.router.add_resource("/client_start"))
    cors.add(
        resource.add_route('POST', ClientStart),
        {
            '*': ResourceOptions(
                allow_methods=['POST'],
                allow_credentials=True,
                expose_headers='*',
                allow_headers='*'
            )
        },
    )
