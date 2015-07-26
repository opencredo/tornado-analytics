# -*- coding: utf-8 -*-

from handlers import web_handlers


url_patterns = [
    (r"/", web_handlers.MainHandler),
    (r"/people-sources", web_handlers.PeopleSourcesHandler),
    (r"/top-countries", web_handlers.TopCountriesHandler),
    (r"/top-pages", web_handlers.TopPagesHandler),
]