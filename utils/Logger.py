import logging
from utils.parameters import Parameters

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

    @staticmethod
    def getLogger():
        if Logger.__instance is not None:
            return Logger.__instance
        return Logger()

    def info(self, msg):
        self.logger.info(msg)

    def verbose(self, msg):
        if Parameters.is_verbose:
            self.info(msg)
