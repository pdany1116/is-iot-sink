import os
import json
import paho.mqtt.client as mqttclient

class CollectorMock:
    def __init__(self, id, settings):
        self.__settings = settings
        self.__host = os.getenv('MQTT_HOST')
        self.__port = self.__settings.get("mqtt/port")
        self.__qos = self.__settings.get("mqtt/qos")
        self.__auth = self.__settings.get("mqtt/auth")
        self.__id = id
        self.__client = mqttclient.Client("collector" + self.__id)

        if self.__auth.lower() == "on":
            self.__client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        self.__client.connect(self.__host, self.__port)
        self.__client.loop_start()

    def connect(self):
        if not self.__client.is_connected():
            self.__client.connect(self.__host, self.__port)

    def publish(self, topic: str, message: str):
        self.connect()
        self.__client.publish(topic, message, self.__qos)

    def register(self, topic):
        register_message = json.dumps({'collectorId' : self.__id})
        self.publish(topic, register_message)

    def send_dummy_data(self, topic):
        self.publish(topic, self.__dummy_data())

    def __dummy_data(self):
        return json.dumps(
            {
                "collectorId": self.__id,
                "soilMoisture": [
                    50,
                    50
                ],
                "timestamp": 1696969420,
                "airTemperature": 10,
                "airHumidity": 50,
                "lightIntensity": 50
            })
