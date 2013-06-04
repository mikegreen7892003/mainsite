#!/usr/bin/python
#encoding=utf-8
import logging
import os.path
import tornado.web
import tornado.gen
from urlparse import urlparse
from tornado.options import define, options, parse_command_line, parse_config_file
from tornado.util import ObjectDict
from utils.config import Config
from utils.base import Base
from tornado.httpclient import AsyncHTTPClient

define("port", default=8888, help="run on the given port", type=int)
define("config_type", default="dev", help="config type")
define("config_file", default="localConfig.py", help="filename for additional configuration")


class BaseHandler(tornado.web.RequestHandler):
    pass


class TestHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine    
    def get(self):
        tmp = yield tornado.gen.Task(Base.dao.composite_comics.jset, "goat", {"nothing":"you"})
        logging.info(tmp)


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class ComicsDetailHandler(BaseHandler):
    def getDetailById(self, detail_id):
        return "%s?detail_id=%s" % (urlparse(self.request.uri).path, detail_id)

    def get(self):
        detail_id = self.get_argument('detail_id')
        image_meta = ObjectDict(dict(
            height=300,
            width=260,
            image_uri="/static/leo.jpg",
            pre_page=self.getDetailById(10),
            next_page=self.getDetailById(20),
        ))
        self.render("comics/detail.html", image_meta=image_meta)

def main():
    parse_command_line()
    Base.install()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/comics/detail", ComicsDetailHandler),
            (r"/test", TestHandler),
        ],
        cookie_secret="IloveYou",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
