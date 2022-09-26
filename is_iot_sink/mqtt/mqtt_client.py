import queue
import os
import paho.mqtt.client as mqtt
from is_iot_sink.logger import LOG
from is_iot_sink.settings import Settings

class MQTTClient:
    def __init__(self, settings: Settings):
        self.__settings = settings
        self.__name = self.__settings.get("name")
        self.__host = os.getenv('MQTT_HOST')
        self.__port = int(self.__settings.get("mqtt/port"))
        self.__qos = int(self.__settings.get("mqtt/qos"))
        self.__auth = self.__settings.get("mqtt/auth")
        self.__registrationTopic = self.__settings.get("mqtt/topics/collector/registration")
        self.__dataTopic = self.__settings.get("mqtt/topics/collector/data")
        self.__valvesTopic = self.__settings.get("mqtt/topics/valves/control")
        self.__valvesStatusRequestTopic = self.__settings.get("mqtt/topics/valves/request")
        self.__irrigationModeTopic = self.__settings.get("mqtt/topics/irrigation/mode")
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
            self.__client.connect(self.__host, self.__port)

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
