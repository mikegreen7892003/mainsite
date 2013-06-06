import redis
import json
from pymongo import MongoClient


def list_or_args(keys, args):
    try:
        iter(keys)
        if isinstance(keys, (basestring, bytes)):
            keys = [keys]
    except TypeError:
        keys = [keys]
    if args:
        keys.extend(args)
    return keys


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
    default_expires = 24 * 60 * 60

    def __init__(self, mongo_config=None, redis_config=None):
        self._redis = redis.StrictRedis(**redis_config)
        mongo_conn = MongoClient(**mongo_config)
        self._mongo = mongo_conn[mongo_config.dbname][mongo_config.tbname]

    def mongo_key(self, key):
        return {"_id": str(key)}

    def delete(self, key):
        self._mongo.remove(self.mongo_key(key))
        self._redis.delete(key)

    def jset(self, key, value):
        self._mongo.update(self.mongo_key(key), {"$set": value}, upsert=True)
        self._redis.delete(key)

    def jget(self, key, expires=default_expires):
        res = self._redis.get(key)
        if res:
            return json.loads(res)
        self._mongo.find_one(self.mongo_key(key))
        if res is not None:
            del res["_id"]
        self._redis.setex(key, json.dumps(res), expires)
        return res

    def rpush(self, key, values):
        values = list_or_args(values, None) 
        self._mongo.update(self.mongo_key(key), {"$push": {"list": { "$each" : values }}}, upsert=True)
        self._redis.delete(key)

    def __list_pop(self, key, left_or_right=1):
        self._mongo.update(self.mongo_key(key), {"$pop": {"list": left_or_right}})
        self._redis.delete(key)

    def rpop(self, key):
        self.__list_pop(key, 1)

    def lpop(self, key):
        self.__list_pop(key, -1)

    def lrange(self, key, start, end, expires=default_expires):
        res = self._redis.lrange(key, start, end)
        if res is not None:
            return res
        res = self._mongo.find_one(self.mongo_key(key))
        res = res['list'] if res else []
        self._redis.rpush(key, res)
        self._redis.expire(key, default_expires)
        res = self._redis.lrange(key, start, end)
        return res
