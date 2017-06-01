from logging import getLogger, DEBUG, Formatter, StreamHandler

log = getLogger('app')
log.setLevel(DEBUG)

form = Formatter('%(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
ch = StreamHandler()
ch.setLevel(DEBUG)
ch.setFormatter(form)
log.addHandler(ch)
