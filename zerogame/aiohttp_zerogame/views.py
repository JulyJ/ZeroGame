import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {'text': 'Zero Game'}


@aiohttp_jinja2.template('start.html')
async def start(request):
    data = await request.post()
    name = data['name']
    return {'text': 'Started for {}'.format(name)}
