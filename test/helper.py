import subprocess
import os
from dotenv import Dotenv
from pathlib import Path
from is_iot_sink.settings import Settings
from is_iot_sink.mongodb.mongodb_client import MongoClient
from threading import Lock

class TestHelper:
    @classmethod
    def suite_setup(self):
        self.set_environment_variables()
        self.__start_local_mqtt_broker()

    @classmethod
    def suite_teardown(self):
        self.__stop_local_mqtt_broker()

    @classmethod
    def test_setup(self):
        pass

    @classmethod
    def test_teardown(self):
        pass

    @classmethod
    def __start_local_mqtt_broker(self):
        subprocess.run('sudo service mosquitto start'.split(), stdout=subprocess.DEVNULL)

    @classmethod
    def __stop_local_mqtt_broker(self):
        subprocess.run('sudo service mosquitto stop'.split(), stdout=subprocess.DEVNULL)

    @classmethod
    def set_environment_variables(self):
        env_file_path = Path(os.getenv('PROJECT_PATH') + '/.env.test')
        dotenv = Dotenv(env_file_path)
        os.environ.update(dotenv)

    @classmethod
    def default_test_settings(self):
        self.__settings_mutex = Lock()
        return Settings(os.getenv('PROJECT_PATH') + '/setup_test.yml', self.__settings_mutex)

    @classmethod
    def cleanup_database(self, settings: Settings):
        MongoClient(settings).cleanup()
