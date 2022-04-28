from is_iot_sink.mqtt.mqtt_client import mqtt_client
from is_iot_sink.irrigation.valves.valves_manager import valve_manager
from is_iot_sink.mongodb.mongodb_client import mongo_client
from is_iot_sink.allowed_collectors import ac
from is_iot_sink.irrigation.irrigation_factory import *
from logger import LOG
import is_iot_sink.irrigation.mode as irr_mode
import queue
import threading
import signal
import sys
import json
import utils
import time

queue_head = queue.Queue(maxsize = 0)
irrigation = IrrigationFactory().create(irr_mode.initial_mode())

def process_data(): 
    global irrigation
    while True:
        message = queue_head.get()
        queue_head.task_done()
        
        ac.check_all()

        try:
            payload = json.loads(str(message.payload.decode("utf-8")))
        except:
            LOG.err("Invalid json format! [{}]".format(message.payload))
            continue

        LOG.info("<{}> [{}]".format(message.topic, payload))
        
        if (message.topic == utils.get_setting("mqtt/topics/collector/registration")):
            ac.add(payload["collectorId"])
            LOG.info("Collector [{}] accepted.".format(payload["collectorId"]))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/collector/data"))):
            if ac.is_allowed(payload["collectorId"]):
                # TODO: check last readings before inserting data
                # TODO: validate fields 
                mongo_client.insert_one(payload, utils.get_setting("mongo/collections/readings"))
            else:
                LOG.err("Unaccepted collector with id: {}".format(payload["collectorId"]))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/control"))):
            if irrigation.mode == irr_mode.Mode.AUTO:
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
            
            payload['timestamp'] = time.time()

            # TODO: check user integrity
            mongo_client.insert_one(payload, utils.get_setting("mongo/collections/valves"))

        elif (message.topic.startswith(utils.get_setting("mqtt/topics/valves/request"))):
            mqtt_client.publish(utils.get_setting("mqtt/topics/valves/response"), valve_manager.get_status())
        
        elif (message.topic.startswith(utils.get_setting("mqtt/topics/irrigation/mode"))):
            new_mode = irr_mode.str_to_mode(payload["mode"].upper())
            if (new_mode == None):
                LOG.err("Invalid irrigation mode configuration!")
                continue

            if (new_mode == irrigation.mode):
                LOG.info("Irrigation mode is already: [{}]".format(irr_mode.mode_to_str(irrigation.mode)))
            else:
                LOG.info("Irrigation mode switched to: [{}]".format(payload["mode"].upper()))
                irrigation.stop()
                irrigation = IrrigationFactory().create(new_mode)
                irrigation.start()

        else:
            LOG.err("Unwanted: <{}> [{}]".format(message.topic, message.payload))

def signal_handler(sig, frame):
    LOG.info("SIGINT received!")
    terminate()

def main():
    signal.signal(signal.SIGINT, signal_handler)
    irrigation.start()
    mqtt_client.attach_queue(queue_head)
    process_data_thread = threading.Thread(target=process_data, daemon=True)
    process_data_thread.start()
    process_data_thread.join()
    terminate()

def terminate():
    valve_manager.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()
