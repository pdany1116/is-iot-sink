import utils
import weather
import mqtt_subscriber
import queue
import threading
from logger import LOG

__queue_head = queue.Queue(maxsize=0)
__sub = mqtt_subscriber.MQTTSubscriber(__queue_head)

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

def main():
    w = weather.Weather(utils.getSetting('latitude'), utils.getSetting('longitude'))
    t = threading.Thread(target=process_data)
    t.setDaemon(True)
    t.start()
    t.join()

if __name__ == "__main__":
    main()
