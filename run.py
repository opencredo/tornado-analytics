#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload

from tornado.options import options
import tornado.web
from utilities.cache import RedisCacheBackend
import redis

from settings import settings
from urls import url_patterns


class TornadoApplication(tornado.web.Application):
    def __init__(self):
        self.redis = redis.Redis()
        self.cache = RedisCacheBackend(self.redis)

        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    app = TornadoApplication()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()