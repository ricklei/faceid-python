import logging


class logger(object):

    def __init__(self):
        logging.basicConfig(level = logging.INFO,
                            format = '%(asctime)s %(levelname)-8s %(message)s',
                            datefmt = '%Y/%m/%d %H:%M:%S')

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)
