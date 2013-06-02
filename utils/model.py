from tornado.util import ObjectDict
from config import Config


class Model(object):
    @classmethod
    def initialize(cls, config_class=None):
        config_class = config_class or Config
        cls.config = config_class()


if __name__ == "__main__":
    pass
