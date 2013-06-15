from config import Config
from dao import Dao


class Base(object):
    def __init__(self):
        pass

    @staticmethod
    def installed():
        return hasattr(Base, "dao") and hasattr(Base, "config")

    @classmethod
    def install(cls, config_class=None):
        assert not Base.installed()
        config_class = config_class or Config
        cls.config = config_class()
        cls.dao = Dao(cls.config)
