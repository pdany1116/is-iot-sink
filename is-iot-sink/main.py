import utils
import weather
import mqtt_client
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
__sub = mqtt_client.MQTTClient()
__sub.attach_queue(__queue_head)
__vm = valves_manager.ValveManager()
__mongo_client = mongodb_client.MongoClient()

def process_data(): 
    while True:
        message = __queue_head.get()
        __queue_head.task_done()
        # For now just log the incoming messages
        payload = str(message.payload.decode("utf-8"))
        LOG.info("<{}> [{}]".format(message.topic, payload))

        if (message.topic == utils.get_setting("mqtt/topics/registration")):
            __sub.subscribe(payload)
            LOG.info("Succesfully subscribed to [{}]".format(payload))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/collectedData"))):
            if(utils.check_json_format(payload) == False):
                LOG.err("Invalid json format! [{}]".format(payload))
                continue
            # TODO: check last readings before inserting data
            __mongo_client.insert_one(json.loads(payload), utils.get_setting("mongo/collections/readings"))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/control"))):
            try:
                data = json.loads(payload)
                valve = data['valveId']
                action = data['action'].upper()
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
            __mongo_client.insert_one(data, utils.get_setting("mongo/collections/valves"))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/request"))):
            __sub.publish(utils.get_setting("mqtt/topics/valves/response"), __vm.get_valves_status())
        
        else:
            LOG.err("Unwanted: <{}> [{}]".format(message.topic, payload))

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
