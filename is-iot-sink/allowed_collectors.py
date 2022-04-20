import time
import utils

class AllowedCollectors:
    def __init__(self):
        self.__collectors = {}
        self.__expire_time = int(utils.get_setting("collectors/expireTime"))
    
    def add(self, id):
        self.__collectors[id] = time.time() + self.__expire_time

    def is_allowed(self, id):
        return id in self.__collectors.keys()

    def check_all(self):
        now = time.time()
        for key in list(self.__collectors):
            if now > self.__collectors[key]:
                self.__collectors.pop(key)
