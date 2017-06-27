from logging import getLogger, DEBUG, basicConfig

DEBUG_MODE = True

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

server_url = 'http://localhost:8080'
client_url = 'http://localhost:3000'

log = getLogger()
basicConfig(
        format='%(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S',
        level=DEBUG,
    )
