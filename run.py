#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload

import tornado.web
from utilities.cache import RedisCacheBackend
import redis

from settings import settings
from urls import url_patterns
import yaml
import sys


class TornadoApplication(tornado.web.Application):
    def __init__(self):
        self.redis = redis.Redis()
        self.cache = RedisCacheBackend(self.redis)
        with open("app_conf.yaml", 'r') as stream:
            document = yaml.load(stream)

            # loading application settings
            try:
                settings["debug"] = document["applicationSettings"]["debug"]
                settings["app_port"] = document["applicationSettings"]["port"]
                settings["app_hostname"] = document["applicationSettings"]["hostname"]
                settings["google_redirect_url"] = 'http://%s:%s/login' % (document["applicationSettings"]['hostname'],
                                                                          document["applicationSettings"]['port'])
                settings["forks_per_cpu"] = document["applicationSettings"]["forksPerCPU"]

            except Exception as ex:
                print("Check your application settings: %s" % ex)
                sys.exit(1)

            # loading service account details
            try:
                settings["service_account_email"] = document["googleAnalyticsApi"]["serviceAccount"]
                settings["ga_profile_id"] = document["googleAnalyticsApi"]["profileId"]
                settings["start_days_ago"] = int(document["googleAnalyticsApi"]["startDaysAgo"])
                settings["website"] = document["googleAnalyticsApi"]["website"]
                key_file = document["googleAnalyticsApi"]["keyFileLocation"]
                if not key_file or key_file == '':
                    settings["key_file_location"] = None
                else:
                    settings["key_file_location"] = key_file

            except Exception as ex:
                print("Check your google service account details: %s" % ex)
                sys.exit(1)

            # loading google oauth details
            try:
                settings["google_oauth"] = dict(key=document["googleOAuth"]["key"],
                                                secret=document["googleOAuth"]["secret"])
                # allowed domain is optional - if it's missing, making it blank and allowing all domains
                try:
                    settings["allowed_domain"] = document["googleOAuth"]["allowedDomain"]
                except KeyError:
                    settings["allowed_domain"] = ''

            except Exception as ex:
                print("Check your googleOAuth details: %s" % ex)
                sys.exit(1)

            # get Salesforce details
            try:
                sf_data = document["salesForce"]
                for key, value in sf_data.items():
                    settings[key] = value

            except KeyError:
                print("Failed to get Salesforce login details, dashboard may not be available")

        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    app = TornadoApplication()
    http_server = tornado.httpserver.HTTPServer(app)

    # checking for debug mode
    if app.settings['debug']:
        http_server.listen(app.settings['app_port'])
        tornado.ioloop.IOLoop.instance().start()
    else:
        # when debugging is off - forking processes per CPU
        http_server.bind(app.settings['app_port'])
        http_server.start(app.settings['forks_per_cpu'])
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()