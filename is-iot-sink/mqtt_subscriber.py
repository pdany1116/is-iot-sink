import utils
import queue
import paho.mqtt.client as mqtt
from logger import LOG

class MQTTSubscriber:
    def __init__(self, queue_head : queue.Queue):
        self.__host = utils.getSetting("host")
        self.__name = utils.getSetting("name")
        self.__queue_head = queue_head
        self.__registrationTopic = utils.getSetting("registrationTopic")
        self.__collectedDataTopic = utils.getSetting("collectedDataTopic")
        self.__valveTopic = utils.getSetting("valveTopic")
        self.__client = mqtt.Client(self.__name)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        #TODO: use authentication

        try:
            self.__client.connect(self.__host)
            
            self.__client.subscribe(self.__registrationTopic)
            self.__client.subscribe(self.__collectedDataTopic)
            self.__client.subscribe(self.__valveTopic + "#")
            
            self.__client.loop_start()
        except Exception as ex:
            LOG.err("MQTT Client failed to start!")

    def disconnect(self):
        self.__client.disconnect()

    def subscribe(self, topic:str):
        self.__client.subscribe(topic)

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
 