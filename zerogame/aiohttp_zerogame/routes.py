from os.path import dirname, abspath, join

from .views import PageViews, StopJourney


views = PageViews()
routes = [
    ('GET', '/index', views.index, 'index'),
    ('*', '/start', views.start, 'login'),
    ('*', '/stop_journey', StopJourney, 'stop_journey')
    ]


def setup_routes(app):
    for method, path, handler, name in routes:
        app.router.add_route(method, path, handler, name=name)
    app.router.add_static('/static/',
                          join(dirname(dirname(abspath(__file__))), 'static'),
                          name='static')
