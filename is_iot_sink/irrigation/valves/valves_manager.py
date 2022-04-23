import json
import RPi.GPIO as GPIO
import utils
from is_iot_sink.logger import LOG

class ValveManager:
    def __init__(self):
        self.__valve_count = int(utils.get_setting('valves/count'))
        self.__gpios = self.__parse_gpios()
        GPIO.setmode(GPIO.BCM)
        for gpio in self.__gpios:
            GPIO.setup(gpio, GPIO.OUT)
            GPIO.output(gpio, GPIO.HIGH)
            
    def turn_on_valve_by_number(self, number: int):
        if number >= self.__valve_count: 
            LOG.err("Invalid valve number [{}]!".format(number))
            return
        GPIO.output(self.__gpios[number], GPIO.LOW)

    def turn_off_valve_by_number(self, number: int):
        if number >= self.__valve_count: 
            LOG.err("Invalid valve number [{}]!".format(number))
            return
        GPIO.output(self.__gpios[number], GPIO.HIGH)

    def turn_on_valve_by_gpio(self, gpio: int):        
        if gpio not in self.__gpios: 
            LOG.err("Gpio [{}] it's not connected to a valve!".format(gpio))
            return
        GPIO.output(gpio, GPIO.LOW)

    def turn_off_valve_by_gpio(self, gpio: int):
        if gpio not in self.__gpios: 
            LOG.err("Gpio [{}] it's not connected to a valve!".format(gpio))
            return
        GPIO.output(gpio, GPIO.HIGH)

    def get_valves_count(self):
        return self.__valve_count

    def get_valves_status(self):
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