from is_iot_sink import utils
import queue
import os
import paho.mqtt.client as mqtt
from is_iot_sink.logger import LOG

class MQTTClient:
    def __init__(self):
        self.__name = utils.get_setting("name")
        self.__host = os.getenv('MQTT_HOST')
        self.__port = int(utils.get_setting("mqtt/port"))
        self.__qos = int(utils.get_setting("mqtt/qos"))
        self.__auth = utils.get_setting("mqtt/auth")
        self.__registrationTopic = utils.get_setting("mqtt/topics/collector/registration")
        self.__dataTopic = utils.get_setting("mqtt/topics/collector/data")
        self.__valvesTopic = utils.get_setting("mqtt/topics/valves/control")
        self.__valvesStatusRequestTopic = utils.get_setting("mqtt/topics/valves/request")
        self.__irrigationModeTopic = utils.get_setting("mqtt/topics/irrigation/mode")
        self.__client = mqtt.Client(self.__name)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
            
        if self.__auth.lower() == "on":
            self.__client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        try:
            self.__client.connect(self.__host, self.__port)
            self.subscribe(self.__registrationTopic)
            self.subscribe(self.__dataTopic)
            self.subscribe(self.__valvesTopic)
            self.subscribe(self.__valvesStatusRequestTopic)
            self.subscribe(self.__irrigationModeTopic)
            self.__client.loop_start()
        except Exception as ex:
            LOG.err("MQTT Client failed to start! : {}".format(ex))

    def connect(self):
        if not self.__client.is_connected():
            self.__client.connect(self.__host)

    def disconnect(self):
        self.__client.disconnect()

    def attach_queue(self, queue_head: queue.Queue):
        self.__queue_head = queue_head

    def subscribe(self, topic: str):
        self.__client.subscribe(topic, self.__qos)

    def publish(self, topic: str, message: str):
        try:
            self.connect()
        except Exception:
            LOG.err("MQTT Client faild to connect!")
            return

        try:
            self.__client.publish(topic, message, self.__qos)
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

mqtt_client = MQTTClient()
