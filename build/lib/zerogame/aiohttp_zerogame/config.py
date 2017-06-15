from logging import getLogger, DEBUG, basicConfig

DEBUG_MODE = True

log = getLogger('app')
basicConfig(
        format='%(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S',
        level=DEBUG,
    )

db_conf = {
    'database': 'zerogame',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5432',
    'minsize': 1,
    'maxsize': 10,
    'timeout': 60
}
