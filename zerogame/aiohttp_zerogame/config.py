from logging import getLogger, DEBUG, basicConfig


log = getLogger('app')
basicConfig(
        format='%(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S',
        level=DEBUG,
    )

DEBUG = True
