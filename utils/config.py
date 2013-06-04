from tornado.util import ObjectDict
from tornado.options import options


class Config(object):
    def __init__(self):
        self._config_type = options.config_type
        getattr(self, "%sConfig" % (self._config_type,))()

    def devConfig(self):
        #self.db_mysql_comics = ObjectDict(dict(
        #    host="localhost:3306",
        #    user="root",
        #    password="",
        #    db="comicsOffline",
        #))
        self.db_mongo_comics = ObjectDict(dict(
            host="localhost",
            port=27017,
            max_pool_size=10,
        ))
        self.db_redis_comics = ObjectDict(dict(
            host="localhost",
            port=6379,
            db=0,
        ))
        self.db_composite_comics = ObjectDict(dict(
            mongo_config=ObjectDict(dict(
                self.db_mongo_comics,
                dbname="comics",
                tbname="redis0",
            )),
            redis_config=self.db_redis_comics,
        ))

    def productConfig(self):
        raise NotImplementedError()
