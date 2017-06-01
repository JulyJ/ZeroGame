from os import path

from .views import PageViews


views = PageViews()
routes = [
    ('GET', '/', views.index,  'main'),
    ('*', '/start',   views.start, 'login')
    ]


def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    app.router.add_static('/static/',
                          path.abspath(__file__)+'/../../'+'/static/',
                          name='static')
