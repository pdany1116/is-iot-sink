import utils
import weather
import mqtt_subscriber
import valves_manager
import mongodb_client
from logger import LOG
import utils
import queue
import threading
import signal
import sys
import json

__queue_head = queue.Queue(maxsize=0)
__sub = mqtt_subscriber.MQTTSubscriber(__queue_head)
__vm = valves_manager.ValveManager()
__mongo_client = mongodb_client.MongoClient()

def process_data(): 
    while True:
        message = __queue_head.get()
        __queue_head.task_done()
        # For now just log the incoming messages
        msg = str(message.payload.decode("utf-8"))
        LOG.info("<{}> [{}]".format(message.topic, msg))

        if (message.topic == utils.get_setting("mqtt/topics/registration")):
            __sub.subscribe(msg)
            LOG.info("Succesfully subscribed to [{}]".format(msg))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/collectedData"))):
            if(utils.check_json_format(msg) == False):
                LOG.err("Invalid json format! [{}]".format(msg))
                continue
            # TODO: check last readings before inserting data
            __mongo_client.insert_one(json.loads(msg), utils.get_setting("mongo/collections/readings"))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves"))):
            valve_str = message.topic.replace(utils.get_setting("mqtt/topics/valves"), "")
            try:
                valve = int(valve_str)
            except:
                LOG.err("Invalid valve number! [{}]".format(valve_str))
                continue

            if (msg == "on"):
                __vm.turn_on_valve_by_number(valve)
            elif (msg == "off"):
                __vm.turn_off_valve_by_number(valve)
            else:
                LOG.err("Invalid valve request! [{}]".format(msg))

        else:
            LOG.err("Unwanted: <{}> [{}]".format(message.topic, msg))

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
