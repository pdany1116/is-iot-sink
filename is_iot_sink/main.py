import utils
import weather
from is_iot_sink.mqtt.mqtt_client import *
from is_iot_sink.irrigation.valves.valves_manager import valve_manager
import is_iot_sink.irrigation.mode as irrig_mode
from is_iot_sink.mongodb.mongodb_client import *
from is_iot_sink.allowed_collectors import *
from logger import LOG
import queue
import threading
import signal
import sys
import json

__queue_head = queue.Queue(maxsize = 0)
__sub = MQTTClient()
__sub.attach_queue(__queue_head)
__mongo_client = MongoClient()
__ac = AllowedCollectors()
__mode = irrig_mode.initial_mode()

def process_data(): 
    global __mode
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
            if __mode == irrig_mode.Mode.AUTO:
                LOG.info("Irrigation is in auto mode. Ignoring all valves control...")
                continue
            
            try:
                valve = payload['valveId']
                action = payload['action'].upper()
                if (action == "TURN_ON"):
                    valve_manager.turn_on_by_number(valve)
                elif (action == "TURN_OFF"):
                    valve_manager.turn_off_by_number(valve)
                else:
                    LOG.err("Invalid valve action request! [{}]".format(action))
                    continue
            except:
                LOG.err("Invalid format for valve control request!")
                continue
            
            # TODO: check user integrity
            __mongo_client.insert_one(payload, utils.get_setting("mongo/collections/valves"))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/request"))):
            __sub.publish(utils.get_setting("mqtt/topics/valves/response"), valve_manager.get_status())
        
        elif (message.topic.startswith(utils.get_setting("mqtt/topics/irrigation/mode"))):
            new_mode = irrig_mode.str_to_mode(payload["mode"].upper())
            if (new_mode == None):
                LOG.err("Invalid irrigation mode configuration!")
                continue

            if (new_mode == __mode):
                LOG.info("Irrigation mode is already: [{}]".format(irrig_mode.mode_to_str(__mode)))
            else:
                __mode = new_mode
                LOG.info("Irrigation mode switched to: [{}]".format(payload["mode"].upper()))

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
    valve_manager.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()
