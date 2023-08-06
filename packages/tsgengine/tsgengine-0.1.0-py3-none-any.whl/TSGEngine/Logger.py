from TSGEngine.Utility import Singleton

from datetime import datetime


class Logger(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def log(message=None, origin=None, log_type="Info"):
        log_message = f'[{datetime.time(datetime.today()).replace(microsecond=0)}] [{log_type}] [{origin}]: {message}\n'
        print(log_message, end='')


def log(message=None, origin=None, log_type="Info"):
    Logger().log(message=message, origin=origin, log_type=log_type)
