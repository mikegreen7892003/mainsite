class Detail(object):
    def __init__(self, detail_id):
        self._detail_id = int(detail_id)

    @property
    def meta(self):
        if not hasattr(self, "_image_meta"):
            pass
            self._image_meta = dict(
                id=self._detail_id,
            )
        return self._image_meta

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

if __name__ == "__main__":
    pass

