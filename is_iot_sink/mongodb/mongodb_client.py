from is_iot_sink import utils
from is_iot_sink.logger import LOG
from is_iot_sink.allowed_collectors import ac
import pymongo
import os

class MongoClient:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGODB_CONNECTION_STR'))
        self.db = self.client[utils.get_setting("mongo/db")]
        self.cols = utils.get_settings("mongo/collections")

    def insert_one(self, doc, collection: str):
        col = self.db[collection]
        x = col.insert_one(doc)

    def read_last_readings(self):
        col = self.db["readings"]
        last_readings = []
        for id in ac.get_all():
            pipeline = [
                {
                    '$match': {
                        'collectorId': id,
                        'soilMoisture': {
                            '$exists': 1
                        },
                        'airHummidity': {
                            '$exists': 1
                        },
                        'airTemperature': {
                            '$exists': 1
                        }
                        #,
                        #'lightIntensity': {
                        #    '$exists': 1
                        #}
                    }
                }, {
                    '$sort': {
                        'timestamp': -1
                    }
                }, {
                    '$limit': 1
                }
            ]
            readings = col.aggregate(pipeline)
            for reading in readings:
                last_readings.append(reading)

        return last_readings

    def __del__(self):
        self.client.close()

mongo_client = MongoClient()
