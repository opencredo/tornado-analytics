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
* Add your table in templates/index.html (include table's URL and create a <div> with ID so it can load your new
  table into that div.