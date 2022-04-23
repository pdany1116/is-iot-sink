import utils
import weather
from is_iot_sink.mqtt.mqtt_client import *
from is_iot_sink.irrigation.valves.valves_manager import *
from is_iot_sink.mongodb.mongodb_client import *
from logger import LOG
import utils
import queue
import threading
import signal
import sys
import json
import allowed_collectors

__queue_head = queue.Queue(maxsize = 0)
__sub = MQTTClient()
__sub.attach_queue(__queue_head)
__vm = ValveManager()
__mongo_client = MongoClient()
__ac = allowed_collectors.AllowedCollectors()

def process_data(): 
    while True:
        message = __queue_head.get()
        __queue_head.task_done()

        __ac.check_all()

        try:
            payload = json.loads(str(message.payload.decode("utf-8")))
        except:
            LOG.err("Invalid json format! [{}]".format(message.payload))
            continue

        LOG.info("<{}> [{}]".format(message.topic, payload))
        
        if (message.topic == utils.get_setting("mqtt/topics/collector/registration")):
            __ac.add(payload["collectorId"])
            LOG.info("Collector [{}] accepted.".format(payload["collectorId"]))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/collector/data"))):
            if __ac.is_allowed(payload["collectorId"]):
                # TODO: check last readings before inserting data
                # TODO: validate fields 
                __mongo_client.insert_one(payload, utils.get_setting("mongo/collections/readings"))
            else:
                LOG.err("Unaccepted collector with id: {}".format(payload["collectorId"]))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/control"))):
            try:
                valve = payload['valveId']
                action = payload['action'].upper()
                if (action == "TURN_ON"):
                    __vm.turn_on_valve_by_number(valve)
                elif (action == "TURN_OFF"):
                    __vm.turn_off_valve_by_number(valve)
                else:
                    LOG.err("Invalid valve action request! [{}]".format(action))
                    continue
            except:
                LOG.err("Invalid format for valve control request!")
                continue
            
            # TODO: check user integrity
            __mongo_client.insert_one(payload, utils.get_setting("mongo/collections/valves"))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/request"))):
            __sub.publish(utils.get_setting("mqtt/topics/valves/response"), __vm.get_valves_status())
        
        else:
            LOG.err("Unwanted: <{}> [{}]".format(message.topic, message.payload))

def signal_handler(sig, frame):
    LOG.info("SIGINT received!")
    terminate()

def main():
    signal.signal(signal.SIGINT, signal_handler)
    w = weather.Weather(utils.get_setting('location/latitude'), utils.get_setting('location/longitude'))
    t = threading.Thread(target=process_data)
    t.setDaemon(True)
    t.start()
    t.join()
    terminate()

def terminate():
    __vm.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()
