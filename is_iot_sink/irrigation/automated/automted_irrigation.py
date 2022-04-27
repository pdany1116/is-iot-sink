from is_iot_sink.irrigation.irrigation import *
from is_iot_sink.irrigation.mode import *
from is_iot_sink.irrigation.automated.flc import *
from is_iot_sink.irrigation.valves.valves_manager import valve_manager
from is_iot_sink.irrigation.weather import *
from is_iot_sink.mongodb.mongodb_client import mongo_client
import time

RAIN_PROB_THRESHOLD = 75
RAIN_FAIL_COUNTER_THRESHOLD = 4
SOIL_ABSORTION_TIMEOUT = 60 * 60   # seconds
RECHECK_TIMEOUT = 15 * 60          # seconds

class AutomatedIrrigation(Irrigation):
    def __init__(self):
        super().__init__()
        self.mode = Mode.AUTO
        self.flc = FLC()
        self.weather = Weather(utils.get_setting("location/latitude"), utils.get_setting("location/longitude"))
        self.rain_fail_counter = 0

    def run(self):
        while True:
            readings = mongo_client.read_last_readings()
            data = self.__calculate_average(readings)
            irrigation_time = self.flc.solve(
                data['soilMoisture'],
                data['airTemperature'],
                data['airHumidity'],
                data['lightIntensity']
            )
            if irrigation_time == 0:
                time.sleep(RECHECK_TIMEOUT)
                continue

            if (self.__rain_probability() < RAIN_PROB_THRESHOLD or
                self.rain_fail_counter >= RAIN_FAIL_COUNTER_THRESHOLD):
                self.rain_fail_counter = 0
                valve_manager.turn_on_all_by_time(irrigation_time)
            else:
                self.rain_fail_counter += 1
                time.sleep(RECHECK_TIMEOUT)
                continue
            
            time.sleep(SOIL_ABSORTION_TIMEOUT)

    def __calculate_average(self, readings):
        data = {
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
            data['soilMoisture'] += avg

            # Air Temperature
            data['airTemperature'] += float(reading['airTemperature'])

            # Air Humidity
            data['airHumidity'] += float(reading['airHumidity'])

            # Light Intensity
            #data['lightIntensity'] += float(reading['lightIntensity'])

        data['soilMoisture'] /= len(readings)
        data['airTemperature'] /= len(readings)
        data['airHumidity'] /= len(readings)
        #data['lightIntensity'] /= len(readings)

        return data

    def __rain_probability(self):
        return self.weather.get_1hour_data()[0]["RainProbability"]
