import logging
import os


class Logger:
    FORMAT = '%(asctime)-15s %(message)s'
    logger = ''
    __instance = None

    def __new__(cls):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
            logging.basicConfig(format=Logger.FORMAT, level=10)
            Logger.logger = logging.getLogger('default')
        return Logger.__instance

    def log(self, msg):
        self.logger.info(msg)
