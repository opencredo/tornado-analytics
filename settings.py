# -*- coding: utf-8 -*-

import os.path

# seconds
CACHE_EXPIRES = 180

settings = {}

settings["cookie_secret"] = "askdfjpo83q47r9haskldfjh8"
settings["login_url"] = "/login-page"

settings["static_path"] = os.path.join(os.path.dirname(__file__), "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), "templates")
settings["xsrf_cookies"] = False
