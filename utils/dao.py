import asyncmongo
import tornadoredis

class Dao(object, config):
    def __init__(self):
        self._config = config

    def __getattr__(self, key):
        if key.startswith("mongo_"):
            mongo_config = self._config[key]
            db = asyncmongo.Client(**mongo_config)
        elif key.startswith("redis_"):
            tornadoredis.ConnectionPool(max_connections=500,wait_for_available=True)
            pass
        elif key.startswith("composite_"):
            pass
        setattr(self, key, db)
        return db
