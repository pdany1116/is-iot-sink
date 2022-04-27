from is_iot_sink.irrigation.irrigation import *
from is_iot_sink.irrigation.mode import *
from is_iot_sink.irrigation.automated.flc import flc
from is_iot_sink.irrigation.valves.valves_manager import valve_manager
from is_iot_sink.irrigation.weather import *
from is_iot_sink.mongodb.mongodb_client import mongo_client
from is_iot_sink.logger import LOG
import time
import threading

RAIN_PROB_THRESHOLD = 75
RAIN_FAIL_COUNTER_THRESHOLD = 4
SOIL_ABSORTION_TIMEOUT = 60 * 60   # seconds
RECHECK_TIMEOUT = 15 * 60          # seconds

class AutomatedIrrigation(Irrigation):
    def __init__(self):
        super().__init__()
        self.mode = Mode.AUTO
        self.weather = Weather(utils.get_setting("location/latitude"), utils.get_setting("location/longitude"))
        self.rain_fail_counter = 0
        self.running = False
        self.thread = threading.Thread(target=self.__run, daemon=True)

    def start(self):
        LOG.info("Automated Irrigation process started.")
        self.running = True
        self.thread.start()

    def stop(self):
        LOG.info("Automated Irrigation process stopped.")
        self.running = False
        self.thread.join()

    def __run(self):
        while self.running:
            try:
                readings = mongo_client.read_last_readings()
                average = self.__calculate_average(readings)
                irrigation_time = flc.solve(
                    average['soilMoisture'],
                    average['airTemperature'],
                    average['airHumidity'],
                    average['lightIntensity']
                )
                LOG.info("Calculated irrigation time: {} minutes.".format(irrigation_time))
                if irrigation_time == 0:
                    self.rain_fail_counter = 0
                    if not self.__sleep(RECHECK_TIMEOUT):
                        break
                    continue

                rain_probability = self.__rain_probability()
                LOG.info("Rain probability {}%".format(rain_probability))
                if (rain_probability < RAIN_PROB_THRESHOLD or
                    self.rain_fail_counter >= RAIN_FAIL_COUNTER_THRESHOLD):
                    self.rain_fail_counter = 0
                    valve_manager.start_valves_cycle(irrigation_time * 60)
                else:
                    self.rain_fail_counter += 1
                    LOG.info("Irrigation not started. Waiting for rain. Fail counter = {}.".format(self.rain_fail_counter))
                    if not self.__sleep(RECHECK_TIMEOUT):
                        break
                    continue
                
                if not self.__sleep(SOIL_ABSORTION_TIMEOUT):
                    break
            except Exception as e:
                LOG.err(e)
                if not self.__sleep(RECHECK_TIMEOUT):
                    break
        valve_manager.stop_valves_cycle()
        valve_manager.turn_off_all()

    def __sleep(self, secs):
        while secs != 0:
            secs -= 1
            time.sleep(1)
            if not self.running:
                return False
        return True

    def __calculate_average(self, readings):
        average = {
            'soilMoisture': 0,
            'airTemperature': 0,
            'airHumidity': 0,
            'lightIntensity': 0
        }

        for reading in readings:
            # Soil Moisture
            sum = 0
            for moisture in reading['soilMoisture']:
                sum += float(moisture)
            avg = sum / len(reading['soilMoisture'])  
            average['soilMoisture'] += avg

            # Air Temperature
            average['airTemperature'] += float(reading['airTemperature'])

            # Air Humidity
            average['airHumidity'] += float(reading['airHumidity'])

            # Light Intensity
            #data['lightIntensity'] += float(reading['lightIntensity'])

        average['soilMoisture'] /= len(readings)
        average['airTemperature'] /= len(readings)
        average['airHumidity'] /= len(readings)
        #data['lightIntensity'] /= len(readings)

        return average

    def __rain_probability(self):
        return self.weather.get_1hour_data()[0]["RainProbability"]
