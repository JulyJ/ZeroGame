from os import path

from .views import PageViews


def setup_routes(app):
    views = PageViews()
    app.router.add_get('/', views.index)
    app.router.add_post('/start', views.start)
    app.router.add_static('/static/',
                          path=path.abspath(__file__)+'/../../'+'/static/',
                          name='static')
