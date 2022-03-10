import utils
import queue
import paho.mqtt.client as mqtt
from logger import LOG

class MQTTClient:
    def __init__(self):
        self.__host = utils.get_setting("mqtt/host")
        self.__name = utils.get_setting("name")
        self.__registrationTopic = utils.get_setting("mqtt/topics/registration")
        self.__collectedDataTopic = utils.get_setting("mqtt/topics/collectedData")
        self.__valvesTopic = utils.get_setting("mqtt/topics/valves/control")
        self.__valvesStatusRequest = utils.get_setting("mqtt/topics/valves/request")
        self.__client = mqtt.Client(self.__name)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        #TODO: use authentication

        try:
            self.__client.connect(self.__host)
            self.subscribe(self.__registrationTopic)
            self.subscribe(self.__collectedDataTopic)
            self.subscribe(self.__valvesTopic)
            self.subscribe(self.__valvesStatusRequest)
            self.__client.loop_start()
        except Exception as ex:
            LOG.err("MQTT Client failed to start! : {}".format(ex))

    def disconnect(self):
        self.__client.disconnect()

    def attach_queue(self, queue_head: queue.Queue):
        self.__queue_head = queue_head

    def subscribe(self, topic: str):
        self.__client.subscribe(topic)

    def publish(self, topic: str, message: str):
        try:
            #self.__client.connect(self.__host)
            self.__client.publish(topic, message)
        except Exception as ex:
            LOG.err("MQTT Publisher Client failed to publish!")

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to connect! Error code = {}".format(rc))
        else:
            LOG.info("MQTT Client connected successfully!")

    def __on_disconnect(self, client, userdata, rc):
        self.__client.loop_stop()
        if rc != 0:
            LOG.err("MQTT Client failed to disconnect! Error code = {}".format(rc))
        else:
            LOG.info("MQTT Client disconnected successfully!")

    def __on_message(self, client, userdata, message):
        self.__queue_head.put(message)
