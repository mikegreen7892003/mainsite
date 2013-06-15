class Detail(object):
    def __init__(self, detail_id):
        super(Detail, self).__init__()
        self._detail_id = int(detail_id)

    @property
    def meta(self):
        if not hasattr(self, "_meta"):
            self._meta = dict(
                id=self._detail_id,
            )
        return self._meta

    @property
    def detail_id(self):
        return self._detail_id

    @property
    def image_meta(self):
        if not hasattr(self, "_image_meta"):
            pass
            self._image_meta = dict(
                id=self._detail_id,
            )
        return self._image_meta


class Comics(object):
    def __init__(self, detail_id):
        pass
