import time
from is_iot_sink import utils
from is_iot_sink.logger import LOG
import threading
import time

class AllowedCollectors:
    def __init__(self):
        self.__collectors = {}
        self.__expire_time = int(utils.get_setting("collectors/expireTime"))
        self.__check_thread = threading.Thread(target=self.__check_all, daemon=True)
        self.__check_thread.start()

    def add(self, id):
        self.__collectors[id] = time.time() + self.__expire_time
        LOG.info("Added collector {}. Collectors: {}".format(id, self.__collectors.keys()))

    def is_allowed(self, id):
        return id in self.__collectors.keys()

    def __check_all(self):
        while True:
            now = time.time()
            for key in list(self.__collectors):
                if now > self.__collectors[key]:
                    LOG.info("Removed collector {}. Collectors: {}".format(key, self.__collectors.keys()))
                    self.__collectors.pop(key)
                    time.sleep(5)
        
    def get_all(self):
        return self.__collectors

ac = AllowedCollectors()
