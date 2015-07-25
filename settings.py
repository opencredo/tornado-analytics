# -*- coding: utf-8 -*-

import os.path

from tornado.options import define


define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")

settings = {}

settings["debug"] = True
settings["cookie_secret"] = "askdfjpo83q47r9haskldfjh8"
settings["login_url"] = "/login"
settings["static_path"] = os.path.join(os.path.dirname(__file__), "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), "templates")
settings["xsrf_cookies"] = False
settings["max_process_workers"] = 100
settings["service_account_email"] = '***REMOVED***'
# download client secrets file from your google developer console > auth > credentials
# settings["key_file_location"] = 'client_secrets2.p12'
