__author__ = 'karolisrusenas'

import tornado
from run import TornadoApplication

application = tornado.wsgi.WSGIAdapter(TornadoApplication)