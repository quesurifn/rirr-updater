import os
from pymongo import MongoClient


class Mongo:
    def __init__(self):
        mongo_host = os.getenv('MONGO_HOST') or "localhost"
        mongo_port = os.getenv("MONGO_PORT") or 21707
        mongo_database = os.getenv("MONGO_DB") or "ipinfo"
        self.db = MongoClient(mongo_host, mongo_port)[mongo_database]

    def insert(self, obj):
        return self.db[obj.get_collection_name()].insert_one(vars(obj)).inserted_id

    def upsert(self, filter, obj):
        return self.db[obj.get_collection_name()].update_one(filter, {"$set": obj}, upsert=True)

    def query(self, col: str, query: dict, limit: int, offset: int):
        return self.db[col].find(query).limit(limit).skip(offset)
