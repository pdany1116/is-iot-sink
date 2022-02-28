import json
import time

class ValveLogJsonBuilder:
    def __init__(self, valve_id, action, user_id):
        self.__data = {}
        now = time.time()
        self.__data['timestamp'] = now
        self.__data['valveId'] = valve_id
        self.__data['action'] = action
        self.__data['userId'] = user_id
    
    def dumps(self):
        return json.dumps(self.__data)

