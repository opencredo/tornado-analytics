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

Provide service account and profile_id in settings.py


# Authentication via Google

provide details for secure authentication in settings.py:
* google_oauth settings value should contain key with your Client ID (create a new client ID application) and secret with Client secret
* allowed_domain settings value should contain whitelisted domain, leave it blank to allow all domains.

# Details to query google API

* SERVICE_ACCOUNT settings value should contain email address of your service account that you created and gave rights
  to access your analytics.
* PROFILE_ID settings value contain your analytics profile ID to reduce query count.

Start the server
================

python run.py


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