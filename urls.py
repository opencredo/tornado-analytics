# -*- coding: utf-8 -*-

from handlers import web_handlers
from handlers.base import GAuthLoginHandler, AuthLogoutHandler


url_patterns = [
    (r"/login-page", web_handlers.LoginPage),
    (r"/login", GAuthLoginHandler),
    (r"/logout", AuthLogoutHandler),
    (r"/", web_handlers.MainHandler),
    (r"/people-sources", web_handlers.PeopleSourcesHandler),
    (r"/top-countries", web_handlers.TopCountriesHandler),
    (r"/top-pages", web_handlers.TopPagesHandler),
    (r"/top-keywords", web_handlers.TopKeywordsHandler),
    (r"/total-users", web_handlers.TotalUsersHandler),
    (r"/referrers", web_handlers.ReferrersHandler),
    (r"/top-browser-n-os", web_handlers.TopBrowserAndOs),
    (r"/stats/fb-shares", web_handlers.FacebookGraph)

]