#encoding=utf-8
import time
import json
from base import Base


class Volume(Base):
    """
    meta(json): include meta_args
    image_meta(list): include image list
    """
    meta_args = ["title"]

    def initialize(self, volume_id=None):
        if volume_id is None:
            self._id = self.__getNewId()
        else:
            self._id = int(volume_id)

    def __getNewId(self):
        return self.getDao().redis_comics.incr("total_volume_id")

    def getId(self):
        return self._id

    @property
    def meta(self):
        assert hasattr(self, "_id")
        if not hasattr(self, "_meta"):
            self._meta = self.getDao().composite_comics.jget("volume:%d" % (self._id, ))
        return self._meta

    @meta.setter
    def meta(self, value):
        assert hasattr(self, "_id")
        assert set(value.keys()) >= set(meta_args)
        self._meta = value
        self.getDao().composite_comics.jset("volume:%d" % (self._id, ), self._meta)

    @property
    def image_meta(self):
        assert hasattr(self, "_id")
        if not hasattr(self, "_image_meta"):
            self._image_meta = self.getDao().composite_comics.lrange("volume:%d:pic_list" % (self._id, ), 0, -1)
        return self._image_meta

    @image_meta.setter
    def image_meta(self, values):
        assert hasattr(self, "_id")
        self._image_meta = values
        self.getDao().composite_comics.delete("volume:%d:pic_list" % (self._id, ))
        self.getDao().composite_comics.rpush("volume:%d:pic_list" % (self._id, ), values)

    def save(self, meta, image_meta):
        self.meta = meta
        self.image_meta = image_meta


class Comics(Base):
    """
    meta(json): include meta_args
    volume_list(list): include volume list
    """
    meta_args = ["create_time", "update_time", "status", "title",
        "author", "cover", "uploader", "uploader_id", "introduction"]

    def initialize(self, comics_id=None):
        if comics_id is None:
            self._id = self.__getNewId()
        else:
            self._id = int(comics_id)

    def __getNewId(self):
        return self.getDao().redis_comics.incr("total_comics_id")

    def getId(self):
        return self._id

    @property
    def meta(self):
        assert hasattr(self, "_id")
        if not hasattr(self, "_meta"):
            self._meta = self.getDao().composite_comics.jget("comics:%d" % (self._id, ))
        return self._meta

    @meta.setter
    def meta(self, value):
        assert hasattr(self, "_id")
        value["update_time"] = int(time.time())
        assert set(value.keys()) >= set(meta_args)
        self._meta = value
        self.getDao().composite_comics.jset("comics:%d" % (self._id, ), self._meta)

    @property
    def volume_list(self):
        volume_ids = self.getDao().composite_comics.lrange("comics:%d:volume_list" % (self._id, ), 0, -1)
        return [Volume(volume_id=volume_id) for volume_id in volume_ids]

    def addVolume(self, volumes):
        volume_ids = map(lambda tmp: tmp.getId(), volumes)
        self.getDao().composite_comics.rpush("comics:%d:volume_list" % (self._id, ), volume_ids)

    def deleteVolume(self, delete_ids):
        volume_ids = self.getDao().composite_comics.lrange("comics:%d:volume_list" % (self._id, ), 0, -1)
        rest_set = set(volume_ids) - set(delete_ids)
        #TODO
        #improve the performance
        rest_ids = [volume_id in rest_set for volume_id in volume_ids]
        self.getDao().composite_comics.delete("comics:%d:volume_list" % (self._id, ))
        self.getDao().composite_comics.rpush("comics:%d:volume_list" % (self._id, ), rest_ids)

    def save(self, meta):
        meta["create_time"] = int(time.time())
        #TODO
        #convert uploader_id to uploader
        self.meta = meta
