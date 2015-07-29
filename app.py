import os

try:
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    exec(compile(open(zvirtenv ).read(), zvirtenv, 'exec'), dict(__file__ = zvirtenv))
except IOError:
    pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#


from utilities.cache import RedisCacheBackend
import redis

import tornado
from run import TornadoApplication
if __name__ == '__main__':
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])

    app = TornadoApplication()
    # overriding default redis settings with openshift ones.
    app.redis = redis.Redis(host=os.environ['OPENSHIFT_REDIS_HOST'], port=os.environ['OPENSHIFT_REDIS_PORT'], password=os.environ['REDIS_PASSWORD'])
    app.cache = RedisCacheBackend(app.redis)

    # overriding google oauth callback url
    app.settings['google_redirect_url'] = 'http://%s/login' % os.environ['OPENSHIFT_APP_DNS']

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port=port, address=ip)

    tornado.ioloop.IOLoop.instance().start()