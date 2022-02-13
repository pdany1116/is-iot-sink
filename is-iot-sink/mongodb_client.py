import utils
from logger import LOG
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

    def __del__(self):
        self.client.close()