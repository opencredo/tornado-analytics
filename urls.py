# -*- coding: utf-8 -*-

from handlers import web_handlers


url_patterns = [
    (r"/", web_handlers.MainHandler),
    (r"/people-sources", web_handlers.PeopleSourcesHandler),
]