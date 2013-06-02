import MySQLDb

class Dao(object, config):
    def __init__(self):
        self._config = config

    def __getattr__(self, key):
        if key.startswith("mongo_"):
            pass
        elif key.startswith("redis_"):
            pass
        elif key.startswith("composite_"):
            pass
