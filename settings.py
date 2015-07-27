# -*- coding: utf-8 -*-

import os.path

from tornado.options import define

SERVICE_ACCOUNT = '***REMOVED***'
PROFILE_ID = '***REMOVED***'
# seconds
CACHE_EXPIRES = 180

# forks one process per cpu, only forks if debug mode is in False
FORKS_PER_CPU = 0
DEBUG = False

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")

settings = {}

settings["debug"] = DEBUG
settings["cookie_secret"] = "askdfjpo83q47r9haskldfjh8"
settings["login_url"] = "/login"
settings["static_path"] = os.path.join(os.path.dirname(__file__), "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), "templates")
settings["xsrf_cookies"] = False

# google API related settings - your account, don't forget to add it to your analytics users
settings["service_account_email"] = SERVICE_ACCOUNT
# provide profile ID to reduce queries.
settings["ga_profile_id"] = PROFILE_ID
