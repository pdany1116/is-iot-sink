from is_iot_sink.irrigation.valves.valves_manager import ValveManager
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.allowed_collectors import AllowedCollectors
from is_iot_sink.irrigation.irrigation_factory import *
from is_iot_sink.mqtt.mqtt_client import MQTTClient
from is_iot_sink.logger import LOG
from queue import Queue, Empty
from threading import Lock
from is_iot_sink.settings import Settings
from is_iot_sink.irrigation.irrigation_mode import IrrigationMode
import threading
import json
import os

class Sink:
    def __init__(self, settings=None):
        if settings == None:
            self.__settings_mutex = Lock()
            self.__settings = Settings(os.getenv('PROJECT_PATH') + '/setup.yml', self.__settings_mutex)
        else:
            self.__settings = settings

        self.__queue_head = Queue(maxsize = 0)
        self.__running = False
        self.__mongo_client = MongoClient(self.__settings)
        self.__valve_manager = ValveManager(self.__settings, self.__mongo_client)
        self.__allowed_collectors = AllowedCollectors(self.__settings)
        self.__mqtt_client = MQTTClient(self.__settings)
        self.__mqtt_client.attach_queue(self.__queue_head)
        self.__irrigation_factory = IrrigationFactory(self.__settings, self.__valve_manager, self.__mongo_client, self.__allowed_collectors)
        self.__irrigation = self.__irrigation_factory.create(IrrigationMode.str_to_mode(self.__settings.get("irrigation/initialMode").upper()))
        self.__thread = threading.Thread(target = self.__process_data, daemon = True)

    def start(self):
        LOG.info("Sink application started.")
        self.__irrigation.start()
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False
        self.__thread.join()
        self.__valve_manager.terminate()
        LOG.info("Sink application stopped.")

    def status(self):
        return self.__running and self.__thread.is_alive()

    def __process_data(self): 
        while self.__running:
            try:
                message = self.__queue_head.get(timeout=1)
            except Empty:
                continue

            self.__queue_head.task_done()

            try:
                payload = json.loads(str(message.payload.decode("utf-8")))
            except:
                LOG.err("Invalid json format! [{}]".format(message.payload))
                continue

            # TODO: check for invalid keys

            LOG.info("<{}> [{}]".format(message.topic, payload))
            
            if (message.topic == self.__settings.get("mqtt/topics/collector/registration")):
                self.__allowed_collectors.add(payload["collectorId"])
                LOG.info("Collector [{}] accepted.".format(payload["collectorId"]))

            elif (message.topic.startswith(self.__settings.get("mqtt/topics/collector/data"))):
                if self.__allowed_collectors.is_allowed(payload["collectorId"]):
                    # TODO: check last readings before inserting data
                    # TODO: validate fields 
                    self.__mongo_client.insert_one(payload, self.__settings.get("mongo/collections/readings"))
                else:
                    LOG.err("Unaccepted collector with id: {}".format(payload["collectorId"]))

            elif (message.topic.startswith(self.__settings.get("mqtt/topics/valves/control"))):
                if self.__irrigation.mode == IrrigationMode.AUTO:
                    LOG.info("Irrigation is in auto mode. Ignoring all valves control...")
                    continue
                
                try:
                    valve = payload['valveId']
                    action = payload['action'].upper()
                    userId = payload['userId']
                    if (action == "TURN_ON"):
                        self.__valve_manager.turn_on_by_number(valve, userId)
                    elif (action == "TURN_OFF"):
                        self.__valve_manager.turn_off_by_number(valve, userId)
                    else:
                        LOG.err("Invalid valve action request! [{}]".format(action))
                        continue
                except Exception as e:
                    LOG.err("Invalid format for valve control request!")
                    continue
    
            elif (message.topic.startswith(self.__settings.get("mqtt/topics/valves/request"))):
                self.__mqtt_client.publish(self.__settings.get("mqtt/topics/valves/response"), self.__valve_manager.get_status())
            
            elif (message.topic.startswith(self.__settings.get("mqtt/topics/irrigation/mode"))):
                new_mode = IrrigationMode.str_to_mode(payload["mode"].upper())
                if (new_mode == None):
                    LOG.err("Invalid irrigation mode configuration!")
                    continue

                if (new_mode == self.__irrigation.mode):
                    LOG.info("Irrigation mode is already: [{}]".format(IrrigationMode.mode_to_str(self.__irrigation.mode)))
                else:
                    LOG.info("Irrigation mode switched to: [{}]".format(payload["mode"].upper()))
                    self.__irrigation.stop()
                    self.__irrigation = self.__irrigation_factory.create(new_mode)
                    self.__irrigation.start()

            else:
                LOG.err("Unwanted: <{}> [{}]".format(message.topic, message.payload))
