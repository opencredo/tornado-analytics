===================
Tornado G Analytics
===================

This is a tornado application that queries Google analytics v3 API

Installation
============

Check out the sources and install the requirements::

python setup.py install

Install Redis for caching or add another caching class in utilities/cache.py and inherit it in base handler
(handlers/base.py).

Configuration
=============

Configure additional requests/second for your project in google developer console:
https://developers.google.com/analytics/devguides/reporting/mcf/v3/limits-quotas

Set Per-user limit to more than 1.

**Rename app_conf.yaml.example to app_conf.yaml**

Then, use this file for configuration:

* applicationSettings - these options are used for callbacks as well as server startup. For local development
  leave them as is.

* googleAnalyticsApi - in your google developer console go to APIs & auth > credentials and create new service account.
  Your profileId is your google analytics profile ID.

* Download client_secrets '.p12' file and add it to "utilities" or specify path to this file in config:
  keyFileLocation: '/Users/your_username/Projects/keys/client_secrets_real.p12'

* googleOAuth - key value should contain key with your Client ID (Client ID for native application) and secret - Client secret
* allowedDomain value should contain whitelisted domain, leave it blank ('') to allow all domains.


Start the server
================

python run.py


Deploying on OpenShift
======================

* Create new application specifying this repo.
* WHen creating native client application through google developer console - specify web application and input your full
  application name (with your domain, i.e. http://analytics-rusenask.rhcloud.com/login )
* Checkout your newly created OpenShift repo and modify app_config.yaml, you can skip host, port settings since they will
  be overwritten by OpenShift environment variables anyway.
  Download your serivce account's p12 key, add it to utilities folder, commit it and push it to that OpenShift repo as well.
* Add redis to your application: rhc add-cartridge http://cartreflect-claytondev.rhcloud.com/reflect?github=smarterclayton/openshift-redis-cart

* Restart your application: rhc app-restart __your_app_name__

Troubleshooting OpenShift app
=============================

* SSH into your application: rhc ssh __your_app_name__
* Check logs in app-root/logs/python.log
* you can modify code, add additional debugging information in /app-root/repo/

Adding new tables
=================

* Define your new query in utilities/gaclient.py
  Use https://developers.google.com/apis-explorer/#p/ to test your queries
  You can inherit or just edit GAcess class with your additional function, it should return raw response from google
  API.
* Define a tornado handler in handlers/web_handlers.py. Use @unblock decorator to make calls asynchronous since
  google API is a blocking operation (at the time of writing this application there were no non-blocking clients or
  libraries available). This handler should return "render_to_string" since @unblock decorator writes whole response
  and returns it to client:
  return self.render_string('webhandler/data_table.html',
                                      data=data,
                                      table_title=table_title,
                                      headers=headers)
  here:  data - is what populates rows
         table_title - surprisingly it names the table
         headers - populates table headers
* Define your handler in urls.py
* Add your table div in templates/index.html, then, in js section add loading div function all:
  loaddiv('#__your_created_div', '/your-new-url-to-data-table');


Style
=====

For style this application uses https://almsaeedstudio.com/AdminLTE template, feel free to change base template and
static css files to improve it or ruin it.


TODO
====

* logging
* testing
* custom views