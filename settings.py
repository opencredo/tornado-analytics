# -*- coding: utf-8 -*-

import os.path

from tornado.options import define

# Details for querying google analytics API
SERVICE_ACCOUNT = '***REMOVED***'
PROFILE_ID = '***REMOVED***'
# seconds
CACHE_EXPIRES = 180

# forks one process per cpu, only forks if debug mode is in False
FORKS_PER_CPU = 0
DEBUG = True

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")

HOSTNAME = 'localhost'
PORT = '8888'
# this is where google provides code token, change according to your domain
google_redirect_url = 'http://%s:%s/login' % (HOSTNAME, PORT)

settings = {}

settings["debug"] = DEBUG

settings["cookie_secret"] = "askdfjpo83q47r9haskldfjh8"
settings["login_url"] = "/login-page"

settings["static_path"] = os.path.join(os.path.dirname(__file__), "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), "templates")
settings["xsrf_cookies"] = False

# google API related settings - your account, don't forget to add it to your analytics users
settings["service_account_email"] = SERVICE_ACCOUNT
# provide profile ID to reduce queries.
settings["ga_profile_id"] = PROFILE_ID
# ============= CLIENT ID ===============
# application credentials from APIs & auth > credentials > Client ID for native application
# key represents "Client ID", secret is "Client secret". Oauth module expects to find "google_oauth" in app settings
settings["google_oauth"] = dict(key='***REMOVED***',
                                secret='***REMOVED***')
settings["allowed_domain"] = 'opencredo.com'
