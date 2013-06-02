from tornado.util import ObjectDict
from tornado.options import options


class Config(object):
    def __init__(self):
        self._config_type = options.config_type
        getattr(self, "%sConfig"%(self._config_type,))()

    def __getattr__(self, key):
        if key.startswith("db_"):
            key = "_%s"%(key,)
        return getattr(self, key)

    def devConfig(self):
        self._db_mysql_comic = ObjectDict(dict(
            host="localhost:3306",
            user="root",
            password="",
            db="offline",
        ))
        self._db_mongo_comic = ObjectDict(dict(
            host="localhost",
            port=27017,
            dbname="comic",
            maxcached=10,
            maxconnections=50,
        ))
        self._db_redis_comic = ObjectDict(dict(
            host="localhost",
            port=16000,
            db=0,
        ))

    def productConfig(self):
        raise NotImplementedError()

if __name__ == "__main__":
    pass
