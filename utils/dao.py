import asyncmongo
import redis
import threading
import json


class Dao(object):

    def __init__(self, config):
        self._config = config

    def __getattr__(self, key):
        if key.startswith("mongo_"):
            impl = asyncmongo.Client
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
        self._mongo = asyncmongo.Client(**mongo_config)

    def jset(self, key, value, callback=None):
        return self._mongo.redis.update({"_id": str(key)}, {"$set": value}, upsert=True, callback)

    def jget(self, key, callback=None):
        res = self._redis.get(key)
        if res:
            return json.loads(res)
