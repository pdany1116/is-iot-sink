import json
import RPi.GPIO as GPIO
from is_iot_sink import utils
import time
import threading
from is_iot_sink.logger import LOG
from is_iot_sink.mongodb.mongodb_client import mongo_client

class ValveManager:
    def __init__(self):
        self.__valve_count = int(utils.get_setting('valves/count'))
        self.__gpios = self.__parse_gpios()
        GPIO.setmode(GPIO.BCM)
        for gpio in self.__gpios:
            GPIO.setup(gpio, GPIO.OUT)
            GPIO.output(gpio, GPIO.HIGH)
        LOG.info("Valve Manager initialized!")
            
    def turn_on_by_number(self, number: int, userId = None):
        if number >= self.__valve_count: 
            LOG.err("Invalid valve number [{}]!".format(number))
            return
        GPIO.output(self.__gpios[number], GPIO.LOW)

        if userId != None:
            payload = {}
            payload['valveId'] = number
            payload['action'] = "TURN_ON"
            payload['userId'] = userId
            payload['timestamp'] = time.time()

            mongo_client.insert_one(payload, utils.get_setting("mongo/collections/valves"))

    def turn_off_by_number(self, number: int, userId = None):
        if number >= self.__valve_count: 
            LOG.err("Invalid valve number [{}]!".format(number))
            return
        GPIO.output(self.__gpios[number], GPIO.HIGH)

        if userId != None:
            payload = {}
            payload['valveId'] = number
            payload['action'] = "TURN_OFF"
            payload['userId'] = userId
            payload['timestamp'] = time.time()

            mongo_client.insert_one(payload, utils.get_setting("mongo/collections/valves"))

    def get_count(self):
        return self.__valve_count

    def get_status(self):
        states = []
        for gpio in self.__gpios:
            state = {}
            state['valveId'] = self.__gpios.index(gpio)
            input = GPIO.input(gpio)
            if input == 1:
                state['state'] = "OFF"
            else:
                state['state'] = "ON"
            states.append(state)
        return json.dumps(states)
        
    def terminate(self):
        LOG.info("Valves Manager terminate!")
        GPIO.cleanup()

    def __valves_cycle(self, secs):        
        LOG.info("Start valves cycle with {} minutes interval!".format(secs / 60))
        admin_id = mongo_client.admin_user_id()
        self.turn_off_all()
        for i in range(self.get_count()):
            self.turn_on_by_number(i, admin_id)
            timeout = secs
            while timeout >= 0:
                timeout -= 1
                time.sleep(1)
                if not self.__cycle_thread_running:
                    self.turn_off_by_number(i, admin_id)
                    LOG.info("Valves cycle interrupted!")
                    return
            self.turn_off_by_number(i, admin_id)
        LOG.info("Valves cycle finished!")
        self.__cycle_thread_running = False

    def start_valves_cycle(self, secs):
        self.__cycle_thread = threading.Thread(target=self.__valves_cycle, daemon=True, args=[secs])
        self.__cycle_thread_running = True
        self.__cycle_thread.start()

    def stop_valves_cycle(self):
        self.__cycle_thread_running = False
        if hasattr(self, '__cycle_thread'):
            self.__cycle_thread.join()
            self.turn_off_all(mongo_client.admin_user_id())

    def turn_off_all(self, userId = None):
        for i in range(self.get_count()):
            self.turn_off_by_number(i, userId)

    def __parse_gpios(self):
        gpios_str = str(utils.get_setting('valves/gpios'))
        if gpios_str == "":
            return []
        else:
            str_array = gpios_str.split(",")
            int_array = [int(x) for x in str_array]
            return int_array

    def __del__(self):
        self.terminate()

valve_manager = ValveManager()