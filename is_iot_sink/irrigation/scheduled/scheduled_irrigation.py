from is_iot_sink.allowed_collectors import AllowedCollectors
from is_iot_sink.irrigation.irrigation_mode import *
from is_iot_sink.irrigation.automated.flc import flc
from is_iot_sink.irrigation.valves.valves_manager import ValveManager
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.settings import Settings
from is_iot_sink.logger import LOG
import time
import threading


class ScheduledIrrigation:
    def __init__(self, settings: Settings, valve_manager: ValveManager, mongo_client: MongoClient, allowed_collectors: AllowedCollectors):
        super().__init__()
        self.__settings = settings
        self.__valve_manager = valve_manager
        self.__mongo_client = mongo_client
        self.__allowed_collectors = allowed_collectors
        self.mode = IrrigationMode.SCHEDULED
        self.running = False
        self.thread = threading.Thread(target=self.__run, daemon=True)

    def start(self):
        LOG.info("Scheduled Irrigation process started.")
        self.running = True
        self.thread.start()

    def stop(self):
        LOG.info("Scheduled Irrigation process stopped.")
        self.running = False
        self.thread.join()

    def __run(self):

        while self.running:
            self.__mongo_client.read_first_appointment()

        return

    def __sleep(self, secs):
        while secs >= 0:
            secs -= 1
            time.sleep(1)
            if not self.running:
                return False
        return True


    def __insert_irrigation(self, irrigation_time, rain_probability):
        data = {}
        data['irrigationTime'] = irrigation_time
        data['rainProbability'] = rain_probability
        data['completed'] = False
        data['timestamp'] = time.time()

        return self.__mongo_client.insert_one(data, "irrigations")

    def __update_irrigation(self, inserted_id):
        self.__mongo_client.update_finished_irrigation(inserted_id)
