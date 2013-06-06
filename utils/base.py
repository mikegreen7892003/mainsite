from utils.config import Config
from utils.dao import Dao


class Base(object):
    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)

    def initialize(self, *args, **kwargs):
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

    @staticmethod
    def getDao():
        assert Base.installed()
        return Base.dao

    @staticmethod
    def getConfig():
        assert Base.installed()
        return Base.config
