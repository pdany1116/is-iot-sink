import pathlib
from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    INFO = 0
    ERROR = 1
    CRITICAL = 2

class Logger:
    def __init__(self, printConsole = False):
        self.__printConsole = printConsole
        self.__levels = { 
            LogLevel.INFO : "INFO", 
            LogLevel.ERROR : "ERROR", 
            LogLevel.CRITICAL : "CRITICAL"
        }

        if pathlib.Path(__file__).parent.parent.joinpath("logs").exists() == False:
            pathlib.Path(__file__).parent.parent.joinpath("logs").mkdir()
        self.__filepath = pathlib.Path(__file__).parent.parent.joinpath("logs").joinpath("log")

    def info(self, message: str):
        self.__log(LogLevel.INFO, message)

    def err(self, message: str):
        self.__log(LogLevel.ERROR, message)

    def critical(self, message: str):
        self.__log(LogLevel.CRITICAL, message)

    def __log(self, level: LogLevel, message: str):
        to_write = "{} [{}]: {}".format(self.__get_time_now(), self.__levels[level], message)
        if self.__printConsole:
            print(to_write)
        file = open(self.__filepath, "a")
        file.write(to_write)
        file.close()
        
    def __get_time_now(self):
        now = datetime.now()
        return now.strftime("%D %H:%M:%S")

LOG = Logger(printConsole = True)