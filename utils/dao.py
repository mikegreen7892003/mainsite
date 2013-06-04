import redis
import threading
import json
from pymongo import MongoClient


class Dao(object):
    def __init__(self, config):
        self._config = config

    def __getattr__(self, key):
        if key.startswith("mongo_"):
            impl = MongoClient
        elif key.startswith("redis_"):
            impl = redis.StrictRedis
        elif key.startswith("composite_"):
            impl = CompositeDB
        else:
            super(Dao, self).__getattribute__(key)
        db = impl(**getattr(self._config, "db_%s" % key))
        setattr(self, key, db)
        return db


class CompositeDB(object):
    def __init__(self, mongo_config=None, redis_config=None):
        self._redis = redis.StrictRedis(**redis_config)
        mongo_conn = MongoClient(**mongo_config)
        self._mongo = mongo_conn[mongo_config.dbname][mongo_config.tbname]

    def mongo_key(self, key):
        return {"_id": str(key)}

    def jset(self, key, value):
        self._mongo.update(self.mongo_key(key), {"$set": value}, upsert=True)
        self._redis.delete(key)

    def jget(self, key, expires=600):
        res = self._redis.get(key)
        if res:
            return json.loads(res)
        self._mongo.redis.find_one(self.mongo_key(key))
        if res is not None:
            del res["_id"]
        self._redis.setex(key, json.dumps(res), expires)
        return res

    def jdel(self, key):
        self._mongo.remove(self.mongo_key(key))
        self._redis.delete(key)

    def rpush(self, key, value):
        self._mongo.update(self.mongo_key(key), {"$push": {"list": str(value)}}, upsert=True)
        self._redis.delete(key)

    def __list_pop(self, key, left_or_right=1):
        self._mongo.update(self.mongo_key(key), {"$push": {"list": left_or_right}})
        self._redis.delete(key)

    def rpop(self, key):
        self.__list_pop(key, 1)

    def lpop(self, key):
        self.__list_pop(key, -1)
