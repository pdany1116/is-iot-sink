import utils
import weather
import mqtt_subscriber
import valves_manager
from logger import LOG
import queue
import threading
import signal
import sys


__queue_head = queue.Queue(maxsize=0)
__sub = mqtt_subscriber.MQTTSubscriber(__queue_head)
__vm = valves_manager.ValveManager()

def process_data():
    while True:
        message = __queue_head.get()
        __queue_head.task_done()
        # For now just log the incoming messages
        msg = str(message.payload.decode("utf-8"))
        LOG.info("<{}> [{}]".format(message.topic, msg))
        if (message.topic == utils.getSetting("registrationTopic")):
            __sub.subscribe(msg)
            LOG.info("Succesfully subscribed to [{}]".format(msg))
        elif (message.topic.startswith(utils.getSetting("collectedDataTopic"))):
            # TODO: upload in database
            pass
        elif (message.topic.startswith(utils.getSetting("valveTopic"))):
            valve_str = message.topic.replace(utils.getSetting("valveTopic"), "")
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
    w = weather.Weather(utils.getSetting('latitude'), utils.getSetting('longitude'))
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
