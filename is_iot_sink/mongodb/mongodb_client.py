from bson import ObjectId
from is_iot_sink import utils
from is_iot_sink.logger import LOG
from is_iot_sink.allowed_collectors import ac
import pymongo
import os
import time

class MongoClient:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGODB_CONNECTION_STR'))
        self.db = self.client[utils.get_setting("mongo/db")]
        self.cols = utils.get_settings("mongo/collections")

    def insert_one(self, doc, collection: str):
        col = self.db[collection]
        result = col.insert_one(doc)
        return result.inserted_id

    def update_finished_irrigation(self, id):
        col = self.db[utils.get_setting("mongo/collections/irrigations")]
        result = col.update_one({'_id': ObjectId(id)}, {'$set': {'completed': True}})

    def admin_user_id(self):
        col = self.db[utils.get_setting("mongo/collections/users")]
        user = col.find_one({'UserName': 'admin'})
        return user['_id']

    def read_last_readings(self):
        col = self.db[utils.get_setting("mongo/collections/readings")]

        last_readings = []
        for id in ac.get_all():
            pipeline = [
                {
                    '$match': {
                        'collectorId': id,
                        'soilMoisture': {
                            '$exists': 1
                        },
                        'airHumidity': {
                            '$exists': 1
                        },
                        'airTemperature': {
                            '$exists': 1
                        }
                        ,
                        'lightIntensity': {
                            '$exists': 1
                        }
                    }
                }, {
                    '$sort': {
                        'timestamp': -1
                    }
                }, {
                    '$limit': int(utils.get_setting("irrigation/automated/last_readings_count"))
                }
            ]
            readings = col.aggregate(pipeline)
            for reading in readings:
                last_readings.append(reading)

        return last_readings

    def __del__(self):
        self.client.close()

mongo_client = MongoClient()
